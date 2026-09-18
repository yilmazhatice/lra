"""evaluate.py'nin soru seti.

Her soru bir sozluk:
  id        karsilastirmada sorulari eslemek icin sabit kimlik
  soru      sorulan metin
  kategori  normal | ozel_ad (tek kavram/ozel ad soran kisa sorular)
  belge     cevabin bulundugu belge; None ise soru belgelerde cevaplanamaz
  kanit     cevabin bulundugu paragraftan kisa bir ifade. Dogru parcanin
            arama sirasi, bu ifadeyi iceren ilk parcanin sirasidir. Parca
            numarasi yerine ifade kullaniliyor ki parcalama degisince set
            gecersiz olmasin.
  anahtar   cevapta gecmesi gereken ifadeler; hepsi aranir
  yasak     cevapta gecmemesi gereken ifadeler (bilinen yanlislar)
  eski12    eval_results.md'deki eski 12 soruluk sette de var

belge, kanit ve anahtar degerlerinde "a|b" bicimi "a ya da b" demektir.
Karsilastirma buyuk/kucuk harf ve Turkce i/I farkini gozetmez.

SENARYOLAR arayuzdeki gibi ayni oturumda ard arda sorulur; yalnizca son
soru senaryo tipiyle puanlanir, onceki sorular "hazirlik" olarak raporlanir.

KONTROL_SORULAR ve KONTROL_SENARYOLAR (Faz 5.5) ayar yapmak icin
KULLANILMAZ: sonuclari gorulmeden yazildi ve dondu (rag_iyilestirme_plani.md
Bolum 2.13). Calistirmak icin: python evaluate.py --set kontrol
"""

