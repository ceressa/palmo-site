# -*- coding: utf-8 -*-
"""Sitenin TEK sabit kaynagi.

Colmo sitesinde `MAIL` ve `PKG` hem `build.py` hem `legal_text.py` icinde ayri
ayri yaziliydi ve aralarinda import yoktu: biri degisince digeri bayat
kaliyordu. Burada iki dosya da bu modulu okuyor.

Alan adi da tek yerde: `CNAME` dosyasi elle konuldugu icin (bkz. README) icerigi
`DOMAIN` ile ayni olmali, `build.py` derlemede bunu kontrol eder.
"""

SITE = "https://palmo.dozi.app"
DOMAIN = SITE.split("//", 1)[1]
PKG = "com.bardino.palmo"
MAIL = "info@dozi.app"
DEV = "Bardino Technology"
DEV_URL = "https://dozi.app"
APP = "Palmo"

# Sayfa basina son guncelleme. Colmo'da tek global tarih vardi ve bir sayfa
# degisince ucunun de tarihi degisiyordu; okuyan icin bu bir yalan.
UPDATED = {
    "privacy.html": "2026-08-30",
    "terms.html": "2026-08-30",
    "account-deletion.html": "2026-08-30",
}

# Dil kodu -> (html lang, og locale, kendi dilindeki adi)
# Sira ve adlar uygulamanin `lib/l10n/strings.dart` dosyasindaki `localeNames`
# ile ayni; iki taraf ayrismasin diye oradan alindi.
LANGS = [
    ("en", "en", "en_US", "English"),
    ("tr", "tr", "tr_TR", "Türkçe"),
    ("de", "de", "de_DE", "Deutsch"),
    ("es", "es", "es_ES", "Español"),
    ("fr", "fr", "fr_FR", "Français"),
    ("pt", "pt", "pt_BR", "Português"),
]

# Kok dizinin dili. Magaza kaydi varsayilan olarak Ingilizce listelenecek ve
# koke gelen ziyaretcinin cogu Turkce bilmiyor. Degistirilecekse tek yer burasi.
ROOT_LANG = "en"

# Yasal metin yalnizca bu dillerde tam yazildi. Yarim cevrilmis bir sozlesme,
# cevrilmemis olandan kotudur; diger dillerin altbilgisi Ingilizceye gider.
LEGAL_LANGS = {"en", "tr"}

LEGAL_PAGES = ("privacy.html", "terms.html", "account-deletion.html")
