# Değerlendirme: 2026-09-19 03:35 — ilk-olcum

| Ayar | Değer |
|---|---|
| soru_seti | kontrol2 |
| sohbet_modeli | qwen2.5-7b-instruct-cuda-gpu |
| gomme_modeli | qwen3-embedding-0.6b-cuda-gpu |
| top_k | 8 |
| min_score | 0.33 |
| takip_farki | 0.2 |
| max_tokens | 600 |
| parca_sayisi | 219 |
| parcalama | paragraf + baslik yolu, ortusme yok |
| chunk_size | 1000 |
| sorgu_talimati | Soruyu cevaplayan paragrafı bul |
| arama | yalnız vektör |
| cevap_dogrulama | kapalı |
| git | c375b15 (kaydedilmemis degisiklik var) |
| set_parmak_izi | 6d45697d02 |

## Özet

> **Uyarı:** İlk token ortalaması 3.17 sn, 3.0 sn sınırının üstünde. Ekran kartı belleği bozuk düzende olabilir (rag_iyilestirme_plani.md Bölüm 2.5); süre ölçütleri geçersiz sayılmalı. Doğruluk ölçütleri bundan etkilenmez. Sunucuyu yeniden başlatıp (foundry server stop) tekrar ölçün.

Puanlanan soru: 51 (36 cevaplanabilir, 15 cevaplanamaz). Senaryoların hazırlık soruları özete katılmaz.

| Ölçüt | Değer |
|---|---|
| Tam başarı (tüm puanlanan sorular) | 76.5% |
| Arama: doğru parça 1. sırada (hit@1) | 72.2% |
| Arama: doğru parça ilk 3'te (hit@3) | 83.3% |
| Arama: MRR (1 = hep 1. sırada) | 0.788 |
| Cevaplanabilir sorularda başarı | 80.6% |
| Yanlış red (cevap belgede varken) | 11.1% |
|   bunun eşikte olanı | 0.0% |
| Anahtar ifadelerin tamamı cevapta | 90.6% |
| Bilinen yanlışı içeren cevap | 0 adet |
| Kaynak satırı var | 100.0% |
| Kaynak doğru belge | 93.8% |
| Cevaplanamaz soruları reddetme | 66.7% |
|   bunun eşikte olanı | 6.7% |
| Red cevabına eklenmiş kaynak satırı | 0 adet |
| Doğrulamada reddedilen cevaplanabilir | 0 adet |
| Doğrulamada reddedilen cevaplanamaz | 0 adet |
| Türkçe olmayan yazı kalan cevap | 0 adet |
| Türkçe olmayan yazı kesilen cevap | 0 adet |
| Süre ortalaması | 4.38 sn |
| Süre medyanı | 3.77 sn |
| En uzun süre | 10.78 sn |
| İlk token ortalaması (modele giden sorular) | 3.17 sn |
| Arama süresi ortalaması | 0.447 sn |

## Kategorilere göre

| Kategori | Soru | Başarılı | hit@1 | hit@3 | Yanlış red |
|---|---|---|---|---|---|
| normal | 27 | 24 | 21 | 24 | 1 |
| ozel_ad | 2 | 2 | 2 | 2 | 0 |
| yakin | 6 | 3 | - | - | - |
| konu_disi | 3 | 3 | - | - | - |
| anlamsiz | 1 | 1 | - | - | - |
| takip | 4 | 2 | 2 | 3 | 1 |
| takip_cevapsiz | 3 | 1 | - | - | - |
| konu_degisimi | 3 | 1 | 1 | 1 | 2 |
| konu_disi_sonra | 2 | 2 | - | - | - |
| hazirlik (puanlanmaz) | 12 | - | - | - | - |

## Başarısız sorular

- **k2-nevruz-bm** (normal) Birleşmiş Milletler 21 Mart'ı ne ilan etmiştir?
  - Neden: yanlış red (model); doğru parça ilk 3'te değil (sıra 25)
  - Cevap: Bu bilgi elimdeki dokümanlarda yok.
- **k2-uygur-matbaa** (normal) Uygurlar metin çoğaltmak için hangi tekniği kullanmıştır?
  - Neden: eksik: matbaa; yanlış kaynak: turkcenin-tarihi-ve-alfabeleri.md; doğru parça ilk 3'te değil (sıra 10)
  - Cevap: Uygurlar metin çoğaltmak için ağaç baskı tekniğini kullanmıştır. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)
- **k2-fetret** (normal) Fetret Devri kaç yıl sürmüştür?
  - Neden: eksik: on bir|11; yanlış kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md; doğru parça ilk 3'te değil (sıra 6)
  - Cevap: Fetret Devri, Yıldırım Bayezid'in Timur'a yenilmesi ve hâkimiyetinin dağılmasıyla başlayarak 1402 yılından itibaren ve Karamanoğulları'na Fatih Sultan Mehmed döneminde son verilmesine kadar, yani 1417 yılına kadar sürmüştür. Fetret Devri'nin ardından birlik adım adım yeniden sağlanmıştır. (Kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md)
- **k2-cevapsiz-sinan-sayi** (yakin) Mimar Sinan tam olarak kaç yapı inşa etmiştir?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Mimar Sinan'in tam olarak kaç yapı inşa ettiğinden kesin bir sayı verilemiyor, ancak kayıtlara göre yüzlerce yapıyı inşa ettiğini biliyoruz. Özellikle Süleymaniye Camii ve Selimiye Camii gibi önemli yapıları inşa ettiği bilinmektedir. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)
- **k2-cevapsiz-akif-mezar** (yakin) Mehmet Âkif Ersoy nereye gömülmüştür?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Mehmet Âkif Ersoy'nün gömüldüğü yer hakkında bilgi bulunmamaktadır. (Kaynak: milli-semboller.md)
- **k2-cevapsiz-pecenek-nufus** (yakin) Peçeneklerin nüfusu ne kadardı?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Bu bilgi elimdeki dok dokümanlarda yok. (Kaynak: bozkir-gocebe-yasami.md)
- **k2-takip-sinan#2** (takip) nerede bulunuyor?
  - Önceki soru: Mimar Sinan ustalık eseri olarak hangi yapıyı göstermiştir?
  - Neden: eksik: Edirne
  - Cevap: Mimar Sinan'nın yaşam ve çalışmalarının önemli kısmında, Kayseri'nin Ağırnas köyünde doğmuş olduğu belirtiliyor. Ayrıca, Mimar Sinan'ın yapıtlarının üç aşamasını gösteren Süleymaniye Camii'nin inşaat yıllarının da verildiği parçalar 6 ve 6'ta anlatılıyor. Bu bilgilerin bulunduğu yerler, dosya.md içinde belirtilmiştir. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)
