#!/usr/bin/env python3
"""Build installable FreeBSD package repositories as coherent source cohorts.

Historical FreeBSD snapshots cannot safely be flattened into one active pkg
catalog when old and new root packages need different versions of ICU, Boost,
OpenSSL, etc.  This builder therefore keeps each verified upstream snapshot as
an independent installable cohort and assigns every requested root package name
to the first cohort that contains its complete *exact* runtime dependency
closure.

`${ABI}/latest` is copied from the cohort with the broadest requested-root
coverage.  Historical package families stay available under
`${ABI}/repos/<cohort>` and are indexed in MANIFESTS/ plus CONFIGS/ guides.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import build_repo as core

ROOT = core.ROOT


def root_candidates(rows, cfg):
    byname = {}
    for c in rows:
        byname.setdefault(c["name"], []).append(c)
    return byname, sorted(n for n in byname if core.is_root(n, cfg))


def strict_resolve(c, byname, selected, stack, notes):
    """Resolve one root using only exact dependencies from one source catalog."""
    name = c["name"]
    if name in stack:
        return True
    if name in selected:
        if selected[name]["version"] != c["version"]:
            notes.append({
                "package": name,
                "selected": selected[name]["version"],
                "also_required": c["version"],
                "reason": "dependency version collision inside one cohort",
            })
            return False
        return True

    stack.add(name)
    for dep_name, wanted_version in core.deps(c):
        opts = byname.get(dep_name, [])
        if wanted_version:
            choices = [x for x in opts if x["version"] == wanted_version]
        else:
            choices = list(opts)
        if not choices:
            notes.append({
                "package": dep_name,
                "required_by": name,
                "required_version": wanted_version,
                "reason": "exact runtime dependency unavailable in this source",
            })
            stack.remove(name)
            return False
        chosen = core.ordered(choices)[0]
        if not strict_resolve(chosen, byname, selected, stack, notes):
            stack.remove(name)
            return False

    selected[name] = c
    stack.remove(name)
    return True


def closure_for_root(name, byname):
    attempts = []
    for c in core.ordered(byname.get(name, [])):
        selected, notes = {}, []
        if strict_resolve(c, byname, selected, set(), notes):
            return c, selected, notes
        attempts.append({
            "version": c["version"],
            "source": c["source"],
            "issues": notes[:20],
        })
    return None, None, attempts


def compatible(a, b):
    for name in set(a) & set(b):
        if a[name]["version"] != b[name]["version"]:
            return False
    return True


def group_closures(items):
    """Merge roots only when every overlapping dependency version agrees."""
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
        "dependency_notes": group["notes"],
    }, []


def publish_latest(target, cohort_report):
    latest = ROOT / target / "latest"
    if latest.exists():
        shutil.rmtree(latest)
    src = ROOT / cohort_report["path"]
    shutil.copytree(src, latest)
    return cohort_report["id"]


def remove_stale_target(target):
    target_dir = ROOT / target
    for name in ("latest", "repos"):
        p = target_dir / name
        if p.exists():
            shutil.rmtree(p)


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
        remove_stale_target(target)
        write_json(manifest_dir / f"{key}.json", {
            "target": target,
            "status": "no-verified-source",
            "cohorts": [],
            "coverage": {},
        })
        print(target, "no verified source; no fake URL used")
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
                    "reason": "incomplete exact runtime closure",
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
        remove_stale_target(target)
        write_json(manifest_dir / f"{key}.json", {
            "target": target,
            "status": "no-requested-packages-resolved",
            "cohorts": [],
            "coverage": {},
            "discovered_roots": sorted(discovered),
            "unresolved": unresolved,
        })
        raise RuntimeError(target + ": no complete requested package cohort could be built")

    best = max(cohorts, key=lambda c: (c["root_count"], c["package_count"], -c["priority"]))
    latest_id = publish_latest(target, best)

    keep = {c["id"] for c in cohorts}
    if repos_root.is_dir():
        for p in repos_root.iterdir():
            if p.is_dir() and p.name not in keep:
                shutil.rmtree(p)

    report = {
        "target": target,
        "status": "ok",
        "latest_cohort": latest_id,
        "cohort_count": len(cohorts),
        "covered_root_count": len(covered),
        "discovered_root_count": len(discovered),
        "coverage": dict(sorted(coverage.items())),
        "cohorts": [{k: v for k, v in c.items() if k != "packages"} for c in cohorts],
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
    for c in cohorts:
        write_json(detail_dir / f"{c['id']}.json", c)

    if migrate and target == "FreeBSD:12:amd64":
        clean_legacy_root12()

    print(target, "DONE", len(cohorts), "cohorts", len(covered), "requested root names covered", "latest=", latest_id)


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
