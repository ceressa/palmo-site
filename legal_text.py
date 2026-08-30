# -*- coding: utf-8 -*-
"""Yasal sayfa metinleri.

Yalnizca Ingilizce ve Turkce tam yazildi; acilis sayfasi alti dilde ama
sozlesme dort dilde daha yarim cevrilmis olsa kimseye faydasi olmazdi.
Diger dillerdeki altbilgi baglantilari Ingilizce surume gider.

METIN URUNUN GERCEK MIMARISINI ANLATIR. 2026-08-30'da tamami yeniden
yazildi: onceki surum "hesap yok, bulut kaydi yok, analitik ve cokme raporu
SDK'si yok" iddiasi uzerine kuruluydu ve bu iddialarin HEPSI gecersiz oldu.
`pubspec.yaml` artik firebase_core, firebase_auth, cloud_firestore,
firebase_analytics, firebase_crashlytics, google_sign_in ve
sign_in_with_apple tasiyor. Play magaza formu bu sayfalarin adresini
gosterecek; beyanla celisen sayfa incelemeyi takar.

Kaynak dosyalar ve metnin hangisinden dogruladigi:
  `lib/cloud_sync.dart`     anonim kimlik, `kCloudFields` listesi, baglama,
                            `deleteAccount()` sirasi (once belge sonra kimlik)
  `firestore.rules`         `/users/{uid}`, `isOwner`, varsayilan ret
  `lib/telemetry.dart`      olay adlari, daraltilmis riza, Crashlytics uid
  `lib/ads.dart`            AdMob, 11. bolum esigi, UMP, ATT
  `lib/state/economy.dart`  can, gunluk reklam tavanlari, `noAds`
  `lib/billing.dart`        `com.bardino.palmo.remove_ads`, non-consumable
  `lib/ui/settings_page.dart` menu yollari ve HANGI satirin ne zaman cizildigi
  `lib/l10n/strings.dart`   uygulamadaki tam etiketler (adim adim anlatim
                            oyuncunun ekranda gordugu kelimeyi kullanmali)
Oradaki gercek degisirse burasi da degisir.

IKI SEY BILEREK BOYLE YAZILDI, kisaltilmasin:
  1. "Ilerlemeyi sifirla" buluttaki BELGEYI SILMEZ. Yerel durumu temizler,
     sonraki esitleme o temiz durumu belgenin uzerine yazar (`push` merge'siz
     `set` kullaniyor). Belgeyi ve kimligi silen tek yol "Hesabi sil".
  2. "Hesabi sil" satiri yalnizca Google/Apple BAGLIYKEN ciziliyor
     (`settings_page.dart`, `_accountRows`). Anonim oyuncuya gorunmuyor;
     silme sayfasi bu yuzden anonim oyuncuya ayri bir yol tarif ediyor.
"""

from config import MAIL, PKG, DEV, APP


def _p(*paras):
    return "".join("<p>%s</p>" % x for x in paras)


def _ul(*items):
    return "<ul>%s</ul>" % "".join("<li>%s</li>" % x for x in items)


def _ol(*items):
    """Numarali adim listesi.

    Google'in veri silme formu "kullanicinin uygulamasi gereken adimlari
    belirgin sekilde goster" diyor ve isaretli liste bir SIRA soylemiyor.
    `css/legal.css` icinde `ul` ile ayni girintiyi aliyor.
    """
    return "<ol>%s</ol>" % "".join("<li>%s</li>" % x for x in items)


def _mail():
    return '<a href="mailto:%s">%s</a>' % (MAIL, MAIL)


# ── Gizlilik ────────────────────────────────────────────────────────────────

