# Değerlendirme: 2026-09-19 00:25 — hibrit-acik

| Ayar | Değer |
|---|---|
| soru_seti | kontrol |
| sohbet_modeli | qwen2.5-7b-instruct-cuda-gpu |
| gomme_modeli | qwen3-embedding-0.6b-cuda-gpu |
| top_k | 8 |
| min_score | 0.33 |
| takip_farki | 0.2 |
| max_tokens | 600 |
| parca_sayisi | 212 |
| parcalama | paragraf + baslik yolu, ortusme yok |
| chunk_size | 1000 |
| sorgu_talimati | Soruyu cevaplayan paragrafı bul |
| arama | hibrit: vektör + FTS5 (5 harf önek), RRF k=60 |
| cevap_dogrulama | kapalı |
| git | dbeaba1 (kaydedilmemis degisiklik var) |
| set_parmak_izi | 48c99f2867 |

## Özet

Puanlanan soru: 41 (25 cevaplanabilir, 16 cevaplanamaz). Senaryoların hazırlık soruları özete katılmaz.

Karşılaştırılan çalışma: `degerlendirmeler/2026-09-18_2220_kontrol_belge-siniri-080.json`

| Ölçüt | Önceki | Şimdi |
|---|---|---|
| Tam başarı (tüm puanlanan sorular) | 82.9% | 80.5% |
| Arama: doğru parça 1. sırada (hit@1) | 80.0% | 88.0% |
| Arama: doğru parça ilk 3'te (hit@3) | 92.0% | 96.0% |
| Arama: MRR (1 = hep 1. sırada) | 0.852 | 0.927 |
| Cevaplanabilir sorularda başarı | 84.0% | 88.0% |
| Yanlış red (cevap belgede varken) | 4.0% | 0.0% |
|   bunun eşikte olanı | 0.0% | 0.0% |
| Anahtar ifadelerin tamamı cevapta | 95.8% | 96.0% |
| Bilinen yanlışı içeren cevap | 0 adet | 0 adet |
| Kaynak satırı var | 100.0% | 100.0% |
| Kaynak doğru belge | 87.5% | 88.0% |
| Cevaplanamaz soruları reddetme | 81.2% | 68.8% |
|   bunun eşikte olanı | 0.0% | 0.0% |
| Red cevabına eklenmiş kaynak satırı | 0 adet | 0 adet |
| Doğrulamada reddedilen cevaplanabilir | 0 adet | 0 adet |
| Doğrulamada reddedilen cevaplanamaz | 0 adet | 0 adet |
| Türkçe olmayan yazı kalan cevap | 0 adet | 0 adet |
| Türkçe olmayan yazı kesilen cevap | 1 adet | 2 adet |
| Süre ortalaması | 4.38 sn | 2.43 sn |
| Süre medyanı | 4.57 sn | 2.12 sn |
| En uzun süre | 7.67 sn | 7.14 sn |
| İlk token ortalaması (modele giden sorular) | 3.0 sn | 0.95 sn |
| Arama süresi ortalaması | 0.495 sn | 0.487 sn |

## Kategorilere göre

| Kategori | Soru | Başarılı | hit@1 | hit@3 | Yanlış red |
|---|---|---|---|---|---|
| normal | 13 | 12 | 12 | 13 | 0 |
| ozel_ad | 5 | 4 | 5 | 5 | 0 |
| yakin | 8 | 6 | - | - | - |
| takip | 4 | 4 | 4 | 4 | 0 |
| takip_cevapsiz | 6 | 3 | - | - | - |
| konu_degisimi | 3 | 2 | 1 | 2 | 0 |
| konu_disi_sonra | 2 | 2 | - | - | - |
| hazirlik (puanlanmaz) | 15 | - | - | - | - |

## Önceki çalışmaya göre değişen sorular

Cevap metni değişen soru: 22. Sonucu değişen soru: 5.

- **k-saltanat** OK → HATA: Osmanlı saltanatı ne zaman ve kim tarafından kaldırılmıştır? (yanlış kaynak: cumhuriyet-inkilaplari.md)
- **k-takip-konya#2** HATA → OK: başkenti daha sonra nereye taşındı?
- **k-cevapsiz-mohac#2** OK → HATA: karşı taraftaki kralın adı neydi? (cevaplanamaz soruya cevap verdi)
- **k-cevapsiz-baskent#2** OK → HATA: başkenti neresiydi? (cevaplanamaz soruya cevap verdi)
- **k-degisim-tugrul#2** HATA → OK: Tuğrul Bey kimdir? (doğru parça ilk 3'te değil (sıra 6))

## Başarısız sorular

- **k-saltanat** (normal) Osmanlı saltanatı ne zaman ve kim tarafından kaldırılmıştır?
  - Neden: yanlış kaynak: cumhuriyet-inkilaplari.md
  - Cevap: Osmanlı saltanatı 1 Kasım 1922'de kaldırılmıştır. Bu tarihle birlikte saltanatın sona ermesi ve Cumhuriyet döneminin başlangıcı yapılmıştır. Cüneyt Atatürk ve Türkiye Büyük Millet Meclisi tarafından saltanat kaldırılarak Osmanlı Padişahı VI. Mehmed Vahdettin'in saltanatın sona ermesi ve Cumhurbaşkanlığı sisteminin başlatılması gerçekleştirilmiştir. (Kaynak: cumhuriyet-inkilaplari.md)
