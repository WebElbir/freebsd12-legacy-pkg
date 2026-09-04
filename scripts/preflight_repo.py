#!/usr/bin/env python3
"""Metadata-only safety preflight for one FreeBSD package repository target.

This command downloads repository catalog metadata only. It does not download
package payloads, create ABI repository trees, stage files, commit, or push.
It estimates the package payload implied by the requested roots and their
runtime dependency closures before a full build is allowed to run.
"""
from __future__ import annotations

import argparse
import json
import sys

import build_repo as core
import build_repo_cohorts as cohorts

MAX_FILE_BYTES = 95 * 1024 * 1024
MAX_TARGET_BYTES = 256 * 1024 * 1024


def package_size(candidate):
    row = candidate.get("r") or {}
    for key in ("pkgsize", "size"):
        value = row.get(key)
        try:
            value = int(value)
        except (TypeError, ValueError):
            continue
        if value >= 0:
            return value
    return None


def estimate_group(source_id, priority, group):
    known_bytes = 0
    unknown = []
    oversized = []
    largest = None

    for name, candidate in sorted(group["selected"].items()):
        size = package_size(candidate)
        if size is None:
            unknown.append(name)
            continue
        known_bytes += size
        if largest is None or size > largest[1]:
            largest = (name, size)
        if size > MAX_FILE_BYTES:
            oversized.append({"name": name, "bytes": size})

    return {
        "id": cohorts.safe_id(source_id),
        "source_id": source_id,
        "priority": priority,
        "roots": sorted(group["roots"]),
        "root_count": len(group["roots"]),
        "package_count": len(group["selected"]),
        "known_package_bytes": known_bytes,
        "unknown_package_size_count": len(unknown),
        "unknown_package_sizes": unknown,
        "largest_known_package": None if largest is None else {
            "name": largest[0],
            "bytes": largest[1],
        },
        "oversized_packages": oversized,
    }


def preflight(target: str):
    cfg = core.jload(core.ROOT / "config/roots.json")
    targets = core.jload(core.ROOT / "config/sources.json")["targets"]
    if target not in targets:
        raise RuntimeError("unknown target: " + target)

    sources = targets[target]
    if not sources:
        return {
            "target": target,
            "status": "no-verified-source",
            "safe_to_attempt_full_build": False,
            "reason": "No verified source is configured for this target.",
            "cohorts": [],
        }

    session = core.session()
    covered = set()
    discovered = set()
    source_stats = []
    reports = []
    unresolved = {}

    for priority, src in enumerate(sources):
        rows = core.remote_catalog(session, src, target, priority)
        for candidate in rows:
            candidate["target"] = target

        source_stats.append({
            "id": src["id"],
            "url": src.get("url"),
            "records": len(rows),
        })
        if not rows:
            continue

        byname, root_names = cohorts.root_candidates(rows, cfg)
        discovered.update(root_names)
        new_names = [name for name in root_names if name not in covered]
        closure_items = []

        for name in new_names:
            root_candidate, closure, notes = cohorts.closure_for_root(name, byname)
            if closure is None:
                unresolved.setdefault(name, []).append({
                    "source": src["id"],
                    "reason": "incomplete runtime closure in this source",
                    "attempts": notes,
                })
                continue
            closure_items.append((name, root_candidate, closure, notes))

        for group_index, group in enumerate(cohorts.group_closures(closure_items), 1):
            report = estimate_group(src["id"], priority, group)
            if group_index > 1:
                report["id"] = cohorts.safe_id(f"{src['id']}-{group_index}")
            reports.append(report)
            covered.update(group["roots"])

    if not reports:
        return {
            "target": target,
            "status": "no-requested-packages-resolved",
            "safe_to_attempt_full_build": False,
            "sources": source_stats,
            "cohorts": [],
            "discovered_roots": sorted(discovered),
            "unresolved": unresolved,
        }

    best = max(reports, key=lambda item: (
        item["root_count"], item["package_count"], -item["priority"]
    ))

    # A full build stores every cohort under repos/ and copies the best cohort
    # to latest/. Count latest/ again deliberately: this is a conservative
    # working-tree estimate before Git's object de-duplication.
    known_bytes = sum(item["known_package_bytes"] for item in reports)
    known_bytes += best["known_package_bytes"]
    unknown_count = sum(item["unknown_package_size_count"] for item in reports)
    unknown_count += best["unknown_package_size_count"]
    oversized = [
        {"cohort": item["id"], **pkg}
        for item in reports
        for pkg in item["oversized_packages"]
    ]

    reasons = []
    if oversized:
        reasons.append("one or more packages exceed the 95 MiB Git safety ceiling")
    if known_bytes > MAX_TARGET_BYTES:
        reasons.append("known package payload exceeds the 256 MiB per-run safety ceiling")
    if unknown_count:
        reasons.append("some package sizes are absent from upstream metadata; full build still requires the exact post-build safety gate")

    hard_block = bool(oversized) or known_bytes > MAX_TARGET_BYTES
    exact_requested = set(cfg.get("exact", []))

    return {
        "target": target,
        "status": "blocked-by-size-policy" if hard_block else "preflight-ok",
        "safe_to_attempt_full_build": not hard_block,
        "policy": {
            "max_single_file_bytes": MAX_FILE_BYTES,
            "max_target_worktree_bytes": MAX_TARGET_BYTES,
            "note": "Estimate includes the best cohort twice because latest/ is a copy of that cohort.",
        },
        "source_count": len(sources),
        "sources": source_stats,
        "cohort_count": len(reports),
        "covered_root_count": len(covered),
        "discovered_root_count": len(discovered),
        "known_package_bytes_conservative": known_bytes,
        "unknown_package_size_count_conservative": unknown_count,
        "oversized_packages": oversized,
        "reasons": reasons,
        "best_cohort": best["id"],
        "cohorts": reports,
        "unresolved_root_names": sorted(discovered - covered),
        "unresolved": unresolved,
        "exact_names_not_seen_in_any_source": sorted(exact_requested - discovered),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    ns = parser.parse_args()
    try:
        report = preflight(ns.target)
    except Exception as exc:
        print("ERROR", exc, file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report.get("safe_to_attempt_full_build") else 20


if __name__ == "__main__":
    raise SystemExit(main())