SORULAR = [
    # ------------------------------------------------ canakkale-ve-kurtulus-savasi.md
    dict(id="canakkale-1", soru="Çanakkale Deniz Zaferi hangi tarihte kazanılmıştır?",
         belge="canakkale-ve-kurtulus-savasi.md", kanit="18 Mart 1915'te yapılan deniz saldırısı",
         anahtar=["18 Mart 1915"]),
    dict(id="canakkale-2", soru="Gelibolu Yarımadası'na kara çıkarmaları ne zaman yapılmıştır?",
         belge="canakkale-ve-kurtulus-savasi.md", kanit="25 Nisan 1915'te Gelibolu",
         anahtar=["25 Nisan 1915"]),
    dict(id="canakkale-3", soru="Sakarya Meydan Muharebesi kaç gün sürmüştür?", eski12=True,
         belge="canakkale-ve-kurtulus-savasi.md", kanit="yirmi iki gün süren Sakarya",
         anahtar=["yirmi iki|22"]),
    dict(id="canakkale-4", soru="Büyük Taarruz'da kesin sonuç nerede alınmıştır?",
         belge="canakkale-ve-kurtulus-savasi.md", kanit="30 Ağustos'ta Dumlupınar'da",
         anahtar=["Dumlupınar"]),
    dict(id="canakkale-5", soru="Lozan Antlaşması ne zaman imzalanmıştır?",
         belge="canakkale-ve-kurtulus-savasi.md", kanit="24 Temmuz 1923'te Lozan",
         anahtar=["24 Temmuz 1923"]),

    # ------------------------------------------------------- ilk-turk-devletleri.md
    dict(id="ilkturk-1", soru="Orhun Yazıtları'nın alfabesini kim ve hangi yılda çözmüştür?", eski12=True,
         belge="ilk-turk-devletleri.md", kanit="Vilhelm Thomsen 1893'te",
         anahtar=["Thomsen", "1893"]),
    dict(id="ilkturk-2", soru="Mete Han orduyu hangi sisteme göre düzenlemiştir?",
         belge="ilk-turk-devletleri.md", kanit="onluk sisteme göre",
         anahtar=["onluk"]),
    dict(id="ilkturk-3", soru="Göktürk Devleti ne zaman ve kimin önderliğinde kurulmuştur?",
         belge="ilk-turk-devletleri.md", kanit="552 yılında Bumin Kağan",
         anahtar=["552", "Bumin"]),
    dict(id="ilkturk-4", soru="Orhun Yazıtları kimler adına dikilmiştir?",
         belge="ilk-turk-devletleri.md", kanit="vezir Tonyukuk",
         anahtar=["Tonyukuk", "Kül Tigin", "Bilge Kağan"]),
    dict(id="ilkturk-5", soru="Uygur Kağanlığı hangi yıl kurulmuştur?",
         belge="ilk-turk-devletleri.md", kanit="744'te Uygur Kağanlığı",
         anahtar=["744"]),

    # ------------------------------------------------------ mustafa-kemal-ataturk.md
    dict(id="ataturk-1", soru="Mustafa Kemal'in annesinin adı nedir?",
         belge="mustafa-kemal-ataturk.md", kanit="annesi Zübeyde Hanım",
         anahtar=["Zübeyde"]),
    dict(id="ataturk-2", soru="Mustafa Kemal'e Kemal adını kim vermiştir?",
         belge="mustafa-kemal-ataturk.md", kanit="matematik öğretmeni Mustafa Efendi",
         anahtar=["Mustafa Efendi"]),
    dict(id="ataturk-3", soru="Nutuk ne zaman okunmuş ve yaklaşık kaç saat sürmüştür?",
         belge="mustafa-kemal-ataturk.md", kanit="yaklaşık otuz altı saat",
         anahtar=["1927", "otuz altı|36"]),
    dict(id="ataturk-4", soru="\"Yurtta sulh, cihanda sulh\" sözü hangi yıl söylenmiştir?",
         belge="mustafa-kemal-ataturk.md", kanit="Yurtta sulh, cihanda sulh",
         anahtar=["1931"]),
    # Nakil tarihi milli-semboller.md'deki Anitkabir bolumunde de geciyor; iki belge de kabul.
    dict(id="ataturk-5", soru="Atatürk'ün naaşı Anıtkabir'e ne zaman nakledilmiştir?",
         belge="mustafa-kemal-ataturk.md|milli-semboller.md",
         kanit="10 Kasım 1953'te buraya nakledilmiştir",
         anahtar=["10 Kasım 1953"]),

    # -------------------------------------------------------- osmanli-padisahlari.md
    # Misir'in alinmasi Mercidabik ve Ridaniye ile; Caldiran Safevilere karsi.
    dict(id="osmanli-1", soru="Yavuz Sultan Selim hangi savaşlarla Mısır'ı Osmanlı topraklarına katmıştır?", eski12=True,
         belge="osmanli-padisahlari.md", kanit="1516'da Mercidabık",
         anahtar=["Mercidabık", "Ridaniye"]),
    dict(id="osmanli-2", soru="fatih kimdir", kategori="ozel_ad",
         belge="osmanli-padisahlari.md", kanit="II. Mehmed, 29 Mayıs 1453'te",
         anahtar=["İstanbul"], yasak=["kurucu"]),
    dict(id="osmanli-3", soru="Osman Gazi kimdir", kategori="ozel_ad",
         belge="osmanli-padisahlari.md", kanit="kurucusu Osman Gazi'dir",
         anahtar=["kurucu"], yasak=["Bursa"]),
    dict(id="osmanli-4", soru="Orhan Gazi kimdir", kategori="ozel_ad",
         belge="osmanli-padisahlari.md", kanit="Orhan Gazi döneminde Bursa alınmış",
         anahtar=["Bursa|Rumeli"], yasak=["1323"]),
    # Ayni olay anadolu-beylikleri belgesinde Fetret Devri anlatilirken de geciyor.
    dict(id="osmanli-5", soru="Yıldırım Bayezid Ankara Savaşı'nda kime yenilmiştir?",
         belge="osmanli-padisahlari.md|anadolu-beylikleri-ve-osmanlinin-kurulusu.md",
         kanit="Ankara Savaşı'nda Timur'a",
         anahtar=["Timur"]),
    dict(id="osmanli-6", soru="Kanuni Sultan Süleyman kaç yıl hüküm sürmüştür?",
         belge="osmanli-padisahlari.md", kanit="kırk altı yıl hüküm sürerek",
         anahtar=["kırk altı|46"]),

    # --------------------------------------------------- selcuklular-ve-malazgirt.md
    dict(id="selcuklu-1", soru="Anadolu Selçuklu Devleti hangi savaşta Moğollara yenilmiştir?", eski12=True,
         belge="selcuklular-ve-malazgirt.md", kanit="1243'teki Kösedağ",
         anahtar=["Kösedağ"]),
    dict(id="selcuklu-2", soru="Malazgirt Savaşı ne zaman yapılmıştır?",
         belge="selcuklular-ve-malazgirt.md", kanit="26 Ağustos 1071'de",
         anahtar=["1071"]),
    dict(id="selcuklu-3", soru="Büyük Selçuklu Devleti'nin kuruluşunu kesinleştiren savaş hangisidir?",
         belge="selcuklular-ve-malazgirt.md", kanit="1040 yılındaki Dandanakan",
         anahtar=["Dandanakan"]),
    dict(id="selcuklu-4", soru="Anadolu Selçuklu Devleti'ni kim kurmuştur?",
         belge="selcuklular-ve-malazgirt.md", kanit="1077'de Süleyman Şah",
         anahtar=["Süleyman Şah"]),
    dict(id="selcuklu-5", soru="Miryokefalon Savaşı'nın sonucu ne olmuştur?",
         belge="selcuklular-ve-malazgirt.md", kanit="1176'daki Miryokefalon",
         anahtar=["Türk yurdu|başarısız"]),

    # ------------------------------------------------------------ turk-destanlari.md
    dict(id="destan-1", soru="Manas Destanı hangi topluma aittir?",
         belge="turk-destanlari.md", kanit="Kırgızlara ait Manas",
         anahtar=["Kırgız"]),
    dict(id="destan-2", soru="Dede Korkut Kitabı kaç hikâyeden oluşur?",
         belge="turk-destanlari.md", kanit="on iki hikâyeden",
         anahtar=["on iki|12"]),
    dict(id="destan-3", soru="Oğuz Kağan Destanı'na göre Oğuz Kağan'ın kaç oğlu vardır?",
         belge="turk-destanlari.md", kanit="altı oğlu olduğu",
         anahtar=["altı|6"]),
    dict(id="destan-4", soru="Ergenekon'dan çıkış günü nasıl kutlanmıştır?",
         belge="turk-destanlari.md", kanit="bahar bayramı olarak",
         anahtar=["bahar bayramı"]),
    dict(id="destan-5", soru="Dede Korkut kültürü UNESCO listesine hangi yıl alınmıştır?",
         belge="turk-destanlari.md", kanit="2018'de UNESCO",
         anahtar=["2018"]),

    # -------------------------------------------------------- turk-devlet-gelenegi.md
    dict(id="gelenek-1", soru="Kut nedir?", kategori="ozel_ad",
         belge="turk-devlet-gelenegi.md", kanit="Bu yetkiye kut denir",
         anahtar=["Tanrı"]),
    dict(id="gelenek-2", soru="Töre nedir?", kategori="ozel_ad",
         belge="turk-devlet-gelenegi.md", kanit="Töre, yazılı olmayan hukuk",
         anahtar=["yazılı olmayan"]),
    dict(id="gelenek-3", soru="Kurultayda hangi konular görüşülürdü?",
         belge="turk-devlet-gelenegi.md", kanit="Savaş, barış ve hükümdar seçimi",
         anahtar=["savaş", "barış"]),
    dict(id="gelenek-4", soru="İkili teşkilat nedir?",
         belge="turk-devlet-gelenegi.md", kanit="İkili teşkilat, ülkenin doğu ve batı",
         anahtar=["doğu", "batı"]),
    dict(id="gelenek-5", soru="Tuğ nedir?", kategori="ozel_ad",
         belge="turk-devlet-gelenegi.md", kanit="Tuğ, at kılından",
         anahtar=["at kılı"]),

    # --------------------------------------------------------- turk-kulturunde-at.md
    dict(id="at-1", soru="Turan taktiği nasıl uygulanır?", eski12=True,
         belge="turk-kulturunde-at.md", kanit="sahte bir geri çekilme",
         anahtar=["geri çekil", "hilal|kuşat"]),
    dict(id="at-2", soru="Kımız nedir?", kategori="ozel_ad",
         belge="turk-kulturunde-at.md", kanit="Kısrak sütünün mayalanmasıyla",
         anahtar=["kısrak"]),
    dict(id="at-3", soru="Üzengi atlı savaşa ne kazandırmıştır?",
         belge="turk-kulturunde-at.md", kanit="Üzengi sayesinde binici",
         anahtar=["denge|iki elini"]),
    dict(id="at-4", soru="Hangi at ırkları dayanıklılıklarıyla bilinir?",
         belge="turk-kulturunde-at.md", kanit="Ahal Teke ve Türkmen atı",
         anahtar=["Ahal Teke"]),

    # ------------------------------------------------------- turk-kulturunde-kurt.md
    dict(id="kurt-1", soru="Eski Türkçede kurdun adı neydi?", eski12=True,
         belge="turk-kulturunde-kurt.md", kanit='kurdun adı "böri"',
         anahtar=["böri"]),
    # Bilinen uydurma: "bu ad kurtçuk ve böcek larvasının anısına geldi"
    dict(id="kurt-2", soru="böri nedir", kategori="ozel_ad",
         belge="turk-kulturunde-kurt.md", kanit='kurdun adı "böri"',
         anahtar=["kurt"], yasak=["larva"]),
    dict(id="kurt-3", soru="Aşina hanedanının soyu nereden gelir?", kategori="ozel_ad",
         belge="turk-kulturunde-kurt.md", kanit="hanedanın adı Aşina'dır",
         anahtar=["kurt"]),
    dict(id="kurt-4", soru="Eski Türkçede kurt kelimesinin anlamı neydi?",
         belge="turk-kulturunde-kurt.md", kanit="solucan, kurtçuk, böcek larvasıdır",
         anahtar=["solucan|kurtçuk|larva"]),
    dict(id="kurt-5", soru="Azerbaycan Türkçesinde kurda ne denir?",
         belge="turk-kulturunde-kurt.md", kanit='"canavar" sözcüğü',
         anahtar=["canavar"]),
    dict(id="kurt-6", soru="Ergenekon'dan çıkan topluluğa yolu kim göstermiştir?",
         belge="turk-kulturunde-kurt.md", kanit="Börteçine adlı bozkurt",
         anahtar=["Börteçine"]),

    # ------------------------------------------------ turk-milliyetciliginin-dogusu.md
    dict(id="dogus-1", soru="Üç Tarz-ı Siyaset yazısı nerede ve hangi yıl yayımlanmıştır?", eski12=True,
         belge="turk-milliyetciliginin-dogusu.md", kanit="1904'te Kahire'de",
         anahtar=["Kahire", "1904"]),
    dict(id="dogus-2", soru="Türkçülüğün Esasları kimin eseridir?",
         belge="turk-milliyetciliginin-dogusu.md", kanit="Türkçülüğün Esasları'dır",
         anahtar=["Gökalp"]),
    dict(id="dogus-3", soru="İsmail Gaspıralı hangi ilkeyi savunmuştur?",
         belge="turk-milliyetciliginin-dogusu.md", kanit="Dilde, fikirde, işte birlik",
         anahtar=["dilde", "fikirde", "birlik"]),
    dict(id="dogus-4", soru="Türk Ocağı ne zaman kurulmuştur?",
         belge="turk-milliyetciliginin-dogusu.md", kanit="25 Mart 1912'de kurulan Türk Ocağı",
         anahtar=["1912"]),

    # ----------------------------------------------- turkcenin-tarihi-ve-alfabeleri.md
    dict(id="alfabe-1", soru="Göktürk alfabesi kaç işaretten oluşur?",
         belge="turkcenin-tarihi-ve-alfabeleri.md", kanit="Otuz sekiz işaretten",
         anahtar=["otuz sekiz|38"]),
    dict(id="alfabe-2", soru="Harf Devrimi hangi tarihte kabul edilmiştir?",
         belge="turkcenin-tarihi-ve-alfabeleri.md", kanit="1 Kasım 1928'de kabul edilen Harf Devrimi",
         anahtar=["1 Kasım 1928"]),
    dict(id="alfabe-3", soru="Türk Dil Kurumu ne zaman kurulmuştur?",
         belge="turkcenin-tarihi-ve-alfabeleri.md", kanit="12 Temmuz 1932'de kurulan",
         anahtar=["1932"]),
    dict(id="alfabe-4", soru="Uygur alfabesi hangi yazıdan uyarlanmıştır?",
         belge="turkcenin-tarihi-ve-alfabeleri.md", kanit="Soğd yazısından",
         anahtar=["Soğd"]),
    # ilk-turk-islam-eserleri.md eseri 1069-1070 diye tarihliyor; yuzyil oradan cikiyor.
    # Bu yuzden hem belge hem kanit ikinci bir karsilik alacak sekilde genisletildi.
    dict(id="alfabe-5", soru="Kutadgu Bilig hangi yüzyılda yazılmıştır?",
         belge="turkcenin-tarihi-ve-alfabeleri.md|ilk-turk-islam-eserleri.md",
         kanit="on birinci yüzyılda yazılmıştır|1069-1070 yıllarında tamamlanarak",
         anahtar=["on birinci|11"]),

    # ------------------------------------------------------ cevaplanamaz sorular
    # kategori: yakin (konuya yakin ama belgede yok) | konu_disi | anlamsiz
    dict(id="cevapsiz-1", soru="Fatih Sultan Mehmed'in annesinin adı nedir?", kategori="yakin", eski12=True),
    dict(id="cevapsiz-2", soru="Malazgirt Savaşı'nda Selçuklu ordusu kaç askerden oluşuyordu?", kategori="yakin"),
    dict(id="cevapsiz-3", soru="Kanuni Sultan Süleyman'ın eşinin adı nedir?", kategori="yakin"),
    dict(id="cevapsiz-4", soru="Lozan Antlaşması'nı Türk heyeti adına kim imzalamıştır?", kategori="yakin"),
    dict(id="cevapsiz-5", soru="Orhun Yazıtları bugün hangi müzede sergilenmektedir?", kategori="yakin"),
    dict(id="cevapsiz-6", soru="Mete Han'ın babasının adı nedir?", kategori="yakin"),
    dict(id="cevapsiz-7", soru="Bugün hava nasıl olacak?", kategori="konu_disi", eski12=True),
    dict(id="cevapsiz-8", soru="Python'da bir liste nasıl sıralanır?", kategori="konu_disi"),
    dict(id="cevapsiz-9", soru="Futbolda ofsayt kuralı nedir?", kategori="konu_disi"),
    dict(id="cevapsiz-10", soru="asdf qwerty zxcv", kategori="anlamsiz", eski12=True),
]

