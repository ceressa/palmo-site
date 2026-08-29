# -*- coding: utf-8 -*-
"""Yasal sayfa metinleri.

Yalnizca Ingilizce ve Turkce tam yazildi; acilis sayfasi alti dilde ama
sozlesme dort dilde daha yarim cevrilmis olsa kimseye faydasi olmazdi.
Diger dillerdeki altbilgi baglantilari Ingilizce surume gider.

METIN URUNUN GERCEK MIMARISINI ANLATIR. Colmo'nun metni kopyalanmadi cunku
Palmo baska bir urun: `pubspec.yaml` icinde hicbir Firebase paketi yok, bulut
kaydi yok, hesap yok, analitik ve cokme raporu SDK'si yok. Buna karsilik
Colmo'da olmayan iki sey var: `in_app_purchase` (reklamsiz surum) ve
`app_tracking_transparency` (iOS izin akisi).

Kaynak dosyalar: `lib/state/economy.dart` (can, 11. bolum esigi, gunde 3 odullu
reklam, `noAds` bayragi), `lib/state/progress.dart` ve `lib/state/settings.dart`
(`shared_preferences`), `lib/l10n/strings.dart` (`reset_progress`).
Oradaki gercek degisirse burasi da degisir.
"""

from config import MAIL, PKG, DEV, APP


def _p(*paras):
    return "".join("<p>%s</p>" % x for x in paras)


def _ul(*items):
    return "<ul>%s</ul>" % "".join("<li>%s</li>" % x for x in items)


def _mail():
    return '<a href="mailto:%s">%s</a>' % (MAIL, MAIL)


# ── Gizlilik ────────────────────────────────────────────────────────────────

PRIVACY_EN = (
    "<h2>1. Overview</h2>"
    + _p("%s is a puzzle game. It runs on your device, it has no account and "
         "it has no server of ours behind it. Your progress never leaves the "
         "phone. This page describes the small amount of data the game handles "
         "and why." % APP)
    + "<h2>2. What stays on your device</h2>"
    + _ul(
        "<strong>Progress</strong>: which levels you cleared and how many "
        "stars each one holds.",
        "<strong>Settings</strong>: sound, music, haptics, path hints and the "
        "language you picked.",
        "<strong>Lives and their timer</strong>, the daily count of rewarded "
        "ads you watched, and whether you bought the ad-free version.")
    + _p("All of it is written with the operating system's own preference "
         "storage. None of it is uploaded, and none of it can be recovered by "
         "us: uninstalling the app removes it for good.")
    + "<h2>3. What leaves the device</h2>"
    + _ul(
        "<strong>Ads</strong> (Google AdMob): from level 11 onwards a "
        "full-screen ad can appear between levels. There is also an ad you may "
        "choose to watch to earn one life; it is always optional, capped per "
        "day, and nothing is taken from you if you skip it. To select and "
        "measure an ad, Google receives the device's advertising identifier "
        "and standard request data such as approximate region, device type and "
        "operating system version. In the EEA, the UK and Switzerland you are "
        "asked for consent before any of this happens, and your answer is "
        "stored on the device.",
        "<strong>App Tracking Transparency</strong> (iOS only): before "
        "anything is requested from the ad network, iOS asks whether the app "
        "may track you across other companies' apps and websites. Saying no "
        "changes nothing about the game; it only means the ads you see are not "
        "personalised.",
        "<strong>Purchases</strong>: the ad-free version is sold by Google "
        "Play and the App Store. Payment happens inside the store, we never "
        "see a card number or a billing address, and the app keeps only a "
        "yes/no flag on the device.")
    + "<h2>4. What we do not do</h2>"
    + _ul("No account, no name, no e-mail address, no sign-in.",
          "No cloud save. Nothing about your play is stored on a server we "
          "operate, because there is no such server.",
          "No separate analytics or crash-reporting SDK. The game does not "
          "record which levels you played or where you gave up.",
          "No location, no contacts, no photos, no microphone.",
          "No banner ads, and no ad at all before level 11.",
          "We do not sell your data. The only third parties that receive "
          "anything are Google (for ads) and the store you bought from, and "
          "only what serving an ad or completing a purchase requires.")
    + "<h2>5. Where the data lives</h2>"
    + _p("On your device. There is no cloud copy, no backup on our side and "
         "no record of you in any database of ours. What Google and Apple do "
         "with the data they receive is covered by their own privacy "
         "documentation.")
    + "<h2>6. Deletion</h2>"
    + _p("Uninstalling the app removes everything. You can also clear progress "
         "without uninstalling: <strong>Settings &rarr; Reset progress</strong>. "
         "See <a href=\"/account-deletion.html\">Account deletion</a> for the "
         "full picture.")
    + "<h2>7. Children</h2>"
    + _p("%s contains no chat and no user-generated content, and it collects "
         "no personal data from anyone. It is not directed at children. The "
         "game does show ads, so it is rated for a general audience rather "
         "than declared a children's app." % APP)
    + "<h2>8. Changes</h2>"
    + _p("Material changes to this policy will be published here with a new "
         "date. If the game ever gains a feature that sends more data - a "
         "cloud save, for instance - this page changes on the day that feature "
         "ships, not after.")
    + "<h2>9. Contact</h2>"
    + _p("%s &middot; %s" % (_mail(), PKG)))

