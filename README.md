# palmo-site

[palmo.bardino.app](https://palmo.bardino.app) - Palmo'nun tanitim sayfasi, gizlilik
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
  Portekizce metin Brezilya Portekizcesi: `lang` ve `hreflang` `pt-BR`, yol
  `/pt/`.
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
| `assets/palmo-mark.svg`, `assets/palmo-lockup-h.svg` | Marka degisirse (`tools/outline-svg.py`) |
| `assets/fonts/*.woff2` | Yazi tipi ya da karakter kumesi degisirse (`tools/build-fonts.py`) |
| `assets/shots/*.webp` | Ekran goruntuleri cekilince (`assets/shots/README.md`) |
| `assets/palmo-share.png` | Feature graphic hazir olunca |

## CNAME

Bu dosya **repoda yok, elle olusturulacak**. Icine tek satir:

```
palmo.bardino.app
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

## Marka isareti

`assets/palmo-mark.svg` (favicon, manifest) ve `assets/palmo-lockup-h.svg`
(ustteki yatay kilit) `design-r3/assets/` altindan kopyalandi; geometri ayni.

**Harfler kontur (14 Ekim 2026).** Eskiden `<text>` idiler ve sayfanin metni
"4 P P a a l l m m o o" oluyordu: her harf golge + renk olarak iki kez, ustune
tohumdaki 4. Arama motoru ve metin cikaran her arac bunu goruyordu.
`tools/outline-svg.py` harfleri Nunito 900'un kendi konturuna ceviriyor
(text-anchor ve dominant-baseline tarayici gibi hesaplanir); SVG'de okunacak
metin kalmadi, erisilebilir ad yalnizca kokteki `role="img"
aria-label="Palmo"`. Favicon da artik ziyaretcinin sistem fontuna dusmuyor.
Marka degisirse `design-r3/assets/` altindaki `<text>`'li surum kopyalanip arac
yeniden kosulur:

```powershell
python tools/outline-svg.py assets/palmo-lockup-h.svg assets/palmo-mark.svg
```

Kilit sayfaya hala gomulu (`build.py` `inline_svg`): koyu temada lacivert
kontur `.kilit [stroke=...]` ile degisiyor ve bu ancak gomulu SVG'de calisir.

## Yazi tipi

Nunito sitenin kendi sunucusundan: `assets/fonts/nunito-{400,700,800,900}.woff2`,
lisans `assets/fonts/OFL.txt`. Google Fonts baglantisi kaldirildi; sayfa
baska bir sunucudan hicbir sey yuklemiyor ve altbilgi bunu soyluyor. Dosyalar
oyun depolarindaki TTF'lerden uretilir (700/800/900 Palmo, 400 Decimo; ayni
surum 3.602), internetten indirilmez. Alt kume Latin + Latin-1 + Latin
Extended-A, Turkce harfleri arac kendisi kontrol ediyor:

```powershell
python tools/build-fonts.py
```

## E-posta adresleri ve Cloudflare

Site Cloudflare arkasinda ve E-posta Adresi Gizleme acik: isaretsiz bir adres
`/cdn-cgi/l/email-protection#...` baglantisina cevrilir, JavaScript kapaliyken
404 verir. Her adres `<!--email_off-->...<!--/email_off-->` icinde
(`build.py` `mail_link`, `legal_text.py` `_mail`). Yeni adres yazarken bu
ikisinden birini kullan.

## Iki kural

**Palet oyunun kendisinden.** `design-r3/tokens/*.css` ve `lib/design/tokens.dart`
ne diyorsa CSS de onu diyor. Siteye renk uydurulmuyor.

**Golge asla bulanik degil ve daima asagi.** Derinlik kati ofset cikintidir ve
ofset `0 Npx 0`; yan kacis yok (`design-r3/tokens/elevation.css`). Colmo'nun
sitesi `3px 3px` kullaniyordu, Palmo kullanmaz.

## Yasal metin gercege bagli

`legal_text.py` Colmo'dan **kopyalanmadi**. 30 Agustos 2026'dan beri metin
oyunun bulut kaydini, istege bagli Google/Apple girisini, Firebase Analytics,
Crashlytics, AdMob ve reklamsiz surum satin almasini anlatiyor; hangi
cumlenin hangi kaynak dosyadan dogrulandigi `legal_text.py` dosyasinin
basindaki listede. (Bu bolum eskiden "Firebase yok, bulut kaydi yok" diyordu;
o urun artik yok.)

Turkce yasal metin "siz" ile yaziliyor (uc oyunun yasal metni ayni hitapla);
acilis sayfalari "sen".

Tarihler sayfa basina: `config.py` icindeki `UPDATED` sozlugu. Bir sayfa
degisince yalnizca onun tarihi elle yukseltilir.

## Magaza baglantilari

Palmo Eylul 2026'dan beri iki magazada. Baglantilar `config.py` icindeki
`APP_STORE` / `GOOGLE_PLAY`, rozetler `assets/badges/<dil>/` altinda: Decimo
deposundaki `store_assets/badges` klasorunden, her dilin resmi rozeti. Google
PNG'sinin seffaf kenari kirpildi ki iki rozet ayni gorunen boyda dursun.
Rozete golge ya da cerceve eklenmez (Apple ve Google kilavuzu).
