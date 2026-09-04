# FreeBSD:11:amd64 pkg conf rehberi

Durum: **ok**

## Ortak / varsayılan `latest`

Bu yol en geniş tek ve kendi içinde uyumlu cohort olan `nepustil-112` deposunu gösterir.

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:11:amd64/latest",
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
| `boost-all` | `sggs-11-latest` |
| `compat11x-amd64` | `sggs-11-latest` |
| `compat7x-amd64` | `sggs-11-latest` |
| `compat8x-amd64` | `sggs-11-latest` |
| `compat9x-amd64` | `nepustil-112` |
| `cryptopp` | `sggs-11-latest` |
| `devil` | `sggs-11-latest` |
| `freecolor` | `sggs-11-latest` |
| `gcc` | `nepustil-112` |
| `gcc10` | `nepustil-114` |
| `gcc11` | `sggs-11-latest` |
| `gcc48` | `sggs-11-latest` |
| `gcc7` | `nepustil-112` |
| `gcc8` | `nepustil-113` |
| `gcc9` | `nepustil-113` |
| `gdb` | `nepustil-112` |
| `gmake` | `nepustil-112` |
| `makedepend` | `nepustil-112` |
| `mariadb103-client` | `sggs-11-latest` |
| `mariadb103-server` | `sggs-11-latest` |
| `mariadb104-client` | `nepustil-112` |
| `mariadb104-server` | `nepustil-112` |
| `mariadb105-client` | `nepustil-113` |
| `mariadb105-server` | `nepustil-113` |
| `mysql55-client` | `sggs-11-latest` |
| `mysql55-server` | `sggs-11-latest` |
| `mysql56-client` | `nepustil-112` |
| `mysql56-server` | `nepustil-112` |
| `mysql57-client` | `nepustil-112` |
| `mysql57-server` | `nepustil-112` |
| `mysql80-client` | `sggs-11-latest` |
| `mysql80-server` | `sggs-11-latest` |
| `nano` | `nepustil-112` |
| `python` | `nepustil-112` |
| `screen` | `nepustil-112` |
| `subversion` | `nepustil-112` |

## Cohort: `nepustil-112`

Root paketler: `compat9x-amd64`, `gcc`, `gcc7`, `gdb`, `gmake`, `makedepend`, `mariadb104-client`, `mariadb104-server`, `mysql56-client`, `mysql56-server`, `mysql57-client`, `mysql57-server`, `nano`, `python`, `screen`, `subversion`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:11:amd64/repos/nepustil-112",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```

## Cohort: `nepustil-113`

Root paketler: `gcc8`, `gcc9`, `mariadb105-client`, `mariadb105-server`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:11:amd64/repos/nepustil-113",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```

## Cohort: `nepustil-114`

Root paketler: `gcc10`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:11:amd64/repos/nepustil-114",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```

## Cohort: `sggs-11-latest`

Root paketler: `boost-all`, `compat11x-amd64`, `compat7x-amd64`, `compat8x-amd64`, `cryptopp`, `devil`, `freecolor`, `gcc11`, `gcc48`, `mariadb103-client`, `mariadb103-server`, `mysql55-client`, `mysql55-server`, `mysql80-client`, `mysql80-server`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:11:amd64/repos/sggs-11-latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```