PRIVACY_TR = (
    "<h2>1. Genel bakış</h2>"
    + _p("%s bir bulmaca oyunudur. Cihazında çalışır, hesap istemez ve "
         "arkasında bize ait bir sunucu yoktur. İlerlemen telefondan hiç "
         "çıkmaz. Bu sayfa, oyunun işlediği az miktardaki veriyi ve nedenini "
         "anlatır." % APP)
    + "<h2>2. Cihazında kalanlar</h2>"
    + _ul(
        "<strong>İlerleme</strong>: hangi bölümleri geçtiğin ve her birinde "
        "kaç yıldızın olduğu.",
        "<strong>Ayarlar</strong>: ses, müzik, titreşim, yol ipucu ve seçtiğin "
        "dil.",
        "<strong>Canlar ve sayacı</strong>, o gün kaç ödüllü reklam izlediğin "
        "ve reklamsız sürümü satın alıp almadığın.")
    + _p("Hepsi işletim sisteminin kendi tercih deposuna yazılır. Hiçbiri "
         "yüklenmez ve hiçbirini biz geri getiremeyiz: uygulamayı kaldırmak "
         "bunları kalıcı olarak siler.")
    + "<h2>3. Cihazdan çıkanlar</h2>"
    + _ul(
        "<strong>Reklamlar</strong> (Google AdMob): 11. bölümden itibaren "
        "bölüm aralarında tam ekran bir reklam çıkabilir. Ayrıca izlemeyi "
        "kendin seçersen bir can kazandıran bir reklam vardır; her zaman "
        "isteğe bağlıdır, günlük bir tavanı vardır ve izlemezsen hiçbir şey "
        "eksilmez. Reklamı seçmek ve ölçmek için Google, cihazın reklam "
        "kimliğini ve standart istek verisini alır: yaklaşık bölge, cihaz tipi, "
        "işletim sistemi sürümü. AEA, Birleşik Krallık ve İsviçre'de bunların "
        "hiçbiri olmadan önce sana rıza sorulur ve cevabın cihazda saklanır.",
        "<strong>App Tracking Transparency</strong> (yalnızca iOS): reklam "
        "ağından bir şey istenmeden önce iOS, uygulamanın seni başka "
        "şirketlerin uygulama ve sitelerinde takip edip edemeyeceğini sorar. "
        "Hayır demek oyunda hiçbir şeyi değiştirmez; yalnızca gördüğün "
        "reklamlar kişiselleştirilmemiş olur.",
        "<strong>Satın alma</strong>: reklamsız sürümü Google Play ve App "
        "Store satar. Ödeme mağazanın içinde olur, biz kart numarasını ya da "
        "fatura adresini hiç görmeyiz, uygulama cihazda yalnızca bir evet/hayır "
        "işareti tutar.")
    + "<h2>4. Yapmadıklarımız</h2>"
    + _ul("Hesap yok, isim yok, e-posta yok, giriş yok.",
          "Bulut kaydı yok. Oynayışına dair hiçbir şey bizim işlettiğimiz bir "
          "sunucuda durmuyor, çünkü öyle bir sunucu yok.",
          "Ayrı bir analitik ya da çökme raporu SDK'sı yok. Oyun hangi bölümü "
          "oynadığını ya da nerede bıraktığını kaydetmiyor.",
          "Konum, rehber, fotoğraf, mikrofon yok.",
          "Banner reklam yok, 11. bölümden önce hiç reklam yok.",
          "Veri satmıyoruz. Bir şey alan tek üçüncü taraflar Google (reklam "
          "için) ve satın aldığın mağaza; ikisi de yalnızca bir reklamı "
          "göstermek ya da bir satın almayı tamamlamak için gerekeni alıyor.")
    + "<h2>5. Verinin yaşadığı yer</h2>"
    + _p("Cihazın. Bulut kopyası yok, bizim tarafımızda yedek yok ve hiçbir "
         "veri tabanımızda sana ait bir kayıt yok. Google ile Apple'ın "
         "aldıkları veriyle ne yaptığı kendi gizlilik dokümantasyonlarına "
         "tabidir.")
    + "<h2>6. Silme</h2>"
    + _p("Uygulamayı kaldırmak her şeyi siler. Kaldırmadan da ilerlemeni "
         "temizleyebilirsin: <strong>Ayarlar &rarr; İlerlemeyi sıfırla</strong>. "
         "Tamamı için <a href=\"/tr/account-deletion.html\">Hesap silme</a> "
         "sayfasına bak.")
    + "<h2>7. Çocuklar</h2>"
    + _p("%s'da sohbet ve kullanıcı içeriği yoktur, kimseden kişisel veri "
         "toplamaz. Çocuklara yönelik değildir. Oyunda reklam gösterildiği için "
         "genel kitleye uygun olarak derecelendirilmiştir, çocuk uygulaması "
         "olarak beyan edilmemiştir." % APP)
    + "<h2>8. Değişiklikler</h2>"
    + _p("Bu politikadaki önemli değişiklikler yeni bir tarihle burada "
         "yayımlanır. Oyun ileride daha fazla veri gönderen bir özellik "
         "kazanırsa (örneğin bulut kaydı), bu sayfa o özelliğin çıktığı gün "
         "değişir, sonrasında değil.")
    + "<h2>9. İletişim</h2>"
    + _p("%s &middot; %s" % (_mail(), PKG)))

