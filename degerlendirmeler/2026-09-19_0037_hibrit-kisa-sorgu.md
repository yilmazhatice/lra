# Değerlendirme: 2026-09-19 00:37 — hibrit-kisa-sorgu

| Ayar | Değer |
|---|---|
| soru_seti | ana |
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
| arama | yalnız vektör |
| cevap_dogrulama | kapalı |
| git | dbeaba1 (kaydedilmemis degisiklik var) |
| set_parmak_izi | 624685f095 |

## Özet

Puanlanan soru: 160 (144 cevaplanabilir, 16 cevaplanamaz). Senaryoların hazırlık soruları özete katılmaz.

Karşılaştırılan çalışma: `degerlendirmeler/2026-09-18_2208_belge-siniri-080.json`

| Ölçüt | Önceki | Şimdi |
|---|---|---|
| Tam başarı (tüm puanlanan sorular) | 96.9% | 96.9% |
| Arama: doğru parça 1. sırada (hit@1) | 86.1% | 87.5% |
| Arama: doğru parça ilk 3'te (hit@3) | 96.5% | 97.2% |
| Arama: MRR (1 = hep 1. sırada) | 0.916 | 0.924 |
| Cevaplanabilir sorularda başarı | 99.3% | 99.3% |
| Yanlış red (cevap belgede varken) | 0.0% | 0.0% |
|   bunun eşikte olanı | 0.0% | 0.0% |
| Anahtar ifadelerin tamamı cevapta | 99.3% | 99.3% |
| Bilinen yanlışı içeren cevap | 1 adet | 1 adet |
| Kaynak satırı var | 100.0% | 100.0% |
| Kaynak doğru belge | 99.3% | 99.3% |
| Cevaplanamaz soruları reddetme | 75.0% | 75.0% |
|   bunun eşikte olanı | 0.0% | 0.0% |
| Red cevabına eklenmiş kaynak satırı | 0 adet | 0 adet |
| Doğrulamada reddedilen cevaplanabilir | 0 adet | 0 adet |
| Doğrulamada reddedilen cevaplanamaz | 0 adet | 0 adet |
| Türkçe olmayan yazı kalan cevap | 0 adet | 0 adet |
| Türkçe olmayan yazı kesilen cevap | 0 adet | 0 adet |
| Süre ortalaması | 4.01 sn | 2.28 sn |
| Süre medyanı | 4.34 sn | 2.2 sn |
| En uzun süre | 7.1 sn | 4.74 sn |
| İlk token ortalaması (modele giden sorular) | 2.69 sn | 0.93 sn |
| Arama süresi ortalaması | 0.424 sn | 0.424 sn |

## Kategorilere göre

| Kategori | Soru | Başarılı | hit@1 | hit@3 | Yanlış red |
|---|---|---|---|---|---|
| normal | 106 | 106 | 93 | 103 | 0 |
| ozel_ad | 29 | 29 | 25 | 29 | 0 |
| yakin | 6 | 5 | - | - | - |
| konu_disi | 3 | 3 | - | - | - |
| anlamsiz | 1 | 1 | - | - | - |
| takip | 5 | 4 | 4 | 4 | 0 |
| takip_cevapsiz | 2 | 0 | - | - | - |
| konu_degisimi | 4 | 4 | 4 | 4 | 0 |
| konu_disi_sonra | 4 | 3 | - | - | - |
| hazirlik (puanlanmaz) | 15 | - | - | - | - |

Eski 12 soruluk set (eval_results.md ile aynı sorular): **10/10** başarılı.

## Önceki çalışmaya göre değişen sorular

Cevap metni değişen soru: 21. Sonucu değişen soru: 0.


## Başarısız sorular

- **cevapsiz-4** (yakin) Lozan Antlaşması'nı Türk heyeti adına kim imzalamıştır?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Lozan Antlaşması'nı Türk heyeti adına İsmet İnönü imzalamıştır. (Kaynak: canakkale-ve-kurtulus-savasi.md)
- **takip-2#2** (takip) hangi yılda?
  - Önceki soru: Orhun Yazıtları'nın alfabesini kim çözmüştür?
  - Neden: eksik: 1893; yasak ifade: 1928; yanlış kaynak: turkcenin-tarihi-ve-alfabeleri.md; doğru parça ilk 3'te değil (sıra 5)
  - Cevap: 1 Kasım 1928'de kabul edilen Harf Devrimi ile Latin alfabesine dayalı yeni Türk alfabesine geçilmiştir. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)
- **takip-cevapsiz-1#2** (takip_cevapsiz) bunun sebebi ne?
  - Önceki soru: Sakarya Meydan Muharebesi kaç gün sürmüştür?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Osmanlı'da yeniden yapılanma sürecinin temel sebeplerinden biri, devletin çevresindeki güç dengesinin değişmesidir. İran savaşlarının uzun süreceği ve Avusturya ile olan anlaşmanın protokol açısından Osmanlı padişahına denk sayılması gibi olaylar, Osmanlı devletinin iç ve dış durumunu değiştirdiği ve reformların gerekliliğini artırarak reform hareketlerinin başlamasını sağlamıştır. (Kaynak: osmanli-islahat-ve-mesrutiyet.md)
- **takip-cevapsiz-2#2** (takip_cevapsiz) ilk başkanı kimdi?
  - Önceki soru: Türk Ocağı ne zaman kurulmuştur?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Mustafa Kemal Atatürk, 29 Ekim 1923'te Cumhuriyet'in ilanıyla Türkistan Cumhuriyeti'nin ilk cumhurbaşkanı seçildi. (Kaynak: mustafa-kemal-ataturk.md)
- **disi-3#2** (konu_disi_sonra) Python listesi nasıl sıralanır?
  - Önceki soru: Osman Gazi kimdir
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Python listesi sıralanırken genellikle aşağıdaki adımlar izlenir:  - Liste oluşturmak için [] kullanılır. - Liste elemanlarına index numaralarıyla erişilir. - Elemanları sırayla eklemek için .append() metodu kullanılır. - Listeyi istediğimiz şekilde sıralayabiliriz.  Örnek:  ```python liste = [] liste.append("elma") liste.append("armut") liste.append("portakal") print(liste) ```  (Cay: osmanli-padisahlari.md) (Kaynak: oguz-boylari-ve-turk-boy-yapisi.md)

## Tüm sonuçlar

