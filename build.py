# -*- coding: utf-8 -*-
"""palmo.dozi.app sayfalarini uretir.

    python build.py

Neden uretici: alti dil x (acilis + yasal) elle tutulunca kaciniyor. Bir
cumleyi degistirmek icin alti dosyaya dokunmak, bes tanesinin bayat kalmasi
demek. Icerik burada sozluk, HTML ciktida. Uretilen .html dosyalarini elle
duzenleme.

Sabitler `config.py` icinde, yasal metinler `legal_text.py` icinde.

EKSIK GORSEL YALAN SOYLETMEZ: ekran goruntusu ya da paylasim gorseli diskte
yoksa o bolum yer tutucuya duser ve <meta og:image> hic yazilmaz. Dosya
konulup yeniden derlenince bolum kendiliginden gercege doner.
"""
import io
import os
import re

from config import (APP, DEV, DEV_URL, DOMAIN, LANGS, LEGAL_LANGS, LEGAL_PAGES,
                    PKG, ROOT_LANG, SITE, UPDATED)

HERE = os.path.dirname(os.path.abspath(__file__))

# Vitrindeki dort kare. Dosya adlari oyunun ekranlarina gore secildi;
# assets/shots/README.md hangisinin ne oldugunu anlatiyor.
SHOTS = ["01_board.webp", "02_settle.webp", "03_result.webp", "04_map.webp"]

SHARE = "assets/palmo-share.png"   # 1200x630, magaza feature graphic'inden
ICON_PNG = "assets/palmo-icon.png"  # apple-touch-icon, 180x180
MARK = "assets/palmo-mark.svg"
LOCKUP = "assets/palmo-lockup-h.svg"

T = {}

T["en"] = {
    "title": "Palmo - Weave the whole board",
    "desc": "A quiet puzzle. The number on a seed is how many cells its region "
            "holds; grow every region to its own size until the board is "
            "covered. Coming soon to Android and iOS.",
    "badge": "Coming soon",
    "h1a": "The number on a seed",
    "h1b": "is the size of its region.",
    "lead": "Palmo is a quiet puzzle. Every seed carries a number, and that "
            "number is how many cells belong to it. Grow each region to "
            "exactly its own size, until the board is covered and nothing is "
            "left over.",
    "small": "Free to play. Works offline.",
    "shotsT": "From the game",
    "shotsS": "Real screenshots, not mock-ups.",
    "caps": ["The board", "A region settling", "The end of a level",
             "The map"],
    "ph": "Screenshot coming",
    "endT": "Not out yet.",
    "endS": "Palmo is still in the workshop. This page will carry the store "
            "links the day it is out.",
    "bandAlt": "Palmo",
    "legal": ("Privacy", "Terms of use", "Account deletion"),
    "by": "Palmo is made by",
    "back": "Back to Palmo",
    "upd": "Last updated",
    "e404T": "Nothing here.",
    "e404S": "That page does not exist.",
}

T["tr"] = {
    "title": "Palmo - Bütün tahtayı doku",
    "desc": "Sessiz bir bulmaca. Tohumdaki rakam, o bölgenin kaç hücre "
            "olduğunu söyler; her bölgeyi tam kendi büyüklüğüne kadar büyüt ve "
            "tahtayı kapat. Android ve iOS'ta çok yakında.",
    "badge": "Çok yakında",
    "h1a": "Tohumdaki rakam,",
    "h1b": "o bölgenin büyüklüğüdür.",
    "lead": "Palmo sessiz bir bulmacadır. Her tohum bir rakam taşır ve o "
            "rakam, tohuma kaç hücrenin ait olduğudur. Her bölgeyi tam kendi "
            "büyüklüğüne kadar büyüt; tahta kapanana ve artan hücre kalmayana "
            "kadar.",
    "small": "Ücretsiz oynanır. İnternetsiz çalışır.",
    "shotsT": "Oyundan kareler",
    "shotsS": "Hepsi gerçek ekran görüntüsü, temsili değil.",
    "caps": ["Tahta", "Yerine oturan bir bölge", "Bölümün sonu", "Harita"],
    "ph": "Ekran görüntüsü yakında",
    "endT": "Henüz çıkmadı.",
    "endS": "Palmo hâlâ atölyede. Çıktığı gün mağaza bağlantıları bu sayfada "
            "olacak.",
    "bandAlt": "Palmo",
    "legal": ("Gizlilik", "Kullanım koşulları", "Hesap silme"),
    "by": "Palmo'yu yapan",
    "back": "Palmo'ya dön",
    "upd": "Son güncelleme",
    "e404T": "Burada bir şey yok.",
    "e404S": "Böyle bir sayfa yok.",
}