# ── Kullanim kosullari ──────────────────────────────────────────────────────

TERMS_EN = (
    "<h2>1. The short version</h2>"
    + "<div class=\"vurgu\">"
    + _p("%s is free to play. There is one optional purchase: removing ads. "
         "Play it, enjoy it, do not try to break it or resell it." % APP)
    + "</div>"
    + "<h2>2. Licence</h2>"
    + _p("%s grants you a personal, non-exclusive, non-transferable licence to "
         "install and play %s on devices you control. The game, its artwork, "
         "its levels, its sounds and its code remain ours." % (DEV, APP))
    + "<h2>3. What you agree not to do</h2>"
    + _ul("Reverse engineer, decompile or modify the app, except where that "
          "right cannot be excluded by law.",
          "Redistribute the app or its assets, or publish it under another "
          "name.",
          "Tamper with the game's stored state or with the store's purchase "
          "verification.")
    + "<h2>4. Your progress lives on your device</h2>"
    + _p("There is no cloud save. Progress, stars and lives are written on the "
         "phone and nowhere else. If you uninstall the app, reset the device "
         "or lose it, that progress is gone and we have no copy to restore. "
         "This is a deliberate trade: nothing about your play is stored on a "
         "server, and the price of that is that nothing can be recovered from "
         "one.")
    + "<h2>5. Purchases</h2>"
    + _ul("The ad-free version is a one-off purchase, not a subscription. It "
          "is tied to the store account you bought it with and can be restored "
          "on a new device from that same account.",
          "Payment, tax and invoicing are handled by Google Play or the App "
          "Store. We are not the seller of record and we never receive your "
          "payment details.",
          "Refunds follow the policy of the store you bought from. We cannot "
          "issue a refund ourselves, but write to us and we will tell you "
          "where to ask.",
          "Lives, stars and the shot budget are not currency. They cannot be "
          "bought, sold or transferred, and they have no value outside the "
          "game.")
    + "<h2>6. Availability and changes</h2>"
    + _p("The game may change. Levels can be rebalanced, features added or "
         "removed. Nothing here promises that a specific feature will exist "
         "forever. A purchase you already made is not taken away by such a "
         "change.")
    + "<h2>7. No warranty</h2>"
    + _p("%s is provided as is. To the extent permitted by law, we make no "
         "warranty that it will be uninterrupted or error free, and we are not "
         "liable for indirect or consequential loss arising from its use." % APP)
    + "<h2>8. Governing law</h2>"
    + _p("These terms are governed by the laws of the Republic of Turkiye. "
         "Nothing in them limits consumer rights you have under the law of the "
         "country you live in.")
    + "<h2>9. Contact</h2>"
    + _p("%s &middot; %s" % (_mail(), PKG)))

