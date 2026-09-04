#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main"


def conf(url: str):
    return f'''```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {{
  url: "{url}",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}}
EOF
pkg update -f
```
'''


def render(target: str):
    key = target.replace(":", "-")
    manifest = ROOT / "MANIFESTS" / f"{key}.json"
    if not manifest.is_file():
        return
    data = json.loads(manifest.read_text(encoding="utf-8"))
    outdir = ROOT / "CONFIGS"
    outdir.mkdir(exist_ok=True)
    out = outdir / f"{key}.md"

    lines = [f"# {target} pkg conf rehberi", ""]
    status = data.get("status", "unknown")
    lines += [f"Durum: **{status}**", ""]
    if status == "no-verified-source":
        lines += ["Bu ABI için doğrulanmış binary kaynak yoktur; sahte repository URL'si üretilmez.", ""]
        out.write_text("\n".join(lines), encoding="utf-8")
        return

    latest = data.get("latest_cohort")
    if latest:
        lines += ["## Ortak / varsayılan `latest`", "",
                  f"Bu yol en geniş tek ve kendi içinde uyumlu cohort olan `{latest}` deposunu gösterir.", "",
                  conf(f"{BASE}/{target}/latest")]

    coverage = data.get("coverage", {})
    if coverage:
        lines += ["## Paket → cohort haritası", "",
                  "Tarihsel MySQL/MariaDB/GCC sürümü `latest` içinde görünmüyorsa aşağıdaki cohort'u kullanın.", "",
                  "| Root paket | Cohort |", "|---|---|"]
        for pkg, cohort in sorted(coverage.items()):
            lines.append(f"| `{pkg}` | `{cohort}` |")
        lines.append("")

    for cohort in data.get("cohorts", []):
        cid = cohort["id"]
        roots = ", ".join(f"`{x}`" for x in cohort.get("roots", [])) or "-"
        lines += [f"## Cohort: `{cid}`", "", f"Root paketler: {roots}", "",
                  conf(f"{BASE}/{target}/repos/{cid}")]

    out.write_text("\n".join(lines), encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--target", required=True)
    ns = p.parse_args()
    render(ns.target)


if __name__ == "__main__":
    main()
