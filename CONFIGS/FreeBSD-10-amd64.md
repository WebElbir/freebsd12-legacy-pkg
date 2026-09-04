# FreeBSD:10:amd64 pkg conf rehberi

Durum: **ok**

## Ortak / varsayılan `latest`

Bu yol en geniş tek ve kendi içinde uyumlu cohort olan `sggs-10-latest` deposunu gösterir.

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:10:amd64/latest",
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
| `boost-all` | `sggs-10-latest` |
| `compat7x-amd64` | `sggs-10-latest` |
| `compat8x-amd64` | `sggs-10-latest` |
| `compat9x-amd64` | `sggs-10-latest` |
| `cryptopp` | `sggs-10-latest` |
| `devil` | `sggs-10-latest` |
| `freecolor` | `sggs-10-latest` |
| `gcc` | `sggs-10-latest` |
| `gcc48` | `sggs-10-latest` |
| `gcc49` | `sggs-10-latest` |
| `gcc5` | `sggs-10-latest` |
| `gcc6` | `sggs-10-latest` |
| `gcc7` | `sggs-10-latest` |
| `gcc8` | `sggs-10-latest` |
| `gdb` | `sggs-10-latest` |
| `gmake` | `sggs-10-latest` |
| `makedepend` | `sggs-10-latest` |
| `mariadb103-client` | `sggs-10-latest` |
| `mariadb103-server` | `sggs-10-latest` |
| `mysql55-client` | `sggs-10-latest` |
| `mysql55-server` | `sggs-10-latest` |
| `mysql56-client` | `sggs-10-latest` |
| `mysql56-server` | `sggs-10-latest` |
| `mysql57-client` | `sggs-10-latest` |
| `mysql57-server` | `sggs-10-latest` |
| `mysql80-client` | `sggs-10-latest` |
| `mysql80-server` | `sggs-10-latest` |
| `nano` | `sggs-10-latest` |
| `python` | `sggs-10-latest` |
| `screen` | `sggs-10-latest` |
| `subversion` | `sggs-10-latest` |

## Cohort: `sggs-10-latest`

Root paketler: `boost-all`, `compat7x-amd64`, `compat8x-amd64`, `compat9x-amd64`, `cryptopp`, `devil`, `freecolor`, `gcc`, `gcc48`, `gcc49`, `gcc5`, `gcc6`, `gcc7`, `gcc8`, `gdb`, `gmake`, `makedepend`, `mariadb103-client`, `mariadb103-server`, `mysql55-client`, `mysql55-server`, `mysql56-client`, `mysql56-server`, `mysql57-client`, `mysql57-server`, `mysql80-client`, `mysql80-server`, `nano`, `python`, `screen`, `subversion`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:10:amd64/repos/sggs-10-latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```
