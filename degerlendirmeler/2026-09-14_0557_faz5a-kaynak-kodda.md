# Değerlendirme: 2026-09-14 05:57 — faz5a-kaynak-kodda

| Ayar | Değer |
|---|---|
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
| git | 64e3342 (kaydedilmemis degisiklik var) |
| set_parmak_izi | dcda3164d3 |

## Özet

Puanlanan soru: 90 (74 cevaplanabilir, 16 cevaplanamaz). Senaryoların hazırlık soruları özete katılmaz.

Karşılaştırılan çalışma: `degerlendirmeler/2026-09-14_0530_faz3b-esik-033.json`

| Ölçüt | Önceki | Şimdi |
|---|---|---|
| Tam başarı (tüm puanlanan sorular) | 87.8% | 93.3% |
| Arama: doğru parça 1. sırada (hit@1) | 87.8% | 87.8% |
| Arama: doğru parça ilk 3'te (hit@3) | 95.9% | 95.9% |
| Arama: MRR (1 = hep 1. sırada) | 0.919 | 0.919 |
| Cevaplanabilir sorularda başarı | 93.2% | 91.9% |
| Yanlış red (cevap belgede varken) | 2.7% | 4.1% |
|   bunun eşikte olanı | 0.0% | 0.0% |
| Anahtar ifadelerin tamamı cevapta | 97.2% | 95.8% |
| Bilinen yanlışı içeren cevap | 1 adet | 1 adet |
| Kaynak satırı var | 100.0% | 98.6% |
| Kaynak doğru belge | 97.2% | 97.2% |
| Cevaplanamaz soruları reddetme | 100.0% | 100.0% |
|   bunun eşikte olanı | 12.5% | 12.5% |
| Red cevabına eklenmiş kaynak satırı | 6 adet | 0 adet |
| Süre ortalaması | 1.97 sn | 1.75 sn |
| Süre medyanı | 1.94 sn | 1.67 sn |
| En uzun süre | 3.48 sn | 3.24 sn |
| İlk token ortalaması (modele giden sorular) | 0.72 sn | 0.78 sn |
| Arama süresi ortalaması | 0.424 sn | 0.426 sn |

## Kategorilere göre

| Kategori | Soru | Başarılı | hit@1 | hit@3 | Yanlış red |
|---|---|---|---|---|---|
| normal | 55 | 53 | 49 | 55 | 2 |
| ozel_ad | 10 | 8 | 9 | 9 | 0 |
| yakin | 6 | 6 | - | - | - |
| konu_disi | 3 | 3 | - | - | - |
| anlamsiz | 1 | 1 | - | - | - |
| takip | 5 | 4 | 4 | 4 | 0 |
| takip_cevapsiz | 2 | 2 | - | - | - |
| konu_degisimi | 4 | 3 | 3 | 3 | 1 |
| konu_disi_sonra | 4 | 4 | - | - | - |
| hazirlik (puanlanmaz) | 15 | - | - | - | - |

Eski 12 soruluk set (eval_results.md ile aynı sorular): **11/12** başarılı.

## Önceki çalışmaya göre değişen sorular

Cevap metni değişen soru: 77. Sonucu değişen soru: 11.

- **canakkale-1** OK → HATA: Çanakkale Deniz Zaferi hangi tarihte kazanılmıştır? (yanlış red (model))
- **ilkturk-1** OK → HATA: Orhun Yazıtları'nın alfabesini kim ve hangi yılda çözmüştür? (yanlış red (model))
- **isimler-2** OK → HATA: Dokuz Işık ilkeleri nelerdir? (eksik: milliyetçilik, ülkücülük)
- **at-1** HATA → OK: Turan taktiği nasıl uygulanır?
- **kurt-6** HATA → OK: Ergenekon'dan çıkan topluluğa yolu kim göstermiştir?
- **cevapsiz-1** HATA → OK: Fatih Sultan Mehmed'in annesinin adı nedir?
- **cevapsiz-2** HATA → OK: Malazgirt Savaşı'nda Selçuklu ordusu kaç askerden oluşuyordu?
- **cevapsiz-4** HATA → OK: Lozan Antlaşması'nı Türk heyeti adına kim imzalamıştır?
- **cevapsiz-5** HATA → OK: Orhun Yazıtları bugün hangi müzede sergilenmektedir?
- **takip-cevapsiz-2#2** HATA → OK: ilk başkanı kimdi?
- **disi-2#2** HATA → OK: asdf qwerty zxcv

## Başarısız sorular

- **canakkale-1** (normal) Çanakkale Deniz Zaferi hangi tarihte kazanılmıştır?
  - Neden: yanlış red (model)
  - Cevap: Bu bilgi elimdeki dokümanlarda yok.
- **ilkturk-1** (normal) Orhun Yazıtları'nın alfabesini kim ve hangi yılda çözmüştür?
  - Neden: yanlış red (model)
  - Cevap: Bu bilgi elimdeki dokümanlarda yok.
- **isimler-2** (ozel_ad) Dokuz Işık ilkeleri nelerdir?
  - Neden: eksik: milliyetçilik, ülkücülük
  - Cevap: Dokuz Işık ilkeleri, ülkeyi ve toplumu kalkınmış hale getirmek için Milliyetçi Hareket tarafından benimsenen ideolojik temellerdir ve şunlarla oluşurlar: ülke ve ülkeye bağlılık, ahlaki değerler, toplumsal sorumluluk, bilimsel yaklaşımlar, özgürlük ve demokrasinin değerleri, kişisel özgürlük, köy yaşamının önemine dair düşünceler, gelişme ve modernleşme stratejileri, halkın rolünün vurgulanması.  (Kaynak: milliyetci-hareketin-isimleri.md)
- **gelenek-1** (ozel_ad) Kut nedir?
  - Neden: eksik: Tanrı; kaynak yok; doğru parça ilk 3'te değil (sıra 4)
  - Cevap: Bu bilgi elimdedeki dokümanlarda yok.
- **takip-2#2** (takip) hangi yılda?
  - Önceki soru: Orhun Yazıtları'nın alfabesini kim çözmüştür?
  - Neden: eksik: 1893; yasak ifade: 1928; yanlış kaynak: turkcenin-tarihi-ve-alfabeleri.md; doğru parça ilk 3'te değil (sıra 5)
  - Cevap: 1 Kasım 1928'de Harf Devrimi kabul edilmiştir. Bu süreçte Türk alfabesine geçiş yapılmıştır.  (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)
- **degisim-3#2** (konu_degisimi) Kımız nedir?
  - Önceki soru: Turan taktiği nasıl uygulanır?
  - Neden: yanlış red (model); doğru parça ilk 3'te değil (sıra 30)
  - Cevap: Bu bilgi elimdeki dokümanlarda yok.

## Tüm sonuçlar