| id | Kategori | Sıra | En iyi skor | Eşikte red | Red | Anahtar | Kaynak | Süre | Sonuç |
|---|---|---|---|---|---|---|---|---|---|
| canakkale-1 | normal | 1 | 0.707 |  |  | tam | doğru | 2.1 | OK |
| canakkale-2 | normal | 1 | 0.561 |  |  | tam | doğru | 2.4 | OK |
| canakkale-3 | normal | 1 | 0.572 |  |  | tam | doğru | 2.3 | OK |
| canakkale-4 | normal | 1 | 0.474 |  |  | tam | doğru | 2.0 | OK |
| canakkale-5 | normal | 2 | 0.492 |  |  | tam | doğru | 2.1 | OK |
| ilkturk-1 | normal | 3 | 0.714 |  |  | tam | doğru | 2.2 | OK |
| ilkturk-2 | normal | 1 | 0.619 |  |  | tam | doğru | 2.3 | OK |
| ilkturk-3 | normal | 1 | 0.758 |  |  | tam | doğru | 2.0 | OK |
| ilkturk-4 | normal | 1 | 0.756 |  |  | tam | doğru | 1.7 | OK |
| ilkturk-5 | normal | 1 | 0.66 |  |  | tam | doğru | 1.8 | OK |
| ataturk-1 | normal | 1 | 0.673 |  |  | tam | doğru | 1.8 | OK |
| ataturk-2 | normal | 1 | 0.693 |  |  | tam | doğru | 1.9 | OK |
| ataturk-3 | normal | 1 | 0.479 |  |  | tam | doğru | 2.6 | OK |
| ataturk-4 | normal | 4 | 0.401 |  |  | tam | doğru | 2.1 | OK |
| ataturk-5 | normal | 1 | 0.745 |  |  | tam | doğru | 2.0 | OK |
| osmanli-1 | normal | 1 | 0.663 |  |  | tam | doğru | 3.1 | OK |
| osmanli-2 | ozel_ad | 1 | 0.566 |  |  | tam | doğru | 3.2 | OK |
| osmanli-3 | ozel_ad | 1 | 0.676 |  |  | tam | doğru | 2.3 | OK |
| osmanli-4 | ozel_ad | 1 | 0.574 |  |  | tam | doğru | 2.4 | OK |
| osmanli-5 | normal | 1 | 0.678 |  |  | tam | doğru | 2.1 | OK |
| osmanli-6 | normal | 1 | 0.705 |  |  | tam | doğru | 2.2 | OK |
| selcuklu-1 | normal | 1 | 0.748 |  |  | tam | doğru | 2.3 | OK |
| selcuklu-2 | normal | 1 | 0.663 |  |  | tam | doğru | 2.1 | OK |
| selcuklu-3 | normal | 1 | 0.756 |  |  | tam | doğru | 2.9 | OK |
| selcuklu-4 | normal | 1 | 0.779 |  |  | tam | doğru | 2.3 | OK |
| selcuklu-5 | normal | 1 | 0.484 |  |  | tam | doğru | 2.4 | OK |
| destan-1 | normal | 1 | 0.748 |  |  | tam | doğru | 1.6 | OK |
| destan-2 | normal | 1 | 0.776 |  |  | tam | doğru | 1.8 | OK |
| destan-3 | normal | 1 | 0.838 |  |  | tam | doğru | 2.2 | OK |
| destan-4 | normal | 1 | 0.628 |  |  | tam | doğru | 2.2 | OK |
| destan-5 | normal | 1 | 0.706 |  |  | tam | doğru | 1.8 | OK |
| gelenek-1 | ozel_ad | 1 | 0.559 |  |  | tam | doğru | 2.5 | OK |
| gelenek-2 | ozel_ad | 1 | 0.642 |  |  | tam | doğru | 2.7 | OK |
| gelenek-3 | normal | 1 | 0.663 |  |  | tam | doğru | 1.8 | OK |
| gelenek-4 | normal | 1 | 0.455 |  |  | tam | doğru | 3.2 | OK |
| gelenek-5 | ozel_ad | 1 | 0.555 |  |  | tam | doğru | 2.5 | OK |
| at-1 | normal | 1 | 0.656 |  |  | tam | doğru | 3.4 | OK |
| at-2 | ozel_ad | 1 | 0.475 |  |  | tam | doğru | 2.6 | OK |
| at-3 | normal | 1 | 0.74 |  |  | tam | doğru | 2.9 | OK |
| at-4 | normal | 1 | 0.582 |  |  | tam | doğru | 2.0 | OK |
| kurt-1 | normal | 1 | 0.725 |  |  | tam | doğru | 2.7 | OK |
| kurt-2 | ozel_ad | 1 | 0.563 |  |  | tam | doğru | 3.7 | OK |
| kurt-3 | ozel_ad | 1 | 0.52 |  |  | tam | doğru | 2.4 | OK |
| kurt-4 | normal | 1 | 0.83 |  |  | tam | doğru | 2.2 | OK |
| kurt-5 | normal | 2 | 0.71 |  |  | tam | doğru | 1.8 | OK |
| kurt-6 | normal | 3 | 0.684 |  |  | tam | doğru | 2.2 | OK |
| dogus-1 | normal | 1 | 0.687 |  |  | tam | doğru | 1.8 | OK |
| dogus-2 | normal | 7 | 0.649 |  |  | tam | doğru | 2.1 | OK |
| dogus-3 | normal | 1 | 0.773 |  |  | tam | doğru | 1.8 | OK |
| dogus-4 | normal | 1 | 0.75 |  |  | tam | doğru | 1.9 | OK |
| alfabe-1 | normal | 1 | 0.736 |  |  | tam | doğru | 2.0 | OK |
| alfabe-2 | normal | 1 | 0.712 |  |  | tam | doğru | 2.1 | OK |
| alfabe-3 | normal | 2 | 0.76 |  |  | tam | doğru | 2.4 | OK |
| alfabe-4 | normal | 1 | 0.816 |  |  | tam | doğru | 2.0 | OK |
| alfabe-5 | normal | 1 | 0.788 |  |  | tam | doğru | 2.4 | OK |
| islam-1 | normal | 1 | 0.763 |  |  | tam | doğru | 1.6 | OK |
| islam-2 | normal | 1 | 0.782 |  |  | tam | doğru | 1.8 | OK |
| islam-3 | normal | 1 | 0.783 |  |  | tam | doğru | 2.3 | OK |
| islam-4 | ozel_ad | 1 | 0.571 |  |  | tam | doğru | 2.2 | OK |
| islam-5 | normal | 1 | 0.728 |  |  | tam | doğru | 2.6 | OK |
| eser-1 | normal | 1 | 0.756 |  |  | tam | doğru | 1.6 | OK |
| eser-2 | normal | 1 | 0.697 |  |  | tam | doğru | 2.2 | OK |
| eser-3 | normal | 1 | 0.827 |  |  | tam | doğru | 2.5 | OK |
| eser-4 | ozel_ad | 1 | 0.815 |  |  | tam | doğru | 2.0 | OK |
| eser-5 | normal | 1 | 0.69 |  |  | tam | doğru | 2.9 | OK |
| teskilat-1 | normal | 1 | 0.715 |  |  | tam | doğru | 3.0 | OK |
| teskilat-2 | normal | 1 | 0.474 |  |  | tam | doğru | 2.1 | OK |
| teskilat-3 | ozel_ad | 1 | 0.69 |  |  | tam | doğru | 2.1 | OK |
| teskilat-4 | normal | 1 | 0.593 |  |  | tam | doğru | 2.1 | OK |
| teskilat-5 | normal | 1 | 0.634 |  |  | tam | doğru | 3.2 | OK |
| islahat-1 | normal | 1 | 0.595 |  |  | tam | doğru | 2.3 | OK |
| islahat-2 | normal | 6 | 0.672 |  |  | tam | doğru | 2.1 | OK |
| islahat-3 | ozel_ad | 1 | 0.674 |  |  | tam | doğru | 2.2 | OK |
| islahat-4 | normal | 1 | 0.663 |  |  | tam | doğru | 2.2 | OK |
| islahat-5 | normal | 2 | 0.688 |  |  | tam | doğru | 2.3 | OK |
| inkilap-1 | normal | 1 | 0.6 |  |  | tam | doğru | 1.5 | OK |
| inkilap-2 | normal | 1 | 0.565 |  |  | tam | doğru | 2.8 | OK |
| inkilap-3 | normal | 1 | 0.633 |  |  | tam | doğru | 2.2 | OK |
| inkilap-4 | normal | 1 | 0.645 |  |  | tam | doğru | 2.6 | OK |
| inkilap-5 | normal | 2 | 0.554 |  |  | tam | doğru | 2.2 | OK |
| beylik-1 | normal | 1 | 0.69 |  |  | tam | doğru | 3.2 | OK |
| beylik-2 | normal | 1 | 0.692 |  |  | tam | doğru | 2.6 | OK |
| beylik-3 | normal | 1 | 0.603 |  |  | tam | doğru | 2.5 | OK |
| beylik-4 | normal | 1 | 0.614 |  |  | tam | doğru | 2.3 | OK |
| beylik-5 | ozel_ad | 1 | 0.701 |  |  | tam | doğru | 3.1 | OK |
| mit-1 | ozel_ad | 1 | 0.702 |  |  | tam | doğru | 2.9 | OK |
| mit-2 | normal | 1 | 0.545 |  |  | tam | doğru | 1.6 | OK |
| mit-3 | ozel_ad | 1 | 0.701 |  |  | tam | doğru | 3.3 | OK |
| mit-4 | ozel_ad | 1 | 0.523 |  |  | tam | doğru | 2.0 | OK |
| mit-5 | normal | 1 | 0.603 |  |  | tam | doğru | 2.3 | OK |
| boy-1 | normal | 1 | 0.664 |  |  | tam | doğru | 2.0 | OK |
| boy-2 | normal | 1 | 0.729 |  |  | tam | doğru | 2.6 | OK |
| boy-3 | normal | 1 | 0.72 |  |  | tam | doğru | 2.0 | OK |
| boy-4 | normal | 3 | 0.63 |  |  | tam | doğru | 1.9 | OK |
| boy-5 | ozel_ad | 1 | 0.59 |  |  | tam | doğru | 2.6 | OK |
| bozkir-1 | ozel_ad | 2 | 0.677 |  |  | tam | doğru | 1.9 | OK |
| bozkir-2 | normal | 1 | 0.726 |  |  | tam | doğru | 2.4 | OK |
| bozkir-3 | ozel_ad | 2 | 0.499 |  |  | tam | doğru | 1.9 | OK |
| bozkir-4 | normal | 1 | 0.696 |  |  | tam | doğru | 2.1 | OK |
| bozkir-5 | normal | 1 | 0.691 |  |  | tam | doğru | 2.4 | OK |
| nevruz-1 | normal | 1 | 0.762 |  |  | tam | doğru | 2.3 | OK |
| nevruz-2 | ozel_ad | 1 | 0.657 |  |  | tam | doğru | 2.0 | OK |
| nevruz-3 | ozel_ad | 1 | 0.65 |  |  | tam | doğru | 2.4 | OK |
| nevruz-4 | normal | 1 | 0.637 |  |  | tam | doğru | 1.6 | OK |
| nevruz-5 | normal | 1 | 0.529 |  |  | tam | doğru | 2.4 | OK |
| ozan-1 | ozel_ad | 3 | 0.627 |  |  | tam | doğru | 2.1 | OK |
| ozan-2 | ozel_ad | 1 | 0.677 |  |  | tam | doğru | 2.0 | OK |
| ozan-3 | ozel_ad | 1 | 0.577 |  |  | tam | doğru | 2.3 | OK |
| ozan-4 | normal | 1 | 0.637 |  |  | tam | doğru | 1.6 | OK |
| ozan-5 | normal | 1 | 0.551 |  |  | tam | doğru | 1.5 | OK |
| bilim-1 | normal | 1 | 0.574 |  |  | tam | doğru | 2.6 | OK |
| bilim-2 | ozel_ad | 1 | 0.757 |  |  | tam | doğru | 1.9 | OK |
| bilim-3 | normal | 1 | 0.813 |  |  | tam | doğru | 2.1 | OK |
| bilim-4 | normal | 1 | 0.775 |  |  | tam | doğru | 1.5 | OK |
| bilim-5 | normal | 1 | 0.759 |  |  | tam | doğru | 1.7 | OK |
| mimari-1 | ozel_ad | 1 | 0.719 |  |  | tam | doğru | 2.2 | OK |
| mimari-2 | ozel_ad | 2 | 0.518 |  |  | tam | doğru | 2.3 | OK |
| mimari-3 | normal | 1 | 0.773 |  |  | tam | doğru | 1.9 | OK |
| mimari-4 | normal | 2 | 0.718 |  |  | tam | doğru | 2.2 | OK |
| mimari-5 | normal | 1 | 0.765 |  |  | tam | doğru | 1.9 | OK |
| deniz-1 | normal | 1 | 0.774 |  |  | tam | doğru | 2.9 | OK |
| deniz-2 | normal | 1 | 0.838 |  |  | tam | doğru | 1.8 | OK |
| deniz-3 | normal | 1 | 0.67 |  |  | tam | doğru | 2.2 | OK |
| deniz-4 | normal | 1 | 0.837 |  |  | tam | doğru | 2.7 | OK |
| deniz-5 | normal | 1 | 0.663 |  |  | tam | doğru | 1.8 | OK |
| sembol-1 | normal | 1 | 0.686 |  |  | tam | doğru | 2.3 | OK |
| sembol-2 | normal | 1 | 0.746 |  |  | tam | doğru | 2.0 | OK |
| sembol-3 | normal | 2 | 0.732 |  |  | tam | doğru | 1.8 | OK |
| sembol-4 | normal | 1 | 0.656 |  |  | tam | doğru | 1.7 | OK |
| sembol-5 | normal | 1 | 0.683 |  |  | tam | doğru | 1.7 | OK |
| dunya-1 | normal | 1 | 0.894 |  |  | tam | doğru | 1.9 | OK |
| dunya-2 | normal | 1 | 0.697 |  |  | tam | doğru | 2.4 | OK |
| dunya-3 | normal | 1 | 0.717 |  |  | tam | doğru | 2.8 | OK |
| dunya-4 | normal | 1 | 0.719 |  |  | tam | doğru | 1.9 | OK |
| dunya-5 | ozel_ad | 1 | 0.654 |  |  | tam | doğru | 2.2 | OK |
| cevapsiz-1 | yakin |  | 0.652 |  | evet |  |  | 1.6 | OK |
| cevapsiz-2 | yakin |  | 0.691 |  | evet |  |  | 1.8 | OK |
| cevapsiz-3 | yakin |  | 0.575 |  | evet |  |  | 1.7 | OK |
| cevapsiz-4 | yakin |  | 0.533 |  |  |  | var | 2.3 | HATA |
| cevapsiz-5 | yakin |  | 0.659 |  | evet |  |  | 1.6 | OK |
| cevapsiz-6 | yakin |  | 0.516 |  | evet |  |  | 1.6 | OK |
| cevapsiz-7 | konu_disi |  | 0.381 |  | evet |  |  | 1.6 | OK |
| cevapsiz-8 | konu_disi |  | 0.369 |  | evet |  |  | 1.8 | OK |
| cevapsiz-9 | konu_disi |  | 0.368 |  | evet |  |  | 1.6 | OK |
| cevapsiz-10 | anlamsiz |  | 0.374 |  | evet |  |  | 1.6 | OK |
| takip-1#1 | hazirlik |  | 0.663 |  |  |  | var | 2.1 | - |
| takip-1#2 | takip | 1 | 0.681 |  |  | tam | doğru | 4.7 | OK |
| takip-2#1 | hazirlik |  | 0.741 |  |  |  | var | 2.5 | - |
| takip-2#2 | takip | 5 | 0.735 |  |  | eksik | yanlış | 2.7 | HATA |
| takip-3#1 | hazirlik |  | 0.748 |  |  |  | var | 1.6 | - |
| takip-3#2 | takip | 1 | 0.79 |  |  | tam | doğru | 2.5 | OK |
| takip-4#1 | hazirlik |  | 0.705 |  |  |  | var | 2.2 | - |
| takip-4#2 | takip | 1 | 0.699 |  |  | tam | doğru | 2.4 | OK |
| takip-5#1 | hazirlik |  | 0.753 |  |  |  | var | 1.9 | - |
| takip-5#2 | takip | 1 | 0.726 |  |  | tam | doğru | 2.0 | OK |
| takip-cevapsiz-1#1 | hazirlik |  | 0.572 |  |  |  | var | 2.3 | - |
| takip-cevapsiz-1#2 | takip_cevapsiz |  | 0.579 |  |  |  | var | 3.7 | HATA |
| takip-cevapsiz-2#1 | hazirlik |  | 0.75 |  |  |  | var | 2.0 | - |
| takip-cevapsiz-2#2 | takip_cevapsiz |  | 0.511 |  |  |  | var | 2.8 | HATA |
| degisim-1#1 | hazirlik |  | 0.563 |  |  |  | var | 3.7 | - |
| degisim-1#2 | konu_degisimi | 1 | 0.566 |  |  | tam | doğru | 3.5 | OK |
| degisim-2#1 | hazirlik |  | 0.574 |  |  |  | var | 2.4 | - |
| degisim-2#2 | konu_degisimi | 1 | 0.563 |  |  | tam | doğru | 3.9 | OK |
| degisim-3#1 | hazirlik |  | 0.656 |  |  |  | var | 3.4 | - |
| degisim-3#2 | konu_degisimi | 1 | 0.475 |  |  | tam | doğru | 3.0 | OK |
| degisim-4#1 | hazirlik |  | 0.712 |  |  |  | var | 2.1 | - |
| degisim-4#2 | konu_degisimi | 1 | 0.555 |  |  | tam | doğru | 3.0 | OK |
| disi-1#1 | hazirlik |  | 0.676 |  |  |  | var | 2.3 | - |
| disi-1#2 | konu_disi_sonra |  | 0.381 |  | evet |  |  | 1.9 | OK |
| disi-2#1 | hazirlik |  | 0.725 |  |  |  | var | 2.7 | - |
| disi-2#2 | konu_disi_sonra |  | 0.719 |  | evet |  |  | 2.1 | OK |
| disi-3#1 | hazirlik |  | 0.676 |  |  |  | var | 2.3 | - |
| disi-3#2 | konu_disi_sonra |  | 0.599 |  |  |  | var | 3.7 | HATA |
| disi-4#1 | hazirlik |  | 0.663 |  |  |  | var | 2.1 | - |
| disi-4#2 | konu_disi_sonra |  | 0.368 |  | evet |  |  | 2.1 | OK |

## Cevaplar (gözle kontrol için)

**canakkale-1** — Çanakkale Deniz Zaferi hangi tarihte kazanılmıştır?
> Çanakkale Deniz Zaferi, 18 Mart 1915'te kazanılmıştır. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#0 0.707 | canakkale-ve-kurtulus-savasi.md#3 0.658 | turk-denizciligi.md#3 0.578 | turk-denizciligi.md#0 0.567`

**canakkale-2** — Gelibolu Yarımadası'na kara çıkarmaları ne zaman yapılmıştır?
> Gelibolu Yarımadası'na kara çıkarmaları 25 Nisan 1915'te yapılmıştır. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#1 0.561 | bozkir-gocebe-yasami.md#1 0.457 | milli-semboller.md#7 0.439 | turk-denizciligi.md#9 0.436 | turk-denizciligi.md#8 0.432`

**canakkale-3** — Sakarya Meydan Muharebesi kaç gün sürmüştür?
> Sakarya Meydan Muharebesi 23 Ağustos - 13 Eylül 1921 tarihleri arasında yirmi iki gün süren bir muharebe olmuştur. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#3 0.572 | selcuklu-ve-osmanli-mimarisi.md#3 0.496 | mustafa-kemal-ataturk.md#4 0.461 | milli-semboller.md#7 0.439 | osmanli-islahat-ve-mesrutiyet.md#0 0.437`

**canakkale-4** — Büyük Taarruz'da kesin sonuç nerede alınmıştır?
> Büyük Taarruz'da kesin sonuç Dumlupınar'da alınmıştır. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#4 0.474 | turk-devlet-gelenegi.md#2 0.453 | turk-islam-dunyasinda-bilim.md#0 0.428 | turklerin-islamiyeti-kabulu.md#1 0.424 | osmanli-islahat-ve-mesrutiyet.md#7 0.423`

**canakkale-5** — Lozan Antlaşması ne zaman imzalanmıştır?
> Lozan Antlaşması 24 Temmuz 1923'te imzalanmıştır. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#3 0.492 | canakkale-ve-kurtulus-savasi.md#4 0.485 | osmanli-islahat-ve-mesrutiyet.md#0 0.466 | cumhuriyet-inkilaplari.md#2 0.408 | bugunku-turk-dunyasi.md#4 0.400`

**ilkturk-1** — Orhun Yazıtları'nın alfabesini kim ve hangi yılda çözmüştür?
> Vilhelm Thomsen, Orhun Yazıtları'nın alfabesini 1893 yılında çözmüştür. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.714 | ilk-turk-devletleri.md#2 0.660 | ilk-turk-devletleri.md#3 0.569 | turkcenin-tarihi-ve-alfabeleri.md#3 0.562 | bugunku-turk-dunyasi.md#6 0.529`

**ilkturk-2** — Mete Han orduyu hangi sisteme göre düzenlemiştir?
> Mete Han orduyu onluk sisteme göre düzenlemiştir. Bu düzen, sonraki Türk devletlerinde ve başka ordularda da örnek alınmıştır. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#0 0.619 | ozan-asik-gelenegi.md#8 0.524 | osmanli-devlet-teskilati.md#8 0.477 | osmanli-devlet-teskilati.md#4 0.468 | osmanli-islahat-ve-mesrutiyet.md#9 0.450`