PRIVACY_EN = (
    "<h2>1. Overview</h2>"
    + _p("%s is a puzzle game made by %s. This page says what the game keeps "
         "on your phone, what it sends away, who receives it and how to get "
         "rid of it." % (APP, DEV),
         "It describes the game as it is built today, including the cloud "
         "save, the optional sign-in, the analytics events and the crash "
         "reporting. An earlier version of this page described a build that "
         "had none of those; it was replaced on the day they shipped.")
    + "<h2>2. Your identity in the game</h2>"
    + _p("The first time you open %s it asks Firebase Authentication for an "
         "<strong>anonymous identity</strong>. This happens on its own. You "
         "are not asked for a name, an e-mail address or a phone number, "
         "there is no sign-up screen and there is no login wall anywhere in "
         "the game. The identity is a random string, and its only job is to "
         "be the name of the folder your cloud save sits in." % APP)
    + _p("Linking a <strong>Google</strong> or <strong>Apple</strong> account "
         "is optional. Its only purpose is to let you pick the game up on a "
         "second device, or on the same device after a reinstall. Linking "
         "converts the anonymous identity instead of making a new one, so the "
         "save you already have stays exactly where it is.")
    + _ul("<strong>Google</strong>: signing in passes an ID token to Firebase, "
          "which is what proves the account is yours.",
          "<strong>Apple</strong>: offered on iOS. The game requests the "
          "e-mail scope only. Apple may hand back a relay address, or no "
          "address at all, and only on the first authorisation.",
          "If an address does come back, Firebase Authentication keeps it on "
          "the device and the Settings screen shows it so you can see which "
          "account you are on. Where no address is available, that row reads "
          "<em>Linked</em> instead.")
    + "<h2>3. What stays on your device</h2>"
    + _p("All of this is written with the operating system's own preference "
         "storage. It is the game's real memory: the cloud copy described in "
         "the next section is made from it, not the other way round.")
    + _ul("<strong>Progress</strong>: which levels you cleared, how many stars "
          "each one holds, and the lifetime counts of regions settled, cells "
          "taken and nine-cell regions.",
          "<strong>Settings</strong>: sound, music, haptics, path hints and "
          "the language you picked.",
          "<strong>Lives and their timer</strong>, how many rewarded ads you "
          "watched today, and whether you bought the ad-free version.",
          "<strong>Jokers</strong>, and a note of which chapter rewards have "
          "already been paid out.",
          "<strong>Housekeeping</strong>: how long it has been since the last "
          "ad, whether you have seen the tutorial, your answer to the ad "
          "consent form, and a random identifier generated on the device that "
          "marks which install last wrote to the cloud. That identifier is "
          "made by the game, not read from the phone; reinstalling produces a "
          "new one.")
    + "<h2>4. What is saved to the cloud</h2>"
    + _p("The game keeps one document per player in Cloud Firestore, at the "
         "path <strong>/users/{your identity}</strong>. There are no other "
         "collections and no sub-documents. It holds:")
    + _ul("levels cleared and stars per level;",
          "the lifetime counters (regions settled, cells taken, nine-cell "
          "regions);",
          "joker counts and the chapter rewards already paid;",
          "which lessons you have been taught and whether the tutorial has "
          "been seen;",
          "your settings: music, sound, haptics, path hints and language;",
          "three bookkeeping fields: a format version, the identifier of the "
          "install that wrote last, and a server timestamp of that write.")
    + _p("<strong>Three things are deliberately not sent</strong>: your lives "
         "and their timer, your daily rewarded-ad counts, and the ad-free "
         "flag. Lives are a timer rather than a possession, and the ad-free "
         "purchase belongs to the store, which is the only thing that can "
         "confirm it.")
    + _p("The database rules require that a request is signed in and that the "
         "identity in the request matches the identity in the path, for "
         "reading, writing and deleting alike. There is no query that lists "
         "the collection, so one save cannot be reached from another. Every "
         "path outside this one is refused by default. The rules are "
         "published as part of every deployment.")
    + _p("The cloud copy is a convenience. If Firebase cannot start, if the "
         "network is down or if a write is refused, the game carries on from "
         "the copy on your phone.")
    + "<h2>5. Analytics</h2>"
    + _p("The game sends Firebase Analytics a short list of events, all of "
         "them about the board rather than about you:")
    + _ul("a level was opened, and a level was finished with its star count, "
          "its duration and how many settled regions you pulled apart;",
          "a level ended without being solved, split into the case where the "
          "board ran out of moves and the case where you left it;",
          "a board reached a dead end, and how much budget was left;",
          "a settled region was pulled apart;",
          "a joker was used, and which of the three it was;",
          "an ad was shown, and whether it paid out;",
          "the ad-free version was bought;",
          "an account was linked, and whether it was Google or Apple.")
    + _p("Consent for analytics is narrowed in code before the first event is "
         "sent: ad storage, ad personalisation signals and ad user data are "
         "all set to denied, and only analytics storage is allowed. The "
         "anonymous identity is not passed to Analytics, so these events "
         "arrive as counts rather than as a profile. There is no level of "
         "detail here that could carry a name, a message or anything you "
         "typed, because the game has no text entry of any kind.")
    + "<h2>6. Crash reports</h2>"
    + _p("Firebase Crashlytics records crashes and the handled errors that "
         "should not pass silently, such as a refused cloud write or a "
         "sign-in that failed. A report contains the stack trace and the "
         "device information the Crashlytics library collects itself: device "
         "model, operating system version and app version.")
    + _p("Two things are attached deliberately. The first is the number of the "
         "level you were on. The second is your anonymous identity, so that a "
         "crash can be matched with the cloud save it belongs to when we are "
         "working out what went wrong. That identity is a random string with "
         "no name, e-mail address or device identifier in it.")
    + "<h2>7. Ads</h2>"
    + _ul("<strong>Between levels</strong> (Google AdMob): from level 11 "
          "onwards a full-screen ad can appear, at most one every four levels "
          "and not within three minutes of the last one. There is never an ad "
          "after a level that ended with zero stars, and there are no banner "
          "ads anywhere.",
          "<strong>Ads you choose to watch</strong>: one earns a life, another "
          "earns a joker. Both are optional, both are capped per day, and "
          "skipping them takes nothing away from you.",
          "<strong>What Google receives</strong>: to select and measure an ad, "
          "the device's advertising identifier and standard request data such "
          "as approximate region, device type and operating system version. "
          "You can reset or switch off that identifier in your device "
          "settings at any time.",
          "<strong>Consent</strong>: in the EEA and the UK, and anywhere else "
          "Google's rules require it, Google's consent form is shown before "
          "the ad library is started, and your answer is stored on the "
          "device. You are not stuck with that first answer: where the form "
          "applies, Settings carries an <strong>Ad privacy</strong> row that "
          "reopens it. Where it does not apply the row is not drawn, because "
          "a row that does nothing when tapped is worse than no row.",
          "<strong>App Tracking Transparency</strong> (iOS only): before "
          "anything is requested from the ad network, iOS asks whether the app "
          "may track you across other companies' apps and websites. Saying no "
          "changes nothing about the game; it only means the ads you see are "
          "not personalised.")
    + "<h2>8. Purchases</h2>"
    + _p("There is one purchase, it removes the ads, and it is a one-off "
         "rather than a subscription. It is sold by Google Play and the App "
         "Store: payment happens inside the store, we are not the seller of "
         "record, and no card number or billing address reaches us. The game "
         "keeps a yes/no flag on the device and asks the store to confirm it "
         "again on a new one.")
    + "<h2>9. Deleting your data</h2>"
    + _p("You can delete the cloud save and the identity it is filed under "
         "from inside the game, and you can clear the copy on your phone "
         "separately. The steps for each, and what each one does not cover, "
         "are set out on the <a href=\"/account-deletion.html\">Account "
         "deletion</a> page.")
    + "<h2>10. Children</h2>"
    + _p("%s contains no chat and no user-generated content, and there is "
         "nowhere in it to type anything. It is not directed at children. The "
         "game does show ads, so it is rated for a general audience rather "
         "than declared a children's app." % APP)
    + "<h2>11. Changes</h2>"
    + _p("Material changes to this page are published here with a new date. "
         "When the game gained cloud save, sign-in and measurement, this page "
         "was rewritten rather than patched, because the previous version "
         "said the opposite. The same applies next time.")
    + "<h2>12. Contact</h2>"
    + _p("%s &middot; %s" % (_mail(), PKG)))