# Senaryo tipleri:
#   takip            onceki soruya bagli, tek basina anlamsiz soru; cevap belgede var
#   takip_cevapsiz   onceki soruya bagli ama cevap belgede yok
#   konu_degisimi    kisa bir soruyla baska konuya geciliyor
#   konu_disi_sonra  belgeyle ilgili bir sorudan sonra konu disi soru
SENARYOLAR = [
    dict(id="takip-1", tip="takip", sorular=[
        dict(soru="Malazgirt Savaşı ne zaman yapılmıştır?"),
        dict(soru="sonucu ne oldu?",
             belge="selcuklular-ve-malazgirt.md", kanit="imparator esir düşmüştür",
             anahtar=["zafer|kazan"]),
    ]),
    # Bilinen hata: model yalnizca "hangi yılda?" goruyor ve 1928 yaziyor.
    dict(id="takip-2", tip="takip", sorular=[
        dict(soru="Orhun Yazıtları'nın alfabesini kim çözmüştür?"),
        dict(soru="hangi yılda?",
             belge="ilk-turk-devletleri.md", kanit="Vilhelm Thomsen 1893'te",
             anahtar=["1893"], yasak=["1928"]),
    ]),
    dict(id="takip-3", tip="takip", sorular=[
        dict(soru="Manas Destanı hangi topluma aittir?"),
        dict(soru="kaç dizeden oluşur?",
             belge="turk-destanlari.md", kanit="yarım milyon dizeye",
             anahtar=["yarım milyon"]),
    ]),
    dict(id="takip-4", tip="takip", sorular=[
        dict(soru="Kanuni Sultan Süleyman kaç yıl hüküm sürmüştür?"),
        dict(soru="onun döneminde hangi şehir kuşatıldı?",
             belge="osmanli-padisahlari.md", kanit="1529'da Viyana kuşatılmıştır",
             anahtar=["Viyana"]),
    ]),
    dict(id="takip-5", tip="takip", sorular=[
        dict(soru="İsmail Gaspıralı hangi gazeteyi çıkarmıştır?"),
        dict(soru="bu gazete nerede çıkarıldı?",
             belge="turk-milliyetciliginin-dogusu.md", kanit="1883'te Kırım'da Tercüman",
             anahtar=["Kırım"]),
    ]),
    dict(id="takip-cevapsiz-1", tip="takip_cevapsiz", sorular=[
        dict(soru="Sakarya Meydan Muharebesi kaç gün sürmüştür?"),
        dict(soru="bunun sebebi ne?"),
    ]),
    dict(id="takip-cevapsiz-2", tip="takip_cevapsiz", sorular=[
        dict(soru="Türk Ocağı ne zaman kurulmuştur?"),
        dict(soru="ilk başkanı kimdi?"),
    ]),
    dict(id="degisim-1", tip="konu_degisimi", sorular=[
        dict(soru="böri nedir"),
        dict(soru="fatih kimdir",
             belge="osmanli-padisahlari.md", kanit="II. Mehmed, 29 Mayıs 1453'te",
             anahtar=["İstanbul"], yasak=["kurucu"]),
    ]),
    dict(id="degisim-2", tip="konu_degisimi", sorular=[
        dict(soru="Orhan Gazi kimdir"),
        dict(soru="böri nedir",
             belge="turk-kulturunde-kurt.md", kanit='kurdun adı "böri"',
             anahtar=["kurt"], yasak=["larva"]),
    ]),
    dict(id="degisim-3", tip="konu_degisimi", sorular=[
        dict(soru="Turan taktiği nasıl uygulanır?"),
        dict(soru="Kımız nedir?",
             belge="turk-kulturunde-at.md", kanit="Kısrak sütünün mayalanmasıyla",
             anahtar=["kısrak"]),
    ]),
    dict(id="degisim-4", tip="konu_degisimi", sorular=[
        dict(soru="Harf Devrimi hangi tarihte kabul edilmiştir?"),
        dict(soru="Tuğ nedir?",
             belge="turk-devlet-gelenegi.md", kanit="Tuğ, at kılından",
             anahtar=["at kılı"]),
    ]),
    dict(id="disi-1", tip="konu_disi_sonra", sorular=[
        dict(soru="Osman Gazi kimdir"),
        dict(soru="Bugün hava nasıl olacak?"),
    ]),
    dict(id="disi-2", tip="konu_disi_sonra", sorular=[
        dict(soru="Eski Türkçede kurdun adı neydi?"),
        dict(soru="asdf qwerty zxcv"),
    ]),
    dict(id="disi-3", tip="konu_disi_sonra", sorular=[
        dict(soru="Osman Gazi kimdir"),
        dict(soru="Python listesi nasıl sıralanır?"),
    ]),
    dict(id="disi-4", tip="konu_disi_sonra", sorular=[
        dict(soru="Malazgirt Savaşı ne zaman yapılmıştır?"),
        dict(soru="Futbolda ofsayt kuralı nedir?"),
    ]),
]