**ilkturk-3** — Göktürk Devleti ne zaman ve kimin önderliğinde kurulmuştur?
> Göktürk Devleti 552 yılında Bumin Kağan önderliğinde kurulmuştur. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#1 0.758 | ilk-turk-devletleri.md#4 0.659 | turk-milliyetciliginin-dogusu.md#4 0.585 | turk-devlet-gelenegi.md#0 0.580 | turklerin-islamiyeti-kabulu.md#3 0.576`

**ilkturk-4** — Orhun Yazıtları kimler adına dikilmiştir?
> Orhun Yazıtları, vezir Tonyukuk, Kül Tigin ve Bilge Kağan adına dikilmiştir. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#2 0.756 | turkcenin-tarihi-ve-alfabeleri.md#0 0.619`

**ilkturk-5** — Uygur Kağanlığı hangi yıl kurulmuştur?
> Uygur Kağanlığı 744'te kurulmuştur. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#4 0.660 | turklerin-islamiyeti-kabulu.md#3 0.576 | turk-islam-dunyasinda-bilim.md#5 0.567 | turkcenin-tarihi-ve-alfabeleri.md#1 0.558 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.541`

**ataturk-1** — Mustafa Kemal'in annesinin adı nedir?
> Mustafa Kemal Atatürk'nün annesinin adı Zübeyde Hanım'dır. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#0 0.673 | mustafa-kemal-ataturk.md#6 0.580 | mustafa-kemal-ataturk.md#1 0.551 | mustafa-kemal-ataturk.md#3 0.505 | mustafa-kemal-ataturk.md#4 0.502`

**ataturk-2** — Mustafa Kemal'e Kemal adını kim vermiştir?
> Mustafa Kemal'e Kemal adını matematik öğretmeni Mustafa Efendi vermiştir. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#1 0.693 | mustafa-kemal-ataturk.md#0 0.688 | mustafa-kemal-ataturk.md#3 0.601 | mustafa-kemal-ataturk.md#6 0.601 | mustafa-kemal-ataturk.md#4 0.596`

**ataturk-3** — Nutuk ne zaman okunmuş ve yaklaşık kaç saat sürmüştür?
> Mustafa Kemal Atatürk'ün Nutuk konuşmasını 15-20 Ekim 1927 tarihleri arasında okumuştur; bu konuşma yaklaşık otuz altı saat süren, Cumhuriyet'in temel kaynağı olan temel bir kaynaktır. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#5 0.479 | ilk-turk-islam-eserleri.md#1 0.437 | ilk-turk-islam-eserleri.md#2 0.415 | milli-semboller.md#10 0.412 | nevruz-ve-turk-bayramlari.md#8 0.400`

**ataturk-4** — "Yurtta sulh, cihanda sulh" sözü hangi yıl söylenmiştir?
> "Yurtta sulh, cihanda sulh" sözü 1931'de söylenmiştir. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#7 0.401 | milli-semboller.md#10 0.399 | turklerin-islamiyeti-kabulu.md#1 0.398 | mustafa-kemal-ataturk.md#5 0.398 | nevruz-ve-turk-bayramlari.md#6 0.398`

**ataturk-5** — Atatürk'ün naaşı Anıtkabir'e ne zaman nakledilmiştir?
> Atatürk'ün naaşı Anıtkabir'e 10 Kasım 1953'te nakledilmiştir. (Kaynak: milli-semboller.md)

Getirilen: `milli-semboller.md#7 0.745 | mustafa-kemal-ataturk.md#6 0.590 | milli-semboller.md#8 0.563 | mustafa-kemal-ataturk.md#4 0.529`

**osmanli-1** — Yavuz Sultan Selim hangi savaşlarla Mısır'ı Osmanlı topraklarına katmıştır?
> Yavuz Sultan Selim, Mısır'ı Osmanlı topraklarına katmak için Çaldıran Savaşı'nda Safevîler'e, Mercidabık Savaşı'nda ve Ridaniye Savaşı'nda Memlükler'e yenilgiye uğrattıktan sonra Mısır'ı Osmanlı topraklarına katmıştır. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#3 0.663 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#8 0.563 | osmanli-islahat-ve-mesrutiyet.md#0 0.562 | osmanli-islahat-ve-mesrutiyet.md#5 0.545 | selcuklu-ve-osmanli-mimarisi.md#5 0.543`

**osmanli-2** — fatih kimdir
> Fatih Sultan Mehmed, 29 Mayıs 1453'te İstanbul'u fethettiğinde yirmi bir yaşındaydı. Fetihle birlikte Doğu Roma İmparatorluğu sona ermiş, Osmanlı Devleti imparatorluğa dönüşmüştür. Ayrıca, Fatih Sultan Mehmed'in hazırlattığı kanunname, devlet teşkilatını ve protokolü yazılı hâle getiren ilk kapsamlı düzenleme sayılır. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#2 0.566 | milli-semboller.md#3 0.434 | osmanli-devlet-teskilati.md#9 0.410 | turk-islam-dunyasinda-bilim.md#6 0.405 | turk-islam-dunyasinda-bilim.md#2 0.474`

**osmanli-3** — Osman Gazi kimdir
> Osman Gazi, Osmanlı Devleti'nin kurucusudur. Devlet altı yüz yıldan uzun süre varlığını sürdürmüş ve toplam otuz altı padişah tarafından yönetilmiştir. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#0 0.676 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.586 | osmanli-padisahlari.md#1 0.659 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#3 0.518 | osmanli-islahat-ve-mesrutiyet.md#1 0.508`

**osmanli-4** — Orhan Gazi kimdir
> Orhan Gazi, Osmanlı Padişahlarının kurucusu Osman Gazi'nin oğludur ve Osmanlı Devleti'nin kurulmasında önemli rol oynamıştır. Onun döneminde Bursa şehrinin alınması ve Rumeli'ye geçiş yapılmıştır. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#1 0.574 | osmanli-padisahlari.md#0 0.465 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.416`

**osmanli-5** — Yıldırım Bayezid Ankara Savaşı'nda kime yenilmiştir?
> Yıldırım Bayezid Ankara Savaşı'nda Timur'a yenilmiştir. (Kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md)

Getirilen: `anadolu-beylikleri-ve-osmanlinin-kurulusu.md#9 0.678 | osmanli-padisahlari.md#1 0.640 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#1 0.605 | turk-denizciligi.md#0 0.544`

**osmanli-6** — Kanuni Sultan Süleyman kaç yıl hüküm sürmüştür?
> Kanuni Sultan Süleyman 1520-1566 yılları arasında kırk altı yıl hüküm sürmüştür. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#4 0.705 | osmanli-islahat-ve-mesrutiyet.md#0 0.593 | osmanli-padisahlari.md#0 0.570 | selcuklu-ve-osmanli-mimarisi.md#5 0.519 | selcuklular-ve-malazgirt.md#3 0.513`

**selcuklu-1** — Anadolu Selçuklu Devleti hangi savaşta Moğollara yenilmiştir?
> Anadolu Selçuklu Devleti 1243'teki Kösedağ Savaşı'nda Moğollara yenilmiştir. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#4 0.748 | selcuklular-ve-malazgirt.md#3 0.675 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#0 0.660 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#1 0.597`

**selcuklu-2** — Malazgirt Savaşı ne zaman yapılmıştır?
> Malazgirt Savaşı 26 Ağustos 1071'de yapılmıştır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.663 | selcuklular-ve-malazgirt.md#2 0.660 | selcuklular-ve-malazgirt.md#0 0.634 | selcuklular-ve-malazgirt.md#4 0.572 | turklerin-islamiyeti-kabulu.md#1 0.486`

**selcuklu-3** — Büyük Selçuklu Devleti'nin kuruluşunu kesinleştiren savaş hangisidir?
> Büyük Selçuklu Devleti'nin kuruluşunu kesinleştiren savaş Dandanakan Savaşı'dır. Bu savaşta Tuğrul Bey ve Çağrı beyler Gazneli ordusunu yenmiş ve Horasan bölgesi Selçukluların eline geçmiştir. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#0 0.756 | selcuklular-ve-malazgirt.md#3 0.647 | selcuklular-ve-malazgirt.md#2 0.606 | canakkale-ve-kurtulus-savasi.md#2 0.598 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#8 0.591`

**selcuklu-4** — Anadolu Selçuklu Devleti'ni kim kurmuştur?
> Selçuklular ve Malazgirt Savaşı bölümündeki metne göre, Anadolu Selçuklu Devleti'ni Süleyman Şah kurmuştur. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#3 0.779 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#0 0.755 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#1 0.725 | selcuklular-ve-malazgirt.md#0 0.691`

**selcuklu-5** — Miryokefalon Savaşı'nın sonucu ne olmuştur?
> Miryokefalon Savaşı'nda Bizans'ın Anadolu'yu geri alma girişimi başarısız olmuştur ve Anadolu'nun Türk yurdu olduğu kesinleşmiştir. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#3 0.484 | canakkale-ve-kurtulus-savasi.md#3 0.467 | selcuklular-ve-malazgirt.md#4 0.457 | osmanli-islahat-ve-mesrutiyet.md#3 0.443 | turklerin-islamiyeti-kabulu.md#6 0.436`

**destan-1** — Manas Destanı hangi topluma aittir?
> Manas Destanı Kırgızlara aittir. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#3 0.748 | ozan-asik-gelenegi.md#2 0.635 | turk-destanlari.md#1 0.527`

**destan-2** — Dede Korkut Kitabı kaç hikâyeden oluşur?
> Dede Korkut Kitabı, Oğuzların İslam sonrası dönemine ait on iki hikâyeden oluşur. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.776 | turk-kulturunde-at.md#5 0.575`

**destan-3** — Oğuz Kağan Destanı'na göre Oğuz Kağan'ın kaç oğlu vardır?
> Oğuz Kağan Destanı'na göre Oğuz Kağan'ın altı oğlu vardır ve bu oğullardan yirmi dört Oğuz boyunun türediği anlatılır. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#1 0.838 | turk-destanlari.md#0 0.552`

**destan-4** — Ergenekon'dan çıkış günü nasıl kutlanmıştır?
> Ergenekon Destanı'nda çıkış günü, bazı Türk topluluklarında bahar bayramı olarak kutlanmıştır. Vadiden çıkış gününde demir bir dağı eriterek dışarı çıkan topluluk, bu gün için özel bir kutlama yapar. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#2 0.628 | turk-kulturunde-kurt.md#2 0.446 | nevruz-ve-turk-bayramlari.md#1 0.440`

**destan-5** — Dede Korkut kültürü UNESCO listesine hangi yıl alınmıştır?
> Dede Korkut kültürü 2018'de UNESCO İnsanlığın Somut Olmayan Kültürel Mirası listesine alınmıştır. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.706 | bugunku-turk-dunyasi.md#7 0.663`

**gelenek-1** — Kut nedir?
> Kut, Türk devletlerinde hüküm süren hükümdarın yönetme yetkisinin Tanrı tarafından verildiğine inanıldığını ifade eden terimdir. Bu inanç, devletin sürekliliğini sağlamakta ve aynı zamanda taht kavgalarına da yol açmaktadır. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#0 0.485 | ilk-turk-islam-eserleri.md#1 0.430 | turk-kulturunde-kurt.md#6 0.559 | turk-kulturunde-kurt.md#0 0.519`

**gelenek-2** — Töre nedir?
> Töre, yazılı olmayan hukuk düzenidir. Eski Türk devletlerinde, töre devletin ve törenin birlikte anılmasıyla ifade edilir ve hükümdar bile bununla uymak zorunda kalmaktadır. Töre, değiştirilmesi için kurultayın onayını gerektirir ancak değişmez bir kurallar bütünü değildir. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#1 0.642 | turk-devlet-gelenegi.md#0 0.412 | turk-devlet-gelenegi.md#5 0.486`

**gelenek-3** — Kurultayda hangi konular görüşülürdü?
> Kurultayda savaş, barış ve hükümdar seçimi gibi konular görüşülürdü. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#2 0.663 | turk-kulturunde-kurt.md#2 0.589 | turk-kulturunde-kurt.md#4 0.555`

**gelenek-4** — İkili teşkilat nedir?
> İkili teşkilat, ülkenin doğu ve batı olmak üzere iki idari kanada ayrılmasıdır. Doğu kanadı daha üstün sayılır ve büyük kağan orada bulunurdu; batı kanadını genellikle hanedandan bir başka üye yönetirdi. Bu düzen, geniş bozkır coğrafyasının tek merkezden yönetilmesinin zorluğuna verilmiş pratik bir cevaptır. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#3 0.455 | oguz-boylari-ve-turk-boy-yapisi.md#2 0.397 | bugunku-turk-dunyasi.md#4 0.393 | osmanli-devlet-teskilati.md#6 0.385 | osmanli-devlet-teskilati.md#9 0.343`

**gelenek-5** — Tuğ nedir?
> Tuğ, at kılından yapılan ve sırık üzerinde taşınan bayrak niteliğindeki bir semboldür. Hükümdarlık sembolleri arasında tuğ sayılır ve sayısı hükümdarın rütbesine göre değişebilir. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#4 0.555 | turk-mitolojisi-ve-gok-tanri.md#6 0.452 | oguz-boylari-ve-turk-boy-yapisi.md#0 0.491 | oguz-boylari-ve-turk-boy-yapisi.md#2 0.484 | turk-destanlari.md#1 0.477`

**at-1** — Turan taktiği nasıl uygulanır?
> Turan taktiği, merkez birlikler sahte bir geri çekilme yaparak uygulanır. Düşmanın takibe başladığında, kanatlar hilal biçiminde kapanarak düşmana kuşatma oluşturur. Bu yöntem, atlı okçuluk becerisi ve atlı savaş stratejisi ile birlikte, Türk ordularının ağır piyadeye karşı hareket üstünlüğünü sağlar. Malazgirt Savaşı'nda da bu taktik kullanılmıştır. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#1 0.656 | turk-devlet-gelenegi.md#1 0.501 | turk-devlet-gelenegi.md#5 0.498 | osmanli-devlet-teskilati.md#3 0.497 | osmanli-devlet-teskilati.md#4 0.496`

