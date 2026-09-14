# Değerlendirme: 2026-09-14 08:01 — hibrit-kapali

| Ayar | Değer |
|---|---|
| soru_seti | kontrol |
| sohbet_modeli | qwen2.5-7b-instruct-cuda-gpu |
| gomme_modeli | qwen3-embedding-0.6b-cuda-gpu |
| top_k | 3 |
| min_score | 0.33 |
| takip_farki | 0.2 |
| max_tokens | 350 |
| parca_sayisi | 86 |
| parcalama | paragraf + baslik yolu, ortusme yok |
| chunk_size | 1000 |
| sorgu_talimati | Soruyu cevaplayan paragrafı bul |
| arama | yalnız vektör |
| git | 64e3342 (kaydedilmemis degisiklik var) |
| set_parmak_izi | bcc0970ce7 |

## Özet

Puanlanan soru: 43 (27 cevaplanabilir, 16 cevaplanamaz). Senaryoların hazırlık soruları özete katılmaz.

| Ölçüt | Değer |
|---|---|
| Tam başarı (tüm puanlanan sorular) | 88.4% |
| Arama: doğru parça 1. sırada (hit@1) | 85.2% |
| Arama: doğru parça ilk 3'te (hit@3) | 88.9% |
| Arama: MRR (1 = hep 1. sırada) | 0.894 |
| Cevaplanabilir sorularda başarı | 88.9% |
| Yanlış red (cevap belgede varken) | 7.4% |
|   bunun eşikte olanı | 0.0% |
| Anahtar ifadelerin tamamı cevapta | 96.0% |
| Bilinen yanlışı içeren cevap | 0 adet |
| Kaynak satırı var | 100.0% |
| Kaynak doğru belge | 100.0% |
| Cevaplanamaz soruları reddetme | 87.5% |
|   bunun eşikte olanı | 0.0% |
| Red cevabına eklenmiş kaynak satırı | 0 adet |
| Süre ortalaması | 2.11 sn |
| Süre medyanı | 2.05 sn |
| En uzun süre | 3.09 sn |
| İlk token ortalaması (modele giden sorular) | 0.81 sn |
| Arama süresi ortalaması | 0.49 sn |

## Kategorilere göre

| Kategori | Soru | Başarılı | hit@1 | hit@3 | Yanlış red |
|---|---|---|---|---|---|
| normal | 15 | 14 | 14 | 15 | 0 |
| ozel_ad | 5 | 4 | 4 | 4 | 1 |
| yakin | 8 | 7 | - | - | - |
| takip | 4 | 4 | 4 | 4 | 0 |
| takip_cevapsiz | 6 | 5 | - | - | - |
| konu_degisimi | 3 | 2 | 1 | 1 | 1 |
| konu_disi_sonra | 2 | 2 | - | - | - |
| hazirlik (puanlanmaz) | 15 | - | - | - | - |

## Başarısız sorular

- **k-harf-sayisi** (normal) Latin harflerine dayalı yeni Türk alfabesinde kaç harf vardır?
  - Neden: eksik: yirmi dokuz|29
  - Cevap: Yeni Türk alfabesinde yirmi dokudan altı harf (ç, ğ, ı, ö, ş, ü) eklenmiştir. Dolayısıyla, toplamda yirmi dokudan altı harf yer almaktadır.  (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)
- **k-ulus** (ozel_ad) Ülüş nedir?
  - Neden: yanlış red (model); doğru parça ilk 3'te değil (sıra 4)
  - Cevap: Bu bilgi elimdeki dokümanlarda yok.
- **k-dogu-cephesi** (yakin) Kurtuluş Savaşı'nda Doğu Cephesi komutanı kimdi?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Mustafa Kemal Atatürk, Doğu C Cephesi'nde görevliyken Muş ve Bitlis'in geri alınmasında görev almış ve 1916 yılında general rütbesine yükseltmiştir. Bu bilgi, [mustafa-kemal-ataturk.md / parca 3] kısmından elde edilmiştir.  (Kaynak: mustafa-kemal-ataturk.md)
- **k-cevapsiz-uygur#2** (takip_cevapsiz) ne zaman yıkıldı?
  - Önceki soru: Uygur Kağanlığı hangi yıl kurulmuştur?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Osmanlı Devleti'nin yıkılışı 1922 yılında gerçekleşmiştir. Bu tarihte Türkiye Büyük Millet Meclisi VI. Mehmed Vahdettin padişahlığı kaldırarak, Osmanlı İmparatorluğu saltanatının sona erdi.  (Kaynak: osmanli-padisahlari.md)