- **k2-takip-akif#2** (takip) hangi dergide yazardı?
  - Önceki soru: İstiklal Marşı'nın şairi kimdir?
  - Neden: yanlış red (model); doğru parça ilk 3'te değil (sıra 31)
  - Cevap: Bu bilgi elimdeki dokümanlarda yok.
- **k2-cevapsiz-takip-sinan#2** (takip_cevapsiz) kaç yaşında öldü?
  - Önceki soru: Mimar Sinan hangi padişahlar döneminde çalışmıştır?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Mimar Sinan 1588 yılında ölmüş ve kayıtlara göre onun yaşam süresi yaklaşık 50-60 yaş aralığında olup, bu da onun ölüm tarihi 1588 ile doğum tarihi arasındaki farkı ifade eder. Ancak tam bir yaşı belirtilmemiştir. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)
- **k2-cevapsiz-takip-kadi#2** (takip_cevapsiz) kaç yıl görev yapardı?
  - Önceki soru: Osmanlı'da kadı ne iş yapardı?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Mimar Sinan, Mimarbaşılık görevinde yaklaşık elli yıla yakın süre görev yaptı. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)
- **k2-degisim-balbal#2** (konu_degisimi) Balbal nedir?
  - Önceki soru: Barbaros Hayreddin Paşa nerede doğmuştur?
  - Neden: yanlış red (model); doğru parça ilk 3'te değil (sıra 106)
  - Cevap: Bu bilgi elimdeki dokümanlarda yok.
- **k2-degisim-semeni#2** (konu_degisimi) Semeni nedir?
  - Önceki soru: Mimar Sinan ne zaman ölmüştür?
  - Neden: yanlış red (model); doğru parça ilk 3'te değil (sıra 71)
  - Cevap: Bu bilgi elimdeki dokümanlarda yok.

## Tüm sonuçlar

