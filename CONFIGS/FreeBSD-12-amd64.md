# FreeBSD:12:amd64 pkg conf rehberi

Durum: **ok**

## Canonical repository

Bu ABI için kullanıcıya verilecek tek varsayılan repository biçimi aşağıdaki `raw.githubusercontent.com/.../${ABI}/latest` yapısıdır.
GitHub Release URL'leri pkg repository adresi olarak kullanılmaz.

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

Aktif `latest` cohort: `nepustil-121`.

## Paket → kaynak cohort haritası

Bu tablo provenance/uyumluluk bilgisidir. Kullanıcı tarafında repository URL'si yine yukarıdaki canonical `latest` adresidir.
Aynı package adı için tarihsel sürümleri tek pkg kataloğunda zorla birleştirmiyoruz; pkg repository veritabanı package adını tekil ele alır ve eski snapshot bağımlılıkları yeni snapshotlarla ABI/SONAME çakışması yaratabilir.

| Root paket | Kaynak cohort |
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
