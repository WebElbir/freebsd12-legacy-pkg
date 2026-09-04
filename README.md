# FreeBSD 9–14 Legacy Selected Package Repository

Bu depo FreeBSD **9, 10, 11, 12, 13 ve 14** için tam FreeBSD package mirror'ı değildir. Yalnızca istenen root paketleri ve bunların **transitif runtime bağımlılıkları** tutulur.

## Canonical repository kuralı

Kullanıcı tarafında bütün desteklenen FreeBSD sürümleri ve mimarileri için **tek geçerli varsayılan URL biçimi** şudur:

```conf
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/${ABI}/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
```

**GitHub Releases URL'leri pkg repository adresi olarak kullanılmaz.** Örneğin `https://github.com/.../releases/download/...` biçimi bu projenin istemci yapılandırması değildir.

`${ABI}` FreeBSD tarafından örneğin `FreeBSD:14:amd64`, `FreeBSD:12:i386` şeklinde açılır. Böylece aynı conf dosyası desteklenen bütün ABI'lerde doğru `main/${ABI}/latest` dizinine gider.

Önerilen kurulum:

```sh
mkdir -p /usr/local/etc/pkg/repos
cat > /usr/local/etc/pkg/repos/FreeBSD.conf <<'EOF'
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/${ABI}/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
EOF

pkg update -f
```

---

## Paket kapsamı

Root politikası `config/roots.json` dosyasındadır.

- MySQL: binary arşivlerde bulunan **5.5 ve üzeri `mysqlXX-client` / `mysqlXX-server` serileri**
- MariaDB: binary arşivlerde bulunan **10.3 ve üzeri `mariadbXXX-client` / `mariadbXXX-server` serileri**
- GCC: **`gcc48` ve üzeri stabil numaralı GCC paketleri** + generic `gcc`
- `gmake`
- `boost-all`
- `subversion`
- `makedepend`
- `devil`
- `python`
- `cryptopp`
- `nano`
- `screen`
- `freecolor`
- `gdb`
- amd64 compat: `compat7x-amd64`, `compat8x-amd64`, `compat9x-amd64`, `compat11x-amd64`, `compat12x-amd64`
- i386 compat: `compat7x-i386`, `compat8x-i386`, `compat9x-i386`, `compat11x-i386`, `compat12x-i386`

`gcc34`, `gcc44`, `gcc46`, `gcc47`, `*-devel` ve cross-toolchain GCC paketleri root değildir. İstenen root paketlerinin runtime dependency'leri otomatik olarak eklenir; sırf derleme için gereken build-only dependency'ler eklenmez.

Bir paket başka FreeBSD major sürümünden veya başka mimariden dependency tamamlamak amacıyla **asla kopyalanmaz**.

---

# ABI dizinleri

Canonical dizinler:

```text
FreeBSD:9:amd64/latest/
FreeBSD:9:i386/latest/
FreeBSD:10:amd64/latest/
FreeBSD:10:i386/latest/
FreeBSD:11:amd64/latest/
FreeBSD:11:i386/latest/
FreeBSD:12:amd64/latest/
FreeBSD:12:i386/latest/
FreeBSD:13:amd64/latest/
FreeBSD:13:i386/latest/
FreeBSD:14:amd64/latest/
FreeBSD:14:i386/latest/
```

Her canonical `latest/` dizini en az şu pkg repository metadata'sını taşır:

```text
latest/
├── All/                    # paket varsa
├── meta
├── meta.conf
├── meta.txz
├── packagesite.txz
├── SHA256SUMS
└── STATUS.json             # yalnız boş/unresolved endpointlerde bulunabilir
```

Doğrulanmış binary kaynağı henüz bulunmamış bir ABI için endpoint 404 bırakılmaz. Bunun yerine **geçerli fakat boş** bir pkg repository metadata seti yayınlanır; gerçek paket bulunmadığı açıkça `MANIFESTS/` ve gerektiğinde `STATUS.json` içinde belirtilir. Böyle bir ABI'ye başka sürüm veya mimariden sahte paket doldurulmaz.

---

# Neden cohort kullanılıyor?

Tarihsel MySQL, MariaDB ve GCC paketleri farklı FreeBSD snapshotlarından gelir. Aynı FreeBSD major içinde eski bir paket eski ICU/Boost/OpenSSL SONAME'ına, yeni paket ise daha yeni bir sürüme bağlı olabilir.

Ayrıca pkg repository tarafında aynı package adının birden fazla aktif sürümünü tek katalogda tutmak güvenilir bir çözüm değildir. Bu nedenle importer önce kaynak snapshotları **dependency-coherent cohort** olarak çözer. Ardından her ABI için en geniş ve kendi içinde uyumlu cohort canonical `${ABI}/latest` olarak yayınlanır.

`MANIFESTS/FreeBSD-X-ARCH.json` dosyaları:

- hangi root paketlerin bulunduğunu,
- hangi kaynak cohort'tan geldiklerini,
- hangilerinin çözülemediğini,
- `latest` olarak hangi cohort'un seçildiğini,
- canonical repository yolunu