| id | Kategori | Sıra | En iyi skor | Eşikte red | Red | Anahtar | Kaynak | Süre | Sonuç |
|---|---|---|---|---|---|---|---|---|---|
| k2-beylik-konum | normal | 1 | 0.805 |  |  | tam | doğru | 4.2 | OK |
| k2-asistan-internet | normal | 1 | 0.64 |  |  | tam | doğru | 2.2 | OK |
| k2-juanjuan | normal | 1 | 0.698 |  |  | tam | doğru | 2.2 | OK |
| k2-kirgizistan | normal | 1 | 0.698 |  |  | tam | doğru | 2.1 | OK |
| k2-kuvayi | normal | 1 | 0.503 |  |  | tam | doğru | 2.2 | OK |
| k2-ilk-anayasa | normal | 1 | 0.654 |  |  | tam | doğru | 2.5 | OK |
| k2-dlt-harita | normal | 1 | 0.731 |  |  | tam | doğru | 2.3 | OK |
| k2-akif-meslek | normal | 1 | 0.817 |  |  | tam | doğru | 1.6 | OK |
| k2-sofya | normal | 2 | 0.652 |  |  | tam | doğru | 2.4 | OK |
| k2-nevruz-bm | normal | 25 | 0.547 |  | evet |  |  | 2.0 | HATA |
| k2-avar | normal | 2 | 0.543 |  |  | tam | doğru | 2.1 | OK |
| k2-kadi | ozel_ad | 1 | 0.771 |  |  | tam | doğru | 2.6 | OK |
| k2-kafes | ozel_ad | 1 | 0.517 |  |  | tam | doğru | 2.5 | OK |
| k2-mehter-calgi | normal | 1 | 0.646 |  |  | tam | doğru | 2.0 | OK |
| k2-sinan-dogum | normal | 1 | 0.746 |  |  | tam | doğru | 1.8 | OK |
| k2-barbaros-cezayir | normal | 1 | 0.773 |  |  | tam | doğru | 1.7 | OK |
| k2-saka-destan | normal | 1 | 0.714 |  |  | tam | doğru | 2.0 | OK |
| k2-biruni-dil | normal | 1 | 0.677 |  |  | tam | doğru | 1.8 | OK |
| k2-kurt-tug | normal | 1 | 0.731 |  |  | tam | doğru | 2.3 | OK |
| k2-kutsal-sayi | normal | 1 | 0.772 |  |  | tam | doğru | 3.2 | OK |
| k2-karahanli-bolunme | normal | 1 | 0.689 |  |  | tam | doğru | 2.2 | OK |
| k2-uygur-matbaa | normal | 10 | 0.614 |  |  | eksik | yanlış | 1.9 | HATA |
| k2-miryokefalon | normal | 1 | 0.484 |  |  | tam | doğru | 2.5 | OK |
| k2-kut-soy | normal | 2 | 0.545 |  |  | tam | doğru | 4.1 | OK |
| k2-uygur-alfabe | normal | 1 | 0.752 |  |  | tam | doğru | 3.6 | OK |
| k2-fetret | normal | 6 | 0.563 |  |  | eksik | yanlış | 10.4 | HATA |
| k2-ahal-teke | normal | 1 | 0.528 |  |  | tam | doğru | 8.9 | OK |
| k2-turk-yurdu | normal | 1 | 0.74 |  |  | tam | doğru | 6.6 | OK |
| k2-sened | normal | 1 | 0.517 |  |  | tam | doğru | 9.3 | OK |
| k2-cevapsiz-sinan-sayi | yakin |  | 0.716 |  |  |  | var | 10.1 | HATA |
| k2-cevapsiz-barbaros-dogum | yakin |  | 0.794 |  | evet |  |  | 3.7 | OK |
| k2-cevapsiz-akif-mezar | yakin |  | 0.773 |  |  |  | var | 3.8 | HATA |
| k2-cevapsiz-pecenek-nufus | yakin |  | 0.476 |  |  |  | var | 4.3 | HATA |
| k2-cevapsiz-biruni-ogrenci | yakin |  | 0.698 |  | evet |  |  | 3.3 | OK |
| k2-cevapsiz-kadi-maas | yakin |  | 0.578 |  | evet |  |  | 4.4 | OK |
| k2-disi-corba | konu_disi |  | 0.442 |  | evet |  |  | 4.2 | OK |
| k2-disi-dolar | konu_disi |  | 0.393 |  | evet |  |  | 3.0 | OK |
| k2-disi-kod | konu_disi |  | 0.326 | evet | evet |  |  | 0.3 | OK |
| k2-anlamsiz | anlamsiz |  | 0.378 |  | evet |  |  | 3.9 | OK |
| k2-takip-sinan#1 | hazirlik |  | 0.718 |  |  |  | var | 9.3 | - |
| k2-takip-sinan#2 | takip | 2 | 0.705 |  |  | eksik | doğru | 10.8 | HATA |
| k2-takip-preveze#1 | hazirlik |  | 0.8 |  |  |  | var | 4.1 | - |
| k2-takip-preveze#2 | takip | 1 | 0.833 |  |  | tam | doğru | 3.9 | OK |
| k2-takip-akif#1 | hazirlik |  | 0.714 |  |  |  | var | 3.8 | - |
| k2-takip-akif#2 | takip | 31 | 0.72 |  | evet |  |  | 4.0 | HATA |
| k2-takip-karahanli#1 | hazirlik |  | 0.727 |  |  |  | var | 3.9 | - |
| k2-takip-karahanli#2 | takip | 1 | 0.72 |  |  | tam | doğru | 4.5 | OK |
| k2-cevapsiz-takip-sinan#1 | hazirlik |  | 0.742 |  |  |  | var | 4.1 | - |
| k2-cevapsiz-takip-sinan#2 | takip_cevapsiz |  | 0.732 |  |  |  | var | 5.2 | HATA |
| k2-cevapsiz-takip-nevruz#1 | hazirlik |  | 0.762 |  |  |  | var | 9.5 | - |
| k2-cevapsiz-takip-nevruz#2 | takip_cevapsiz |  | 0.747 |  | evet |  |  | 10.3 | OK |
| k2-cevapsiz-takip-kadi#1 | hazirlik |  | 0.565 |  |  |  | var | 10.3 | - |
| k2-cevapsiz-takip-kadi#2 | takip_cevapsiz |  | 0.441 |  |  |  | var | 5.0 | HATA |
| k2-degisim-mehter#1 | hazirlik |  | 0.677 |  |  |  | var | 3.8 | - |
| k2-degisim-mehter#2 | konu_degisimi | 1 | 0.64 |  |  | tam | doğru | 6.0 | OK |
| k2-degisim-balbal#1 | hazirlik |  | 0.782 |  |  |  | var | 3.4 | - |
| k2-degisim-balbal#2 | konu_degisimi | 106 | 0.698 |  | evet |  |  | 3.5 | HATA |
| k2-degisim-semeni#1 | hazirlik |  | 0.727 |  |  |  | var | 3.9 | - |
| k2-degisim-semeni#2 | konu_degisimi | 71 | 0.743 |  | evet |  |  | 3.9 | HATA |
| k2-disi-sonra-hava#1 | hazirlik |  | 0.712 |  |  |  | var | 7.0 | - |
| k2-disi-sonra-hava#2 | konu_disi_sonra |  | 0.627 |  | evet |  |  | 4.6 | OK |
| k2-disi-sonra-tarif#1 | hazirlik |  | 0.565 |  |  |  | var | 10.3 | - |
| k2-disi-sonra-tarif#2 | konu_disi_sonra |  | 0.56 |  | evet |  |  | 4.6 | OK |

## Cevaplar (gözle kontrol için)

**k2-beylik-konum** — Osmanlı Beyliği'nin büyümesinde coğrafi konumun rolü nedir?
> Osmanlı Beyliği'nin coğrafi konumu, beyliğin büyümesinde önemli bir rol oynamıştır. Coğrafi konum, Osmanlı'nın Bizans sınırında yer alması sayesinde Bizans topraklarına daha hızlı erişim sağladı ve genişleme yönü Bizans topraklarına değil, Müslüman komşulara dönüştü. Bu durum, Osmanlı'nın gaza anlayışıyla meşruiyet sağlamasına ve diğer beyliklerle erken çatışmayı önledi. Aynı zamanda, Moğol baskısından kaçan Türkmen nüfusun bu bölgeye yönelmesini sağlayarak Osmanlı'a sürekli bir insan kaynağı sağladı. (Kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md)

Getirilen: `anadolu-beylikleri-ve-osmanlinin-kurulusu.md#6 0.805 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#8 0.643 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#2 0.609 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.601 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#7 0.595`

**k2-asistan-internet** — Asistan çalışmak için internet bağlantısına ihtiyaç duyar mı?
> Asistan tümüyle kullanıcının kendi bilgisayarında çalışır ve internet bağlantısı gerektirmemektedir. Dil modeli ve gömme modeli yerelde çalıştığından, internet bağlantısı olmadan da kullanılabilir. (Kaynak: asistan-hakkinda.md)

Getirilen: `asistan-hakkinda.md#5 0.640 | asistan-hakkinda.md#3 0.497 | asistan-hakkinda.md#6 0.486 | asistan-hakkinda.md#2 0.484 | asistan-hakkinda.md#4 0.470`

**k2-juanjuan** — Göktürkler bağımsızlıklarından önce hangi devlet için demir işlemiştir?
> Göktürkler bağımsızlıklarından önce Juan-juan Devleti için demir işlemişlerdir. (Kaynak: bozkir-gocebe-yasami.md)