TERMS_TR = (
    "<h2>1. Kısa hali</h2>"
    + "<div class=\"vurgu\">"
    + _p("%s ücretsiz oynanır. İsteğe bağlı tek bir satın alma var: reklamları "
         "kaldırmak. Oyna, keyfini çıkar, kırmaya ve yeniden satmaya çalışma."
         % APP)
    + "</div>"
    + "<h2>2. Lisans</h2>"
    + _p("%s, %s'yu kendi kontrolündeki cihazlara kurup oynaman için kişisel, "
         "münhasır olmayan ve devredilemez bir lisans verir. Oyun, görselleri, "
         "bölümleri, sesleri ve kodu bize aittir." % (DEV, APP))
    + "<h2>3. Yapmamayı kabul ettiklerin</h2>"
    + _ul("Uygulamayı tersine mühendislik yapmak, kaynak koda çevirmek ya da "
          "değiştirmek (kanunen hariç tutulamayan haller dışında).",
          "Uygulamayı ya da varlıklarını yeniden dağıtmak, başka bir adla "
          "yayımlamak.",
          "Oyunun cihazda tuttuğu kayda ya da mağazanın satın alma "
          "doğrulamasına müdahale etmek.")
    + "<h2>4. İlerlemen cihazında durur</h2>"
    + _p("Bulut kaydı yoktur. İlerleme, yıldızlar ve canlar telefona yazılır, "
         "başka hiçbir yere yazılmaz. Uygulamayı kaldırırsan, cihazı "
         "sıfırlarsan ya da kaybedersen o ilerleme gider ve bizde geri "
         "yükleyecek bir kopya bulunmaz. Bu bilinçli bir takas: oynayışına dair "
         "hiçbir şey bir sunucuda durmuyor, bedeli de bir sunucudan hiçbir "
         "şeyin geri gelmemesi.")
    + "<h2>5. Satın alma</h2>"
    + _ul("Reklamsız sürüm tek seferlik bir satın almadır, abonelik değildir. "
          "Satın aldığın mağaza hesabına bağlıdır ve yeni bir cihazda aynı "
          "hesaptan geri yüklenebilir.",
          "Ödeme, vergi ve faturalama Google Play ya da App Store tarafından "
          "yürütülür. Kayıtlı satıcı biz değiliz ve ödeme bilgilerini hiç "
          "almayız.",
          "İade, satın aldığın mağazanın politikasına tabidir. İadeyi biz "
          "veremeyiz ama bize yazarsan nereye başvuracağını söyleriz.",
          "Canlar, yıldızlar ve vuruş bütçesi para birimi değildir. Satın "
          "alınamaz, satılamaz, devredilemez ve oyunun dışında bir değerleri "
          "yoktur.")
    + "<h2>6. Erişilebilirlik ve değişiklikler</h2>"
    + _p("Oyun değişebilir. Bölümler yeniden dengelenebilir, özellikler "
         "eklenebilir ya da kaldırılabilir. Burada hiçbir özelliğin sonsuza "
         "kadar var olacağı vaat edilmiyor. Halihazırda yaptığın bir satın "
         "alma böyle bir değişiklikle elinden alınmaz.")
    + "<h2>7. Garanti yok</h2>"
    + _p("%s olduğu gibi sunulur. Kanunun izin verdiği ölçüde, kesintisiz ya da "
         "hatasız çalışacağına dair bir garanti vermiyoruz ve kullanımından "
         "doğan dolaylı zararlardan sorumlu değiliz." % APP)
    + "<h2>8. Uygulanacak hukuk</h2>"
    + _p("Bu koşullar Türkiye Cumhuriyeti kanunlarına tabidir. Buradaki hiçbir "
         "hüküm, yaşadığın ülkenin kanunlarından doğan tüketici haklarını "
         "sınırlamaz.")
    + "<h2>9. İletişim</h2>"
    + _p("%s &middot; %s" % (_mail(), PKG)))

# ── Hesap silme ─────────────────────────────────────────────────────────────
#
# Sayfa "hesap yok" diye kaldirilmadi: magazalar bu baglantiyi ariyor ve
# hicbir sey saklamadigimizi soylemek de bir cevaptir.

