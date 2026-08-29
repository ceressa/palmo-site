# palmo-site

[palmo.dozi.app](https://palmo.dozi.app) - Palmo'nun tanitim sayfasi, gizlilik
politikasi, kullanim kosullari ve hesap silme sayfasi.

Oyun deposu ayri: `com.bardino.palmo`, `C:\Users\Ufuk\dev\mobile\palmo`.

## Sayfalar elle yazilmaz, uretilir

```powershell
python build.py
```

Alti dil x (acilis + yasal) elle tutulunca kaciniyor: bir cumleyi degistirmek
icin alti dosyaya dokunmak, bes tanesinin bayat kalmasi demek. Icerik
`build.py` icinde sozluk, yasal metinler `legal_text.py` icinde, sabitler
`config.py` icinde, HTML yalnizca cikti.

**Uretilen `.html` dosyalarini elle duzenleme**, bir sonraki derlemede geri
gider. Uretilen dosyalar: `index.html`, `tr|de|es|fr|pt/index.html`,
`privacy.html`, `terms.html`, `account-deletion.html` (kokte ve `tr/` altinda),
`404.html`, `sitemap.xml`, `robots.txt`, `manifest.json`, `.nojekyll`.

- Acilis sayfasi alti dilde: **en (kok)**, tr, de, es, fr, pt. Sira ve dil
  adlari oyundaki `lib/l10n/strings.dart` icindeki `localeNames` ile ayni.
- Yasal sayfalar yalnizca Ingilizce ve Turkce. Yarim cevrilmis bir sozlesme
  cevrilmemis olandan kotudur; diger dillerin altbilgisi Ingilizceye gider ve
  dil cubugu o sayfalarda yalnizca iki dil gosterir.

`build.py` derleme sonunda eksikleri listeler (CNAME, gorseller). O liste is
listesidir, hata degil.

Yerelde bakmak icin (mutlak yollar `/css/...` oldugu icin dosyayi cift
tiklamak yetmez, sunucu gerekiyor):

```powershell
python -m http.server 8099 --bind 127.0.0.1
```

## Elle guncellenecek dosyalar

Bunlar uretilmiyor, repoda elle duruyor:

| Dosya | Ne zaman |
|---|---|
| `CNAME` | Bir kez, asagida |
| `app-ads.txt` | AdMob hesabi acilinca ve AdMob listesi degistikce |
| `assets/palmo-mark.svg`, `assets/palmo-lockup-h.svg` | Marka degisirse |
| `assets/shots/*.webp` | Ekran goruntuleri cekilince (`assets/shots/README.md`) |
| `assets/palmo-share.png` | Feature graphic hazir olunca |

## CNAME

Bu dosya **repoda yok, elle olusturulacak**. Icine tek satir:

```
palmo.dozi.app
```

`build.py` dosyayi yazmiyor ama her derlemede kontrol ediyor: yoksa ya da
icerigi `config.py` icindeki `DOMAIN` ile ayni degilse uyari basiyor.

## Yayin

GitHub Pages, `main` dali, kok dizin. Actions yok, Jekyll ciktisi
kullanilmiyor: `python build.py` **yerelde** kosuluyor ve cikti commit
ediliyor. `.nojekyll` uretiliyor, boylece alt cizgiyle baslayan bir klasor
ileride sessizce yayindan dusmez.

DNS: `palmo` alt alani icin repo hangi GitHub hesabindaysa
`<hesap>.github.io` CNAME kaydi gerekir. Colmo `ceressa` altinda; Palmo icin
hesap **kararlastirilmadi**.

Yayina aldiktan sonra tek tek GET ile geri oku, panelin "basarili" demesine
guvenme: `/`, `/tr/`, `/privacy.html`, `/tr/privacy.html`, `/sitemap.xml`,
`/app-ads.txt`, olmayan bir yol (404 dondugunu dogrula).

## Gorseller

Eksik gorsel **yalan soyletmiyor**. `build.py` diski kontrol ediyor:

- `assets/shots/*.webp` yoksa vitrin kutusu acikca bos bir cerceveye dusuyor,
  temsili bir kare cizilmiyor ve olmayan dosyaya baglanti verilmiyor.
- `assets/palmo-share.png` (1200x630) yoksa `og:image` etiketleri **hic**
  yazilmiyor ve tam genislikteki bant bolumu sayfada yer almiyor. Dosya
  konulup yeniden derlenince ikisi de kendiliginden geliyor.
- `assets/palmo-icon.png` (180x180) yoksa `apple-touch-icon` yazilmiyor.
- `assets/palmo-icon-192.png` / `-512.png` yoksa manifest ikon listesinde
  yalnizca SVG isaret kaliyor.

Hangi karenin ne olmasi gerektigi: `assets/shots/README.md`.

## Marka isareti ve bir borc

`assets/palmo-mark.svg` (favicon, manifest) ve `assets/palmo-lockup-h.svg`
(ustteki yatay kilit) `design-r3/assets/` altindan kopyalandi; geometri ayni,
yalnizca `<title>`/`<desc>` kisaltildi ve font yiginina yedek eklendi.

**Borc: harfler hala `<text>`.** `<img>` icindeki bir SVG belgenin yazi
tiplerine ulasamaz, o yuzden kilit ve isaret sayfaya **gomulu** olarak
yaziliyor (`build.py` icindeki `inline_svg`) ve Nunito 900 boylece uygulaniyor.
Favicon ise dosyadan okundugu icin Nunito'suz bir makinede sistem yazi tipiyle
cizilir. Kalici cozum harfleri outline'a cevirmek; o gun `inline_svg` durur,
yalnizca dosyalar degisir. `design-r3/assets/palmo-mark.svg` dosyasinin kendi
notu da bunu soyluyor.

## Yazi tipi

Nunito, Google Fonts CDN'inden. Kabul edilen borc: gizlilik sayfasi tasiyan bir
site her ziyarette Google'a IP sizdiriyor. Uygulama zaten
`assets/fonts/Nunito-{Bold,ExtraBold,Black}.ttf` tasiyor; siteye yerel woff2
koymak hem tutarli hem hizli olur. Dikkat: sitede govde metni icin 400 agirligi
da isteniyor, uygulamada yalnizca 700/800/900 var.

## Iki kural

**Palet oyunun kendisinden.** `design-r3/tokens/*.css` ve `lib/design/tokens.dart`
ne diyorsa CSS de onu diyor. Siteye renk uydurulmuyor.

**Golge asla bulanik degil ve daima asagi.** Derinlik kati ofset cikintidir ve
ofset `0 Npx 0`; yan kacis yok (`design-r3/tokens/elevation.css`). Colmo'nun
sitesi `3px 3px` kullaniyordu, Palmo kullanmaz.

## Yasal metin gercege bagli

`legal_text.py` Colmo'dan **kopyalanmadi**, cunku Palmo baska bir urun: Firebase
yok, bulut kaydi yok, hesap yok, analitik ve cokme raporu SDK'si yok; buna
karsilik `in_app_purchase` (reklamsiz surum) ve `app_tracking_transparency`
(iOS izin akisi) var. Metin `lib/state/economy.dart` (can, 11. bolum esigi,
gunde 3 odullu reklam, `noAds`), `lib/state/progress.dart`,
`lib/state/settings.dart` ve `lib/l10n/strings.dart` (`reset_progress`)
uzerinden yazildi.

**Yayindan once dogrulanacak:** reklam ve satin alma kodu su an uygulamada
yazili degil (`google_mobile_ads` ve `in_app_purchase` pubspec'te, `lib/`
altinda kullanan dosya yok). Metin `economy.dart` icindeki karara gore yazildi.
Magazaya gonderilen surumde gercek yerlesim farkliysa metin once duzelir, sonra
gonderilir.

Tarihler sayfa basina: `config.py` icindeki `UPDATED` sozlugu. Bir sayfa
degisince yalnizca onun tarihi elle yukseltilir.

## Cikinca yapilacak

- Kahraman bolumundeki `.magaza-cip` iki `<span>`, cunku gidilecek yer yok.
  Magaza baglantilari hazir olunca ikisi `<a>` olur; metinler `build.py`
  icindeki `badge`, `endT`, `endS` anahtarlarinda.
- `assets/shots/` gercek karelerle dolar.
- `app-ads.txt` icindeki DIRECT satirinin yorumu kalkar.
