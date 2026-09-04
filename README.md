# FreeBSD 9–14 Legacy Selected Package Repository

Bu depo FreeBSD **9, 10, 11, 12, 13 ve 14** için tam FreeBSD package mirror'ı değildir. Yalnızca istenen root paketleri ve bunların **transitif runtime bağımlılıkları** tutulur.

## Paket kapsamı

Root politikası `config/roots.json` dosyasındadır.

- MySQL: binary arşivlerde bulunan **5.5 ve üzeri tüm `mysqlXX-client` / `mysqlXX-server` serileri**
- MariaDB: binary arşivlerde bulunan **10.3 ve üzeri tüm `mariadbXXX-client` / `mariadbXXX-server` serileri**
- GCC: **`gcc48` ve üzeri stabil numaralı GCC paketleri** + `gcc` meta/default paketi
- `gmake`, `boost-all`, `subversion`, `makedepend`, `devil`, `python`, `cryptopp`, `nano`, `screen`, `freecolor`, `gdb`
- `compat7x-amd64`, `compat8x-amd64`, `compat9x-amd64`, `compat11x-amd64`, `compat12x-amd64`
- `compat7x-i386`, `compat8x-i386`, `compat9x-i386`, `compat11x-i386`, `compat12x-i386`

`gcc34`, `gcc44`, `gcc46`, `gcc47`, `*-devel`, cross-toolchain GCC paketleri veya başka paket aileleri root olarak alınmaz. Yukarıdaki paketlerden birinin runtime dependency'si ise gerekli yan paket otomatik olarak eklenir. Build-only dependency'ler sırf derleme sırasında lazım diye eklenmez.

---

# Repository yapısı

Her FreeBSD major/mimari ayrı ABI root'udur:

```text
FreeBSD:9:amd64/
FreeBSD:9:i386/
FreeBSD:10:amd64/
FreeBSD:10:i386/
FreeBSD:11:amd64/
FreeBSD:11:i386/
FreeBSD:12:amd64/
FreeBSD:12:i386/
FreeBSD:13:amd64/
FreeBSD:13:i386/
FreeBSD:14:amd64/
FreeBSD:14:i386/
```

Bir ABI'nin paketi başka ABI'den dependency tamamlamak için kullanılmaz.

## `latest` ve cohort yapısı

Eski MySQL/MariaDB/GCC serileri farklı tarihli FreeBSD snapshotlarından gelir. Örneğin aynı FreeBSD major içinde eski bir MySQL paketi ICU'nun eski SONAME sürümünü, daha yeni MySQL paketi ise yeni ICU sürümünü isteyebilir. Bunları tek `packagesite` içine zorla birleştirmek çalışma zamanında `.so not found` veya dependency çakışması üretir.

Bu nedenle repo iki katmanlıdır:

```text
FreeBSD:X:ARCH/
├── latest/                 # en geniş tek ve kendi içinde uyumlu cohort
└── repos/
    ├── nepustil-...
    ├── sggs-...
    ├── freebsd-...
    └── ...
```

- `${ABI}/latest` günlük kullanım için tek, kendi içinde uyumlu bir repository'dir.
- Tarihsel MySQL/MariaDB/GCC serileri gerektiğinde `${ABI}/repos/<cohort>` üzerinden kurulur.
- Hangi root paketin hangi cohort içinde bulunduğu `MANIFESTS/FreeBSD-X-ARCH.json` içindeki `coverage` alanında kayıtlıdır.
- Her senkron sonrasında `CONFIGS/FreeBSD-X-ARCH.md` dosyası otomatik üretilir. Bu dosyalarda **paket → cohort haritası ve doğrudan kopyala-yapıştır conf blokları** vardır.

Bu düzen sayesinde tüm istenen binary seriler arşivlenebilir fakat birbirleriyle ABI uyumsuz tarihsel dependency sürümleri aynı aktif `pkg` kataloğuna zorlanmaz.

---

# Kaynak sırası

Kaynak matrisi `config/sources.json` dosyasındadır. Temel sıra:

1. Nepustil tarihsel snapshotları
2. SGGS / Neonet EOL mirrorları
3. Resmî `pkg.FreeBSD.org` repository'leri
4. FreeBSD 9 için PC-BSD pkgng arşivleri

Kullanılan kataloglar `SOURCES/`, üretilen paket/cohort haritası ve SHA-256 bilgileri `MANIFESTS/` altında takip edilir. Kaynak bulunmayan ABI için sahte URL oluşturulmaz.

---

# Hızlı kurulum — ortak `${ABI}` yöntemi

Önerilen yöntem `/etc/pkg/FreeBSD.conf` dosyasını doğrudan değiştirmek yerine `/usr/local/etc/pkg/repos/FreeBSD.conf` ile override etmektir.

Önce ABI'nizi kontrol edin:

```sh
pkg config ABI
```

Ardından:

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

Sonra normal şekilde:

```sh
pkg search mysql
pkg search mariadb
pkg search gcc
pkg install -y gmake boost-all subversion makedepend devil python cryptopp nano screen freecolor gdb
```

> `${ABI}` çıktısı repository dizin adıyla eşleşmiyorsa aşağıdaki explicit conf bloklarından sisteminize uygun olanı kullanın. Özellikle eski FreeBSD 9 `pkg` sürümlerinde explicit yol daha güvenlidir.