PRIVACY_TR = (
    "<h2>1. Genel bakış</h2>"
    + _p("%s, %s tarafından yapılan bir bulmaca oyunudur. Bu sayfa oyunun "
         "telefonunda ne tuttuğunu, dışarı ne gönderdiğini, kimin aldığını ve "
         "bunlardan nasıl kurtulacağını anlatır." % (APP, DEV),
         "Anlatılan şey oyunun bugünkü hali: bulut kaydı, isteğe bağlı giriş, "
         "ölçüm olayları ve çökme raporlaması dahil. Bu sayfanın önceki "
         "sürümü bunların hiçbirinin bulunmadığı bir yapıyı anlatıyordu; "
         "özellikler çıktığı gün değiştirildi.")
    + "<h2>2. Oyundaki kimliğin</h2>"
    + _p("%s'yu ilk açtığında Firebase Authentication'dan bir "
         "<strong>anonim kimlik</strong> ister. Bu kendiliğinden olur. Senden "
         "isim, e-posta ya da telefon istenmez, kayıt ekranı yoktur ve oyunun "
         "hiçbir yerinde giriş kapısı yoktur. Kimlik rastgele bir dizedir ve "
         "tek işi, bulut kaydının durduğu klasörün adı olmaktır." % APP)
    + _p("<strong>Google</strong> ya da <strong>Apple</strong> hesabı bağlamak "
         "isteğe bağlıdır. Tek amacı oyunu ikinci bir cihazda, ya da aynı "
         "cihazda yeniden kurduktan sonra kaldığın yerden sürdürebilmendir. "
         "Bağlama, yeni bir kimlik üretmez, var olan anonim kimliği dönüştürür; "
         "yani elindeki kayıt yerinden kıpırdamaz.")
    + _ul("<strong>Google</strong>: giriş, Firebase'e bir kimlik jetonu "
          "iletir; hesabın senin olduğunu kanıtlayan şey odur.",
          "<strong>Apple</strong>: iOS'ta sunulur. Oyun yalnızca e-posta "
          "kapsamını ister. Apple bir takma adres verebilir, hiç adres "
          "vermeyebilir, verirse de yalnızca ilk yetkilendirmede verir.",
          "Bir adres geldiyse Firebase Authentication onu cihazda tutar ve "
          "Ayarlar ekranı hangi hesapta olduğunu görebilesin diye gösterir. "
          "Adres yoksa o satırda <em>Bağlı</em> yazar.")
    + "<h2>3. Cihazında kalanlar</h2>"
    + _p("Bunların hepsi işletim sisteminin kendi tercih deposuna yazılır. "
         "Oyunun asıl hafızası burasıdır: bir sonraki bölümde anlatılan bulut "
         "kopyası buradan üretilir, tersi değil.")
    + _ul("<strong>İlerleme</strong>: hangi bölümleri geçtiğin, her birinde "
          "kaç yıldızın olduğu ve ömür boyu oturttuğun bölge, aldığın hücre, "
          "kurduğun dokuz hücrelik bölge sayıları.",
          "<strong>Ayarlar</strong>: ses, müzik, titreşim, yol ipucu ve "
          "seçtiğin dil.",
          "<strong>Canlar ve sayacı</strong>, o gün kaç ödüllü reklam "
          "izlediğin ve reklamsız sürümü satın alıp almadığın.",
          "<strong>Jokerler</strong> ve hangi bölük ödüllerinin ödendiği.",
          "<strong>İç işleyiş</strong>: son reklamdan bu yana geçen süre, "
          "öğreticiyi görüp görmediğin, reklam rıza formuna verdiğin cevap, ve "
          "buluta en son hangi kurulumun yazdığını işaretleyen, cihazda "
          "üretilmiş rastgele bir işaret. O işaret telefondan okunmaz, oyun "
          "tarafından üretilir; uygulamayı yeniden kurmak yenisini yaratır.")
    + "<h2>4. Buluta gidenler</h2>"
    + _p("Oyun, Cloud Firestore'da oyuncu başına tek bir belge tutar; yolu "
         "<strong>/users/{kimliğin}</strong>. Başka koleksiyon ve alt belge "
         "yoktur. Belgede şunlar durur:")
    + _ul("geçtiğin bölümler ve bölüm başına yıldız;",
          "ömür boyu sayaçlar (oturtulan bölge, alınan hücre, dokuz hücrelik "
          "bölge);",
          "joker sayıları ve ödenmiş bölük ödülleri;",
          "hangi dersleri öğrendiğin ve öğreticinin görülüp görülmediği;",
          "ayarların: müzik, ses, titreşim, yol ipucu ve dil;",
          "üç tane defter alanı: biçim sürümü, en son yazan kurulumun işareti "
          "ve o yazmanın sunucu zaman damgası.")
    + _p("<strong>Üç şey bilerek gönderilmiyor</strong>: canların ve sayacı, "
         "günlük ödüllü reklam hakların, ve reklamsızlık işareti. Can bir "
         "varlık değil bir zaman kapısıdır; reklamsız satın alma ise "
         "mağazaya aittir ve onu doğrulayabilecek tek yer mağazadır.")
    + _p("Veri tabanı kuralları, isteğin giriş yapmış olmasını ve istekteki "
         "kimliğin yoldaki kimlikle aynı olmasını şart koşar; okumada, yazmada "
         "ve silmede aynı şekilde. Koleksiyonu listeleyen bir sorgu "
         "tanımlanmadığı için bir kayıttan başka bir kayda ulaşılamaz. Bu "
         "yolun dışındaki her yol varsayılan olarak reddedilir. Kurallar her "
         "dağıtımın parçası olarak yayımlanır.")
    + _p("Bulut kopyası bir kolaylıktır. Firebase başlatılamazsa, ağ yoksa ya "
         "da bir yazma reddedilirse oyun telefonundaki kopyadan devam eder.")
    + "<h2>5. Ölçüm</h2>"
    + _p("Oyun, Firebase Analytics'e kısa bir olay listesi gönderir; hepsi "
         "seninle değil tahtayla ilgilidir:")
    + _ul("bir bölüm açıldı, ve bir bölüm bitti: yıldızı, süresi ve kaç "
          "oturmuş bölgeyi söktüğün;",
          "bir bölüm çözülmeden bitti: tahtanın hamlesi kalmadığı durum ile "
          "senin bıraktığın durum ayrı ayrı;",
          "tahta çıkmaza düştü, ve geriye ne kadar bütçe kaldı;",
          "oturmuş bir bölge söküldü;",
          "joker kullanıldı, ve üçünden hangisi olduğu;",
          "reklam gösterildi, ve bir şey kazandırıp kazandırmadığı;",
          "reklamsız sürüm satın alındı;",
          "hesap bağlandı, ve Google mı Apple mı olduğu.")
    + _p("Ölçüm rızası ilk olay gönderilmeden önce kodda daraltılır: reklam "
         "depolaması, reklam kişiselleştirme sinyalleri ve reklam kullanıcı "
         "verisi reddedilmiş olarak ayarlanır, yalnızca ölçüm depolamasına "
         "izin verilir. Anonim kimlik Analytics'e verilmez; yani bu olaylar "
         "bir profil olarak değil, toplam olarak birikir. Burada isim, mesaj "
         "ya da yazdığın bir şeyi taşıyabilecek bir ayrıntı yok, çünkü oyunda "
         "hiçbir yazı girişi yok.")
    + "<h2>6. Çökme raporları</h2>"
    + _p("Firebase Crashlytics, çökmeleri ve sessiz kalmaması gereken "
         "yakalanmış hataları kaydeder: reddedilen bir bulut yazması ya da "
         "başarısız bir giriş gibi. Bir rapor, yığın izini ve Crashlytics "
         "kitaplığının kendi topladığı cihaz bilgisini içerir: cihaz modeli, "
         "işletim sistemi sürümü ve uygulama sürümü.")
    + _p("İki şey bilerek ekleniyor. Birincisi o an bulunduğun bölümün "
         "numarası. İkincisi anonim kimliğin: bir çökmenin hangi bulut "
         "kaydına denk geldiğini, neyin bozulduğunu ararken eşleştirebilmek "
         "için. O kimlik rastgele bir dizedir; içinde isim, e-posta ya da "
         "cihaz kimliği yoktur.")
    + "<h2>7. Reklamlar</h2>"
    + _ul("<strong>Bölüm aralarında</strong> (Google AdMob): 11. bölümden "
          "itibaren tam ekran bir reklam çıkabilir; en fazla dört bölümde bir "
          "ve son reklamdan üç dakika geçmeden değil. Sıfır yıldızla biten bir "
          "bölümden sonra asla reklam yoktur ve hiçbir yerde banner reklam "
          "yoktur.",
          "<strong>İzlemeyi kendin seçtiğin reklamlar</strong>: biri can, "
          "diğeri joker kazandırır. İkisi de isteğe bağlıdır, ikisinin de "
          "günlük tavanı vardır ve izlemezsen hiçbir şey eksilmez.",
          "<strong>Google'ın aldığı</strong>: reklamı seçmek ve ölçmek için "
          "cihazın reklam kimliği ve standart istek verisi: yaklaşık bölge, "
          "cihaz tipi, işletim sistemi sürümü. O kimliği cihaz ayarlarından "
          "istediğin zaman sıfırlayabilir ya da kapatabilirsin.",
          "<strong>Rıza</strong>: AEA ve Birleşik Krallık'ta, ve Google'ın "
          "kurallarının gerektirdiği diğer yerlerde, reklam kitaplığı "
          "başlatılmadan önce Google'ın rıza formu gösterilir ve cevabın "
          "cihazda saklanır. İlk cevabına mahkûm değilsin: formun geçerli "
          "olduğu yerlerde Ayarlar'da formu yeniden açan bir "
          "<strong>Reklam gizliliği</strong> satırı var. Geçerli olmadığı "
          "yerlerde satır çizilmiyor, çünkü dokununca hiçbir şey yapmayan bir "
          "satır, hiç olmamasından kötüdür.",
          "<strong>App Tracking Transparency</strong> (yalnızca iOS): reklam "
          "ağından bir şey istenmeden önce iOS, uygulamanın seni başka "
          "şirketlerin uygulama ve sitelerinde takip edip edemeyeceğini sorar. "
          "Hayır demek oyunda hiçbir şeyi değiştirmez; yalnızca gördüğün "
          "reklamlar kişiselleştirilmemiş olur.")
    + "<h2>8. Satın alma</h2>"
    + _p("Tek bir satın alma var, reklamları kaldırıyor ve abonelik değil tek "
         "seferlik. Google Play ve App Store satıyor: ödeme mağazanın içinde "
         "olur, kayıtlı satıcı biz değiliz, kart numarası ya da fatura adresi "
         "bize ulaşmaz. Oyun cihazda bir evet/hayır işareti tutar ve yeni bir "
         "cihazda mağazadan yeniden doğrulatır.")
    + "<h2>9. Verini silme</h2>"
    + _p("Bulut kaydını ve bağlı olduğu kimliği oyunun içinden "
         "silebilirsin; telefonundaki kopyayı da ayrıca temizleyebilirsin. "
         "İkisinin adımları ve hangisinin neyi kapsamadığı "
         "<a href=\"/tr/account-deletion.html\">Hesap silme</a> sayfasında "
         "yazıyor.")
    + "<h2>10. Çocuklar</h2>"
    + _p("%s'da sohbet ve kullanıcı içeriği yoktur, oyunun hiçbir yerinde bir "
         "şey yazılabilecek bir alan yoktur. Çocuklara yönelik değildir. "
         "Oyunda reklam gösterildiği için genel kitleye uygun olarak "
         "derecelendirilmiştir, çocuk uygulaması olarak beyan "
         "edilmemiştir." % APP)
    + "<h2>11. Değişiklikler</h2>"
    + _p("Bu sayfadaki önemli değişiklikler yeni bir tarihle burada "
         "yayımlanır. Oyun bulut kaydı, giriş ve ölçüm kazandığında bu sayfa "
         "yamalanmadı, yeniden yazıldı; çünkü önceki sürüm bunun tersini "
         "söylüyordu. Bir dahakinde de aynısı geçerli.")
    + "<h2>12. İletişim</h2>"
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
          "Tamper with the game's stored state, with the cloud save, or with "
          "the store's purchase verification.",
          "Use another player's account, or try to reach a save that is not "
          "yours.")
    + "<h2>4. Your account</h2>"
    + _p("The game gives you an anonymous identity on first launch and files "
         "your cloud save under it. Linking a Google or Apple account is "
         "optional and exists so you can pick the game up on another device. "
         "You are responsible for keeping access to whichever account you "
         "link; we cannot identify a save without it.")
    + _p("You can delete the account and its cloud save from inside the game "
         "at any time. See <a href=\"/account-deletion.html\">Account "
         "deletion</a>.")
    + "<h2>5. Progress and the cloud save</h2>"
    + _p("The copy on your device is the one the game plays from. The cloud "
         "copy is a convenience laid on top of it, so that progress survives a "
         "new phone. If the network is down, if the service is unavailable or "
         "if you never link an account, the game carries on from the device "
         "and nothing about it breaks.")
    + _p("Because of that, some things are not carried between devices: lives "
         "and their timer, and the daily counts of rewarded ads, stay on the "
         "device that earned them. Where the same save has been changed on two "
         "devices, the game keeps the higher of the two for levels, stars and "
         "lifetime counters, and takes the most recent writer's numbers for "
         "joker counts and settings. Progress made offline on a device that "
         "later loses the tie-break can be lost. We do not promise that a "
         "cloud save can always be restored.")
    + "<h2>6. Purchases</h2>"
    + _ul("The ad-free version is a one-off purchase, not a subscription. It "
          "is tied to the store account you bought it with and can be restored "
          "on a new device from that same account.",
          "It is not tied to the Google or Apple account you may have linked "
          "inside the game, and it is not part of the cloud save. Deleting "
          "your account in the game does not take the purchase away.",
          "Payment, tax and invoicing are handled by Google Play or the App "
          "Store. We are not the seller of record and we never receive your "
          "payment details.",
          "Refunds follow the policy of the store you bought from. We cannot "
          "issue a refund ourselves, but write to us and we will tell you "
          "where to ask.",
          "Lives, stars, jokers and the shot budget are not currency. They "
          "cannot be bought, sold or transferred, and they have no value "
          "outside the game.")
    + "<h2>7. Availability and changes</h2>"
    + _p("The game may change. Levels can be rebalanced, features added or "
         "removed. Nothing here promises that a specific feature will exist "
         "forever, and that includes the cloud save. A purchase you already "
         "made is not taken away by such a change.")
    + "<h2>8. No warranty</h2>"
    + _p("%s is provided as is. To the extent permitted by law, we make no "
         "warranty that it will be uninterrupted or error free, and we are not "
         "liable for indirect or consequential loss arising from its use, "
         "including lost progress." % APP)
    + "<h2>9. Governing law</h2>"
    + _p("These terms are governed by the laws of the Republic of Turkiye. "
         "Nothing in them limits consumer rights you have under the law of the "
         "country you live in.")
    + "<h2>10. Contact</h2>"
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
          "Oyunun cihazda tuttuğu kayda, bulut kaydına ya da mağazanın satın "
          "alma doğrulamasına müdahale etmek.",
          "Başka bir oyuncunun hesabını kullanmak ya da sana ait olmayan bir "
          "kayda ulaşmaya çalışmak.")
    + "<h2>4. Hesabın</h2>"
    + _p("Oyun ilk açılışta sana anonim bir kimlik verir ve bulut kaydını onun "
         "altına yazar. Google ya da Apple hesabı bağlamak isteğe bağlıdır ve "
         "oyunu başka bir cihazda sürdürebilmen için vardır. Bağladığın "
         "hesaba erişimini korumak senin sorumluluğundadır; onsuz bir kaydı "
         "tanımlayamayız.")
    + _p("Hesabı ve bulut kaydını oyunun içinden istediğin zaman "
         "silebilirsin. Bkz. <a href=\"/tr/account-deletion.html\">Hesap "
         "silme</a>.")
    + "<h2>5. İlerleme ve bulut kaydı</h2>"
    + _p("Oyunun oynadığı kopya cihazındakidir. Bulut kopyası onun üstüne "
         "konmuş bir kolaylıktır; telefon değişince ilerlemenin hayatta "
         "kalması içindir. Ağ yoksa, hizmet erişilemezse ya da hiç hesap "
         "bağlamadıysan oyun cihazdan devam eder ve hiçbir şeyi bozulmaz.")
    + _p("Bunun sonucu olarak bazı şeyler cihazlar arasında taşınmaz: canlar "
         "ve sayacı, bir de günlük ödüllü reklam hakları, onları kazanan "
         "cihazda kalır. Aynı kayıt iki cihazda değişmişse oyun bölümler, "
         "yıldızlar ve ömür boyu sayaçlar için yüksek olanı tutar; joker "
         "sayıları ve ayarlar için en son yazanın değerlerini alır. "
         "Çevrimdışıyken kazanılan ve sonra bu karşılaştırmayı kaybeden bir "
         "ilerleme kaybolabilir. Bir bulut kaydının her koşulda geri "
         "getirilebileceğine dair söz vermiyoruz.")
    + "<h2>6. Satın alma</h2>"
    + _ul("Reklamsız sürüm tek seferlik bir satın almadır, abonelik değildir. "
          "Satın aldığın mağaza hesabına bağlıdır ve yeni bir cihazda aynı "
          "hesaptan geri yüklenebilir.",
          "Oyunun içinde bağlamış olabileceğin Google ya da Apple hesabına "
          "bağlı değildir ve bulut kaydının parçası değildir. Oyunda hesabını "
          "silmek satın almanı elinden almaz.",
          "Ödeme, vergi ve faturalama Google Play ya da App Store tarafından "
          "yürütülür. Kayıtlı satıcı biz değiliz ve ödeme bilgilerini hiç "
          "almayız.",
          "İade, satın aldığın mağazanın politikasına tabidir. İadeyi biz "
          "veremeyiz ama bize yazarsan nereye başvuracağını söyleriz.",
          "Canlar, yıldızlar, jokerler ve vuruş bütçesi para birimi değildir. "
          "Satın alınamaz, satılamaz, devredilemez ve oyunun dışında bir "
          "değerleri yoktur.")
    + "<h2>7. Erişilebilirlik ve değişiklikler</h2>"
    + _p("Oyun değişebilir. Bölümler yeniden dengelenebilir, özellikler "
         "eklenebilir ya da kaldırılabilir. Burada hiçbir özelliğin sonsuza "
         "kadar var olacağı vaat edilmiyor, bulut kaydı da buna dahil. "
         "Halihazırda yaptığın bir satın alma böyle bir değişiklikle elinden "
         "alınmaz.")
    + "<h2>8. Garanti yok</h2>"
    + _p("%s olduğu gibi sunulur. Kanunun izin verdiği ölçüde, kesintisiz ya da "
         "hatasız çalışacağına dair bir garanti vermiyoruz ve kullanımından "
         "doğan dolaylı zararlardan, kaybolan ilerleme dahil, sorumlu "
         "değiliz." % APP)
    + "<h2>9. Uygulanacak hukuk</h2>"
    + _p("Bu koşullar Türkiye Cumhuriyeti kanunlarına tabidir. Buradaki hiçbir "
         "hüküm, yaşadığın ülkenin kanunlarından doğan tüketici haklarını "
         "sınırlamaz.")
    + "<h2>10. İletişim</h2>"
    + _p("%s &middot; %s" % (_mail(), PKG)))

