# FreeBSD:14:i386 pkg conf rehberi

Durum: **ok**

## Canonical repository

Bu ABI için kullanıcıya verilecek tek varsayılan repository biçimi aşağıdaki `raw.githubusercontent.com/.../${ABI}/latest` yapısıdır.
GitHub Release URL'leri pkg repository adresi olarak kullanılmaz.

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:14:i386/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```

Aktif `latest` cohort: `freebsd-14i386-release5`.

## Paket → kaynak cohort haritası

Bu tablo provenance/uyumluluk bilgisidir. Kullanıcı tarafında repository URL'si yine yukarıdaki canonical `latest` adresidir.
Aynı package adı için tarihsel sürümleri tek pkg kataloğunda zorla birleştirmiyoruz; pkg repository veritabanı package adını tekil ele alır ve eski snapshot bağımlılıkları yeni snapshotlarla ABI/SONAME çakışması yaratabilir.

| Root paket | Kaynak cohort |
|---|---|
| `boost-all` | `freebsd-14i386-release5` |
| `compat11x-i386` | `freebsd-14i386-release5` |
| `compat12x-i386` | `freebsd-14i386-release5` |
| `compat7x-i386` | `freebsd-14i386-release5` |
| `compat8x-i386` | `freebsd-14i386-release5` |
| `compat9x-i386` | `freebsd-14i386-release5` |
| `cryptopp` | `freebsd-14i386-release5` |
| `devil` | `freebsd-14i386-release5` |
| `freecolor` | `freebsd-14i386-release5` |
| `gcc` | `freebsd-14i386-release5` |
| `gcc12` | `freebsd-14i386-release5` |
| `gcc13` | `freebsd-14i386-release5` |
| `gcc14` | `freebsd-14i386-release5` |
| `gcc15` | `freebsd-14i386-release5` |
| `gcc16` | `freebsd-14i386-release5` |
| `gdb` | `freebsd-14i386-release5` |
| `gmake` | `freebsd-14i386-release5` |
| `makedepend` | `freebsd-14i386-release5` |
| `mariadb1011-client` | `freebsd-14i386-release5` |
| `mariadb1011-server` | `freebsd-14i386-release5` |
| `mariadb114-client` | `freebsd-14i386-release5` |
| `mariadb114-server` | `freebsd-14i386-release5` |
| `mariadb118-client` | `freebsd-14i386-release5` |
| `mariadb118-server` | `freebsd-14i386-release5` |
| `mariadb123-client` | `freebsd-14i386-release5` |
| `mariadb123-server` | `freebsd-14i386-release5` |
| `mysql80-client` | `freebsd-14i386-release5` |
| `mysql80-server` | `freebsd-14i386-release5` |
| `nano` | `freebsd-14i386-release5` |
| `python` | `freebsd-14i386-release5` |
| `screen` | `freebsd-14i386-release5` |
| `subversion` | `freebsd-14i386-release5` |
