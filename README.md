# FreeBSD 9–14 Legacy Selected Package Repository

Bu depo FreeBSD **9, 10, 11, 12, 13 ve 14** için tam FreeBSD package mirror'ı değildir. Yalnızca proje için gerekli seçilmiş paket ailelerini ve onların **transitif runtime bağımlılıklarını** arşivler.

## Kapsam

Root paket politikası `config/roots.json` dosyasındadır.

- MySQL: FreeBSD binary arşivlerinde gerçekten bulunan **5.5 ve üzeri tüm `mysqlXX-client` / `mysqlXX-server` serileri**
- MariaDB: gerçekten bulunan **10.3 ve üzeri tüm `mariadbXXX-client` / `mariadbXXX-server` serileri**
- GCC: **`gcc48`'den itibaren bulunan stabil numaralı GCC paketleri** ve `gcc` meta/default paketi
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
- `compat7x-amd64`, `compat8x-amd64`, `compat9x-amd64`, `compat11x-amd64`, `compat12x-amd64`
- `compat7x-i386`, `compat8x-i386`, `compat9x-i386`, `compat11x-i386`, `compat12x-i386`

Bunların dışında bir paket yalnızca yukarıdaki root paketlerden birinin runtime bağımlılığı ise depoya alınır. Build-only dependency paketleri sırf bir portu derlemek için gerekli diye otomatik eklenmez.

## ABI yapısı

Her FreeBSD major/mimari ayrı repository root'udur:

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

Bir ABI'nin paketi başka ABI'yi tamamlamak için kullanılmaz. Örneğin `FreeBSD:12:amd64` deposundaki eksik bir dependency `FreeBSD:13:amd64` veya `FreeBSD:12:i386` paketinden doldurulmaz.

`FreeBSD:11:i386` için doğrulanmış tam binary kaynak henüz bulunmadığı sürece importer sahte URL üretmez ve bu hedefi boş/status-only bırakır.

## Kaynak önceliği

Kaynak matrisi `config/sources.json` içindedir. Genel sıra:

1. Eski DB/GCC sürümlerini kurtarmak için Nepustil snapshotları
2. SGGS / Neonet EOL mirrorları
3. Halen mevcut hedeflerde resmi `pkg.FreeBSD.org`
4. FreeBSD 9 için PC-BSD pkgng arşivleri

Her üretilen ABI için kullanılan kaynaklar `SOURCES/` altında, seçilen root/dependency paketler ve SHA-256 bilgileri `MANIFESTS/` altında kaydedilir.

## FreeBSD 12 mevcut paketlerinin migrasyonu

Bu repository başlangıçta `FreeBSD:12:amd64` paketlerini root seviyesindeki `All/` altında içeriyordu. Importer:

1. mevcut katalogu okur,
2. mevcut `.pkg` dosyasının katalog SHA-256 değeriyle uyuştuğunu doğrular,
3. hedef root/dependency closure içinde ise dosyayı yeniden indirmek yerine kullanır,
4. eksik veya checksum'u hatalı paketi arşiv kaynaklarından backfill eder,
5. yeni `FreeBSD:12:amd64/latest/` deposu eksiksiz oluşmadan eski root düzenini silmez.

Bu nedenle eski 12 paketleri gereksiz yere tekrar indirilmez.

---

# Hızlı Kurulum — `${ABI}` ile ortak conf

Önerilen yöntem `/etc/pkg/FreeBSD.conf` dosyasını doğrudan değiştirmek yerine override dosyası oluşturmaktır.

Önce ABI'nizi görün:

```sh
pkg config ABI
```

Çıktı `FreeBSD:10:amd64`, `FreeBSD:12:i386`, `FreeBSD:14:amd64` gibi bu repository dizinleriyle eşleşiyorsa aşağıdaki ortak ayar kullanılabilir:

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

Ardından normal `pkg` komutları kullanılır:

```sh
pkg search mysql
pkg search mariadb
pkg search gcc
pkg install -y gmake boost-all subversion makedepend devil python cryptopp nano screen freecolor gdb
```

> FreeBSD 9'daki çok eski pkg sürümleri ABI'yi `freebsd:9:x86:64` / `freebsd:9:x86:32` şeklinde raporlayabilir. Böyle bir sistemde `${ABI}` ortak yolu yerine aşağıdaki **explicit FreeBSD 9 conf** bloklarından uygun olanı kullanın. Üretilen `packagesite.txz` katalogları `pkg >= 1.1` içindir; `pkg 1.0` yalnızca eski `repo.txz` formatını beklediğinden önce pkg'nin güncellenmesi gerekir.

---

# Sürüm / Mimari Bazlı Hazır Conf'lar

Aşağıdaki bloklarda kendi sisteminize uygun **tek** conf'u kopyalayıp `/usr/local/etc/pkg/repos/FreeBSD.conf` olarak kaydedebilirsiniz.

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

Bu hedef için doğrulanmış binary kaynak bulunana ve `MANIFESTS/FreeBSD-11-i386.json` durumu `ok` olana kadar bu conf'u kullanmayın.

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

Her explicit conf'tan sonra:

```sh
pkg update -f
```

## Tek komutla conf yazma örneği

Örneğin FreeBSD 12 amd64:

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

---

# Paket kurulum örnekleri

```sh
pkg install -y gdb gmake boost-all subversion makedepend devil python cryptopp nano screen freecolor
```

Mevcut ABI katalogunda bulunan DB/GCC serilerini görmek için:

```sh
pkg search -g 'mysql*-client'
pkg search -g 'mysql*-server'
pkg search -g 'mariadb*-client'
pkg search -g 'mariadb*-server'
pkg search -g 'gcc*'
```

Örnek:

```sh
pkg install mysql57-server
pkg install mysql80-server
pkg install mariadb106-server
pkg install gcc48
pkg install gcc10
pkg install gcc
```

Bir package serisinin belirli FreeBSD ABI'sinde arşiv binary'si hiç yoksa importer başka ABI'den paket kopyalamaz. Hangi root'ların bulunduğu/bulunamadığı ilgili `MANIFESTS/FreeBSD-X-ARCH.json` dosyasından görülebilir.

---

# Repository metadata

Her çalışan repository root'u en az şu yapıyı üretir:

```text
FreeBSD:X:ARCH/latest/
├── All/
├── Latest/
├── meta
├── meta.conf
├── meta.txz
├── packagesite.txz
└── SHA256SUMS
```

`signature_type: "none"` şu anda bilinçli olarak kullanılır. Paket dosyaları SHA-256 ile takip edilir ancak repository henüz cryptographic signing key ile imzalanmış değildir. İleride public-key/fingerprint signing eklenebilir.

## Otomatik importer

`./scripts/build_repo.py --target FreeBSD:12:amd64 --migrate-existing-12`

Importer kaynak metadata'sını okur, root paketleri seçer, transitif dependency closure'ı çözer, SHA-256 doğrulaması yapar ve sadece gerekli package dosyalarını repository'ye materialize eder.

GitHub Actions workflow'u hedefleri sırayla üretir ve her ABI'yi ayrı commit ederek büyük tek push riskini azaltır.
