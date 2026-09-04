# FreeBSD:13:amd64 pkg conf rehberi

Durum: **ok**

## Ortak / varsayılan `latest`

Bu yol en geniş tek ve kendi içinde uyumlu cohort olan `nepustil-130` deposunu gösterir.

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:13:amd64/latest",
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
| `boost-all` | `freebsd-13-latest` |
| `compat11x-amd64` | `freebsd-13-latest` |
| `compat12x-amd64` | `nepustil-130` |
| `compat7x-amd64` | `freebsd-13-latest` |
| `compat8x-amd64` | `freebsd-13-latest` |
| `compat9x-amd64` | `nepustil-130` |
| `cryptopp` | `nepustil-130` |
| `devil` | `freebsd-13-latest` |
| `freecolor` | `freebsd-13-latest` |
| `gcc` | `nepustil-130` |
| `gcc10` | `nepustil-131` |
| `gcc11` | `nepustil-130` |
| `gcc12` | `nepustil-131` |
| `gcc13` | `nepustil-132` |
| `gcc14` | `freebsd-13-latest` |
| `gcc15` | `freebsd-13-latest` |
| `gdb` | `nepustil-130` |
| `gmake` | `nepustil-130` |
| `makedepend` | `nepustil-130` |
| `mariadb1011-client` | `freebsd-13-latest` |
| `mariadb1011-server` | `freebsd-13-latest` |
| `mariadb104-client` | `nepustil-130` |
| `mariadb104-server` | `nepustil-130` |
| `mariadb105-client` | `nepustil-130` |
| `mariadb105-server` | `nepustil-130` |
| `mariadb106-client` | `nepustil-131` |
| `mariadb106-server` | `nepustil-131` |
| `mariadb114-client` | `freebsd-13-latest` |
| `mariadb114-server` | `freebsd-13-latest` |
| `mariadb118-client` | `freebsd-13-latest` |
| `mariadb118-server` | `freebsd-13-latest` |
| `mysql57-client` | `nepustil-130` |
| `mysql57-server` | `nepustil-130` |
| `mysql80-client` | `freebsd-13-quarterly` |
| `mysql80-server` | `freebsd-13-quarterly` |
| `mysql84-client` | `freebsd-13-quarterly` |
| `mysql84-server` | `freebsd-13-quarterly` |
| `mysql96-client` | `freebsd-13-quarterly` |
| `mysql96-server` | `freebsd-13-quarterly` |
| `nano` | `nepustil-130` |
| `python` | `freebsd-13-latest` |
| `screen` | `nepustil-130` |
| `subversion` | `nepustil-130` |

## Cohort: `nepustil-130`

Root paketler: `compat12x-amd64`, `compat9x-amd64`, `cryptopp`, `gcc`, `gcc11`, `gdb`, `gmake`, `makedepend`, `mariadb104-client`, `mariadb104-server`, `mariadb105-client`, `mariadb105-server`, `mysql57-client`, `mysql57-server`, `nano`, `screen`, `subversion`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:13:amd64/repos/nepustil-130",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```

## Cohort: `nepustil-131`

Root paketler: `gcc10`, `gcc12`, `mariadb106-client`, `mariadb106-server`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:13:amd64/repos/nepustil-131",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```

## Cohort: `nepustil-132`

Root paketler: `gcc13`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:13:amd64/repos/nepustil-132",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```

## Cohort: `freebsd-13-latest`

Root paketler: `boost-all`, `compat11x-amd64`, `compat7x-amd64`, `compat8x-amd64`, `devil`, `freecolor`, `gcc14`, `gcc15`, `mariadb1011-client`, `mariadb1011-server`, `mariadb114-client`, `mariadb114-server`, `mariadb118-client`, `mariadb118-server`, `python`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:13:amd64/repos/freebsd-13-latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```

## Cohort: `freebsd-13-quarterly`

Root paketler: `mysql80-client`, `mysql80-server`, `mysql84-client`, `mysql84-server`, `mysql96-client`, `mysql96-server`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:13:amd64/repos/freebsd-13-quarterly",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```
