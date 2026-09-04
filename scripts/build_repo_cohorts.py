#!/usr/bin/env python3
"""Build installable FreeBSD package repositories as coherent source cohorts.

Historical FreeBSD snapshots cannot safely be flattened into one active pkg
catalog when old and new root packages need different versions of ICU, Boost,
OpenSSL, etc. This builder keeps each verified upstream snapshot/mirror as an
independent installable cohort. Every requested root package name is assigned
to the first cohort that contains a complete runtime dependency closure.

Dependency version strings in pkg manifests are provenance, not hard solver
constraints. Inside one original source snapshot we therefore trust the version
of a dependency actually published by that same snapshot. We never use a
package from another snapshot or ABI to fill that closure.

`${ABI}/latest` is the canonical public pkg endpoint. It is copied from the
cohort with the broadest requested-root coverage. If an ABI has no verified
binary source, a valid empty repository is still emitted at `${ABI}/latest` so
that the canonical raw.githubusercontent.com URL never becomes a 404. The
manifest remains explicit that the ABI has no verified package source.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys

import build_repo as core

ROOT = core.ROOT


def root_candidates(rows, cfg):
    byname = {}
    for c in rows:
        byname.setdefault(c["name"], []).append(c)
    return byname, sorted(n for n in byname if core.is_root(n, cfg))


def closure_for_root(name, byname):
    """Resolve one root strictly inside the current source snapshot."""
    attempts = []
    for candidate in core.ordered(byname.get(name, [])):
        selected, notes = {}, []
        if core.resolve(candidate, byname, selected, notes, set()):
            return candidate, selected, notes
        attempts.append({
            "version": candidate["version"],
            "source": candidate["source"],
            "issues": notes[:20],
        })
    return None, None, attempts


def compatible(a, b):
    for name in set(a) & set(b):
        if a[name]["version"] != b[name]["version"]:
            return False
    return True


def group_closures(items):
    """Merge roots only when every overlapping selected dependency agrees."""
    groups = []
    for root_name, root_c, closure, notes in items:
        for group in groups:
            if compatible(group["selected"], closure):
                group["selected"].update(closure)
                group["roots"].append(root_name)
                group["root_candidates"][root_name] = root_c
                group["notes"].extend(notes)
                break
        else:
            groups.append({
                "selected": dict(closure),
                "roots": [root_name],
                "root_candidates": {root_name: root_c},
                "notes": list(notes),
            })
    return groups


def safe_id(value: str):
    return "".join(ch if ch.isalnum() or ch in "-_." else "-" for ch in value)


def build_group(session, target, cohort_id, group):
    repo = ROOT / target / "repos" / cohort_id
    if repo.exists():
        shutil.rmtree(repo)
    out = repo / "All"
    out.mkdir(parents=True, exist_ok=True)

    selected = group["selected"]
    root_set = set(group["roots"])
    info, errors = {}, []

    for index, name in enumerate(sorted(selected), 1):
        c = selected[name]
        try:
            package_path, digest = core.materialize(session, c, out)
            info[name] = {
                "filename": package_path.name,
                "sha256": digest,
                "size": package_path.stat().st_size,
                "version": c["version"],
                "source": c["source"],
                "role": "root" if name in root_set else "dependency",
            }
            print(target, cohort_id, f"{index}/{len(selected)}", name, c["version"])
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
        "dependency_version_notes": group["notes"],
    }, []


def publish_latest(target, cohort_report):
    latest = ROOT / target / "latest"
    if latest.exists():
        shutil.rmtree(latest)
    source_repo = ROOT / cohort_report["path"]
    shutil.copytree(source_repo, latest)
    return cohort_report["id"]


def publish_empty_latest(target, status, note):
    """Create a valid zero-package pkg repository instead of leaving a 404."""
    latest = ROOT / target / "latest"
    if latest.exists():
        shutil.rmtree(latest)
    latest.mkdir(parents=True, exist_ok=True)
    core.metadata(latest, {}, {})
    (latest / "SHA256SUMS").write_text("", encoding="utf-8")
    write_json(latest / "STATUS.json", {
        "target": target,
        "status": status,
        "note": note,
        "package_count": 0,
    })


def remove_stale_repos(target):
    repos = ROOT / target / "repos"
    if repos.exists():
        shutil.rmtree(repos)


def clean_legacy_root12():
    for directory in ("All", "Libs"):
        p = ROOT / directory
        if p.exists():
            shutil.rmtree(p)
    for filename in (
        "packagesite.pkg", "packagesite.txz", "data.pkg", "data.txz", "meta", "meta.conf",
        "meta.pkg", "meta.txz", "digests.txz", "SNAPSHOT_INFO.txt", "SHA256SUMS",
        "ROOTS_REQUESTED.txt",
    ):
        (ROOT / filename).unlink(missing_ok=True)


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build(target: str, migrate: bool):
    cfg = core.jload(ROOT / "config/roots.json")
    targets = core.jload(ROOT / "config/sources.json")["targets"]
    if target not in targets:
        raise RuntimeError("unknown target: " + target)
    sources = targets[target]

    manifest_dir = ROOT / "MANIFESTS"
    sources_dir = ROOT / "SOURCES"
    manifest_dir.mkdir(exist_ok=True)
    sources_dir.mkdir(exist_ok=True)
    key = target.replace(":", "-")

    if not sources:
        remove_stale_repos(target)
        publish_empty_latest(
            target,
            "no-verified-source",
            "No verified binary source is configured for this ABI. The canonical repository endpoint is intentionally valid but empty.",
        )
        write_json(manifest_dir / f"{key}.json", {
            "target": target,
            "status": "no-verified-source",
            "latest_cohort": None,
            "cohorts": [],
            "coverage": {},
            "canonical_repo": f"{target}/latest",
        })
        write_json(sources_dir / f"{key}.json", {"target": target, "sources": []})
        print(target, "no verified source; emitted valid empty canonical latest repo")
        return

    session = core.session()
    source_stats = []
    covered = set()
    discovered = set()
    coverage = {}
    cohorts = []
    unresolved = {}

    repos_root = ROOT / target / "repos"
    if repos_root.exists():
        shutil.rmtree(repos_root)

    for priority, src in enumerate(sources):
        rows = core.remote_catalog(session, src, target, priority)
        for c in rows:
            c["target"] = target
        source_stats.append({
            "id": src["id"],
            "url": src.get("url"),
            "records": len(rows),
        })
        if not rows:
            continue

        byname, root_names = root_candidates(rows, cfg)
        discovered.update(root_names)
        new_names = [name for name in root_names if name not in covered]
        if not new_names:
            print(target, src["id"], "no new requested root names")
            continue

        closure_items = []
        for name in new_names:
            root_c, closure, notes = closure_for_root(name, byname)
            if closure is None:
                unresolved.setdefault(name, []).append({
                    "source": src["id"],
                    "reason": "incomplete runtime closure in this source",
                    "attempts": notes,
                })
                continue
            closure_items.append((name, root_c, closure, notes))

        for group_index, group in enumerate(group_closures(closure_items), 1):
            suffix = "" if group_index == 1 else f"-{group_index}"
            cohort_id = safe_id(src["id"] + suffix)
            report, errors = build_group(session, target, cohort_id, group)
            if report is None:
                for name in group["roots"]:
                    unresolved.setdefault(name, []).append({
                        "source": src["id"],
                        "reason": "package download failed",
                        "errors": errors[:10],
                    })
                continue

            report["source_id"] = src["id"]
            report["source_url"] = src.get("url")
            report["priority"] = priority
            cohorts.append(report)
            for name in group["roots"]:
                covered.add(name)
                coverage[name] = cohort_id
            print(target, cohort_id, "DONE", report["root_count"], "roots", report["package_count"], "packages")

    write_json(sources_dir / f"{key}.json", {"target": target, "sources": source_stats})

    if not cohorts:
        existing_latest = ROOT / target / "latest"
        if existing_latest.is_dir() and (existing_latest / "packagesite.txz").is_file():
            status = "sync-failed-preserved-latest"
            note = "No source cohort could be rebuilt during this run; the previously published canonical latest repository was preserved."
        else:
            status = "no-requested-packages-resolved"
            note = "No requested package cohort could be resolved. The canonical repository endpoint is valid but empty."
            publish_empty_latest(target, status, note)
        remove_stale_repos(target)
        write_json(manifest_dir / f"{key}.json", {
            "target": target,
            "status": status,
            "cohorts": [],
            "coverage": {},
            "discovered_roots": sorted(discovered),
            "unresolved": unresolved,
            "canonical_repo": f"{target}/latest",
        })
        print(target, status, "canonical latest endpoint retained")
        return

    best = max(cohorts, key=lambda c: (c["root_count"], c["package_count"], -c["priority"]))
    latest_id = publish_latest(target, best)

    keep = {c["id"] for c in cohorts}
    if repos_root.is_dir():
        for p in repos_root.iterdir():
            if p.is_dir() and p.name not in keep:
                shutil.rmtree(p)

    unresolved_names = sorted(discovered - covered)
    report = {
        "target": target,
        "status": "ok" if not unresolved_names else "partial",
        "latest_cohort": latest_id,
        "canonical_repo": f"{target}/latest",
        "cohort_count": len(cohorts),
        "covered_root_count": len(covered),
        "discovered_root_count": len(discovered),
        "coverage": dict(sorted(coverage.items())),
        "cohorts": [{k: v for k, v in c.items() if k != "packages"} for c in cohorts],
        "unresolved_root_names": unresolved_names,
        "unresolved": unresolved,
        "exact_names_not_seen_in_any_source": sorted(
            name for name in cfg.get("exact", []) if name not in discovered
        ),
    }
    write_json(manifest_dir / f"{key}.json", report)

    detail_dir = manifest_dir / key
    if detail_dir.exists():
        shutil.rmtree(detail_dir)
    detail_dir.mkdir(parents=True, exist_ok=True)
    for cohort in cohorts:
        write_json(detail_dir / f"{cohort['id']}.json", cohort)

    if migrate and target == "FreeBSD:12:amd64":
        clean_legacy_root12()

    print(target, report["status"].upper(), len(cohorts), "cohorts", len(covered), "/", len(discovered), "requested root names covered", "latest=", latest_id)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--migrate-existing-12", action="store_true")
    ns = parser.parse_args()
    try:
        build(ns.target, ns.migrate_existing_12)
    except Exception as exc:
        print("ERROR", exc, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