# =============================================================== KONTROL SETI
# Faz 5.5. Ana setin sonuclari gorulduktan sonra, ama bu sorularin sonuclari
# gorulmeden yazildi; olcumden sonra degistirilmez. Sorular ana sette
# kullanilmayan bilgilerden ve farkli soru kaliplariyla yazildi. Sinirlama:
# yazan (asistan) ana setin sonuclarini gormustu.

KONTROL_SORULAR = [
    # ------------------------------------------ cevaplanabilir, farkli kaliplar
    dict(id="k-canakkale", soru="Çanakkale'de İtilaf Devletleri neyi amaçlıyordu?",
         belge="canakkale-ve-kurtulus-savasi.md", kanit="boğazı geçip İstanbul'a ulaşmayı",
         anahtar=["İstanbul", "Rusya"]),
    dict(id="k-mete", soru="Mete Han Çin kaynaklarında hangi adla anılır?",
         belge="ilk-turk-devletleri.md", kanit="Modu Chanyu",
         anahtar=["Modu Chanyu"]),
    dict(id="k-kutluk", soru="İkinci Göktürk Devleti'ni kim, hangi yılda kurmuştur?",
         belge="ilk-turk-devletleri.md", kanit="İlteriş Kutluk Kağan",
         anahtar=["İlteriş", "682"]),
    dict(id="k-baba", soru="Mustafa Kemal'in babası kimdir, hangi işleri yapmıştır?",
         belge="mustafa-kemal-ataturk.md", kanit="Ali Rıza Efendi",
         anahtar=["Ali Rıza", "gümrük|kereste"]),
    dict(id="k-murad", soru="I. Murad'ın hayatı nasıl sona ermiştir?",
         belge="osmanli-padisahlari.md", kanit="savaş alanında öldürülmüştür",
         anahtar=["Kosova|savaş alanında"]),
    dict(id="k-saltanat", soru="Osmanlı saltanatı ne zaman ve kim tarafından kaldırılmıştır?",
         belge="osmanli-padisahlari.md", kanit="saltanat 1 Kasım 1922'de",
         anahtar=["1 Kasım 1922", "Meclis"]),
    dict(id="k-kinik", soru="Büyük Selçuklu hanedanı hangi Oğuz boyundan gelir?",
         belge="selcuklular-ve-malazgirt.md", kanit="Kınık boyundan",
         anahtar=["Kınık"]),
    dict(id="k-malazgirt-onem", soru="Malazgirt Savaşı Anadolu'nun tarihi açısından neden önemlidir?",
         belge="selcuklular-ve-malazgirt.md", kanit="Türkleşme sürecinin başlangıcı",
         anahtar=["Türkleşme|yerleş"]),
    dict(id="k-akcura", soru="Yusuf Akçura yazısında hangi siyaset biçimlerini karşılaştırmıştır?",
         belge="turk-milliyetciliginin-dogusu.md", kanit="Osmanlıcılık, İslamcılık ve Türkçülük",
         anahtar=["Osmanlıcılık", "İslamcılık", "Türkçülük"]),
    dict(id="k-harf-sayisi", soru="Latin harflerine dayalı yeni Türk alfabesinde kaç harf vardır?",
         belge="turkcenin-tarihi-ve-alfabeleri.md", kanit="Yirmi dokuz harften",
         anahtar=["yirmi dokuz|29"]),
    dict(id="k-millet-mektep", soru="Yeni alfabeye geçişte halka okuma yazma öğretmek için hangi okullar açıldı?",
         belge="turkcenin-tarihi-ve-alfabeleri.md", kanit="Millet Mektepleri",
         anahtar=["Millet Mektep"]),
    dict(id="k-kurt-neden", soru="Türk kültüründe sembol olarak neden kurt seçilmiştir?",
         belge="turk-kulturunde-kurt.md", kanit="sürü hâlinde yaşaması",
         anahtar=["sürü", "evcil"]),
    dict(id="k-ad-koyma", soru="Dede Korkut hikâyelerindeki ad koyma geleneği nasıldır?",
         belge="turk-destanlari.md", kanit="yiğitlik gösterdikten sonra ad alması",
         anahtar=["yiğitlik"]),

    # ------------------------------------------------- kisa kavram / ozel ad
    dict(id="k-ulus", soru="Ülüş nedir?", kategori="ozel_ad",
         belge="turk-devlet-gelenegi.md", kanit="Ülüş ise ganimetin",
         anahtar=["ganimet|gelir"]),
    dict(id="k-toy", soru="Toy nedir?", kategori="ozel_ad",
         belge="turk-devlet-gelenegi.md", kanit="Kurultay ya da toy",
         anahtar=["meclis|kurultay"]),
    dict(id="k-manasci", soru="Manasçı kimdir?", kategori="ozel_ad",
         belge="turk-destanlari.md", kanit="manasçı denilen anlatıcılar",
         anahtar=["anlatıcı"]),
    dict(id="k-ortmece", soru="Örtmece nedir?", kategori="ozel_ad",
         belge="turk-kulturunde-kurt.md", kanit="örtmece adlandırma",
         anahtar=["gerçek adını|başka bir sözcük"]),
    dict(id="k-asena", soru="Asena nedir?", kategori="ozel_ad",
         belge="turk-kulturunde-kurt.md", kanit='"Asena" biçimi',
         anahtar=["Aşina|okunuş"]),

    # --------------------------------- cevaplanamaz, konuya yakin (yakin)
    dict(id="k-bumin-baba", soru="Bumin Kağan'ın babasının adı nedir?", kategori="yakin"),
    dict(id="k-edirne", soru="Osmanlı başkenti Edirne'ye ne zaman taşınmıştır?", kategori="yakin"),
    dict(id="k-alparslan-olum", soru="Sultan Alparslan hangi yıl ölmüştür?", kategori="yakin"),
    dict(id="k-gokalp-olum", soru="Ziya Gökalp hangi şehirde vefat etmiştir?", kategori="yakin"),
    dict(id="k-macar-kral", soru="Mohaç Savaşı'nda yenilen Macar kralının adı nedir?", kategori="yakin"),
    dict(id="k-thomsen-univ", soru="Vilhelm Thomsen hangi üniversitede çalışıyordu?", kategori="yakin"),
    dict(id="k-korkut-hikaye", soru="Dede Korkut Kitabı'ndaki ilk hikâyenin adı nedir?", kategori="yakin"),
    # Tuzak: belgede Mustafa Kemal'in Birinci Dunya Savasi'nda Dogu Cephesi'nde
    # gorev yaptigi yaziyor; Kurtulus Savasi'ndaki komutan yazmiyor.
    dict(id="k-dogu-cephesi", soru="Kurtuluş Savaşı'nda Doğu Cephesi komutanı kimdi?", kategori="yakin"),
]