- **k-degisim-otag#2** (konu_degisimi) Otağ nedir?
  - Önceki soru: Lozan Antlaşması ne zaman imzalanmıştır?
  - Neden: yanlış red (model); doğru parça ilk 3'te değil (sıra 5)
  - Cevap: Bu bilgi elimdeki dokümanlarda yok.

## Tüm sonuçlar

| id | Kategori | Sıra | En iyi skor | Eşikte red | Red | Anahtar | Kaynak | Süre | Sonuç |
|---|---|---|---|---|---|---|---|---|---|
| k-canakkale | normal | 1 | 0.626 |  |  | tam | doğru | 2.3 | OK |
| k-mete | normal | 1 | 0.578 |  |  | tam | doğru | 1.8 | OK |
| k-kutluk | normal | 1 | 0.677 |  |  | tam | doğru | 1.9 | OK |
| k-baba | normal | 1 | 0.747 |  |  | tam | doğru | 2.0 | OK |
| k-murad | normal | 1 | 0.49 |  |  | tam | doğru | 2.0 | OK |
| k-saltanat | normal | 1 | 0.622 |  |  | tam | doğru | 2.5 | OK |
| k-kinik | normal | 1 | 0.66 |  |  | tam | doğru | 1.9 | OK |
| k-malazgirt-onem | normal | 1 | 0.738 |  |  | tam | doğru | 3.1 | OK |
| k-akcura | normal | 1 | 0.793 |  |  | tam | doğru | 2.2 | OK |
| k-harf-sayisi | normal | 1 | 0.793 |  |  | eksik | doğru | 2.6 | HATA |
| k-millet-mektep | normal | 1 | 0.608 |  |  | tam | doğru | 2.1 | OK |
| k-bildiri | normal | 2 | 0.814 |  |  | tam | doğru | 2.6 | OK |
| k-veteriner | normal | 1 | 0.81 |  |  | tam | doğru | 2.0 | OK |
| k-kurt-neden | normal | 1 | 0.836 |  |  | tam | doğru | 2.9 | OK |
| k-ad-koyma | normal | 1 | 0.773 |  |  | tam | doğru | 2.6 | OK |
| k-ulus | ozel_ad | 4 | 0.469 |  | evet |  |  | 1.3 | HATA |
| k-toy | ozel_ad | 1 | 0.406 |  |  | tam | doğru | 2.6 | OK |
| k-manasci | ozel_ad | 1 | 0.534 |  |  | tam | doğru | 1.8 | OK |
| k-ortmece | ozel_ad | 1 | 0.424 |  |  | tam | doğru | 2.5 | OK |
| k-asena | ozel_ad | 1 | 0.433 |  |  | tam | doğru | 2.1 | OK |
| k-bumin-baba | yakin |  | 0.549 |  | evet |  |  | 1.5 | OK |
| k-edirne | yakin |  | 0.576 |  | evet |  |  | 1.7 | OK |
| k-alparslan-olum | yakin |  | 0.591 |  | evet |  |  | 2.0 | OK |
| k-gokalp-olum | yakin |  | 0.707 |  | evet |  |  | 2.0 | OK |
| k-macar-kral | yakin |  | 0.521 |  | evet |  |  | 1.5 | OK |
| k-thomsen-univ | yakin |  | 0.397 |  | evet |  |  | 2.3 | OK |
| k-korkut-hikaye | yakin |  | 0.728 |  | evet |  |  | 1.5 | OK |
| k-dogu-cephesi | yakin |  | 0.662 |  |  |  | var | 2.5 | HATA |
| k-takip-gokalp#1 | hazirlik |  | 0.77 |  |  |  | var | 1.8 | - |
| k-takip-gokalp#2 | takip | 1 | 0.809 |  |  | tam | doğru | 2.5 | OK |
| k-takip-korkut#1 | hazirlik |  | 0.776 |  |  |  | var | 1.8 | - |
| k-takip-korkut#2 | takip | 1 | 0.79 |  |  | tam | doğru | 2.3 | OK |
| k-takip-sam#1 | hazirlik |  | 0.706 |  |  |  | var | 1.9 | - |
| k-takip-sam#2 | takip | 1 | 0.76 |  |  | tam | doğru | 2.2 | OK |
| k-takip-konya#1 | hazirlik |  | 0.721 |  |  |  | var | 1.9 | - |
| k-takip-konya#2 | takip | 1 | 0.74 |  |  | tam | doğru | 2.4 | OK |
| k-cevapsiz-malazgirt#1 | hazirlik |  | 0.663 |  |  |  | var | 1.9 | - |
| k-cevapsiz-malazgirt#2 | takip_cevapsiz |  | 0.419 |  | evet |  |  | 2.4 | OK |
| k-cevapsiz-nutuk#1 | hazirlik |  | 0.503 |  |  |  | var | 2.1 | - |
| k-cevapsiz-nutuk#2 | takip_cevapsiz |  | 0.346 |  | evet |  |  | 1.8 | OK |
| k-cevapsiz-tdk#1 | hazirlik |  | 0.76 |  |  |  | var | 2.2 | - |
| k-cevapsiz-tdk#2 | takip_cevapsiz |  | 0.725 |  | evet |  |  | 2.1 | OK |
| k-cevapsiz-mohac#1 | hazirlik |  | 0.488 |  | evet |  |  | 1.6 | - |
| k-cevapsiz-mohac#2 | takip_cevapsiz |  | 0.424 |  | evet |  |  | 2.4 | OK |
| k-cevapsiz-baskent#1 | hazirlik |  | 0.766 |  |  |  | var | 1.7 | - |
| k-cevapsiz-baskent#2 | takip_cevapsiz |  | 0.722 |  | evet |  |  | 2.2 | OK |
| k-cevapsiz-uygur#1 | hazirlik |  | 0.66 |  |  |  | var | 1.8 | - |
| k-cevapsiz-uygur#2 | takip_cevapsiz |  | 0.435 |  |  |  | var | 2.7 | HATA |
| k-degisim-otag#1 | hazirlik |  | 0.485 |  |  |  | var | 1.9 | - |
| k-degisim-otag#2 | konu_degisimi | 5 | 0.45 |  | evet |  |  | 1.8 | HATA |
| k-degisim-okculuk#1 | hazirlik |  | 0.756 |  |  |  | var | 1.9 | - |
| k-degisim-okculuk#2 | konu_degisimi | 1 | 0.607 |  |  | tam | doğru | 2.8 | OK |
| k-degisim-tugrul#1 | hazirlik |  | 0.69 |  |  |  | var | 2.2 | - |
| k-degisim-tugrul#2 | konu_degisimi | 5 | 0.496 |  |  | tam | doğru | 2.8 | OK |
| k-disi-telefon#1 | hazirlik |  | 0.631 |  |  |  | var | 2.1 | - |
| k-disi-telefon#2 | konu_disi_sonra |  | 0.572 |  | evet |  |  | 2.0 | OK |
| k-disi-yagmur#1 | hazirlik |  | 0.75 |  |  |  | var | 1.7 | - |
| k-disi-yagmur#2 | konu_disi_sonra |  | 0.666 |  | evet |  |  | 1.9 | OK |

