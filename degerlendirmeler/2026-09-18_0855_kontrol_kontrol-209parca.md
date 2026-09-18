# Değerlendirme: 2026-09-18 08:55 — kontrol-209parca

| Ayar | Değer |
|---|---|
| soru_seti | kontrol |
| sohbet_modeli | qwen2.5-7b-instruct-cuda-gpu |
| gomme_modeli | qwen3-embedding-0.6b-cuda-gpu |
| top_k | 8 |
| min_score | 0.33 |
| takip_farki | 0.2 |
| max_tokens | 600 |
| parca_sayisi | 209 |
| parcalama | paragraf + baslik yolu, ortusme yok |
| chunk_size | 1000 |
| sorgu_talimati | Soruyu cevaplayan paragrafı bul |
| arama | yalnız vektör |
| cevap_dogrulama | kapalı |
| git | 9e60ec8 (kaydedilmemis degisiklik var) |
| set_parmak_izi | 48c99f2867 |

## Özet

Puanlanan soru: 41 (25 cevaplanabilir, 16 cevaplanamaz). Senaryoların hazırlık soruları özete katılmaz.

| Ölçüt | Değer |
|---|---|
| Tam başarı (tüm puanlanan sorular) | 78.0% |
| Arama: doğru parça 1. sırada (hit@1) | 80.0% |
| Arama: doğru parça ilk 3'te (hit@3) | 88.0% |
| Arama: MRR (1 = hep 1. sırada) | 0.844 |
| Cevaplanabilir sorularda başarı | 76.0% |
| Yanlış red (cevap belgede varken) | 4.0% |
|   bunun eşikte olanı | 0.0% |
| Anahtar ifadelerin tamamı cevapta | 91.7% |
| Bilinen yanlışı içeren cevap | 0 adet |
| Kaynak satırı var | 100.0% |
| Kaynak doğru belge | 79.2% |
| Cevaplanamaz soruları reddetme | 81.2% |
|   bunun eşikte olanı | 0.0% |
| Red cevabına eklenmiş kaynak satırı | 0 adet |
| Doğrulamada reddedilen cevaplanabilir | 0 adet |
| Doğrulamada reddedilen cevaplanamaz | 0 adet |
| Türkçe olmayan yazı kalan cevap | 0 adet |
| Türkçe olmayan yazı kesilen cevap | 0 adet |
| Süre ortalaması | 2.9 sn |
| Süre medyanı | 2.39 sn |
| En uzun süre | 7.25 sn |
| İlk token ortalaması (modele giden sorular) | 1.51 sn |
| Arama süresi ortalaması | 0.479 sn |

## Kategorilere göre

| Kategori | Soru | Başarılı | hit@1 | hit@3 | Yanlış red |
|---|---|---|---|---|---|
| normal | 13 | 12 | 12 | 13 | 0 |
| ozel_ad | 5 | 3 | 4 | 4 | 0 |
| yakin | 8 | 6 | - | - | - |
| takip | 4 | 3 | 3 | 4 | 0 |
| takip_cevapsiz | 6 | 5 | - | - | - |
| konu_degisimi | 3 | 1 | 1 | 1 | 1 |
| konu_disi_sonra | 2 | 2 | - | - | - |
| hazirlik (puanlanmaz) | 15 | - | - | - | - |

## Başarısız sorular

- **k-ad-koyma** (normal) Dede Korkut hikâyelerindeki ad koyma geleneği nasıldır?
  - Neden: yanlış kaynak: ozan-asik-gelenegi.md
  - Cevap: Dede Korkut hikâyelerindeki ad koyma geleneği, bir gencin yiğitlik gösterdiği zaman ad alması şeklinde öne çıkmaktadır. Bu geleneğe göre, sadece yiğitlik gösteren ve başarıya ulaşan gençler adlar alabilirler. Bu ad koyma süreci, genellikle Dede Korkut tarafından doneklerle ve kopuzuyla gerçekleştirilir. Dede Korkut, gençlere ad vererek onlara bilgi ve bilgelik kazandırırken, aynı zamanda topluluğun hafızası ve bilgesi olarak da işlev görür. (Kaynak: ozan-asik-gelenegi.md)
- **k-ulus** (ozel_ad) Ülüş nedir?
  - Neden: eksik: ganimet|gelir; yanlış kaynak: turk-kulturunde-at.md, oguz-boylari-ve-turk-boy-yapisi.md; doğru parça ilk 3'te değil (sıra 7)
  - Cevap: Ülüş, Türk toplumunda temel bir siyasi ve sosyal yapıdır. Eski Türk toplumu, birbirinin içinden çıkan basamaklı bir yapıya göre örgütlenmiştir ve bu yapıda en küçük birim ailedir (oğuş). Akraba ailelerin birleşmesiyle urug, urugların birleşmesiyle boy, boyların birleşmesiyle budun ve budunun birleşmesiyle il veya el oluşur. Bu yapıda ülüş, boy veya budunun bir parçası olarak görülür. (Kaynak: turk-kulturunde-at.md, oguz-boylari-ve-turk-boy-yapisi.md)
- **k-manasci** (ozel_ad) Manasçı kimdir?
  - Neden: yanlış kaynak: ozan-asik-gelenegi.md
  - Cevap: Manasçı, Kırgızlarda destan anlatıcısını ifade eder ve Manas Destanı'nı ezberden ve doğaçlama eklemelerle anlatır. Manasçılar, yarım milyon dizeye yaklaşan Manas Destanı'nı yazıya bakmadan anlatırlar. Bu gelenek, usta-çırak ilişkisiyle aktarılmış ve 2013'te UNESCO listesine alınmıştır. (Kaynak: ozan-asik-gelenegi.md)
