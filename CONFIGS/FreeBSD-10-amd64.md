# FreeBSD:10:amd64 pkg conf rehberi

Durum: **ok**

## Canonical repository

Bu ABI için kullanıcıya verilecek tek varsayılan repository biçimi aşağıdaki `raw.githubusercontent.com/.../${ABI}/latest` yapısıdır.
GitHub Release URL'leri pkg repository adresi olarak kullanılmaz.

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

Aktif `latest` cohort: `sggs-10-latest`.

## Paket → kaynak cohort haritası

Bu tablo provenance/uyumluluk bilgisidir. Kullanıcı tarafında repository URL'si yine yukarıdaki canonical `latest` adresidir.
Aynı package adı için tarihsel sürümleri tek pkg kataloğunda zorla birleştirmiyoruz; pkg repository veritabanı package adını tekil ele alır ve eski snapshot bağımlılıkları yeni snapshotlarla ABI/SONAME çakışması yaratabilir.

| Root paket | Kaynak cohort |
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