# ── Hesap silme ─────────────────────────────────────────────────────────────
#
# Magaza formu BU sayfaya bakiyor. Iki akis birbirinden ayri anlatiliyor
# cunku uygulamada da ayrilar: "Hesabi sil" belgeyi ve kimligi siler,
# "Ilerlemeyi sifirla" yalnizca durumu temizler. Ikisini tek basligin altinda
# toplamak, magaza incelemesine yanlis beyan vermek olurdu.

DELETE_EN = (
    "<h2>What an account is in %s</h2>" % APP
    + "<div class=\"vurgu\">"
    + _p("The game gives you an <strong>anonymous identity</strong> on first "
         "launch, without asking for anything, and files your cloud save "
         "under it. Linking a <strong>Google</strong> or <strong>Apple</strong> "
         "account is optional; it attaches that identity to a sign-in you "
         "already have so the save can follow you to another device.")
    + "</div>"
    + "<h2>1. Delete your account and cloud save</h2>"
    + _p("This is the route that deletes the record on our side.")
    + _ol("Open <strong>Settings</strong> in the game.",
          "Scroll down to <strong>Account</strong>.",
          "Tap <strong>Delete account</strong>.",
          "The confirmation reads <em>Your account and its cloud save will be "
          "deleted. Progress on this device stays.</em> Tap "
          "<strong>Delete account</strong> again to confirm.")
    + _p("The game deletes the document at <strong>/users/{your "
         "identity}</strong> first, then deletes the authentication record "
         "itself, then signs you in with a fresh anonymous identity so you can "
         "keep playing. If a step fails, the settings screen says so instead "
         "of pretending it worked; try again, and write to us if it keeps "
         "failing.")
    + _p("<strong>This works whether or not you ever signed in.</strong> An "
         "anonymous identity is an account too: it has a document in the "
         "cloud, so it has something to delete. Making you create an account "
         "before you are allowed to delete one would mean handing us more "
         "about yourself in order to get rid of what we already hold, so the "
         "row is there from the start. The <strong>Account</strong> section "
         "appears as soon as the cloud is running; if the game cannot reach "
         "it, the section is not drawn at all and there is nothing stored on "
         "our side to remove.")
    + "<h2>2. Clear your progress on this device</h2>"
    + _ol("Open <strong>Settings</strong> in the game.",
          "Scroll down to <strong>Data</strong>.",
          "Tap <strong>Reset progress</strong>.",
          "The confirmation reads <em>All levels and stars will be deleted. "
          "Are you sure?</em> Tap <strong>Reset progress</strong> again to "
          "confirm.")
    + _p("This clears the levels you cleared, your stars, the lifetime "
         "counters and the record of which lessons you were taught. The next "
         "time the game syncs, it writes that cleared state over your cloud "
         "document, so the progress in the cloud copy goes too.")
    + _p("<strong>What it does not do</strong>: it does not delete the cloud "
         "document or the identity, and it leaves your jokers, settings, "
         "lives and ad-free purchase alone. To remove the record itself, use "
         "step 1.")
    + "<h2>3. Ask us by e-mail</h2>"
    + _p("Write to %s from the address linked to your Google or Apple account, "
         "with the subject <strong>%s deletion request</strong>. That address "
         "is what lets us find the right save; we reply to the same address "
         "and delete the correspondence along with it if you ask."
         % (_mail(), APP))
    + _p("An anonymous save carries no e-mail address, no name and nothing "
         "else that could be matched to a message, which is exactly why it "
         "holds so little. If you never linked an account, an e-mail cannot "
         "identify your save and the in-app routes above are the only ones "
         "that work.")
    + "<h2>What is deleted, and what is not</h2>"
    + _ul("<strong>Deleted</strong>: the document at /users/{your identity} "
          "with everything listed in the "
          "<a href=\"/privacy.html\">privacy policy</a>, and the "
          "authentication record for that identity.",
          "<strong>Kept, at the store</strong>: if you bought the ad-free "
          "version, that receipt belongs to Google Play or the App Store. We "
          "have no access to it, and deleting it there would also remove your "
          "right to restore the purchase. Deleting your account here does not "
          "take the purchase away.",
          "<strong>Kept, as counts</strong>: the analytics events described in "
          "the privacy policy arrive without your identity attached, so there "
          "is nothing in them to pick out and delete afterwards.",
          "<strong>Crash reports already sent</strong>: these carry the "
          "identity string, and they age out on Firebase Crashlytics' own "
          "schedule. Once the authentication record is deleted, that string no "
          "longer points at anything of ours.",
          "<strong>What the ad network received</strong>: Google's handling of "
          "the advertising identifier is covered by its own documentation. You "
          "can reset or switch off that identifier in your device settings at "
          "any time.")
    + "<h2>Uninstalling</h2>"
    + _p("Uninstalling removes the copy on the phone, including the anonymous "
         "session that identifies you. It does not delete the cloud document, "
         "and afterwards there is no way to reach it. If you want the cloud "
         "copy gone, do step 1 before you uninstall.")
    + "<h2>Contact</h2>"
    + _p("%s &middot; %s" % (_mail(), PKG)))

