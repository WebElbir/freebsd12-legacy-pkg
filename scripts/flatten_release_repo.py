#!/usr/bin/env python3
"""Prepare one built pkg cohort for GitHub Release asset hosting.

GitHub Release assets are flat. This helper copies package archives from All/
to a flat staging directory and rewrites packagesite.txz so package paths are
relative filenames at the release download root.
"""
from __future__ import annotations

import argparse
import io
import json
import shutil
import tarfile
from pathlib import Path

import build_repo as core


def extract_packagesite(path: Path) -> bytes:
    with tarfile.open(path, "r:xz") as tf:
        member = next((m for m in tf.getmembers() if Path(m.name).name == "packagesite.yaml"), None)
        if member is None:
            raise RuntimeError(f"packagesite.yaml missing in {path}")
        fh = tf.extractfile(member)
        if fh is None:
            raise RuntimeError(f"cannot read packagesite.yaml in {path}")
        return fh.read()


def rewrite_catalog(src: Path, dst: Path, package_dir: Path) -> tuple[int, list[str]]:
    payload = extract_packagesite(src)
    lines = []
    names = []
    for raw in payload.decode("utf-8", "replace").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        row = json.loads(raw)
        p = row.get("repopath") or row.get("path")
        if not p:
            raise RuntimeError(f"catalog entry has no package path: {row.get('name')}")
        filename = Path(str(p)).name
        if not (package_dir / filename).is_file():
            raise RuntimeError(f"catalog package missing: {filename}")
        row["path"] = filename
        row["repopath"] = filename
        lines.append(json.dumps(row, separators=(",", ":"), ensure_ascii=False))
        names.append(filename)
    data = ("\n".join(lines) + "\n").encode("utf-8")
    core.txz(dst, "packagesite.yaml", data)
    return len(lines), names


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="Built cohort directory containing All/ and packagesite.txz")
    ap.add_argument("--output", required=True, help="Flat staging directory for release assets")
    ns = ap.parse_args()

    repo = Path(ns.repo).resolve()
    out = Path(ns.output).resolve()
    all_dir = repo / "All"
    if not all_dir.is_dir() or not (repo / "packagesite.txz").is_file():
        raise RuntimeError(f"not a built cohort repository: {repo}")

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    package_files = sorted(p for p in all_dir.iterdir() if p.is_file())
    for p in package_files:
        shutil.copy2(p, out / p.name)

    entry_count, catalog_names = rewrite_catalog(repo / "packagesite.txz", out / "packagesite.txz", all_dir)
    missing = sorted(set(p.name for p in package_files) - set(catalog_names))
    if missing:
        raise RuntimeError("package files not represented by catalog: " + ", ".join(missing[:20]))

    for name in ("meta.conf", "meta", "meta.txz"):
        src = repo / name
        if src.is_file():
            shutil.copy2(src, out / name)

    sums = []
    for p in sorted(out.iterdir()):
        if p.is_file() and p.name != "SHA256SUMS":
            sums.append(f"{core.sha256(p)}  {p.name}\n")
    (out / "SHA256SUMS").write_text("".join(sums), encoding="utf-8")

    report = {
        "catalog_entries": entry_count,
        "package_assets": len(package_files),
        "release_asset_count": len([p for p in out.iterdir() if p.is_file()]),
        "total_bytes": sum(p.stat().st_size for p in out.iterdir() if p.is_file()),
        "largest_asset": max(
            ({"name": p.name, "bytes": p.stat().st_size} for p in out.iterdir() if p.is_file()),
            key=lambda x: x["bytes"],
        ),
    }
    (out / "RELEASE_INFO.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