Getirilen: `bozkir-gocebe-yasami.md#6 0.698 | ilk-turk-devletleri.md#1 0.579 | ilk-turk-devletleri.md#4 0.566 | bugunku-turk-dunyasi.md#1 0.554 | turk-milliyetciliginin-dogusu.md#0 0.535`

**k2-kirgizistan** — Kırgızistan bağımsızlığını ne zaman ilan etmiştir?
> Kırgızistan 31 Ağustos 1991'de bağımsızlığını ilan etmiştir. (Kaynak: bugunku-turk-dunyasi.md)

Getirilen: `bugunku-turk-dunyasi.md#1 0.698 | bugunku-turk-dunyasi.md#2 0.597 | oguz-boylari-ve-turk-boy-yapisi.md#8 0.504 | cumhuriyet-inkilaplari.md#3 0.494 | turklerin-islamiyeti-kabulu.md#2 0.493`

**k2-kuvayi** — İşgallere karşı ilk tepki hangi birliklerden gelmiştir?
> Bölgesel olarak kurulan ve Kuvâ-yi Milliye adıyla anılan gönüllü birliklerden ilk tepki gelmiştir. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#2 0.503 | turklerin-islamiyeti-kabulu.md#0 0.461 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#7 0.449 | canakkale-ve-kurtulus-savasi.md#0 0.438 | ilk-turk-devletleri.md#4 0.427`

**k2-ilk-anayasa** — İlk anayasa hangi tarihte kabul edilmiştir?
> 20 Ocak 1921'de kabul edilen Teşkilat-ı Esasiye Kanunu, ilk anayasa olarak kabul edilmiştir. (Kaynak: cumhuriyet-inkilaplari.md)

Getirilen: `cumhuriyet-inkilaplari.md#2 0.654 | cumhuriyet-inkilaplari.md#4 0.548 | ilk-turk-islam-eserleri.md#0 0.522 | cumhuriyet-inkilaplari.md#1 0.509 | ilk-turk-devletleri.md#1 0.504`

**k2-dlt-harita** — Dîvânu Lugâti't-Türk'teki haritanın merkezinde hangi şehir vardır?
> Dîvânu Lugâti't-Türk'teki haritanın merkezinde Balasagun şehri bulunmaktadır. (Kaynak: ilk-turk-islam-eserleri.md)

Getirilen: `ilk-turk-islam-eserleri.md#4 0.731 | ilk-turk-islam-eserleri.md#3 0.675 | ilk-turk-islam-eserleri.md#7 0.517 | selcuklu-ve-osmanli-mimarisi.md#7 0.515`

**k2-akif-meslek** — Mehmet Âkif Ersoy hangi mesleği yapmıştır?
> Mehmet Âkif Ersoy, veteriner hekimliği mesleğini yapmıştır. (Kaynak: milli-semboller.md)

Getirilen: `milli-semboller.md#3 0.817 | milli-semboller.md#4 0.693`

**k2-sofya** — Mustafa Kemal Sofya'da hangi görevde bulunmuştur?
> Mustafa Kemal Atatürk, 1913-1915 yılları arasında Sofya'da askerî ataşe olarak görevlendirilmiştir. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#3 0.652 | mustafa-kemal-ataturk.md#2 0.649 | mustafa-kemal-ataturk.md#1 0.637 | mustafa-kemal-ataturk.md#0 0.621 | mustafa-kemal-ataturk.md#4 0.616`

**k2-nevruz-bm** — Birleşmiş Milletler 21 Mart'ı ne ilan etmiştir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `milli-semboller.md#9 0.547 | milli-semboller.md#1 0.545 | bugunku-turk-dunyasi.md#4 0.508 | bugunku-turk-dunyasi.md#1 0.505 | mustafa-kemal-ataturk.md#4 0.486`

