# -*- coding: utf-8 -*-
"""Colmo'nun bozuk app-ads.txt dosyasindan Palmo'nunkini onararak uretir.

    python tools/build-app-ads.py            # kuru calisma, raporla
    python tools/build-app-ads.py --write    # ../app-ads.txt yaz

Colmo'nun dosyasi bir web sayfasindan kopyalanirken 45 karakterde SERT
sarilmis; kendi DIRECT satiri bile ikiye bolunmus:

    google.com, pub-1767292468741192, DIRECT, f08
    c47fec0942fa0

Ayristirici bu dosyayi okuyamaz. Sarma satir sonu EKLEYEREK bozdugu icin
onarim mumkun: yorumlar atilir, kalan her sey aralarina hicbir sey konmadan
tek bir dizeye yapistirilir, sonra kayit dilbilgisiyle yeniden bolunur.

Kayit dilbilgisi (IAB app-ads.txt): alanadi, yayinciKimligi, DIRECT|RESELLER
[, sertifikaKimligi]. Kayit sonu bu uc sozcukten biriyle ya da onu izleyen
onaltilik kimlikle bittigi icin sinirlar belirsiz degil.

Yayinci ayni (Bardino Technology / AdMob pub-1767292468741192), yetkili
satici listesi hesap duzeyinde oldugu icin Palmo'ya oldugu gibi gecerli.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\Users\Ufuk\dev\web\colmo-site\app-ads.txt"
DST = os.path.join(os.path.dirname(HERE), "app-ads.txt")

PUB = "pub-1767292468741192"
DIRECT = "google.com, %s, DIRECT, f08c47fec0942fa0" % PUB

RECORD = re.compile(
    r"[a-z0-9][a-z0-9.\-]*\.[a-z]{2,},"      # satici alan adi
    r"[^,]{1,80},"                            # yayinci kimligi
    r"(?:DIRECT|RESELLER)"                    # iliski
    # Sertifika kimligi TAM 16 onaltilik: TAG-ID boyu. Araligi {16,32} yapmak
    # sonraki kaydin ilk harfini yutuyor ve "e-planning.net" kaydi
    # "planning.net" olarak cikiyor - alan adi degistigi icin satir sessizce
    # yanlis, bicim kontrolunden de geciyor.
    r"(?:,[0-9a-fA-F]{16})?",
    re.IGNORECASE)


def main():
    with open(SRC, encoding="utf-8", errors="replace") as f:
        raw = f.readlines()

    # Yorum ve bos satirlari at, kalani BOSLUKSUZ yapistir: sarma yalnizca
    # satir sonu ekledi, karakter silmedi.
    blob = "".join(l.strip() for l in raw
                   if l.strip() and not l.lstrip().startswith("#"))
    blob = blob.replace(" ", "")

    records, pos, gaps = [], 0, []
    for m in RECORD.finditer(blob):
        if m.start() != pos:
            gaps.append(blob[pos:m.start()])
        records.append(m.group(0))
        pos = m.end()
    if pos != len(blob):
        gaps.append(blob[pos:])

    seen, out = set(), []
    for r in records:
        parts = [p.strip() for p in r.split(",")]
        line = ", ".join(parts)
        k = line.lower()
        if k not in seen:
            seen.add(k)
            out.append(line)

    # Kendi DIRECT satirimiz her zaman bassa ve DOGRU olmali.
    out = [DIRECT] + [l for l in out if PUB not in l]

    print("kaynak satir      :", len(raw))
    print("cozulen kayit     :", len(records))
    print("tekillestirilmis  :", len(out))
    print("artik (coz\u00fclemeyen):", len(gaps))
    for g in gaps[:5]:
        print("   ->", g[:90])
    print("ilk satir         :", out[0])
    bad = [l for l in out if not RECORD.fullmatch(l.replace(" ", ""))]
    print("bicimi bozuk      :", len(bad))
    for b in bad[:5]:
        print("   ->", b[:90])

    if "--write" not in sys.argv:
        print("\nKuru calisma. Yazmak icin: --write")
        return

    header = [
        "# Palmo - app-ads.txt",
        "#",
        "# Yayinci: Bardino Technology / AdMob %s." % PUB,
        "# Yetkili satici listesi hesap duzeyinde, o yuzden Colmo ve Decimo ile",
        "# ayni. Magaza kaydindaki web sitesi alani palmo.dozi.app oldugu icin",
        "# dogrulama bu dosyadan yapiliyor.",
        "#",
        "# Bu dosya tools/build-app-ads.py ile uretildi. ELLE DUZENLEME: kopyala",
        "# yapistir satirlari sarar ve DIRECT satirini ikiye boler; ayristirici",
        "# o dosyayi okuyamaz ve envanter yetkisiz sayilir.",
        "#",
        "# Yayina aldiktan SONRA https://palmo.dozi.app/app-ads.txt adresini GET",
        "# ile geri oku. Yazma isleminin \"basarili\" demesi yetmez.",
        "",
    ]
    with open(DST, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(header + out) + "\n")
    print("\nyazildi:", DST)


if __name__ == "__main__":
    main()