T["de"] = {
    "title": "Palmo - Webe das ganze Brett",
    "desc": "Ein ruhiges Puzzle. Die Zahl auf einem Samen sagt, wie viele "
            "Felder sein Gebiet umfasst; lass jedes Gebiet auf seine eigene "
            "Größe wachsen. Bald für Android und iOS.",
    "badge": "Bald verfügbar",
    "h1a": "Die Zahl auf einem Samen",
    "h1b": "ist die Größe seines Gebiets.",
    "lead": "Palmo ist ein ruhiges Puzzle. Jeder Samen trägt eine Zahl, und "
            "diese Zahl ist die Anzahl der Felder, die zu ihm gehören. Lass "
            "jedes Gebiet auf genau seine eigene Größe wachsen, bis das Brett "
            "bedeckt ist und nichts übrig bleibt.",
    "small": "Kostenlos spielbar. Funktioniert offline.",
    "shotsT": "Aus dem Spiel",
    "shotsS": "Echte Screenshots, keine Montagen.",
    "caps": ["Das Brett", "Ein Gebiet setzt sich", "Das Ende eines Levels",
             "Die Karte"],
    "ph": "Screenshot folgt",
    "endT": "Noch nicht erschienen.",
    "endS": "Palmo ist noch in der Werkstatt. Am Tag der Veröffentlichung "
            "stehen die Store-Links hier.",
    "bandAlt": "Palmo",
    "legal": ("Datenschutz", "Nutzungsbedingungen", "Konto löschen"),
    "by": "Palmo stammt von",
    "back": "Zurück zu Palmo",
    "upd": "Zuletzt aktualisiert",
    "e404T": "Hier ist nichts.",
    "e404S": "Diese Seite gibt es nicht.",
}

T["es"] = {
    "title": "Palmo - Teje todo el tablero",
    "desc": "Un puzle tranquilo. El número de la semilla dice cuántas casillas "
            "tiene su región; haz crecer cada región hasta su tamaño exacto. "
            "Muy pronto en Android e iOS.",
    "badge": "Muy pronto",
    "h1a": "El número de la semilla",
    "h1b": "es el tamaño de su región.",
    "lead": "Palmo es un puzle tranquilo. Cada semilla lleva un número, y ese "
            "número es cuántas casillas le pertenecen. Haz crecer cada región "
            "hasta su tamaño exacto, hasta que el tablero quede cubierto y no "
            "sobre ninguna casilla.",
    "small": "Gratis. Se juega sin conexión.",
    "shotsT": "Del juego",
    "shotsS": "Capturas reales, no montajes.",
    "caps": ["El tablero", "Una región que se asienta", "El final de un nivel",
             "El mapa"],
    "ph": "Captura próximamente",
    "endT": "Todavía no ha salido.",
    "endS": "Palmo sigue en el taller. El día del lanzamiento los enlaces de "
            "las tiendas estarán aquí.",
    "bandAlt": "Palmo",
    "legal": ("Privacidad", "Términos de uso", "Eliminar cuenta"),
    "by": "Palmo está hecho por",
    "back": "Volver a Palmo",
    "upd": "Última actualización",
    "e404T": "Aquí no hay nada.",
    "e404S": "Esa página no existe.",
}

