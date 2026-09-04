# FreeBSD:9:amd64 pkg conf rehberi

Durum: **ok**

## Ortak / varsayılan `latest`

Bu yol en geniş tek ve kendi içinde uyumlu cohort olan `pcbsd-92-gr` deposunu gösterir.

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:9:amd64/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```

## Paket → cohort haritası

Tarihsel MySQL/MariaDB/GCC sürümü `latest` içinde görünmüyorsa aşağıdaki cohort'u kullanın.

| Root paket | Cohort |
|---|---|
| `boost-all` | `pcbsd-92-gr` |
| `compat7x-amd64` | `pcbsd-92-gr` |
| `compat8x-amd64` | `pcbsd-92-gr` |
| `compat9x-amd64` | `pcbsd-92-gr` |
| `cryptopp` | `pcbsd-92-gr` |
| `devil` | `pcbsd-92-gr` |
| `gcc` | `pcbsd-92-gr` |
| `gcc48` | `pcbsd-92-gr` |
| `gcc49` | `pcbsd-92-gr` |
| `gdb` | `pcbsd-92-gr` |
| `gmake` | `pcbsd-92-gr` |
| `makedepend` | `pcbsd-92-gr` |
| `mysql55-client` | `pcbsd-92-gr` |
| `mysql55-server` | `pcbsd-92-gr` |
| `mysql56-client` | `pcbsd-92-gr` |
| `mysql56-server` | `pcbsd-92-gr` |
| `nano` | `pcbsd-92-gr` |
| `python` | `pcbsd-92-gr` |
| `screen` | `pcbsd-92-gr` |
| `subversion` | `pcbsd-92-gr` |

## Cohort: `pcbsd-92-gr`

Root paketler: `boost-all`, `compat7x-amd64`, `compat8x-amd64`, `compat9x-amd64`, `cryptopp`, `devil`, `gcc`, `gcc48`, `gcc49`, `gdb`, `gmake`, `makedepend`, `mysql55-client`, `mysql55-server`, `mysql56-client`, `mysql56-server`, `nano`, `python`, `screen`, `subversion`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:9:amd64/repos/pcbsd-92-gr",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```
