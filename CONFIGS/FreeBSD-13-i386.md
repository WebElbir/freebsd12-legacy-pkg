# FreeBSD:13:i386 pkg conf rehberi

Durum: **partial**

## Ortak / varsayılan `latest`

Bu yol en geniş tek ve kendi içinde uyumlu cohort olan `freebsd-13i386-release5` deposunu gösterir.

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:13:i386/latest",
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
| `compat11x-i386` | `freebsd-13i386-release5` |
| `compat12x-i386` | `freebsd-13i386-release5` |
| `compat7x-i386` | `freebsd-13i386-release5` |
| `compat8x-i386` | `freebsd-13i386-release5` |
| `compat9x-i386` | `freebsd-13i386-release5` |
| `cryptopp` | `freebsd-13i386-release5` |
| `devil` | `freebsd-13i386-release5` |
| `freecolor` | `freebsd-13i386-release5` |
| `gcc11` | `freebsd-13i386-release5` |
| `gcc12` | `freebsd-13i386-release5` |
| `gcc13` | `freebsd-13i386-release5` |
| `gcc14` | `freebsd-13i386-release5` |
| `gdb` | `freebsd-13i386-release5` |
| `gmake` | `freebsd-13i386-release5` |
| `makedepend` | `freebsd-13i386-release5` |
| `mariadb1011-client` | `freebsd-13i386-release5` |
| `mariadb1011-server` | `freebsd-13i386-release5` |
| `mariadb105-client` | `freebsd-13i386-release5` |
| `mariadb105-server` | `freebsd-13i386-release5` |
| `mariadb106-client` | `freebsd-13i386-release5` |
| `mariadb106-server` | `freebsd-13i386-release5` |
| `mariadb114-client` | `freebsd-13i386-release5` |
| `mariadb114-server` | `freebsd-13i386-release5` |
| `mysql80-client` | `freebsd-13i386-release5` |
| `mysql80-server` | `freebsd-13i386-release5` |
| `nano` | `freebsd-13i386-release5` |
| `screen` | `freebsd-13i386-release5` |

## Cohort: `freebsd-13i386-release5`

Root paketler: `compat11x-i386`, `compat12x-i386`, `compat7x-i386`, `compat8x-i386`, `compat9x-i386`, `cryptopp`, `devil`, `freecolor`, `gcc11`, `gcc12`, `gcc13`, `gcc14`, `gdb`, `gmake`, `makedepend`, `mariadb1011-client`, `mariadb1011-server`, `mariadb105-client`, `mariadb105-server`, `mariadb106-client`, `mariadb106-server`, `mariadb114-client`, `mariadb114-server`, `mysql80-client`, `mysql80-server`, `nano`, `screen`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:13:i386/repos/freebsd-13i386-release5",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```
