# -*- coding: utf-8 -*-
"""Nunito'yu siteye yerel woff2 olarak koyar.

    python tools/build-fonts.py

Neden: site Nunito'yu fonts.googleapis.com'dan yukluyordu; her ziyaret
ziyaretcinin IP'sini Google'a veriyordu. Dosyalar oyun depolarindaki TTF'lerden
uretilir, internetten bir sey indirilmez. 700/800/900 Palmo'nun kendi
deposundan; 400 Palmo'da yok, Decimo'nun deposundan (ayni surum, 3.602).

Alt kume: Latin + Latin-1 + Latin Extended-A (Turkce, Almanca, Fransizca,
Ispanyolca, Portekizce harfler), genel noktalama ve euro. Yasal sayfalardaki
geri okunu (U+2190) Nunito hic tasimiyor; Google Fonts'ta da yoktu, sistem
fontundan gelir. Yalnizca CSS'in istedigi agirliklar uretilir: 400 govde,
700 strong, 800 ve 900 basliklar.

Nunito OFL 1.1 ile lisansli; lisans dosyasi `assets/fonts/OFL.txt`.
"""
import os
import sys

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "assets", "fonts")

PALMO = r"E:\dev\mobile\palmo\assets\fonts"
DECIMO = r"E:\dev\mobile\Decimo-numberchain\assets\fonts"

SOURCES = {
    400: os.path.join(DECIMO, "Nunito-Regular.ttf"),
    700: os.path.join(PALMO, "Nunito-Bold.ttf"),
    800: os.path.join(PALMO, "Nunito-ExtraBold.ttf"),
    900: os.path.join(PALMO, "Nunito-Black.ttf"),
}

UNICODES = (
    list(range(0x20, 0x7F))        # Basic Latin
    + list(range(0xA0, 0x100))     # Latin-1: a-umlaut, c-cedilla, n-tilde, middle dot, copyright
    + list(range(0x100, 0x180))    # Latin Extended-A: dotless i, I-dot, s-cedilla, g-breve, oe
    + list(range(0x2010, 0x203B))  # dashes, quote marks, ellipsis, bullet, guillemets
    + [0x20AC, 0x2122]
)

# Turkce harfler alt kumede yoksa sayfa sessizce sistem fontuna duser.
MUST = "ıİşŞğĞçÇöÖüÜäÄßéèêëàâîïôûùÿœñáíóúãõ€·©«»’“”"


def main():
    os.makedirs(OUT, exist_ok=True)
    for weight, src in sorted(SOURCES.items()):
        if not os.path.exists(src):
            sys.exit("kaynak yok: %s" % src)
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["*"]
        opts.name_IDs = ["*"]
        opts.notdef_outline = True
        font = TTFont(src)
        sub = subset.Subsetter(options=opts)
        sub.populate(unicodes=UNICODES)
        sub.subset(font)
        dst = os.path.join(OUT, "nunito-%d.woff2" % weight)
        font.flavor = "woff2"
        font.save(dst)

        cmap = TTFont(dst).getBestCmap()
        missing = [c for c in MUST if ord(c) not in cmap]
        if missing:
            sys.exit("%s: eksik harf %s" % (dst, "".join(missing)))
        print("%s  %d bayt, %d karakter" % (os.path.relpath(dst, HERE),
                                             os.path.getsize(dst), len(cmap)))


if __name__ == "__main__":
    main()
