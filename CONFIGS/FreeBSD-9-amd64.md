# FreeBSD:9:amd64 pkg conf rehberi

Durum: **ok**

## Canonical repository

Bu ABI için kullanıcıya verilecek tek varsayılan repository biçimi aşağıdaki `raw.githubusercontent.com/.../${ABI}/latest` yapısıdır.
GitHub Release URL'leri pkg repository adresi olarak kullanılmaz.

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:9:amd64/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```

Aktif `latest` cohort: `pcbsd-92-gr`.

## Paket → kaynak cohort haritası

Bu tablo provenance/uyumluluk bilgisidir. Kullanıcı tarafında repository URL'si yine yukarıdaki canonical `latest` adresidir.
Aynı package adı için tarihsel sürümleri tek pkg kataloğunda zorla birleştirmiyoruz; pkg repository veritabanı package adını tekil ele alır ve eski snapshot bağımlılıkları yeni snapshotlarla ABI/SONAME çakışması yaratabilir.

| Root paket | Kaynak cohort |
|---|---|
| `boost-all` | `pcbsd-92-gr` |
| `compat7x-amd64` | `pcbsd-92-gr` |
| `compat8x-amd64` | `pcbsd-92-gr` |
| `compat9x-amd64` | `pcbsd-92-gr` |
| `cryptopp` | `pcbsd-92-gr` |
| `devil` | `pcbsd-92-gr` |
| `gcc` | `pcbsd-92-gr` |
| `gcc48` | `pcbsd-92-gr` |
| `gcc49` | `pcbsd-92-gr` |
| `gdb` | `pcbsd-92-gr` |
| `gmake` | `pcbsd-92-gr` |
| `makedepend` | `pcbsd-92-gr` |
| `mysql55-client` | `pcbsd-92-gr` |
| `mysql55-server` | `pcbsd-92-gr` |
| `mysql56-client` | `pcbsd-92-gr` |
| `mysql56-server` | `pcbsd-92-gr` |
| `nano` | `pcbsd-92-gr` |
| `python` | `pcbsd-92-gr` |
| `screen` | `pcbsd-92-gr` |
| `subversion` | `pcbsd-92-gr` |
