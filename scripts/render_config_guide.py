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

    status = data.get("status", "unknown")
    latest = data.get("latest_cohort")
    canonical = f"{BASE}/{target}/latest"

    lines = [
        f"# {target} pkg conf rehberi",
        "",
        f"Durum: **{status}**",
        "",
        "## Canonical repository",
        "",
        "Bu ABI için kullanıcıya verilecek tek varsayılan repository biçimi aşağıdaki `raw.githubusercontent.com/.../${ABI}/latest` yapısıdır.",
        "GitHub Release URL'leri pkg repository adresi olarak kullanılmaz.",
        "",
        conf(canonical),
    ]

    if latest:
        lines += [
            f"Aktif `latest` cohort: `{latest}`.",
            "",
        ]
    elif status in {"no-verified-source", "no-requested-packages-resolved"}:
        lines += [
            "Bu ABI için doğrulanmış paket kaynağı bulunmadığından endpoint geçerli fakat bilinçli olarak boş bir pkg repository'dir.",
            "Başka FreeBSD major/mimariden paket kopyalanmaz.",
            "",
        ]
    elif status == "sync-failed-preserved-latest":
        lines += [
            "Son senkron sırasında kaynak cohort yeniden üretilemedi; daha önce doğrulanmış `latest` repository korunmuştur.",
            "",
        ]

    coverage = data.get("coverage", {})
    if coverage:
        lines += [
            "## Paket → kaynak cohort haritası",
            "",
            "Bu tablo provenance/uyumluluk bilgisidir. Kullanıcı tarafında repository URL'si yine yukarıdaki canonical `latest` adresidir.",
            "Aynı package adı için tarihsel sürümleri tek pkg kataloğunda zorla birleştirmiyoruz; pkg repository veritabanı package adını tekil ele alır ve eski snapshot bağımlılıkları yeni snapshotlarla ABI/SONAME çakışması yaratabilir.",
            "",
            "| Root paket | Kaynak cohort |",
            "|---|---|",
        ]
        for pkg, cohort in sorted(coverage.items()):
            lines.append(f"| `{pkg}` | `{cohort}` |")
        lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--target", required=True)
    ns = p.parse_args()
    render(ns.target)


if __name__ == "__main__":
    main()
