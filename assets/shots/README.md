# assets/shots

Vitrin bolumunun dort karesi. Dosya yoksa `build.py` o kutuyu **yer tutucuya**
dusuruyor: olmayan goruntuye baglanti verilmiyor ve temsili bir kare
cizilmiyor. Dosyayi koyup `python build.py` calistirmak yeterli, HTML kendini
duzeltir.

| Dosya | Ne olmali |
|---|---|
| `01_board.webp` | Oyun ekrani: tohumlar duruyor, en az bir bolge oturmus. Kahraman gorseli de budur. |
| `02_settle.webp` | Bir bolgenin yerine oturdugu an (ic isik basamagi gorunsun). |
| `03_result.webp` | Bolum sonu paneli, yildizlar damgalanmis. |
| `04_map.webp` | Harita izgarasi, bir kismi acik bir kismi kilitli. |

## Kurallar

- **Gercek ekran goruntusu.** Photoshop'ta duzeltilmis, cerceveye oturtulmus ya
  da temsili olarak cizilmis kare konulmaz. Aile kurali: gorunen her kare
  oyunun kendisinden gelir.
- **Olcu 390 x 844** (mantiksal ekran, `design-r3/tokens/space.css`). HTML'de
  `width="390" height="844"` sabit yaziliyor. Baska bir olcude cekilirse
  `build.py` icindeki `_shot()` fonksiyonundaki degerler de degismeli, yoksa
  sayfa yuklenirken zipliyor.
- **Bicim webp.** Dosya adlari `build.py` tepesindeki `SHOTS` listesinde.
- Metin tasiyan ekranlar (harita, sonuc paneli) **Ingilizce** cekilsin: kok dil
  Ingilizce ve ayni kareler alti dilde de gosteriliyor.

## Ayrica gereken, buraya degil bir ust klasore

- `assets/palmo-share.png` - 1200x630. Konulunca `og:image` etiketleri ve tam
  genislikteki bant bolumu kendiliginden yaziliyor; yokken ikisi de yok.
- `assets/palmo-icon.png` - 180x180, `apple-touch-icon`.
- `assets/palmo-icon-192.png`, `assets/palmo-icon-512.png` - manifest ikonlari.