DELETE_EN = (
    "<h2>There is no account</h2>"
    + "<div class=\"vurgu\">"
    + _p("%s has no sign-up, no login and no cloud save. We hold no record of "
         "you, so there is no remote account for us to delete." % APP)
    + "</div>"
    + "<h2>Deleting your progress</h2>"
    + _ul("<strong>Without uninstalling</strong>: "
          "<strong>Settings &rarr; Reset progress</strong>. Levels and stars "
          "are cleared; your sound and language preferences stay.",
          "<strong>Completely</strong>: uninstall the app. Progress, settings, "
          "lives and the ad-free flag all go with it.")
    + _p("Both are immediate and neither needs our involvement. Nothing is "
         "kept in a backup afterwards, because there was never a copy "
         "anywhere else.")
    + "<h2>What we cannot delete</h2>"
    + _ul("<strong>Your purchase record.</strong> If you bought the ad-free "
          "version, the receipt belongs to Google Play or the App Store. Ask "
          "them; we have no access to it, and deleting it there would also "
          "remove your right to restore the purchase.",
          "<strong>What the ad network received.</strong> Google's handling of "
          "the advertising identifier is covered by its own documentation. You "
          "can reset or disable that identifier in your device settings at any "
          "time.")
    + "<h2>If you have written to us</h2>"
    + _p("An e-mail you sent stays in the mailbox until you ask us to remove "
         "it. Write to %s with the subject <strong>%s data request</strong> "
         "and we will delete the correspondence." % (_mail(), APP))
    + "<h2>Contact</h2>"
    + _p("%s &middot; %s" % (_mail(), PKG)))

DELETE_TR = (
    "<h2>Hesap diye bir şey yok</h2>"
    + "<div class=\"vurgu\">"
    + _p("%s'da kayıt, giriş ve bulut kaydı yoktur. Sana ait hiçbir kaydımız "
         "olmadığı için silinecek uzak bir hesap da yok." % APP)
    + "</div>"
    + "<h2>İlerlemeni silme</h2>"
    + _ul("<strong>Kaldırmadan</strong>: "
          "<strong>Ayarlar &rarr; İlerlemeyi sıfırla</strong>. Bölümler ve "
          "yıldızlar temizlenir; ses ve dil tercihlerin kalır.",
          "<strong>Tamamen</strong>: uygulamayı kaldır. İlerleme, ayarlar, "
          "canlar ve reklamsız işareti onunla birlikte gider.")
    + _p("İkisi de anında olur ve ikisi için de bize ihtiyacın yok. "
         "Sonrasında hiçbir yedek tutulmuyor, çünkü zaten başka bir yerde "
         "kopyası hiç olmadı.")
    + "<h2>Silemediklerimiz</h2>"
    + _ul("<strong>Satın alma kaydın.</strong> Reklamsız sürümü aldıysan "
          "makbuz Google Play'e ya da App Store'a aittir. Onlara sor; bizim "
          "erişimimiz yok ve orada silmek satın almayı geri yükleme hakkını da "
          "ortadan kaldırır.",
          "<strong>Reklam ağının aldıkları.</strong> Google'ın reklam kimliğini "
          "nasıl işlediği kendi dokümantasyonuna tabidir. O kimliği cihaz "
          "ayarlarından istediğin zaman sıfırlayabilir ya da kapatabilirsin.")
    + "<h2>Bize yazdıysan</h2>"
    + _p("Gönderdiğin e-posta, sen istemedikçe posta kutusunda kalır. %s "
         "adresine <strong>%s veri talebi</strong> konusuyla yaz, yazışmayı "
         "silelim." % (_mail(), APP))
    + "<h2>İletişim</h2>"
    + _p("%s &middot; %s" % (_mail(), PKG)))


# Baslik ve meta aciklama sayfa basina. Colmo'da yasal sayfalarin meta
# aciklamasi acilis sayfasindan kopyaydi ve dort sayfa ayni metinle
# indeksleniyordu.
_PAGES = {
    "en": [
        ("privacy.html", "Privacy policy",
         "What %s stores on your device, what leaves it, and what we never "
         "collect. No account, no cloud save." % APP,
         PRIVACY_EN),
        ("terms.html", "Terms of use",
         "The licence, the one optional purchase, and what happens to progress "
         "that lives only on your device.",
         TERMS_EN),
        ("account-deletion.html", "Account deletion",
         "%s has no account and no cloud save. How to clear your progress and "
         "what we cannot delete for you." % APP,
         DELETE_EN),
    ],
    "tr": [
        ("privacy.html", "Gizlilik politikası",
         "%s'nın cihazında ne sakladığı, cihazdan ne çıktığı ve hiç "
         "toplamadıklarımız. Hesap yok, bulut kaydı yok." % APP,
         PRIVACY_TR),
        ("terms.html", "Kullanım koşulları",
         "Lisans, isteğe bağlı tek satın alma ve yalnızca cihazında duran "
         "ilerlemenin başına gelenler.",
         TERMS_TR),
        ("account-deletion.html", "Hesap silme",
         "%s'da hesap ve bulut kaydı yoktur. İlerlemeni nasıl temizlersin, "
         "senin adına neyi silemeyiz." % APP,
         DELETE_TR),
    ],
}


def pages(code):
    """(dosya, baslik, meta aciklama, govde) dortlulerini dondurur."""
    return _PAGES.get(code, _PAGES["en"])
