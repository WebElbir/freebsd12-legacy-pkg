# FreeBSD:10:i386 pkg conf rehberi

Durum: **ok**

## Canonical repository

Bu ABI için kullanıcıya verilecek tek varsayılan repository biçimi aşağıdaki `raw.githubusercontent.com/.../${ABI}/latest` yapısıdır.
GitHub Release URL'leri pkg repository adresi olarak kullanılmaz.

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

Aktif `latest` cohort: `neonet-10i386-quarterly`.

## Paket → kaynak cohort haritası

Bu tablo provenance/uyumluluk bilgisidir. Kullanıcı tarafında repository URL'si yine yukarıdaki canonical `latest` adresidir.
Aynı package adı için tarihsel sürümleri tek pkg kataloğunda zorla birleştirmiyoruz; pkg repository veritabanı package adını tekil ele alır ve eski snapshot bağımlılıkları yeni snapshotlarla ABI/SONAME çakışması yaratabilir.

| Root paket | Kaynak cohort |
|---|---|
| `boost-all` | `neonet-10i386-quarterly` |
| `compat7x-i386` | `neonet-10i386-quarterly` |
| `compat8x-i386` | `neonet-10i386-quarterly` |
| `compat9x-i386` | `neonet-10i386-quarterly` |
| `cryptopp` | `neonet-10i386-quarterly` |
| `devil` | `neonet-10i386-quarterly` |
| `freecolor` | `neonet-10i386-quarterly` |
| `gcc` | `neonet-10i386-quarterly` |
| `gcc48` | `neonet-10i386-quarterly` |
| `gcc49` | `neonet-10i386-quarterly` |
| `gcc5` | `neonet-10i386-quarterly` |
| `gcc6` | `neonet-10i386-quarterly` |
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
| `mysql57-client` | `neonet-10i386-quarterly` |
| `mysql57-server` | `neonet-10i386-quarterly` |
| `mysql80-client` | `neonet-10i386-quarterly` |
| `mysql80-server` | `neonet-10i386-quarterly` |
| `nano` | `neonet-10i386-quarterly` |
| `python` | `neonet-10i386-quarterly` |
| `screen` | `neonet-10i386-quarterly` |
| `subversion` | `neonet-10i386-quarterly` |