- **k-edirne** (yakin) Osmanlı başkenti Edirne'ye ne zaman taşınmıştır?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Osmanlı başkenti Edirne'ye taşınmasının tam tarihi belirsiz olarak verilmemiştir. Ancak, Koyunhisar Savaşı ile Bursa'nın 1302 yılında düşmesi ve 1326'da Orhan Gazi döneminde Bursa'nın alınması ve başkent olarak yapıldığı bilinmektedir. Edirne'nin başkent olarak tanınmasından önce Bursa'nın bu rolü olduğu düşünülür. (Kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md)
- **k-dogu-cephesi** (yakin) Kurtuluş Savaşı'nda Doğu Cephesi komutanı kimdi?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Kurtuluş Savaşı'nda Doğu Cephesi komutanı Mustafa Kemal'di. (Kaynak: canakkale-ve-kurtulus-savasi.md)
- **k-takip-konya#2** (takip) başkenti daha sonra nereye taşındı?
  - Önceki soru: Anadolu Selçuklu Devleti'nin ilk merkezi neresiydi?
  - Neden: yanlış kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md
  - Cevap: Beyliklerin başkenti Bursa'dan Konya'ya taşındı. (Kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md)
- **k-cevapsiz-uygur#2** (takip_cevapsiz) ne zaman yıkıldı?
  - Önceki soru: Uygur Kağanlığı hangi yıl kurulmuştur?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Saltanatın 1 Kasım 1922'de kaldırıldı. (Kaynak: cumhuriyet-inkilaplari.md)
- **k-degisim-otag#2** (konu_degisimi) Otağ nedir?
  - Önceki soru: Lozan Antlaşması ne zaman imzalanmıştır?
  - Neden: eksik: sembol; yanlış kaynak: bozkir-gocebe-yasami.md; doğru parça ilk 3'te değil (sıra 14)
  - Cevap: Otağ, Türk topluluklarında yurt veya kerege adlarıyla anılan sökülüp taşınabilen keçe çadırın isminin bir formudur. Bu yapı, iskeleti makas biçiminde açılıp kapanan kafes duvarlar ve çubuklardan oluşur ve tepedeki çember hem baca hem pencere görevi görürken dumanı dışarı verir. Üzeri keçeyle kaplanarak kışın soğuğu geçirmezken, yazın sıcağı geçirir. (Kaynak: bozkir-gocebe-yasami.md)
- **k-degisim-tugrul#2** (konu_degisimi) Tuğrul Bey kimdir?
  - Önceki soru: Yusuf Akçura'nın yazısı nerede yayımlanmıştır?
  - Neden: yanlış red (model); doğru parça ilk 3'te değil (sıra 19)
  - Cevap: Tuğrul Bey, Selçukluların kurucusu olarak anılır. Bağlamda belirtilmemiş, ancak Türk-İslam Dünyasında Bilim ve Türk Denizciliği metinlerinde de geçmemektedir. Bu bilgi elimdeki dokümanlarda yok.

## Tüm sonuçlar