**k2-avar** — Avarlar İstanbul'u hangi yılda kuşatmıştır?
> Avarlar İstanbul'u 626'da kuşatmıştır. (Kaynak: oguz-boylari-ve-turk-boy-yapisi.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#0 0.543 | oguz-boylari-ve-turk-boy-yapisi.md#7 0.505 | canakkale-ve-kurtulus-savasi.md#1 0.498 | turk-islam-dunyasinda-bilim.md#7 0.489 | mustafa-kemal-ataturk.md#6 0.486`

**k2-kadi** — Osmanlı taşra yönetiminde kaza düzeyinde kim görev yapardı?
> Kaza düzeyinde kadı görev yapardı; kadı hem yargıç hem noter hem de yerel yönetim görevlisidir ve doğrudan merkeze bağlıdır. (Kaynak: osmanli-devlet-teskilati.md)

Getirilen: `osmanli-devlet-teskilati.md#3 0.771 | osmanli-devlet-teskilati.md#0 0.586 | osmanli-devlet-teskilati.md#2 0.564 | osmanli-devlet-teskilati.md#4 0.550 | osmanli-islahat-ve-mesrutiyet.md#1 0.548`

**k2-kafes** — Şehzadelerin sarayda tutulduğu düzene ne ad verilir?
> Şehzadelerin sarayda kapalı bir dairede, kafes adı verilen düzende tutulmuştur. (Kaynak: osmanli-islahat-ve-mesrutiyet.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#2 0.517 | turk-kulturunde-at.md#1 0.478 | osmanli-devlet-teskilati.md#6 0.458 | ozan-asik-gelenegi.md#3 0.451 | osmanli-devlet-teskilati.md#4 0.449`

**k2-mehter-calgi** — Mehter topluluğunda hangi çalgılar bulunur?
> Mehter topluluğunda zurna, boru, kös, nakkare, davul ve zil bulunur. (Kaynak: ozan-asik-gelenegi.md)

Getirilen: `ozan-asik-gelenegi.md#8 0.646 | ozan-asik-gelenegi.md#7 0.479 | ozan-asik-gelenegi.md#6 0.467`

**k2-sinan-dogum** — Mimar Sinan nerede doğmuştur?
> Mimar Sinan, Kayseri'nin Ağırnas köyünde doğmuştur. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)

Getirilen: `selcuklu-ve-osmanli-mimarisi.md#5 0.746 | selcuklu-ve-osmanli-mimarisi.md#6 0.587 | turk-islam-dunyasinda-bilim.md#3 0.584`

**k2-barbaros-cezayir** — Barbaros Hayreddin Paşa hangi şehrin yönetimini üstlenmiştir?
> Barbaros Hayreddin Paşa Cezayir'in yönetimini üstlenmiştir. (Kaynak: turk-denizciligi.md)

Getirilen: `turk-denizciligi.md#2 0.773 | turk-denizciligi.md#3 0.520`

**k2-saka-destan** — Sakalara ait destanlar hangileridir?
> Sakalara ait destanlar arasında Alp Er Tunga ve Şu destanları sayılır. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#0 0.714 | turk-destanlari.md#1 0.568 | turk-destanlari.md#3 0.549 | turk-destanlari.md#4 0.515 | ozan-asik-gelenegi.md#2 0.511`

**k2-biruni-dil** — Bîrûnî hangi dili öğrenmiştir?
> Bîrûnî, Hindistan seferlerine katılarak Sanskritçe öğrenmiştir. (Kaynak: turk-islam-dunyasinda-bilim.md)

Getirilen: `turk-islam-dunyasinda-bilim.md#4 0.677 | turk-kulturunde-kurt.md#5 0.448`

**k2-kurt-tug** — Göktürklerde kurt figürü nerelerde kullanılmıştır?
> Göktürklerde kurt figürü bayrak ve sancaklarda yer almıştır. Ayrıca, kurt başlı tuğların da kullanıldığı kaynaklarda belirtilmiştir. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#3 0.731 | turk-kulturunde-kurt.md#0 0.671 | turk-kulturunde-kurt.md#2 0.668 | turk-kulturunde-kurt.md#1 0.657 | turk-kulturunde-kurt.md#6 0.655`

**k2-kutsal-sayi** — Türk inancında hangi sayılar kutsal sayılır?
> Üç, yedi, dokuz ve kırk sayılar Türk inancında kutsal sayılır. Göğün kat kat olduğu düşüncesi, hükümdarın rütbesini gösteren dokuz tuğ, destanlarda kahramanın yanındaki kırk yiğit ve kırk gün süren düğünler bu sayıların kullanımına örnek olmaktadır. (Kaynak: turk-mitolojisi-ve-gok-tanri.md)

Getirilen: `turk-mitolojisi-ve-gok-tanri.md#6 0.772 | turk-mitolojisi-ve-gok-tanri.md#0 0.638 | turk-mitolojisi-ve-gok-tanri.md#1 0.605 | turk-mitolojisi-ve-gok-tanri.md#4 0.594 | turk-mitolojisi-ve-gok-tanri.md#2 0.593`

**k2-karahanli-bolunme** — Karahanlı Devleti ne zaman ikiye ayrılmıştır?
> Karahanlı Devleti 1042'de ikiye ayrılmıştır. (Kaynak: turklerin-islamiyeti-kabulu.md)

Getirilen: `turklerin-islamiyeti-kabulu.md#4 0.689 | turklerin-islamiyeti-kabulu.md#3 0.637 | turk-devlet-gelenegi.md#3 0.532 | osmanli-islahat-ve-mesrutiyet.md#9 0.495 | cumhuriyet-inkilaplari.md#1 0.492`

**k2-uygur-matbaa** — Uygurlar metin çoğaltmak için hangi tekniği kullanmıştır?
> Uygurlar metin çoğaltmak için ağaç baskı tekniğini kullanmıştır. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#1 0.614 | turk-kulturunde-at.md#2 0.447 | bozkir-gocebe-yasami.md#6 0.435`

**k2-miryokefalon** — Miryokefalon Savaşı'nın sonucu ne olmuştur?
> Miryokefalon Savaşı'nda Bizans'ın Anadolu'yu geri alma girişimi başarısız olmuştur ve Anadolu'nun Türk yurdu olduğu kesinleşmiştir. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#3 0.484 | canakkale-ve-kurtulus-savasi.md#3 0.467 | selcuklular-ve-malazgirt.md#4 0.457 | osmanli-islahat-ve-mesrutiyet.md#3 0.443 | turklerin-islamiyeti-kabulu.md#6 0.436`

**k2-kut-soy** — Kut kime verilmiş sayılırdı?
> Kut, kişiye değil soya verilmiş sayılırdı. Bu anlayış, devletin sürekliliğini sağlarken taht kavgalarına da yol açmıştır. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-kulturunde-kurt.md#6 0.545 | turk-devlet-gelenegi.md#0 0.523 | turk-kulturunde-kurt.md#5 0.519`

**k2-uygur-alfabe** — Uygur alfabesi kaç harften oluşur?
> Uygur alfabesi on dört harften oluşur. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#1 0.752 | turkcenin-tarihi-ve-alfabeleri.md#0 0.633 | bugunku-turk-dunyasi.md#6 0.602`

**k2-fetret** — Fetret Devri kaç yıl sürmüştür?
> Fetret Devri, Yıldırım Bayezid'in Timur'a yenilmesi ve hâkimiyetinin dağılmasıyla başlayarak 1402 yılından itibaren ve Karamanoğulları'na Fatih Sultan Mehmed döneminde son verilmesine kadar, yani 1417 yılına kadar sürmüştür. Fetret Devri'nin ardından birlik adım adım yeniden sağlanmıştır. (Kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#4 0.563 | selcuklu-ve-osmanli-mimarisi.md#2 0.451 | osmanli-padisahlari.md#2 0.450 | turk-denizciligi.md#3 0.449 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#9 0.448`

**k2-ahal-teke** — Ahal Teke atı hangi özellikleriyle bilinir?
> Ahal Teke atı dayanıklılık ve uzun mesafe performansıyla bilinir. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#5 0.528 | bozkir-gocebe-yasami.md#5 0.496 | turk-kulturunde-at.md#1 0.473 | ilk-turk-islam-eserleri.md#5 0.437 | turkcenin-tarihi-ve-alfabeleri.md#0 0.416`

**k2-turk-yurdu** — Türk Yurdu dergisi ne zaman kurulmuştur?
> Turk Yurdu dergisi 1911'de kurulmuştur. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.740 | bugunku-turk-dunyasi.md#2 0.580 | turkcenin-tarihi-ve-alfabeleri.md#4 0.579 | bugunku-turk-dunyasi.md#5 0.576 | bugunku-turk-dunyasi.md#4 0.553`

**k2-sened** — Sened-i İttifak hangi yıl imzalanmıştır?
> Sened-i İttifak 1808'de imzalanmıştır. (Kaynak: osmanli-islahat-ve-mesrutiyet.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#5 0.517 | osmanli-islahat-ve-mesrutiyet.md#9 0.473 | cumhuriyet-inkilaplari.md#1 0.448 | milli-semboller.md#1 0.440 | milli-semboller.md#0 0.438`

**k2-cevapsiz-sinan-sayi** — Mimar Sinan tam olarak kaç yapı inşa etmiştir?
> Mimar Sinan'in tam olarak kaç yapı inşa ettiğinden kesin bir sayı verilemiyor, ancak kayıtlara göre yüzlerce yapıyı inşa ettiğini biliyoruz. Özellikle Süleymaniye Camii ve Selimiye Camii gibi önemli yapıları inşa ettiği bilinmektedir. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)

Getirilen: `selcuklu-ve-osmanli-mimarisi.md#5 0.716 | selcuklu-ve-osmanli-mimarisi.md#6 0.692 | selcuklu-ve-osmanli-mimarisi.md#4 0.512 | selcuklu-ve-osmanli-mimarisi.md#1 0.511 | selcuklu-ve-osmanli-mimarisi.md#0 0.511`

**k2-cevapsiz-barbaros-dogum** — Barbaros Hayreddin Paşa hangi yıl doğmuştur?
> Bağlamda Barbaros Hayreddin Paşa'nın doğduğu yıl belirtilmemiştir. Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-denizciligi.md#2 0.794 | turk-denizciligi.md#3 0.519`

**k2-cevapsiz-akif-mezar** — Mehmet Âkif Ersoy nereye gömülmüştür?
> Mehmet Âkif Ersoy'nün gömüldüğü yer hakkında bilgi bulunmamaktadır. (Kaynak: milli-semboller.md)

Getirilen: `milli-semboller.md#3 0.773 | milli-semboller.md#4 0.683 | mustafa-kemal-ataturk.md#6 0.600`

**k2-cevapsiz-pecenek-nufus** — Peçeneklerin nüfusu ne kadardı?
> Bu bilgi elimdeki dok dokümanlarda yok. (Kaynak: bozkir-gocebe-yasami.md)

Getirilen: `bozkir-gocebe-yasami.md#0 0.476 | bozkir-gocebe-yasami.md#3 0.448 | ozan-asik-gelenegi.md#7 0.440 | oguz-boylari-ve-turk-boy-yapisi.md#6 0.438 | osmanli-islahat-ve-mesrutiyet.md#1 0.433`

**k2-cevapsiz-biruni-ogrenci** — Bîrûnî'nin öğrencileri kimlerdi?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-islam-dunyasinda-bilim.md#4 0.698 | turk-islam-dunyasinda-bilim.md#2 0.438`

**k2-cevapsiz-kadi-maas** — Osmanlı'da kadılar ne kadar maaş alırdı?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#1 0.578 | osmanli-padisahlari.md#0 0.562 | osmanli-devlet-teskilati.md#7 0.558 | osmanli-padisahlari.md#1 0.556 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.542`

**k2-disi-corba** — Mercimek çorbası nasıl yapılır?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `bozkir-gocebe-yasami.md#4 0.442 | bozkir-gocebe-yasami.md#2 0.427 | turk-kulturunde-at.md#3 0.414 | turk-kulturunde-kurt.md#6 0.384 | selcuklu-ve-osmanli-mimarisi.md#1 0.380`

**k2-disi-dolar** — Bugün dolar kaç lira?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `bugunku-turk-dunyasi.md#0 0.393 | bugunku-turk-dunyasi.md#6 0.316`

**k2-disi-kod** — JavaScript'te bir dizi nasıl ters çevrilir?
> Bu bilgi elimdeki dokümanlarda yok. En yakın bölümler şu belgelerde geçiyor: asistan-hakkinda.md, bugunku-turk-dunyasi.md, turk-devlet-gelenegi.md. Soruyu biraz daha açık yazarsanız yeniden bakabilirim.

Getirilen: `asistan-hakkinda.md#2 0.326 | bugunku-turk-dunyasi.md#6 0.306 | turk-devlet-gelenegi.md#1 0.299 | ozan-asik-gelenegi.md#4 0.298 | turk-kulturunde-at.md#1 0.298 | turk-denizciligi.md#6 0.294 | turk-denizciligi.md#1 0.292 | turkcenin-tarihi-ve-alfabeleri.md#0 0.288`

**k2-anlamsiz** — qwerty asdf 12345
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.378 | bugunku-turk-dunyasi.md#6 0.378 | asistan-hakkinda.md#2 0.373 | asistan-hakkinda.md#5 0.340 | ilk-turk-devletleri.md#3 0.334`

**k2-takip-sinan#1** — Mimar Sinan ustalık eseri olarak hangi yapıyı göstermiştir?
> Mimar Sinan ustalık eseri olarak Edirne'deki Selimiye Camii'ni göstermiştir. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)

Getirilen: `selcuklu-ve-osmanli-mimarisi.md#5 0.718 | selcuklu-ve-osmanli-mimarisi.md#6 0.714 | selcuklu-ve-osmanli-mimarisi.md#0 0.576 | selcuklu-ve-osmanli-mimarisi.md#4 0.561 | selcuklu-ve-osmanli-mimarisi.md#1 0.544`

**k2-takip-sinan#2** — nerede bulunuyor?  
_Önceki soru: Mimar Sinan ustalık eseri olarak hangi yapıyı göstermiştir?_
> Mimar Sinan'nın yaşam ve çalışmalarının önemli kısmında, Kayseri'nin Ağırnas köyünde doğmuş olduğu belirtiliyor. Ayrıca, Mimar Sinan'ın yapıtlarının üç aşamasını gösteren Süleymaniye Camii'nin inşaat yıllarının da verildiği parçalar 6 ve 6'ta anlatılıyor. Bu bilgilerin bulunduğu yerler, dosya.md içinde belirtilmiştir. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)

Getirilen: `selcuklu-ve-osmanli-mimarisi.md#5 0.705 | selcuklu-ve-osmanli-mimarisi.md#6 0.701 | selcuklu-ve-osmanli-mimarisi.md#4 0.547 | selcuklu-ve-osmanli-mimarisi.md#0 0.544 | selcuklu-ve-osmanli-mimarisi.md#1 0.521`

**k2-takip-preveze#1** — Preveze Deniz Savaşı'nı kim kazanmıştır?
> Barbaros Hayreddin Paşa komutasındaki Osmanlı donanması Preveze Deniz Savaşı'nda Andrea Doria komutasındaki Haçlı donanmasını mağlup etmiştir. Bu zafer, Osmanlıların Akdeniz'deki güçlerinin artmasına neden olmuştur. (Kaynak: turk-denizciligi.md)

Getirilen: `turk-denizciligi.md#3 0.800 | turk-denizciligi.md#8 0.540`

**k2-takip-preveze#2** — hangi tarihte oldu?  
_Önceki soru: Preveze Deniz Savaşı'nı kim kazanmıştır?_
> Preveze Deniz Savaşı 28 Eylül 1538'de yapılmıştır. (Kaynak: turk-denizciligi.md)

Getirilen: `turk-denizciligi.md#3 0.833 | turk-denizciligi.md#8 0.553`

**k2-takip-akif#1** — İstiklal Marşı'nın şairi kimdir?
> İstiklal Marşı'nın şairi Mehmet Âkif Ersoy'dur. (Kaynak: milli-semboller.md)

Getirilen: `milli-semboller.md#0 0.714 | milli-semboller.md#1 0.651 | milli-semboller.md#2 0.565`

**k2-takip-akif#2** — hangi dergide yazardı?  
_Önceki soru: İstiklal Marşı'nın şairi kimdir?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `milli-semboller.md#0 0.720 | milli-semboller.md#1 0.645 | milli-semboller.md#2 0.560`

**k2-takip-karahanli#1** — Karahanlı Devleti ne zaman kurulmuştur?
> Karahanlı Devleti, Uygur Kağanlığı'nın yıkılmasının ardından, 840 yılında Karluk, Yağma ve Çiğil boylarının birleşmesiyle kurulmuştur. (Kaynak: turklerin-islamiyeti-kabulu.md)

Getirilen: `turklerin-islamiyeti-kabulu.md#3 0.727 | turklerin-islamiyeti-kabulu.md#4 0.716`

**k2-takip-karahanli#2** — ne zaman ikiye ayrıldı?  
_Önceki soru: Karahanlı Devleti ne zaman kurulmuştur?_
> Devlet 1042'de Doğu ve Batı Karahanlılar olmak üzere ikiye ayrılmıştır. (Kaynak: turklerin-islamiyeti-kabulu.md)

Getirilen: `turklerin-islamiyeti-kabulu.md#4 0.720 | turklerin-islamiyeti-kabulu.md#3 0.697 | cumhuriyet-inkilaplari.md#1 0.504`

**k2-cevapsiz-takip-sinan#1** — Mimar Sinan hangi padişahlar döneminde çalışmıştır?
> Mimar Sinan, Kanuni Sultan Süleyman, II. Selim ve III. Murad dönemlerinde çalışmıştır. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)

Getirilen: `selcuklu-ve-osmanli-mimarisi.md#5 0.742 | selcuklu-ve-osmanli-mimarisi.md#6 0.614 | turk-islam-dunyasinda-bilim.md#3 0.524`

**k2-cevapsiz-takip-sinan#2** — kaç yaşında öldü?  
_Önceki soru: Mimar Sinan hangi padişahlar döneminde çalışmıştır?_
> Mimar Sinan 1588 yılında ölmüş ve kayıtlara göre onun yaşam süresi yaklaşık 50-60 yaş aralığında olup, bu da onun ölüm tarihi 1588 ile doğum tarihi arasındaki farkı ifade eder. Ancak tam bir yaşı belirtilmemiştir. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)