**at-2** — Kımız nedir?
> Kısrak sütünün mayalanmasıyla elde edilen kımız, sağılan süt deriden yapılmış tulumlara konup düzenli olarak çalkalanarak mayalandırılır; ortaya çıkan içecek hafif ekşi tatlı ve düşük alkollüdür. Kımız yaz aylarında hazırlanır, şölenlerde ve konuk ağırlamada ikram edilir. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#3 0.475 | turk-mitolojisi-ve-gok-tanri.md#5 0.351`

**at-3** — Üzengi atlı savaşa ne kazandırmıştır?
> Üzengi atlı savaşa şu avantajları kazandırmıştır:  - Binicinin at üstünde dengeli durabilmesi - İki elini birden kullanabilmesi - Mızrak darbesine vücut ağırlığını verebilmesi  Bu buluş, atlı savaşın daha etkili bir şekilde yürütülmesine olanak sağlaymıştır. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#2 0.740 | turk-kulturunde-at.md#1 0.629 | turklerin-islamiyeti-kabulu.md#1 0.524 | osmanli-islahat-ve-mesrutiyet.md#0 0.522`

**at-4** — Hangi at ırkları dayanıklılıklarıyla bilinir?
> Ahal Teke ve Türkmen atı dayanıklılıkları ve uzun mesafe performanslarıyla bilinir. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#5 0.582 | turk-kulturunde-at.md#0 0.531 | turk-kulturunde-at.md#1 0.519 | turk-kulturunde-at.md#2 0.463 | turk-kulturunde-at.md#4 0.457`

**kurt-1** — Eski Türkçede kurdun adı neydi?
> Eski Türkçede kurdun adı "böri" idi. Bu sözcük Orhun Yazıtları'nda ve on birinci yüzyılda Kaşgarlı Mahmud'un yazdığı Dîvânu Lugâti't-Türk'te geçer. Ayrıca, bugün birçok Türk lehçesinde bile böri biçimi kullanılmaktadır. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.725 | turk-kulturunde-kurt.md#6 0.612 | turk-kulturunde-kurt.md#4 0.591 | turk-kulturunde-kurt.md#0 0.510`

**kurt-2** — böri nedir
> Eski Türkçede kurdun adı "böri" idi. Bu sözcük Orhun Yazıtları'nda ve on birinci yüzyılda Kaşgarlı Mahmud'un yazdığı Dîvânu Lugâti't-Türk'te geçer. Bugün Kazakçada börı, Kırgızcada börü, Özbekçede bo'ri olarak kullanılmaktadır. Türkiye Türkçesinde ise sözcük yalnızca "bozkurt" ve destan kahramanı "Börteçine" gibi kalıplarda korunmuştur. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.563 | turk-kulturunde-kurt.md#6 0.456 | bozkir-gocebe-yasami.md#0 0.484 | bozkir-gocebe-yasami.md#2 0.467 | turk-kulturunde-at.md#0 0.442`

**kurt-3** — Aşina hanedanının soyu nereden gelir?
> Aşina hanedanının soyu bir dişi kurttan gelir. Göktürklerin türeyiş anlatısına göre, hanedanın adı Aşina'dır ve soyun dişi bir kurttan olduğu aktarılır. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#1 0.520 | oguz-boylari-ve-turk-boy-yapisi.md#4 0.433 | ozan-asik-gelenegi.md#3 0.371`

**kurt-4** — Eski Türkçede kurt kelimesinin anlamı neydi?
> Eski Türkçede kurt kelimesinin anlamı solucan, kurtçuk, böcek larvasıydı. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#6 0.830 | turk-kulturunde-kurt.md#5 0.724 | turk-kulturunde-kurt.md#3 0.688 | turk-kulturunde-kurt.md#0 0.685 | turk-kulturunde-kurt.md#4 0.663`

**kurt-5** — Azerbaycan Türkçesinde kurda ne denir?
> Azerbaycan Türkçesinde kurt için "canavar" sözcüğü kullanılmaktadır. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.710 | turk-kulturunde-kurt.md#6 0.705 | bozkir-gocebe-yasami.md#2 0.569`

**kurt-6** — Ergenekon'dan çıkan topluluğa yolu kim göstermiştir?
> Ergenekon Destanı'nda topluluğa yolu Börteçine adlı bozkurt göstermiştir. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-destanlari.md#2 0.684 | bozkir-gocebe-yasami.md#7 0.544 | turk-kulturunde-kurt.md#2 0.527 | bozkir-gocebe-yasami.md#6 0.496 | oguz-boylari-ve-turk-boy-yapisi.md#7 0.486`

**dogus-1** — Üç Tarz-ı Siyaset yazısı nerede ve hangi yıl yayımlanmıştır?
> Üç Tarz-ı Siyaset yazısı 1904'te Kahire'de yayımlanmıştır. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#1 0.687 | osmanli-islahat-ve-mesrutiyet.md#7 0.461`

**dogus-2** — Türkçülüğün Esasları kimin eseridir?
> Türkçülüğün Esasları eseri Ziya Gökalp tarafından yazılmıştır. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `ilk-turk-islam-eserleri.md#0 0.649 | ilk-turk-islam-eserleri.md#3 0.613 | turk-milliyetciliginin-dogusu.md#2 0.579 | turkcenin-tarihi-ve-alfabeleri.md#0 0.560`

**dogus-3** — İsmail Gaspıralı hangi ilkeyi savunmuştur?
> İsmail Gaspıralı, "Dilde, fikirde, işte birlik" ilkesini savunmuştur. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#3 0.773 | osmanli-islahat-ve-mesrutiyet.md#7 0.525`

**dogus-4** — Türk Ocağı ne zaman kurulmuştur?
> Türk Ocağı 25 Mart 1912'de kurulmuştur. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.750 | bugunku-turk-dunyasi.md#5 0.615 | ilk-turk-devletleri.md#1 0.603 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.592 | bugunku-turk-dunyasi.md#4 0.581`

**alfabe-1** — Göktürk alfabesi kaç işaretten oluşur?
> Göktürk alfabesi otuz sekiz işaretten oluşur. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.736 | turkcenin-tarihi-ve-alfabeleri.md#3 0.648 | bugunku-turk-dunyasi.md#6 0.617 | ilk-turk-devletleri.md#4 0.534 | turk-kulturunde-kurt.md#1 0.524`

**alfabe-2** — Harf Devrimi hangi tarihte kabul edilmiştir?
> Harf Devrimi 1 Kasım 1928'de kabul edilmiştir. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#3 0.712 | turkcenin-tarihi-ve-alfabeleri.md#4 0.555 | bugunku-turk-dunyasi.md#6 0.550 | cumhuriyet-inkilaplari.md#5 0.550 | ilk-turk-devletleri.md#3 0.530`

**alfabe-3** — Türk Dil Kurumu ne zaman kurulmuştur?
> Türk Dil Kurumu, 12 Temmuz 1932'de kurulan Türk Dili Tetkik Cemiyeti olarak başlamış ve bugüne kadar faaliyet göstermektedir. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.760 | turkcenin-tarihi-ve-alfabeleri.md#4 0.760 | bugunku-turk-dunyasi.md#4 0.671 | bugunku-turk-dunyasi.md#5 0.645 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#4 0.637`

**alfabe-4** — Uygur alfabesi hangi yazıdan uyarlanmıştır?
> Uygur alfabesi Soğd yazısından uyarlanmıştır. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#1 0.816 | turkcenin-tarihi-ve-alfabeleri.md#0 0.664 | turkcenin-tarihi-ve-alfabeleri.md#3 0.643 | turkcenin-tarihi-ve-alfabeleri.md#2 0.632 | bugunku-turk-dunyasi.md#6 0.627`

**alfabe-5** — Kutadgu Bilig hangi yüzyılda yazılmıştır?
> Kutadgu Bilig, 11. yüzyılda yazılmıştır. Yazarı Yusuf Has Hâcib tarafından 1069-1070 yıllarında tamamlanmış ve Karahanlı hükümdarı Tabgaç Buğra Han'a sunulmuştur. (Kaynak: ilk-turk-islam-eserleri.md)

Getirilen: `ilk-turk-islam-eserleri.md#1 0.788 | ilk-turk-islam-eserleri.md#2 0.700`

**islam-1** — Talas Savaşı hangi yıl yapılmıştır?
> Talas Savaşı 751 yılında yapılmıştır. (Kaynak: turklerin-islamiyeti-kabulu.md)

Getirilen: `turklerin-islamiyeti-kabulu.md#1 0.763 | selcuklular-ve-malazgirt.md#2 0.516`

**islam-2** — Talas Savaşı'nda hangi Türk boyu Abbasîlerin yanında yer almıştır?
> Talas Savaşı'nda Karluk Türkleri Abbasîlerin yanında yer almıştır. (Kaynak: turklerin-islamiyeti-kabulu.md)

Getirilen: `turklerin-islamiyeti-kabulu.md#1 0.782 | oguz-boylari-ve-turk-boy-yapisi.md#6 0.542`

**islam-3** — İslamiyet'i resmî din olarak kabul eden ilk Türk devleti hangisidir?
> İslamiyet'i resmî din olarak kabul eden ilk Türk devleti İtil (Volga) Bulgarlarıdır. (Kaynak: turklerin-islamiyeti-kabulu.md)

Getirilen: `turklerin-islamiyeti-kabulu.md#2 0.783 | turklerin-islamiyeti-kabulu.md#3 0.738 | ilk-turk-devletleri.md#1 0.734 | ilk-turk-devletleri.md#0 0.716 | ilk-turk-islam-eserleri.md#0 0.685`

**islam-4** — Satuk Buğra Han Müslüman olduktan sonra hangi adı almıştır?
> Satuk Buğra Han Müslüman olduktan sonra Abdülkerim adını almıştır. (Kaynak: turklerin-islamiyeti-kabulu.md)

Getirilen: `turklerin-islamiyeti-kabulu.md#3 0.571 | turklerin-islamiyeti-kabulu.md#2 0.505 | turk-islam-dunyasinda-bilim.md#5 0.439 | turklerin-islamiyeti-kabulu.md#4 0.435 | ilk-turk-islam-eserleri.md#1 0.434`

**islam-5** — Gazneli Devleti'nin en parlak dönemi hangi hükümdarın zamanıdır?
> Gazneli Devleti'nin en parlak dönemi Gazneli Mahmud'un zamanıdır. Mahmud, Hindistan'a düzenlediği seferlerle tanınır ve Abbasî halifesi tarafından "sultan" unvanı verildiği bildirilir. (Kaynak: turklerin-islamiyeti-kabulu.md)

Getirilen: `turklerin-islamiyeti-kabulu.md#5 0.728 | osmanli-padisahlari.md#1 0.544 | osmanli-padisahlari.md#0 0.530`

**eser-1** — Kutadgu Bilig'i kim yazmıştır?
> Kutadgu Bilig, Yusuf Has Hâcib tarafından yazılmıştır. (Kaynak: ilk-turk-islam-eserleri.md)

Getirilen: `ilk-turk-islam-eserleri.md#1 0.756 | ilk-turk-islam-eserleri.md#2 0.706`

**eser-2** — Kutadgu Bilig'de hükümdar Küntoğdı neyi temsil eder?
> Kutadgu Bilig'de hükümdar Küntoğdı adaleti ve kanunu temsil eder. (Kaynak: ilk-turk-islam-eserleri.md)

Getirilen: `ilk-turk-islam-eserleri.md#2 0.697 | ilk-turk-islam-eserleri.md#1 0.661 | turk-devlet-gelenegi.md#0 0.528 | turk-kulturunde-kurt.md#3 0.506 | turk-kulturunde-kurt.md#2 0.503`

**eser-3** — Dîvânu Lugâti't-Türk hangi amaçla yazılmıştır?
> Dîvânu Lugâti't-Türk, Kaşgarlı Mahmud tarafından Araplara Türkçe öğretmek amacıyla 1072-1074 yılları arasında yazılmıştır. Eserin yazılış amacı Araplara Türkçe öğretmektir; bu nedenle açıklamalar Arapça yazılmışken, örnekler Türkçe verilmiştir. (Kaynak: ilk-turk-islam-eserleri.md)

Getirilen: `ilk-turk-islam-eserleri.md#3 0.827 | ilk-turk-islam-eserleri.md#4 0.764`

**eser-4** — Atabetü'l-Hakayık'ı kim yazmıştır?
> Atabetü'l-Hakayık'ı Edip Ahmed Yükneki tarafından on ikinci yüzyılda, Karahanlı döneminin sonlarında yazılmıştır. (Kaynak: ilk-turk-islam-eserleri.md)

Getirilen: `ilk-turk-islam-eserleri.md#5 0.815 | turk-kulturunde-at.md#5 0.519`

**eser-5** — Dîvân-ı Hikmet'te hangi ölçü kullanılmıştır?
> Dîvân-ı Hikmet'te şiirlerde aruz yerine hece ölçüsü ve dörtlük kullanılmıştır. Bu kullanım, eseri halk edebiyatı geleneğine yaklaştırarak Türkçe ve halkın anlayacağı bir dille tasavvuf konularını anlatmayı amaçlamıştır. (Kaynak: ilk-turk-islam-eserleri.md)

Getirilen: `ilk-turk-islam-eserleri.md#6 0.690 | osmanli-devlet-teskilati.md#1 0.541 | ilk-turk-islam-eserleri.md#7 0.540 | osmanli-devlet-teskilati.md#9 0.486 | ilk-turk-islam-eserleri.md#3 0.485`

**teskilat-1** — Divan-ı Hümayun'a Fatih Sultan Mehmed'den sonra kim başkanlık etmiştir?
> Fatih Sultan Mehmed döneminde padişahlar kendileri Divan-ı Hümayun başkanlık etmişlerdir. Fatih'ten sonra padişahların divan toplantılarını kafes arkasından izleyerek ve başkanlığın veziriazama bırakarak divanın işleyişine müdahale etmeye başlamışlardır. (Kaynak: osmanli-devlet-teskilati.md)

Getirilen: `osmanli-devlet-teskilati.md#1 0.715 | osmanli-padisahlari.md#2 0.665 | osmanli-devlet-teskilati.md#2 0.606 | osmanli-padisahlari.md#4 0.591 | ilk-turk-islam-eserleri.md#6 0.553`