| id | Kategori | Sıra | En iyi skor | Eşikte red | Red | Anahtar | Kaynak | Süre | Sonuç |
|---|---|---|---|---|---|---|---|---|---|
| k-canakkale | normal | 1 | 0.626 |  |  | tam | doğru | 2.3 | OK |
| k-mete | normal | 1 | 0.578 |  |  | tam | doğru | 1.4 | OK |
| k-kutluk | normal | 1 | 0.677 |  |  | tam | doğru | 2.1 | OK |
| k-baba | normal | 1 | 0.747 |  |  | tam | doğru | 2.1 | OK |
| k-murad | normal | 1 | 0.49 |  |  | tam | doğru | 2.5 | OK |
| k-saltanat | normal | 3 | 0.649 |  |  | tam | doğru | 3.3 | OK |
| k-kinik | normal | 1 | 0.66 |  |  | tam | doğru | 2.5 | OK |
| k-malazgirt-onem | normal | 1 | 0.738 |  |  | tam | doğru | 3.4 | OK |
| k-akcura | normal | 1 | 0.793 |  |  | tam | doğru | 2.3 | OK |
| k-harf-sayisi | normal | 1 | 0.793 |  |  | tam | doğru | 2.1 | OK |
| k-millet-mektep | normal | 1 | 0.608 |  |  | tam | doğru | 2.3 | OK |
| k-kurt-neden | normal | 1 | 0.836 |  |  | tam | doğru | 3.2 | OK |
| k-ad-koyma | normal | 1 | 0.773 |  |  | tam | yanlış | 4.4 | HATA |
| k-ulus | ozel_ad | 7 | 0.469 |  |  | eksik | yanlış | 4.0 | HATA |
| k-toy | ozel_ad | 1 | 0.406 |  |  | tam | doğru | 2.9 | OK |
| k-manasci | ozel_ad | 1 | 0.534 |  |  | tam | yanlış | 3.5 | HATA |
| k-ortmece | ozel_ad | 1 | 0.424 |  |  | tam | doğru | 3.4 | OK |
| k-asena | ozel_ad | 1 | 0.433 |  |  | tam | doğru | 2.4 | OK |
| k-bumin-baba | yakin |  | 0.549 |  | evet |  |  | 2.0 | OK |
| k-edirne | yakin |  | 0.594 |  |  |  | var | 4.0 | HATA |
| k-alparslan-olum | yakin |  | 0.558 |  | evet |  |  | 2.1 | OK |
| k-gokalp-olum | yakin |  | 0.707 |  | evet |  |  | 1.7 | OK |
| k-macar-kral | yakin |  | 0.521 |  | evet |  |  | 2.5 | OK |
| k-thomsen-univ | yakin |  | 0.397 |  | evet |  |  | 2.1 | OK |
| k-korkut-hikaye | yakin |  | 0.728 |  | evet |  |  | 1.9 | OK |
| k-dogu-cephesi | yakin |  | 0.662 |  |  |  | var | 2.5 | HATA |
| k-takip-gokalp#1 | hazirlik |  | 0.77 |  |  |  | var | 2.0 | - |
| k-takip-gokalp#2 | takip | 1 | 0.809 |  |  | tam | doğru | 2.4 | OK |
| k-takip-korkut#1 | hazirlik |  | 0.776 |  |  |  | var | 2.0 | - |
| k-takip-korkut#2 | takip | 1 | 0.79 |  |  | tam | doğru | 2.4 | OK |
| k-takip-sam#1 | hazirlik |  | 0.706 |  |  |  | var | 2.1 | - |
| k-takip-sam#2 | takip | 1 | 0.76 |  |  | tam | doğru | 2.3 | OK |
| k-takip-konya#1 | hazirlik |  | 0.721 |  |  |  | var | 2.5 | - |
| k-takip-konya#2 | takip | 2 | 0.55 |  |  | tam | yanlış | 4.7 | HATA |
| k-cevapsiz-malazgirt#1 | hazirlik |  | 0.663 |  |  |  | var | 2.1 | - |
| k-cevapsiz-malazgirt#2 | takip_cevapsiz |  | 0.44 |  | evet |  |  | 4.4 | OK |
| k-cevapsiz-nutuk#1 | hazirlik |  | 0.503 |  |  |  | var | 4.6 | - |
| k-cevapsiz-nutuk#2 | takip_cevapsiz |  | 0.384 |  | evet |  |  | 2.1 | OK |
| k-cevapsiz-tdk#1 | hazirlik |  | 0.76 |  |  |  | var | 2.7 | - |
| k-cevapsiz-tdk#2 | takip_cevapsiz |  | 0.725 |  | evet |  |  | 2.3 | OK |
| k-cevapsiz-mohac#1 | hazirlik |  | 0.488 |  |  |  | var | 2.2 | - |
| k-cevapsiz-mohac#2 | takip_cevapsiz |  | 0.426 |  | evet |  |  | 4.5 | OK |
| k-cevapsiz-baskent#1 | hazirlik |  | 0.766 |  |  |  | var | 2.2 | - |
| k-cevapsiz-baskent#2 | takip_cevapsiz |  | 0.567 |  | evet |  |  | 7.2 | OK |
| k-cevapsiz-uygur#1 | hazirlik |  | 0.66 |  |  |  | var | 2.1 | - |
| k-cevapsiz-uygur#2 | takip_cevapsiz |  | 0.45 |  |  |  | var | 4.3 | HATA |
| k-degisim-otag#1 | hazirlik |  | 0.492 |  |  |  | var | 4.4 | - |
| k-degisim-otag#2 | konu_degisimi | 14 | 0.461 |  |  | eksik | yanlış | 6.1 | HATA |
| k-degisim-okculuk#1 | hazirlik |  | 0.756 |  |  |  | var | 2.0 | - |
| k-degisim-okculuk#2 | konu_degisimi | 1 | 0.607 |  |  | tam | doğru | 3.7 | OK |
| k-degisim-tugrul#1 | hazirlik |  | 0.69 |  |  |  | var | 2.2 | - |
| k-degisim-tugrul#2 | konu_degisimi | 19 | 0.63 |  | evet |  |  | 5.0 | HATA |
| k-disi-telefon#1 | hazirlik |  | 0.631 |  |  |  | var | 2.4 | - |
| k-disi-telefon#2 | konu_disi_sonra |  | 0.572 |  | evet |  |  | 2.1 | OK |
| k-disi-yagmur#1 | hazirlik |  | 0.75 |  |  |  | var | 2.3 | - |
| k-disi-yagmur#2 | konu_disi_sonra |  | 0.666 |  | evet |  |  | 2.4 | OK |

## Cevaplar (gözle kontrol için)

**k-canakkale** — Çanakkale'de İtilaf Devletleri neyi amaçlıyordu?
> İtilaf Devletleri, Çanakkale'de boğazı geçip İstanbul'a ulaşmayı ve Rusya'ya ulaşım hattı açmayı amaçlamıştır. Bu operasyonlar, Birinci Dünya Savaşı sırasında önemli bir batış noktası olmuştur. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#0 0.626 | canakkale-ve-kurtulus-savasi.md#1 0.548 | turklerin-islamiyeti-kabulu.md#3 0.514 | osmanli-islahat-ve-mesrutiyet.md#10 0.504 | turklerin-islamiyeti-kabulu.md#2 0.497`