kayıt altında tutar.

Cohort bilgileri provenance ve uyumluluk denetimi içindir. Kullanıcıya verilecek varsayılan repository URL'si değişmez: **`main/${ABI}/latest`**.

---

# Kaynak sırası

Kaynak matrisi `config/sources.json` dosyasındadır. Öncelik sırası genel olarak:

1. Nepustil tarihsel snapshotları
2. SGGS / Neonet EOL mirrorları
3. resmî `pkg.FreeBSD.org` repository'leri
4. FreeBSD 9 için PC-BSD pkgng arşivleri

Kaynak bulunmayan ABI için URL uydurulmaz veya başka ABI paketi kullanılmaz.

---

# Sürüm / mimari bazlı explicit conf örnekleri

`${ABI}` kullanmak istemeyen sistemlerde aynı canonical yapının açık halleri aşağıdadır.

## FreeBSD 9 amd64 / x64

```conf
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:9:amd64/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
```

## FreeBSD 9 i386 / x32

```conf
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:9:i386/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
```

## FreeBSD 10 amd64 / x64

```conf
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:10:amd64/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
```

## FreeBSD 10 i386 / x32

```conf
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:10:i386/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
```

## FreeBSD 11 amd64 / x64

```conf
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:11:amd64/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
```

## FreeBSD 11 i386 / x32

```conf
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:11:i386/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
```

## FreeBSD 12 amd64 / x64

```conf
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:12:amd64/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
```

## FreeBSD 12 i386 / x32

```conf
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:12:i386/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
```

## FreeBSD 13 amd64 / x64

```conf
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:13:amd64/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
```

## FreeBSD 13 i386 / x32

```conf
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:13:i386/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
```

## FreeBSD 14 amd64 / x64

```conf
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:14:amd64/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
```

## FreeBSD 14 i386 / x32

```conf
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:14:i386/latest",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
```

Her explicit conf sonrasında:

```sh
pkg update -f
```

---

# Kullanım örnekleri

```sh
pkg search mysql
pkg search mariadb
pkg search gcc
```

```sh
pkg install -y gdb gmake boost-all subversion makedepend devil python cryptopp nano screen freecolor
```

Örnek database/compiler paketleri:

```sh
pkg install mysql57-server
pkg install mysql80-server
pkg install mariadb103-server
pkg install mariadb106-server
pkg install mariadb1011-server
pkg install gcc48
pkg install gcc10
pkg install gcc
```

Bir paket o ABI'nin canonical `latest` cohort'unda yoksa `pkg install` ile zorla başka ABI'ye yönlendirme yapılmaz. Gerçek kapsam `MANIFESTS/FreeBSD-X-ARCH.json` üzerinden kontrol edilir.

---

# Repository metadata ve bütünlük

Paketler `SHA256SUMS` ile takip edilir. Importer upstream checksum mevcut olduğunda indirme sırasında doğrular. Repository şu anda public-key/fingerprint ile imzalanmadığı için:

```conf
signature_type: "none"
```

kullanılır.

Canonical raw yayın akışı ayrıca:

1. `packagesite.txz` içinde `packagesite.yaml` bulunduğunu,
2. GitHub'ın normal Git blob sınırına yaklaşan paketlerin güvenlik eşiğini aşmadığını,
3. push sonrasında `raw.githubusercontent.com/.../${ABI}/latest/meta.conf` ve `packagesite.txz` erişimini,
4. paket varsa en az bir gerçek `All/<paket>` nesnesinin uzaktan erişilebilir olduğunu

otomatik kontrol eder.

---

# FreeBSD 9 notu

FreeBSD 9 dönemindeki çok eski `pkg` sürümleri repository metadata formatı bakımından farklı davranabilir. Bu depo `packagesite.txz` kullanan pkgng istemcilerini hedefler. Yalnız eski `repo.txz` bekleyen `pkg 1.0` sistemlerinde önce pkg güncellenmesi gerekebilir.

---

# Otomatik importer

Ana builder:

```sh
python scripts/build_repo_cohorts.py --target FreeBSD:12:amd64 --migrate-existing-12
```

Conf rehberi:

```sh
python scripts/render_config_guide.py --target FreeBSD:12:amd64
```

Importer akışı:

1. doğrulanmış upstream kataloglarını okur,
2. yalnız istenen root paket adlarını seçer,
3. transitif runtime dependency closure'ını çözer,
4. başka ABI veya FreeBSD major ile dependency tamamlamaz,
5. uyumlu root closure'larını cohort'lar halinde toplar,
6. paketleri indirip checksum kontrolü yapar,
7. pkg repository metadata'sını üretir,
8. en geniş uyumlu cohort'u `${ABI}/latest` olarak yayınlar,
9. kaynak/coverage bilgisini `MANIFESTS/` ve `SOURCES/` altında saklar,
10. kullanıcı conf rehberini `CONFIGS/` altında üretir.

Ana kural değişmez:

```text
https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/${ABI}/latest
```
