# FreeBSD:12:i386 pkg conf rehberi

Durum: **ok**

## Canonical repository

Bu ABI için kullanıcıya verilecek tek varsayılan repository biçimi aşağıdaki `raw.githubusercontent.com/.../${ABI}/latest` yapısıdır.
GitHub Release URL'leri pkg repository adresi olarak kullanılmaz.

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

Aktif `latest` cohort: `sggs-12i386-latest`.

## Paket → kaynak cohort haritası

Bu tablo provenance/uyumluluk bilgisidir. Kullanıcı tarafında repository URL'si yine yukarıdaki canonical `latest` adresidir.
Aynı package adı için tarihsel sürümleri tek pkg kataloğunda zorla birleştirmiyoruz; pkg repository veritabanı package adını tekil ele alır ve eski snapshot bağımlılıkları yeni snapshotlarla ABI/SONAME çakışması yaratabilir.

| Root paket | Kaynak cohort |
|---|---|
| `boost-all` | `sggs-12i386-latest` |
| `compat11x-i386` | `sggs-12i386-latest` |
| `compat12x-i386` | `sggs-12i386-latest` |
| `compat7x-i386` | `sggs-12i386-latest` |
| `compat8x-i386` | `sggs-12i386-latest` |
| `compat9x-i386` | `sggs-12i386-latest` |
| `cryptopp` | `sggs-12i386-latest` |
| `devil` | `sggs-12i386-latest` |
| `freecolor` | `sggs-12i386-latest` |
| `gcc` | `sggs-12i386-latest` |
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
| `python` | `sggs-12i386-latest` |
| `screen` | `sggs-12i386-latest` |
| `subversion` | `sggs-12i386-latest` |