**k-mete** — Mete Han Çin kaynaklarında hangi adla anılır?
> Mete Han Çin kaynaklarında Modu Chanyu adıyla anılır. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#0 0.578 | ozan-asik-gelenegi.md#8 0.481`

**k-kutluk** — İkinci Göktürk Devleti'ni kim, hangi yılda kurmuştur?
> İkinci Göktürk Devleti'ni İlteriş Kutluk Kağan, 682'de kurmuştur. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#1 0.677 | ilk-turk-devletleri.md#4 0.557 | bozkir-gocebe-yasami.md#6 0.516 | bozkir-gocebe-yasami.md#7 0.502 | turklerin-islamiyeti-kabulu.md#3 0.499`

**k-baba** — Mustafa Kemal'in babası kimdir, hangi işleri yapmıştır?
> Mustafa Kemal'in babası Ali Rıza Efendi'dir ve gümrük memurluğu ve kereste ticareti yapmıştır. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#0 0.747 | mustafa-kemal-ataturk.md#1 0.631`

**k-murad** — I. Murad'ın hayatı nasıl sona ermiştir?
> I. Murad 1389'daki I. Kosova Savaşı'nı kazanmış ancak savaş alanında öldürülmüştür. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#1 0.490 | osmanli-islahat-ve-mesrutiyet.md#3 0.455 | turk-denizciligi.md#2 0.447 | osmanli-padisahlari.md#4 0.447 | mustafa-kemal-ataturk.md#6 0.445`

**k-saltanat** — Osmanlı saltanatı ne zaman ve kim tarafından kaldırılmıştır?
> Osmanlı saltanatı 1 Kasım 1922'de kaldırılmıştır. Bu tarihle birlikte Türkiye Büyük Millet Meclisi, saltanatın kaldırılmasına karar vermiştir. Cevabı veren kişi VI. Mehmed Vahdettin'dir; onun saltanatı deşife alınmıştır. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#0 0.649 | cumhuriyet-inkilaplari.md#1 0.640 | osmanli-padisahlari.md#4 0.622 | osmanli-islahat-ve-mesrutiyet.md#7 0.610 | osmanli-devlet-teskilati.md#5 0.603`

**k-kinik** — Büyük Selçuklu hanedanı hangi Oğuz boyundan gelir?
> Büyük Selçuklu hanedanı Kınık boyundan gelir. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#0 0.660 | oguz-boylari-ve-turk-boy-yapisi.md#6 0.619 | oguz-boylari-ve-turk-boy-yapisi.md#4 0.604 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#0 0.592 | turk-destanlari.md#1 0.576`

**k-malazgirt-onem** — Malazgirt Savaşı Anadolu'nun tarihi açısından neden önemlidir?
> Malazgirt Savaşı Anadolu'nun tarihi açısından önemlidir çünkü savaşın ardından Bizans'ın Anadolu savunma düzeni çökmüş ve Türkmen boyları Anadolu içlerine doğru yerleşmeye başlamıştır. Bu süreç, Anadolu'nun Türkleşme sürecinin başlangıcı olarak kabul edilir ve Bizans İmparatorluğu'nun Anadolu bölgelerindeki kontrolünün zayıflamasına neden olmuştur. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#2 0.738 | selcuklular-ve-malazgirt.md#1 0.671`

**k-akcura** — Yusuf Akçura yazısında hangi siyaset biçimlerini karşılaştırmıştır?
> Yusuf Akçura yazısında Osmanlıcılık, İslamcılık ve Türkçülük olmak üzere üç siyaset biçimini karşılaştırmıştır. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#1 0.793 | milli-semboller.md#4 0.491`

**k-harf-sayisi** — Latin harflerine dayalı yeni Türk alfabesinde kaç harf vardır?
> Yeni Türk alfabesinde yirmi dokuz harf vardır. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#3 0.793 | bugunku-turk-dunyasi.md#6 0.738 | turkcenin-tarihi-ve-alfabeleri.md#4 0.661`

**k-millet-mektep** — Yeni alfabeye geçişte halka okuma yazma öğretmek için hangi okullar açıldı?
> Millet Mektepleri açılmıştır. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#3 0.608 | cumhuriyet-inkilaplari.md#5 0.543 | turkcenin-tarihi-ve-alfabeleri.md#4 0.541 | bugunku-turk-dunyasi.md#6 0.534 | ilk-turk-devletleri.md#3 0.477`

**k-kurt-neden** — Türk kültüründe sembol olarak neden kurt seçilmiştir?
> Türk kültüründe kurt sembol olarak seçilmesinin nedeni, kurtun sürü hâlinde yaşaması, dayanıklılığı ve evcilleşmemesi ile bozkır topluluklarının kendilerini tanımlamak için hayvan sembolleri kullanımına sahip olmasıdır. Ayrıca, kurt figürü, özellikle Göktürklerde siyasi sembolizme de yansımanın yanı sıra, modern dönemde Türk milliyetçiliğinde de önemli bir görsel işaret haline gelmiştir. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#4 0.836 | turk-kulturunde-kurt.md#3 0.806`

**k-ad-koyma** — Dede Korkut hikâyelerindeki ad koyma geleneği nasıldır?
> Dede Korkut hikâyelerindeki ad koyma geleneği, bir gencin yiğitlik gösterdiği zaman ad alması şeklinde öne çıkmaktadır. Bu geleneğe göre, sadece yiğitlik gösteren ve başarıya ulaşan gençler adlar alabilirler. Bu ad koyma süreci, genellikle Dede Korkut tarafından doneklerle ve kopuzuyla gerçekleştirilir. Dede Korkut, gençlere ad vererek onlara bilgi ve bilgelik kazandırırken, aynı zamanda topluluğun hafızası ve bilgesi olarak da işlev görür. (Kaynak: ozan-asik-gelenegi.md)

