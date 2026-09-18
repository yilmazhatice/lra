# Değerlendirme: 2026-09-18 04:54 — birlesik-nihai

| Ayar | Değer |
|---|---|
| soru_seti | kontrol |
| sohbet_modeli | qwen2.5-7b-instruct-cuda-gpu |
| gomme_modeli | qwen3-embedding-0.6b-cuda-gpu |
| top_k | 8 |
| min_score | 0.33 |
| takip_farki | 0.2 |
| max_tokens | 600 |
| parca_sayisi | 86 |
| parcalama | paragraf + baslik yolu, ortusme yok |
| chunk_size | 1000 |
| sorgu_talimati | Soruyu cevaplayan paragrafı bul |
| arama | yalnız vektör |
| cevap_dogrulama | kapalı |
| git | 2ed4700 (kaydedilmemis degisiklik var) |
| set_parmak_izi | bcc0970ce7 |

## Özet

> **Uyarı:** İlk token ortalaması 6.79 sn, 3.0 sn sınırının üstünde. Ekran kartı belleği bozuk düzende olabilir (rag_iyilestirme_plani.md Bölüm 2.5); süre ölçütleri geçersiz sayılmalı. Doğruluk ölçütleri bundan etkilenmez. Sunucuyu yeniden başlatıp (foundry server stop) tekrar ölçün.

Puanlanan soru: 43 (27 cevaplanabilir, 16 cevaplanamaz). Senaryoların hazırlık soruları özete katılmaz.

Karşılaştırılan çalışma: `degerlendirmeler/2026-09-15_0124_kontrol_nihai.json`

| Ölçüt | Önceki | Şimdi |
|---|---|---|
| Tam başarı (tüm puanlanan sorular) | 88.4% | 86.0% |
| Arama: doğru parça 1. sırada (hit@1) | 85.2% | 85.2% |
| Arama: doğru parça ilk 3'te (hit@3) | 88.9% | 88.9% |
| Arama: MRR (1 = hep 1. sırada) | 0.894 | 0.894 |
| Cevaplanabilir sorularda başarı | 88.9% | 92.6% |
| Yanlış red (cevap belgede varken) | 7.4% | 3.7% |
|   bunun eşikte olanı | 0.0% | 0.0% |
| Anahtar ifadelerin tamamı cevapta | 96.0% | 96.2% |
| Bilinen yanlışı içeren cevap | 0 adet | 0 adet |
| Kaynak satırı var | 100.0% | 100.0% |
| Kaynak doğru belge | 100.0% | 100.0% |
| Cevaplanamaz soruları reddetme | 87.5% | 75.0% |
|   bunun eşikte olanı | 0.0% | 0.0% |
| Red cevabına eklenmiş kaynak satırı | 0 adet | 0 adet |
| Doğrulamada reddedilen cevaplanabilir | 0 adet | 0 adet |
| Doğrulamada reddedilen cevaplanamaz | 0 adet | 0 adet |
| Türkçe olmayan yazı kalan cevap | 0 adet | 0 adet |
| Türkçe olmayan yazı kesilen cevap | 1 adet | 1 adet |
| Süre ortalaması | 2.21 sn | 8.06 sn |
| Süre medyanı | 2.17 sn | 10.34 sn |
| En uzun süre | 3.15 sn | 14.75 sn |
| İlk token ortalaması (modele giden sorular) | 0.92 sn | 6.79 sn |
| Arama süresi ortalaması | 0.495 sn | 0.477 sn |

## Kategorilere göre

| Kategori | Soru | Başarılı | hit@1 | hit@3 | Yanlış red |
|---|---|---|---|---|---|
| normal | 15 | 13 | 14 | 15 | 1 |
| ozel_ad | 5 | 5 | 4 | 4 | 0 |
| yakin | 8 | 7 | - | - | - |
| takip | 4 | 4 | 4 | 4 | 0 |
| takip_cevapsiz | 6 | 3 | - | - | - |
| konu_degisimi | 3 | 3 | 1 | 1 | 0 |
| konu_disi_sonra | 2 | 2 | - | - | - |
| hazirlik (puanlanmaz) | 15 | - | - | - | - |

## Önceki çalışmaya göre değişen sorular

Cevap metni değişen soru: 46. Sonucu değişen soru: 7.

