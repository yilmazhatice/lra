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

    # ------------------------------------------- turklerin-islamiyeti-kabulu.md
    dict(id="islam-1", soru="Talas Savaşı hangi yıl yapılmıştır?",
         belge="turklerin-islamiyeti-kabulu.md", kanit="Talas Savaşı 751 yılında",
         anahtar=["751"]),
    dict(id="islam-2", soru="Talas Savaşı'nda hangi Türk boyu Abbasîlerin yanında yer almıştır?",
         belge="turklerin-islamiyeti-kabulu.md", kanit="Karluk Türklerinin Abbasîlerin yanında",
         anahtar=["Karluk"]),
    dict(id="islam-3", soru="İslamiyet'i resmî din olarak kabul eden ilk Türk devleti hangisidir?",
         belge="turklerin-islamiyeti-kabulu.md", kanit="İslamiyet'i resmî din olarak kabul eden ilk Türk devleti",
         anahtar=["Bulgar"]),
    dict(id="islam-4", soru="Satuk Buğra Han Müslüman olduktan sonra hangi adı almıştır?", kategori="ozel_ad",
         belge="turklerin-islamiyeti-kabulu.md", kanit="Abdülkerim adını almıştır",
         anahtar=["Abdülkerim"]),
    dict(id="islam-5", soru="Gazneli Devleti'nin en parlak dönemi hangi hükümdarın zamanıdır?",
         belge="turklerin-islamiyeti-kabulu.md", kanit="998-1030 arasında hüküm süren Gazneli Mahmud",
         anahtar=["Mahmud"]),

    # ------------------------------------------------ ilk-turk-islam-eserleri.md
    dict(id="eser-1", soru="Kutadgu Bilig'i kim yazmıştır?",
         belge="ilk-turk-islam-eserleri.md", kanit="Yusuf Has Hâcib tarafından yazılmış",
         anahtar=["Yusuf Has Hâcib|Yusuf Has Hacib"]),
    dict(id="eser-2", soru="Kutadgu Bilig'de hükümdar Küntoğdı neyi temsil eder?",
         belge="ilk-turk-islam-eserleri.md", kanit="Küntoğdı adaleti ve kanunu",
         anahtar=["adalet"]),
    dict(id="eser-3", soru="Dîvânu Lugâti't-Türk hangi amaçla yazılmıştır?",
         belge="ilk-turk-islam-eserleri.md", kanit="Araplara Türkçe öğretmektir",
         anahtar=["Arap"]),
    dict(id="eser-4", soru="Atabetü'l-Hakayık'ı kim yazmıştır?", kategori="ozel_ad",
         belge="ilk-turk-islam-eserleri.md", kanit="Edip Ahmed Yükneki tarafından",
         anahtar=["Yükneki"]),
    dict(id="eser-5", soru="Dîvân-ı Hikmet'te hangi ölçü kullanılmıştır?",
         belge="ilk-turk-islam-eserleri.md", kanit="aruz yerine hece ölçüsü ve dörtlük",
         anahtar=["hece"]),

    # ----------------------------------------------- osmanli-devlet-teskilati.md
    dict(id="teskilat-1", soru="Divan-ı Hümayun'a Fatih Sultan Mehmed'den sonra kim başkanlık etmiştir?",
         belge="osmanli-devlet-teskilati.md", kanit="başkanlığın veziriazama bırakılması",
         anahtar=["veziriazam|sadrazam"]),
    dict(id="teskilat-2", soru="Nişancının görevi nedir?",
         belge="osmanli-devlet-teskilati.md", kanit="padişah fermanlarına tuğra çekmekten",
         anahtar=["tuğra"]),
    dict(id="teskilat-3", soru="Tımar sisteminde sipahinin yetiştirdiği atlı askerlere ne ad verilir?", kategori="ozel_ad",
         belge="osmanli-devlet-teskilati.md", kanit="cebelü denilen atlı askerleri",
         anahtar=["cebelü"]),
    # Ayni olay osmanli-islahat belgesinde II. Mahmud reformlari icinde de anlatiliyor.
    dict(id="teskilat-4", soru="Yeniçeri Ocağı hangi olayla kaldırılmıştır?",
         belge="osmanli-devlet-teskilati.md|osmanli-islahat-ve-mesrutiyet.md",
         kanit="Vaka-i Hayriye ile kaldırılmıştır|bu olay Vaka-i Hayriye olarak anılır",
         anahtar=["Vaka-i Hayriye"]),
    dict(id="teskilat-5", soru="Millet sisteminde gayrimüslimler hangi esasa göre örgütlenmiştir?",
         belge="osmanli-devlet-teskilati.md", kanit="etnik köken yerine mezhep esasına göre",
         anahtar=["mezhep|din"]),

    # ------------------------------------------ osmanli-islahat-ve-mesrutiyet.md
    dict(id="islahat-1", soru="Karlofça Antlaşması hangi yıl imzalanmıştır?",
         belge="osmanli-islahat-ve-mesrutiyet.md", kanit="1699'da imzalanan Karlofça Antlaşması",
         anahtar=["1699"]),
    dict(id="islahat-2", soru="İlk Türk matbaasını kimler kurmuştur?",
         belge="osmanli-islahat-ve-mesrutiyet.md", kanit="İbrahim Müteferrika ile Said Efendi 1727'de",
         anahtar=["Müteferrika"]),
    dict(id="islahat-3", soru="III. Selim'in kurduğu yeni ordunun adı nedir?", kategori="ozel_ad",
         belge="osmanli-islahat-ve-mesrutiyet.md", kanit="Nizam-ı Cedid adıyla Avrupa usulünde",
         anahtar=["Nizam-ı Cedid"]),
    dict(id="islahat-4", soru="Tanzimat Fermanı hangi tarihte okunmuştur?",
         belge="osmanli-islahat-ve-mesrutiyet.md", kanit="3 Kasım 1839'da Mustafa Reşid Paşa",
         anahtar=["3 Kasım 1839|1839"]),
    dict(id="islahat-5", soru="I. Meşrutiyet hangi tarihte ilan edilmiştir?",
         belge="osmanli-islahat-ve-mesrutiyet.md", kanit="23 Aralık 1876'da Kanun-i Esasi",
         anahtar=["23 Aralık 1876|1876"]),

    # ----------------------------------------------- cumhuriyet-inkilaplari.md
    dict(id="inkilap-1", soru="Saltanat hangi tarihte kaldırılmıştır?",
         belge="cumhuriyet-inkilaplari.md", kanit="1 Kasım 1922'de saltanata son vermiş",
         anahtar=["1 Kasım 1922"]),
    dict(id="inkilap-2", soru="Halifelik hangi tarihte kaldırılmıştır?",
         belge="cumhuriyet-inkilaplari.md", kanit="3 Mart 1924'te ise aynı gün çıkarılan üç kanunla halifelik",
         anahtar=["3 Mart 1924"]),
    dict(id="inkilap-3", soru="Türk Medeni Kanunu hangi ülkenin kanunu esas alınarak hazırlanmıştır?",
         belge="cumhuriyet-inkilaplari.md", kanit="İsviçre Medeni Kanunu esas alınarak",
         anahtar=["İsviçre"]),
    dict(id="inkilap-4", soru="Kadınlara milletvekili seçme ve seçilme hakkı ne zaman tanınmıştır?",
         belge="cumhuriyet-inkilaplari.md", kanit="5 Aralık 1934'te yapılan anayasa değişikliğiyle",
         anahtar=["5 Aralık 1934|1934"]),
    dict(id="inkilap-5", soru="Soyadı Kanunu hangi tarihte kabul edilmiştir?",
         belge="cumhuriyet-inkilaplari.md", kanit="21 Haziran 1934 tarihli Soyadı Kanunu",
         anahtar=["21 Haziran 1934|1934"]),

    # ----------------------------- anadolu-beylikleri-ve-osmanlinin-kurulusu.md
    dict(id="beylik-1", soru="Osmanlı Devleti'ne katılan ilk beylik hangisidir?",
         belge="anadolu-beylikleri-ve-osmanlinin-kurulusu.md", kanit="Karesi, Osmanlı Devleti'ne katılan ilk beyliktir",
         anahtar=["Karesi"]),
    dict(id="beylik-2", soru="Türkçenin resmî dil olarak kullanılmasına dair buyruğu kim vermiştir?",
         belge="anadolu-beylikleri-ve-osmanlinin-kurulusu.md", kanit="Karamanoğlu Mehmed Bey'in 1277'de",
         anahtar=["Karamanoğlu Mehmed"]),
    dict(id="beylik-3", soru="Malazgirt sonrası kurulan beyliklerden hangisi donanmasıyla tanınır?",
         belge="anadolu-beylikleri-ve-osmanlinin-kurulusu.md", kanit="Çaka Beyliği ise donanma kurup",
         anahtar=["Çaka"]),
    dict(id="beylik-4", soru="Osmanlılar Rumeli'ye hangi kalenin alınmasıyla geçmiştir?",
         belge="anadolu-beylikleri-ve-osmanlinin-kurulusu.md", kanit="Çimpe Kalesi'nin alınmasıyla Rumeli'ye",
         anahtar=["Çimpe"]),
    dict(id="beylik-5", soru="Osmanlı'nın fethettiği yerlerdeki halka uyguladığı politikanın adı nedir?", kategori="ozel_ad",
         belge="anadolu-beylikleri-ve-osmanlinin-kurulusu.md", kanit="istimâlet politikasıdır",
         anahtar=["istimâlet|istimalet"]),

    # --------------------------------------------- turk-mitolojisi-ve-gok-tanri.md
    dict(id="mit-1", soru="Eski Türk inancında tek yaratıcı güce ne ad verilir?", kategori="ozel_ad",
         belge="turk-mitolojisi-ve-gok-tanri.md", kanit="Tengri adı verilen bu varlık",
         anahtar=["Tengri|Gök Tanrı"]),
    dict(id="mit-2", soru="Umay neyi korur?",
         belge="turk-mitolojisi-ve-gok-tanri.md", kanit="Doğumu, çocukları ve bereketi koruduğuna",
         anahtar=["doğum|çocuk"]),
    dict(id="mit-3", soru="Türk inancında ruhlarla ilişki kurduğuna inanılan din adamına ne denir?", kategori="ozel_ad",
         belge="turk-mitolojisi-ve-gok-tanri.md", kanit="Kam, ruhlarla ilişki kurduğuna inanılan din adamıdır",
         anahtar=["kam"]),
    dict(id="mit-4", soru="Ölünün ardından yapılan yas törenine ne ad verilir?", kategori="ozel_ad",
         belge="turk-mitolojisi-ve-gok-tanri.md", kanit="Ölünün ardından yapılan törene yuğ denir",
         anahtar=["yuğ"]),
    dict(id="mit-5", soru="Uygur Kağanlığı hangi dini resmî din olarak benimsemiştir?",
         belge="turk-mitolojisi-ve-gok-tanri.md", kanit="763'te Maniheizm'i resmî din olarak benimsemiş",
         anahtar=["Maniheizm"]),

    # ------------------------------------------- oguz-boylari-ve-turk-boy-yapisi.md
    dict(id="boy-1", soru="Eski Türk toplumunda en küçük birim nedir?",
         belge="oguz-boylari-ve-turk-boy-yapisi.md", kanit="En küçük birim oguş yani ailedir",
         anahtar=["oguş|aile"]),
    dict(id="boy-2", soru="Oğuzlar kaç boya ayrılır?",
         belge="oguz-boylari-ve-turk-boy-yapisi.md", kanit="Yirmi dört boya ayrıldıkları",
         anahtar=["yirmi dört|24"]),
    dict(id="boy-3", soru="Oğuz boylarının iki kolunun adı nedir?",
         belge="oguz-boylari-ve-turk-boy-yapisi.md", kanit="Bozoklar ile Üçoklar olmak üzere iki kola",
         anahtar=["Bozok", "Üçok"]),
    dict(id="boy-4", soru="Osmanlı hanedanı hangi boydan çıkmıştır?",
         belge="oguz-boylari-ve-turk-boy-yapisi.md", kanit="Kayı boyundan Osmanlı hanedanı",
         anahtar=["Kayı"]),
    dict(id="boy-5", soru="Boyların kullandığı işarete ne ad verilir?", kategori="ozel_ad",
         belge="oguz-boylari-ve-turk-boy-yapisi.md", kanit="tamga adı verilen bu işaret",
         anahtar=["tamga|damga"]),

    # ---------------------------------------------------- bozkir-gocebe-yasami.md
    dict(id="bozkir-1", soru="Bozkırda yazın çıkılan otlağa ne ad verilir?", kategori="ozel_ad",
         belge="bozkir-gocebe-yasami.md", kanit="yüksek otlaklara, yani yaylağa çıkarılır",
         anahtar=["yaylak|yaylağ"]),
    dict(id="bozkir-2", soru="Bozkır çadırının tepesindeki çember ne işe yarar?",
         belge="bozkir-gocebe-yasami.md", kanit="Tepedeki çember hem baca hem pencere",
         anahtar=["baca|pencere|duman"]),
    dict(id="bozkir-3", soru="Hükümdarın çadırına ne ad verilir?", kategori="ozel_ad",
         belge="bozkir-gocebe-yasami.md", kanit="Hükümdarın çadırına otağ denir",
         anahtar=["otağ"]),
    dict(id="bozkir-4", soru="Bilinen en eski düğümlü halı nerede bulunmuştur?",
         belge="bozkir-gocebe-yasami.md", kanit="Pazırık kurganında bulunan",
         anahtar=["Pazırık"]),
    dict(id="bozkir-5", soru="Göktürkler ipek ticareti için hangi devlete elçilik göndermiştir?",
         belge="bozkir-gocebe-yasami.md", kanit="568 yılında Bizans'a elçilik heyeti",
         anahtar=["Bizans"]),

    # ------------------------------------------------- nevruz-ve-turk-bayramlari.md
    dict(id="nevruz-1", soru="Nevruz hangi tarihte kutlanır?",
         belge="nevruz-ve-turk-bayramlari.md", kanit="Nevruz, 21 Mart'ta",
         anahtar=["21 Mart"]),
    dict(id="nevruz-2", soru="Nevruz Kazakistan'da hangi adla anılır?", kategori="ozel_ad",
         belge="nevruz-ve-turk-bayramlari.md", kanit="Kazakistan'da Nauryz",
         anahtar=["Nauryz"]),
    dict(id="nevruz-3", soru="Nevruz'da buğdayın filizlendirilmesiyle hazırlanan yiyeceğin adı nedir?", kategori="ozel_ad",
         belge="nevruz-ve-turk-bayramlari.md", kanit="semeni ya da sümelek",
         anahtar=["semeni|sümelek"]),
    dict(id="nevruz-4", soru="Hıdrellez hangi tarihte kutlanır?",
         belge="nevruz-ve-turk-bayramlari.md", kanit="6 Mayıs'ta kutlanır",
         anahtar=["6 Mayıs"]),
    dict(id="nevruz-5", soru="Hıdrellez adı nereden gelmektedir?",
         belge="nevruz-ve-turk-bayramlari.md", kanit="Hızır ile İlyas adlarının birleşmesinden",
         anahtar=["Hızır", "İlyas"]),

    # -------------------------------------------------------- ozan-asik-gelenegi.md
    dict(id="ozan-1", soru="İslamiyet öncesinde destan anlatan kişiye ne ad verilirdi?", kategori="ozel_ad",
         belge="ozan-asik-gelenegi.md", kanit="bu kişiye ozan denirdi",
         anahtar=["ozan"]),
    dict(id="ozan-2", soru="Kırgızlarda destan anlatıcısına ne ad verilir?", kategori="ozel_ad",
         belge="ozan-asik-gelenegi.md", kanit="destan anlatıcısına manasçı denir",
         anahtar=["manasçı"]),
    dict(id="ozan-3", soru="İki âşığın karşılıklı doğaçlama şiir söylemesine ne ad verilir?", kategori="ozel_ad",
         belge="ozan-asik-gelenegi.md", kanit="atışma ya da karşılaşma denir",
         anahtar=["atışma|karşılaşma"]),
    dict(id="ozan-4", soru="Telli sazların atası sayılan çalgı hangisidir?",
         belge="ozan-asik-gelenegi.md", kanit="telli sazların atası sayılan kopuzdur",
         anahtar=["kopuz"]),
    dict(id="ozan-5", soru="Bağlama ailesinin en küçük üyesi hangisidir?",
         belge="ozan-asik-gelenegi.md", kanit="En küçüğü cura",
         anahtar=["cura"]),

    # ----------------------------------------------- turk-islam-dunyasinda-bilim.md
    dict(id="bilim-1", soru="Cebir sözcüğü kimin eserinden gelmektedir?",
         belge="turk-islam-dunyasinda-bilim.md", kanit="cebir sözcüğü bu kitabın adındaki",
         anahtar=["Hârezmî|Harezmi"]),
    dict(id="bilim-2", soru="Fârâbî'ye hangi unvan verilmiştir?", kategori="ozel_ad",
         belge="turk-islam-dunyasinda-bilim.md", kanit="Muallim-i Sânî",
         anahtar=["Muallim-i Sânî|İkinci Öğretmen"]),
    dict(id="bilim-3", soru="İbn Sînâ'nın tıp alanındaki temel eseri hangisidir?",
         belge="turk-islam-dunyasinda-bilim.md", kanit="el-Kânûn fi't-Tıbb",
         anahtar=["Kânûn|Kanun"]),
    dict(id="bilim-4", soru="Uluğ Bey kimin torunudur?",
         belge="turk-islam-dunyasinda-bilim.md", kanit="Timur'un torunudur",
         anahtar=["Timur"]),
    dict(id="bilim-5", soru="Ali Kuşçu'yu İstanbul'a kim davet etmiştir?",
         belge="turk-islam-dunyasinda-bilim.md", kanit="Fatih Sultan Mehmed'in daveti üzerine",
         anahtar=["Fatih"]),

    # ---------------------------------------------- selcuklu-ve-osmanli-mimarisi.md
    dict(id="mimari-1", soru="Selçuklu yapılarındaki anıtsal giriş kapısına ne ad verilir?", kategori="ozel_ad",
         belge="selcuklu-ve-osmanli-mimarisi.md", kanit="buna taçkapı denir",
         anahtar=["taçkapı"]),
    dict(id="mimari-2", soru="Altında mezar odası bulunan anıt mezara ne ad verilir?", kategori="ozel_ad",
         belge="selcuklu-ve-osmanli-mimarisi.md", kanit="Kümbet, altında mezar odası",
         anahtar=["kümbet"]),
    dict(id="mimari-3", soru="Divriği Ulu Camii ne zaman yapılmıştır?",
         belge="selcuklu-ve-osmanli-mimarisi.md", kanit="1228-1229 yıllarında Mengücekliler",
         anahtar=["1228|1229"]),
    dict(id="mimari-4", soru="Mimar Sinan ustalık eseri olarak hangi yapıyı göstermiştir?",
         belge="selcuklu-ve-osmanli-mimarisi.md", kanit="ustalık eseri olarak Edirne'deki Selimiye",
         anahtar=["Selimiye"]),
    dict(id="mimari-5", soru="Kervansaraylar birbirinden hangi aralıklarla yapılmıştır?",
         belge="selcuklu-ve-osmanli-mimarisi.md", kanit="otuz ila kırk kilometre aralıklarla",
         anahtar=["otuz|kırk"]),

    # ------------------------------------------------------------ turk-denizciligi.md
    dict(id="deniz-1", soru="Bilinen ilk Türk denizci beyi kimdir?",
         belge="turk-denizciligi.md", kanit="beylik kuran Çaka Bey",
         anahtar=["Çaka"]),
    dict(id="deniz-2", soru="Preveze Deniz Savaşı hangi tarihte yapılmıştır?",
         belge="turk-denizciligi.md", kanit="Preveze Deniz Savaşı 28 Eylül 1538",
         anahtar=["28 Eylül 1538|1538"]),
    dict(id="deniz-3", soru="Preveze'de Osmanlı donanmasının karşısındaki komutan kimdir?",
         belge="turk-denizciligi.md", kanit="Andrea Doria komutasındaki Haçlı donanmasını",
         anahtar=["Andrea Doria"]),
    dict(id="deniz-4", soru="Piri Reis'in Akdeniz kılavuzu niteliğindeki eseri hangisidir?",
         belge="turk-denizciligi.md", kanit="Kitâb-ı Bahriye",
         anahtar=["Bahriye"]),
    dict(id="deniz-5", soru="Kabotaj Kanunu ne zaman yürürlüğe girmiştir?",
         belge="turk-denizciligi.md", kanit="1 Temmuz 1926'da yürürlüğe giren Kabotaj Kanunu",
         anahtar=["1 Temmuz 1926|1926"]),

    # -------------------------------------------------------------- milli-semboller.md
    dict(id="sembol-1", soru="İstiklal Marşı TBMM'de hangi tarihte kabul edilmiştir?",
         belge="milli-semboller.md", kanit="12 Mart 1921'de millî marş olarak kabul",
         anahtar=["12 Mart 1921"]),
    dict(id="sembol-2", soru="Mehmet Âkif İstiklal Marşı'nı nerede yazmıştır?",
         belge="milli-semboller.md", kanit="Tacettin Dergâhı'nda yazmıştır",
         anahtar=["Tacettin"]),
    dict(id="sembol-3", soru="İstiklal Marşı kaç mısradan oluşur?",
         belge="milli-semboller.md", kanit="Kırk bir mısradan oluşur",
         anahtar=["kırk bir|41"]),
    dict(id="sembol-4", soru="Anıtkabir'in projesini kimler hazırlamıştır?",
         belge="milli-semboller.md", kanit="Emin Onat ve Orhan Arda'nın projesi",
         anahtar=["Emin Onat", "Orhan Arda"]),
    dict(id="sembol-5", soru="Anıtkabir'deki Aslanlı Yol'da kaç aslan heykeli vardır?",
         belge="milli-semboller.md", kanit="yirmi dört aslan heykeli",
         anahtar=["yirmi dört|24"]),

    # ---------------------------------------------------------- bugunku-turk-dunyasi.md
    dict(id="dunya-1", soru="Kuzey Kıbrıs Türk Cumhuriyeti ne zaman ilan edilmiştir?",
         belge="bugunku-turk-dunyasi.md", kanit="15 Kasım 1983'te ilan edilmiştir",
         anahtar=["15 Kasım 1983|1983"]),
    dict(id="dunya-2", soru="Türk Devletleri Teşkilatı hangi anlaşmayla kurulmuştur?",
         belge="bugunku-turk-dunyasi.md", kanit="Nahçıvan Anlaşması",
         anahtar=["Nahçıvan"]),
    dict(id="dunya-3", soru="Türk Keneşi'nin adı ne zaman Türk Devletleri Teşkilatı olarak değişmiştir?",
         belge="bugunku-turk-dunyasi.md", kanit="12 Kasım 2021'deki İstanbul zirvesinde",
         anahtar=["2021"]),
    dict(id="dunya-4", soru="TÜRKSOY ne zaman kurulmuştur?",
         belge="bugunku-turk-dunyasi.md", kanit="1993'te kurulmuş ve merkezi Ankara",
         anahtar=["1993"]),
    dict(id="dunya-5", soru="Moldova'daki özerk Türk bölgesinin adı nedir?", kategori="ozel_ad",
         belge="bugunku-turk-dunyasi.md", kanit="Gagavuz Yeri özerk bölgesinde",
         anahtar=["Gagavuz"]),

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