Getirilen: `turk-destanlari.md#4 0.773 | ozan-asik-gelenegi.md#1 0.711 | turk-kulturunde-at.md#4 0.617 | turk-kulturunde-kurt.md#6 0.577 | turk-kulturunde-kurt.md#5 0.552`

**k-ulus** — Ülüş nedir?
> Ülüş, Türk toplumunda temel bir siyasi ve sosyal yapıdır. Eski Türk toplumu, birbirinin içinden çıkan basamaklı bir yapıya göre örgütlenmiştir ve bu yapıda en küçük birim ailedir (oğuş). Akraba ailelerin birleşmesiyle urug, urugların birleşmesiyle boy, boyların birleşmesiyle budun ve budunun birleşmesiyle il veya el oluşur. Bu yapıda ülüş, boy veya budunun bir parçası olarak görülür. (Kaynak: turk-kulturunde-at.md, oguz-boylari-ve-turk-boy-yapisi.md)

Getirilen: `turk-kulturunde-at.md#2 0.469 | oguz-boylari-ve-turk-boy-yapisi.md#0 0.462 | turk-mitolojisi-ve-gok-tanri.md#7 0.433 | ozan-asik-gelenegi.md#3 0.416 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#7 0.415`

**k-toy** — Toy nedir?
> Toy, devletin önemli kararlarının alındığı bir kurultaydır. Burada tartışılacak konular genellikle savaş, barış ve hükümdar seçimi gibi önemli materyaller olurken, kararlar boy beyleri ve hanedan üyeleri tarafından tartışılarak alınırdı. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#2 0.406 | turk-kulturunde-at.md#0 0.363 | turk-devlet-gelenegi.md#1 0.349 | turk-mitolojisi-ve-gok-tanri.md#0 0.341 | bugunku-turk-dunyasi.md#5 0.338`

**k-manasci** — Manasçı kimdir?
> Manasçı, Kırgızlarda destan anlatıcısını ifade eder ve Manas Destanı'nı ezberden ve doğaçlama eklemelerle anlatır. Manasçılar, yarım milyon dizeye yaklaşan Manas Destanı'nı yazıya bakmadan anlatırlar. Bu gelenek, usta-çırak ilişkisiyle aktarılmış ve 2013'te UNESCO listesine alınmıştır. (Kaynak: ozan-asik-gelenegi.md)

Getirilen: `turk-destanlari.md#3 0.534 | ozan-asik-gelenegi.md#2 0.524 | turk-mitolojisi-ve-gok-tanri.md#5 0.395 | selcuklu-ve-osmanli-mimarisi.md#5 0.391`

**k-ortmece** — Örtmece nedir?
> Örtmece, korkulan ya da saygı duyulan bir varlığın gerçek adını söylemekten kaçınılıp, başka bir sözcük kullanmaya başvurma tarzıdır. Bu yöntem, kurtçuk gibi zayıf ve korkunç görünen canlıların adı olarak daha güçlü ve onurlu görünen "kurt" sözcüğünü kullanmaya başlandığında ortaya çıkmıştır. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#6 0.424 | bozkir-gocebe-yasami.md#4 0.402 | bozkir-gocebe-yasami.md#0 0.378 | turkcenin-tarihi-ve-alfabeleri.md#0 0.368 | turk-kulturunde-at.md#3 0.367`

**k-asena** — Asena nedir?
> Asena, "Aşina"nın modern Türkçe okunuşudur ve Türk kültüründe Kurt hanedanının adı olarak kullanılmaktadır. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#1 0.433 | ozan-asik-gelenegi.md#3 0.426 | ozan-asik-gelenegi.md#0 0.390 | turk-kulturunde-at.md#3 0.359 | turk-kulturunde-at.md#0 0.354`

**k-bumin-baba** — Bumin Kağan'ın babasının adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-destanlari.md#1 0.549 | ozan-asik-gelenegi.md#0 0.479 | oguz-boylari-ve-turk-boy-yapisi.md#6 0.462 | mustafa-kemal-ataturk.md#0 0.458 | selcuklu-ve-osmanli-mimarisi.md#5 0.452`

**k-edirne** — Osmanlı başkenti Edirne'ye ne zaman taşınmıştır?
> Osmanlı başkenti Edirne'ye taşınmasının tam tarihi belirsiz olarak verilmemiştir. Ancak, Koyunhisar Savaşı ile Bursa'nın 1302 yılında düşmesi ve 1326'da Orhan Gazi döneminde Bursa'nın alınması ve başkent olarak yapıldığı bilinmektedir. Edirne'nin başkent olarak tanınmasından önce Bursa'nın bu rolü olduğu düşünülür. (Kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md)

Getirilen: `anadolu-beylikleri-ve-osmanlinin-kurulusu.md#8 0.594 | osmanli-padisahlari.md#0 0.576 | osmanli-islahat-ve-mesrutiyet.md#6 0.544 | osmanli-padisahlari.md#2 0.544 | osmanli-islahat-ve-mesrutiyet.md#0 0.534`