T["fr"] = {
    "title": "Palmo - Tisse tout le plateau",
    "desc": "Un puzzle calme. Le chiffre de la graine indique combien de cases "
            "compte sa région ; fais grandir chaque région jusqu'à sa taille "
            "exacte. Bientôt sur Android et iOS.",
    "badge": "Bientôt disponible",
    "h1a": "Le chiffre de la graine",
    "h1b": "est la taille de sa région.",
    "lead": "Palmo est un puzzle calme. Chaque graine porte un chiffre, et ce "
            "chiffre est le nombre de cases qui lui appartiennent. Fais "
            "grandir chaque région jusqu'à sa taille exacte, jusqu'à ce que le "
            "plateau soit couvert et qu'il ne reste rien.",
    "small": "Gratuit. Jouable hors ligne.",
    "shotsT": "Images du jeu",
    "shotsS": "De vraies captures, pas des maquettes.",
    "caps": ["Le plateau", "Une région qui se pose", "La fin d'un niveau",
             "La carte"],
    "ph": "Capture à venir",
    "endT": "Pas encore sorti.",
    "endS": "Palmo est encore à l'atelier. Les liens vers les stores seront "
            "ici le jour de la sortie.",
    "bandAlt": "Palmo",
    "legal": ("Confidentialité", "Conditions d'utilisation",
              "Suppression du compte"),
    "by": "Palmo est réalisé par",
    "back": "Retour à Palmo",
    "upd": "Dernière mise à jour",
    "e404T": "Il n'y a rien ici.",
    "e404S": "Cette page n'existe pas.",
}

T["pt"] = {
    "title": "Palmo - Teça o tabuleiro inteiro",
    "desc": "Um puzzle tranquilo. O número da semente diz quantas células a "
            "região tem; faça cada região crescer até o seu tamanho exato. Em "
            "breve para Android e iOS.",
    "badge": "Em breve",
    "h1a": "O número da semente",
    "h1b": "é o tamanho da sua região.",
    "lead": "Palmo é um puzzle tranquilo. Cada semente carrega um número, e "
            "esse número é quantas células pertencem a ela. Faça cada região "
            "crescer até o seu tamanho exato, até o tabuleiro ficar coberto e "
            "não sobrar nenhuma célula.",
    "small": "Grátis. Joga-se offline.",
    "shotsT": "Do jogo",
    "shotsS": "Capturas reais, não montagens.",
    "caps": ["O tabuleiro", "Uma região se assentando", "O fim de uma fase",
             "O mapa"],
    "ph": "Captura em breve",
    "endT": "Ainda não lançado.",
    "endS": "Palmo ainda está na oficina. No dia do lançamento os links das "
            "lojas estarão aqui.",
    "bandAlt": "Palmo",
    "legal": ("Privacidade", "Termos de uso", "Excluir conta"),
    "by": "Palmo é feito por",
    "back": "Voltar ao Palmo",
    "upd": "Última atualização",
    "e404T": "Não há nada aqui.",
    "e404S": "Essa página não existe.",
}


# ── yollar ──────────────────────────────────────────────────────────────────
#
# URL ile DOSYA ayri: URL dizin bicimindedir (/tr/), dosya her zaman
# index.html'dir. Colmo sitesinde canonical /index.html'i, x-default ise /'i
# gosteriyordu; ayni belge iki adresle isaret ediliyordu.

def path_for(code, page):
    """Yayindaki URL yolu. Acilis sayfasi dizin olarak biter."""
    d = "" if code == ROOT_LANG else code + "/"
    return d if page == "index.html" else d + page


def file_for(code, page):
    """Diskteki dosya yolu."""
    return page if code == ROOT_LANG else "%s/%s" % (code, page)


