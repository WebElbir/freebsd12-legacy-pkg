# FreeBSD:12:amd64 pkg conf rehberi

Durum: **ok**

## Ortak / varsayılan `latest`

Bu yol en geniş tek ve kendi içinde uyumlu cohort olan `local-existing-12` deposunu gösterir.

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:12:amd64/latest",
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
| `boost-all` | `local-existing-12` |
| `compat11x-amd64` | `local-existing-12` |
| `compat12x-amd64` | `local-existing-12` |
| `compat7x-amd64` | `local-existing-12` |
| `compat8x-amd64` | `local-existing-12` |
| `compat9x-amd64` | `local-existing-12` |
| `cryptopp` | `local-existing-12` |
| `devil` | `local-existing-12` |
| `freecolor` | `local-existing-12` |
| `gcc` | `local-existing-12` |
| `gcc10` | `local-existing-12` |
| `gcc11` | `local-existing-12` |
| `gcc12` | `local-existing-12` |
| `gcc13` | `local-existing-12` |
| `gcc48` | `local-existing-12` |
| `gcc8` | `local-existing-12` |
| `gcc9` | `local-existing-12` |
| `gdb` | `local-existing-12` |
| `gmake` | `local-existing-12` |
| `makedepend` | `local-existing-12` |
| `mariadb1011-client` | `local-existing-12` |
| `mariadb1011-server` | `local-existing-12` |
| `mariadb103-client` | `local-existing-12` |
| `mariadb103-server` | `local-existing-12` |
| `mariadb104-client` | `local-existing-12` |
| `mariadb104-server` | `local-existing-12` |
| `mariadb105-client` | `local-existing-12` |
| `mariadb105-server` | `local-existing-12` |
| `mariadb106-client` | `local-existing-12` |
| `mariadb106-server` | `local-existing-12` |
| `mysql55-client` | `local-existing-12` |
| `mysql55-server` | `local-existing-12` |
| `mysql56-client` | `local-existing-12` |
| `mysql56-server` | `local-existing-12` |
| `mysql57-client` | `local-existing-12` |
| `mysql57-server` | `local-existing-12` |
| `mysql80-client` | `local-existing-12` |
| `mysql80-server` | `local-existing-12` |
| `mysql81-client` | `local-existing-12` |
| `mysql81-server` | `local-existing-12` |
| `nano` | `local-existing-12` |
| `python` | `local-existing-12` |
| `screen` | `local-existing-12` |
| `subversion` | `local-existing-12` |

## Cohort: `local-existing-12`

Root paketler: `boost-all`, `compat11x-amd64`, `compat12x-amd64`, `compat7x-amd64`, `compat8x-amd64`, `compat9x-amd64`, `cryptopp`, `devil`, `freecolor`, `gcc`, `gcc10`, `gcc11`, `gcc12`, `gcc13`, `gcc48`, `gcc8`, `gcc9`, `gdb`, `gmake`, `makedepend`, `mariadb1011-client`, `mariadb1011-server`, `mariadb103-client`, `mariadb103-server`, `mariadb104-client`, `mariadb104-server`, `mariadb105-client`, `mariadb105-server`, `mariadb106-client`, `mariadb106-server`, `mysql55-client`, `mysql55-server`, `mysql56-client`, `mysql56-server`, `mysql57-client`, `mysql57-server`, `mysql80-client`, `mysql80-server`, `mysql81-client`, `mysql81-server`, `nano`, `python`, `screen`, `subversion`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:12:amd64/repos/local-existing-12",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```