**teskilat-2** — Nişancının görevi nedir?
> Nişancı, padişah fermanlarına tuğra çekmekten ve arazi kayıtlarından sorumludur. (Kaynak: osmanli-devlet-teskilati.md)

Getirilen: `osmanli-devlet-teskilati.md#2 0.474 | osmanli-devlet-teskilati.md#3 0.446 | selcuklu-ve-osmanli-mimarisi.md#5 0.377 | turk-denizciligi.md#1 0.376 | mustafa-kemal-ataturk.md#3 0.362`

**teskilat-3** — Tımar sisteminde sipahinin yetiştirdiği atlı askerlere ne ad verilir?
> Tımar sisteminde sipahinin yetiştirdiği atlı askerlere cebelü adı verilir. (Kaynak: osmanli-devlet-teskilati.md)

Getirilen: `osmanli-devlet-teskilati.md#4 0.690 | osmanli-devlet-teskilati.md#5 0.568 | turk-kulturunde-at.md#1 0.508`

**teskilat-4** — Yeniçeri Ocağı hangi olayla kaldırılmıştır?
> Yeniçeri Ocağı, Vaka-i Hayriye olayı ile kaldırılmıştır. (Kaynak: osmanli-islahat-ve-mesrutiyet.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#6 0.593 | osmanli-devlet-teskilati.md#7 0.573 | osmanli-islahat-ve-mesrutiyet.md#1 0.536 | cumhuriyet-inkilaplari.md#1 0.481 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#0 0.478`

**teskilat-5** — Millet sisteminde gayrimüslimler hangi esasa göre örgütlenmiştir?
> Millet sisteminde gayrimüslimler mezhep esasına göre örgütlenmiştir. Bu sistemde Rum Ortodoks, Ermeni ve Yahudi cemaatleri kendi dinî önderlerinin yönetiminde ve evlilik, miras ve cemaat içi anlaşmazlıklar gibi konularda kendi hukuklarını uygulardı. (Kaynak: osmanli-devlet-teskilati.md)

Getirilen: `osmanli-devlet-teskilati.md#8 0.634 | osmanli-devlet-teskilati.md#4 0.513 | turk-devlet-gelenegi.md#2 0.491 | osmanli-devlet-teskilati.md#6 0.491 | oguz-boylari-ve-turk-boy-yapisi.md#0 0.489`

**islahat-1** — Karlofça Antlaşması hangi yıl imzalanmıştır?
> Karlofça Antlaşması 1699'da imzalanmıştır. (Kaynak: osmanli-islahat-ve-mesrutiyet.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#3 0.595 | canakkale-ve-kurtulus-savasi.md#4 0.510 | canakkale-ve-kurtulus-savasi.md#1 0.496 | osmanli-islahat-ve-mesrutiyet.md#0 0.483 | turklerin-islamiyeti-kabulu.md#3 0.468`

**islahat-2** — İlk Türk matbaasını kimler kurmuştur?
> İlk Türk matbaasını kurmuş olanlar İbrahim Müteferrika ile Said Efendi'dir. (Kaynak: osmanli-islahat-ve-mesrutiyet.md)

Getirilen: `ilk-turk-islam-eserleri.md#0 0.672 | ilk-turk-islam-eserleri.md#4 0.658 | ilk-turk-devletleri.md#4 0.652 | ilk-turk-devletleri.md#1 0.648 | osmanli-islahat-ve-mesrutiyet.md#4 0.628`

**islahat-3** — III. Selim'in kurduğu yeni ordunun adı nedir?
> III. Selim'in kurduğu yeni ordunun adı Nizam-ı Cedid'dir. (Kaynak: osmanli-islahat-ve-mesrutiyet.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#5 0.674 | selcuklu-ve-osmanli-mimarisi.md#6 0.503 | osmanli-devlet-teskilati.md#7 0.502 | osmanli-padisahlari.md#3 0.500 | osmanli-islahat-ve-mesrutiyet.md#8 0.490`

**islahat-4** — Tanzimat Fermanı hangi tarihte okunmuştur?
> Tanzimat Fermanı 3 Kasım 1839'ta okunmuştur. (Kaynak: osmanli-islahat-ve-mesrutiyet.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#7 0.663 | osmanli-islahat-ve-mesrutiyet.md#8 0.543 | mustafa-kemal-ataturk.md#5 0.526 | mustafa-kemal-ataturk.md#4 0.510 | mustafa-kemal-ataturk.md#6 0.497`

**islahat-5** — I. Meşrutiyet hangi tarihte ilan edilmiştir?
> I. Meşrutiyet 23 Aralık 1876'da ilan edilmiştir. (Kaynak: osmanli-islahat-ve-mesrutiyet.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#9 0.688 | osmanli-islahat-ve-mesrutiyet.md#8 0.603 | osmanli-islahat-ve-mesrutiyet.md#7 0.553 | osmanli-devlet-teskilati.md#9 0.519 | ozan-asik-gelenegi.md#8 0.518`

**inkilap-1** — Saltanat hangi tarihte kaldırılmıştır?
> Saltanat 1 Kasım 1922'de kaldırılmıştır. (Kaynak: cumhuriyet-inkilaplari.md)

Getirilen: `cumhuriyet-inkilaplari.md#1 0.600 | osmanli-padisahlari.md#4 0.459`

**inkilap-2** — Halifelik hangi tarihte kaldırılmıştır?
> Halifelik 3 Mart 1924'te kaldırılmıştır. Bu tarihte çıkarılan üç kanunda halifelik kaldırılmış, Şer'iye ve Evkaf Vekâleti ile Erkân-ı Harbiye Vekâleti kapatılmış ve öğretim birliği sağlanmıştır. (Kaynak: cumhuriyet-inkilaplari.md)

Getirilen: `cumhuriyet-inkilaplari.md#1 0.529 | osmanli-padisahlari.md#3 0.475 | osmanli-islahat-ve-mesrutiyet.md#6 0.496 | osmanli-padisahlari.md#4 0.475 | turklerin-islamiyeti-kabulu.md#5 0.464`

**inkilap-3** — Türk Medeni Kanunu hangi ülkenin kanunu esas alınarak hazırlanmıştır?
> Türkiye'nin Medeni Kanunu, İsviçre Medeni Kanunu esas alınarak hazırlanmıştır. (Kaynak: cumhuriyet-inkilaplari.md)

Getirilen: `cumhuriyet-inkilaplari.md#4 0.633 | osmanli-devlet-teskilati.md#9 0.555 | turk-devlet-gelenegi.md#1 0.552 | turk-devlet-gelenegi.md#2 0.546 | bugunku-turk-dunyasi.md#4 0.533`

**inkilap-4** — Kadınlara milletvekili seçme ve seçilme hakkı ne zaman tanınmıştır?
> Kadınlara milletvekili seçme ve seçilme hakkı 5 Aralık 1934'te 5 Aralık 1934'te yapılan anayasa değişikliğiyle tanınmıştır. (Kaynak: cumhuriyet-inkilaplari.md)

Getirilen: `cumhuriyet-inkilaplari.md#7 0.645 | osmanli-islahat-ve-mesrutiyet.md#9 0.514 | turk-milliyetciliginin-dogusu.md#0 0.511 | osmanli-islahat-ve-mesrutiyet.md#8 0.507 | cumhuriyet-inkilaplari.md#6 0.505`

**inkilap-5** — Soyadı Kanunu hangi tarihte kabul edilmiştir?
> Soyadı Kanunu 21 Haziran 1934 tarihinde kabul edilmiştir. (Kaynak: cumhuriyet-inkilaplari.md)

Getirilen: `cumhuriyet-inkilaplari.md#4 0.554 | cumhuriyet-inkilaplari.md#6 0.551 | turk-denizciligi.md#9 0.510 | osmanli-devlet-teskilati.md#9 0.455 | milli-semboller.md#9 0.414`

**beylik-1** — Osmanlı Devleti'ne katılan ilk beylik hangisidir?
> Karesioğulları'nın beyliği, Osmanlı Devleti'ne katılan ilk beylicktir. Karesioğulları'nın donanması ve deneyimli komutanları, 1345'te Osmanlı'ya katılmasıyla Osmanlı hizmetine girerken, bu katılım Rumeli'ye geçiş yolunu açtığı için Osmanlı büyümesinin önemli dönüm noktasından sayılır. (Kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md)

Getirilen: `anadolu-beylikleri-ve-osmanlinin-kurulusu.md#3 0.690 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#8 0.658 | osmanli-devlet-teskilati.md#0 0.637 | osmanli-padisahlari.md#0 0.631`

**beylik-2** — Türkçenin resmî dil olarak kullanılmasına dair buyruğu kim vermiştir?
> Karamanoğlu Mehmed Bey'in 1277'de Türkçenin resmî dil olarak kullanılmasına dair verdiği buyruk bu tutumun en bilinen örneğidir. (Kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md)

Getirilen: `anadolu-beylikleri-ve-osmanlinin-kurulusu.md#4 0.692 | turkcenin-tarihi-ve-alfabeleri.md#4 0.664 | bugunku-turk-dunyasi.md#6 0.628 | turkcenin-tarihi-ve-alfabeleri.md#2 0.620 | bugunku-turk-dunyasi.md#4 0.608`

**beylik-3** — Malazgirt sonrası kurulan beyliklerden hangisi donanmasıyla tanınır?
> İzmir merkezli Çaka Beyliği donanması kurup denizde Bizans'a karşı mücadele etmesiyle tanınır. (Kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md)

Getirilen: `anadolu-beylikleri-ve-osmanlinin-kurulusu.md#1 0.603 | selcuklular-ve-malazgirt.md#2 0.596 | selcuklular-ve-malazgirt.md#0 0.595 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#2 0.560 | oguz-boylari-ve-turk-boy-yapisi.md#7 0.514`

**beylik-4** — Osmanlılar Rumeli'ye hangi kalenin alınmasıyla geçmiştir?
> Osmanlılar Çimpe Kalesi'nin alınmasıyla Rumeli'ye geçmiştir. (Kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md)

Getirilen: `anadolu-beylikleri-ve-osmanlinin-kurulusu.md#8 0.614 | osmanli-padisahlari.md#1 0.598 | osmanli-padisahlari.md#3 0.589 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#3 0.577 | osmanli-devlet-teskilati.md#8 0.576`

**beylik-5** — Osmanlı'nın fethettiği yerlerdeki halka uyguladığı politikanın adı nedir?
> Osmanlı'nın fethettiği yerlerdeki halka uyguladığı politikanın adı istimâlet politikasıdır. Bu politika, yerel halkın dinine, mülküne ve düzenine dokunmaması ve vergilerin daha hafif tutulması ile direnci azaltmıştır. (Kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md)

Getirilen: `anadolu-beylikleri-ve-osmanlinin-kurulusu.md#7 0.701 | osmanli-devlet-teskilati.md#0 0.663 | osmanli-devlet-teskilati.md#6 0.649 | osmanli-islahat-ve-mesrutiyet.md#10 0.623 | osmanli-islahat-ve-mesrutiyet.md#2 0.612`

**mit-1** — Eski Türk inancında tek yaratıcı güce ne ad verilir?
> Eski Türk inancında tek yaratıcı güce Tengri adı verilir. Bu varlık, her şeyi yaratan ve yöneten tek güç olarak kabul edilir ve gözle görülmez, herhangi bir biçime sokulmaz ve heykeli ya da putu yapılmaz. (Kaynak: turk-mitolojisi-ve-gok-tanri.md)

Getirilen: `turk-mitolojisi-ve-gok-tanri.md#0 0.702 | turk-devlet-gelenegi.md#0 0.587 | turk-mitolojisi-ve-gok-tanri.md#8 0.584 | ilk-turk-islam-eserleri.md#7 0.573`

**mit-2** — Umay neyi korur?
> Umay, Türk inanç dünyasında çocukları ve bereketi korur. (Kaynak: turk-mitolojisi-ve-gok-tanri.md)

Getirilen: `turk-mitolojisi-ve-gok-tanri.md#3 0.545 | nevruz-ve-turk-bayramlari.md#3 0.345`

**mit-3** — Türk inancında ruhlarla ilişki kurduğuna inanılan din adamına ne denir?
> Türk inancında ruhlarla ilişki kurduğuna inanılan din adamına kam denir. Kam, hastaları iyileştirmek, ölünün ruhunu uğurlamak ve gelecekten haber vermek gibi görevlerini yerine getirirken, törenlerde davul kullanarak ezgi ve dansla kendinden geçtiği bir duruma girerdi. (Kaynak: turk-mitolojisi-ve-gok-tanri.md)

Getirilen: `turk-mitolojisi-ve-gok-tanri.md#5 0.701 | turk-mitolojisi-ve-gok-tanri.md#2 0.647 | turk-mitolojisi-ve-gok-tanri.md#8 0.637 | turk-mitolojisi-ve-gok-tanri.md#9 0.625 | turk-mitolojisi-ve-gok-tanri.md#1 0.625`

**mit-4** — Ölünün ardından yapılan yas törenine ne ad verilir?
> Yas törenine yuğ adı verilir. (Kaynak: turk-mitolojisi-ve-gok-tanri.md)

Getirilen: `turk-mitolojisi-ve-gok-tanri.md#2 0.523 | nevruz-ve-turk-bayramlari.md#4 0.481 | turk-devlet-gelenegi.md#1 0.471 | oguz-boylari-ve-turk-boy-yapisi.md#1 0.455 | milli-semboller.md#5 0.438`

**mit-5** — Uygur Kağanlığı hangi dini resmî din olarak benimsemiştir?
> Uygur Kağanlığı 763'te Maniheizm'i resmî din olarak benimsemiştir. (Kaynak: turk-mitolojisi-ve-gok-tanri.md)

Getirilen: `turk-mitolojisi-ve-gok-tanri.md#8 0.603 | turk-destanlari.md#1 0.580 | oguz-boylari-ve-turk-boy-yapisi.md#8 0.572 | turklerin-islamiyeti-kabulu.md#3 0.550 | ilk-turk-devletleri.md#4 0.534`

**boy-1** — Eski Türk toplumunda en küçük birim nedir?
> Eski Türk toplumunda en küçük birim oğuz yani ailedir. (Kaynak: oguz-boylari-ve-turk-boy-yapisi.md)

Getirilen: `oguz-boylari-ve-turk-boy-yapisi.md#0 0.664 | turk-kulturunde-at.md#0 0.559 | turk-devlet-gelenegi.md#2 0.548 | oguz-boylari-ve-turk-boy-yapisi.md#8 0.520 | ilk-turk-devletleri.md#0 0.512`

**boy-2** — Oğuzlar kaç boya ayrılır?
> Oğuzlar, Türk boyları arasında tarihsel etkisi en geniş olan topluluktur ve yirmi dört boya ayrılır. Bu boylar Bozoklar ile Üçoklar olarak iki kola bölünür. (Kaynak: oguz-boylari-ve-turk-boy-yapisi.md)

Getirilen: `oguz-boylari-ve-turk-boy-yapisi.md#2 0.729 | oguz-boylari-ve-turk-boy-yapisi.md#3 0.609 | oguz-boylari-ve-turk-boy-yapisi.md#5 0.563 | turk-destanlari.md#1 0.556 | oguz-boylari-ve-turk-boy-yapisi.md#6 0.520`

**boy-3** — Oğuz boylarının iki kolunun adı nedir?
> Oğuz boylarının iki kolunun adları Bozoklar ve Üçoklardır. (Kaynak: oguz-boylari-ve-turk-boy-yapisi.md)

Getirilen: `oguz-boylari-ve-turk-boy-yapisi.md#2 0.720 | oguz-boylari-ve-turk-boy-yapisi.md#3 0.665 | turk-destanlari.md#1 0.597`

**boy-4** — Osmanlı hanedanı hangi boydan çıkmıştır?
> Osmanlı hanedanı Kayı boyundan çıkmıştır. (Kaynak: oguz-boylari-ve-turk-boy-yapisi.md)

Getirilen: `osmanli-padisahlari.md#0 0.630 | osmanli-devlet-teskilati.md#0 0.588 | oguz-boylari-ve-turk-boy-yapisi.md#4 0.587 | osmanli-padisahlari.md#1 0.579 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#0 0.556`

**boy-5** — Boyların kullandığı işarete ne ad verilir?
> Boyların kullandığı işareti "tamga" adı verilir. Bu işaret hayvanlara, eşyalara ve mezar taşlarına vurulurken, mülkiyeti ve aidiyeti gösterirdi. (Kaynak: oguz-boylari-ve-turk-boy-yapisi.md)

Getirilen: `oguz-boylari-ve-turk-boy-yapisi.md#1 0.590 | oguz-boylari-ve-turk-boy-yapisi.md#2 0.565 | oguz-boylari-ve-turk-boy-yapisi.md#4 0.524 | oguz-boylari-ve-turk-boy-yapisi.md#3 0.492 | oguz-boylari-ve-turk-boy-yapisi.md#0 0.483`

**bozkir-1** — Bozkırda yazın çıkılan otlağa ne ad verilir?
> Yazın çıkılan otlağa yaylak adı verilir. (Kaynak: bozkir-gocebe-yasami.md)

Getirilen: `bozkir-gocebe-yasami.md#2 0.677 | bozkir-gocebe-yasami.md#1 0.585 | oguz-boylari-ve-turk-boy-yapisi.md#2 0.555`

**bozkir-2** — Bozkır çadırının tepesindeki çember ne işe yarar?
> Bozkır çadırının tepesindeki çember hem baca hem pencere görevi görür ve dumanı dışarı verir. (Kaynak: bozkir-gocebe-yasami.md)

Getirilen: `bozkir-gocebe-yasami.md#2 0.726 | bozkir-gocebe-yasami.md#5 0.573 | turk-kulturunde-at.md#0 0.544 | bozkir-gocebe-yasami.md#6 0.536 | bozkir-gocebe-yasami.md#0 0.511`

**bozkir-3** — Hükümdarın çadırına ne ad verilir?
> Hükümdarın çadırına otağ denilir. (Kaynak: bozkir-gocebe-yasami.md)

Getirilen: `turk-devlet-gelenegi.md#0 0.499 | bozkir-gocebe-yasami.md#2 0.494 | turk-devlet-gelenegi.md#2 0.458 | osmanli-devlet-teskilati.md#1 0.450 | osmanli-devlet-teskilati.md#2 0.443`

**bozkir-4** — Bilinen en eski düğümlü halı nerede bulunmuştur?
> Altay Dağları'ndaki Pazırık kurganında bulunulan ve bugün bilinen en eski düğümlü halı, bu sanatın eskiye gittiğini göstermektedir. (Kaynak: bozkir-gocebe-yasami.md)

Getirilen: `bozkir-gocebe-yasami.md#5 0.696 | ilk-turk-islam-eserleri.md#4 0.455`

**bozkir-5** — Göktürkler ipek ticareti için hangi devlete elçilik göndermiştir?
> Göktürkler ipek ticaretini İran'ın tekelinden çıkarmak için 568 yılında Bizans'a elçilik heyeti göndermiştir. (Kaynak: bozkir-gocebe-yasami.md)

Getirilen: `bozkir-gocebe-yasami.md#7 0.691 | bozkir-gocebe-yasami.md#6 0.559 | turklerin-islamiyeti-kabulu.md#2 0.548 | ilk-turk-devletleri.md#1 0.513 | turklerin-islamiyeti-kabulu.md#0 0.513`

**nevruz-1** — Nevruz hangi tarihte kutlanır?
> Nevruz, 21 Mart'ta kutlanır. Bu tarih, gece ile gündüzün eşitlendiği ilkbahar gündönümünde gerçekleşir ve bahar bayramı olarak kutlanır. (Kaynak: nevruz-ve-turk-bayramlari.md)

Getirilen: `nevruz-ve-turk-bayramlari.md#0 0.762 | nevruz-ve-turk-bayramlari.md#5 0.696 | nevruz-ve-turk-bayramlari.md#6 0.673 | nevruz-ve-turk-bayramlari.md#1 0.631 | nevruz-ve-turk-bayramlari.md#2 0.587`

**nevruz-2** — Nevruz Kazakistan'da hangi adla anılır?
> Kazakistan'da Nevruz bayramı Nauryz adıyla anılır. (Kaynak: nevruz-ve-turk-bayramlari.md)

Getirilen: `nevruz-ve-turk-bayramlari.md#2 0.657 | nevruz-ve-turk-bayramlari.md#0 0.584 | nevruz-ve-turk-bayramlari.md#1 0.530 | nevruz-ve-turk-bayramlari.md#6 0.525 | nevruz-ve-turk-bayramlari.md#5 0.516`

**nevruz-3** — Nevruz'da buğdayın filizlendirilmesiyle hazırlanan yiyeceğin adı nedir?
> Nevruz'ta buğdayın filizlendirilmesiyle hazırlanan yiyecek adı semeni veya sümelek'tir. (Kaynak: nevruz-ve-turk-bayramlari.md)

Getirilen: `nevruz-ve-turk-bayramlari.md#4 0.650 | nevruz-ve-turk-bayramlari.md#2 0.576 | nevruz-ve-turk-bayramlari.md#0 0.564 | nevruz-ve-turk-bayramlari.md#1 0.556 | nevruz-ve-turk-bayramlari.md#5 0.516`

**nevruz-4** — Hıdrellez hangi tarihte kutlanır?
> Hıdrellez, 6 Mayıs'ta kutlanır. (Kaynak: nevruz-ve-turk-bayramlari.md)

Getirilen: `nevruz-ve-turk-bayramlari.md#6 0.637 | turk-denizciligi.md#3 0.505`

**nevruz-5** — Hıdrellez adı nereden gelmektedir?
> Hıdrellez adı, inanışa göre Hızır ve İlyas adlarının birleşmesinden gelmektedir; bu iki kişi yılda bir kez 6 Mayıs'ta buluştuğuna göre adın kaynağı buradan elde edilmiştir. (Kaynak: nevruz-ve-turk-bayramlari.md)

Getirilen: `nevruz-ve-turk-bayramlari.md#6 0.529 | oguz-boylari-ve-turk-boy-yapisi.md#4 0.319`

**ozan-1** — İslamiyet öncesinde destan anlatan kişiye ne ad verilirdi?
> İslamiyet öncesi dönemde destan anlatan kişiye ozan denilirdi. (Kaynak: ozan-asik-gelenegi.md)

Getirilen: `turk-destanlari.md#0 0.627 | turk-destanlari.md#1 0.546 | ozan-asik-gelenegi.md#0 0.541 | ilk-turk-islam-eserleri.md#6 0.540 | ilk-turk-islam-eserleri.md#7 0.532`

**ozan-2** — Kırgızlarda destan anlatıcısına ne ad verilir?
> Kırgızlarda destan anlatıcısına manasçı denir. (Kaynak: ozan-asik-gelenegi.md)

Getirilen: `ozan-asik-gelenegi.md#2 0.677 | turk-destanlari.md#3 0.634 | turk-destanlari.md#1 0.628 | turk-kulturunde-kurt.md#2 0.563 | oguz-boylari-ve-turk-boy-yapisi.md#8 0.518`

**ozan-3** — İki âşığın karşılıklı doğaçlama şiir söylemesine ne ad verilir?
> İki âşığın karşılıklı doğaçlama şiir söylemesine atışma ya da karşılaşma denir. (Kaynak: ozan-asik-gelenegi.md)

Getirilen: `ozan-asik-gelenegi.md#3 0.577 | ozan-asik-gelenegi.md#4 0.502 | ozan-asik-gelenegi.md#0 0.428 | bozkir-gocebe-yasami.md#1 0.428 | turk-kulturunde-at.md#1 0.415`

**ozan-4** — Telli sazların atası sayılan çalgı hangisidir?
> Telli sazların atası sayılan çalgı kopuzdur. (Kaynak: ozan-asik-gelenegi.md)

Getirilen: `ozan-asik-gelenegi.md#6 0.637 | ozan-asik-gelenegi.md#7 0.552`

**ozan-5** — Bağlama ailesinin en küçük üyesi hangisidir?
> Bağlama ailesinin en küçük üyesi curadır. (Kaynak: ozan-asik-gelenegi.md)

Getirilen: `ozan-asik-gelenegi.md#7 0.551 | oguz-boylari-ve-turk-boy-yapisi.md#0 0.419`

**bilim-1** — Cebir sözcüğü kimin eserinden gelmektedir?
> Cebir sözcüğü el-Hârezmî'nin "Kitâbü'l-Muhtasar fî Hisâbi'l-Cebr ve'l-Mukabele" adlı eserinin adından gelmektedir. (Kaynak: turk-islam-dunyasinda-bilim.md)

Getirilen: `turk-islam-dunyasinda-bilim.md#1 0.574 | turkcenin-tarihi-ve-alfabeleri.md#2 0.480 | turkcenin-tarihi-ve-alfabeleri.md#0 0.463 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#4 0.460 | ilk-turk-islam-eserleri.md#6 0.455`

**bilim-2** — Fârâbî'ye hangi unvan verilmiştir?
> Fârâbî, "Muallim-i Sânî" yani İkinci Öğretmen unvanı verilmiştir. (Kaynak: turk-islam-dunyasinda-bilim.md)

Getirilen: `turk-islam-dunyasinda-bilim.md#2 0.757 | turk-islam-dunyasinda-bilim.md#1 0.436`

**bilim-3** — İbn Sînâ'nın tıp alanındaki temel eseri hangisidir?
> İbn Sînâ'nın tıp alanındaki temel eseri "el-Kânûn fi't-Tıbb" adlı eseridir. (Kaynak: turk-islam-dunyasinda-bilim.md)

Getirilen: `turk-islam-dunyasinda-bilim.md#3 0.813 | ilk-turk-islam-eserleri.md#5 0.461`

**bilim-4** — Uluğ Bey kimin torunudur?
> Uluğ Bey, Timur'un torunudur. (Kaynak: turk-islam-dunyasinda-bilim.md)

Getirilen: `turk-islam-dunyasinda-bilim.md#5 0.775 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.518`

**bilim-5** — Ali Kuşçu'yu İstanbul'a kim davet etmiştir?
> Fatih Sultan Mehmed'nin daveti üzerine Ali Kuşçu İstanbul'a gelmiştir. (Kaynak: turk-islam-dunyasinda-bilim.md)

Getirilen: `turk-islam-dunyasinda-bilim.md#6 0.759 | ilk-turk-islam-eserleri.md#7 0.467`

**mimari-1** — Selçuklu yapılarındaki anıtsal giriş kapısına ne ad verilir?
> Selçuklu yapılarındaki anıtsal giriş kapısına taçkapı denir. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)

Getirilen: `selcuklu-ve-osmanli-mimarisi.md#0 0.719 | selcuklu-ve-osmanli-mimarisi.md#1 0.610 | selcuklu-ve-osmanli-mimarisi.md#6 0.572 | selcuklu-ve-osmanli-mimarisi.md#2 0.551 | selcuklu-ve-osmanli-mimarisi.md#7 0.549`

**mimari-2** — Altında mezar odası bulunan anıt mezara ne ad verilir?
> Kümbet, altındaki mezar odası bulunan anıt mezara kümbet adı verilir. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)