- **k-manasci** (ozel_ad) Manasçı kimdir?
  - Neden: yanlış kaynak: ozan-asik-gelenegi.md
  - Cevap: Manasçı, Kırgızlarda destan anlatıcısını ifade eder ve Manas Destanı'nı ezberden ve doğaçlama eklemelerle anlatır. Manasçılar, yarım milyon dizeye yaklaşan Manas Destanı'nı yazıya bakmadan anlatırlar. Bu gelenek, usta-çırak ilişkisiyle aktarılmış ve 2013'te UNESCO listesine alınmıştır. (Kaynak: ozan-asik-gelenegi.md)
- **k-edirne** (yakin) Osmanlı başkenti Edirne'ye ne zaman taşınmıştır?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Osmanlı başkenti Edirne'ye taşınma tarihi belirsiz olarak verilmiştir. (Kaynak: osmanli-padisahlari.md)
- **k-dogu-cephesi** (yakin) Kurtuluş Savaşı'nda Doğu Cephesi komutanı kimdi?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Kurtuluş Savaşı'nda Doğu Cephesi komutanı Mustafa Kemal Atatürk'tü. (Kaynak: mustafa-kemal-ataturk.md)
- **k-cevapsiz-mohac#2** (takip_cevapsiz) karşı taraftaki kralın adı neydi?
  - Önceki soru: Mohaç Savaşı hangi yıl yapılmıştır?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: IV. Romanos Diogenes (Kaynak: selcuklular-ve-malazgirt.md)
- **k-cevapsiz-baskent#2** (takip_cevapsiz) başkenti neresiydi?
  - Önceki soru: Göktürk Devleti ne zaman kurulmuştur?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Selçuklular başkentini Konya'ya taşımıştır.  Anadolu Beylikleri ve Osmanlı'nın Kuruluşu metninde belirtiliyor ki, 1302'deki Koyunhisar Savaşı ile Bursa çevresindeki Bizans direnci kırılmış ve 1326'da Orhan Gazi döneminde Bursa alınmış, başkent olarak yapılmıştır.  Bugünkü Türk Dünyası metninde ise Türk Kültür ve Miras Vakfı'nın Bakü'de bulunmaktadır.  Selçuklu ve Osmanlı Mimarisi metninde külliye yapısının cami, medrese, kütüphane, darüşşifa, imaret, hamam, sıbyan mektebi, türbe ve arasta içerdiğini anlatıyor ancak başkent konusuna referans verilmiyor.  Bozkır Göçebe Yaşamı metninde göçebe yaşamın yerleşik hayatın hiç bilinmediği anlamına geldiğini ve Uygurların dokuzuncu yüzyılda tapınaklar ve şehirler kurduğunu belirtiyor ancak başkent konusuna değinmiyor.  Sonuç olarak, Selçuklular'ın başkenti Konya ve Osmanlıların başkenti Bursa olmuştur. (Kaynak: selcuklular-ve-malazgirt.md, anadolu-beylikleri-ve-osmanlinin-kurulusu.md)
- **k-cevapsiz-uygur#2** (takip_cevapsiz) ne zaman yıkıldı?
  - Önceki soru: Uygur Kağanlığı hangi yıl kurulmuştur?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Osmanlı Devleti, Cumhuriyet ilan edildiği 29 Ekim 1923'te saltanatın kaldırılarak Cumhuriyet dönemi başladığında sona ermiştir. (Kaynak: cumhuriyet-inkilaplari.md)
- **k-degisim-otag#2** (konu_degisimi) Otağ nedir?
  - Önceki soru: Lozan Antlaşması ne zaman imzalanmıştır?
  - Neden: eksik: sembol; yanlış kaynak: bozkir-gocebe-yasami.md
  - Cevap: Otağ, Türk topluluklarında yurt veya kerege adıyla anılan sökülüp taşınabilen keçe çadırın ismini verir. Bu yapının tepedeki çemberi hem baca hem pencere olarak kullanırken, dumanı dışarı vermek için de kullanılır. Otağın kapısı genellikle doğuya bakar ve büyük hükmardan farklıdır. (Kaynak: bozkir-gocebe-yasami.md)

## Tüm sonuçlar

