# -*- coding: utf-8 -*-
"""Sitenin TEK sabit kaynagi.

Colmo sitesinde `MAIL` ve `PKG` hem `build.py` hem `legal_text.py` icinde ayri
ayri yaziliydi ve aralarinda import yoktu: biri degisince digeri bayat
kaliyordu. Burada iki dosya da bu modulu okuyor.

Alan adi da tek yerde: `CNAME` dosyasi elle konuldugu icin (bkz. README) icerigi
`DOMAIN` ile ayni olmali, `build.py` derlemede bunu kontrol eder.
"""

SITE = "https://palmo.bardino.app"
DOMAIN = SITE.split("//", 1)[1]
PKG = "com.bardino.palmo"
MAIL = "info@bardino.app"
DEV = "Bardino Technology"
DEV_URL = "https://bardino.app"
APP = "Palmo"
APP_STORE = "https://apps.apple.com/app/palmo-number-weave/id6806719070"
GOOGLE_PLAY = "https://play.google.com/store/apps/details?id=" + PKG

# Sayfa basina son guncelleme. Colmo'da tek global tarih vardi ve bir sayfa
# degisince ucunun de tarihi degisiyordu; okuyan icin bu bir yalan.
UPDATED = {
    "privacy.html": "2026-10-14",
    "terms.html": "2026-08-30",
    "account-deletion.html": "2026-08-30",
}

# Dil kodu (yol) -> (html lang + hreflang, og locale, kendi dilindeki adi)
# Sira ve adlar uygulamanin `lib/l10n/strings.dart` dosyasindaki `localeNames`
# ile ayni; iki taraf ayrismasin diye oradan alindi. Portekizce metin Brezilya
# Portekizcesi (voce, fase) ve magaza kaydi da pt-BR: lang pt-BR, yol /pt/.
LANGS = [
    ("en", "en", "en_US", "English"),
    ("tr", "tr", "tr_TR", "Türkçe"),
    ("de", "de", "de_DE", "Deutsch"),
    ("es", "es", "es_ES", "Español"),
    ("fr", "fr", "fr_FR", "Français"),
    ("pt", "pt-BR", "pt_BR", "Português"),
]

# Kok dizinin dili. Magaza kaydi varsayilan olarak Ingilizce listelenecek ve
# koke gelen ziyaretcinin cogu Turkce bilmiyor. Degistirilecekse tek yer burasi.
ROOT_LANG = "en"

# Yasal metin yalnizca bu dillerde tam yazildi. Yarim cevrilmis bir sozlesme,
# cevrilmemis olandan kotudur; diger dillerin altbilgisi Ingilizceye gider.
LEGAL_LANGS = {"en", "tr"}

LEGAL_PAGES = ("privacy.html", "terms.html", "account-deletion.html")