Getirilen: `selcuklu-ve-osmanli-mimarisi.md#5 0.732 | selcuklu-ve-osmanli-mimarisi.md#6 0.585 | turk-islam-dunyasinda-bilim.md#3 0.557`

**k2-cevapsiz-takip-nevruz#1** — Nevruz hangi tarihte kutlanır?
> Nevruz, 21 Mart'ta kutlanır. Bu tarih, gece ile gündüzün eşitlendiği ilkbahar gündönümünde gerçekleşir ve bahar bayramı olarak kutlanır. (Kaynak: nevruz-ve-turk-bayramlari.md)

Getirilen: `nevruz-ve-turk-bayramlari.md#0 0.762 | nevruz-ve-turk-bayramlari.md#5 0.696 | nevruz-ve-turk-bayramlari.md#6 0.673 | nevruz-ve-turk-bayramlari.md#1 0.631 | nevruz-ve-turk-bayramlari.md#2 0.587`

**k2-cevapsiz-takip-nevruz#2** — kaç ülkede resmî tatildir?  
_Önceki soru: Nevruz hangi tarihte kutlanır?_
> Türkiye'de 1991'den sonra resmî törenlerle kutlanmaya başılmış ve 1995'te resmî bayram olarak kabul edilmiştir. Ancak belirtilen metinde başka ülkelerin resmî tatil olup olmadığı belirtilmemiştir. Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `nevruz-ve-turk-bayramlari.md#0 0.747 | nevruz-ve-turk-bayramlari.md#5 0.745 | nevruz-ve-turk-bayramlari.md#6 0.647 | nevruz-ve-turk-bayramlari.md#1 0.614 | nevruz-ve-turk-bayramlari.md#2 0.603`