| id | Kategori | Sıra | En iyi skor | Eşikte red | Red | Anahtar | Kaynak | Süre | Sonuç |
|---|---|---|---|---|---|---|---|---|---|
| k-canakkale | normal | 1 | 0.626 |  |  | tam | doğru | 2.2 | OK |
| k-mete | normal | 1 | 0.578 |  |  | tam | doğru | 1.4 | OK |
| k-kutluk | normal | 1 | 0.677 |  |  | tam | doğru | 2.0 | OK |
| k-baba | normal | 1 | 0.747 |  |  | tam | doğru | 2.2 | OK |
| k-murad | normal | 1 | 0.49 |  |  | tam | doğru | 2.1 | OK |
| k-saltanat | normal | 2 | 0.649 |  |  | tam | yanlış | 3.4 | HATA |
| k-kinik | normal | 1 | 0.66 |  |  | tam | doğru | 2.0 | OK |
| k-malazgirt-onem | normal | 1 | 0.738 |  |  | tam | doğru | 3.4 | OK |
| k-akcura | normal | 1 | 0.793 |  |  | tam | doğru | 1.9 | OK |
| k-harf-sayisi | normal | 1 | 0.793 |  |  | tam | doğru | 1.7 | OK |
| k-millet-mektep | normal | 1 | 0.608 |  |  | tam | doğru | 2.0 | OK |
| k-kurt-neden | normal | 1 | 0.836 |  |  | tam | doğru | 3.3 | OK |
| k-ad-koyma | normal | 1 | 0.773 |  |  | tam | doğru | 2.7 | OK |
| k-ulus | ozel_ad | 1 | 0.469 |  |  | tam | doğru | 3.6 | OK |
| k-toy | ozel_ad | 1 | 0.406 |  |  | tam | doğru | 2.6 | OK |
| k-manasci | ozel_ad | 1 | 0.534 |  |  | tam | yanlış | 3.2 | HATA |
| k-ortmece | ozel_ad | 1 | 0.424 |  |  | tam | doğru | 3.9 | OK |
| k-asena | ozel_ad | 1 | 0.433 |  |  | tam | doğru | 3.2 | OK |
| k-bumin-baba | yakin |  | 0.549 |  | evet |  |  | 1.8 | OK |
| k-edirne | yakin |  | 0.594 |  |  |  | var | 3.7 | HATA |
| k-alparslan-olum | yakin |  | 0.558 |  | evet |  |  | 1.7 | OK |
| k-gokalp-olum | yakin |  | 0.707 |  | evet |  |  | 1.5 | OK |
| k-macar-kral | yakin |  | 0.521 |  | evet |  |  | 2.1 | OK |
| k-thomsen-univ | yakin |  | 0.397 |  | evet |  |  | 1.6 | OK |
| k-korkut-hikaye | yakin |  | 0.728 |  | evet |  |  | 1.5 | OK |
| k-dogu-cephesi | yakin |  | 0.662 |  |  |  | var | 2.2 | HATA |
| k-takip-gokalp#1 | hazirlik |  | 0.77 |  |  |  | var | 1.7 | - |
| k-takip-gokalp#2 | takip | 1 | 0.809 |  |  | tam | doğru | 2.3 | OK |
| k-takip-korkut#1 | hazirlik |  | 0.776 |  |  |  | var | 1.8 | - |
| k-takip-korkut#2 | takip | 1 | 0.79 |  |  | tam | doğru | 2.0 | OK |
| k-takip-sam#1 | hazirlik |  | 0.706 |  |  |  | var | 2.2 | - |
| k-takip-sam#2 | takip | 1 | 0.76 |  |  | tam | doğru | 2.3 | OK |
| k-takip-konya#1 | hazirlik |  | 0.721 |  |  |  | var | 2.3 | - |
| k-takip-konya#2 | takip | 1 | 0.55 |  |  | tam | doğru | 2.7 | OK |
| k-cevapsiz-malazgirt#1 | hazirlik |  | 0.663 |  |  |  | var | 2.1 | - |
| k-cevapsiz-malazgirt#2 | takip_cevapsiz |  | 0.44 |  | evet |  |  | 2.0 | OK |
| k-cevapsiz-nutuk#1 | hazirlik |  | 0.503 |  |  |  | var | 2.4 | - |
| k-cevapsiz-nutuk#2 | takip_cevapsiz |  | 0.384 |  | evet |  |  | 2.0 | OK |
| k-cevapsiz-tdk#1 | hazirlik |  | 0.76 |  |  |  | var | 2.4 | - |
| k-cevapsiz-tdk#2 | takip_cevapsiz |  | 0.725 |  | evet |  |  | 2.1 | OK |
| k-cevapsiz-mohac#1 | hazirlik |  | 0.488 |  |  |  | var | 1.9 | - |
| k-cevapsiz-mohac#2 | takip_cevapsiz |  | 0.426 |  |  |  | var | 2.5 | HATA |
| k-cevapsiz-baskent#1 | hazirlik |  | 0.766 |  |  |  | var | 2.0 | - |
| k-cevapsiz-baskent#2 | takip_cevapsiz |  | 0.567 |  |  |  | var | 7.1 | HATA |
| k-cevapsiz-uygur#1 | hazirlik |  | 0.66 |  |  |  | var | 2.0 | - |
| k-cevapsiz-uygur#2 | takip_cevapsiz |  | 0.45 |  |  |  | var | 2.8 | HATA |
| k-degisim-otag#1 | hazirlik |  | 0.492 |  |  |  | var | 2.1 | - |
| k-degisim-otag#2 | konu_degisimi | 2 | 0.461 |  |  | eksik | yanlış | 3.5 | HATA |
| k-degisim-okculuk#1 | hazirlik |  | 0.756 |  |  |  | var | 1.8 | - |
| k-degisim-okculuk#2 | konu_degisimi | 1 | 0.607 |  |  | tam | doğru | 3.2 | OK |
| k-degisim-tugrul#1 | hazirlik |  | 0.69 |  |  |  | var | 1.9 | - |
| k-degisim-tugrul#2 | konu_degisimi | 6 | 0.63 |  |  | tam | doğru | 4.1 | OK |
| k-disi-telefon#1 | hazirlik |  | 0.631 |  |  |  | var | 2.0 | - |
| k-disi-telefon#2 | konu_disi_sonra |  | 0.572 |  | evet |  |  | 2.0 | OK |
| k-disi-yagmur#1 | hazirlik |  | 0.75 |  |  |  | var | 2.0 | - |
| k-disi-yagmur#2 | konu_disi_sonra |  | 0.666 |  | evet |  |  | 2.1 | OK |

## Cevaplar (gözle kontrol için)

**k-canakkale** — Çanakkale'de İtilaf Devletleri neyi amaçlıyordu?
> İtilaf Devletleri, Çanakkale'de boğazı geçip İstanbul'a ulaşmayı ve Rusya'ya ulaşım hattı açmayı amaçlamıştır. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#0 0.626 | canakkale-ve-kurtulus-savasi.md#1 0.548 | turklerin-islamiyeti-kabulu.md#3 0.514 | turklerin-islamiyeti-kabulu.md#4 0.488 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#0 0.497`

**k-mete** — Mete Han Çin kaynaklarında hangi adla anılır?
> Mete Han Çin kaynaklarında Modu Chanyu adıyla anılır. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#0 0.578 | turk-kulturunde-kurt.md#1 0.395`