| id | Kategori | Sıra | En iyi skor | Eşikte red | Red | Anahtar | Kaynak | Süre | Sonuç |
|---|---|---|---|---|---|---|---|---|---|
| canakkale-1 | normal | 1 | 0.707 |  | evet |  |  | 1.4 | HATA |
| canakkale-2 | normal | 1 | 0.561 |  |  | tam | doğru | 1.9 | OK |
| canakkale-3 | normal | 1 | 0.572 |  |  | tam | doğru | 1.9 | OK |
| canakkale-4 | normal | 1 | 0.474 |  |  | tam | doğru | 1.6 | OK |
| canakkale-5 | normal | 1 | 0.485 |  |  | tam | doğru | 1.5 | OK |
| ilkturk-1 | normal | 3 | 0.714 |  | evet |  |  | 1.5 | HATA |
| ilkturk-2 | normal | 1 | 0.619 |  |  | tam | doğru | 1.5 | OK |
| ilkturk-3 | normal | 1 | 0.758 |  |  | tam | doğru | 1.6 | OK |
| ilkturk-4 | normal | 1 | 0.756 |  |  | tam | doğru | 1.6 | OK |
| ilkturk-5 | normal | 1 | 0.66 |  |  | tam | doğru | 1.5 | OK |
| isimler-1 | normal | 1 | 0.763 |  |  | tam | doğru | 1.9 | OK |
| isimler-2 | ozel_ad | 1 | 0.523 |  |  | eksik | doğru | 3.2 | HATA |
| isimler-3 | normal | 1 | 0.847 |  |  | tam | doğru | 1.7 | OK |
| isimler-4 | normal | 1 | 0.703 |  |  | tam | doğru | 2.0 | OK |
| isimler-5 | normal | 3 | 0.523 |  |  | tam | doğru | 1.7 | OK |
| isimler-6 | normal | 1 | 0.608 |  |  | tam | doğru | 1.6 | OK |
| ataturk-1 | normal | 1 | 0.673 |  |  | tam | doğru | 1.4 | OK |
| ataturk-2 | normal | 1 | 0.693 |  |  | tam | doğru | 1.8 | OK |
| ataturk-3 | normal | 1 | 0.479 |  |  | tam | doğru | 2.7 | OK |
| ataturk-4 | normal | 3 | 0.421 |  |  | tam | doğru | 1.8 | OK |
| ataturk-5 | normal | 1 | 0.59 |  |  | tam | doğru | 1.8 | OK |
| osmanli-1 | normal | 1 | 0.663 |  |  | tam | doğru | 2.1 | OK |
| osmanli-2 | ozel_ad | 1 | 0.566 |  |  | tam | doğru | 2.0 | OK |
| osmanli-3 | ozel_ad | 1 | 0.676 |  |  | tam | doğru | 1.5 | OK |
| osmanli-4 | ozel_ad | 1 | 0.574 |  |  | tam | doğru | 1.9 | OK |
| osmanli-5 | normal | 1 | 0.64 |  |  | tam | doğru | 1.7 | OK |
| osmanli-6 | normal | 1 | 0.705 |  |  | tam | doğru | 1.7 | OK |
| selcuklu-1 | normal | 1 | 0.748 |  |  | tam | doğru | 1.8 | OK |
| selcuklu-2 | normal | 1 | 0.663 |  |  | tam | doğru | 1.5 | OK |
| selcuklu-3 | normal | 1 | 0.756 |  |  | tam | doğru | 1.7 | OK |
| selcuklu-4 | normal | 1 | 0.779 |  |  | tam | doğru | 1.6 | OK |
| selcuklu-5 | normal | 1 | 0.484 |  |  | tam | doğru | 1.8 | OK |
| destan-1 | normal | 1 | 0.748 |  |  | tam | doğru | 1.4 | OK |
| destan-2 | normal | 1 | 0.776 |  |  | tam | doğru | 1.5 | OK |
| destan-3 | normal | 1 | 0.838 |  |  | tam | doğru | 2.0 | OK |
| destan-4 | normal | 1 | 0.628 |  |  | tam | doğru | 1.6 | OK |
| destan-5 | normal | 1 | 0.706 |  |  | tam | doğru | 1.8 | OK |
| gelenek-1 | ozel_ad | 4 | 0.559 |  |  | eksik | yok | 1.4 | HATA |
| gelenek-2 | ozel_ad | 1 | 0.642 |  |  | tam | doğru | 1.9 | OK |
| gelenek-3 | normal | 1 | 0.663 |  |  | tam | doğru | 1.5 | OK |
| gelenek-4 | normal | 1 | 0.455 |  |  | tam | doğru | 2.5 | OK |
| gelenek-5 | ozel_ad | 1 | 0.552 |  |  | tam | doğru | 1.8 | OK |
| at-1 | normal | 1 | 0.656 |  |  | tam | doğru | 2.3 | OK |
| at-2 | ozel_ad | 1 | 0.346 |  |  | tam | doğru | 1.4 | OK |
| at-3 | normal | 1 | 0.74 |  |  | tam | doğru | 2.6 | OK |
| at-4 | normal | 1 | 0.582 |  |  | tam | doğru | 1.5 | OK |
| kurt-1 | normal | 1 | 0.725 |  |  | tam | doğru | 1.5 | OK |
| kurt-2 | ozel_ad | 1 | 0.563 |  |  | tam | doğru | 2.8 | OK |
| kurt-3 | ozel_ad | 1 | 0.52 |  |  | tam | doğru | 2.1 | OK |
| kurt-4 | normal | 1 | 0.83 |  |  | tam | doğru | 1.7 | OK |
| kurt-5 | normal | 2 | 0.71 |  |  | tam | doğru | 1.5 | OK |
| kurt-6 | normal | 2 | 0.684 |  |  | tam | doğru | 1.7 | OK |
| dogus-1 | normal | 1 | 0.687 |  |  | tam | doğru | 1.8 | OK |
| dogus-2 | normal | 1 | 0.579 |  |  | tam | doğru | 1.6 | OK |
| dogus-3 | normal | 1 | 0.773 |  |  | tam | doğru | 1.8 | OK |
| dogus-4 | normal | 1 | 0.75 |  |  | tam | doğru | 1.4 | OK |
| alfabe-1 | normal | 1 | 0.719 |  |  | tam | doğru | 1.5 | OK |
| alfabe-2 | normal | 1 | 0.712 |  |  | tam | doğru | 1.6 | OK |
| alfabe-3 | normal | 2 | 0.76 |  |  | tam | doğru | 1.9 | OK |
| alfabe-4 | normal | 1 | 0.816 |  |  | tam | doğru | 1.4 | OK |
| alfabe-5 | normal | 1 | 0.462 |  |  | tam | doğru | 1.6 | OK |
| ulku-1 | normal | 1 | 0.727 |  |  | tam | doğru | 1.8 | OK |
| ulku-2 | normal | 1 | 0.636 |  |  | tam | doğru | 1.5 | OK |
| ulku-3 | normal | 1 | 0.693 |  |  | tam | doğru | 1.7 | OK |
| ulku-4 | normal | 1 | 0.787 |  |  | tam | doğru | 1.7 | OK |
| cevapsiz-1 | yakin |  | 0.652 |  | evet |  |  | 1.4 | OK |
| cevapsiz-2 | yakin |  | 0.691 |  | evet |  |  | 1.5 | OK |
| cevapsiz-3 | yakin |  | 0.575 |  | evet |  |  | 1.5 | OK |
| cevapsiz-4 | yakin |  | 0.521 |  | evet |  |  | 1.5 | OK |
| cevapsiz-5 | yakin |  | 0.659 |  | evet |  |  | 1.4 | OK |
| cevapsiz-6 | yakin |  | 0.516 |  | evet |  |  | 1.3 | OK |
| cevapsiz-7 | konu_disi |  | 0.317 | evet | evet |  |  | 0.3 | OK |
| cevapsiz-8 | konu_disi |  | 0.367 |  | evet |  |  | 1.4 | OK |
| cevapsiz-9 | konu_disi |  | 0.321 | evet | evet |  |  | 0.3 | OK |
| cevapsiz-10 | anlamsiz |  | 0.369 |  | evet |  |  | 1.3 | OK |
| takip-1#1 | hazirlik |  | 0.663 |  |  |  | var | 1.5 | - |
| takip-1#2 | takip | 1 | 0.681 |  |  | tam | doğru | 3.1 | OK |
| takip-2#1 | hazirlik |  | 0.742 |  | evet |  |  | 1.4 | - |
| takip-2#2 | takip | 5 | 0.734 |  |  | eksik | yanlış | 2.2 | HATA |
| takip-3#1 | hazirlik |  | 0.748 |  |  |  | var | 1.4 | - |
| takip-3#2 | takip | 1 | 0.79 |  |  | tam | doğru | 2.3 | OK |
| takip-4#1 | hazirlik |  | 0.705 |  |  |  | var | 1.7 | - |
| takip-4#2 | takip | 1 | 0.699 |  |  | tam | doğru | 2.1 | OK |
| takip-5#1 | hazirlik |  | 0.753 |  |  |  | var | 1.8 | - |
| takip-5#2 | takip | 1 | 0.726 |  |  | tam | doğru | 1.9 | OK |
| takip-cevapsiz-1#1 | hazirlik |  | 0.572 |  |  |  | var | 1.9 | - |
| takip-cevapsiz-1#2 | takip_cevapsiz |  | 0.579 |  | evet |  |  | 1.8 | OK |
| takip-cevapsiz-2#1 | hazirlik |  | 0.75 |  |  |  | var | 1.5 | - |
| takip-cevapsiz-2#2 | takip_cevapsiz |  | 0.511 |  | evet |  |  | 1.8 | OK |
| degisim-1#1 | hazirlik |  | 0.563 |  |  |  | var | 2.7 | - |
| degisim-1#2 | konu_degisimi | 1 | 0.566 |  |  | tam | doğru | 2.4 | OK |
| degisim-2#1 | hazirlik |  | 0.574 |  |  |  | var | 1.9 | - |
| degisim-2#2 | konu_degisimi | 1 | 0.563 |  |  | tam | doğru | 3.1 | OK |
| degisim-3#1 | hazirlik |  | 0.656 |  |  |  | var | 2.3 | - |
| degisim-3#2 | konu_degisimi | 30 | 0.657 |  | evet |  |  | 1.6 | HATA |
| degisim-4#1 | hazirlik |  | 0.712 |  |  |  | var | 1.6 | - |
| degisim-4#2 | konu_degisimi | 1 | 0.552 |  |  | tam | doğru | 2.3 | OK |
| disi-1#1 | hazirlik |  | 0.676 |  |  |  | var | 1.4 | - |
| disi-1#2 | konu_disi_sonra |  | 0.562 |  | evet |  |  | 1.7 | OK |
| disi-2#1 | hazirlik |  | 0.725 |  |  |  | var | 1.5 | - |
| disi-2#2 | konu_disi_sonra |  | 0.719 |  | evet |  |  | 1.9 | OK |
| disi-3#1 | hazirlik |  | 0.676 |  |  |  | var | 1.5 | - |
| disi-3#2 | konu_disi_sonra |  | 0.599 |  | evet |  |  | 1.7 | OK |
| disi-4#1 | hazirlik |  | 0.663 |  |  |  | var | 1.6 | - |
| disi-4#2 | konu_disi_sonra |  | 0.549 |  | evet |  |  | 1.8 | OK |