Getirilen: `turk-mitolojisi-ve-gok-tanri.md#2 0.518 | selcuklu-ve-osmanli-mimarisi.md#1 0.511 | milli-semboller.md#7 0.503 | bozkir-gocebe-yasami.md#2 0.457 | milli-semboller.md#8 0.455`

**mimari-3** — Divriği Ulu Camii ne zaman yapılmıştır?
> Divriği Ulu Camii, 1228-1229 yıllarında yapılmıştır. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)

Getirilen: `selcuklu-ve-osmanli-mimarisi.md#2 0.773 | selcuklu-ve-osmanli-mimarisi.md#6 0.559`

**mimari-4** — Mimar Sinan ustalık eseri olarak hangi yapıyı göstermiştir?
> Mimar Sinan ustalık eseri olarak Edirne'deki Selimiye Camii'ni göstermiştir. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)

Getirilen: `selcuklu-ve-osmanli-mimarisi.md#5 0.718 | selcuklu-ve-osmanli-mimarisi.md#6 0.714 | selcuklu-ve-osmanli-mimarisi.md#0 0.576 | selcuklu-ve-osmanli-mimarisi.md#4 0.561 | selcuklu-ve-osmanli-mimarisi.md#1 0.544`

**mimari-5** — Kervansaraylar birbirinden hangi aralıklarla yapılmıştır?
> Kervansaraylar ortalama otuz ila kırk kilometre aralıklarla yapılmıştır. (Kaynak: selcuklu-ve-osmanli-mimarisi.md)