**k-kutluk** — İkinci Göktürk Devleti'ni kim, hangi yılda kurmuştur?
> İkinci Göktürk Devleti'ni İlteriş Kutluk Kağan, 682'de kurmuştur. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#1 0.677 | ilk-turk-devletleri.md#4 0.557 | bozkir-gocebe-yasami.md#6 0.516 | bozkir-gocebe-yasami.md#7 0.502 | turk-kulturunde-kurt.md#1 0.498`

**k-baba** — Mustafa Kemal'in babası kimdir, hangi işleri yapmıştır?
> Mustafa Kemal'in babası Ali Rıza Efendi'dir. Ali Rıza Efendi gümrük memurluğu ve kereste ticareti yapmıştır. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#0 0.747 | mustafa-kemal-ataturk.md#1 0.631 | mustafa-kemal-ataturk.md#6 0.586 | mustafa-kemal-ataturk.md#4 0.568 | mustafa-kemal-ataturk.md#2 0.547`

**k-murad** — I. Murad'ın hayatı nasıl sona ermiştir?
> I. Murad 1389'daki I. Kosova Savaşı'nı kazanmış ancak savaş alanında öldürülmüştür. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#1 0.490 | osmanli-padisahlari.md#2 0.379 | osmanli-islahat-ve-mesrutiyet.md#3 0.455 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#0 0.369 | turk-islam-dunyasinda-bilim.md#7 0.379`

**k-saltanat** — Osmanlı saltanatı ne zaman ve kim tarafından kaldırılmıştır?
> Osmanlı saltanatı 1 Kasım 1922'de kaldırılmıştır. Bu tarihle birlikte saltanatın sona ermesi ve Cumhuriyet döneminin başlangıcı yapılmıştır. Cüneyt Atatürk ve Türkiye Büyük Millet Meclisi tarafından saltanat kaldırılarak Osmanlı Padişahı VI. Mehmed Vahdettin'in saltanatın sona ermesi ve Cumhurbaşkanlığı sisteminin başlatılması gerçekleştirilmiştir. (Kaynak: cumhuriyet-inkilaplari.md)

Getirilen: `cumhuriyet-inkilaplari.md#1 0.640 | osmanli-padisahlari.md#4 0.622 | osmanli-islahat-ve-mesrutiyet.md#6 0.570 | osmanli-islahat-ve-mesrutiyet.md#0 0.649 | osmanli-padisahlari.md#3 0.588`

**k-kinik** — Büyük Selçuklu hanedanı hangi Oğuz boyundan gelir?
> Büyük Selçuklu hanedanı Kınık boyundan gelir. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#0 0.660 | oguz-boylari-ve-turk-boy-yapisi.md#4 0.604 | turk-destanlari.md#1 0.576 | oguz-boylari-ve-turk-boy-yapisi.md#5 0.577 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.559`

**k-malazgirt-onem** — Malazgirt Savaşı Anadolu'nun tarihi açısından neden önemlidir?
> Malazgirt Savaşı Anadolu'nun tarihi açısından önemlidir çünkü savaşın ardından Bizans'ın Anadolu'daki savunma düzeni çökmüş ve Türkmen boyları Anadolu içlerine doğru yerleşmeye başlamıştır. Bu süreç, Anadolu'nun Türkleşme sürecinin başlangıcı olarak kabul edilir ve Bizans İmparatorluğu'nun Anadolu'daki kontrolünün zayıflamasına yol açmıştır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#2 0.738 | selcuklular-ve-malazgirt.md#1 0.671 | selcuklular-ve-malazgirt.md#4 0.635 | selcuklular-ve-malazgirt.md#3 0.571 | selcuklular-ve-malazgirt.md#0 0.631`

**k-akcura** — Yusuf Akçura yazısında hangi siyaset biçimlerini karşılaştırmıştır?
> Yusuf Akçura yazısında Osmanlıcılık, İslamcılık ve Türkçülük olmak üzere üç siyaset biçimini karşılaştırmıştır. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#1 0.793 | osmanli-islahat-ve-mesrutiyet.md#10 0.447`

**k-harf-sayisi** — Latin harflerine dayalı yeni Türk alfabesinde kaç harf vardır?
> Yeni Türk alfabesinde yirmi dokuz harf vardır. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#3 0.793 | bugunku-turk-dunyasi.md#6 0.738 | turkcenin-tarihi-ve-alfabeleri.md#4 0.661`

**k-millet-mektep** — Yeni alfabeye geçişte halka okuma yazma öğretmek için hangi okullar açıldı?
> Millet Mektepleri açılmıştır. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md, cumhuriyet-inkilaplari.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#3 0.608 | cumhuriyet-inkilaplari.md#5 0.543 | turkcenin-tarihi-ve-alfabeleri.md#1 0.536 | bugunku-turk-dunyasi.md#6 0.534 | ilk-turk-devletleri.md#3 0.477`

**k-kurt-neden** — Türk kültüründe sembol olarak neden kurt seçilmiştir?
> Türk kültüründe kurt sembol olarak seçilmesinin nedeni, kurtun sürü hâlinde yaşaması, dayanıklılığı ve evcilleşmemesi olgusundan kaynaklanmaktadır. Ayrıca, kurt figürü, Bozkır topluluklarının hayvan sembolleri arasında önemli bir yer tuttuğu ve bunlar topluluğun kendini tanımlama biçimleri olarak kullanılması sonucunda bu tanımın merkezinde yer aldığını gösterir. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#4 0.836 | turk-kulturunde-kurt.md#3 0.806 | turk-kulturunde-kurt.md#0 0.786 | turk-kulturunde-kurt.md#6 0.718 | turk-kulturunde-kurt.md#2 0.651`

