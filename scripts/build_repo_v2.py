#!/usr/bin/env python3
"""Runtime-coherent selector layered on top of build_repo.py.

The first importer deliberately preserved exact dependency versions from source
catalogues. That is useful for audit, but a union repository can contain only
one active package record per package name. This selector treats the version
stored in a pkg dependency as provenance, then chooses one dependency candidate
that best satisfies the shared-library (SONAME) requirements of all parents.
If no single selected set can provide a package-managed required SONAME, the
build fails instead of publishing a silently broken repository.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import build_repo as core


def _strset(c, key):
    v = c["r"].get(key) or []
    if isinstance(v, dict):
        return {str(x) for x in v}
    if isinstance(v, (list, tuple, set)):
        return {str(x) for x in v}
    return set()


def shreq(c):
    return _strset(c, "shlibs_required") | _strset(c, "shlibs")


def shprov(c):
    return _strset(c, "shlibs_provided")


def version_key(v):
    out = []
    for token in re.findall(r"\d+|[A-Za-z]+|[^A-Za-z0-9]+", str(v)):
        if token.isdigit(): out.append((2, int(token)))
        elif token.isalpha(): out.append((1, token.lower()))
        else: out.append((0, token))
    return tuple(out)


def local12_v2(target, priority):
    candidates = []
    old_all = core.ROOT / "All"
    old_cat = next((core.ROOT / x for x in ("packagesite.pkg", "packagesite.txz") if (core.ROOT / x).exists()), None)
    if old_all.is_dir() and old_cat:
        candidates.append((old_all, old_cat))
    new_root = core.ROOT / target / "latest"
    new_all = new_root / "All"
    new_cat = next((new_root / x for x in ("packagesite.pkg", "packagesite.txz") if (new_root / x).exists()), None)
    if new_all.is_dir() and new_cat:
        candidates.append((new_all, new_cat))
    seen, good = set(), []
    for package_dir, cat in candidates:
        try:
            rows = core.parse_catalog(cat.read_bytes(), cat.name, "local-existing-12", target, priority, None, True)
        except Exception as e:
            print(target, "WARN local catalogue unreadable", cat, type(e).__name__)
            continue
        for c in rows:
            c["target"] = target
            key = (c["name"], c["version"])
            if key in seen: continue
            f = package_dir / Path(core.relpath(c)).name
            if not f.exists(): continue
            expected = core.normsum(c["r"].get("sum")); got = core.sha256(f)
            if expected and got != expected:
                print(target, "WARN bad local checksum", f.name); continue
            c["local_file"] = str(f); good.append(c); seen.add(key)
    print(target, "verified reusable FreeBSD 12 packages", len(good))
    return good


def _candidate_score(c, parents):
    provided = shprov(c)
    runtime_coverage = sum(len(provided & shreq(parent)) for parent, _ in parents)
    exact_provenance = sum(1 for _, wanted in parents if wanted and c["version"] == wanted)
    same_snapshot = sum(1 for parent, _ in parents if c["source"] == parent["source"])
    return (runtime_coverage, same_snapshot, exact_provenance, version_key(c["version"]), -int(c["priority"]))


def _runtime_validation(selected, all_rows):
    known_providers = defaultdict(list)
    for c in all_rows:
        for lib in shprov(c): known_providers[lib].append(c)
    provided = set()
    for c in selected.values(): provided |= shprov(c)
    missing = defaultdict(list)
    for c in selected.values():
        for lib in shreq(c):
            if lib in known_providers and lib not in provided: missing[lib].append(c)
    report = []
    for lib, parents in sorted(missing.items()):
        report.append({"soname": lib,
                       "required_by": sorted({p["name"] + "-" + p["version"] for p in parents}),
                       "available_providers": sorted({p["name"] + "-" + p["version"] + "@" + p["source"] for p in known_providers[lib]})})
    return report


def select_v2(rows, cfg):
    byname = defaultdict(list)
    for c in rows: byname[c["name"]].append(c)
    requested = {n for n in byname if core.is_root(n, cfg)} | set(cfg.get("exact", []))
    gcc = cfg["families"]["gcc"]
    if gcc.get("include_generic"): requested.add(gcc.get("generic_name", "gcc"))
    roots, root_selected = [], {}
    for name in sorted(requested):
        opts = core.ordered(byname.get(name, []))
        if not opts:
            roots.append({"name": name, "status": "unresolved", "attempts": []}); continue
        c = opts[0]; root_selected[name] = c
        roots.append({"name": name, "status": "selected", "version": c["version"], "source": c["source"]})
    selected, version_notes = dict(root_selected), []
    for _ in range(64):
        requirements = defaultdict(list); unresolved_deps = []
        for parent in selected.values():
            for dep_name, wanted_version in core.deps(parent):
                requirements[dep_name].append((parent, wanted_version))
                if dep_name not in byname:
                    unresolved_deps.append({"package": dep_name, "required_by": parent["name"], "required_version": wanted_version})
        if unresolved_deps:
            raise RuntimeError("unresolved runtime dependencies: " + json.dumps(unresolved_deps[:20], sort_keys=True))
        new_selected = dict(root_selected); notes = []
        for dep_name, parents in requirements.items():
            if dep_name in root_selected:
                chosen = root_selected[dep_name]
            else:
                opts = byname.get(dep_name, [])
                if not opts: continue
                chosen = max(opts, key=lambda c: _candidate_score(c, parents)); new_selected[dep_name] = chosen
            wanted = sorted({v for _, v in parents if v})
            if wanted and (len(wanted) > 1 or chosen["version"] not in wanted):
                notes.append({"package": dep_name, "selected": chosen["version"], "historical_versions": wanted,
                              "reason": "union repo selected one runtime candidate; dependency version is provenance, SONAME validation is authoritative"})
        old_sig = {(n,c["version"],c["source"]) for n,c in selected.items()}; new_sig = {(n,c["version"],c["source"]) for n,c in new_selected.items()}
        selected, version_notes = new_selected, notes
        if new_sig == old_sig: break
    else:
        raise RuntimeError("dependency closure did not stabilize")
    missing = _runtime_validation(selected, rows)
    if missing:
        raise RuntimeError("runtime SONAME incompatibility: " + json.dumps(missing[:30], sort_keys=True))
    return selected, roots, version_notes


core.local12 = local12_v2
core.select = select_v2

if __name__ == "__main__":
    raise SystemExit(core.main())