Getirilen: `selcuklu-ve-osmanli-mimarisi.md#3 0.765 | selcuklu-ve-osmanli-mimarisi.md#1 0.511`

**deniz-1** — Bilinen ilk Türk denizci beyi kimdir?
> Bilinen ilk Türk denizci beyi Çaka Bey'dir. Çaka Bey, 1081'de İzmir'i merkez yaparak bir beylik kuran kişi olarak anılmaktadır. Kendi tersanesini kurup donanma oluşturmuş, Ege adalarına seferler düzenlemiş ve Bizans donanmasıyla denizde çarpışmıştır. (Kaynak: turk-denizciligi.md)

Getirilen: `turk-denizciligi.md#0 0.774 | turk-denizciligi.md#1 0.633 | ilk-turk-islam-eserleri.md#0 0.597 | ilk-turk-islam-eserleri.md#6 0.596 | turk-denizciligi.md#2 0.585`

**deniz-2** — Preveze Deniz Savaşı hangi tarihte yapılmıştır?
> Preveze Deniz Savaşı 28 Eylül 1538'de yapılmıştır. (Kaynak: turk-denizciligi.md)

Getirilen: `turk-denizciligi.md#3 0.838 | turk-denizciligi.md#8 0.553`

**deniz-3** — Preveze'de Osmanlı donanmasının karşısındaki komutan kimdir?
> Andrea Doria komutasındaki Haçlı donanmasının Preveze'de Osmanlı donanmasının karşısındaki komutanı idi. (Kaynak: turk-denizciligi.md)

Getirilen: `turk-denizciligi.md#3 0.670 | mustafa-kemal-ataturk.md#3 0.520 | osmanli-devlet-teskilati.md#2 0.509 | turk-denizciligi.md#1 0.503 | selcuklu-ve-osmanli-mimarisi.md#5 0.480`

**deniz-4** — Piri Reis'in Akdeniz kılavuzu niteliğindeki eseri hangisidir?
> Piri Reis'in Akdeniz kılavuzu niteliğindeki eseri Kitâb-ı Bahriye'dir. Bu kılavuz, Akdeniz kıyılarını, limanları, akıntıları, sığlıkları, demirleme yerlerini ve şehirleri haritalarla detaylı olarak anlatır. (Kaynak: turk-denizciligi.md)

Getirilen: `turk-denizciligi.md#6 0.837 | turk-denizciligi.md#5 0.784 | turk-denizciligi.md#4 0.612`

**deniz-5** — Kabotaj Kanunu ne zaman yürürlüğe girmiştir?
> Kabotaj Kanunu 1 Temmuz 1926'da yürürlüğe girmiştir. (Kaynak: turk-denizciligi.md)

Getirilen: `turk-denizciligi.md#9 0.663 | cumhuriyet-inkilaplari.md#4 0.471`

**sembol-1** — İstiklal Marşı TBMM'de hangi tarihte kabul edilmiştir?
> İstiklal Marşı, Türkiye Büyük Millet Meclisi'nde 12 Mart 1921'de millî marş olarak kabul edilmiştir. (Kaynak: milli-semboller.md)

Getirilen: `milli-semboller.md#1 0.686 | milli-semboller.md#0 0.675 | milli-semboller.md#2 0.584 | osmanli-islahat-ve-mesrutiyet.md#9 0.531 | milli-semboller.md#9 0.528`

**sembol-2** — Mehmet Âkif İstiklal Marşı'nı nerede yazmıştır?
> Mehmet Âkif İstiklal Marşı'nı Ankara'daki Tacettin Dergâhı'nda yazmıştır. (Kaynak: milli-semboller.md)

Getirilen: `milli-semboller.md#0 0.746 | milli-semboller.md#1 0.676 | milli-semboller.md#2 0.566 | milli-semboller.md#4 0.542`

**sembol-3** — İstiklal Marşı kaç mısradan oluşur?
> İstiklal Marşı kırk bir mısradan oluşur. (Kaynak: milli-semboller.md)

Getirilen: `milli-semboller.md#0 0.732 | milli-semboller.md#1 0.684 | milli-semboller.md#2 0.605 | osmanli-islahat-ve-mesrutiyet.md#9 0.517`

**sembol-4** — Anıtkabir'in projesini kimler hazırlamıştır?
> Anıtkabir'in projesini Emin Onat ve Orhan Arda hazırlamıştır. (Kaynak: milli-semboller.md)

Getirilen: `milli-semboller.md#7 0.656 | milli-semboller.md#8 0.548`

**sembol-5** — Anıtkabir'deki Aslanlı Yol'da kaç aslan heykeli vardır?
> Anıtkabir'deki Aslanlı Yololu'nda 24 aslan heykeli vardır. (Kaynak: milli-semboller.md)

Getirilen: `milli-semboller.md#8 0.683 | milli-semboller.md#7 0.483`

**dunya-1** — Kuzey Kıbrıs Türk Cumhuriyeti ne zaman ilan edilmiştir?
> Kuzey Kıbrıs Türk Cumhuriyeti 15 Kasım 1983'te ilan edilmiştir. (Kaynak: bugunku-turk-dunyasi.md)

Getirilen: `bugunku-turk-dunyasi.md#2 0.894 | bugunku-turk-dunyasi.md#1 0.622`

**dunya-2** — Türk Devletleri Teşkilatı hangi anlaşmayla kurulmuştur?
> Türk Devletleri Teşkilatı Nahçıvan Anlaşmasıyla kurulmuştur. Bu anlaşma 3 Ekim 2009'da imzalanmıştır. (Kaynak: bugunku-turk-dunyasi.md)

Getirilen: `bugunku-turk-dunyasi.md#4 0.697 | turk-milliyetciliginin-dogusu.md#4 0.640 | bugunku-turk-dunyasi.md#5 0.623 | ilk-turk-devletleri.md#1 0.599 | turk-devlet-gelenegi.md#2 0.596`

**dunya-3** — Türk Keneşi'nin adı ne zaman Türk Devletleri Teşkilatı olarak değişmiştir?
> Türk Dili Konuşan Ülkeler İşbirliği Konseyi adıyla kurulduktan 12 Kasım 2021'de İstanbul zirvesinde Türk Devletleri Teşkilatı olarak adı değiştirilmiştir. (Kaynak: bugunku-turk-dunyasi.md)

Getirilen: `bugunku-turk-dunyasi.md#4 0.717 | turk-milliyetciliginin-dogusu.md#4 0.615 | bugunku-turk-dunyasi.md#2 0.602 | turkcenin-tarihi-ve-alfabeleri.md#4 0.564 | ilk-turk-devletleri.md#1 0.553`

**dunya-4** — TÜRKSOY ne zaman kurulmuştur?
> TÜRKSOY, 1993'te kurulmuştur. (Kaynak: bugunku-turk-dunyasi.md)

Getirilen: `bugunku-turk-dunyasi.md#5 0.719 | turk-milliyetciliginin-dogusu.md#4 0.676 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.517 | ilk-turk-devletleri.md#4 0.531 | ilk-turk-devletleri.md#1 0.578`

**dunya-5** — Moldova'daki özerk Türk bölgesinin adı nedir?
> Moldova'daki özerk Türk bölgesinin adı Gagavuz Yeri özerk bölgesidir. (Kaynak: bugunku-turk-dunyasi.md)

Getirilen: `bugunku-turk-dunyasi.md#3 0.654 | bugunku-turk-dunyasi.md#0 0.492 | turk-milliyetciliginin-dogusu.md#0 0.484 | bugunku-turk-dunyasi.md#5 0.473 | bugunku-turk-dunyasi.md#4 0.464`

**cevapsiz-1** — Fatih Sultan Mehmed'in annesinin adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-padisahlari.md#2 0.652 | osmanli-devlet-teskilati.md#9 0.511 | osmanli-padisahlari.md#4 0.508 | mustafa-kemal-ataturk.md#0 0.500 | milli-semboller.md#4 0.476`

**cevapsiz-2** — Malazgirt Savaşı'nda Selçuklu ordusu kaç askerden oluşuyordu?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `selcuklular-ve-malazgirt.md#0 0.691 | selcuklular-ve-malazgirt.md#1 0.675 | selcuklular-ve-malazgirt.md#2 0.643 | selcuklular-ve-malazgirt.md#4 0.636 | selcuklular-ve-malazgirt.md#3 0.585`

**cevapsiz-3** — Kanuni Sultan Süleyman'ın eşinin adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-padisahlari.md#4 0.575 | osmanli-devlet-teskilati.md#9 0.532 | osmanli-islahat-ve-mesrutiyet.md#0 0.521 | selcuklu-ve-osmanli-mimarisi.md#5 0.519 | osmanli-padisahlari.md#2 0.497`

**cevapsiz-4** — Lozan Antlaşması'nı Türk heyeti adına kim imzalamıştır?
> Lozan Antlaşması'nı Türk heyeti adına İsmet İnönü imzalamıştır. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#7 0.533 | osmanli-islahat-ve-mesrutiyet.md#3 0.531 | bugunku-turk-dunyasi.md#4 0.526 | canakkale-ve-kurtulus-savasi.md#4 0.521 | ilk-turk-islam-eserleri.md#7 0.472`

**cevapsiz-5** — Orhun Yazıtları bugün hangi müzede sergilenmektedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `ilk-turk-devletleri.md#2 0.659 | turkcenin-tarihi-ve-alfabeleri.md#0 0.571 | bugunku-turk-dunyasi.md#7 0.474 | turk-devlet-gelenegi.md#1 0.463`

**cevapsiz-6** — Mete Han'ın babasının adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `ilk-turk-devletleri.md#0 0.516 | ozan-asik-gelenegi.md#8 0.438 | milli-semboller.md#3 0.409 | mustafa-kemal-ataturk.md#0 0.393 | turklerin-islamiyeti-kabulu.md#2 0.383`

**cevapsiz-7** — Bugün hava nasıl olacak?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `bugunku-turk-dunyasi.md#0 0.381 | bozkir-gocebe-yasami.md#1 0.323 | turk-kulturunde-kurt.md#6 0.317 | bugunku-turk-dunyasi.md#6 0.297 | turk-mitolojisi-ve-gok-tanri.md#0 0.295`

**cevapsiz-8** — Python'da bir liste nasıl sıralanır?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.369 | bugunku-turk-dunyasi.md#6 0.338 | turk-denizciligi.md#6 0.320 | ozan-asik-gelenegi.md#4 0.307 | turk-mitolojisi-ve-gok-tanri.md#6 0.307`

**cevapsiz-9** — Futbolda ofsayt kuralı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `oguz-boylari-ve-turk-boy-yapisi.md#1 0.368 | oguz-boylari-ve-turk-boy-yapisi.md#2 0.353 | nevruz-ve-turk-bayramlari.md#4 0.331 | bozkir-gocebe-yasami.md#1 0.330 | milli-semboller.md#5 0.326`

**cevapsiz-10** — asdf qwerty zxcv
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.374 | bugunku-turk-dunyasi.md#6 0.372 | turkcenin-tarihi-ve-alfabeleri.md#1 0.326 | ilk-turk-devletleri.md#3 0.326 | turk-kulturunde-kurt.md#6 0.313`

**takip-1#1** — Malazgirt Savaşı ne zaman yapılmıştır?
> Malazgirt Savaşı 26 Ağustos 1071'de yapılmıştır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.663 | selcuklular-ve-malazgirt.md#2 0.660 | selcuklular-ve-malazgirt.md#0 0.634 | selcuklular-ve-malazgirt.md#4 0.572 | turklerin-islamiyeti-kabulu.md#1 0.486`

**takip-1#2** — sonucu ne oldu?  
_Önceki soru: Malazgirt Savaşı ne zaman yapılmıştır?_
> Savaşın sonuç olarak Selçukluların zaferiyle Malazgirt Ovası'nda Bizans İmparatoru IV. Romanos Diogenes'in ordusu yenilgiye uğramış ve imparator esir alınmıştır. Bu zafer, Bizans'ın Anadolu'daki savunma düzeninin çökmesine ve Türkmen boylarının Anadolu içlerine doğru yerleşmesine neden olmuştur. Bu nedenle 1071 yılı, Anadolu'nun Türkleşme sürecinin başlangıcı olarak kabul edilir.  Sonuç olarak, Malazgirt Savaşı'nın sonucunda Bizans'a yenilgi ve Anadolu'nun Türkmen boylarının yerleşmesi gerçekleşmiştir. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.681 | selcuklular-ve-malazgirt.md#2 0.668 | selcuklular-ve-malazgirt.md#0 0.634 | selcuklular-ve-malazgirt.md#4 0.594 | selcuklular-ve-malazgirt.md#3 0.500`

**takip-2#1** — Orhun Yazıtları'nın alfabesini kim çözmüştür?
> Orhun Yazıtları'nın alfabesini çözmüş olan kişi Danimarkalı dilbilimci Vilhelm Thomsen 1893'te olmuştur. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.741 | ilk-turk-devletleri.md#2 0.663 | turkcenin-tarihi-ve-alfabeleri.md#1 0.580 | ilk-turk-devletleri.md#3 0.567 | bugunku-turk-dunyasi.md#6 0.543`

**takip-2#2** — hangi yılda?  
_Önceki soru: Orhun Yazıtları'nın alfabesini kim çözmüştür?_
> 1 Kasım 1928'de kabul edilen Harf Devrimi ile Latin alfabesine dayalı yeni Türk alfabesine geçilmiştir. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.735 | ilk-turk-devletleri.md#2 0.673 | turkcenin-tarihi-ve-alfabeleri.md#3 0.586 | ilk-turk-devletleri.md#3 0.570 | bugunku-turk-dunyasi.md#6 0.547`