**k-ad-koyma** — Dede Korkut hikâyelerindeki ad koyma geleneği nasıldır?
> Dede Korkut hikâyelerinde bir gencin ad alabilmek için önce bir yiğitlik göstermesi gerekmektedir. Bu geleneğin en bilinen örneği olarak, bir gencin adını alabilmek için yiğitlik gösterdiği anlatılmaktadır. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.773 | turk-kulturunde-at.md#5 0.617 | ozan-asik-gelenegi.md#1 0.553 | turk-kulturunde-kurt.md#6 0.577`

**k-ulus** — Ülüş nedir?
> Ülüş, gelirin ve ganimetin boylar arasında paylaşılan bir gelenektir. Savaştan veya vergiden elde edilen malların boylar arasında töreye uygun biçimde bölünmesi beklenirken, pay dağıtımındaki sırayla boyların devlet içindeki önem gösterilir. Hükümdarın cömertlik, paylaşımda haksızlık yapan hükümdarın meşruiyetini yitireceği inanışı da yöneticilik erdemlerinden biridir. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#5 0.452 | turk-kulturunde-at.md#2 0.469 | oguz-boylari-ve-turk-boy-yapisi.md#0 0.462 | turk-mitolojisi-ve-gok-tanri.md#7 0.433 | ozan-asik-gelenegi.md#3 0.416`

**k-toy** — Toy nedir?
> Toy, devletin önemli kararlarının alındığı bir kurultaydır. Burada tartışılacak konular genellikle savaş, barış ve hükümdar seçimi gibi önemli materyaller olurken, kararlar boy beyleri ve hanedan üyeleri tarafından tartışılarak alınırdı. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#2 0.406 | turk-kulturunde-at.md#0 0.363 | turk-devlet-gelenegi.md#1 0.349 | turk-mitolojisi-ve-gok-tanri.md#0 0.341 | bugunku-turk-dunyasi.md#5 0.338`

**k-manasci** — Manasçı kimdir?
> Manasçı, Kırgızlarda destan anlatıcısını ifade eder ve Manas Destanı'nı ezberden ve doğaçlama eklemelerle anlatır. Manasçılar, yarım milyon dizeye yaklaşan Manas Destanı'nı yazıya bakmadan anlatırlar. Bu gelenek, usta-çırak ilişkisiyle aktarılmış ve 2013'te UNESCO listesine alınmıştır. (Kaynak: ozan-asik-gelenegi.md)

Getirilen: `turk-destanlari.md#3 0.534 | ozan-asik-gelenegi.md#2 0.524 | turk-mitolojisi-ve-gok-tanri.md#5 0.395 | selcuklu-ve-osmanli-mimarisi.md#5 0.391`

**k-ortmece** — Örtmece nedir?
> Örtmece, korkulan ya da saygı duyulan bir varlığın gerçek adını söylemekten kaçınılıp, yerine başka bir sözcük kullanma alışkanlığıdır. Bu yöntem, genellikle zayıf veya olumsuz nitelikli bir şeyin adını verilen bir varlığa atıfta bulunarak kullanılır. Türkçedeki "kurt" sözcüğünün eski anlamının solucan, kurtçuk, böcek larvası olduğunu gösterirken, kurtçuk yerine "kurt" adının kullanılmasının bir örtmece örneği olduğunu ifade eder. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#6 0.424 | selcuklu-ve-osmanli-mimarisi.md#4 0.274 | bozkir-gocebe-yasami.md#4 0.402 | bozkir-gocebe-yasami.md#0 0.378 | turkcenin-tarihi-ve-alfabeleri.md#0 0.370`

**k-asena** — Asena nedir?
> Asena, "Aşina"nın modern Türkçe okunuşudur. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#1 0.433 | ozan-asik-gelenegi.md#3 0.426 | ozan-asik-gelenegi.md#0 0.390 | turk-kulturunde-at.md#0 0.354 | milli-semboller.md#8 0.345`

**k-bumin-baba** — Bumin Kağan'ın babasının adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-destanlari.md#1 0.549 | mustafa-kemal-ataturk.md#0 0.458 | turk-mitolojisi-ve-gok-tanri.md#3 0.411 | ilk-turk-devletleri.md#1 0.392 | milli-semboller.md#3 0.392`

**k-edirne** — Osmanlı başkenti Edirne'ye ne zaman taşınmıştır?
> Osmanlı başkenti Edirne'ye taşınma tarihi belirsiz olarak verilmiştir. (Kaynak: osmanli-padisahlari.md)

Getirilen: `anadolu-beylikleri-ve-osmanlinin-kurulusu.md#8 0.594 | osmanli-padisahlari.md#0 0.576 | osmanli-padisahlari.md#2 0.544 | selcuklu-ve-osmanli-mimarisi.md#4 0.492 | osmanli-islahat-ve-mesrutiyet.md#0 0.534`

**k-alparslan-olum** — Sultan Alparslan hangi yıl ölmüştür?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `selcuklular-ve-malazgirt.md#1 0.541 | osmanli-padisahlari.md#2 0.501 | osmanli-padisahlari.md#4 0.541 | osmanli-islahat-ve-mesrutiyet.md#0 0.558 | selcuklular-ve-malazgirt.md#0 0.491`

**k-gokalp-olum** — Ziya Gökalp hangi şehirde vefat etmiştir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-milliyetciliginin-dogusu.md#2 0.707 | mustafa-kemal-ataturk.md#6 0.499 | bozkir-gocebe-yasami.md#8 0.522`