---

# Sürüm / mimari bazlı hazır conf'lar

Aşağıdakiler `latest` cohort'una gider. İlgili ABI'nin senkron durumunu önce `MANIFESTS/FreeBSD-X-ARCH.json` dosyasından kontrol etmek önerilir.

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

Doğrulanmış FreeBSD 11 i386 binary kaynağı olmadığı sürece `MANIFESTS/FreeBSD-11-i386.json` `no-verified-source` gösterecektir; bu durumda bu URL kullanılmamalıdır.

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

Explicit conf'u dosyaya kaydettikten sonra:

```sh
pkg update -f
```

---

# Tarihsel bir MySQL / MariaDB / GCC cohort'una geçme

Önce kendi ABI rehberinizi açın:

```text
CONFIGS/FreeBSD-9-amd64.md
CONFIGS/FreeBSD-9-i386.md
CONFIGS/FreeBSD-10-amd64.md
CONFIGS/FreeBSD-10-i386.md
CONFIGS/FreeBSD-11-amd64.md
CONFIGS/FreeBSD-11-i386.md
CONFIGS/FreeBSD-12-amd64.md
CONFIGS/FreeBSD-12-i386.md
CONFIGS/FreeBSD-13-amd64.md
CONFIGS/FreeBSD-13-i386.md
CONFIGS/FreeBSD-14-amd64.md
CONFIGS/FreeBSD-14-i386.md
```

Bu dosyada örneğin `mysql57-server` karşısında `nepustil-132` yazıyorsa ilgili hazır blok şu mantıktadır:

```conf
FreeBSD: {
  url: "https://raw.githubusercontent.com/WebElbir/freebsd12-legacy-pkg/main/FreeBSD:13:amd64/repos/nepustil-132",
  mirror_type: "none",
  signature_type: "none",
  enabled: yes
}
```

Ardından:

```sh
pkg update -f
pkg install mysql57-server
```

Başka tarihsel seri gerekiyorsa CONFIGS dosyasındaki o pakete ait cohort conf'una geçilir. Bu bilinçli bir tasarımdır; farklı snapshotların uyumsuz ICU/Boost/OpenSSL dependency sürümlerini tek aktif katalogda karıştırmamak için yapılır.

---

# Kurulum örnekleri

```sh
pkg install -y gdb gmake boost-all subversion makedepend devil python cryptopp nano screen freecolor
```

DB/GCC arama:

```sh
pkg search -g 'mysql*-client'
pkg search -g 'mysql*-server'
pkg search -g 'mariadb*-client'
pkg search -g 'mariadb*-server'
pkg search -g 'gcc*'
```

Örnek:

```sh
pkg install mysql55-server
pkg install mysql56-server
pkg install mysql57-server
pkg install mysql80-server
pkg install mariadb103-server
pkg install mariadb106-server
pkg install mariadb1011-server
pkg install gcc48
pkg install gcc10
pkg install gcc
```

Bir seri ilgili FreeBSD ABI için hiçbir doğrulanmış binary kaynakta yoksa başka ABI'den paket kopyalanmaz. Durum `MANIFESTS/FreeBSD-X-ARCH.json` içinde görünür.

---

# Repository metadata

Her çalışan cohort en az şu yapıyı taşır:

```text
FreeBSD:X:ARCH/repos/COHORT/
├── All/
├── meta
├── meta.conf
├── meta.txz
├── packagesite.txz
└── SHA256SUMS
```

`latest/` aynı yapının seçilmiş en geniş uyumlu cohort kopyasıdır.

`signature_type: "none"` şu anda bilinçli olarak kullanılır. Paketler SHA-256 ile takip edilir fakat repository henüz public-key/fingerprint ile imzalanmış değildir.

## FreeBSD 9 notu

FreeBSD 9 dönemindeki çok eski `pkg` sürümleri repository metadata formatı bakımından farklı davranabilir. Bu depo `packagesite.txz` kullanan pkgng istemcilerini hedefler. Yalnız eski `repo.txz` bekleyen `pkg 1.0` sistemlerinde önce pkg güncellenmelidir. FreeBSD 9 i386 arşivlerinin legacy SQLite katalogları ayrıca importer tarafından doğrulanır; katalog okunamıyorsa hedef sahte şekilde başarılı gösterilmez.

---

# Otomatik importer

Ana cohort builder:

```sh
python scripts/build_repo_cohorts.py --target FreeBSD:12:amd64 --migrate-existing-12
```

Conf rehberi üretimi:

```sh
python scripts/render_config_guide.py --target FreeBSD:12:amd64
```

Importer:

1. doğrulanmış upstream kataloglarını okur,
2. yalnız istenen root paket adlarını seçer,
3. her root için transitif runtime dependency closure'ı çözer,
4. farklı snapshotları aynı dependency setine zorla karıştırmaz,
5. birbirleriyle uyumlu root closure'larını cohort altında toplar,
6. package dosyalarını indirip SHA-256 doğrular,
7. `packagesite.txz` ve repository metadata'sını üretir,
8. paket → cohort haritasını `MANIFESTS/` altında kaydeder,
9. kullanıcı için `CONFIGS/` altında kopyala-yapıştır conf rehberi oluşturur.

GitHub Actions tüm hedefleri sırayla üretir ve her ABI'yi ayrı commit/push eder.