**takip-3#1** — Manas Destanı hangi topluma aittir?
> Manas Destanı Kırgızlara aittir. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#3 0.748 | ozan-asik-gelenegi.md#2 0.635 | turk-destanlari.md#1 0.527`

**takip-3#2** — kaç dizeden oluşur?  
_Önceki soru: Manas Destanı hangi topluma aittir?_
> Manas Destanı, farklı derlemelerde yarım milyon dizeye yaklaşır. Bu destanın boyutu, kırgızların destan anlatıcısına manasçı denildiği gibi anlatıldığı bilinmektedir. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#3 0.790 | ozan-asik-gelenegi.md#2 0.631`

**takip-4#1** — Kanuni Sultan Süleyman kaç yıl hüküm sürmüştür?
> Kanuni Sultan Süleyman 1520-1566 yılları arasında kırk altı yıl hüküm sürmüştür. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#4 0.705 | osmanli-islahat-ve-mesrutiyet.md#0 0.593 | osmanli-padisahlari.md#0 0.570 | selcuklu-ve-osmanli-mimarisi.md#5 0.519 | selcuklular-ve-malazgirt.md#3 0.513`

**takip-4#2** — onun döneminde hangi şehir kuşatıldı?  
_Önceki soru: Kanuni Sultan Süleyman kaç yıl hüküm sürmüştür?_
> Kanuni Sultan Süleyman döneminde Viyana kuşatılmıştır. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#4 0.699 | osmanli-islahat-ve-mesrutiyet.md#0 0.640 | selcuklular-ve-malazgirt.md#3 0.597 | osmanli-padisahlari.md#0 0.575 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#8 0.551`

**takip-5#1** — İsmail Gaspıralı hangi gazeteyi çıkarmıştır?
> İsmail Gaspıralı, 1883'te Kırım'da Tercüman gazetesini çıkarmıştır. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#3 0.753 | turk-milliyetciliginin-dogusu.md#2 0.502`

**takip-5#2** — bu gazete nerede çıkarıldı?  
_Önceki soru: İsmail Gaspıralı hangi gazeteyi çıkarmıştır?_
> Kırım'da çıkarılmıştır. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#3 0.726 | turk-milliyetciliginin-dogusu.md#2 0.473`

**takip-cevapsiz-1#1** — Sakarya Meydan Muharebesi kaç gün sürmüştür?
> Sakarya Meydan Muharebesi 23 Ağustos - 13 Eylül 1921 tarihleri arasında yirmi iki gün süren bir muharebe olmuştur. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#3 0.572 | selcuklu-ve-osmanli-mimarisi.md#3 0.496 | mustafa-kemal-ataturk.md#4 0.461 | milli-semboller.md#7 0.439 | osmanli-islahat-ve-mesrutiyet.md#0 0.437`

**takip-cevapsiz-1#2** — bunun sebebi ne?  
_Önceki soru: Sakarya Meydan Muharebesi kaç gün sürmüştür?_
> Osmanlı'da yeniden yapılanma sürecinin temel sebeplerinden biri, devletin çevresindeki güç dengesinin değişmesidir. İran savaşlarının uzun süreceği ve Avusturya ile olan anlaşmanın protokol açısından Osmanlı padişahına denk sayılması gibi olaylar, Osmanlı devletinin iç ve dış durumunu değiştirdiği ve reformların gerekliliğini artırarak reform hareketlerinin başlamasını sağlamıştır. (Kaynak: osmanli-islahat-ve-mesrutiyet.md)

Getirilen: `canakkale-ve-kurtulus-savasi.md#3 0.579 | selcuklu-ve-osmanli-mimarisi.md#3 0.494 | mustafa-kemal-ataturk.md#4 0.463 | osmanli-islahat-ve-mesrutiyet.md#0 0.459 | osmanli-islahat-ve-mesrutiyet.md#6 0.438`

**takip-cevapsiz-2#1** — Türk Ocağı ne zaman kurulmuştur?
> Türk Ocağı 25 Mart 1912'de kurulmuştur. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.750 | bugunku-turk-dunyasi.md#5 0.615 | ilk-turk-devletleri.md#1 0.603 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.592 | bugunku-turk-dunyasi.md#4 0.581`

**takip-cevapsiz-2#2** — ilk başkanı kimdi?  
_Önceki soru: Türk Ocağı ne zaman kurulmuştur?_
> Mustafa Kemal Atatürk, 29 Ekim 1923'te Cumhuriyet'in ilanıyla Türkistan Cumhuriyeti'nin ilk cumhurbaşkanı seçildi. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `ilk-turk-devletleri.md#0 0.511 | ilk-turk-islam-eserleri.md#0 0.501 | mustafa-kemal-ataturk.md#5 0.497 | ilk-turk-devletleri.md#1 0.491 | cumhuriyet-inkilaplari.md#1 0.469`

**degisim-1#1** — böri nedir
> Eski Türkçede kurdun adı "böri" idi. Bu sözcük Orhun Yazıtları'nda ve on birinci yüzyılda Kaşgarlı Mahmud'un yazdığı Dîvânu Lugâti't-Türk'te geçer. Bugün Kazakçada börı, Kırgızcada börü, Özbekçede bo'ri olarak kullanılmaktadır. Türkiye Türkçesinde ise sözcük yalnızca "bozkurt" ve destan kahramanı "Börteçine" gibi kalıplarda korunmuştur. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.563 | turk-kulturunde-kurt.md#6 0.456 | bozkir-gocebe-yasami.md#0 0.484 | bozkir-gocebe-yasami.md#2 0.467 | turk-kulturunde-at.md#0 0.442`

**degisim-1#2** — fatih kimdir  
_Önceki soru: böri nedir_
> Fatih Sultan Mehmed, 29 Mayıs 1453'te İstanbul'u fethettiğinde yirmi bir yaşındaydı. Fetihle birlikte Doğu Roma İmparatorluğu sona ermiş, Osmanlı Devleti imparatorluğa dönüşmüştür. Ayrıca, Fatih Sultan Mehmed'in hazırlattığı kanunname, devlet teşkilatını ve protokolü yazılı hâle getiren ilk kapsamlı düzenleme sayılır. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#2 0.566 | milli-semboller.md#3 0.434 | osmanli-devlet-teskilati.md#9 0.410 | turk-islam-dunyasinda-bilim.md#6 0.405 | turk-islam-dunyasinda-bilim.md#2 0.474`

**degisim-2#1** — Orhan Gazi kimdir
> Orhan Gazi, Osmanlı Padişahlarının kurucusu Osman Gazi'nin oğludur ve Osmanlı Devleti'nin kurulmasında önemli rol oynamıştır. Onun döneminde Bursa şehrinin alınması ve Rumeli'ye geçiş yapılmıştır. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#1 0.574 | osmanli-padisahlari.md#0 0.465 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.416`

**degisim-2#2** — böri nedir  
_Önceki soru: Orhan Gazi kimdir_
> Eski Türkçede kurdun adı "böri" idi. Bu sözcük Orhun Yazıtları'nda ve on birinci yüzyılda Kaşgarlı Mahmud'un yazdığı Dîvânu Lugâti't-Türk'te geçer. Bugün Kazakçada börı, Kırgızcada börü, Özbekçede bo'ri olarak kullanılmaktadır. Türkiye Türkçesinde ise sözcük yalnızca "bozkurt" ve destan kahramanı "Börteçine" gibi kalıplarda korunmuştur. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.563 | turk-kulturunde-kurt.md#6 0.456 | bozkir-gocebe-yasami.md#0 0.484 | bozkir-gocebe-yasami.md#2 0.467 | turk-kulturunde-at.md#0 0.442`

**degisim-3#1** — Turan taktiği nasıl uygulanır?
> Turan taktiği, merkez birlikler sahte bir geri çekilme yaparak uygulanır. Düşmanın takibe başladığında, kanatlar hilal biçiminde kapanarak düşmana kuşatma oluşturur. Bu yöntem, atlı okçuluk becerisi ve atlı savaş stratejisi ile birlikte, Türk ordularının ağır piyadeye karşı hareket üstünlüğünü sağlar. Malazgirt Savaşı'nda da bu taktik kullanılmıştır. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#1 0.656 | turk-devlet-gelenegi.md#1 0.501 | turk-devlet-gelenegi.md#5 0.498 | osmanli-devlet-teskilati.md#3 0.497 | osmanli-devlet-teskilati.md#4 0.496`

**degisim-3#2** — Kımız nedir?  
_Önceki soru: Turan taktiği nasıl uygulanır?_
> Kısrak sütünün mayalanmasıyla elde edilen kımız, sağılan süt deriden yapılmış tulumlara konup düzenli olarak çalkalanarak mayalandırılır; ortaya çıkan içecek hafif ekşi tatlı ve düşük alkollüdür. Kımız yaz aylarında hazırlanır, şölenlerde ve konuk ağırlamada ikram edilir. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#3 0.475 | turk-mitolojisi-ve-gok-tanri.md#5 0.351`

**degisim-4#1** — Harf Devrimi hangi tarihte kabul edilmiştir?
> Harf Devrimi 1 Kasım 1928'de kabul edilmiştir. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#3 0.712 | turkcenin-tarihi-ve-alfabeleri.md#4 0.555 | bugunku-turk-dunyasi.md#6 0.550 | cumhuriyet-inkilaplari.md#5 0.550 | ilk-turk-devletleri.md#3 0.530`

**degisim-4#2** — Tuğ nedir?  
_Önceki soru: Harf Devrimi hangi tarihte kabul edilmiştir?_
> Tuğ, at kılından yapılan ve sırık üzerinde taşınan bayrak niteliğindeki bir semboldür. Hükümdarlık sembolleri arasında tuğ sayılır ve sayısı hükümdarın rütbesine göre değişebilir. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#4 0.555 | turk-mitolojisi-ve-gok-tanri.md#6 0.452 | oguz-boylari-ve-turk-boy-yapisi.md#0 0.491 | oguz-boylari-ve-turk-boy-yapisi.md#2 0.484 | turk-destanlari.md#1 0.477`

**disi-1#1** — Osman Gazi kimdir
> Osman Gazi, Osmanlı Devleti'nin kurucusudur. Devlet altı yüz yıldan uzun süre varlığını sürdürmüş ve toplam otuz altı padişah tarafından yönetilmiştir. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#0 0.676 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.586 | osmanli-padisahlari.md#1 0.659 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#3 0.518 | osmanli-islahat-ve-mesrutiyet.md#1 0.508`

**disi-1#2** — Bugün hava nasıl olacak?  
_Önceki soru: Osman Gazi kimdir_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `bugunku-turk-dunyasi.md#0 0.381 | bozkir-gocebe-yasami.md#1 0.323 | turk-kulturunde-kurt.md#6 0.317 | bugunku-turk-dunyasi.md#6 0.297 | turk-mitolojisi-ve-gok-tanri.md#0 0.295`

**disi-2#1** — Eski Türkçede kurdun adı neydi?
> Eski Türkçede kurdun adı "böri" idi. Bu sözcük Orhun Yazıtları'nda ve on birinci yüzyılda Kaşgarlı Mahmud'un yazdığı Dîvânu Lugâti't-Türk'te geçer. Ayrıca, bugün birçok Türk lehçesinde bile böri biçimi kullanılmaktadır. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.725 | turk-kulturunde-kurt.md#6 0.612 | turk-kulturunde-kurt.md#4 0.591 | turk-kulturunde-kurt.md#0 0.510`

**disi-2#2** — asdf qwerty zxcv  
_Önceki soru: Eski Türkçede kurdun adı neydi?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-kulturunde-kurt.md#5 0.719 | turk-kulturunde-kurt.md#6 0.615 | turk-kulturunde-kurt.md#4 0.587 | turk-kulturunde-kurt.md#0 0.511`

**disi-3#1** — Osman Gazi kimdir
> Osman Gazi, Osmanlı Devleti'nin kurucusudur. Devlet altı yüz yıldan uzun süre varlığını sürdürmüş ve toplam otuz altı padişah tarafından yönetilmiştir. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#0 0.676 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.586 | osmanli-padisahlari.md#1 0.659 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#3 0.518 | osmanli-islahat-ve-mesrutiyet.md#1 0.508`

**disi-3#2** — Python listesi nasıl sıralanır?  
_Önceki soru: Osman Gazi kimdir_
> Python listesi sıralanırken genellikle aşağıdaki adımlar izlenir:  - Liste oluşturmak için [] kullanılır. - Liste elemanlarına index numaralarıyla erişilir. - Elemanları sırayla eklemek için .append() metodu kullanılır. - Listeyi istediğimiz şekilde sıralayabiliriz.  Örnek:  ```python liste = [] liste.append("elma") liste.append("armut") liste.append("portakal") print(liste) ```  (Cay: osmanli-padisahlari.md) (Kaynak: oguz-boylari-ve-turk-boy-yapisi.md)

Getirilen: `osmanli-padisahlari.md#0 0.599 | osmanli-padisahlari.md#1 0.581 | ozan-asik-gelenegi.md#0 0.550 | oguz-boylari-ve-turk-boy-yapisi.md#3 0.549 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.528`

**disi-4#1** — Malazgirt Savaşı ne zaman yapılmıştır?
> Malazgirt Savaşı 26 Ağustos 1071'de yapılmıştır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.663 | selcuklular-ve-malazgirt.md#2 0.660 | selcuklular-ve-malazgirt.md#0 0.634 | selcuklular-ve-malazgirt.md#4 0.572 | turklerin-islamiyeti-kabulu.md#1 0.486`

**disi-4#2** — Futbolda ofsayt kuralı nedir?  
_Önceki soru: Malazgirt Savaşı ne zaman yapılmıştır?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `oguz-boylari-ve-turk-boy-yapisi.md#1 0.368 | oguz-boylari-ve-turk-boy-yapisi.md#2 0.353 | nevruz-ve-turk-bayramlari.md#4 0.331 | bozkir-gocebe-yasami.md#1 0.330 | milli-semboller.md#5 0.326`