**k-macar-kral** — Mohaç Savaşı'nda yenilen Macar kralının adı nedir?
> Mohaç Savaşı'nda yenilen Macar kralının adı metnede belirtilmemiştir. Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `selcuklular-ve-malazgirt.md#4 0.486 | osmanli-padisahlari.md#4 0.521 | osmanli-padisahlari.md#1 0.440 | selcuklular-ve-malazgirt.md#1 0.469 | osmanli-islahat-ve-mesrutiyet.md#0 0.417`

**k-thomsen-univ** — Vilhelm Thomsen hangi üniversitede çalışıyordu?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `ilk-turk-devletleri.md#3 0.397 | turk-islam-dunyasinda-bilim.md#1 0.361 | turk-islam-dunyasinda-bilim.md#0 0.361 | selcuklu-ve-osmanli-mimarisi.md#5 0.318`

**k-korkut-hikaye** — Dede Korkut Kitabı'ndaki ilk hikâyenin adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-destanlari.md#4 0.728 | turk-kulturunde-at.md#5 0.558 | ilk-turk-islam-eserleri.md#0 0.513`

**k-dogu-cephesi** — Kurtuluş Savaşı'nda Doğu Cephesi komutanı kimdi?
> Kurtuluş Savaşı'nda Doğu Cephesi komutanı Mustafa Kemal Atatürk'tü. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#3 0.662 | canakkale-ve-kurtulus-savasi.md#3 0.528 | canakkale-ve-kurtulus-savasi.md#1 0.552 | canakkale-ve-kurtulus-savasi.md#2 0.516 | turk-denizciligi.md#3 0.516`

**k-takip-gokalp#1** — Ziya Gökalp nerede doğmuştur?
> Ziya Gökalp, 1876'da Diyarbakır'da doğmuştur. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#2 0.770 | mustafa-kemal-ataturk.md#0 0.454`

**k-takip-gokalp#2** — hangi formülü savunmuştur?  
_Önceki soru: Ziya Gökalp nerede doğmuştur?_
> Ziya Gökalp "Türkleşmek, İslamlaşmak, Muasırlaşmak" formülünü savunmuştur. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#2 0.809 | turk-milliyetciliginin-dogusu.md#3 0.507`

**k-takip-korkut#1** — Dede Korkut Kitabı kaç hikâyeden oluşur?
> Dede Korkut Kitabı, Oğuzların İslam sonrası dönemine ait on iki hikâyeden oluşur. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.776 | turk-kulturunde-at.md#5 0.575`

**k-takip-korkut#2** — yazmaları nerede bulunuyor?  
_Önceki soru: Dede Korkut Kitabı kaç hikâyeden oluşur?_
> Yazmaları Dresden ve Vatikan'da bulunuyor. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.790 | turk-kulturunde-at.md#5 0.583`

**k-takip-sam#1** — Mustafa Kemal Harp Akademisi'ni hangi yıl bitirmiştir?
> Mustafa Kemal Atatürk Harp Akademisi'ni 1905'te bitirmiştir. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#1 0.706 | mustafa-kemal-ataturk.md#6 0.599 | mustafa-kemal-ataturk.md#0 0.549 | mustafa-kemal-ataturk.md#4 0.535 | mustafa-kemal-ataturk.md#3 0.520`

**k-takip-sam#2** — ilk görev yeri neresiydi?  
_Önceki soru: Mustafa Kemal Harp Akademisi'ni hangi yıl bitirmiştir?_
> Mustafa Kemal Atatürk'nün ilk görev yeri Şam'daydı. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#1 0.760 | mustafa-kemal-ataturk.md#6 0.594 | mustafa-kemal-ataturk.md#2 0.540 | mustafa-kemal-ataturk.md#3 0.559 | mustafa-kemal-ataturk.md#0 0.539`

**k-takip-konya#1** — Anadolu Selçuklu Devleti'nin ilk merkezi neresiydi?
> Anadolu Selçuklu Devleti'nin ilk merkezi İznik'te yer almaktadır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#3 0.721 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#1 0.650 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#0 0.666 | selcuklular-ve-malazgirt.md#2 0.627 | ilk-turk-islam-eserleri.md#7 0.608`

**k-takip-konya#2** — başkenti daha sonra nereye taşındı?  
_Önceki soru: Anadolu Selçuklu Devleti'nin ilk merkezi neresiydi?_
> Anadolu Selçuklu Devleti'nin başkenti daha sonra Konya'ya taşındı. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#3 0.481 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#8 0.550 | turk-devlet-gelenegi.md#3 0.442 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#7 0.446 | osmanli-devlet-teskilati.md#5 0.406`

**k-cevapsiz-malazgirt#1** — Malazgirt Savaşı ne zaman yapılmıştır?
> Malazgirt Savaşı 26 Ağustos 1071'de yapılmıştır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.663 | selcuklular-ve-malazgirt.md#2 0.660 | selcuklular-ve-malazgirt.md#0 0.634 | selcuklular-ve-malazgirt.md#4 0.572 | selcuklular-ve-malazgirt.md#3 0.485`

**k-cevapsiz-malazgirt#2** — savaşta kaç kişi öldü?  
_Önceki soru: Malazgirt Savaşı ne zaman yapılmıştır?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `canakkale-ve-kurtulus-savasi.md#0 0.419 | turklerin-islamiyeti-kabulu.md#1 0.440 | selcuklular-ve-malazgirt.md#2 0.375 | selcuklular-ve-malazgirt.md#0 0.347 | mustafa-kemal-ataturk.md#2 0.343`

