# FreeBSD:12:i386 pkg conf rehberi

Durum: **partial**

## Ortak / varsayılan `latest`

Bu yol en geniş tek ve kendi içinde uyumlu cohort olan `sggs-12i386-latest` deposunu gösterir.

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:12:i386/latest",
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
| `compat11x-i386` | `sggs-12i386-latest` |
| `compat12x-i386` | `sggs-12i386-latest` |
| `compat7x-i386` | `sggs-12i386-latest` |
| `compat8x-i386` | `sggs-12i386-latest` |
| `compat9x-i386` | `sggs-12i386-latest` |
| `cryptopp` | `sggs-12i386-latest` |
| `devil` | `sggs-12i386-latest` |
| `freecolor` | `sggs-12i386-latest` |
| `gcc10` | `sggs-12i386-latest` |
| `gcc11` | `sggs-12i386-latest` |
| `gcc12` | `sggs-12i386-latest` |
| `gcc13` | `sggs-12i386-latest` |
| `gcc48` | `sggs-12i386-latest` |
| `gcc8` | `sggs-12i386-latest` |
| `gcc9` | `sggs-12i386-latest` |
| `gdb` | `sggs-12i386-latest` |
| `gmake` | `sggs-12i386-latest` |
| `makedepend` | `sggs-12i386-latest` |
| `mariadb1011-client` | `sggs-12i386-latest` |
| `mariadb1011-server` | `sggs-12i386-latest` |
| `mariadb105-client` | `sggs-12i386-latest` |
| `mariadb105-server` | `sggs-12i386-latest` |
| `mariadb106-client` | `sggs-12i386-latest` |
| `mariadb106-server` | `sggs-12i386-latest` |
| `mysql57-client` | `sggs-12i386-latest` |
| `mysql57-server` | `sggs-12i386-latest` |
| `mysql80-client` | `sggs-12i386-latest` |
| `mysql80-server` | `sggs-12i386-latest` |
| `mysql81-client` | `sggs-12i386-latest` |
| `mysql81-server` | `sggs-12i386-latest` |
| `nano` | `sggs-12i386-latest` |
| `screen` | `sggs-12i386-latest` |

## Cohort: `sggs-12i386-latest`

Root paketler: `compat11x-i386`, `compat12x-i386`, `compat7x-i386`, `compat8x-i386`, `compat9x-i386`, `cryptopp`, `devil`, `freecolor`, `gcc10`, `gcc11`, `gcc12`, `gcc13`, `gcc48`, `gcc8`, `gcc9`, `gdb`, `gmake`, `makedepend`, `mariadb1011-client`, `mariadb1011-server`, `mariadb105-client`, `mariadb105-server`, `mariadb106-client`, `mariadb106-server`, `mysql57-client`, `mysql57-server`, `mysql80-client`, `mysql80-server`, `mysql81-client`, `mysql81-server`, `nano`, `screen`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:12:i386/repos/sggs-12i386-latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```