def langs_with(page):
    """Bu sayfanin gercekten uretildigi diller.

    Yasal sayfalar yalnizca LEGAL_LANGS icin uretiliyor. Colmo'da dil cubugu ve
    hreflang bu filtreyi bilmiyordu ve her yasal sayfa uretilmemis dort dosyaya
    baglanti veriyordu: sayfa basina dort olu baglanti, dort hatali alternate.
    """
    if page == "index.html":
        return [c for c, _l, _o, _n in LANGS]
    return [c for c, _l, _o, _n in LANGS if c in LEGAL_LANGS]


def has(rel):
    return os.path.exists(os.path.join(HERE, rel.replace("/", os.sep)))


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def inline_svg(rel, cls):
    """SVG'yi HTML'in icine gomer.

    <img> icindeki bir SVG belgenin yazi tiplerine ULASAMAZ. Kilit ve isaret
    Nunito 900 ile cizilmis <text> tasiyor; <img src> olarak konulsalardi
    ziyaretcinin sistem yazi tipiyle render olurlardi ve marka her makinede
    baska turlu gorunurdu. Gomulu SVG sayfanin fontunu kullanir.

    Kalici cozum harfleri outline'a cevirmektir (bkz. README); o gun bu
    fonksiyon durur, yalnizca dosyalar degisir.
    """
    raw = io.open(os.path.join(HERE, rel.replace("/", os.sep)),
                  encoding="utf-8").read().strip()
    m = re.match(r"<svg\b[^>]*>", raw)
    tag = re.sub(r'\s(width|height)="[^"]*"', "", m.group(0))
    tag = tag.replace("<svg", '<svg class="%s" focusable="false"' % cls, 1)
    return tag + raw[m.end():]


# ── iskelet ─────────────────────────────────────────────────────────────────

def head(code, page, title, desc, index=True):
    lang = dict((c, l) for c, l, _o, _n in LANGS)[code]
    loc = dict((c, o) for c, _l, o, _n in LANGS)[code]
    avail = langs_with(page)
    alts = "\n    ".join(
        '<link rel="alternate" hreflang="%s" href="%s/%s">'
        % (c, SITE, path_for(c, page)) for c in avail)
    # x-default sayfa bazli: gizlilik sayfasinin dil-notr karsiligi ana sayfa
    # degil, Ingilizce gizlilik sayfasidir.
    alts += ('\n    <link rel="alternate" hreflang="x-default" href="%s/%s">'
             % (SITE, path_for(ROOT_LANG, page)))

    og = ""
    if has(SHARE):
        og = ('\n    <meta property="og:image" content="%s/%s">'
              '\n    <meta property="og:image:width" content="1200">'
              '\n    <meta property="og:image:height" content="630">'
              '\n    <meta name="twitter:image" content="%s/%s">'
              % (SITE, SHARE, SITE, SHARE))
    touch = ('\n    <link rel="apple-touch-icon" href="/%s">' % ICON_PNG
             if has(ICON_PNG) else "")
    extra_css = ('\n    <link rel="stylesheet" href="/css/legal.css">'
                 if page != "index.html" else "")

    return """<!DOCTYPE html>
<html lang="%(lang)s">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="%(desc)s">
    <meta name="robots" content="%(robots)s">
    <meta property="og:type" content="website">
    <meta property="og:url" content="%(site)s/%(path)s">
    <meta property="og:title" content="%(title)s">
    <meta property="og:description" content="%(desc)s">
    <meta property="og:locale" content="%(loc)s">
    <meta property="og:site_name" content="%(app)s">%(og)s
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="%(title)s">
    <meta name="twitter:description" content="%(desc)s">
    <meta name="theme-color" content="#FFF4FB">
    <title>%(title)s</title>
%(canon)s    %(alts)s
    <link rel="icon" type="image/svg+xml" href="/%(mark)s">%(touch)s
    <link rel="manifest" href="/manifest.json">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/style.css">%(extra)s
</head>
<body>
""" % dict(lang=lang, desc=esc(desc), site=SITE, path=path_for(code, page),
           title=esc(title), loc=loc, alts=alts, og=og, touch=touch,
           app=APP, mark=MARK, extra=extra_css,
           robots="index, follow" if index else "noindex, follow",
           canon=('    <link rel="canonical" href="%s/%s">\n'
                  % (SITE, path_for(code, page)) if index else ""))