**k2-cevapsiz-takip-kadi#1** — Osmanlı'da kadı ne iş yapardı?
> Osmanlı'da kadı, hukuki sorunları çözerken ve mahkemelerde yargı yaparken çeşitli görevler görürdü. Kadılar, kanunları uygulamaya ve uygulanmasına yardımcı olurlardı. Ayrıca, vatandaşların hukuki taleplerini karşılamak ve adaleti sağlamak için de çalışırlardı. (Kaynak: osmanli-devlet-teskilati.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#5 0.565 | osmanli-padisahlari.md#1 0.562 | osmanli-padisahlari.md#0 0.562 | osmanli-devlet-teskilati.md#0 0.561 | osmanli-islahat-ve-mesrutiyet.md#2 0.550`

**k2-cevapsiz-takip-kadi#2** — kaç yıl görev yapardı?  
_Önceki soru: Osmanlı'da kadı ne iş yapardı?_
> Mimar Sinan, Mimarbaşılık görevinde yaklaşık elli yıla yakın süre görev yaptı. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)

Getirilen: `mustafa-kemal-ataturk.md#2 0.441 | mustafa-kemal-ataturk.md#5 0.406 | osmanli-padisahlari.md#4 0.389 | selcuklu-ve-osmanli-mimarisi.md#5 0.382 | turk-islam-dunyasinda-bilim.md#5 0.372`