DELETE_TR = (
    "<h2>%s'da hesap ne demek</h2>" % APP
    + "<div class=\"vurgu\">"
    + _p("Oyun ilk açılışta, senden hiçbir şey istemeden bir "
         "<strong>anonim kimlik</strong> verir ve bulut kaydını onun altına "
         "yazar. <strong>Google</strong> ya da <strong>Apple</strong> hesabı "
         "bağlamak isteğe bağlıdır; o kimliği zaten sahip olduğun bir girişe "
         "iliştirir, böylece kayıt seninle başka bir cihaza gelebilir.")
    + "</div>"
    + "<h2>1. Hesabını ve bulut kaydını sil</h2>"
    + _p("Bizim tarafımızdaki kaydı silen yol budur.")
    + _ol("Oyunda <strong>Ayarlar</strong>'ı aç.",
          "Aşağı kaydırıp <strong>Hesap</strong> bölümüne gel.",
          "<strong>Hesabı sil</strong> satırına dokun.",
          "Onay ekranında şu yazar: <em>Hesabın ve buluttaki kaydın "
          "silinecek. Bu cihazdaki ilerlemen kalır.</em> Onaylamak için "
          "yeniden <strong>Hesabı sil</strong>'e dokun.")
    + _p("Oyun önce <strong>/users/{kimliğin}</strong> yolundaki belgeyi "
         "siler, sonra kimlik kaydının kendisini siler, sonra oynamaya devam "
         "edebilesin diye seni yeni bir anonim kimlikle içeri alır. Bir adım "
         "başarısız olursa ayarlar ekranı bunu söyler, olmuş gibi yapmaz; "
         "tekrar dene, olmuyorsa bize yaz.")
    + _p("<strong>Bu yol, hiç giriş yapmamış olsan da çalışır.</strong> Anonim "
         "kimlik de bir hesaptır: bulutta bir belgesi vardır, yani silinecek "
         "bir şey vardır. Bir hesabı silebilmen için önce hesap açmanı "
         "istemek, elimizde olandan kurtulmak uğruna senden daha fazla bilgi "
         "istemek olurdu; o yüzden satır en baştan orada. "
         "<strong>Hesap</strong> bölümü bulut çalışır çalışmaz görünür; oyun "
         "buluta erişemiyorsa bölüm hiç çizilmez ve bizim tarafımızda "
         "silinecek bir şey de yoktur.")
    + "<h2>2. Bu cihazdaki ilerlemeni temizle</h2>"
    + _ol("Oyunda <strong>Ayarlar</strong>'ı aç.",
          "Aşağı kaydırıp <strong>Veriler</strong> bölümüne gel.",
          "<strong>İlerlemeyi sıfırla</strong> satırına dokun.",
          "Onay ekranında şu yazar: <em>Tüm bölümler ve yıldızlar silinecek. "
          "Emin misin?</em> Onaylamak için yeniden <strong>İlerlemeyi "
          "sıfırla</strong>'ya dokun.")
    + _p("Bu, geçtiğin bölümleri, yıldızlarını, ömür boyu sayaçları ve hangi "
         "dersleri öğrendiğinin kaydını temizler. Oyun bir sonraki "
         "eşitlemesinde bu temiz durumu bulut belgenin üzerine yazar; yani "
         "bulut kopyasındaki ilerleme de gider.")
    + _p("<strong>Yapmadığı şey</strong>: bulut belgesini ya da kimliği "
         "silmez, jokerlerine, ayarlarına, canlarına ve reklamsız satın "
         "almana dokunmaz. Kaydın kendisini kaldırmak için 1. adımı kullan.")
    + "<h2>3. E-posta ile bize sor</h2>"
    + _p("%s adresine, Google ya da Apple hesabına bağlı adresten, "
         "<strong>%s silme talebi</strong> konusuyla yaz. Doğru kaydı "
         "bulmamızı sağlayan şey o adrestir; aynı adrese cevap veririz ve "
         "istersen yazışmayı da onunla birlikte sileriz." % (_mail(), APP))
    + _p("Anonim bir kayıtta e-posta adresi, isim ya da bir mesajla "
         "eşleştirilebilecek başka bir şey yoktur; zaten bu kadar az şey "
         "tutmasının sebebi de budur. Hiç hesap bağlamadıysan bir e-posta "
         "kaydını tanımlayamaz ve yukarıdaki uygulama içi yollar tek "
         "çalışan yollardır.")
    + "<h2>Neler siliniyor, neler silinmiyor</h2>"
    + _ul("<strong>Silinen</strong>: /users/{kimliğin} yolundaki belge, "
          "<a href=\"/tr/privacy.html\">gizlilik politikasında</a> sayılan her "
          "şeyle birlikte, ve o kimliğin kimlik doğrulama kaydı.",
          "<strong>Mağazada kalan</strong>: reklamsız sürümü aldıysan o makbuz "
          "Google Play'e ya da App Store'a aittir. Bizim erişimimiz yok ve "
          "orada silmek satın almayı geri yükleme hakkını da ortadan "
          "kaldırır. Burada hesabını silmek satın almanı elinden almaz.",
          "<strong>Toplam olarak kalan</strong>: gizlilik politikasında "
          "anlatılan ölçüm olayları kimliğin iliştirilmeden gelir; yani "
          "içlerinde sonradan ayıklanıp silinebilecek bir şey yoktur.",
          "<strong>Gönderilmiş çökme raporları</strong>: bunlar kimlik "
          "dizesini taşır ve Firebase Crashlytics'in kendi takvimine göre "
          "düşer. Kimlik doğrulama kaydı silindikten sonra o dize bizim "
          "hiçbir şeyimizi işaret etmez.",
          "<strong>Reklam ağının aldıkları</strong>: Google'ın reklam "
          "kimliğini nasıl işlediği kendi dokümantasyonuna tabidir. O kimliği "
          "cihaz ayarlarından istediğin zaman sıfırlayabilir ya da "
          "kapatabilirsin.")
    + "<h2>Uygulamayı kaldırmak</h2>"
    + _p("Kaldırmak telefondaki kopyayı, seni tanımlayan anonim oturum dahil, "
         "siler. Bulut belgesini silmez ve sonrasında o belgeye ulaşmanın bir "
         "yolu kalmaz. Bulut kopyasının gitmesini istiyorsan kaldırmadan önce "
         "1. adımı yap.")
    + "<h2>İletişim</h2>"
    + _p("%s &middot; %s" % (_mail(), PKG)))