def lang_bar(code, page):
    avail = set(langs_with(page))
    out = []
    for c, _l, _o, name in LANGS:
        if c not in avail:
            continue
        cur = ' aria-current="page"' if c == code else ""
        out.append('<a href="/%s" hreflang="%s"%s>%s</a>'
                   % (path_for(c, page), c, cur, esc(name)))
    return '<div class="diller">%s</div>' % "".join(out)


def header(code, page):
    return """<header class="ust">
    <div class="kap">
        <a class="marka" href="/%(home)s">%(lockup)s</a>
        %(bar)s
    </div>
</header>
""" % dict(home=path_for(code, "index.html"), bar=lang_bar(code, page),
           lockup=inline_svg(LOCKUP, "kilit"))


def footer(code, t):
    p, tm, ad = t["legal"]
    lc = code if code in LEGAL_LANGS else ROOT_LANG
    return """<footer>
    <div class="kap">
        <span>%(by)s <a href="%(devurl)s">%(dev)s</a>.</span>
        <div class="f-baglantilar">
            <a href="/%(lp)s">%(p)s</a>
            <a href="/%(lt)s">%(tm)s</a>
            <a href="/%(la)s">%(ad)s</a>
        </div>
    </div>
    <div class="kap f-alt">&copy; 2026 %(dev)s &middot; %(pkg)s</div>
</footer>

</body>
</html>
""" % dict(by=esc(t["by"]), p=esc(p), tm=esc(tm), ad=esc(ad), pkg=PKG,
           dev=DEV, devurl=DEV_URL,
           lp=path_for(lc, "privacy.html"), lt=path_for(lc, "terms.html"),
           la=path_for(lc, "account-deletion.html"))


# ── acilis sayfasi ──────────────────────────────────────────────────────────

def _shot(rel, cap, ph, eager=False):
    """Kare varsa gercek goruntu, yoksa yer tutucu.

    Siteye oyun cizilmiyor. Yer tutucu bir ekran goruntusu taklidi degil, acikca
    bos bir cerceve: olmayan goruntuye baglanti vermek 404 uretir, temsili bir
    kare cizmek ise yalan olur.
    """
    if has("assets/shots/" + rel):
        return ('<img src="/assets/shots/%s" alt="%s" width="390" height="844" '
                'loading="%s">' % (rel, esc(cap), "eager" if eager else "lazy"))
    return ('<div class="yer-tutucu" role="img" aria-label="%s"><span>%s</span>'
            '</div>' % (esc(cap), esc(ph)))