# ---------------------------------------------------------------------------
# Ikinci kontrol seti (28 belgelik koleksiyon icin, 2026-09-19).
#
# Birinci kontrol seti (KONTROL_SORULAR) 13 belgelik koleksiyon icin yazilmisti
# ve bagimsizligini yitirdi: 2026-09-18'de "Ulus nedir?" ile Dede Korkut
# sorularindaki basarisizliklara bakilip belgeler ona gore duzeltildi. Tarihsel
# kayit olarak duruyor, ama artik gorulmemis bir olcek degil.
#
# Bu set sonuclari gorulmeden yazildi ve donduruldu. Onyargiyi azaltmak icin
# sorular sistematik uretildi: ana setin hic kullanmadigi paragraflar
# taranip her birinden bir olgu sorusu yazildi (olcum_betikleri/
# kontrol2_kapsam.py). Zayif noktalar hedeflenmedi ya da korunmadi.
#
# SINIRLAMA: seti yazan, ayni oturumda sistemin butun basarisizlik
# bicimlerini gormus olan asistandir. Sistemi hic gormemis birinin yazdigi
# bir set kadar bagimsiz degildir; bu kayit altina alinmistir.
# Ayar icin KULLANILMAZ. Calistirmak icin: python evaluate.py --set kontrol2
# ---------------------------------------------------------------------------