# Baslik ve meta aciklama sayfa basina. Colmo'da yasal sayfalarin meta
# aciklamasi acilis sayfasindan kopyaydi ve dort sayfa ayni metinle
# indeksleniyordu.
_PAGES = {
    "en": [
        ("privacy.html", "Privacy policy",
         "What %s keeps on your device, what goes to the cloud save, which "
         "events it measures and what the ads receive. Anonymous by default, "
         "sign-in optional." % APP,
         PRIVACY_EN),
        ("terms.html", "Terms of use",
         "The licence, the one optional purchase, your anonymous account, and "
         "what the cloud save does and does not promise.",
         TERMS_EN),
        ("account-deletion.html", "Account deletion",
         "Numbered steps to delete your %s account and cloud save from inside "
         "the game, to clear progress on the device, and what is kept "
         "afterwards." % APP,
         DELETE_EN),
    ],
    "tr": [
        ("privacy.html", "Gizlilik politikası",
         "%s'nın cihazında ne sakladığı, bulut kaydına ne gittiği, hangi "
         "olayları ölçtüğü ve reklamların ne aldığı. Varsayılan olarak "
         "anonim, giriş isteğe bağlı." % APP,
         PRIVACY_TR),
        ("terms.html", "Kullanım koşulları",
         "Lisans, isteğe bağlı tek satın alma, anonim hesabın ve bulut "
         "kaydının neyi vaat edip neyi etmediği.",
         TERMS_TR),
        ("account-deletion.html", "Hesap silme",
         "%s hesabını ve bulut kaydını oyunun içinden silmek, cihazdaki "
         "ilerlemeyi temizlemek için numaralı adımlar, ve sonrasında neyin "
         "kaldığı." % APP,
         DELETE_TR),
    ],
}


def pages(code):
    """(dosya, baslik, meta aciklama, govde) dortlulerini dondurur."""
    return _PAGES.get(code, _PAGES["en"])