## Cevaplar (gözle kontrol için)

**k-canakkale** — Çanakkale'de İtilaf Devletleri neyi amaçlıyordu?
> İtilaf Devletleri, Çanakkale'de boğazı geçip İstanbul'a ulaşmayı ve Rusya'ya ulaşım hattı açmayı amaçlamıştır.  (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#0 0.626 | canakkale-ve-kurtulus-savasi.md#1 0.548 | canakkale-ve-kurtulus-savasi.md#3 0.503`

**k-mete** — Mete Han Çin kaynaklarında hangi adla anılır?
> Mete Han Çin kaynaklarında Modu Chanyu adıyla anılır.  (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#0 0.578 | turk-kulturunde-kurt.md#1 0.395 | turk-destanlari.md#3 0.384`

**k-kutluk** — İkinci Göktürk Devleti'ni kim, hangi yılda kurmuştur?
> İkinci Göktürk Devleti, İlteriş Kutluk Kağan tarafından 682'de kurulmuştur.  (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#1 0.677 | ilk-turk-devletleri.md#4 0.557 | turk-kulturunde-kurt.md#1 0.498`

**k-baba** — Mustafa Kemal'in babası kimdir, hangi işleri yapmıştır?
> Mustafa Kemal'in babası Ali Rıza Efendi'dir. Ali Rıza Efendi gümrük memurluğu ve kereste ticareti yapmıştır.  (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#0 0.747 | mustafa-kemal-ataturk.md#1 0.631 | mustafa-kemal-ataturk.md#6 0.586`

**k-murad** — I. Murad'ın hayatı nasıl sona ermiştir?
> I. Murad 1389'daki I. Kosova Savaşı'nı kazanmasından sonra savaş alanında öldürülmüştür.  (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#1 0.490 | osmanli-padisahlari.md#4 0.447 | mustafa-kemal-ataturk.md#6 0.445`

**k-saltanat** — Osmanlı saltanatı ne zaman ve kim tarafından kaldırılmıştır?
> Osmanlı saltanatı 1 Kasım 1922'de Türkiye Büyük Millet Meclisi tarafından kaldırılmıştır. Bu işlem, VI. Mehmed Vahdettin'in saltanatının sona ermesiyle birlikte gerçekleşmiştir.  (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#4 0.622 | osmanli-padisahlari.md#3 0.588 | osmanli-padisahlari.md#0 0.588`

**k-kinik** — Büyük Selçuklu hanedanı hangi Oğuz boyundan gelir?
> Büyük Selçuklu hanedanı Kınık boyundan gelir.  (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#0 0.660 | turk-destanlari.md#1 0.576 | osmanli-padisahlari.md#3 0.557`

**k-malazgirt-onem** — Malazgirt Savaşı Anadolu'nun tarihi açısından neden önemlidir?
> Malazgirt Savaşı Anadolu'nun tarihi açısından önemli çünkü savaşın ardından Bizans'ın Anadolu savunma düzeni çökmüş ve Türkmen boyları Anadolu içlerine doğru yerleşmeye başlamıştır. Bu süreç, Anadolu'nun Türkleşme sürecinin başlangıcı olarak kabul edilir ve Bizans İmparatorluğu'nun güçsüz hale gelmesine neden olmuştur.  (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#2 0.738 | selcuklular-ve-malazgirt.md#1 0.671 | selcuklular-ve-malazgirt.md#4 0.635`

**k-akcura** — Yusuf Akçura yazısında hangi siyaset biçimlerini karşılaştırmıştır?
> Yusuf Akçura yazısında Osmanlıcılık, İslamcılık ve Türkçülük olmak üzere üç siyaset biçimini karşılaştırmıştır.  (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#1 0.793 | ulku-ocaklari.md#3 0.510 | turk-milliyetciliginin-dogusu.md#0 0.472`

**k-harf-sayisi** — Latin harflerine dayalı yeni Türk alfabesinde kaç harf vardır?
> Yeni Türk alfabesinde yirmi dokudan altı harf (ç, ğ, ı, ö, ş, ü) eklenmiştir. Dolayısıyla, toplamda yirmi dokudan altı harf yer almaktadır.  (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#3 0.793 | turkcenin-tarihi-ve-alfabeleri.md#4 0.661 | turkcenin-tarihi-ve-alfabeleri.md#0 0.650`

**k-millet-mektep** — Yeni alfabeye geçişte halka okuma yazma öğretmek için hangi okullar açıldı?
> Millet Mektepleri açılmıştır, bu süreçte okuma yazma öğretimi yapılmıştır.  (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#3 0.608 | turkcenin-tarihi-ve-alfabeleri.md#4 0.541 | turkcenin-tarihi-ve-alfabeleri.md#1 0.536`

**k-bildiri** — Alparslan Türkeş 27 Mayıs 1960'ta hangi olayla tanınmıştır?
> Alparslan Türkeş, 27 Mayıs 1960 askerî müdahale sırasında yer alan otuz sekiz kişilik grubun içindeyken ve radyodan okuyulan darbe bildirisini radyodan okuyan kişi olarak tanınmıştır.  (Kaynak: milliyetci-hareketin-isimleri.md)

Getirilen: `milliyetci-hareketin-isimleri.md#6 0.814 | milliyetci-hareketin-isimleri.md#7 0.643 | milliyetci-hareketin-isimleri.md#10 0.634`

**k-veteriner** — Muhsin Yazıcıoğlu hangi fakülteden mezun olmuştur?
> Muhsin Yazıcıoğlu Ankara Üniversitesi Veteriner Fakültesi'nden mezun olmuştur.  (Kaynak: milliyetci-hareketin-isimleri.md)

Getirilen: `milliyetci-hareketin-isimleri.md#12 0.810 | milliyetci-hareketin-isimleri.md#15 0.612 | milliyetci-hareketin-isimleri.md#16 0.588`

**k-kurt-neden** — Türk kültüründe sembol olarak neden kurt seçilmiştir?
> Kurt, Türk kültüründe sembol olarak seçilmesinin nedenleri, bozkır topluluklarının dayanıklılığı ve evcilleşmemesi, ayrıca kurtun sürü hâlinde yaşaması ve dayanıklılığıdır. Ayrıca, kurt figürü, özellikle Göktürklerde siyasi sembolizme da yansımayıp, modern dönemde Türk milliyetçiliğinde de önemli bir görsel simge olmuştur.  (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#4 0.836 | turk-kulturunde-kurt.md#3 0.806 | turk-kulturunde-kurt.md#0 0.786`

**k-ad-koyma** — Dede Korkut hikâyelerindeki ad koyma geleneği nasıldır?
> Bir gencin yiğitlik gösterdiği sonra ad alması Dede Korkut hikâyelerinde ad koyma geleneğinin en bilinen örneğidir. Bu geleneğe göre, sadece yiğitlik gösteren gençler adlar alabilirler.  (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.773 | turk-kulturunde-at.md#4 0.617 | turk-kulturunde-kurt.md#6 0.577`

**k-ulus** — Ülüş nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-kulturunde-at.md#2 0.469 | ulku-ocaklari.md#0 0.460 | ulku-ocaklari.md#4 0.419`

**k-toy** — Toy nedir?
> Toy, devletin önemli kararlarının alındığı meclisdir. Kurultay同类文档中的“Toy”是指“库尔特”的旧土耳其语名称，但在给定的文档片段中，“Toy”指的是古代土耳其社会中用于做出重要决策的会议或议会。因此，直接回答问题：  库尔特是古代土耳其社会中用于做出重要决策的会议或议会。 （来源：turk-devlet-gelenegi.md）  (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#2 0.406 | turk-kulturunde-at.md#0 0.363 | turk-devlet-gelenegi.md#1 0.349`

**k-manasci** — Manasçı kimdir?
> Manasçı, sözlü olarak Manas Destanı anlatarak kuşaktan kuşağa aktarılan anlatıcılar anlamına gelir.  (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#3 0.534 | mustafa-kemal-ataturk.md#0 0.326 | milliyetci-hareketin-isimleri.md#12 0.323`

**k-ortmece** — Örtmece nedir?
> Örtmece, korkulan ya da saygı duyulan bir varlığın gerçek adını söylemekten kaçınılarak, başka bir daha az korkunç veya saygıdeğer bir sözcük kullanmaya başvurmak anlamına gelir. Bu yöntem, kurt gibi bazı hayvan isimlerinde görülebilir.  (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#6 0.424 | turkcenin-tarihi-ve-alfabeleri.md#0 0.368 | turk-kulturunde-at.md#3 0.367`

**k-asena** — Asena nedir?
> Asena, "Aşina"nın Türkçe çevirisi olarak yaygın olarak kullanıldığı modern bir okunuşudur. Bu terim, Türk kültüründe Kurt hanedanının kökenini anlatan anlatımda kullanılmaktadır.  (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#1 0.433 | milliyetci-hareketin-isimleri.md#20 0.421 | turk-kulturunde-at.md#3 0.359`

**k-bumin-baba** — Bumin Kağan'ın babasının adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-destanlari.md#1 0.549 | mustafa-kemal-ataturk.md#0 0.458 | milliyetci-hareketin-isimleri.md#19 0.437`

**k-edirne** — Osmanlı başkenti Edirne'ye ne zaman taşınmıştır?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-padisahlari.md#0 0.576 | osmanli-padisahlari.md#2 0.544 | osmanli-padisahlari.md#1 0.543`

**k-alparslan-olum** — Sultan Alparslan hangi yıl ölmüştür?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `milliyetci-hareketin-isimleri.md#6 0.591 | selcuklular-ve-malazgirt.md#1 0.541 | osmanli-padisahlari.md#4 0.541`

**k-gokalp-olum** — Ziya Gökalp hangi şehirde vefat etmiştir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-milliyetciliginin-dogusu.md#2 0.707 | milliyetci-hareketin-isimleri.md#15 0.547 | mustafa-kemal-ataturk.md#6 0.499`

**k-macar-kral** — Mohaç Savaşı'nda yenilen Macar kralının adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-padisahlari.md#4 0.521 | selcuklular-ve-malazgirt.md#4 0.486 | selcuklular-ve-malazgirt.md#1 0.469`

**k-thomsen-univ** — Vilhelm Thomsen hangi üniversitede çalışıyordu?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `ilk-turk-devletleri.md#3 0.397 | mustafa-kemal-ataturk.md#1 0.386 | mustafa-kemal-ataturk.md#5 0.321`

**k-korkut-hikaye** — Dede Korkut Kitabı'ndaki ilk hikâyenin adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-destanlari.md#4 0.728 | turk-kulturunde-at.md#4 0.558 | turk-kulturunde-kurt.md#2 0.500`

**k-dogu-cephesi** — Kurtuluş Savaşı'nda Doğu Cephesi komutanı kimdi?
> Mustafa Kemal Atatürk, Doğu C Cephesi'nde görevliyken Muş ve Bitlis'in geri alınmasında görev almış ve 1916 yılında general rütbesine yükseltmiştir. Bu bilgi, [mustafa-kemal-ataturk.md / parca 3] kısmından elde edilmiştir.  (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#3 0.662 | canakkale-ve-kurtulus-savasi.md#1 0.552 | canakkale-ve-kurtulus-savasi.md#3 0.528`

**k-takip-gokalp#1** — Ziya Gökalp nerede doğmuştur?
> Ziya Gökalp, 1876 yılında Diyarbakır şehirinde doğmuştur.  (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#2 0.770 | milliyetci-hareketin-isimleri.md#12 0.499 | milliyetci-hareketin-isimleri.md#17 0.476`

**k-takip-gokalp#2** — hangi formülü savunmuştur?  
_Önceki soru: Ziya Gökalp nerede doğmuştur?_
> Gökalp, "Türkleşmek, İslamlaşmak, Muasırlaşmak" formülünü savunmuştur.  (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#2 0.809 | turk-milliyetciliginin-dogusu.md#3 0.507 | milliyetci-hareketin-isimleri.md#15 0.485`

**k-takip-korkut#1** — Dede Korkut Kitabı kaç hikâyeden oluşur?
> Dede Korkut Kitabı, on iki hikâyeden oluşur.  (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.776 | turk-kulturunde-at.md#4 0.575 | turk-kulturunde-kurt.md#2 0.503`

**k-takip-korkut#2** — yazmaları nerede bulunuyor?  
_Önceki soru: Dede Korkut Kitabı kaç hikâyeden oluşur?_
> Dresden ve Vatikan'da bulunan yazmalar Dede Korkut Kitabı'nın esas kaynaklarıdır.  (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.790 | turk-kulturunde-at.md#4 0.583 | turk-kulturunde-kurt.md#2 0.508`

**k-takip-sam#1** — Mustafa Kemal Harp Akademisi'ni hangi yıl bitirmiştir?
> Mustafa Kemal Atatürk, Harp Akademisi'ni 1905'te bitirmiştir.  (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#1 0.706 | mustafa-kemal-ataturk.md#6 0.599 | mustafa-kemal-ataturk.md#0 0.549`

**k-takip-sam#2** — ilk görev yeri neresiydi?  
_Önceki soru: Mustafa Kemal Harp Akademisi'ni hangi yıl bitirmiştir?_
> Mustafa Kemal Atatürk'nün ilk görev yeri Şam'daydı.  (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#1 0.760 | mustafa-kemal-ataturk.md#6 0.594 | mustafa-kemal-ataturk.md#3 0.559`

**k-takip-konya#1** — Anadolu Selçuklu Devleti'nin ilk merkezi neresiydi?
> Anadolu Selçuklu Devleti'nin ilk merkezi İznik'teydi.  (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#3 0.721 | selcuklular-ve-malazgirt.md#2 0.627 | selcuklular-ve-malazgirt.md#4 0.602`

**k-takip-konya#2** — başkenti daha sonra nereye taşındı?  
_Önceki soru: Anadolu Selçuklu Devleti'nin ilk merkezi neresiydi?_
> Anadolu Selçuklu Devleti başkentini daha sonra Konya'ya taşımıştır.  (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#3 0.740 | selcuklular-ve-malazgirt.md#2 0.625 | selcuklular-ve-malazgirt.md#4 0.607`

**k-cevapsiz-malazgirt#1** — Malazgirt Savaşı ne zaman yapılmıştır?
> Malazgirt Savaavaşı 26 Ağustos 1071'de yapılmıştır.  (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.663 | selcuklular-ve-malazgirt.md#2 0.660 | selcuklular-ve-malazgirt.md#0 0.634`

**k-cevapsiz-malazgirt#2** — savaşta kaç kişi öldü?  
_Önceki soru: Malazgirt Savaşı ne zaman yapılmıştır?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `canakkale-ve-kurtulus-savasi.md#0 0.419 | milliyetci-hareketin-isimleri.md#15 0.386 | selcuklular-ve-malazgirt.md#1 0.381`

**k-cevapsiz-nutuk#1** — Nutuk ne zaman okunmuştur?
> Mustafa Kemal Atatürk, 15-20 Ekim 1927 tarihleri arasında Cumhuriyet Halk Partisi kongresinde Nutuk adlı konuşmasını okumuştur.  (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#5 0.503 | ilk-turk-devletleri.md#3 0.384 | ulku-ocaklari.md#0 0.368`

**k-cevapsiz-nutuk#2** — kaç sayfadır?  
_Önceki soru: Nutuk ne zaman okunmuştur?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-destanlari.md#3 0.346 | turkcenin-tarihi-ve-alfabeleri.md#0 0.335 | turk-destanlari.md#1 0.320`

**k-cevapsiz-tdk#1** — Türk Dil Kurumu ne zaman kurulmuştur?
> Türk Dil Kurumu, 12 Temmuz 1932'de kurulan Türk Dili Tetkik Cemiyeti olarak kurulmuştur ve bugün hala faaliyet göstermektedir.  (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.760 | turkcenin-tarihi-ve-alfabeleri.md#4 0.760 | turkcenin-tarihi-ve-alfabeleri.md#3 0.626`

**k-cevapsiz-tdk#2** — ilk başkanı kimdi?  
_Önceki soru: Türk Dil Kurumu ne zaman kurulmuştur?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#4 0.725 | turk-milliyetciliginin-dogusu.md#4 0.703 | ilk-turk-devletleri.md#1 0.621`

**k-cevapsiz-mohac#1** — Mohaç Savaşı hangi yıl yapılmıştır?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `selcuklular-ve-malazgirt.md#4 0.488 | selcuklular-ve-malazgirt.md#0 0.454 | selcuklular-ve-malazgirt.md#1 0.452`

**k-cevapsiz-mohac#2** — karşı taraftaki kralın adı neydi?  
_Önceki soru: Mohaç Savaşı hangi yıl yapılmıştır?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-padisahlari.md#1 0.424 | turk-devlet-gelenegi.md#0 0.415 | osmanli-padisahlari.md#4 0.410`

**k-cevapsiz-baskent#1** — Göktürk Devleti ne zaman kurulmuştur?
> Göktürk Devleti 552 yılında kurulmuştur.  (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#1 0.766 | ilk-turk-devletleri.md#4 0.670 | turk-milliyetciliginin-dogusu.md#4 0.602`

**k-cevapsiz-baskent#2** — başkenti neresiydi?  
_Önceki soru: Göktürk Devleti ne zaman kurulmuştur?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `ilk-turk-devletleri.md#1 0.722 | ilk-turk-devletleri.md#4 0.639 | turk-milliyetciliginin-dogusu.md#4 0.573`

**k-cevapsiz-uygur#1** — Uygur Kağanlığı hangi yıl kurulmuştur?
> Uygur Kağanlığı 744'te kurulmuştur.  (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#4 0.660 | turkcenin-tarihi-ve-alfabeleri.md#1 0.558 | ulku-ocaklari.md#0 0.549`

**k-cevapsiz-uygur#2** — ne zaman yıkıldı?  
_Önceki soru: Uygur Kağanlığı hangi yıl kurulmuştur?_
> Osmanlı Devleti'nin yıkılışı 1922 yılında gerçekleşmiştir. Bu tarihte Türkiye Büyük Millet Meclisi VI. Mehmed Vahdettin padişahlığı kaldırarak, Osmanlı İmparatorluğu saltanatının sona erdi.  (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#4 0.435 | osmanli-padisahlari.md#0 0.403 | selcuklular-ve-malazgirt.md#4 0.398`

**k-degisim-otag#1** — Lozan Antlaşması ne zaman imzalanmıştır?
> Lozan Antlaşması 24 Temmuz 1923'te imzalanmıştır.  (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#4 0.485 | canakkale-ve-kurtulus-savasi.md#2 0.391 | osmanli-padisahlari.md#0 0.382`

**k-degisim-otag#2** — Otağ nedir?  
_Önceki soru: Lozan Antlaşması ne zaman imzalanmıştır?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-destanlari.md#1 0.450 | turk-kulturunde-at.md#0 0.425 | turk-kulturunde-at.md#1 0.409`

**k-degisim-okculuk#1** — Orhun Yazıtları kimler adına dikilmiştir?
> Orhun Yazıtları, Tonyukuk, Kül Tigin ve Bilge Kağan adına dikilmiştir.  (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#2 0.756 | turkcenin-tarihi-ve-alfabeleri.md#0 0.613 | osmanli-padisahlari.md#1 0.491`

**k-degisim-okculuk#2** — Atlı okçuluk nedir?  
_Önceki soru: Orhun Yazıtları kimler adına dikilmiştir?_
> Atlı okçuluk, atlı askerlerin yoldaşlarının dörtnala hareket ederken ok atmayı yaptığı bir savaş teknikidir. Bu yöntem, Türk ordularında önemli bir avantaj sağlamış ve ağır piyade gücüne karşı hareket özgürlüğü kazandırmıştır.  (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#1 0.607 | turk-kulturunde-at.md#0 0.505 | turk-kulturunde-at.md#4 0.502`

**k-degisim-tugrul#1** — Yusuf Akçura'nın yazısı nerede yayımlanmıştır?
> Yusuf Akçura'nın "Üç Tarz-ı Siyaset" başlıklı yazısı 1904'te Kahire'de yayımlanmıştır.  (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#1 0.690 | turk-milliyetciliginin-dogusu.md#4 0.436 | ulku-ocaklari.md#0 0.406`

**k-degisim-tugrul#2** — Tuğrul Bey kimdir?  
_Önceki soru: Yusuf Akçura'nın yazısı nerede yayımlanmıştır?_
> Tuğrul Bey, Sultan Alparslan'nın babasıdır. Kuruluş dönemi Selçuklu hanlarının başında bulunan Tuğrul Bey, Anadolu'ya yöneldiği akınlar ve toprak kazanmalarıyla tanınır.  (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.496 | turk-devlet-gelenegi.md#4 0.490 | turk-destanlari.md#1 0.473`

**k-disi-telefon#1** — Kurultayda hangi kararlar alınırdı?
> Kurultayda savaş, barış ve hükümdar seçimi gibi konular görüşülürdü ve kararlar tartışılarak alındı.  (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#2 0.631 | turk-kulturunde-kurt.md#2 0.570 | turk-kulturunde-kurt.md#4 0.536`

**k-disi-telefon#2** — En iyi akıllı telefon hangisidir?  
_Önceki soru: Kurultayda hangi kararlar alınırdı?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-devlet-gelenegi.md#2 0.572 | turk-kulturunde-kurt.md#2 0.494 | turk-kulturunde-kurt.md#6 0.493`

**k-disi-yagmur#1** — Türk Ocağı ne zaman kurulmuştur?
> Türk Ocağı 25 Mart 1912'de kurulmuştur.  (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.750 | ulku-ocaklari.md#0 0.669 | ulku-ocaklari.md#2 0.664`

**k-disi-yagmur#2** — Yarın İstanbul'da yağmur yağacak mı?  
_Önceki soru: Türk Ocağı ne zaman kurulmuştur?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.666 | ulku-ocaklari.md#0 0.632 | ulku-ocaklari.md#2 0.624`