**k-cevapsiz-nutuk#1** — Nutuk ne zaman okunmuştur?
> Mustafa Kemal Atatürk, 15-20 Ekim 1927 tarihleri arasında Cumhuriyet Halk Partisi kongresinde Nutuk adlı konuşmasını okumuştur. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#5 0.503 | ilk-turk-islam-eserleri.md#1 0.456 | milli-semboller.md#10 0.446 | ilk-turk-islam-eserleri.md#2 0.428 | nevruz-ve-turk-bayramlari.md#0 0.416`

**k-cevapsiz-nutuk#2** — kaç sayfadır?  
_Önceki soru: Nutuk ne zaman okunmuştur?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-mitolojisi-ve-gok-tanri.md#6 0.384 | ilk-turk-islam-eserleri.md#1 0.361 | ilk-turk-islam-eserleri.md#2 0.355 | turkcenin-tarihi-ve-alfabeleri.md#0 0.348 | turk-destanlari.md#3 0.346`

**k-cevapsiz-tdk#1** — Türk Dil Kurumu ne zaman kurulmuştur?
> Türk Dil Kurumu, 12 Temmuz 1932'de kurulan Türk Dili Tetkik Cemiyeti olarak kurulmuştur ve bugün faaliyet göstermektedir. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.760 | turkcenin-tarihi-ve-alfabeleri.md#4 0.760 | bugunku-turk-dunyasi.md#4 0.671 | cumhuriyet-inkilaplari.md#5 0.627 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#4 0.637`

**k-cevapsiz-tdk#2** — ilk başkanı kimdi?  
_Önceki soru: Türk Dil Kurumu ne zaman kurulmuştur?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#4 0.725 | turk-milliyetciliginin-dogusu.md#4 0.703 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#4 0.628 | bugunku-turk-dunyasi.md#5 0.619 | bugunku-turk-dunyasi.md#4 0.648`

**k-cevapsiz-mohac#1** — Mohaç Savaşı hangi yıl yapılmıştır?
> Mohaç Savaşı 1526 yılında yapılmıştır. (Kaynak: osmanli-padisahlari.md)

Getirilen: `turklerin-islamiyeti-kabulu.md#1 0.472 | osmanli-padisahlari.md#4 0.435 | turk-denizciligi.md#3 0.442 | selcuklular-ve-malazgirt.md#4 0.488 | selcuklular-ve-malazgirt.md#0 0.454`

