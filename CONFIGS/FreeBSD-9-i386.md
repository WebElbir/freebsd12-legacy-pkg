# FreeBSD:9:i386 pkg conf rehberi

Durum: **no-requested-packages-resolved**

## Canonical repository

Bu ABI için kullanıcıya verilecek tek varsayılan repository biçimi aşağıdaki `raw.githubusercontent.com/.../${ABI}/latest` yapısıdır.
GitHub Release URL'leri pkg repository adresi olarak kullanılmaz.

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:9:i386/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF
pkg update -f
```

Bu ABI için doğrulanmış paket kaynağı bulunmadığından endpoint geçerli fakat bilinçli olarak boş bir pkg repository'dir.
Başka FreeBSD major/mimariden paket kopyalanmaz.
