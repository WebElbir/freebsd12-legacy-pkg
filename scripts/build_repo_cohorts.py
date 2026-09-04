#!/usr/bin/env python3
"""Build runtime-coherent FreeBSD package repositories by source cohort.

Why cohorts exist:
A single pkg repository cannot safely mix historical snapshots when packages
with different root names require incompatible versions of a shared dependency
(e.g. ICU, Boost, OpenSSL).  Instead, each verified upstream snapshot/mirror is
kept as an installable cohort.  Every requested package name is assigned to the
first verified cohort that contains a complete runtime dependency closure.

The target's ``latest`` directory is a copy of the cohort with the broadest
requested-root coverage, so the simple ${ABI}/latest configuration remains
useful.  Historical package families remain available under
``${ABI}/repos/<cohort>`` and are indexed in MANIFESTS/*.json.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import build_repo as core

ROOT = core.ROOT
PKG_EXTS = {".pkg", ".txz", ".tbz", ".tgz", ".tzst"}


def local12_reusable(target: str, priority: int):
    """Reuse a previously published FreeBSD 12 amd64 repository as a source."""
    candidates = []
    old_all = ROOT / "All"
    old_cat = next((ROOT / x for x in ("packagesite.pkg", "packagesite.txz")
                    if (ROOT / x).exists()), None)
    if old_all.is_dir() and old_cat:
        candidates.append((old_all, old_cat))

    current = ROOT / target / "latest"
    cur_all = current / "All"
    cur_cat = next((current / x for x in ("packagesite.pkg", "packagesite.txz")
                    if (current / x).exists()), None)
    if cur_all.is_dir() and cur_cat:
        candidates.append((cur_all, cur_cat))

    out, seen = [], set()
    for package_dir, cat in candidates:
        try:
            rows = core.parse_catalog(cat.read_bytes(), cat.name, "local-existing-12",
                                      target, priority, None, True)
        except Exception as exc:
            print(target, "WARN local catalogue unreadable", cat, type(exc).__name__)
            continue
        for c in rows:
            c["target"] = target
            key = (c["name"], c["version"])
            if key in seen:
                continue
            f = package_dir / Path(core.relpath(c)).name
            if not f.is_file():
                continue
            expected = core.normsum(c["r"].get("sum"))
            got = core.sha256(f)
            if expected and got != expected:
                print(target, "WARN bad local checksum", f.name)
                continue
            c["local_file"] = str(f)
            out.append(c)
            seen.add(key)
    print(target, "verified reusable local packages", len(out))
    return out


def root_candidates(rows, cfg):
    byname = {}
    for c in rows:
        byname.setdefault(c["name"], []).append(c)
    return byname, sorted(n for n in byname if core.is_root(n, cfg))


def closure_for_candidate(c, byname):
    selected, conflicts = {}, []
    ok = core.resolve(c, byname, selected, conflicts, set())
    if not ok:
        return None, conflicts
    return selected, conflicts


def closure_for_root(name, byname):
    attempts = []
    for c in core.ordered(byname.get(name, [])):
        selected, conflicts = closure_for_candidate(c, byname)
        if selected is not None:
            return c, selected, conflicts
        attempts.append({"version": c["version"], "source": c["source"]})
    return None, None, attempts


def compatible(a, b):
    for name in set(a) & set(b):
        if a[name]["version"] != b[name]["version"]:
            return False
    return True


def group_closures(items):
    """Pack root closures together only when dependency versions agree."""
    groups = []
    for root_name, root_c, closure, conflicts in items:
        placed = False
        for g in groups:
            if compatible(g["selected"], closure):
                g["selected"].update(closure)
                g["roots"].append(root_name)
                g["root_candidates"][root_name] = root_c
                g["conflicts"].extend(conflicts)
                placed = True
                break
        if not placed:
            groups.append({
                "selected": dict(closure),
                "roots": [root_name],
                "root_candidates": {root_name: root_c},
                "conflicts": list(conflicts),
            })
    return groups


def safe_id(value: str):
    return "".join(ch if ch.isalnum() or ch in "-_." else "-" for ch in value)


def build_group(s, target, cohort_id, group, cfg):
    repo = ROOT / target / "repos" / cohort_id
    if repo.exists():
        shutil.rmtree(repo)
    out = repo / "All"
    out.mkdir(parents=True, exist_ok=True)

    info, errors = {}, []
    selected = group["selected"]
    root_set = set(group["roots"])
    for i, name in enumerate(sorted(selected), 1):
        c = selected[name]
        try:
            p, h = core.materialize(s, c, out)
            info[name] = {
                "filename": p.name,
                "sha256": h,
                "size": p.stat().st_size,
                "version": c["version"],
                "source": c["source"],
                "role": "root" if name in root_set else "dependency",
            }
            print(target, cohort_id, f"{i}/{len(selected)}", name, c["version"])
        except Exception as exc:
            errors.append({
                "name": name,
                "version": c["version"],
                "source": c["source"],
                "error": str(exc),
            })

    if errors:
        shutil.rmtree(repo, ignore_errors=True)
        return None, errors

    core.metadata(repo, selected, info)
    (repo / "SHA256SUMS").write_text(
        "".join(f"{x['sha256']}  All/{x['filename']}\n" for _, x in sorted(info.items())),
        encoding="utf-8",
    )
    return {
        "id": cohort_id,
        "path": f"{target}/repos/{cohort_id}",
        "roots": sorted(root_set),
        "root_count": len(root_set),
        "package_count": len(info),
        "packages": info,
        "dependency_version_notes": group["conflicts"],
    }, []


def publish_latest(target, cohort_report):
    latest = ROOT / target / "latest"
    if latest.exists():
        shutil.rmtree(latest)
    src = ROOT / cohort_report["path"]
    shutil.copytree(src, latest)
    return cohort_report["id"]


def clean_legacy_root12():
    for d in ("All", "Libs"):
        p = ROOT / d
        if p.exists():
            shutil.rmtree(p)
    for f in (
        "packagesite.pkg", "packagesite.txz", "data.pkg", "data.txz", "meta", "meta.conf",
        "meta.pkg", "meta.txz", "digests.txz", "SNAPSHOT_INFO.txt", "SHA256SUMS",
        "ROOTS_REQUESTED.txt",
    ):
        (ROOT / f).unlink(missing_ok=True)


def build(target: str, migrate: bool):
    cfg = core.jload(ROOT / "config/roots.json")
    all_sources = core.jload(ROOT / "config/sources.json")["targets"]
    if target not in all_sources:
        raise RuntimeError("unknown target: " + target)
    sources = all_sources[target]

    man_dir = ROOT / "MANIFESTS"
    src_dir = ROOT / "SOURCES"
    man_dir.mkdir(exist_ok=True)
    src_dir.mkdir(exist_ok=True)
    target_key = target.replace(":", "-")

    if not sources:
        report = {"target": target, "status": "no-verified-source", "cohorts": [], "coverage": {}}
        (man_dir / f"{target_key}.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(target, "no verified source; no fake URL used")
        return

    s = core.session()
    source_stats = []
    covered = set()
    discovered = set()
    coverage = {}
    cohorts = []
    unresolved = {}

    # Start clean.  We rebuild all cohorts deterministically from verified upstreams.
    repos_root = ROOT / target / "repos"
    if repos_root.exists():
        shutil.rmtree(repos_root)

    for priority, src in enumerate(sources):
        if src.get("type") == "local-existing":
            rows = local12_reusable(target, priority)
        else:
            rows = core.remote_catalog(s, src, target, priority)
        for c in rows:
            c["target"] = target
        source_stats.append({"id": src["id"], "url": src.get("url"), "records": len(rows)})
        if not rows:
            continue

        byname, root_names = root_candidates(rows, cfg)
        discovered.update(root_names)
        new_names = [n for n in root_names if n not in covered]
        if not new_names:
            print(target, src["id"], "no new requested root names")
            continue

        closure_items = []
        for name in new_names:
            root_c, closure, notes = closure_for_root(name, byname)
            if closure is None:
                unresolved.setdefault(name, []).append({"source": src["id"], "reason": "incomplete runtime closure", "detail": notes})
                continue
            closure_items.append((name, root_c, closure, notes))

        for idx, group in enumerate(group_closures(closure_items), 1):
            suffix = "" if idx == 1 else f"-{idx}"
            cohort_id = safe_id(src["id"] + suffix)
            report, errors = build_group(s, target, cohort_id, group, cfg)
            if report is None:
                for name in group["roots"]:
                    unresolved.setdefault(name, []).append({"source": src["id"], "reason": "package download failed", "errors": errors[:10]})
                continue
            report["source_id"] = src["id"]
            report["source_url"] = src.get("url")
            report["priority"] = priority
            cohorts.append(report)
            for name in group["roots"]:
                covered.add(name)
                coverage[name] = cohort_id
            print(target, cohort_id, "DONE", report["root_count"], "roots", report["package_count"], "packages")

    if not cohorts:
        report = {
            "target": target,
            "status": "no-requested-packages-resolved",
            "cohorts": [],
            "coverage": {},
            "discovered_roots": sorted(discovered),
            "unresolved": unresolved,
        }
        (man_dir / f"{target_key}.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (src_dir / f"{target_key}.json").write_text(json.dumps({"target": target, "sources": source_stats}, indent=2) + "\n", encoding="utf-8")
        raise RuntimeError(target + ": no complete requested package cohort could be built")

    # Broadest coherent cohort becomes the simple ${ABI}/latest endpoint.
    best = max(cohorts, key=lambda c: (c["root_count"], c["package_count"], -c["priority"]))
    latest_id = publish_latest(target, best)

    # Remove stale source cohort directories left by a previous generation if any.
    keep_dirs = {c["id"] for c in cohorts}
    if repos_root.is_dir():
        for p in repos_root.iterdir():
            if p.is_dir() and p.name not in keep_dirs:
                shutil.rmtree(p)

    exact_missing = sorted(n for n in cfg.get("exact", []) if n not in discovered)
    report = {
        "target": target,
        "status": "ok" if covered else "partial",
        "latest_cohort": latest_id,
        "cohort_count": len(cohorts),
        "covered_root_count": len(covered),
        "discovered_root_count": len(discovered),
        "coverage": dict(sorted(coverage.items())),
        "cohorts": [{k: v for k, v in c.items() if k != "packages"} for c in cohorts],
        "unresolved": unresolved,
        "exact_names_not_seen_in_any_source": exact_missing,
    }
    (man_dir / f"{target_key}.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (src_dir / f"{target_key}.json").write_text(json.dumps({"target": target, "sources": source_stats}, indent=2) + "\n", encoding="utf-8")

    # Store detailed per-cohort package manifests separately to keep the target index readable.
    detail_dir = man_dir / target_key
    if detail_dir.exists():
        shutil.rmtree(detail_dir)
    detail_dir.mkdir(parents=True, exist_ok=True)
    for c in cohorts:
        (detail_dir / f"{c['id']}.json").write_text(json.dumps(c, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if migrate and target == "FreeBSD:12:amd64":
        clean_legacy_root12()

    print(target, "DONE", len(cohorts), "cohorts", len(covered), "requested root names covered", "latest=", latest_id)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--target", required=True)
    p.add_argument("--migrate-existing-12", action="store_true")
    ns = p.parse_args()
    try:
        build(ns.target, ns.migrate_existing_12)
    except Exception as exc:
        print("ERROR", exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
