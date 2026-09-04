# FreeBSD:14:amd64 pkg conf rehberi

Durum: **ok**

## Canonical repository

Bu ABI için kullanıcıya verilecek tek varsayılan repository biçimi aşağıdaki `raw.githubusercontent.com/.../${ABI}/latest` yapısıdır.
GitHub Release URL'leri pkg repository adresi olarak kullanılmaz.

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:14:amd64/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```

Aktif `latest` cohort: `nepustil-140`.

## Paket → kaynak cohort haritası

Bu tablo provenance/uyumluluk bilgisidir. Kullanıcı tarafında repository URL'si yine yukarıdaki canonical `latest` adresidir.
Aynı package adı için tarihsel sürümleri tek pkg kataloğunda zorla birleştirmiyoruz; pkg repository veritabanı package adını tekil ele alır ve eski snapshot bağımlılıkları yeni snapshotlarla ABI/SONAME çakışması yaratabilir.

| Root paket | Kaynak cohort |
|---|---|
| `boost-all` | `freebsd-14-latest` |
| `compat11x-amd64` | `nepustil-143` |
| `compat12x-amd64` | `nepustil-140` |
| `compat7x-amd64` | `freebsd-14-latest` |
| `compat8x-amd64` | `freebsd-14-latest` |
| `compat9x-amd64` | `nepustil-140` |
| `cryptopp` | `nepustil-140` |
| `devil` | `freebsd-14-latest` |
| `freecolor` | `freebsd-14-latest` |
| `gcc` | `nepustil-140` |
| `gcc12` | `nepustil-140` |
| `gcc13` | `nepustil-140` |
| `gcc14` | `nepustil-143` |
| `gcc15` | `freebsd-14-latest` |
| `gcc16` | `freebsd-14-latest` |
| `gdb` | `nepustil-140` |
| `gmake` | `nepustil-140` |
| `makedepend` | `nepustil-140` |
| `mariadb1011-client` | `nepustil-140` |
| `mariadb1011-server` | `nepustil-140` |
| `mariadb105-client` | `nepustil-140` |
| `mariadb105-server` | `nepustil-140` |
| `mariadb106-client` | `nepustil-140` |
| `mariadb106-server` | `nepustil-140` |
| `mariadb114-client` | `nepustil-141` |
| `mariadb114-server` | `nepustil-141` |
| `mariadb118-client` | `nepustil-143` |
| `mariadb118-server` | `nepustil-143` |
| `mariadb123-client` | `freebsd-14-latest` |
| `mariadb123-server` | `freebsd-14-latest` |
| `mysql80-client` | `nepustil-140` |
| `mysql80-server` | `nepustil-140` |
| `mysql84-client` | `freebsd-14-latest` |
| `mysql84-server` | `freebsd-14-latest` |
| `mysql97-client` | `freebsd-14-latest` |
| `mysql97-server` | `freebsd-14-latest` |
| `nano` | `nepustil-140` |
| `python` | `freebsd-14-latest` |
| `screen` | `nepustil-140` |
| `subversion` | `nepustil-140` |
