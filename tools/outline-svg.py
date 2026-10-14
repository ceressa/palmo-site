# -*- coding: utf-8 -*-
"""Marka SVG'lerindeki <text> harflerini Nunito 900 konturuna cevirir.

    python tools/outline-svg.py assets/palmo-lockup-h.svg assets/palmo-mark.svg

Neden: kilit harfleri <text> iken sayfanin metni "4 P P a a l l m m o o"
oluyordu (her harf golge + renk olarak iki kez, ustune tohumdaki 4). Arama
motoru, okuma modu ve metin cikaran her arac bunu goruyordu. Kontur olunca
SVG'de metin kalmaz; erisilebilir ad yalnizca kokteki aria-label="Palmo".
Ikinci kazanc: favicon (`<img>` gibi okunan SVG) sayfanin fontuna
ulasamadigi icin "4"u sistem fontuyla ciziyordu.

Kaynak dosyalar `design-r3/assets/` altindaki <text>'li surumler. Marka
degisirse oradan yeniden kopyalanip bu arac kosulur.

Tarayici davranisi birebir taklit ediliyor:
  - text-anchor="middle": glif ilerlemesinin yarisi kadar sola.
  - dominant-baseline="central": em kutusunun ortasi y'ye oturur, yani
    alfabetik taban cizgisi y + (ascent - descent) / 2. Nunito
    USE_TYPO_METRICS bayragini tasiyor, ascent/descent typo degerleri.
"""
import io
import re
import sys

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT = r"E:\dev\mobile\palmo\assets\fonts\Nunito-Black.ttf"

TEXT_RE = re.compile(r"<text\b([^>]*)>([^<]*)</text>")
ATTR_RE = re.compile(r'([\w:-]+)="([^"]*)"')
DROP = {"x", "y", "text-anchor", "dominant-baseline", "font-family",
        "font-weight", "font-size"}


def _num(v):
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class _RoundPen(SVGPathPen):
    def _fmt(self, pt):
        return " ".join(_num(c) for c in pt)

    def _moveTo(self, pt):
        self._commands.append("M" + self._fmt(pt))

    def _lineTo(self, pt):
        self._commands.append("L" + self._fmt(pt))

    def _curveToOne(self, p1, p2, p3):
        self._commands.append("C" + " ".join(self._fmt(p) for p in (p1, p2, p3)))

    def _qCurveToOne(self, p1, p2):
        self._commands.append("Q" + " ".join(self._fmt(p) for p in (p1, p2)))

    def _closePath(self):
        self._commands.append("Z")


def outline(svg, font):
    upm = font["head"].unitsPerEm
    os2 = font["OS/2"]
    asc, desc = os2.sTypoAscender, -os2.sTypoDescender
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()

    # Her <text>'in font-size'i ya kendinde ya bir ust <g>'de (kilitte harfler
    # boyu gruptan aliyor). Acik <g>'ler yigitta tutulur.
    sizes = []
    stack = []
    for t in re.finditer(r"<(/?)(g|text)\b([^>]*)>", svg):
        close, name, raw = t.groups()
        if name == "g":
            if close:
                stack.pop()
            elif not raw.rstrip().endswith("/"):
                stack.append(dict(ATTR_RE.findall(raw)).get("font-size"))
        elif not close:
            own = dict(ATTR_RE.findall(raw)).get("font-size")
            inh = next((v for v in reversed(stack) if v), None)
            sizes.append(float(own or inh))
    sizes.reverse()

    def repl(m):
        attrs = dict(ATTR_RE.findall(m.group(1)))
        ch = m.group(2)
        if len(ch) != 1:
            sys.exit("tek harfli <text> bekleniyordu: %r" % ch)
        s = sizes.pop() / upm
        g = cmap[ord(ch)]
        x = float(attrs.get("x", 0))
        y = float(attrs.get("y", 0))
        if attrs.get("text-anchor") == "middle":
            x -= gs[g].width * s / 2
        if attrs.get("dominant-baseline") == "central":
            y += (asc - desc) * s / 2
        pen = _RoundPen(gs)
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, y)))
        keep = "".join(' %s="%s"' % (k, v) for k, v in attrs.items()
                       if k not in DROP)
        return '<path d="%s"%s/>' % (pen.getCommands(), keep)

    out = TEXT_RE.sub(repl, svg)
    # Harfler gitti, fonta dair oznitelikler artik bir sey yapmiyor.
    out = re.sub(r'\s(font-family|font-weight|font-size)="[^"]*"', "", out)
    # aria-label tek ad; <title> onunla birlikte iki kez okunuyordu.
    out = re.sub(r"<title>[^<]*</title>\n?", "", out)
    return out


def main(paths):
    font = TTFont(FONT)
    for p in paths:
        src = io.open(p, encoding="utf-8").read()
        if "<text" not in src:
            print("%s: <text> yok, atlandi" % p)
            continue
        io.open(p, "w", encoding="utf-8", newline="\n").write(outline(src, font))
        print("%s: donusturuldu" % p)


if __name__ == "__main__":
    main(sys.argv[1:])