KONTROL_SENARYOLAR = [
    # ----------------------------------------------- takip, cevap belgede var
    dict(id="k-takip-gokalp", tip="takip", sorular=[
        dict(soru="Ziya Gökalp nerede doğmuştur?"),
        dict(soru="hangi formülü savunmuştur?",
             belge="turk-milliyetciliginin-dogusu.md", kanit="Türkleşmek, İslamlaşmak, Muasırlaşmak",
             anahtar=["Türkleşmek", "Muasırlaşmak"]),
    ]),
    dict(id="k-takip-korkut", tip="takip", sorular=[
        dict(soru="Dede Korkut Kitabı kaç hikâyeden oluşur?"),
        dict(soru="yazmaları nerede bulunuyor?",
             belge="turk-destanlari.md", kanit="Dresden ve Vatikan",
             anahtar=["Dresden", "Vatikan"]),
    ]),
    dict(id="k-takip-sam", tip="takip", sorular=[
        dict(soru="Mustafa Kemal Harp Akademisi'ni hangi yıl bitirmiştir?"),
        dict(soru="ilk görev yeri neresiydi?",
             belge="mustafa-kemal-ataturk.md", kanit="Şam'daki 5. Ordu",
             anahtar=["Şam"]),
    ]),
    dict(id="k-takip-konya", tip="takip", sorular=[
        dict(soru="Anadolu Selçuklu Devleti'nin ilk merkezi neresiydi?"),
        dict(soru="başkenti daha sonra nereye taşındı?",
             belge="selcuklular-ve-malazgirt.md", kanit="başkentini Konya'ya taşımıştır",
             anahtar=["Konya"]),
    ]),

    # ---------------------------------------------- takip, cevap belgede yok
    dict(id="k-cevapsiz-malazgirt", tip="takip_cevapsiz", sorular=[
        dict(soru="Malazgirt Savaşı ne zaman yapılmıştır?"),
        dict(soru="savaşta kaç kişi öldü?"),
    ]),
    dict(id="k-cevapsiz-nutuk", tip="takip_cevapsiz", sorular=[
        dict(soru="Nutuk ne zaman okunmuştur?"),
        dict(soru="kaç sayfadır?"),
    ]),
    dict(id="k-cevapsiz-tdk", tip="takip_cevapsiz", sorular=[
        dict(soru="Türk Dil Kurumu ne zaman kurulmuştur?"),
        dict(soru="ilk başkanı kimdi?"),
    ]),
    dict(id="k-cevapsiz-mohac", tip="takip_cevapsiz", sorular=[
        dict(soru="Mohaç Savaşı hangi yıl yapılmıştır?"),
        dict(soru="karşı taraftaki kralın adı neydi?"),
    ]),
    # Tuzak: "Ötüken" belgede yalnizca bir dergi adi olarak geciyor.
    dict(id="k-cevapsiz-baskent", tip="takip_cevapsiz", sorular=[
        dict(soru="Göktürk Devleti ne zaman kurulmuştur?"),
        dict(soru="başkenti neresiydi?"),
    ]),
    dict(id="k-cevapsiz-uygur", tip="takip_cevapsiz", sorular=[
        dict(soru="Uygur Kağanlığı hangi yıl kurulmuştur?"),
        dict(soru="ne zaman yıkıldı?"),
    ]),

    # ----------------------------------------------- konu degisimi, kisa soru
    dict(id="k-degisim-otag", tip="konu_degisimi", sorular=[
        dict(soru="Lozan Antlaşması ne zaman imzalanmıştır?"),
        dict(soru="Otağ nedir?",
             belge="turk-devlet-gelenegi.md", kanit="tuğ, otağ, taht ve davul",
             anahtar=["sembol"]),
    ]),
    dict(id="k-degisim-okculuk", tip="konu_degisimi", sorular=[
        dict(soru="Orhun Yazıtları kimler adına dikilmiştir?"),
        dict(soru="Atlı okçuluk nedir?",
             belge="turk-kulturunde-at.md", kanit="dörtnala giderken ok atabilme",
             anahtar=["dörtnala|ok at"]),
    ]),
    dict(id="k-degisim-tugrul", tip="konu_degisimi", sorular=[
        dict(soru="Yusuf Akçura'nın yazısı nerede yayımlanmıştır?"),
        dict(soru="Tuğrul Bey kimdir?",
             belge="selcuklular-ve-malazgirt.md", kanit="Tuğrul Bey ilk sultan olarak",
             anahtar=["sultan"]),
    ]),

    # ------------------------------------------ konu disi, onceki sorudan sonra
    dict(id="k-disi-telefon", tip="konu_disi_sonra", sorular=[
        dict(soru="Kurultayda hangi kararlar alınırdı?"),
        dict(soru="En iyi akıllı telefon hangisidir?"),
    ]),
    dict(id="k-disi-yagmur", tip="konu_disi_sonra", sorular=[
        dict(soru="Türk Ocağı ne zaman kurulmuştur?"),
        dict(soru="Yarın İstanbul'da yağmur yağacak mı?"),
    ]),
]
