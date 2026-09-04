# FreeBSD:10:i386 pkg conf rehberi

Durum: **partial**

## Ortak / varsayılan `latest`

Bu yol en geniş tek ve kendi içinde uyumlu cohort olan `neonet-10i386-quarterly` deposunu gösterir.

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:10:i386/latest",
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
| `compat7x-i386` | `neonet-10i386-quarterly` |
| `compat8x-i386` | `neonet-10i386-quarterly` |
| `compat9x-i386` | `neonet-10i386-quarterly` |
| `cryptopp` | `neonet-10i386-quarterly` |
| `freecolor` | `neonet-10i386-quarterly` |
| `gcc48` | `neonet-10i386-quarterly` |
| `gcc49` | `neonet-10i386-quarterly` |
| `gcc5` | `neonet-10i386-quarterly` |
| `gcc7` | `neonet-10i386-quarterly` |
| `gcc8` | `neonet-10i386-quarterly` |
| `gdb` | `neonet-10i386-quarterly` |
| `gmake` | `neonet-10i386-quarterly` |
| `makedepend` | `neonet-10i386-quarterly` |
| `mariadb103-client` | `neonet-10i386-quarterly` |
| `mariadb103-server` | `neonet-10i386-quarterly` |
| `mysql55-client` | `neonet-10i386-quarterly` |
| `mysql55-server` | `neonet-10i386-quarterly` |
| `mysql56-client` | `neonet-10i386-quarterly` |
| `mysql56-server` | `neonet-10i386-quarterly` |
| `mysql80-client` | `neonet-10i386-quarterly` |
| `mysql80-server` | `neonet-10i386-quarterly` |
| `nano` | `neonet-10i386-quarterly` |
| `screen` | `neonet-10i386-quarterly` |
| `subversion` | `neonet-10i386-quarterly` |

## Cohort: `neonet-10i386-quarterly`

Root paketler: `compat7x-i386`, `compat8x-i386`, `compat9x-i386`, `cryptopp`, `freecolor`, `gcc48`, `gcc49`, `gcc5`, `gcc7`, `gcc8`, `gdb`, `gmake`, `makedepend`, `mariadb103-client`, `mariadb103-server`, `mysql55-client`, `mysql55-server`, `mysql56-client`, `mysql56-server`, `mysql80-client`, `mysql80-server`, `nano`, `screen`, `subversion`

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:10:i386/repos/neonet-10i386-quarterly",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```