KONTROL2_SORULAR = [
    # ------------------------------------------------------ cevaplanabilir
    dict(id="k2-beylik-konum", soru="Osmanlı Beyliği'nin büyümesinde coğrafi konumun rolü nedir?",
         belge="anadolu-beylikleri-ve-osmanlinin-kurulusu.md",
         kanit="beylik doğrudan Bizans sınırında bulunduğu", anahtar=["Bizans"]),
    dict(id="k2-asistan-internet", soru="Asistan çalışmak için internet bağlantısına ihtiyaç duyar mı?",
         belge="asistan-hakkinda.md",
         kanit="internet bağlantısı olmadan da kullanılabilir", anahtar=["internet"]),
    dict(id="k2-juanjuan", soru="Göktürkler bağımsızlıklarından önce hangi devlet için demir işlemiştir?",
         belge="bozkir-gocebe-yasami.md",
         kanit="Juan-juan Devleti için demir işlediği", anahtar=["Juan-juan"]),
    dict(id="k2-kirgizistan", soru="Kırgızistan bağımsızlığını ne zaman ilan etmiştir?",
         belge="bugunku-turk-dunyasi.md",
         kanit="Kırgızistan 31 Ağustos 1991'de", anahtar=["31 Ağustos 1991|1991"]),
    dict(id="k2-kuvayi", soru="İşgallere karşı ilk tepki hangi birliklerden gelmiştir?",
         belge="canakkale-ve-kurtulus-savasi.md",
         kanit="Kuvâ-yi Milliye adıyla anılan gönüllü birliklerden", anahtar=["Kuvâ-yi Milliye|Kuva-yi Milliye"]),
    dict(id="k2-ilk-anayasa", soru="İlk anayasa hangi tarihte kabul edilmiştir?",
         belge="cumhuriyet-inkilaplari.md",
         kanit="20 Ocak 1921'de kabul edilen Teşkilat-ı Esasiye", anahtar=["20 Ocak 1921|1921"]),
    dict(id="k2-dlt-harita", soru="Dîvânu Lugâti't-Türk'teki haritanın merkezinde hangi şehir vardır?",
         belge="ilk-turk-islam-eserleri.md",
         kanit="merkezine Balasagun yerleştirilmiştir", anahtar=["Balasagun"]),
    dict(id="k2-akif-meslek", soru="Mehmet Âkif Ersoy hangi mesleği yapmıştır?",
         belge="milli-semboller.md",
         kanit="veteriner hekim olmuş", anahtar=["veteriner"]),
    dict(id="k2-sofya", soru="Mustafa Kemal Sofya'da hangi görevde bulunmuştur?",
         belge="mustafa-kemal-ataturk.md",
         kanit="Sofya'da askerî ataşe olarak", anahtar=["ataşe"]),
    dict(id="k2-nevruz-bm", soru="Birleşmiş Milletler 21 Mart'ı ne ilan etmiştir?",
         belge="nevruz-ve-turk-bayramlari.md",
         kanit="Dünya Nevruz Günü ilan etmiştir", anahtar=["Dünya Nevruz Günü"]),
    dict(id="k2-avar", soru="Avarlar İstanbul'u hangi yılda kuşatmıştır?",
         belge="oguz-boylari-ve-turk-boy-yapisi.md",
         kanit="626'da İstanbul'u kuşatmıştır", anahtar=["626"]),
    dict(id="k2-kadi", soru="Osmanlı taşra yönetiminde kaza düzeyinde kim görev yapardı?", kategori="ozel_ad",
         belge="osmanli-devlet-teskilati.md",
         kanit="Kaza düzeyinde ise kadı görev yapar", anahtar=["kadı"]),
    dict(id="k2-kafes", soru="Şehzadelerin sarayda tutulduğu düzene ne ad verilir?", kategori="ozel_ad",
         belge="osmanli-islahat-ve-mesrutiyet.md",
         kanit="kafes adı verilen düzende", anahtar=["kafes"]),
    dict(id="k2-mehter-calgi", soru="Mehter topluluğunda hangi çalgılar bulunur?",
         belge="ozan-asik-gelenegi.md",
         kanit="zurna, boru, kös, nakkare, davul ve zil", anahtar=["zurna"]),
    dict(id="k2-sinan-dogum", soru="Mimar Sinan nerede doğmuştur?",
         belge="selcuklu-ve-osmanli-mimarisi.md",
         kanit="Kayseri'nin Ağırnas köyünde doğmuş", anahtar=["Ağırnas|Kayseri"]),
    dict(id="k2-barbaros-cezayir", soru="Barbaros Hayreddin Paşa hangi şehrin yönetimini üstlenmiştir?",
         belge="turk-denizciligi.md",
         kanit="Cezayir'in yönetimini üstlenmiş", anahtar=["Cezayir"]),
    dict(id="k2-saka-destan", soru="Sakalara ait destanlar hangileridir?",
         belge="turk-destanlari.md",
         kanit="Sakalara ait Alp Er Tunga ve Şu", anahtar=["Alp Er Tunga"]),
    dict(id="k2-biruni-dil", soru="Bîrûnî hangi dili öğrenmiştir?",
         belge="turk-islam-dunyasinda-bilim.md",
         kanit="Sanskritçe öğrenmiştir", anahtar=["Sanskritçe"]),
    dict(id="k2-kurt-tug", soru="Göktürklerde kurt figürü nerelerde kullanılmıştır?",
         belge="turk-kulturunde-kurt.md",
         kanit="kurt başlı tuğların kullanıldığı", anahtar=["tuğ"]),
    dict(id="k2-kutsal-sayi", soru="Türk inancında hangi sayılar kutsal sayılır?",
         belge="turk-mitolojisi-ve-gok-tanri.md",
         kanit="Üç, yedi, dokuz ve kırk", anahtar=["dokuz", "kırk"]),
    dict(id="k2-karahanli-bolunme", soru="Karahanlı Devleti ne zaman ikiye ayrılmıştır?",
         belge="turklerin-islamiyeti-kabulu.md",
         kanit="1042'de Doğu ve Batı Karahanlılar", anahtar=["1042"]),
    dict(id="k2-uygur-matbaa", soru="Uygurlar metin çoğaltmak için hangi tekniği kullanmıştır?",
         belge="ilk-turk-devletleri.md",
         kanit="matbaanın erken biçimlerini kullanmış", anahtar=["matbaa"]),
    dict(id="k2-miryokefalon", soru="Miryokefalon Savaşı'nın sonucu ne olmuştur?",
         belge="selcuklular-ve-malazgirt.md",
         kanit="Bizans'ın Anadolu'yu geri alma girişimi başarısız", anahtar=["başarısız"]),
    dict(id="k2-kut-soy", soru="Kut kime verilmiş sayılırdı?",
         belge="turk-devlet-gelenegi.md",
         kanit="kişiye değil soya verilmiş sayıldığı", anahtar=["soy"]),
    dict(id="k2-uygur-alfabe", soru="Uygur alfabesi kaç harften oluşur?",
         belge="turkcenin-tarihi-ve-alfabeleri.md",
         kanit="on dört harften oluşur", anahtar=["on dört|14"]),
    dict(id="k2-fetret", soru="Fetret Devri kaç yıl sürmüştür?",
         belge="osmanli-padisahlari.md",
         kanit="on bir yıllık taht mücadelesine", anahtar=["on bir|11"]),
    dict(id="k2-ahal-teke", soru="Ahal Teke atı hangi özellikleriyle bilinir?",
         belge="turk-kulturunde-at.md",
         kanit="dayanıklılıkları ve uzun mesafe", anahtar=["dayanıklı"]),
    dict(id="k2-turk-yurdu", soru="Türk Yurdu dergisi ne zaman kurulmuştur?",
         belge="turk-milliyetciliginin-dogusu.md",
         kanit="Türk Yurdu dergisi 1911'de", anahtar=["1911"]),
    dict(id="k2-sened", soru="Sened-i İttifak hangi yıl imzalanmıştır?",
         belge="osmanli-islahat-ve-mesrutiyet.md",
         kanit="1808'de ayanlarla Sened-i İttifak", anahtar=["1808"]),

    # -------------------------------------------------------- cevaplanamaz
    dict(id="k2-cevapsiz-sinan-sayi", soru="Mimar Sinan tam olarak kaç yapı inşa etmiştir?", kategori="yakin"),
    dict(id="k2-cevapsiz-barbaros-dogum", soru="Barbaros Hayreddin Paşa hangi yıl doğmuştur?", kategori="yakin"),
    dict(id="k2-cevapsiz-akif-mezar", soru="Mehmet Âkif Ersoy nereye gömülmüştür?", kategori="yakin"),
    dict(id="k2-cevapsiz-pecenek-nufus", soru="Peçeneklerin nüfusu ne kadardı?", kategori="yakin"),
    dict(id="k2-cevapsiz-biruni-ogrenci", soru="Bîrûnî'nin öğrencileri kimlerdi?", kategori="yakin"),
    dict(id="k2-cevapsiz-kadi-maas", soru="Osmanlı'da kadılar ne kadar maaş alırdı?", kategori="yakin"),
    dict(id="k2-disi-corba", soru="Mercimek çorbası nasıl yapılır?", kategori="konu_disi"),
    dict(id="k2-disi-dolar", soru="Bugün dolar kaç lira?", kategori="konu_disi"),
    dict(id="k2-disi-kod", soru="JavaScript'te bir dizi nasıl ters çevrilir?", kategori="konu_disi"),
    dict(id="k2-anlamsiz", soru="qwerty asdf 12345", kategori="anlamsiz"),
]