- **k-harf-sayisi** HATA → OK: Latin harflerine dayalı yeni Türk alfabesinde kaç harf vardır?
- **k-millet-mektep** OK → HATA: Yeni alfabeye geçişte halka okuma yazma öğretmek için hangi okullar açıldı? (yanlış red (model))
- **k-bildiri** OK → HATA: Alparslan Türkeş 27 Mayıs 1960'ta hangi olayla tanınmıştır? (eksik: bildiri)
- **k-ulus** HATA → OK: Ülüş nedir? (doğru parça ilk 3'te değil (sıra 4))
- **k-cevapsiz-mohac#2** OK → HATA: karşı taraftaki kralın adı neydi? (cevaplanamaz soruya cevap verdi)
- **k-cevapsiz-baskent#2** OK → HATA: başkenti neresiydi? (cevaplanamaz soruya cevap verdi)
- **k-degisim-otag#2** HATA → OK: Otağ nedir? (doğru parça ilk 3'te değil (sıra 5))

## Başarısız sorular

- **k-millet-mektep** (normal) Yeni alfabeye geçişte halka okuma yazma öğretmek için hangi okullar açıldı?
  - Neden: yanlış red (model)
  - Cevap: Bu bilgi elimdeki dokümanlarda yok.
- **k-bildiri** (normal) Alparslan Türkeş 27 Mayıs 1960'ta hangi olayla tanınmıştır?
  - Neden: eksik: bildiri
  - Cevap: Alparslan Türkeş, 27 Mayıs 1960 askerî müdahalesinde radyodan okuyan kişi olarak tanınmıştır. (Kaynak: milliyetci-hareketin-isimleri.md)
- **k-dogu-cephesi** (yakin) Kurtuluş Savaşı'nda Doğu Cephesi komutanı kimdi?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Çanakkale ve Kurtuluş Savaşı sırasında Doğu Cephesi komutanı Mustafa Kemal Atatürk'tü. Batı cephesindeki muharebeler 1921'de yoğunlaşırken, Mustafa Kemal Atatürk, Anafartalar Grubu komutanlığındaki başarısıyla tanınmış ve Çanakkale Savaşları sırasında Arıburnu ve Conkbayırı'ndaki çarpışmaları yönetmiştir. (Kaynak: mustafa-kemal-ataturk.md, canakkale-ve-kurtulus-savasi.md)
- **k-cevapsiz-mohac#2** (takip_cevapsiz) karşı taraftaki kralın adı neydi?
  - Önceki soru: Mohaç Savaşı hangi yıl yapılmıştır?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: IV. Romanos Diogenes (Kaynak: selcuklular-ve-malazgirt.md)
- **k-cevapsiz-baskent#2** (takip_cevapsiz) başkenti neresiydi?
  - Önceki soru: Göktürk Devleti ne zaman kurulmuştur?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Selçukluların başkenti 1077'den itibaren Konya'daydı. (Kaynak: selcuklular-ve-malazgirt.md)
- **k-cevapsiz-uygur#2** (takip_cevapsiz) ne zaman yıkıldı?
  - Önceki soru: Uygur Kağanlığı hangi yıl kurulmuştur?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Osmanlı Padişahları saltanatının kaldırıllığı 1 Kasım 1922'de Türkiye Büyük Millet Meclisi tarafından yapılmıştır. (Kaynak: osmanli-padisahlari.md)

## Tüm sonuçlar

| id | Kategori | Sıra | En iyi skor | Eşikte red | Red | Anahtar | Kaynak | Süre | Sonuç |
|---|---|---|---|---|---|---|---|---|---|
| k-canakkale | normal | 1 | 0.626 |  |  | tam | doğru | 11.5 | OK |
| k-mete | normal | 1 | 0.578 |  |  | tam | doğru | 1.8 | OK |
| k-kutluk | normal | 1 | 0.677 |  |  | tam | doğru | 11.7 | OK |
| k-baba | normal | 1 | 0.747 |  |  | tam | doğru | 2.1 | OK |
| k-murad | normal | 1 | 0.49 |  |  | tam | doğru | 11.3 | OK |
| k-saltanat | normal | 1 | 0.622 |  |  | tam | doğru | 10.2 | OK |
| k-kinik | normal | 1 | 0.66 |  |  | tam | doğru | 11.0 | OK |
| k-malazgirt-onem | normal | 1 | 0.738 |  |  | tam | doğru | 3.3 | OK |
| k-akcura | normal | 1 | 0.793 |  |  | tam | doğru | 2.1 | OK |
| k-harf-sayisi | normal | 1 | 0.793 |  |  | tam | doğru | 2.1 | OK |
| k-millet-mektep | normal | 1 | 0.608 |  | evet |  |  | 8.0 | HATA |
| k-bildiri | normal | 2 | 0.814 |  |  | eksik | doğru | 2.2 | HATA |
| k-veteriner | normal | 1 | 0.81 |  |  | tam | doğru | 1.9 | OK |
| k-kurt-neden | normal | 1 | 0.836 |  |  | tam | doğru | 3.1 | OK |
| k-ad-koyma | normal | 1 | 0.773 |  |  | tam | doğru | 11.3 | OK |
| k-ulus | ozel_ad | 4 | 0.469 |  |  | tam | doğru | 11.2 | OK |
| k-toy | ozel_ad | 1 | 0.406 |  |  | tam | doğru | 10.9 | OK |
| k-manasci | ozel_ad | 1 | 0.534 |  |  | tam | doğru | 2.1 | OK |
| k-ortmece | ozel_ad | 1 | 0.424 |  |  | tam | doğru | 12.6 | OK |
| k-asena | ozel_ad | 1 | 0.433 |  |  | tam | doğru | 9.6 | OK |
| k-bumin-baba | yakin |  | 0.549 |  | evet |  |  | 9.7 | OK |
| k-edirne | yakin |  | 0.576 |  | evet |  |  | 10.5 | OK |
| k-alparslan-olum | yakin |  | 0.591 |  | evet |  |  | 10.9 | OK |
| k-gokalp-olum | yakin |  | 0.707 |  | evet |  |  | 7.6 | OK |
| k-macar-kral | yakin |  | 0.521 |  | evet |  |  | 9.8 | OK |
| k-thomsen-univ | yakin |  | 0.397 |  | evet |  |  | 7.9 | OK |
| k-korkut-hikaye | yakin |  | 0.728 |  | evet |  |  | 1.6 | OK |
| k-dogu-cephesi | yakin |  | 0.662 |  |  |  | var | 13.3 | HATA |
| k-takip-gokalp#1 | hazirlik |  | 0.77 |  |  |  | var | 1.9 | - |
| k-takip-gokalp#2 | takip | 1 | 0.809 |  |  | tam | doğru | 2.4 | OK |
| k-takip-korkut#1 | hazirlik |  | 0.776 |  |  |  | var | 2.0 | - |
| k-takip-korkut#2 | takip | 1 | 0.79 |  |  | tam | doğru | 2.2 | OK |
| k-takip-sam#1 | hazirlik |  | 0.706 |  |  |  | var | 1.9 | - |
| k-takip-sam#2 | takip | 1 | 0.76 |  |  | tam | doğru | 2.2 | OK |
| k-takip-konya#1 | hazirlik |  | 0.721 |  |  |  | var | 11.8 | - |
| k-takip-konya#2 | takip | 1 | 0.74 |  |  | tam | doğru | 9.9 | OK |
| k-cevapsiz-malazgirt#1 | hazirlik |  | 0.663 |  |  |  | var | 2.0 | - |
| k-cevapsiz-malazgirt#2 | takip_cevapsiz |  | 0.419 |  | evet |  |  | 11.9 | OK |
| k-cevapsiz-nutuk#1 | hazirlik |  | 0.503 |  |  |  | var | 11.9 | - |
| k-cevapsiz-nutuk#2 | takip_cevapsiz |  | 0.346 |  | evet |  |  | 10.7 | OK |
| k-cevapsiz-tdk#1 | hazirlik |  | 0.76 |  |  |  | var | 11.4 | - |
| k-cevapsiz-tdk#2 | takip_cevapsiz |  | 0.725 |  | evet |  |  | 11.4 | OK |
| k-cevapsiz-mohac#1 | hazirlik |  | 0.488 |  |  |  | var | 10.9 | - |
| k-cevapsiz-mohac#2 | takip_cevapsiz |  | 0.424 |  |  |  | var | 11.4 | HATA |
| k-cevapsiz-baskent#1 | hazirlik |  | 0.766 |  |  |  | var | 11.2 | - |
| k-cevapsiz-baskent#2 | takip_cevapsiz |  | 0.722 |  |  |  | var | 14.7 | HATA |
| k-cevapsiz-uygur#1 | hazirlik |  | 0.66 |  |  |  | var | 10.7 | - |
| k-cevapsiz-uygur#2 | takip_cevapsiz |  | 0.435 |  |  |  | var | 11.8 | HATA |
| k-degisim-otag#1 | hazirlik |  | 0.485 |  |  |  | var | 11.5 | - |
| k-degisim-otag#2 | konu_degisimi | 5 | 0.45 |  |  | tam | doğru | 12.0 | OK |
| k-degisim-okculuk#1 | hazirlik |  | 0.756 |  |  |  | var | 1.9 | - |
| k-degisim-okculuk#2 | konu_degisimi | 1 | 0.607 |  |  | tam | doğru | 12.0 | OK |
| k-degisim-tugrul#1 | hazirlik |  | 0.69 |  |  |  | var | 2.2 | - |
| k-degisim-tugrul#2 | konu_degisimi | 5 | 0.496 |  |  | tam | doğru | 13.7 | OK |
| k-disi-telefon#1 | hazirlik |  | 0.631 |  |  |  | var | 8.2 | - |
| k-disi-telefon#2 | konu_disi_sonra |  | 0.572 |  | evet |  |  | 8.1 | OK |
| k-disi-yagmur#1 | hazirlik |  | 0.75 |  |  |  | var | 11.5 | - |
| k-disi-yagmur#2 | konu_disi_sonra |  | 0.666 |  | evet |  |  | 10.9 | OK |

## Cevaplar (gözle kontrol için)

**k-canakkale** — Çanakkale'de İtilaf Devletleri neyi amaçlıyordu?
> İtilaf Devletleri, Çanakkale'de boğazı geçip İstanbul'a ulaşmayı ve Rusya'ya ulaşım hattı açmayı amaçlamıştır. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#0 0.626 | canakkale-ve-kurtulus-savasi.md#1 0.548 | turk-devlet-gelenegi.md#3 0.488 | selcuklular-ve-malazgirt.md#3 0.484 | turk-milliyetciliginin-dogusu.md#0 0.446`

**k-mete** — Mete Han Çin kaynaklarında hangi adla anılır?
> Mete Han Çin kaynaklarında Modu Chanyu adıyla anılır. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#0 0.578 | turk-kulturunde-kurt.md#1 0.395`

**k-kutluk** — İkinci Göktürk Devleti'ni kim, hangi yılda kurmuştur?
> İkinci Göktürk Devleti'ni İlteriş Kutluk Kağan, 682'de kurmuştur. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#1 0.677 | ilk-turk-devletleri.md#4 0.557 | turk-kulturunde-kurt.md#1 0.498 | turk-milliyetciliginin-dogusu.md#2 0.485 | turk-milliyetciliginin-dogusu.md#0 0.485`

**k-baba** — Mustafa Kemal'in babası kimdir, hangi işleri yapmıştır?
> Mustafa Kemal'in babası Ali Rıza Efendi'dir ve gümrük memurluğu ve kereste ticareti yapmıştır. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#0 0.747 | mustafa-kemal-ataturk.md#1 0.631`

**k-murad** — I. Murad'ın hayatı nasıl sona ermiştir?
> I. Murad 1389'daki I. Kosova Savaşı'nı kazanmış ancak savaş alanında öldürülmüştür. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#1 0.490 | osmanli-padisahlari.md#4 0.447 | mustafa-kemal-ataturk.md#6 0.445 | milliyetci-hareketin-isimleri.md#10 0.382 | mustafa-kemal-ataturk.md#5 0.379`

**k-saltanat** — Osmanlı saltanatı ne zaman ve kim tarafından kaldırılmıştır?
> Osmanlı saltanatı 1 Kasım 1922'de Türkiye Büyük Millet Meclisi tarafından kaldırılmıştır. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#4 0.622 | osmanli-padisahlari.md#3 0.588 | selcuklular-ve-malazgirt.md#4 0.526 | selcuklular-ve-malazgirt.md#0 0.512`

**k-kinik** — Büyük Selçuklu hanedanı hangi Oğuz boyundan gelir?
> Büyük Selçuklu hanedanı Oğuzların Kınık boyundan gelir. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#0 0.660 | turk-destanlari.md#1 0.576 | osmanli-padisahlari.md#3 0.557 | osmanli-padisahlari.md#1 0.552 | selcuklular-ve-malazgirt.md#4 0.551`

**k-malazgirt-onem** — Malazgirt Savaşı Anadolu'nun tarihi açısından neden önemlidir?
> Malazgirt Savaşı Anadolu'nun tarihi açısından önemlidir çünkü savaşın ardından Bizans'ın Anadolu savunma düzeni çökmüş ve Türkmen boyları Anadolu içlerine doğru yerleşmeye başlamıştır. Bu süreç, Anadolu'nun Türkleşme sürecinin başlangıcı olarak kabul edilir ve Bizans İmparatorluğu'nun Anadolu bölgelerindeki kontrolünün zayıflamasına neden olmuştur. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#2 0.738 | selcuklular-ve-malazgirt.md#1 0.671`

**k-akcura** — Yusuf Akçura yazısında hangi siyaset biçimlerini karşılaştırmıştır?
> Yusuf Akçura yazısında Osmanlıcılık, İslamcılık ve Türkçülük olmak üzere üç siyaset biçimini karşılaştırmıştır. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#1 0.793 | ulku-ocaklari.md#3 0.510`

**k-harf-sayisi** — Latin harflerine dayalı yeni Türk alfabesinde kaç harf vardır?
> Türkçenin yeni Latin alfabesinde toplam yirmi dokuz harf bulunur. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#3 0.793 | turkcenin-tarihi-ve-alfabeleri.md#4 0.661`

**k-millet-mektep** — Yeni alfabeye geçişte halka okuma yazma öğretmek için hangi okullar açıldı?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#3 0.608 | turkcenin-tarihi-ve-alfabeleri.md#4 0.541 | ilk-turk-devletleri.md#3 0.477`

**k-bildiri** — Alparslan Türkeş 27 Mayıs 1960'ta hangi olayla tanınmıştır?
> Alparslan Türkeş, 27 Mayıs 1960 askerî müdahalesinde radyodan okuyan kişi olarak tanınmıştır. (Kaynak: milliyetci-hareketin-isimleri.md)

Getirilen: `milliyetci-hareketin-isimleri.md#6 0.814 | milliyetci-hareketin-isimleri.md#7 0.643`

**k-veteriner** — Muhsin Yazıcıoğlu hangi fakülteden mezun olmuştur?
> Muhsin Yazıcıoğlu Ankara Üniversitesi Veteriner Fakültesi'nden mezun olmuştur. (Kaynak: milliyetci-hareketin-isimleri.md)

Getirilen: `milliyetci-hareketin-isimleri.md#12 0.810 | milliyetci-hareketin-isimleri.md#15 0.612`

**k-kurt-neden** — Türk kültüründe sembol olarak neden kurt seçilmiştir?
> Türk kültüründe kurt sembol olarak seçilmesinin nedeni, kurtun sürü hâlinde yaşaması, dayanıklılığı ve evcilleşmemesi ile bozkır topluluklarının kendilerini tanımlamak için hayvan sembolleri kullanımına sahip olmasıdır. Ayrıca, kurt figürü, özellikle Göktürklerde siyasi sembolizme de yansımanın yanı sıra, modern dönemde Türk milliyetçiliğinde de önemli bir görsel işaret haline gelmiştir. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#4 0.836 | turk-kulturunde-kurt.md#3 0.806`

**k-ad-koyma** — Dede Korkut hikâyelerindeki ad koyma geleneği nasıldır?
> Dede Korkut hikâyelerinde bir gencin ad alabilmek için önce bir yiğitlik göstermesi gerekmektedir. Bu geleneğin en bilinen örneği, bir gencin yalnızca yiğitlik göstererek ad alabildiğidır. Bu ad koyma geleneği, hikâyelerde kahramanlık ve aile bağlarını vurgulamak için kullanılır. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.773 | turk-kulturunde-at.md#4 0.617 | turk-kulturunde-kurt.md#6 0.577 | turk-kulturunde-kurt.md#5 0.552`

**k-ulus** — Ülüş nedir?
> Ülüş, ganimetin ve gelirin boylar arasında paylandırılmasının geleneğidir ve hükümdarın cömertliği yöneticilik erdemlerinden birisidir. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-kulturunde-at.md#2 0.469 | ulku-ocaklari.md#0 0.460 | ulku-ocaklari.md#4 0.419 | turk-devlet-gelenegi.md#4 0.412 | turkcenin-tarihi-ve-alfabeleri.md#1 0.396`

**k-toy** — Toy nedir?
> Toy, Kurultay ya da devletin önemli kararlarının alındığı meclisdir. Burada savaş, barış ve hükümdar seçimi gibi konular görüşülürdü ve kararlar tartışılarak alındı. Bu yapı, Türk devletlerinde yönetimin tek kişinin keyfine bırakılmadığını gösteren en belirgin unsurdur. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#2 0.406 | turk-kulturunde-at.md#0 0.363 | turk-devlet-gelenegi.md#1 0.349 | turk-kulturunde-kurt.md#6 0.327 | turk-kulturunde-kurt.md#0 0.323`

**k-manasci** — Manasçı kimdir?
> Manasçı, sözlü olarak Manas Destanı anlatarak ve kahramanın ve soyundan gelenlerin mücadelelerini anlatarak kuşaktan kuşağa aktarılan anlatıcılar anlamına gelir. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#3 0.534 | mustafa-kemal-ataturk.md#0 0.326`

**k-ortmece** — Örtmece nedir?
> Örtmece, korkulan ya da saygı duyulan bir varlığın gerçek adını söylemekten kaçınılıp, daha aptallık veya zayıflığa atıfta bulunacak bir başka sözcük kullanmakla ifade edilir. Bu yöntem, kurtçuk gibi zayıf canlıların adı, böri yerine "kurt" olarak değiştirilmesi gibi durumlarda görülebilir. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#6 0.424 | turkcenin-tarihi-ve-alfabeleri.md#0 0.368 | turk-kulturunde-at.md#3 0.367 | turk-kulturunde-kurt.md#2 0.359 | turk-kulturunde-at.md#1 0.341`

**k-asena** — Asena nedir?
> Asena, "Aşina"nın Türkçe'deki modern okunuşudur ve Türk kültüründe Kurt hanedanının adı olarak kullanılmaktadır. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#1 0.433 | milliyetci-hareketin-isimleri.md#20 0.421 | turk-kulturunde-at.md#3 0.359 | turk-kulturunde-at.md#0 0.354`

**k-bumin-baba** — Bumin Kağan'ın babasının adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-destanlari.md#1 0.549 | mustafa-kemal-ataturk.md#0 0.458 | milliyetci-hareketin-isimleri.md#19 0.437 | osmanli-padisahlari.md#1 0.417 | turk-destanlari.md#3 0.417`

**k-edirne** — Osmanlı başkenti Edirne'ye ne zaman taşınmıştır?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-padisahlari.md#0 0.576 | osmanli-padisahlari.md#2 0.544 | mustafa-kemal-ataturk.md#6 0.514 | mustafa-kemal-ataturk.md#4 0.513 | canakkale-ve-kurtulus-savasi.md#2 0.490`

**k-alparslan-olum** — Sultan Alparslan hangi yıl ölmüştür?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `milliyetci-hareketin-isimleri.md#6 0.591 | selcuklular-ve-malazgirt.md#1 0.541 | osmanli-padisahlari.md#4 0.541 | osmanli-padisahlari.md#0 0.535 | selcuklular-ve-malazgirt.md#0 0.491`

**k-gokalp-olum** — Ziya Gökalp hangi şehirde vefat etmiştir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-milliyetciliginin-dogusu.md#2 0.707 | milliyetci-hareketin-isimleri.md#15 0.547 | mustafa-kemal-ataturk.md#6 0.499`

**k-macar-kral** — Mohaç Savaşı'nda yenilen Macar kralının adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-padisahlari.md#4 0.521 | selcuklular-ve-malazgirt.md#4 0.486 | selcuklular-ve-malazgirt.md#1 0.469 | osmanli-padisahlari.md#1 0.440`

**k-thomsen-univ** — Vilhelm Thomsen hangi üniversitede çalışıyordu?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `ilk-turk-devletleri.md#3 0.397 | mustafa-kemal-ataturk.md#1 0.386 | mustafa-kemal-ataturk.md#5 0.321`

**k-korkut-hikaye** — Dede Korkut Kitabı'ndaki ilk hikâyenin adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-destanlari.md#4 0.728 | turk-kulturunde-at.md#4 0.558`

**k-dogu-cephesi** — Kurtuluş Savaşı'nda Doğu Cephesi komutanı kimdi?
> Çanakkale ve Kurtuluş Savaşı sırasında Doğu Cephesi komutanı Mustafa Kemal Atatürk'tü. Batı cephesindeki muharebeler 1921'de yoğunlaşırken, Mustafa Kemal Atatürk, Anafartalar Grubu komutanlığındaki başarısıyla tanınmış ve Çanakkale Savaşları sırasında Arıburnu ve Conkbayırı'ndaki çarpışmaları yönetmiştir. (Kaynak: mustafa-kemal-ataturk.md, canakkale-ve-kurtulus-savasi.md)

Getirilen: `mustafa-kemal-ataturk.md#3 0.662 | canakkale-ve-kurtulus-savasi.md#1 0.552 | canakkale-ve-kurtulus-savasi.md#3 0.528 | mustafa-kemal-ataturk.md#1 0.491 | milliyetci-hareketin-isimleri.md#7 0.481`

**k-takip-gokalp#1** — Ziya Gökalp nerede doğmuştur?
> Ziya Gökalp, 1876'da Diyarbakır'da doğmuştur. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#2 0.770 | milliyetci-hareketin-isimleri.md#12 0.499`

**k-takip-gokalp#2** — hangi formülü savunmuştur?  
_Önceki soru: Ziya Gökalp nerede doğmuştur?_
> Ziya Gökalp "Türkleşmek, İslamlaşmak, Muasırlaşmak" formülünü savunmuştur. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#2 0.809 | turk-milliyetciliginin-dogusu.md#3 0.507`

**k-takip-korkut#1** — Dede Korkut Kitabı kaç hikâyeden oluşur?
> Dede Korkut Kitabı, Oğuzların İslam sonrası dönemine ait on iki hikâyeden oluşur. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.776 | turk-kulturunde-at.md#4 0.575`

**k-takip-korkut#2** — yazmaları nerede bulunuyor?  
_Önceki soru: Dede Korkut Kitabı kaç hikâyeden oluşur?_
> Yazmaları Dresden ve Vatikan'da bulunuyor. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.790 | turk-kulturunde-at.md#4 0.583`

**k-takip-sam#1** — Mustafa Kemal Harp Akademisi'ni hangi yıl bitirmiştir?
> Mustafa Kemal Atatürk Harp Akademisi'ni 1905'te bitirmiştir. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#1 0.706 | mustafa-kemal-ataturk.md#6 0.599`

**k-takip-sam#2** — ilk görev yeri neresiydi?  
_Önceki soru: Mustafa Kemal Harp Akademisi'ni hangi yıl bitirmiştir?_
> İlk görev yeri Şam'daki 5. Ordu olmuştur. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#1 0.760 | mustafa-kemal-ataturk.md#6 0.594`

**k-takip-konya#1** — Anadolu Selçuklu Devleti'nin ilk merkezi neresiydi?
> Selçuklular ve ve Malazgirt Savaşı'ndan göre, Anadolu Selçuklu Devleti'nin ilk merkezi İznik'te yer almaktadır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#3 0.721 | selcuklular-ve-malazgirt.md#2 0.627 | canakkale-ve-kurtulus-savasi.md#2 0.556 | ilk-turk-devletleri.md#1 0.532 | ilk-turk-devletleri.md#0 0.529`

**k-takip-konya#2** — başkenti daha sonra nereye taşındı?  
_Önceki soru: Anadolu Selçuklu Devleti'nin ilk merkezi neresiydi?_
> Anadolu Selçuklu Devleti'nin başkenti daha sonra Konya'ya taşınmıştır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#3 0.740 | selcuklular-ve-malazgirt.md#2 0.625 | osmanli-padisahlari.md#3 0.558 | canakkale-ve-kurtulus-savasi.md#2 0.550`

**k-cevapsiz-malazgirt#1** — Malazgirt Savaşı ne zaman yapılmıştır?
> Malazgirt Savaşı 26 Ağustos 1071'de yapılmıştır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.663 | selcuklular-ve-malazgirt.md#2 0.660`

**k-cevapsiz-malazgirt#2** — savaşta kaç kişi öldü?  
_Önceki soru: Malazgirt Savaşı ne zaman yapılmıştır?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `canakkale-ve-kurtulus-savasi.md#0 0.419 | milliyetci-hareketin-isimleri.md#15 0.386 | selcuklular-ve-malazgirt.md#1 0.381 | selcuklular-ve-malazgirt.md#2 0.375 | turk-kulturunde-at.md#1 0.375`

**k-cevapsiz-nutuk#1** — Nutuk ne zaman okunmuştur?
> Mustafa Kemal Atatürk, 15-20 Ekim 1927 tarihleri arasında Cumhuriyet Halk Partisi kongresinde Nutuk adlı konuşmasını okumuştur. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#5 0.503 | ilk-turk-devletleri.md#3 0.384 | ulku-ocaklari.md#0 0.368 | milliyetci-hareketin-isimleri.md#1 0.362 | turk-milliyetciliginin-dogusu.md#4 0.360`

**k-cevapsiz-nutuk#2** — kaç sayfadır?  
_Önceki soru: Nutuk ne zaman okunmuştur?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-destanlari.md#3 0.346 | turkcenin-tarihi-ve-alfabeleri.md#0 0.335 | turk-destanlari.md#1 0.320 | turk-milliyetciliginin-dogusu.md#1 0.311 | turkcenin-tarihi-ve-alfabeleri.md#1 0.301`

**k-cevapsiz-tdk#1** — Türk Dil Kurumu ne zaman kurulmuştur?
> Türk Dil Kurumu, 12 Temmuz 1932'de kurulan Türk Dili Tetkik Cemiyeti olarak başlamış ve bugün faaliyet göstermektedir. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.760 | turkcenin-tarihi-ve-alfabeleri.md#4 0.760 | turkcenin-tarihi-ve-alfabeleri.md#3 0.626 | ilk-turk-devletleri.md#1 0.594 | ulku-ocaklari.md#0 0.589`

**k-cevapsiz-tdk#2** — ilk başkanı kimdi?  
_Önceki soru: Türk Dil Kurumu ne zaman kurulmuştur?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#4 0.725 | turk-milliyetciliginin-dogusu.md#4 0.703 | ilk-turk-devletleri.md#1 0.621 | turkcenin-tarihi-ve-alfabeleri.md#3 0.615 | ilk-turk-devletleri.md#3 0.606`

**k-cevapsiz-mohac#1** — Mohaç Savaşı hangi yıl yapılmıştır?
> Mohaç Savaşı 1526 yılında yapılmıştır. (Kaynak: osmanli-padisahlari.md)

Getirilen: `selcuklular-ve-malazgirt.md#4 0.488 | selcuklular-ve-malazgirt.md#0 0.454 | osmanli-padisahlari.md#4 0.435 | canakkale-ve-kurtulus-savasi.md#3 0.430 | canakkale-ve-kurtulus-savasi.md#4 0.423`

**k-cevapsiz-mohac#2** — karşı taraftaki kralın adı neydi?  
_Önceki soru: Mohaç Savaşı hangi yıl yapılmıştır?_
> IV. Romanos Diogenes (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `osmanli-padisahlari.md#1 0.424 | turk-devlet-gelenegi.md#0 0.415 | osmanli-padisahlari.md#4 0.410 | selcuklular-ve-malazgirt.md#1 0.401 | turk-devlet-gelenegi.md#2 0.387`

**k-cevapsiz-baskent#1** — Göktürk Devleti ne zaman kurulmuştur?
> Göktürk Devleti 552 yılında kurulmuştur. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#1 0.766 | ilk-turk-devletleri.md#4 0.670 | turk-milliyetciliginin-dogusu.md#4 0.602 | turk-milliyetciliginin-dogusu.md#0 0.585 | turk-devlet-gelenegi.md#0 0.570`

**k-cevapsiz-baskent#2** — başkenti neresiydi?  
_Önceki soru: Göktürk Devleti ne zaman kurulmuştur?_
> Selçukluların başkenti 1077'den itibaren Konya'daydı. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `ilk-turk-devletleri.md#1 0.722 | ilk-turk-devletleri.md#4 0.639 | turk-milliyetciliginin-dogusu.md#4 0.573 | selcuklular-ve-malazgirt.md#3 0.562 | selcuklular-ve-malazgirt.md#0 0.562`

**k-cevapsiz-uygur#1** — Uygur Kağanlığı hangi yıl kurulmuştur?
> Uygur Kağanlığı 744'te kurulmuştur. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#4 0.660 | turkcenin-tarihi-ve-alfabeleri.md#1 0.558 | ulku-ocaklari.md#0 0.549 | turk-destanlari.md#1 0.524 | milliyetci-hareketin-isimleri.md#17 0.522`

**k-cevapsiz-uygur#2** — ne zaman yıkıldı?  
_Önceki soru: Uygur Kağanlığı hangi yıl kurulmuştur?_
> Osmanlı Padişahları saltanatının kaldırıllığı 1 Kasım 1922'de Türkiye Büyük Millet Meclisi tarafından yapılmıştır. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#4 0.435 | osmanli-padisahlari.md#0 0.403 | selcuklular-ve-malazgirt.md#4 0.398 | ulku-ocaklari.md#2 0.395 | milliyetci-hareketin-isimleri.md#15 0.382`

**k-degisim-otag#1** — Lozan Antlaşması ne zaman imzalanmıştır?
> Lozan Antlaşması 24 Temmuz 1923'te imzalanmıştır. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#4 0.485 | canakkale-ve-kurtulus-savasi.md#2 0.391 | osmanli-padisahlari.md#0 0.382 | osmanli-padisahlari.md#1 0.365 | selcuklular-ve-malazgirt.md#0 0.362`

**k-degisim-otag#2** — Otağ nedir?  
_Önceki soru: Lozan Antlaşması ne zaman imzalanmıştır?_
> Otağ, Türk devlet geleneğinde hüküm süren bir semboldür. Bu sembol, at kılından yapılmış ve sırık üzerinde taşınan bir bayrak niteliğindedir. Otağın sayısı hüküm süren kişinin rütbesine göre değişebilir. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-destanlari.md#1 0.450 | turk-kulturunde-at.md#0 0.425 | turk-kulturunde-at.md#1 0.409 | turk-devlet-gelenegi.md#4 0.372 | turkcenin-tarihi-ve-alfabeleri.md#1 0.363`

**k-degisim-okculuk#1** — Orhun Yazıtları kimler adına dikilmiştir?
> Orhun Yazıtları, vezir Tonyukuk, Kül Tigin ve Bilge Kağan adına dikilmiştir. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#2 0.756 | turkcenin-tarihi-ve-alfabeleri.md#0 0.613`

**k-degisim-okculuk#2** — Atlı okçuluk nedir?  
_Önceki soru: Orhun Yazıtları kimler adına dikilmiştir?_
> Atlı okçuluk, dörtnala giderken ok atabilme becerisi ile ağır piyadeye karşı hareket üstünlüğü sağlanan askerî bir yöntemdir. Bu teknik, Turan taktiği adıyla bilinen yöntemde kullanılır: merkez birlikler sahte bir geri çekilme yapar, düşman takibe geçince kanatlar hilal biçiminde kapanarak kuşatma tamamlanır. Malazgirt Savaşı'nda da bu taktik uygulanmıştır. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#1 0.607 | turk-kulturunde-at.md#0 0.505 | ulku-ocaklari.md#0 0.444`

**k-degisim-tugrul#1** — Yusuf Akçura'nın yazısı nerede yayımlanmıştır?
> Yusuf Akçura'nın "Üç Tarz-ı Siyaset" başlıklı yazısı 1904'te Kahire'de yayımlanmıştır. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#1 0.690 | turk-milliyetciliginin-dogusu.md#4 0.436`

**k-degisim-tugrul#2** — Tuğrul Bey kimdir?  
_Önceki soru: Yusuf Akçura'nın yazısı nerede yayımlanmıştır?_
> Tuğrul Bey, Büyük Selçuklu Devleti'nin ilk sultanıdır. Devletin kuruluşunu 1040 yılındaki Dandanakan Savaşı'da kesinleştiren olayla ilgili olarak, Gazneli ordusunu yenmiş ve Horasan bölgesi Selçukluların eline geçmiş olan olayda da öncülkü yapmıştır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.496 | turk-devlet-gelenegi.md#4 0.490 | turk-destanlari.md#1 0.473 | turk-devlet-gelenegi.md#2 0.471 | selcuklular-ve-malazgirt.md#0 0.466`

**k-disi-telefon#1** — Kurultayda hangi kararlar alınırdı?
> Kurultayda savaş, barış ve hükümdar seçimi gibi konular görüşülürdü ve kararlar tartışılarak alındı. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#2 0.631 | turk-kulturunde-kurt.md#2 0.570 | turk-kulturunde-kurt.md#4 0.536`

**k-disi-telefon#2** — En iyi akıllı telefon hangisidir?  
_Önceki soru: Kurultayda hangi kararlar alınırdı?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-devlet-gelenegi.md#2 0.572 | turk-kulturunde-kurt.md#2 0.494 | turk-kulturunde-kurt.md#6 0.493`

**k-disi-yagmur#1** — Türk Ocağı ne zaman kurulmuştur?
> Türk Ocağı 25 Mart 1912'de kurulmuştur. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.750 | ulku-ocaklari.md#0 0.669 | ulku-ocaklari.md#2 0.664 | ilk-turk-devletleri.md#1 0.603 | selcuklular-ve-malazgirt.md#0 0.580`

**k-disi-yagmur#2** — Yarın İstanbul'da yağmur yağacak mı?  
_Önceki soru: Türk Ocağı ne zaman kurulmuştur?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.666 | ulku-ocaklari.md#0 0.632 | ulku-ocaklari.md#2 0.624 | osmanli-padisahlari.md#0 0.520 | ilk-turk-devletleri.md#4 0.518`