**k-cevapsiz-mohac#2** — karşı taraftaki kralın adı neydi?  
_Önceki soru: Mohaç Savaşı hangi yıl yapılmıştır?_
> IV. Romanos Diogenes (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `anadolu-beylikleri-ve-osmanlinin-kurulusu.md#2 0.426 | selcuklular-ve-malazgirt.md#1 0.401 | turk-devlet-gelenegi.md#0 0.415 | osmanli-padisahlari.md#4 0.410 | osmanli-padisahlari.md#1 0.424`

**k-cevapsiz-baskent#1** — Göktürk Devleti ne zaman kurulmuştur?
> Göktürk Devleti 552 yılında kurulmuştur. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#1 0.766 | ilk-turk-devletleri.md#4 0.670 | selcuklular-ve-malazgirt.md#0 0.565 | turk-milliyetciliginin-dogusu.md#4 0.602 | turklerin-islamiyeti-kabulu.md#3 0.582`

**k-cevapsiz-baskent#2** — başkenti neresiydi?  
_Önceki soru: Göktürk Devleti ne zaman kurulmuştur?_
> Selçuklular başkentini Konya'ya taşımıştır.  Anadolu Beylikleri ve Osmanlı'nın Kuruluşu metninde belirtiliyor ki, 1302'deki Koyunhisar Savaşı ile Bursa çevresindeki Bizans direnci kırılmış ve 1326'da Orhan Gazi döneminde Bursa alınmış, başkent olarak yapılmıştır.  Bugünkü Türk Dünyası metninde ise Türk Kültür ve Miras Vakfı'nın Bakü'de bulunmaktadır.  Selçuklu ve Osmanlı Mimarisi metninde külliye yapısının cami, medrese, kütüphane, darüşşifa, imaret, hamam, sıbyan mektebi, türbe ve arasta içerdiğini anlatıyor ancak başkent konusuna referans verilmiyor.  Bozkır Göçebe Yaşamı metninde göçebe yaşamın yerleşik hayatın hiç bilinmediği anlamına geldiğini ve Uygurların dokuzuncu yüzyılda tapınaklar ve şehirler kurduğunu belirtiyor ancak başkent konusuna değinmiyor.  Sonuç olarak, Selçuklular'ın başkenti Konya ve Osmanlıların başkenti Bursa olmuştur. (Kaynak: selcuklular-ve-malazgirt.md, anadolu-beylikleri-ve-osmanlinin-kurulusu.md)

Getirilen: `selcuklular-ve-malazgirt.md#3 0.489 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#8 0.567 | bugunku-turk-dunyasi.md#5 0.402 | selcuklu-ve-osmanli-mimarisi.md#7 0.485 | bozkir-gocebe-yasami.md#8 0.478`

**k-cevapsiz-uygur#1** — Uygur Kağanlığı hangi yıl kurulmuştur?
> Uygur Kağanlığı 744'te kurulmuştur. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#4 0.660 | turklerin-islamiyeti-kabulu.md#3 0.576 | oguz-boylari-ve-turk-boy-yapisi.md#8 0.535 | turkcenin-tarihi-ve-alfabeleri.md#1 0.558 | turk-mitolojisi-ve-gok-tanri.md#8 0.505`

**k-cevapsiz-uygur#2** — ne zaman yıkıldı?  
_Önceki soru: Uygur Kağanlığı hangi yıl kurulmuştur?_
> Osmanlı Devleti, Cumhuriyet ilan edildiği 29 Ekim 1923'te saltanatın kaldırılarak Cumhuriyet dönemi başladığında sona ermiştir. (Kaynak: cumhuriyet-inkilaplari.md)

Getirilen: `osmanli-padisahlari.md#0 0.403 | turklerin-islamiyeti-kabulu.md#3 0.338 | oguz-boylari-ve-turk-boy-yapisi.md#9 0.323 | cumhuriyet-inkilaplari.md#1 0.450 | osmanli-padisahlari.md#4 0.435`

**k-degisim-otag#1** — Lozan Antlaşması ne zaman imzalanmıştır?
> Lozan Antlaşması 24 Temmuz 1923'te imzalanmıştır. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#3 0.492 | canakkale-ve-kurtulus-savasi.md#4 0.485 | osmanli-islahat-ve-mesrutiyet.md#0 0.466 | bugunku-turk-dunyasi.md#4 0.400 | canakkale-ve-kurtulus-savasi.md#2 0.387`

**k-degisim-otag#2** — Otağ nedir?  
_Önceki soru: Lozan Antlaşması ne zaman imzalanmıştır?_
> Otağ, Türk topluluklarında yurt veya kerege adıyla anılan sökülüp taşınabilen keçe çadırın ismini verir. Bu yapının tepedeki çemberi hem baca hem pencere olarak kullanırken, dumanı dışarı vermek için de kullanılır. Otağın kapısı genellikle doğuya bakar ve büyük hükmardan farklıdır. (Kaynak: bozkir-gocebe-yasami.md)

Getirilen: `bozkir-gocebe-yasami.md#2 0.461 | turk-devlet-gelenegi.md#4 0.366 | turk-destanlari.md#1 0.450 | turk-kulturunde-at.md#0 0.425 | turk-kulturunde-at.md#1 0.409`

**k-degisim-okculuk#1** — Orhun Yazıtları kimler adına dikilmiştir?
> Orhun Yazıtları, vezir Tonyukuk, Kül Tigin ve Bilge Kağan adına dikilmiştir. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#2 0.756 | turkcenin-tarihi-ve-alfabeleri.md#0 0.619`

**k-degisim-okculuk#2** — Atlı okçuluk nedir?  
_Önceki soru: Orhun Yazıtları kimler adına dikilmiştir?_
> Atlı okçuluk, dörtnala giderken ok atabilme becerisidir ve Türk ordularının askerî açıdan belirleyici bir özelliği olmuştur. Bu beceri, ağır piyadeye karşı hareket üstünlüğü sağlamış ve Turan taktiği adı altında kullanılan yöntemde de kullanılmıştır. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#1 0.607 | turk-kulturunde-at.md#2 0.461 | turk-kulturunde-at.md#0 0.505 | turk-kulturunde-at.md#5 0.502 | osmanli-devlet-teskilati.md#6 0.485`

**k-degisim-tugrul#1** — Yusuf Akçura'nın yazısı nerede yayımlanmıştır?
> Yusuf Akçura'nın yazısı 1904'te Kahire'de yayımlanmıştır. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#1 0.690 | milli-semboller.md#3 0.443`

**k-degisim-tugrul#2** — Tuğrul Bey kimdir?  
_Önceki soru: Yusuf Akçura'nın yazısı nerede yayımlanmıştır?_
> Tuğrul Bey, Selçukluların kurucusu olan bir Türk lideridir. Bağlamda belirtilmemiş, ancak Selçuklular ve Malazgirt Savaşı metninde Tuğrul Bey'in ardından tahta çıkan Sultan Alparslan döneminde Anadolu yönündeki akınlar yoğunlaşmış olduğu ve Malazgirt Savaşı'nın gerçekleştiği bilinir. Bu bilgilere göre, Tuğrul Bey Selçukluların kurucusu olduğu anlaşılmaktadır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `turk-islam-dunyasinda-bilim.md#5 0.630 | turk-denizciligi.md#0 0.553 | selcuklular-ve-malazgirt.md#1 0.496 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#4 0.500 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.508`

**k-disi-telefon#1** — Kurultayda hangi kararlar alınırdı?
> Kurultayda savaş, barış ve hükümdar seçimi gibi konular görüşülürdü ve kararlar tartışılarak alındı. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#2 0.631 | turk-destanlari.md#4 0.437 | osmanli-islahat-ve-mesrutiyet.md#6 0.458`

**k-disi-telefon#2** — En iyi akıllı telefon hangisidir?  
_Önceki soru: Kurultayda hangi kararlar alınırdı?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-devlet-gelenegi.md#2 0.572 | bugunku-turk-dunyasi.md#6 0.414 | turk-milliyetciliginin-dogusu.md#4 0.415 | osmanli-islahat-ve-mesrutiyet.md#6 0.410`

**k-disi-yagmur#1** — Türk Ocağı ne zaman kurulmuştur?
> Türk Ocağı 25 Mart 1912'de kurulmuştur. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.750 | bugunku-turk-dunyasi.md#5 0.615 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.592 | osmanli-islahat-ve-mesrutiyet.md#6 0.567 | selcuklular-ve-malazgirt.md#0 0.580`

**k-disi-yagmur#2** — Yarın İstanbul'da yağmur yağacak mı?  
_Önceki soru: Türk Ocağı ne zaman kurulmuştur?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.666 | osmanli-islahat-ve-mesrutiyet.md#6 0.533 | bugunku-turk-dunyasi.md#4 0.554 | cumhuriyet-inkilaplari.md#5 0.531 | bugunku-turk-dunyasi.md#5 0.572`