def landing(code, t):
    """Acilis sayfasi.

    Iki kural Colmo'dan devralindi. SAYI VERILMIYOR: "24 bolum", "0 reklam"
    gibi sayilar sayfayi bir ozellik listesine cevirir ve bolum sayisi zaten
    degisecek. GORSEL UYDURULMUYOR: gorunen her kare oyunun kendi ekran
    goruntusu, yoksa acikca bos bir cerceve.

    Colmo'dan ayrilan yer: orada kural hic anlatilmiyordu. Palmo'nun kurali tek
    cumlede soyleniyor cunku "tohumdaki rakam bolgenin buyuklugudur" bir ozellik
    listesi degil, oyunun ne oldugunun kendisi. Bunun otesine gecilmiyor.
    """
    caps = t["caps"]
    shots = "".join(
        '<figure>%s<figcaption>%s</figcaption></figure>'
        % (_shot(f, c, t["ph"]), esc(c))
        for f, c in zip(SHOTS, caps))

    band = ""
    if has(SHARE):
        band = """
<section class="bant">
    <img src="/%(share)s" alt="%(alt)s" width="1200" height="630" loading="lazy">
</section>
""" % dict(share=SHARE, alt=esc(t["bandAlt"]))

    hero_gorsel = _shot(SHOTS[0], caps[0], t["ph"], eager=True)
    if not has("assets/shots/" + SHOTS[0]):
        # Ekran goruntusu yokken kahraman bos kalmasin: marka isareti bir
        # ekran taklidi degil, kendi varligimiz.
        hero_gorsel = inline_svg(MARK, "isaret")

    return (head(code, "index.html", t["title"], t["desc"])
            + header(code, "index.html")
            + """
<section class="kahraman">
    <div class="kap">
        <div>
            <span class="rozet">%(badge)s</span>
            <h1>%(h1a)s<br><em>%(h1b)s</em></h1>
            <p class="alt">%(lead)s</p>
            <p class="kucuk">%(small)s</p>
            <div class="magaza">
                <span class="magaza-cip">Google Play <b>%(badge)s</b></span>
                <span class="magaza-cip">App Store <b>%(badge)s</b></span>
            </div>
        </div>
        <div class="telefon">%(hero)s</div>
    </div>
</section>
%(band)s
<section class="duvar-bolum">
    <div class="kap">
        <h2>%(shotsT)s</h2>
        <p class="bolum-alt">%(shotsS)s</p>
        <div class="vitrin">%(shots)s</div>
    </div>
</section>

<section class="kapanis">
    <div class="kap">
        <div class="kutu">
            <h2>%(endT)s</h2>
            <p class="bolum-alt">%(endS)s</p>
        </div>
    </div>
</section>
""" % dict(badge=esc(t["badge"]), h1a=esc(t["h1a"]), h1b=esc(t["h1b"]),
           lead=esc(t["lead"]), small=esc(t["small"]), hero=hero_gorsel,
           band=band, shotsT=esc(t["shotsT"]), shotsS=esc(t["shotsS"]),
           shots=shots, endT=esc(t["endT"]), endS=esc(t["endS"]))
            + """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MobileApplication",
  "name": "%(app)s",
  "applicationCategory": "GameApplication",
  "operatingSystem": "Android, iOS",
  "url": "%(site)s/%(path)s",
  "inLanguage": "%(code)s",
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "TRY"},
  "publisher": {"@type": "Organization", "name": "%(dev)s"}
}
</script>
""" % dict(site=SITE, app=APP, dev=DEV, code=code,
           path=path_for(code, "index.html"))
            + footer(code, t))


def legal(code, t, page, title, desc, body):
    return (head(code, page, "%s - %s" % (title, APP), desc)
            + header(code, page)
            + """
<section class="yasal">
    <div class="kap">
        <a class="geri" href="/%(home)s">&larr; %(back)s</a>
        <h1>%(title)s</h1>
        <p class="tarih">%(upd)s: %(date)s</p>
        <div class="govde">%(body)s</div>
    </div>
</section>
""" % dict(home=path_for(code, "index.html"), back=esc(t["back"]),
           title=esc(title), date=UPDATED[page], body=body,
           upd=esc(t["upd"]))
            + footer(code, t))


# ── yazma ───────────────────────────────────────────────────────────────────

def write(rel, text):
    p = os.path.join(HERE, rel.replace("/", os.sep))
    d = os.path.dirname(p)
    if d:
        os.makedirs(d, exist_ok=True)
    io.open(p, "w", encoding="utf-8", newline="\n").write(text)
    return rel


