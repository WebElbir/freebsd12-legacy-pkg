# FreeBSD:11:amd64 pkg conf rehberi

Durum: **ok**

## Canonical repository

Bu ABI için kullanıcıya verilecek tek varsayılan repository biçimi aşağıdaki `raw.githubusercontent.com/.../${ABI}/latest` yapısıdır.
GitHub Release URL'leri pkg repository adresi olarak kullanılmaz.

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

Aktif `latest` cohort: `nepustil-112`.

## Paket → kaynak cohort haritası

Bu tablo provenance/uyumluluk bilgisidir. Kullanıcı tarafında repository URL'si yine yukarıdaki canonical `latest` adresidir.
Aynı package adı için tarihsel sürümleri tek pkg kataloğunda zorla birleştirmiyoruz; pkg repository veritabanı package adını tekil ele alır ve eski snapshot bağımlılıkları yeni snapshotlarla ABI/SONAME çakışması yaratabilir.

| Root paket | Kaynak cohort |
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