KONTROL2_SENARYOLAR = [
    # ------------------------------------------------------- takip sorusu
    dict(id="k2-takip-sinan", tip="takip", sorular=[
        dict(soru="Mimar Sinan ustalık eseri olarak hangi yapıyı göstermiştir?"),
        dict(soru="nerede bulunuyor?",
             belge="selcuklu-ve-osmanli-mimarisi.md",
             kanit="Edirne'deki Selimiye", anahtar=["Edirne"]),
    ]),
    dict(id="k2-takip-preveze", tip="takip", sorular=[
        dict(soru="Preveze Deniz Savaşı'nı kim kazanmıştır?"),
        dict(soru="hangi tarihte oldu?",
             belge="turk-denizciligi.md",
             kanit="Preveze Deniz Savaşı 28 Eylül 1538", anahtar=["28 Eylül 1538|1538"]),
    ]),
    dict(id="k2-takip-akif", tip="takip", sorular=[
        dict(soru="İstiklal Marşı'nın şairi kimdir?"),
        dict(soru="hangi dergide yazardı?",
             belge="milli-semboller.md",
             kanit="Sebilürreşad dergisinde", anahtar=["Sebilürreşad|Sırat-ı Müstakim"]),
    ]),
    dict(id="k2-takip-karahanli", tip="takip", sorular=[
        dict(soru="Karahanlı Devleti ne zaman kurulmuştur?"),
        dict(soru="ne zaman ikiye ayrıldı?",
             belge="turklerin-islamiyeti-kabulu.md",
             kanit="1042'de Doğu ve Batı Karahanlılar", anahtar=["1042"]),
    ]),

    # --------------------------------------- takip sorusu, cevabi belgede yok
    dict(id="k2-cevapsiz-takip-sinan", tip="takip_cevapsiz", sorular=[
        dict(soru="Mimar Sinan hangi padişahlar döneminde çalışmıştır?"),
        dict(soru="kaç yaşında öldü?"),
    ]),
    dict(id="k2-cevapsiz-takip-nevruz", tip="takip_cevapsiz", sorular=[
        dict(soru="Nevruz hangi tarihte kutlanır?"),
        dict(soru="kaç ülkede resmî tatildir?"),
    ]),
    dict(id="k2-cevapsiz-takip-kadi", tip="takip_cevapsiz", sorular=[
        dict(soru="Osmanlı'da kadı ne iş yapardı?"),
        dict(soru="kaç yıl görev yapardı?"),
    ]),

    # ----------------------------------------- konu degisimi, kisa yeni soru
    dict(id="k2-degisim-mehter", tip="konu_degisimi", sorular=[
        dict(soru="Bîrûnî hangi dili öğrenmiştir?"),
        dict(soru="Mehter nedir?",
             belge="ozan-asik-gelenegi.md",
             kanit="Osmanlı ordusunun askerî müzik topluluğudur", anahtar=["askerî müzik|bando"]),
    ]),
    dict(id="k2-degisim-balbal", tip="konu_degisimi", sorular=[
        dict(soru="Barbaros Hayreddin Paşa nerede doğmuştur?"),
        dict(soru="Balbal nedir?",
             belge="turk-mitolojisi-ve-gok-tanri.md",
             kanit="dikilen taşlara balbal denir", anahtar=["taş"]),
    ]),
    dict(id="k2-degisim-semeni", tip="konu_degisimi", sorular=[
        dict(soru="Mimar Sinan ne zaman ölmüştür?"),
        dict(soru="Semeni nedir?",
             belge="nevruz-ve-turk-bayramlari.md",
             kanit="semeni ya da sümelek", anahtar=["buğday"]),
    ]),

    # ------------------------------- onceki sorudan sonra konu disi soru
    dict(id="k2-disi-sonra-hava", tip="konu_disi_sonra", sorular=[
        dict(soru="Türk bayrağında hangi renkler vardır?"),
        dict(soru="Yarın hava nasıl olacak?"),
    ]),
    dict(id="k2-disi-sonra-tarif", tip="konu_disi_sonra", sorular=[
        dict(soru="Osmanlı'da kadı ne iş yapardı?"),
        dict(soru="Bana pizza tarifi verir misin?"),
    ]),
]
