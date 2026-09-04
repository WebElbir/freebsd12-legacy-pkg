# FreeBSD:13:amd64 pkg conf rehberi

Durum: **ok**

## Canonical repository

Bu ABI için kullanıcıya verilecek tek varsayılan repository biçimi aşağıdaki `raw.githubusercontent.com/.../${ABI}/latest` yapısıdır.
GitHub Release URL'leri pkg repository adresi olarak kullanılmaz.

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

Aktif `latest` cohort: `nepustil-130`.

## Paket → kaynak cohort haritası

Bu tablo provenance/uyumluluk bilgisidir. Kullanıcı tarafında repository URL'si yine yukarıdaki canonical `latest` adresidir.
Aynı package adı için tarihsel sürümleri tek pkg kataloğunda zorla birleştirmiyoruz; pkg repository veritabanı package adını tekil ele alır ve eski snapshot bağımlılıkları yeni snapshotlarla ABI/SONAME çakışması yaratabilir.

| Root paket | Kaynak cohort |
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
