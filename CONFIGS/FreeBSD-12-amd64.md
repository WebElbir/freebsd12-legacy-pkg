# FreeBSD:12:amd64 pkg conf rehberi

Durum: **ok**

## Ortak / varsayılan `latest`

Bu yol en geniş tek ve kendi içinde uyumlu cohort olan `nepustil-121` deposunu gösterir.

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
| `boost-all` | `sggs-12-latest` |
| `compat11x-amd64` | `sggs-12-latest` |
| `compat12x-amd64` | `sggs-12-latest` |
| `compat7x-amd64` | `sggs-12-latest` |
| `compat8x-amd64` | `sggs-12-latest` |
| `compat9x-amd64` | `nepustil-121` |
| `cryptopp` | `nepustil-123` |
| `devil` | `sggs-12-latest` |
| `freecolor` | `sggs-12-latest` |
| `gcc` | `nepustil-121` |
| `gcc10` | `nepustil-121` |
| `gcc11` | `nepustil-123` |
| `gcc12` | `sggs-12-latest` |
| `gcc13` | `sggs-12-latest` |
| `gcc48` | `sggs-12-latest` |
| `gcc8` | `nepustil-121` |
| `gcc9` | `nepustil-121` |
| `gdb` | `nepustil-121` |
| `gmake` | `nepustil-121` |
| `makedepend` | `nepustil-121` |
| `mariadb1011-client` | `sggs-12-latest` |
| `mariadb1011-server` | `sggs-12-latest` |
| `mariadb104-client` | `nepustil-121` |
| `mariadb104-server` | `nepustil-121` |
| `mariadb105-client` | `nepustil-121` |
| `mariadb105-server` | `nepustil-121` |
| `mariadb106-client` | `sggs-12-latest` |
| `mariadb106-server` | `sggs-12-latest` |
| `mysql57-client` | `nepustil-121` |
| `mysql57-server` | `nepustil-121` |
| `mysql80-client` | `sggs-12-latest` |
| `mysql80-server` | `sggs-12-latest` |
| `mysql81-client` | `sggs-12-latest` |
| `mysql81-server` | `sggs-12-latest` |
| `nano` | `nepustil-121` |
| `python` | `nepustil-121` |
| `screen` | `nepustil-121` |
| `subversion` | `nepustil-121` |

## Cohort: `nepustil-121`

Root paketler: `compat9x-amd64`, `gcc`, `gcc10`, `gcc8`, `gcc9`, `gdb`, `gmake`, `makedepend`, `mariadb104-client`, `mariadb104-server`, `mariadb105-client`, `mariadb105-server`, `mysql57-client`, `mysql57-server`, `nano`, `python`, `screen`, `subversion`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:12:amd64/repos/nepustil-121",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```

## Cohort: `nepustil-123`

Root paketler: `cryptopp`, `gcc11`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:12:amd64/repos/nepustil-123",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```

## Cohort: `sggs-12-latest`

Root paketler: `boost-all`, `compat11x-amd64`, `compat12x-amd64`, `compat7x-amd64`, `compat8x-amd64`, `devil`, `freecolor`, `gcc12`, `gcc13`, `gcc48`, `mariadb1011-client`, `mariadb1011-server`, `mariadb106-client`, `mariadb106-server`, `mysql80-client`, `mysql80-server`, `mysql81-client`, `mysql81-server`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:12:amd64/repos/sggs-12-latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```