**k-alparslan-olum** — Sultan Alparslan hangi yıl ölmüştür?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#0 0.558 | selcuklular-ve-malazgirt.md#1 0.541 | osmanli-padisahlari.md#4 0.541 | osmanli-padisahlari.md#0 0.535 | osmanli-islahat-ve-mesrutiyet.md#3 0.496`

**k-gokalp-olum** — Ziya Gökalp hangi şehirde vefat etmiştir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-milliyetciliginin-dogusu.md#2 0.707 | bozkir-gocebe-yasami.md#8 0.522 | mustafa-kemal-ataturk.md#6 0.499`

**k-macar-kral** — Mohaç Savaşı'nda yenilen Macar kralının adı nedir?
> Mohaç Savaşı hakkında metinde Macar kralının adı belirtilmemiş. Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-padisahlari.md#4 0.521 | selcuklular-ve-malazgirt.md#4 0.486 | selcuklular-ve-malazgirt.md#1 0.469 | osmanli-padisahlari.md#1 0.440 | osmanli-islahat-ve-mesrutiyet.md#3 0.421`

**k-thomsen-univ** — Vilhelm Thomsen hangi üniversitede çalışıyordu?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `ilk-turk-devletleri.md#3 0.397 | mustafa-kemal-ataturk.md#1 0.386 | turk-islam-dunyasinda-bilim.md#4 0.362 | turk-islam-dunyasinda-bilim.md#0 0.361 | mustafa-kemal-ataturk.md#5 0.321`

**k-korkut-hikaye** — Dede Korkut Kitabı'ndaki ilk hikâyenin adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-destanlari.md#4 0.728 | ozan-asik-gelenegi.md#1 0.599 | turk-kulturunde-at.md#4 0.558 | ilk-turk-islam-eserleri.md#0 0.513`

**k-dogu-cephesi** — Kurtuluş Savaşı'nda Doğu Cephesi komutanı kimdi?
> Kurtuluş Savaşı'nda Doğu Cephesi komutanı Mustafa Kemal'di. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `mustafa-kemal-ataturk.md#3 0.662 | canakkale-ve-kurtulus-savasi.md#1 0.552 | canakkale-ve-kurtulus-savasi.md#3 0.528 | turk-denizciligi.md#3 0.516 | oguz-boylari-ve-turk-boy-yapisi.md#6 0.495`

**k-takip-gokalp#1** — Ziya Gökalp nerede doğmuştur?
> Ziya Gökalp, 1876 yılında Diyarbakır'da doğmuştur. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#2 0.770 | bozkir-gocebe-yasami.md#8 0.490`

**k-takip-gokalp#2** — hangi formülü savunmuştur?  
_Önceki soru: Ziya Gökalp nerede doğmuştur?_
> Ziya Gökalp "Türkleşmek, İslamlaşmak, Muasırlaşmak" formülünü savunmuştur. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#2 0.809 | bozkir-gocebe-yasami.md#7 0.518`

**k-takip-korkut#1** — Dede Korkut Kitabı kaç hikâyeden oluşur?
> Dede Korkut Kitabı, on iki hikâyeden oluşur. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.776 | ozan-asik-gelenegi.md#1 0.612 | turk-kulturunde-at.md#4 0.575`

**k-takip-korkut#2** — yazmaları nerede bulunuyor?  
_Önceki soru: Dede Korkut Kitabı kaç hikâyeden oluşur?_
> Dresden ve Vatikan'da bulunan yazmalar Dede Korkut Kitabı'nı oluşturur. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.790 | ozan-asik-gelenegi.md#1 0.599 | turk-kulturunde-at.md#4 0.583`

**k-takip-sam#1** — Mustafa Kemal Harp Akademisi'ni hangi yıl bitirmiştir?
> Mustafa Kemal Atatürk Harp Akademisi'ni 1905'te bitirmiştir. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#1 0.706 | mustafa-kemal-ataturk.md#6 0.599 | cumhuriyet-inkilaplari.md#5 0.496`

**k-takip-sam#2** — ilk görev yeri neresiydi?  
_Önceki soru: Mustafa Kemal Harp Akademisi'ni hangi yıl bitirmiştir?_
> İlk görev yeri Şam'daki 5. Ordu olmuştur. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#1 0.760 | mustafa-kemal-ataturk.md#6 0.594`

**k-takip-konya#1** — Anadolu Selçuklu Devleti'nin ilk merkezi neresiydi?
> Anadolu Selçuklu Devleti'nin ilk merkezi İznik'te yer almıştır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#3 0.721 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#8 0.688 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#0 0.666 | selcuklular-ve-malazgirt.md#2 0.627 | turk-denizciligi.md#0 0.616`

**k-takip-konya#2** — başkenti daha sonra nereye taşındı?  
_Önceki soru: Anadolu Selçuklu Devleti'nin ilk merkezi neresiydi?_
> Beyliklerin başkenti Bursa'dan Konya'ya taşındı. (Kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md)

Getirilen: `anadolu-beylikleri-ve-osmanlinin-kurulusu.md#8 0.550 | selcuklular-ve-malazgirt.md#3 0.481 | oguz-boylari-ve-turk-boy-yapisi.md#7 0.470 | osmanli-islahat-ve-mesrutiyet.md#6 0.467 | osmanli-padisahlari.md#3 0.460`