**k2-degisim-mehter#1** — Bîrûnî hangi dili öğrenmiştir?
> Bîrûnî, Hindistan seferlerine katılarak Sanskritçe öğrenmiştir. (Kaynak: turk-islam-dunyasinda-bilim.md)

Getirilen: `turk-islam-dunyasinda-bilim.md#4 0.677 | turk-kulturunde-kurt.md#5 0.448`

**k2-degisim-mehter#2** — Mehter nedir?  
_Önceki soru: Bîrûnî hangi dili öğrenmiştir?_
> Mehter, Osmanlı ordusunun askerî müzik topluluğudur ve dünyanın bilinen en eski askerî bandosu kabul edilir. Toplulukta zurna, boru, kös, nakkare, davul ve zil gibi çalgılardan oluşan bir grup bulunmaktadır ve çalınan parçalara peşrev ve mehter marşı denilmektedir. Mehterin yürüyüş düzeni ve durup dönerek ilerlemesi kendine özgüdür. Yeniçeri Ocağı'nın 1826'da kaldırılmasıyla mehter dağılmış, ancak yirminci yüzyılda tarihî topluk olarak yeniden kurulmuştur. (Kaynak: ozan-asik-gelenegi.md)

Getirilen: `ozan-asik-gelenegi.md#8 0.640 | milli-semboller.md#0 0.360`

**k2-degisim-balbal#1** — Barbaros Hayreddin Paşa nerede doğmuştur?
> Barbaros Hayreddin Paşa, Midilli adasında doğmuştur. (Kaynak: turk-denizciligi.md)

Getirilen: `turk-denizciligi.md#2 0.782 | turk-denizciligi.md#3 0.511`

**k2-degisim-balbal#2** — Balbal nedir?  
_Önceki soru: Barbaros Hayreddin Paşa nerede doğmuştur?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-denizciligi.md#2 0.698 | turk-denizciligi.md#3 0.490`

**k2-degisim-semeni#1** — Mimar Sinan ne zaman ölmüştür?
> Mimar Sinan 1588'de ölmüştür. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)

Getirilen: `selcuklu-ve-osmanli-mimarisi.md#5 0.727 | selcuklu-ve-osmanli-mimarisi.md#6 0.583 | turk-islam-dunyasinda-bilim.md#3 0.558`

**k2-degisim-semeni#2** — Semeni nedir?  
_Önceki soru: Mimar Sinan ne zaman ölmüştür?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `selcuklu-ve-osmanli-mimarisi.md#5 0.743 | selcuklu-ve-osmanli-mimarisi.md#6 0.613 | turk-islam-dunyasinda-bilim.md#3 0.574`

**k2-disi-sonra-hava#1** — Türk bayrağında hangi renkler vardır?
> Türk bayrağında kırmızı ve beyaz renkler vardır. Bayrağın zemin kırmızı rektangel şeklindedir ve üzerinde beyaz ay ve yıldız simgeleri yer almaktadır. (Kaynak: milli-semboller.md)

Getirilen: `milli-semboller.md#5 0.712 | bugunku-turk-dunyasi.md#0 0.570 | oguz-boylari-ve-turk-boy-yapisi.md#2 0.566 | milli-semboller.md#6 0.551 | nevruz-ve-turk-bayramlari.md#2 0.526`

**k2-disi-sonra-hava#2** — Yarın hava nasıl olacak?  
_Önceki soru: Türk bayrağında hangi renkler vardır?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `milli-semboller.md#5 0.627 | bugunku-turk-dunyasi.md#0 0.562 | milli-semboller.md#6 0.511 | nevruz-ve-turk-bayramlari.md#2 0.503 | turk-mitolojisi-ve-gok-tanri.md#0 0.494`

**k2-disi-sonra-tarif#1** — Osmanlı'da kadı ne iş yapardı?
> Osmanlı'da kadı, hukuki sorunları çözerken ve mahkemelerde yargı yaparken çeşitli görevler görürdü. Kadılar, kanunları uygulamaya ve uygulanmasına yardımcı olurlardı. Ayrıca, vatandaşların hukuki taleplerini karşılamak ve adaleti sağlamak için de çalışırlardı. (Kaynak: osmanli-devlet-teskilati.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#5 0.565 | osmanli-padisahlari.md#1 0.562 | osmanli-padisahlari.md#0 0.562 | osmanli-devlet-teskilati.md#0 0.561 | osmanli-islahat-ve-mesrutiyet.md#2 0.550`

**k2-disi-sonra-tarif#2** — Bana pizza tarifi verir misin?  
_Önceki soru: Osmanlı'da kadı ne iş yapardı?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-padisahlari.md#0 0.560 | osmanli-devlet-teskilati.md#0 0.550 | osmanli-padisahlari.md#1 0.540 | osmanli-islahat-ve-mesrutiyet.md#5 0.533 | osmanli-devlet-teskilati.md#7 0.530`