def main():
    import legal_text

    made = []
    for code, _l, _o, _n in LANGS:
        t = T[code]
        made.append(write(file_for(code, "index.html"), landing(code, t)))
        if code in LEGAL_LANGS:
            for page, title, desc, body in legal_text.pages(code):
                made.append(write(file_for(code, page),
                                  legal(code, t, page, title, desc, body)))

    # ── sabit dosyalar ──────────────────────────────────────────────────
    made.append(write(".nojekyll", ""))
    made.append(write("robots.txt",
                      "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n"
                      % SITE))

    urls = []
    for c, _l, _o, _n in LANGS:
        urls.append("  <url><loc>%s/%s</loc></url>\n"
                    % (SITE, path_for(c, "index.html")))
        if c in LEGAL_LANGS:
            for p in LEGAL_PAGES:
                urls.append("  <url><loc>%s/%s</loc><lastmod>%s</lastmod>"
                            "</url>\n" % (SITE, path_for(c, p), UPDATED[p]))
    made.append(write("sitemap.xml",
                      '<?xml version="1.0" encoding="UTF-8"?>\n'
                      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                      '%s</urlset>\n' % "".join(urls)))

    # Ikon listesi: yalnizca diskte VAR olan dosyalar. Olmayan ikonu manifeste
    # yazmak tarayicida 404 uretir.
    icons = ['    {"src": "/%s", "sizes": "any", "type": "image/svg+xml"}'
             % MARK]
    for rel, size in (("assets/palmo-icon-192.png", "192x192"),
                      ("assets/palmo-icon-512.png", "512x512")):
        if has(rel):
            icons.append('    {"src": "/%s", "sizes": "%s", "type": '
                         '"image/png", "purpose": "any maskable"}'
                         % (rel, size))
    made.append(write("manifest.json",
                      '{\n'
                      '  "id": "/",\n'
                      '  "name": "%s",\n'
                      '  "short_name": "%s",\n'
                      '  "description": %s,\n'
                      '  "lang": "%s",\n'
                      '  "start_url": "/",\n'
                      '  "scope": "/",\n'
                      '  "display": "standalone",\n'
                      '  "background_color": "#FFF4FB",\n'
                      '  "theme_color": "#FFF4FB",\n'
                      '  "icons": [\n%s\n  ]\n}\n'
                      % (APP, APP,
                         '"%s"' % T[ROOT_LANG]["desc"].replace('"', '\\"'),
                         ROOT_LANG, ",\n".join(icons))))

    t = T[ROOT_LANG]
    made.append(write("404.html",
                      head(ROOT_LANG, "index.html", "404 - %s" % APP,
                           t["e404S"], index=False)
                      + header(ROOT_LANG, "index.html")
                      + '\n<section class="kapanis"><div class="kap">'
                        '<div class="kutu"><h2>%s</h2>'
                        '<p class="bolum-alt">%s <a href="/">%s</a>.</p>'
                        '</div></div></section>\n'
                        % (esc(t["e404T"]), esc(t["e404S"]), esc(t["back"]))
                      + footer(ROOT_LANG, t)))

    print("uretilen dosya: %d" % len(made))
    for m in sorted(made):
        print("  " + m)

    # ── derleme sonrasi uyarilar ────────────────────────────────────────
    warn = []
    cname = os.path.join(HERE, "CNAME")
    if not os.path.exists(cname):
        warn.append("CNAME yok. Icine tek satir yaz: %s (bkz. README)" % DOMAIN)
    else:
        got = io.open(cname, encoding="utf-8").read().strip()
        if got != DOMAIN:
            warn.append("CNAME icerigi '%s', config.DOMAIN ise '%s'"
                        % (got, DOMAIN))
    if not has(SHARE):
        warn.append("%s yok: og:image ve bant bolumu yazilmadi" % SHARE)
    if not has(ICON_PNG):
        warn.append("%s yok: apple-touch-icon yazilmadi" % ICON_PNG)
    eksik = [s for s in SHOTS if not has("assets/shots/" + s)]
    if eksik:
        warn.append("ekran goruntusu eksik (yer tutucuya dusuldu): %s"
                    % ", ".join(eksik))
    if warn:
        print("\nyapilacaklar:")
        for w in warn:
            print("  - " + w)


if __name__ == "__main__":
    main()