**k-cevapsiz-malazgirt#1** — Malazgirt Savaşı ne zaman yapılmıştır?
> Malazgirt Savaşı 26 Ağustos 1071'de yapılmıştır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.663 | selcuklular-ve-malazgirt.md#2 0.660 | turklerin-islamiyeti-kabulu.md#1 0.486`

**k-cevapsiz-malazgirt#2** — savaşta kaç kişi öldü?  
_Önceki soru: Malazgirt Savaşı ne zaman yapılmıştır?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turklerin-islamiyeti-kabulu.md#1 0.440 | canakkale-ve-kurtulus-savasi.md#0 0.419 | turk-denizciligi.md#3 0.382 | selcuklular-ve-malazgirt.md#1 0.381 | selcuklular-ve-malazgirt.md#2 0.375`

**k-cevapsiz-nutuk#1** — Nutuk ne zaman okunmuştur?
> Mustafa Kemal Atatürk, 15-20 Ekim 1927 tarihleri arasında Cumhuriyet Halk Partisi kongresinde Nutuk adlı konuşmasını okumuştur. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#5 0.503 | ilk-turk-islam-eserleri.md#1 0.456 | milli-semboller.md#10 0.446 | ilk-turk-islam-eserleri.md#2 0.428 | nevruz-ve-turk-bayramlari.md#0 0.416`

**k-cevapsiz-nutuk#2** — kaç sayfadır?  
_Önceki soru: Nutuk ne zaman okunmuştur?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-mitolojisi-ve-gok-tanri.md#6 0.384 | ilk-turk-islam-eserleri.md#1 0.361 | ilk-turk-islam-eserleri.md#2 0.355 | turk-destanlari.md#3 0.346`

**k-cevapsiz-tdk#1** — Türk Dil Kurumu ne zaman kurulmuştur?
> Türk Dil Kurumu, 12 Temmuz 1932'de kurulan Türk Dili Tetkik Cemiyeti olarak başlamış ve bugüne kadar faaliyet göstermektedir. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.760 | turkcenin-tarihi-ve-alfabeleri.md#4 0.760 | bugunku-turk-dunyasi.md#4 0.671 | bugunku-turk-dunyasi.md#5 0.645 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#4 0.637`

**k-cevapsiz-tdk#2** — ilk başkanı kimdi?  
_Önceki soru: Türk Dil Kurumu ne zaman kurulmuştur?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#4 0.725 | turk-milliyetciliginin-dogusu.md#4 0.703 | bugunku-turk-dunyasi.md#4 0.648 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#4 0.628 | ilk-turk-devletleri.md#1 0.621`

**k-cevapsiz-mohac#1** — Mohaç Savaşı hangi yıl yapılmıştır?
> Mohaç Savaşı 1526 yılında yapılmıştır. (Kaynak: osmanli-padisahlari.md)

Getirilen: `selcuklular-ve-malazgirt.md#4 0.488 | turklerin-islamiyeti-kabulu.md#1 0.472 | selcuklular-ve-malazgirt.md#0 0.454 | turk-denizciligi.md#3 0.442 | osmanli-padisahlari.md#4 0.435`

**k-cevapsiz-mohac#2** — karşı taraftaki kralın adı neydi?  
_Önceki soru: Mohaç Savaşı hangi yıl yapılmıştır?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `anadolu-beylikleri-ve-osmanlinin-kurulusu.md#2 0.426 | osmanli-padisahlari.md#1 0.424 | turk-devlet-gelenegi.md#0 0.415 | oguz-boylari-ve-turk-boy-yapisi.md#6 0.412 | osmanli-padisahlari.md#4 0.410`

**k-cevapsiz-baskent#1** — Göktürk Devleti ne zaman kurulmuştur?
> Göktürk Devleti 552 yılında kurulmuştur. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#1 0.766 | ilk-turk-devletleri.md#4 0.670 | turk-milliyetciliginin-dogusu.md#4 0.602 | turk-milliyetciliginin-dogusu.md#0 0.585 | turklerin-islamiyeti-kabulu.md#3 0.582`

**k-cevapsiz-baskent#2** — başkenti neresiydi?  
_Önceki soru: Göktürk Devleti ne zaman kurulmuştur?_
> Bursa'nın başkenti 1326 yılında Orhan Gazi döneminde yapılmıştır.  Selçukluların başkenti ise Konya'ya taşınmıştır.  Osmanlı'nın külliyesi ve şehir düzeni genel olarak çeşitli şehirlerde kurulmuş olabilir, ancak belirli bir başkenti belirtilmemiştir.  Mustafa Kemal Atatürk'ün başkenti Ankara'dır, ancak soruda belirtilen tarihlerdeki başkentler hakkında bilgi verilmiştir.  Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `anadolu-beylikleri-ve-osmanlinin-kurulusu.md#8 0.567 | selcuklular-ve-malazgirt.md#3 0.489 | selcuklu-ve-osmanli-mimarisi.md#7 0.485 | bozkir-gocebe-yasami.md#8 0.478 | mustafa-kemal-ataturk.md#5 0.477`

**k-cevapsiz-uygur#1** — Uygur Kağanlığı hangi yıl kurulmuştur?
> Uygur Kağanlığı 744'te kurulmuştur. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#4 0.660 | turklerin-islamiyeti-kabulu.md#3 0.576 | turk-islam-dunyasinda-bilim.md#5 0.567 | turkcenin-tarihi-ve-alfabeleri.md#1 0.558 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.541`