## Cevaplar (gözle kontrol için)

**canakkale-1** — Çanakkale Deniz Zaferi hangi tarihte kazanılmıştır?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `canakkale-ve-kurtulus-savasi.md#0 0.707 | canakkale-ve-kurtulus-savasi.md#3 0.658 | canakkale-ve-kurtulus-savasi.md#4 0.622`

**canakkale-2** — Gelibolu Yarımadası'na kara çıkarmaları ne zaman yapılmıştır?
> Gelibolu Yarımadası'na kara çıkarmaları 25 Nisan 1915'te yapılmıştır.  (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#1 0.561 | turkcenin-tarihi-ve-alfabeleri.md#3 0.426 | osmanli-padisahlari.md#1 0.407`

**canakkale-3** — Sakarya Meydan Muharebesi kaç gün sürmüştür?
> Sakarya Meydan Muharebesi 23 Ağustos - 13 Eylül 1921 tarihleri arasında yirmi iki gün süren bir muharebedir.  (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#3 0.572 | mustafa-kemal-ataturk.md#4 0.461 | milliyetci-hareketin-isimleri.md#7 0.457`

**canakkale-4** — Büyük Taarruz'da kesin sonuç nerede alınmıştır?
> Büyük Taarruz'un kesin sonuçları 30 Ağustos'ta Dumlupınar'da alınmıştır.  (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#4 0.474 | turk-devlet-gelenegi.md#2 0.453 | selcuklular-ve-malazgirt.md#0 0.422`

**canakkale-5** — Lozan Antlaşması ne zaman imzalanmıştır?
> Lozan Antlaşması 24 Temmuz 1923'te imzalanmıştır.  (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#4 0.485 | canakkale-ve-kurtulus-savasi.md#2 0.391 | osmanli-padisahlari.md#0 0.382`

**ilkturk-1** — Orhun Yazıtları'nın alfabesini kim ve hangi yılda çözmüştür?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.714 | ilk-turk-devletleri.md#2 0.660 | ilk-turk-devletleri.md#3 0.569`

**ilkturk-2** — Mete Han orduyu hangi sisteme göre düzenlemiştir?
> Mete Han orduyu onluk sisteme göre düzenlemiştir.  (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#0 0.619 | turk-devlet-gelenegi.md#3 0.415 | turk-devlet-gelenegi.md#1 0.412`

**ilkturk-3** — Göktürk Devleti ne zaman ve kimin önderliğinde kurulmuştur?
> Göktürk Devleti 552 yılında Bumin Kağan önderliğinde kurulmuştur.  (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#1 0.758 | ilk-turk-devletleri.md#4 0.659 | turk-milliyetciliginin-dogusu.md#4 0.585`

**ilkturk-4** — Orhun Yazıtları kimler adına dikilmiştir?
> Orhun Yazıtları, Tonyukuk, Kül Tigin ve Bilge Kağan adına dikilmiştir.  (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#2 0.756 | turkcenin-tarihi-ve-alfabeleri.md#0 0.613 | osmanli-padisahlari.md#1 0.491`

**ilkturk-5** — Uygur Kağanlığı hangi yıl kurulmuştur?
> Uygur Kağanlığı 744'te kurulmuştur.  (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#4 0.660 | turkcenin-tarihi-ve-alfabeleri.md#1 0.558 | ulku-ocaklari.md#0 0.549`

**isimler-1** — Milliyetçi Hareket Partisi adı hangi kongrede kabul edilmiştir?
> Milliyetçi Hareket Partisi adı 8-9 Şubat 1969'daki Adana kongresinde kabul edilmiştir.  (Kaynak: milliyetci-hareketin-isimleri.md)

Getirilen: `milliyetci-hareketin-isimleri.md#8 0.763 | milliyetci-hareketin-isimleri.md#13 0.634 | milliyetci-hareketin-isimleri.md#14 0.607`

**isimler-2** — Dokuz Işık ilkeleri nelerdir?
> Dokuz Işık ilkeleri, ülkeyi ve toplumu kalkınmış hale getirmek için Milliyetçi Hareket tarafından benimsenen ideolojik temellerdir ve şunlarla oluşurlar: ülke ve ülkeye bağlılık, ahlaki değerler, toplumsal sorumluluk, bilimsel yaklaşımlar, özgürlük ve demokrasinin değerleri, kişisel özgürlük, köy yaşamının önemine dair düşünceler, gelişme ve modernleşme stratejileri, halkın rolünün vurgulanması.  (Kaynak: milliyetci-hareketin-isimleri.md)

Getirilen: `milliyetci-hareketin-isimleri.md#9 0.523 | ilk-turk-devletleri.md#3 0.344 | milliyetci-hareketin-isimleri.md#16 0.344`

**isimler-3** — Alparslan Türkeş nerede doğmuştur?
> Alparslan Türkeş, Kıbrıs'ın Lefkoşa şehrinde 25 Kasım 1917'de doğmuştur.  (Kaynak: milliyetci-hareketin-isimleri.md)

Getirilen: `milliyetci-hareketin-isimleri.md#6 0.847 | turk-milliyetciliginin-dogusu.md#3 0.541 | milliyetci-hareketin-isimleri.md#10 0.539`

**isimler-4** — Nihal Atsız'ın Göktürk dönemini anlatan romanları hangileridir?
> Nihal Atsız'ın Göktürk dönemini anlatan romanları "Bozkurtların Ölümü" ve "Bozkurtlar Diriliyor" dir.  (Kaynak: milliyetci-hareketin-isimleri.md)

Getirilen: `milliyetci-hareketin-isimleri.md#4 0.703 | milliyetci-hareketin-isimleri.md#2 0.609 | milliyetci-hareketin-isimleri.md#1 0.607`

**isimler-5** — Büyük Birlik Partisi'ni kim kurmuştur?
> Büyük Birlik Partisi'ni Ocak 1993'te kurucu genel başkanı olarak Muhsin Yazıcıoğlu kurmuştur.  (Kaynak: milliyetci-hareketin-isimleri.md)

Getirilen: `milliyetci-hareketin-isimleri.md#8 0.523 | ulku-ocaklari.md#0 0.516 | milliyetci-hareketin-isimleri.md#14 0.512`

**isimler-6** — Türkçülük Günü olarak hangi tarih anılmaktadır?
> 3 Mayıs tarihi Türkçülük Günü olarak anılmaktadır.  (Kaynak: milliyetci-hareketin-isimleri.md)

Getirilen: `milliyetci-hareketin-isimleri.md#3 0.608 | turk-milliyetciliginin-dogusu.md#4 0.594 | ulku-ocaklari.md#2 0.588`

**ataturk-1** — Mustafa Kemal'in annesinin adı nedir?
> Mustafa Kemal'in annesinin adı Zübeyde Hanım'dır.  (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#0 0.673 | mustafa-kemal-ataturk.md#6 0.580 | mustafa-kemal-ataturk.md#1 0.551`

**ataturk-2** — Mustafa Kemal'e Kemal adını kim vermiştir?
> Selanik Askerî Rüştiyesi'nde matematik öğretmeni Mustafa Efendi, aynı adı taşımaları nedeniyle Kemal adını vermiştir.  (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#1 0.693 | mustafa-kemal-ataturk.md#0 0.688 | mustafa-kemal-ataturk.md#3 0.601`

**ataturk-3** — Nutuk ne zaman okunmuş ve yaklaşık kaç saat sürmüştür?
> Mustafa Kemal Atatürk, 15-20 Ekim 1927 tarihleri arasında Cumhuriyet Halk Partisi kongresinde Nutuk adlı konuşmasını okumuştur; bu konuşma yaklaşık otuz altı saat süren, 1919-1927 dönemini kendi anlatımıyla aktaran temel kaynaktır.  (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#5 0.479 | ilk-turk-devletleri.md#3 0.377 | milliyetci-hareketin-isimleri.md#1 0.360`

**ataturk-4** — "Yurtta sulh, cihanda sulh" sözü hangi yıl söylenmiştir?
> "Yurtta sulh, cihanda sulh" sözü 1931'de söylenmiştir.  (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `ulku-ocaklari.md#3 0.421 | milliyetci-hareketin-isimleri.md#3 0.407 | mustafa-kemal-ataturk.md#5 0.398`

**ataturk-5** — Atatürk'ün naaşı Anıtkabir'e ne zaman nakledilmiştir?
> Atatürk'ün naaşı Anıtkabir'e 10 Kasım 1953'te nakledilmiştir.  (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#6 0.590 | mustafa-kemal-ataturk.md#4 0.529 | mustafa-kemal-ataturk.md#5 0.493`

**osmanli-1** — Yavuz Sultan Selim hangi savaşlarla Mısır'ı Osmanlı topraklarına katmıştır?
> Yavuz Sultan Selim, 1516'da Mercidabık ve 1517'de Ridaniye savaşlarında Mısır'ı Osmanlı topraklarına katmıştır.  (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#3 0.663 | selcuklular-ve-malazgirt.md#1 0.542 | mustafa-kemal-ataturk.md#3 0.541`

**osmanli-2** — fatih kimdir
> Fatih Sultan Mehmed, 29 Mayıs 1453'te İstanbul'u fethettiğinde yirmi bir yaşındaydı. Fetihle birlikte Osmanlı Devleti imparatorluğuna dönüşmüş, Osmanlı Padişahları dönemini başlatmıştır.  (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#2 0.566 | milliyetci-hareketin-isimleri.md#17 0.517 | milliyetci-hareketin-isimleri.md#1 0.485`

**osmanli-3** — Osman Gazi kimdir
> Osman Gazi, Osmanlı Devleti'nin kurucusudur.  (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#0 0.676 | osmanli-padisahlari.md#1 0.659 | osmanli-padisahlari.md#4 0.526`

**osmanli-4** — Orhan Gazi kimdir
> Orhan Gazi, Osmanlı Padişahları döneminde belirleyici bir hükümdardır. Kuruluş döneminin önemli figürü olan Orhan Gazi, Bursa'yı alarak Rumeli'ye geçiş yapmıştır.  (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#1 0.574 | osmanli-padisahlari.md#0 0.465 | turkcenin-tarihi-ve-alfabeleri.md#0 0.456`

**osmanli-5** — Yıldırım Bayezid Ankara Savaşı'nda kime yenilmiştir?
> Yıldırım Bayezid, Ankara Savaşı'nda Timur'e yenilmiştir.  (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#1 0.640 | canakkale-ve-kurtulus-savasi.md#2 0.556 | selcuklular-ve-malazgirt.md#2 0.532`

**osmanli-6** — Kanuni Sultan Süleyman kaç yıl hüküm sürmüştür?
> Kanuni Sultan Süleyman, 1520-1566 yılları arasında kırk altı yıl hüküm sürmüştür.  (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#4 0.705 | osmanli-padisahlari.md#0 0.570 | osmanli-padisahlari.md#2 0.519`

**selcuklu-1** — Anadolu Selçuklu Devleti hangi savaşta Moğollara yenilmiştir?
> Selçuklular Anadolu Selçuklu Devleti 1243'teki Kösedağ Savaşı'nda Moğollara yenilmiştir.  (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#4 0.748 | selcuklular-ve-malazgirt.md#3 0.675 | selcuklular-ve-malazgirt.md#2 0.612`

**selcuklu-2** — Malazgirt Savaşı ne zaman yapılmıştır?
> Malazgirt Savaşı 26 Ağustos 1071'de yapılmıştır.  (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.663 | selcuklular-ve-malazgirt.md#2 0.660 | selcuklular-ve-malazgirt.md#0 0.634`

**selcuklu-3** — Büyük Selçuklu Devleti'nin kuruluşunu kesinleştiren savaş hangisidir?
> Dandanakan Savaşı, Büyük Selçuklu Devleti'nin kuruluşunu kesinleştiren savaştır.  (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#0 0.756 | selcuklular-ve-malazgirt.md#3 0.647 | selcuklular-ve-malazgirt.md#2 0.606`

**selcuklu-4** — Anadolu Selçuklu Devleti'ni kim kurmuştur?
> İznik merkezli Anadolu Selçuklu Devleti'ni Süleyman Şah kurmuştur.  (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#3 0.779 | selcuklular-ve-malazgirt.md#0 0.691 | selcuklular-ve-malazgirt.md#4 0.626`

**selcuklu-5** — Miryokefalon Savaşı'nın sonucu ne olmuştur?
> Miryokefalon Savaşı'nda Bizans'ın Anadolu'yuna geri alma girişimi başarısız olmuş, Anadolu'nun Türk yurdu olduğu kesinleşmiştir.  (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#3 0.484 | canakkale-ve-kurtulus-savasi.md#3 0.467 | selcuklular-ve-malazgirt.md#4 0.457`

**destan-1** — Manas Destanı hangi topluma aittir?
> Manas Destanı Kırgızlara aittır.  (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#3 0.748 | turk-destanlari.md#1 0.527 | turk-destanlari.md#0 0.476`

**destan-2** — Dede Korkut Kitabı kaç hikâyeden oluşur?
> Dede Korkut Kitabı on iki hikâyeden oluşur.  (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.776 | turk-kulturunde-at.md#4 0.575 | turk-kulturunde-kurt.md#2 0.503`

**destan-3** — Oğuz Kağan Destanı'na göre Oğuz Kağan'ın kaç oğlu vardır?
> Oğuz Kağan Destanı'na göre Oğuz Kağan altı oğlu vardır. Bu oğullardan yirmi dört Oğuz boyunun türediği anlatılmaktadır.  (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#1 0.838 | turk-destanlari.md#0 0.552 | turk-destanlari.md#3 0.552`

**destan-4** — Ergenekon'dan çıkış günü nasıl kutlanmıştır?
> Ergenekon Destanı'nda çıkış günü, bazı Türk topluluklarında bahar bayramı olarak kutlanmıştır.  (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#2 0.628 | turk-kulturunde-kurt.md#2 0.446 | ulku-ocaklari.md#2 0.423`

**destan-5** — Dede Korkut kültürü UNESCO listesine hangi yıl alınmıştır?
> Dede Korkut kültürü 2018'de UNESCO İnsanlığın Somut Olmayan Kültürel Mirası listesine alınmıştır.  (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.706 | turk-kulturunde-at.md#4 0.450 | turk-kulturunde-kurt.md#6 0.442`

**gelenek-1** — Kut nedir?
> Bu bilgi elimdedeki dokümanlarda yok.

Getirilen: `turk-kulturunde-kurt.md#6 0.559 | turk-kulturunde-kurt.md#0 0.519 | turk-kulturunde-kurt.md#5 0.493`

**gelenek-2** — Töre nedir?
> Töre, yazılı olmayan hukuk düzenidir ve değiştirilmesi için kurultayın onayını gerektirirdi. Hükümdar bile töreye uymak zorunda kalırdı.  (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#1 0.642 | turk-devlet-gelenegi.md#4 0.414 | turk-devlet-gelenegi.md#3 0.412`

**gelenek-3** — Kurultayda hangi konular görüşülürdü?
> Savaş, barış ve hükümdar seçimi gibi konular kurultayda görüşülürdü.  (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#2 0.663 | turk-kulturunde-kurt.md#2 0.589 | turk-kulturunde-kurt.md#4 0.555`

**gelenek-4** — İkili teşkilat nedir?
> İkili teşkilat, ülkenin doğu ve batı olmak üzere iki idari kanaya ayrılmasıdır. Doğu kanadı daha üstün sayılır ve büyük kağan orada bulunurdu; batı kanadını genellikle hanedandan bir başka üye yönetirdi. Bu düzen, bozkır coğrafyasının yönetilmesinde zorluğa bir çözüm sunmuştur.  (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#3 0.455 | turk-kulturunde-at.md#2 0.406 | milliyetci-hareketin-isimleri.md#7 0.349`

**gelenek-5** — Tuğ nedir?
> Tuğ, at kılıncından yapılmış ve sırık üzerinde taşınan bir bayrak niteliğindeki semboldür. Sayısı hükümdarın rütbesine göre değişebilir.  (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#4 0.552 | turk-destanlari.md#1 0.477 | turk-devlet-gelenegi.md#0 0.465`

**at-1** — Turan taktiği nasıl uygulanır?
> Turan taktiği, merkez birlikler sahte bir geri çekilme yapar ve düşman takibe başladığında, kanatlar hilal biçiminde kapanarak düşmana kuşatma oluşturur. Bu taktik, Türk ordularının atlı okçuluk becerilerinin ve hareket üstünlüğünün kullanıldığı bir yöntemdir.  (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#1 0.656 | turk-devlet-gelenegi.md#1 0.501 | turk-devlet-gelenegi.md#2 0.456`

**at-2** — Kımız nedir?
> Kımız, kısrak sütünün mayalanmasıyla elde edilen içecektir.  (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#3 0.346 | turk-kulturunde-kurt.md#6 0.330 | turk-kulturunde-at.md#0 0.298`

**at-3** — Üzengi atlı savaşa ne kazandırmıştır?
> Üzengi, atlı savaşta binicinin at üstünde daha iyi denge sağlayarak iki elini birden kullanabilmesini ve mızrak darbesine daha fazla vücut ağırlığını verebilmelerini mümkün kılmıştır. Bu, savaşta daha etkili bir şekilde hareket edebilmelerini ve daha iyi bir kontrol sahibi olmalarını sağlaymıştır.  (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#2 0.740 | turk-kulturunde-at.md#1 0.629 | selcuklular-ve-malazgirt.md#2 0.511`

**at-4** — Hangi at ırkları dayanıklılıklarıyla bilinir?
> Ahal Teke ve Türkmen atı dayanıklılıklarıyla bilinir.  (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#4 0.582 | turk-kulturunde-at.md#0 0.531 | turk-kulturunde-at.md#3 0.520`

**kurt-1** — Eski Türkçede kurdun adı neydi?
> Eski Türkçede kurdun adı "böri" idi.  (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.725 | turk-kulturunde-kurt.md#6 0.612 | turk-kulturunde-kurt.md#4 0.591`

**kurt-2** — böri nedir
> Böri, Türkçede eski adı olan kurtun eski adıdır. Eski Türkçede kurdan kullanılan bu terim, bugün Kazakçada börı, Kırgızcada börü, Özbekçede bo'ri olarak kullanılmaktadır. Türkçede "böri" sözcüğü bugün "bozkurt" ve destan kahramanı "Börteçine" gibi kalıplarda kullanılıyormaktadır.  (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.563 | turk-kulturunde-kurt.md#6 0.456 | turk-kulturunde-at.md#0 0.442`

**kurt-3** — Aşina hanedanının soyu nereden gelir?
> Aşina hanedanının soyu bir dişi kurttan gelir. Kurtdan sağ kurtulan bir çocuğun dişi bir kurt tarafından beslendiği ve soyun ondan devam ettiği anlatılmaktadır.  (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#1 0.520 | milliyetci-hareketin-isimleri.md#20 0.329 | milliyetci-hareketin-isimleri.md#1 0.323`

**kurt-4** — Eski Türkçede kurt kelimesinin anlamı neydi?
> Eski Türkçede kurt kelimesinin anlamı solucan, kurtçuk, böcek larvasıydı.  (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#6 0.830 | turk-kulturunde-kurt.md#5 0.724 | turk-kulturunde-kurt.md#3 0.688`

**kurt-5** — Azerbaycan Türkçesinde kurda ne denir?
> Azerbaycan Türkçesinde kurta "canavar" adı verilir.  (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.710 | turk-kulturunde-kurt.md#6 0.705 | turk-kulturunde-kurt.md#4 0.658`

**kurt-6** — Ergenekon'dan çıkan topluluğa yolu kim göstermiştir?
> Ergenenekon Destanı'nda, topluluğa yolu Börteçine adlı bozkurt göstermiştir.  (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-destanlari.md#2 0.684 | turk-kulturunde-kurt.md#2 0.527 | turk-devlet-gelenegi.md#3 0.463`

**dogus-1** — Üç Tarz-ı Siyaset yazısı nerede ve hangi yıl yayımlanmıştır?
> Üç Tarz-ı Siyaset yazısı 1904'te Kahire'de yayımlanmıştır.  (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#1 0.687 | mustafa-kemal-ataturk.md#5 0.460 | turk-devlet-gelenegi.md#1 0.453`

**dogus-2** — Türkçülüğün Esasları kimin eseridir?
> Türkçülüğün Esasları eseri Ziya Gökalp tarafından yazılmıştır.  (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#2 0.579 | turk-destanlari.md#0 0.557 | milliyetci-hareketin-isimleri.md#4 0.542`

**dogus-3** — İsmail Gaspıralı hangi ilkeyi savunmuştur?
> İsmail Gaspıralı, "Dilde, fikirde, işte birlik" ilkesini savunmuştur.  (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#3 0.773 | turk-milliyetciliginin-dogusu.md#2 0.509 | osmanli-padisahlari.md#1 0.507`

**dogus-4** — Türk Ocağı ne zaman kurulmuştur?
> Türk Ocağı 25 Mart 1912'de kurulmuştur.  (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.750 | ulku-ocaklari.md#0 0.669 | ulku-ocaklari.md#2 0.664`

**alfabe-1** — Göktürk alfabesi kaç işaretten oluşur?
> Göktürk alfabesi otuz sekiz işaretten oluşur.  (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.719 | turkcenin-tarihi-ve-alfabeleri.md#3 0.648 | turkcenin-tarihi-ve-alfabeleri.md#4 0.607`

**alfabe-2** — Harf Devrimi hangi tarihte kabul edilmiştir?
> Harf Devrimi 1 Kasım 1928'de kabul edilmiştir.  (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#3 0.712 | turkcenin-tarihi-ve-alfabeleri.md#4 0.555 | ilk-turk-devletleri.md#3 0.530`

**alfabe-3** — Türk Dil Kurumu ne zaman kurulmuştur?
> Türk Dil Kurumu, 12 Temmuz 1932'de kurulan Türk Dili Tetkik Cemiyeti olarak kuruldu ve bugüne kadar faaliyet göstermektedir.  (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.760 | turkcenin-tarihi-ve-alfabeleri.md#4 0.760 | turkcenin-tarihi-ve-alfabeleri.md#3 0.626`

**alfabe-4** — Uygur alfabesi hangi yazıdan uyarlanmıştır?
> Uygur alfabesi Soğd yazısından uyarlanmıştır.  (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#1 0.816 | turkcenin-tarihi-ve-alfabeleri.md#0 0.663 | turkcenin-tarihi-ve-alfabeleri.md#3 0.643`

**alfabe-5** — Kutadgu Bilig hangi yüzyılda yazılmıştır?
> Kutadgu Bilig, on birinci yüzyılda yazılmıştır.  (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#2 0.462 | turk-kulturunde-kurt.md#5 0.403 | turk-destanlari.md#4 0.388`

**ulku-1** — Ülkü Ocakları 12 Mart 1971'den sonra hangi adla yeniden kurulmuştur?
> Ülkü Ocakları, 12 Mart 1971'den sonra Ülkü Ocakları Derneği adıyla yeniden kurulmuştur.  (Kaynak: ulku-ocaklari.md)

Getirilen: `ulku-ocaklari.md#2 0.727 | ulku-ocaklari.md#0 0.636 | ulku-ocaklari.md#1 0.627`

**ulku-2** — Ülkü Ocakları 1978'de hangi adı almıştır?
> Ülkü Ocakları 1978'de Ülkücü Gençlik Derneği adını almıştır.  (Kaynak: ulku-ocaklari.md)

Getirilen: `ulku-ocaklari.md#2 0.636 | ulku-ocaklari.md#1 0.622 | ulku-ocaklari.md#3 0.607`

**ulku-3** — Ülkü Ocakları bugün hangi adla faaliyet göstermektedir?
> Ülkü Ocakları günümüzde Ülkü Ocakları Eğitim ve Kültür Vakfı adıyla faaliyet göstermektedir.  (Kaynak: ulku-ocaklari.md)

Getirilen: `ulku-ocaklari.md#4 0.693 | ulku-ocaklari.md#0 0.633 | ulku-ocaklari.md#2 0.606`

**ulku-4** — Ülkü Ocakları Birliği adı altında merkezi örgütlenme hangi dönemde olmuştur?
> 1969-1970 döneminde Ülkü Ocakları Birliği adı altında merkezi örgütlenme olmuştur.  (Kaynak: ulku-ocaklari.md)

Getirilen: `ulku-ocaklari.md#1 0.787 | ulku-ocaklari.md#0 0.710 | ulku-ocaklari.md#2 0.674`

**cevapsiz-1** — Fatih Sultan Mehmed'in annesinin adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-padisahlari.md#2 0.652 | osmanli-padisahlari.md#4 0.508 | mustafa-kemal-ataturk.md#0 0.500`

**cevapsiz-2** — Malazgirt Savaşı'nda Selçuklu ordusu kaç askerden oluşuyordu?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `selcuklular-ve-malazgirt.md#0 0.691 | selcuklular-ve-malazgirt.md#1 0.675 | selcuklular-ve-malazgirt.md#2 0.643`

**cevapsiz-3** — Kanuni Sultan Süleyman'ın eşinin adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-padisahlari.md#4 0.575 | osmanli-padisahlari.md#2 0.497 | osmanli-padisahlari.md#0 0.487`

**cevapsiz-4** — Lozan Antlaşması'nı Türk heyeti adına kim imzalamıştır?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `canakkale-ve-kurtulus-savasi.md#4 0.521 | milliyetci-hareketin-isimleri.md#6 0.476 | milliyetci-hareketin-isimleri.md#7 0.469`

**cevapsiz-5** — Orhun Yazıtları bugün hangi müzede sergilenmektedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `ilk-turk-devletleri.md#2 0.659 | turkcenin-tarihi-ve-alfabeleri.md#0 0.568 | turk-devlet-gelenegi.md#1 0.463`

**cevapsiz-6** — Mete Han'ın babasının adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `ilk-turk-devletleri.md#0 0.516 | mustafa-kemal-ataturk.md#0 0.393 | osmanli-padisahlari.md#2 0.367`

**cevapsiz-7** — Bugün hava nasıl olacak?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-kulturunde-kurt.md#6 0.317 | turk-kulturunde-at.md#3 0.297 | turk-kulturunde-kurt.md#2 0.290`

**cevapsiz-8** — Python'da bir liste nasıl sıralanır?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.367 | turk-destanlari.md#0 0.307 | turkcenin-tarihi-ve-alfabeleri.md#4 0.296`

**cevapsiz-9** — Futbolda ofsayt kuralı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-kulturunde-kurt.md#6 0.321 | turk-kulturunde-at.md#1 0.320 | ulku-ocaklari.md#0 0.315`

**cevapsiz-10** — asdf qwerty zxcv
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.369 | turkcenin-tarihi-ve-alfabeleri.md#1 0.326 | ilk-turk-devletleri.md#3 0.326`

**takip-1#1** — Malazgirt Savaşı ne zaman yapılmıştır?
> Malazgirt Savaşı 26 Ağustos 1071'de yapılmıştır.  (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.663 | selcuklular-ve-malazgirt.md#2 0.660 | selcuklular-ve-malazgirt.md#0 0.634`

**takip-1#2** — sonucu ne oldu?  
_Önceki soru: Malazgirt Savaşı ne zaman yapılmıştır?_
> Savaşın sonuçları Selçukluların zaferi ve Bizans İmparatoru IV. Romanos'un esir alınması oldu. Ayrıca, Bizans'ın Anadolu'daki savunma düzeninin çökmesi ve Türkmen boylarının Anadolu içlerine yerleşmesi de önemli sonuclar arasında sayılabilir. Bu nedenle 1071 yılı, Anadolu'nun Türkleşme sürecinin başlangıcı olarak kabul edilir.  (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.681 | selcuklular-ve-malazgirt.md#2 0.668 | selcuklular-ve-malazgirt.md#0 0.634`

**takip-2#1** — Orhun Yazıtları'nın alfabesini kim çözmüştür?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.742 | ilk-turk-devletleri.md#2 0.663 | turkcenin-tarihi-ve-alfabeleri.md#1 0.580`

**takip-2#2** — hangi yılda?  
_Önceki soru: Orhun Yazıtları'nın alfabesini kim çözmüştür?_
> 1 Kasım 1928'de Harf Devrimi kabul edilmiştir. Bu süreçte Türk alfabesine geçiş yapılmıştır.  (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.734 | ilk-turk-devletleri.md#2 0.673 | turkcenin-tarihi-ve-alfabeleri.md#3 0.586`

**takip-3#1** — Manas Destanı hangi topluma aittir?
> Manas Destanı Kırgızlara aittır.  (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#3 0.748 | turk-destanlari.md#1 0.527 | turk-destanlari.md#0 0.476`

**takip-3#2** — kaç dizeden oluşur?  
_Önceki soru: Manas Destanı hangi topluma aittir?_
> Manas Destanı, farklı derlemelerde yarım milyon dizeye yaklaşır. Bu destanın tam adedi belirtilmediği için tam sayı dize sayısını belirtmek mümkün değil.  (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#3 0.790 | turk-destanlari.md#1 0.548 | turk-destanlari.md#0 0.503`

**takip-4#1** — Kanuni Sultan Süleyman kaç yıl hüküm sürmüştür?
> Kanuni Sultan Süleyman, 1520-1566 yılları arasında kırk altı yıl hüküm sürmüştür.  (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#4 0.705 | osmanli-padisahlari.md#0 0.570 | osmanli-padisahlari.md#2 0.519`

**takip-4#2** — onun döneminde hangi şehir kuşatıldı?  
_Önceki soru: Kanuni Sultan Süleyman kaç yıl hüküm sürmüştür?_
> Vienna kuşatılmıştır. Kanuni Sultan Süleyman döneminde 1529'da Viyana kuşatılmıştır.  (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#4 0.699 | selcuklular-ve-malazgirt.md#3 0.597 | osmanli-padisahlari.md#0 0.575`

**takip-5#1** — İsmail Gaspıralı hangi gazeteyi çıkarmıştır?
> Ismail Gaspıralı, 1883'te Kırım'da Tercüman gazetesini çıkarmıştır.  (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#3 0.753 | turk-milliyetciliginin-dogusu.md#2 0.502 | milliyetci-hareketin-isimleri.md#6 0.482`

**takip-5#2** — bu gazete nerede çıkarıldı?  
_Önceki soru: İsmail Gaspıralı hangi gazeteyi çıkarmıştır?_
> Tercüman gazetesinin Kırım'da çıkarıldığı belirtilmiştir.  (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#3 0.726 | milliyetci-hareketin-isimleri.md#6 0.475 | turk-milliyetciliginin-dogusu.md#2 0.473`

**takip-cevapsiz-1#1** — Sakarya Meydan Muharebesi kaç gün sürmüştür?
> Sakarya Meydan Muharebesi 23 Ağustos - 13 Eylül 1921 tarihleri arasında yirmi iki gün süren bir muharebedir.  (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#3 0.572 | mustafa-kemal-ataturk.md#4 0.461 | milliyetci-hareketin-isimleri.md#7 0.457`

**takip-cevapsiz-1#2** — bunun sebebi ne?  
_Önceki soru: Sakarya Meydan Muharebesi kaç gün sürmüştür?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `canakkale-ve-kurtulus-savasi.md#3 0.579 | mustafa-kemal-ataturk.md#4 0.463 | milliyetci-hareketin-isimleri.md#3 0.458`

**takip-cevapsiz-2#1** — Türk Ocağı ne zaman kurulmuştur?
> Türk Ocağı 25 Mart 1912'de kurulmuştur.  (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.750 | ulku-ocaklari.md#0 0.669 | ulku-ocaklari.md#2 0.664`

**takip-cevapsiz-2#2** — ilk başkanı kimdi?  
_Önceki soru: Türk Ocağı ne zaman kurulmuştur?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `ilk-turk-devletleri.md#0 0.511 | mustafa-kemal-ataturk.md#5 0.497 | ilk-turk-devletleri.md#1 0.491`

**degisim-1#1** — böri nedir
> Böri, Türkçede eski adı olan kurtun eski adıdır. Eski Türkçede kurdan kullanılan bu terim, bugün Kazakçada börı, Kırgızcada börü, Özbekçede bo'ri olarak kullanılmaktadır. Türkçede "böri" sözcüğü bugün "bozkurt" ve destan kahramanı "Börteçine" gibi kalıplarda kullanılıyormaktadır.  (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.563 | turk-kulturunde-kurt.md#6 0.456 | turk-kulturunde-at.md#0 0.442`

**degisim-1#2** — fatih kimdir  
_Önceki soru: böri nedir_
> Fatih Sultan Mehmed, 29 Mayıs 1453'te İstanbul'u fethettiğinde yirmi bir yaşındaydı. Fetihle birlikte Osmanlı Devleti imparatorluğuna dönüşmüş, Osmanlı Padişahları dönemini başlatmıştır.  (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#2 0.566 | milliyetci-hareketin-isimleri.md#17 0.517 | milliyetci-hareketin-isimleri.md#1 0.485`

**degisim-2#1** — Orhan Gazi kimdir
> Orhan Gazi, Osmanlı Padişahları döneminde belirleyici bir hükümdardır. Kuruluş döneminin önemli figürü olan Orhan Gazi, Bursa'yı alarak Rumeli'ye geçiş yapmıştır.  (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#1 0.574 | osmanli-padisahlari.md#0 0.465 | turkcenin-tarihi-ve-alfabeleri.md#0 0.456`

**degisim-2#2** — böri nedir  
_Önceki soru: Orhan Gazi kimdir_
> Böri, Türkçede eski adı olan kurtun eski adıdır. Eski Türkçede kurdan kullanılan bu terim, bugün Kazakçada börı, Kırgızcada börü, Özbekçede bo'ri olarak kullanılmaktadır. Türkçede "böri" sözcüğü bugün "bozkurt" ve destan kahramanı "Börteçine" gibi kalıplarda kullanılıyormaktadır.  (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.563 | turk-kulturunde-kurt.md#6 0.456 | turk-kulturunde-at.md#0 0.442`

**degisim-3#1** — Turan taktiği nasıl uygulanır?
> Turan taktiği, merkez birlikler sahte bir geri çekilme yapar ve düşman takibe başladığında, kanatlar hilal biçiminde kapanarak düşmana kuşatma oluşturur. Bu taktik, Türk ordularının atlı okçuluk becerilerinin ve hareket üstünlüğünün kullanıldığı bir yöntemdir.  (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#1 0.656 | turk-devlet-gelenegi.md#1 0.501 | turk-devlet-gelenegi.md#2 0.456`

**degisim-3#2** — Kımız nedir?  
_Önceki soru: Turan taktiği nasıl uygulanır?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-kulturunde-at.md#1 0.657 | turk-devlet-gelenegi.md#1 0.524 | turk-devlet-gelenegi.md#2 0.479`

**degisim-4#1** — Harf Devrimi hangi tarihte kabul edilmiştir?
> Harf Devrimi 1 Kasım 1928'de kabul edilmiştir.  (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#3 0.712 | turkcenin-tarihi-ve-alfabeleri.md#4 0.555 | ilk-turk-devletleri.md#3 0.530`

**degisim-4#2** — Tuğ nedir?  
_Önceki soru: Harf Devrimi hangi tarihte kabul edilmiştir?_
> Tuğ, at kılıncından yapılmış ve sırık üzerinde taşınan bir bayrak niteliğindeki semboldür. Sayısı hükümdarın rütbesine göre değişebilir.  (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#4 0.552 | turk-destanlari.md#1 0.477 | turk-devlet-gelenegi.md#0 0.465`

**disi-1#1** — Osman Gazi kimdir
> Osman Gazi, Osmanlı Devleti'nin kurucusudur.  (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#0 0.676 | osmanli-padisahlari.md#1 0.659 | osmanli-padisahlari.md#4 0.526`

**disi-1#2** — Bugün hava nasıl olacak?  
_Önceki soru: Osman Gazi kimdir_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-padisahlari.md#0 0.562 | osmanli-padisahlari.md#1 0.541 | turk-destanlari.md#1 0.506`

**disi-2#1** — Eski Türkçede kurdun adı neydi?
> Eski Türkçede kurdun adı "böri" idi.  (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.725 | turk-kulturunde-kurt.md#6 0.612 | turk-kulturunde-kurt.md#4 0.591`

**disi-2#2** — asdf qwerty zxcv  
_Önceki soru: Eski Türkçede kurdun adı neydi?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-kulturunde-kurt.md#5 0.719 | turk-kulturunde-kurt.md#6 0.615 | turk-kulturunde-kurt.md#4 0.587`

**disi-3#1** — Osman Gazi kimdir
> Osman Gazi, Osmanlı Devleti'nin kurucusudur.  (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#0 0.676 | osmanli-padisahlari.md#1 0.659 | osmanli-padisahlari.md#4 0.526`

**disi-3#2** — Python listesi nasıl sıralanır?  
_Önceki soru: Osman Gazi kimdir_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-padisahlari.md#0 0.599 | osmanli-padisahlari.md#1 0.581 | turk-destanlari.md#1 0.523`

**disi-4#1** — Malazgirt Savaşı ne zaman yapılmıştır?
> Malazgirt Savaşı 26 Ağustos 1071'de yapılmıştır.  (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.663 | selcuklular-ve-malazgirt.md#2 0.660 | selcuklular-ve-malazgirt.md#0 0.634`

**disi-4#2** — Futbolda ofsayt kuralı nedir?  
_Önceki soru: Malazgirt Savaşı ne zaman yapılmıştır?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `selcuklular-ve-malazgirt.md#0 0.549 | selcuklular-ve-malazgirt.md#2 0.544 | selcuklular-ve-malazgirt.md#1 0.534`