**k-cevapsiz-uygur#2** — ne zaman yıkıldı?  
_Önceki soru: Uygur Kağanlığı hangi yıl kurulmuştur?_
> Saltanatın 1 Kasım 1922'de kaldırıldı. (Kaynak: cumhuriyet-inkilaplari.md)

Getirilen: `cumhuriyet-inkilaplari.md#1 0.450 | osmanli-padisahlari.md#4 0.435 | osmanli-islahat-ve-mesrutiyet.md#1 0.434 | osmanli-islahat-ve-mesrutiyet.md#0 0.413 | cumhuriyet-inkilaplari.md#0 0.411`

**k-degisim-otag#1** — Lozan Antlaşması ne zaman imzalanmıştır?
> Lozan Antlaşması 24 Temmuz 1923'te imzalanmıştır. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#3 0.492 | canakkale-ve-kurtulus-savasi.md#4 0.485 | osmanli-islahat-ve-mesrutiyet.md#0 0.466 | cumhuriyet-inkilaplari.md#2 0.408 | bugunku-turk-dunyasi.md#4 0.400`

**k-degisim-otag#2** — Otağ nedir?  
_Önceki soru: Lozan Antlaşması ne zaman imzalanmıştır?_
> Otağ, Türk topluluklarında yurt veya kerege adlarıyla anılan sökülüp taşınabilen keçe çadırın isminin bir formudur. Bu yapı, iskeleti makas biçiminde açılıp kapanan kafes duvarlar ve çubuklardan oluşur ve tepedeki çember hem baca hem pencere görevi görürken dumanı dışarı verir. Üzeri keçeyle kaplanarak kışın soğuğu geçirmezken, yazın sıcağı geçirir. (Kaynak: bozkir-gocebe-yasami.md)

Getirilen: `bozkir-gocebe-yasami.md#2 0.461 | turk-destanlari.md#1 0.450 | turk-kulturunde-at.md#0 0.425 | turk-kulturunde-at.md#1 0.409 | oguz-boylari-ve-turk-boy-yapisi.md#5 0.400`

**k-degisim-okculuk#1** — Orhun Yazıtları kimler adına dikilmiştir?
> Orhun Yazıtları, vezir Tonyukuk, Kül Tigin ve Bilge Kağan adına dikilmiştir. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#2 0.756 | turkcenin-tarihi-ve-alfabeleri.md#0 0.613`

**k-degisim-okculuk#2** — Atlı okçuluk nedir?  
_Önceki soru: Orhun Yazıtları kimler adına dikilmiştir?_
> Atlı okçuluk, dörtnala giderken ok atabilme becerisi olarak tanımlanabilir. Bu beceri, Türk ordularında askeri üstünlük sağlayarak ağır piyade karşı hareketlerde fayda sağlar. Bu yöntem, Turan taktiği adı altında bilinen bir yöntemle desteklenir ve Malazgirt Savaşı'nda da uygulanmıştır. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#1 0.607 | turk-kulturunde-at.md#0 0.505 | osmanli-devlet-teskilati.md#6 0.485 | ilk-turk-islam-eserleri.md#5 0.444`

**k-degisim-tugrul#1** — Yusuf Akçura'nın yazısı nerede yayımlanmıştır?
> Yusuf Akçura'nın yazısı 1904'te Kahire'de yayımlanmıştır. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#1 0.690 | milli-semboller.md#4 0.477`

**k-degisim-tugrul#2** — Tuğrul Bey kimdir?  
_Önceki soru: Yusuf Akçura'nın yazısı nerede yayımlanmıştır?_
> Tuğrul Bey, Selçukluların kurucusu olarak anılır. Bağlamda belirtilmemiş, ancak Türk-İslam Dünyasında Bilim ve Türk Denizciliği metinlerinde de geçmemektedir. Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-islam-dunyasinda-bilim.md#5 0.630 | turk-denizciligi.md#0 0.553 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#2 0.508 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.508 | selcuklular-ve-malazgirt.md#1 0.496`

**k-disi-telefon#1** — Kurultayda hangi kararlar alınırdı?
> Kurultayda savaş, barış ve hükümdar seçimi gibi konular görüşülürdü ve kararlar tartışılarak alındı. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#2 0.631 | turk-kulturunde-kurt.md#2 0.570 | turk-kulturunde-kurt.md#4 0.536 | osmanli-islahat-ve-mesrutiyet.md#2 0.493`

**k-disi-telefon#2** — En iyi akıllı telefon hangisidir?  
_Önceki soru: Kurultayda hangi kararlar alınırdı?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-devlet-gelenegi.md#2 0.572 | turk-kulturunde-kurt.md#2 0.494 | turk-kulturunde-kurt.md#6 0.493`

**k-disi-yagmur#1** — Türk Ocağı ne zaman kurulmuştur?
> Türk Ocağı 25 Mart 1912'de kurulmuştur. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.750 | bugunku-turk-dunyasi.md#5 0.615 | ilk-turk-devletleri.md#1 0.603 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.592 | bugunku-turk-dunyasi.md#4 0.581`

**k-disi-yagmur#2** — Yarın İstanbul'da yağmur yağacak mı?  
_Önceki soru: Türk Ocağı ne zaman kurulmuştur?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.666 | bugunku-turk-dunyasi.md#5 0.572 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.564 | bugunku-turk-dunyasi.md#4 0.554 | osmanli-islahat-ve-mesrutiyet.md#6 0.533`

