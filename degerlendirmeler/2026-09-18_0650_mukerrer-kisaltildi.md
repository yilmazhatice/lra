# Değerlendirme: 2026-09-18 06:50 — mukerrer-kisaltildi

| Ayar | Değer |
|---|---|
| soru_seti | ana |
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
| git | d4c3ecc (kaydedilmemis degisiklik var) |
| set_parmak_izi | 9eb290ebbd |

## Özet

Puanlanan soru: 80 (64 cevaplanabilir, 16 cevaplanamaz). Senaryoların hazırlık soruları özete katılmaz.

Karşılaştırılan çalışma: `degerlendirmeler/2026-09-18_0552_209parca-kaynak-duzeltildi.json` — **uyarı: soru seti farklı, karşılaştırma kısmen geçerli**

| Ölçüt | Önceki | Şimdi |
|---|---|---|
| Tam başarı (tüm puanlanan sorular) | 87.5% | 90.0% |
| Arama: doğru parça 1. sırada (hit@1) | 82.8% | 82.8% |
| Arama: doğru parça ilk 3'te (hit@3) | 90.6% | 92.2% |
| Arama: MRR (1 = hep 1. sırada) | 0.882 | 0.883 |
| Cevaplanabilir sorularda başarı | 90.6% | 93.8% |
| Yanlış red (cevap belgede varken) | 0.0% | 0.0% |
|   bunun eşikte olanı | 0.0% | 0.0% |
| Anahtar ifadelerin tamamı cevapta | 92.2% | 95.3% |
| Bilinen yanlışı içeren cevap | 1 adet | 1 adet |
| Kaynak satırı var | 100.0% | 100.0% |
| Kaynak doğru belge | 95.3% | 96.9% |
| Cevaplanamaz soruları reddetme | 75.0% | 75.0% |
|   bunun eşikte olanı | 0.0% | 0.0% |
| Red cevabına eklenmiş kaynak satırı | 0 adet | 0 adet |
| Doğrulamada reddedilen cevaplanabilir | 0 adet | 0 adet |
| Doğrulamada reddedilen cevaplanamaz | 0 adet | 0 adet |
| Türkçe olmayan yazı kalan cevap | 0 adet | 0 adet |
| Türkçe olmayan yazı kesilen cevap | 0 adet | 0 adet |
| Süre ortalaması | 31.97 sn | 2.42 sn |
| Süre medyanı | 32.85 sn | 2.33 sn |
| En uzun süre | 67.22 sn | 4.18 sn |
| İlk token ortalaması (modele giden sorular) | 22.68 sn | 1.09 sn |
| Arama süresi ortalaması | 0.431 sn | 0.425 sn |

## Kategorilere göre

| Kategori | Soru | Başarılı | hit@1 | hit@3 | Yanlış red |
|---|---|---|---|---|---|
| normal | 46 | 46 | 39 | 44 | 0 |
| ozel_ad | 9 | 8 | 7 | 8 | 0 |
| yakin | 6 | 5 | - | - | - |
| konu_disi | 3 | 3 | - | - | - |
| anlamsiz | 1 | 1 | - | - | - |
| takip | 5 | 3 | 4 | 4 | 0 |
| takip_cevapsiz | 2 | 0 | - | - | - |
| konu_degisimi | 4 | 3 | 3 | 3 | 0 |
| konu_disi_sonra | 4 | 3 | - | - | - |
| hazirlik (puanlanmaz) | 15 | - | - | - | - |

Eski 12 soruluk set (eval_results.md ile aynı sorular): **10/10** başarılı.

## Önceki çalışmaya göre değişen sorular

Cevap metni değişen soru: 7. Sonucu değişen soru: 2.

- **selcuklu-4** HATA → OK: Anadolu Selçuklu Devleti'ni kim kurmuştur?
- **kurt-6** HATA → OK: Ergenekon'dan çıkan topluluğa yolu kim göstermiştir?

## Başarısız sorular

- **at-2** (ozel_ad) Kımız nedir?
  - Neden: eksik: kısrak
  - Cevap: Kımız, Türkçede at kırsaklarının mayalanmasıyla elde edilen içecektir. (Kaynak: turk-kulturunde-at.md)
- **cevapsiz-4** (yakin) Lozan Antlaşması'nı Türk heyeti adına kim imzalamıştır?
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Lozan Antlaşması'nı Türk heyeti adına İsmet İnönü imzalamıştır. (Kaynak: canakkale-ve-kurtulus-savasi.md)
- **takip-1#2** (takip) sonucu ne oldu?
  - Önceki soru: Malazgirt Savaşı ne zaman yapılmıştır?
  - Neden: yanlış kaynak: turklerin-islamiyeti-kabulu.md
  - Cevap: Bölgedeki Karluk Türklerinin Abbasîlerin yanında yer alması sonucunda Abbasî ordusu zafer elde etmiş ve Talas Savaşı'nda Çin'in Tang hanedanı orduları yenilmiştir. (Kaynak: turklerin-islamiyeti-kabulu.md)
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
- **degisim-3#2** (konu_degisimi) Kımız nedir?
  - Önceki soru: Turan taktiği nasıl uygulanır?
  - Neden: eksik: kısrak; doğru parça ilk 3'te değil (sıra 90)
  - Cevap: Kımız, Türk kültüründe atların önemli bir yer aldığını gösterir. Atlı okçuluk ve Turan taktiği gibi askeri tekniklerde atın kritik rolü vurgulanmaktadır. Ayrıca, mitolojide ve törenda atın sembolik önemi de gözlemlenir. At, Türk kültüründe ölümlere ve törenlere de dahil olmak üzere çeşitli ritüellere de katılmıştır. (Kaynak: turk-kulturunde-at.md)
- **disi-3#2** (konu_disi_sonra) Python listesi nasıl sıralanır?
  - Önceki soru: Osman Gazi kimdir
  - Neden: cevaplanamaz soruya cevap verdi
  - Cevap: Python listesi sıralanırken genellikle aşağıdaki adımlar izlenir:  - Liste oluşturmak için [] kullanılır. - Liste elemanlarına index numaralarıyla erişilir. - Elemanları sırayla eklemek için .append() metodu kullanılır. - Listeyi istediğimiz şekilde sıralayabiliriz.  Örnek:  ```python liste = [] liste.append("elma") liste.append("armut") liste.append("portakal") print(liste) ```  (Cay: osmanli-padisahlari.md) (Kaynak: oguz-boylari-ve-turk-boy-yapisi.md)

## Tüm sonuçlar

| id | Kategori | Sıra | En iyi skor | Eşikte red | Red | Anahtar | Kaynak | Süre | Sonuç |
|---|---|---|---|---|---|---|---|---|---|
| canakkale-1 | normal | 1 | 0.707 |  |  | tam | doğru | 2.1 | OK |
| canakkale-2 | normal | 1 | 0.561 |  |  | tam | doğru | 2.6 | OK |
| canakkale-3 | normal | 1 | 0.572 |  |  | tam | doğru | 2.6 | OK |
| canakkale-4 | normal | 1 | 0.474 |  |  | tam | doğru | 2.2 | OK |
| canakkale-5 | normal | 2 | 0.492 |  |  | tam | doğru | 2.5 | OK |
| ilkturk-1 | normal | 3 | 0.714 |  |  | tam | doğru | 2.9 | OK |
| ilkturk-2 | normal | 1 | 0.619 |  |  | tam | doğru | 2.6 | OK |
| ilkturk-3 | normal | 1 | 0.758 |  |  | tam | doğru | 2.2 | OK |
| ilkturk-4 | normal | 1 | 0.756 |  |  | tam | doğru | 1.7 | OK |
| ilkturk-5 | normal | 1 | 0.66 |  |  | tam | doğru | 2.0 | OK |
| ataturk-1 | normal | 1 | 0.673 |  |  | tam | doğru | 1.4 | OK |
| ataturk-2 | normal | 1 | 0.693 |  |  | tam | doğru | 1.6 | OK |
| ataturk-3 | normal | 1 | 0.479 |  |  | tam | doğru | 2.9 | OK |
| ataturk-4 | normal | 4 | 0.401 |  |  | tam | doğru | 2.4 | OK |
| ataturk-5 | normal | 1 | 0.745 |  |  | tam | doğru | 2.1 | OK |
| osmanli-1 | normal | 1 | 0.663 |  |  | tam | doğru | 3.3 | OK |
| osmanli-2 | ozel_ad | 1 | 0.566 |  |  | tam | doğru | 2.5 | OK |
| osmanli-3 | ozel_ad | 1 | 0.676 |  |  | tam | doğru | 2.3 | OK |
| osmanli-4 | ozel_ad | 1 | 0.574 |  |  | tam | doğru | 2.9 | OK |
| osmanli-5 | normal | 1 | 0.678 |  |  | tam | doğru | 2.6 | OK |
| osmanli-6 | normal | 1 | 0.705 |  |  | tam | doğru | 2.6 | OK |
| selcuklu-1 | normal | 1 | 0.748 |  |  | tam | doğru | 2.7 | OK |
| selcuklu-2 | normal | 1 | 0.663 |  |  | tam | doğru | 2.0 | OK |
| selcuklu-3 | normal | 1 | 0.756 |  |  | tam | doğru | 2.7 | OK |
| selcuklu-4 | normal | 1 | 0.779 |  |  | tam | doğru | 2.5 | OK |
| selcuklu-5 | normal | 1 | 0.484 |  |  | tam | doğru | 2.9 | OK |
| destan-1 | normal | 1 | 0.748 |  |  | tam | doğru | 1.7 | OK |
| destan-2 | normal | 1 | 0.776 |  |  | tam | doğru | 1.8 | OK |
| destan-3 | normal | 1 | 0.838 |  |  | tam | doğru | 2.2 | OK |
| destan-4 | normal | 1 | 0.628 |  |  | tam | doğru | 2.4 | OK |
| destan-5 | normal | 1 | 0.706 |  |  | tam | doğru | 2.2 | OK |
| gelenek-1 | ozel_ad | 4 | 0.559 |  |  | tam | doğru | 3.9 | OK |
| gelenek-2 | ozel_ad | 1 | 0.642 |  |  | tam | doğru | 2.1 | OK |
| gelenek-3 | normal | 1 | 0.663 |  |  | tam | doğru | 1.9 | OK |
| gelenek-4 | normal | 1 | 0.455 |  |  | tam | doğru | 3.4 | OK |
| gelenek-5 | ozel_ad | 1 | 0.552 |  |  | tam | doğru | 2.4 | OK |
| at-1 | normal | 1 | 0.656 |  |  | tam | doğru | 3.5 | OK |
| at-2 | ozel_ad | 2 | 0.351 |  |  | eksik | doğru | 2.1 | HATA |
| at-3 | normal | 1 | 0.74 |  |  | tam | doğru | 3.0 | OK |
| at-4 | normal | 1 | 0.582 |  |  | tam | doğru | 2.6 | OK |
| kurt-1 | normal | 1 | 0.725 |  |  | tam | doğru | 1.6 | OK |
| kurt-2 | ozel_ad | 1 | 0.563 |  |  | tam | doğru | 3.8 | OK |
| kurt-3 | ozel_ad | 1 | 0.52 |  |  | tam | doğru | 2.4 | OK |
| kurt-4 | normal | 1 | 0.83 |  |  | tam | doğru | 2.2 | OK |
| kurt-5 | normal | 2 | 0.71 |  |  | tam | doğru | 1.9 | OK |
| kurt-6 | normal | 3 | 0.684 |  |  | tam | doğru | 2.4 | OK |
| dogus-1 | normal | 1 | 0.687 |  |  | tam | doğru | 1.9 | OK |
| dogus-2 | normal | 7 | 0.649 |  |  | tam | doğru | 2.1 | OK |
| dogus-3 | normal | 1 | 0.773 |  |  | tam | doğru | 1.9 | OK |
| dogus-4 | normal | 1 | 0.75 |  |  | tam | doğru | 2.1 | OK |
| alfabe-1 | normal | 1 | 0.719 |  |  | tam | doğru | 2.1 | OK |
| alfabe-2 | normal | 1 | 0.712 |  |  | tam | doğru | 2.3 | OK |
| alfabe-3 | normal | 2 | 0.76 |  |  | tam | doğru | 2.5 | OK |
| alfabe-4 | normal | 1 | 0.816 |  |  | tam | doğru | 1.9 | OK |
| alfabe-5 | normal | 1 | 0.788 |  |  | tam | doğru | 2.6 | OK |
| cevapsiz-1 | yakin |  | 0.652 |  | evet |  |  | 1.8 | OK |
| cevapsiz-2 | yakin |  | 0.691 |  | evet |  |  | 2.1 | OK |
| cevapsiz-3 | yakin |  | 0.575 |  | evet |  |  | 2.0 | OK |
| cevapsiz-4 | yakin |  | 0.533 |  |  |  | var | 2.4 | HATA |
| cevapsiz-5 | yakin |  | 0.659 |  | evet |  |  | 1.7 | OK |
| cevapsiz-6 | yakin |  | 0.516 |  | evet |  |  | 1.7 | OK |
| cevapsiz-7 | konu_disi |  | 0.381 |  | evet |  |  | 1.7 | OK |
| cevapsiz-8 | konu_disi |  | 0.367 |  | evet |  |  | 1.8 | OK |
| cevapsiz-9 | konu_disi |  | 0.368 |  | evet |  |  | 1.7 | OK |
| cevapsiz-10 | anlamsiz |  | 0.372 |  | evet |  |  | 1.8 | OK |
| takip-1#1 | hazirlik |  | 0.663 |  |  |  | var | 2.0 | - |
| takip-1#2 | takip | 1 | 0.681 |  |  | tam | yanlış | 2.8 | HATA |
| takip-2#1 | hazirlik |  | 0.742 |  |  |  | var | 2.8 | - |
| takip-2#2 | takip | 5 | 0.734 |  |  | eksik | yanlış | 2.8 | HATA |
| takip-3#1 | hazirlik |  | 0.748 |  |  |  | var | 2.1 | - |
| takip-3#2 | takip | 1 | 0.79 |  |  | tam | doğru | 2.6 | OK |
| takip-4#1 | hazirlik |  | 0.705 |  |  |  | var | 2.5 | - |
| takip-4#2 | takip | 1 | 0.699 |  |  | tam | doğru | 2.6 | OK |
| takip-5#1 | hazirlik |  | 0.753 |  |  |  | var | 2.0 | - |
| takip-5#2 | takip | 1 | 0.726 |  |  | tam | doğru | 2.0 | OK |
| takip-cevapsiz-1#1 | hazirlik |  | 0.572 |  |  |  | var | 2.4 | - |
| takip-cevapsiz-1#2 | takip_cevapsiz |  | 0.579 |  |  |  | var | 3.8 | HATA |
| takip-cevapsiz-2#1 | hazirlik |  | 0.75 |  |  |  | var | 2.0 | - |
| takip-cevapsiz-2#2 | takip_cevapsiz |  | 0.511 |  |  |  | var | 2.8 | HATA |
| degisim-1#1 | hazirlik |  | 0.563 |  |  |  | var | 3.9 | - |
| degisim-1#2 | konu_degisimi | 1 | 0.566 |  |  | tam | doğru | 2.8 | OK |
| degisim-2#1 | hazirlik |  | 0.574 |  |  |  | var | 2.9 | - |
| degisim-2#2 | konu_degisimi | 1 | 0.563 |  |  | tam | doğru | 4.2 | OK |
| degisim-3#1 | hazirlik |  | 0.656 |  |  |  | var | 3.5 | - |
| degisim-3#2 | konu_degisimi | 90 | 0.657 |  |  | eksik | doğru | 3.9 | HATA |
| degisim-4#1 | hazirlik |  | 0.712 |  |  |  | var | 2.2 | - |
| degisim-4#2 | konu_degisimi | 1 | 0.552 |  |  | tam | doğru | 2.8 | OK |
| disi-1#1 | hazirlik |  | 0.676 |  |  |  | var | 2.3 | - |
| disi-1#2 | konu_disi_sonra |  | 0.381 |  | evet |  |  | 2.0 | OK |
| disi-2#1 | hazirlik |  | 0.725 |  |  |  | var | 1.6 | - |
| disi-2#2 | konu_disi_sonra |  | 0.719 |  | evet |  |  | 1.9 | OK |
| disi-3#1 | hazirlik |  | 0.676 |  |  |  | var | 2.3 | - |
| disi-3#2 | konu_disi_sonra |  | 0.599 |  |  |  | var | 3.8 | HATA |
| disi-4#1 | hazirlik |  | 0.663 |  |  |  | var | 2.0 | - |
| disi-4#2 | konu_disi_sonra |  | 0.368 |  | evet |  |  | 2.2 | OK |

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

Getirilen: `canakkale-ve-kurtulus-savasi.md#4 0.474 | turk-devlet-gelenegi.md#2 0.453 | turk-islam-dunyasinda-bilim.md#0 0.428 | turklerin-islamiyeti-kabulu.md#1 0.424 | turklerin-islamiyeti-kabulu.md#6 0.424`

**canakkale-5** — Lozan Antlaşması ne zaman imzalanmıştır?
> Lozan Antlaşması 24 Temmuz 1923'te imzalanmıştır. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#3 0.492 | canakkale-ve-kurtulus-savasi.md#4 0.485 | osmanli-islahat-ve-mesrutiyet.md#0 0.466 | cumhuriyet-inkilaplari.md#2 0.408 | bugunku-turk-dunyasi.md#4 0.400`

**ilkturk-1** — Orhun Yazıtları'nın alfabesini kim ve hangi yılda çözmüştür?
> Yazıtaların dili uzun süre çözülememişti. Danimarkalı dilbilimci Vilhelm Thomsen 1893'te alfabeyi çözmüş ve metinler böylece okunabilir hale gelmiştir. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.714 | ilk-turk-devletleri.md#2 0.660 | ilk-turk-devletleri.md#3 0.569 | turkcenin-tarihi-ve-alfabeleri.md#3 0.562 | bugunku-turk-dunyasi.md#6 0.529`

**ilkturk-2** — Mete Han orduyu hangi sisteme göre düzenlemiştir?
> Mete Han orduyu onluk sisteme göre düzenlemiştir. Bu düzen, sonraki Türk devletlerinde ve başka ordularda da örnek alınmıştır. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#0 0.619 | ozan-asik-gelenegi.md#8 0.524 | osmanli-devlet-teskilati.md#8 0.477 | osmanli-devlet-teskilati.md#4 0.468 | osmanli-islahat-ve-mesrutiyet.md#9 0.450`

**ilkturk-3** — Göktürk Devleti ne zaman ve kimin önderliğinde kurulmuştur?
> Göktürk Devleti 552 yılında Bumin Kağan önderliğinde kurulmuştur. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#1 0.758 | ilk-turk-devletleri.md#4 0.659 | turk-milliyetciliginin-dogusu.md#4 0.585 | turk-devlet-gelenegi.md#0 0.580 | turklerin-islamiyeti-kabulu.md#3 0.576`

**ilkturk-4** — Orhun Yazıtları kimler adına dikilmiştir?
> Orhun Yazıtları, vezir Tonyukuk, Kül Tigin ve Bilge Kağan adına dikilmiştir. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#2 0.756 | turkcenin-tarihi-ve-alfabeleri.md#0 0.613`

**ilkturk-5** — Uygur Kağanlığı hangi yıl kurulmuştur?
> Uygur Kağanlığı 744'te kurulmuştur. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `ilk-turk-devletleri.md#4 0.660 | turklerin-islamiyeti-kabulu.md#3 0.576 | turk-islam-dunyasinda-bilim.md#5 0.567 | turkcenin-tarihi-ve-alfabeleri.md#1 0.558 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.541`

**ataturk-1** — Mustafa Kemal'in annesinin adı nedir?
> Mustafa Kemal Atatürk'nün annesinin adı Zübeyde Hanım'dır. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#0 0.673 | mustafa-kemal-ataturk.md#6 0.580`

**ataturk-2** — Mustafa Kemal'e Kemal adını kim vermiştir?
> Mustafa Kemal'e Kemal adını matematik öğretmeni Mustafa Efendi vermiştir. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#1 0.693 | mustafa-kemal-ataturk.md#0 0.688`

**ataturk-3** — Nutuk ne zaman okunmuş ve yaklaşık kaç saat sürmüştür?
> Mustafa Kemal Atatürk'ün Nutuk konuşmasını 15-20 Ekim 1927 tarihleri arasında okumuştur; bu konuşma yaklaşık otuz altı saat süren, Cumhuriyet'in temel kaynağı olan temel bir kaynaktır. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `mustafa-kemal-ataturk.md#5 0.479 | ilk-turk-islam-eserleri.md#1 0.437 | ilk-turk-islam-eserleri.md#2 0.415 | milli-semboller.md#10 0.412 | nevruz-ve-turk-bayramlari.md#7 0.400`

**ataturk-4** — "Yurtta sulh, cihanda sulh" sözü hangi yıl söylenmiştir?
> "Yurtta sulh, cihanda sulh" sözü 1931'de söylenmiştir. (Kaynak: mustafa-kemal-ataturk.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#7 0.401 | milli-semboller.md#10 0.399 | turklerin-islamiyeti-kabulu.md#1 0.398 | mustafa-kemal-ataturk.md#5 0.398 | nevruz-ve-turk-bayramlari.md#5 0.398`

**ataturk-5** — Atatürk'ün naaşı Anıtkabir'e ne zaman nakledilmiştir?
> Atatürk'ün naaşı Anıtkabir'e 10 Kasım 1953'te nakledilmiştir. (Kaynak: milli-semboller.md)

Getirilen: `milli-semboller.md#7 0.745 | mustafa-kemal-ataturk.md#6 0.590 | milli-semboller.md#8 0.563 | mustafa-kemal-ataturk.md#4 0.529`

**osmanli-1** — Yavuz Sultan Selim hangi savaşlarla Mısır'ı Osmanlı topraklarına katmıştır?
> Yavuz Sultan Selim, Mısır'ı Osmanlı topraklarına katmak için Çaldıran Savaşı'nda Safevîler'e, Mercidabık Savaşı'nda ve Ridaniye Savaşı'nda Memlükler'e yenilgiye uğrattıktan sonra Mısır'ı Osmanlı topraklarına katmıştır. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#3 0.663 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#8 0.563 | osmanli-islahat-ve-mesrutiyet.md#0 0.562 | osmanli-islahat-ve-mesrutiyet.md#5 0.545 | selcuklu-ve-osmanli-mimarisi.md#5 0.543`

**osmanli-2** — fatih kimdir
> Fatih Sultan Mehmed, 29 Mayıs 1453'te İstanbul'u fethettiğinde yirmi bir yaşındaydı. Fetihle birlikte Doğu Roma İmparatorluğu sona ermiş, Osmanlı Devleti imparatorluğa dönüşmüştür. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#2 0.566 | turk-islam-dunyasinda-bilim.md#2 0.474 | mustafa-kemal-ataturk.md#6 0.465 | mustafa-kemal-ataturk.md#0 0.463 | milli-semboller.md#4 0.461`

**osmanli-3** — Osman Gazi kimdir
> Osman Gazi, Osmanlı Devleti'nin kurucusudur. Devletin kuruluşu geleneksel olarak 1299 yılında tarihlenmektedir. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#0 0.676 | osmanli-padisahlari.md#1 0.659 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.586 | ozan-asik-gelenegi.md#0 0.584 | osmanli-devlet-teskilati.md#0 0.555`

**osmanli-4** — Orhan Gazi kimdir
> Orhan Gazi, Osmanlı Padişahlarının kuruluş döneminin belirleyici hükümdarıdır. Bursa'yı alarak Rumeli'ye geçişin yapıp Osmanlı Devleti'nin temelini attığı için önemli bir rol oynamıştır. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#1 0.574 | ozan-asik-gelenegi.md#0 0.530 | ozan-asik-gelenegi.md#1 0.485 | osmanli-padisahlari.md#0 0.465 | turkcenin-tarihi-ve-alfabeleri.md#0 0.456`

**osmanli-5** — Yıldırım Bayezid Ankara Savaşı'nda kime yenilmiştir?
> Yıldırım Bayezid Ankara Savaşı'nda Timur'a yenilmiştir. (Kaynak: anadolu-beylikleri-ve-osmanlinin-kurulusu.md)

Getirilen: `anadolu-beylikleri-ve-osmanlinin-kurulusu.md#9 0.678 | osmanli-padisahlari.md#1 0.640 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#1 0.605 | canakkale-ve-kurtulus-savasi.md#2 0.556 | turk-denizciligi.md#0 0.544`

**osmanli-6** — Kanuni Sultan Süleyman kaç yıl hüküm sürmüştür?
> Kanuni Sultan Süleyman 1520-1566 yılları arasında kırk altı yıl hüküm sürmüştür. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#4 0.705 | osmanli-islahat-ve-mesrutiyet.md#0 0.593 | osmanli-padisahlari.md#0 0.570 | selcuklu-ve-osmanli-mimarisi.md#5 0.519 | selcuklular-ve-malazgirt.md#3 0.513`

**selcuklu-1** — Anadolu Selçuklu Devleti hangi savaşta Moğollara yenilmiştir?
> Anadolu Selçuklu Devleti 1243'teki Kösedağ Savaşı'nda Moğollara yenilmiştir. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#4 0.748 | selcuklular-ve-malazgirt.md#3 0.675 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#0 0.660 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#1 0.597 | turklerin-islamiyeti-kabulu.md#6 0.587`

**selcuklu-2** — Malazgirt Savaşı ne zaman yapılmıştır?
> Malazgirt Savaşı 26 Ağustos 1071'de yapılmıştır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.663 | selcuklular-ve-malazgirt.md#2 0.660 | turklerin-islamiyeti-kabulu.md#1 0.486`

**selcuklu-3** — Büyük Selçuklu Devleti'nin kuruluşunu kesinleştiren savaş hangisidir?
> Büyük Selçuklu Devleti'nin kuruluşunu kesinleştiren savaş 1040 yılındaki Dandanakan Savaşı'dır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#0 0.756 | selcuklular-ve-malazgirt.md#3 0.647 | turklerin-islamiyeti-kabulu.md#6 0.631 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#8 0.591 | osmanli-islahat-ve-mesrutiyet.md#0 0.585`

**selcuklu-4** — Anadolu Selçuklu Devleti'ni kim kurmuştur?
> Selçuklular ve Malazgirt Savaşı bölümündeki metne göre, Anadolu Selçuklu Devleti'ni Süleyman Şah kurmuştur. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#3 0.779 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#0 0.755 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#1 0.725 | selcuklular-ve-malazgirt.md#0 0.691`

**selcuklu-5** — Miryokefalon Savaşı'nın sonucu ne olmuştur?
> Miryokefalon Savaşı'nda Bizans'ın Anadolu'yu geri alma girişimi başarısız olmuştur ve Anadolu'nun Türk yurdu olduğu durumunun kesinleşmesiyle sonuçlanmıştır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#3 0.484 | canakkale-ve-kurtulus-savasi.md#3 0.467 | selcuklular-ve-malazgirt.md#4 0.457 | osmanli-islahat-ve-mesrutiyet.md#3 0.443 | turklerin-islamiyeti-kabulu.md#6 0.442`

**destan-1** — Manas Destanı hangi topluma aittir?
> Manas Destanı Kırgızlara aittir. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#3 0.748 | ozan-asik-gelenegi.md#2 0.635 | turk-destanlari.md#1 0.527`

**destan-2** — Dede Korkut Kitabı kaç hikâyeden oluşur?
> Dede Korkut Kitabı, on iki hikâyeden oluşur. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.776 | ozan-asik-gelenegi.md#1 0.612 | turk-kulturunde-at.md#4 0.575`

**destan-3** — Oğuz Kağan Destanı'na göre Oğuz Kağan'ın kaç oğlu vardır?
> Oğuz Kağan Destanı'na göre Oğuz Kağan'ın altı oğlu vardır ve bu oğullardan yirmi dört Oğuz boyunun türediği anlatılır. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#1 0.838 | turk-destanlari.md#0 0.552`

**destan-4** — Ergenekon'dan çıkış günü nasıl kutlanmıştır?
> Ergenekon Destanı'nda çıkış günü, bazı Türk topluluklarında bahar bayramı olarak kutlanmıştır. Vadiden çıkış gününde demir bir dağı eriterek dışarı çıkan topluluk, bu gün için özel bir kutlama yapar. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#2 0.628 | turk-kulturunde-kurt.md#2 0.446 | nevruz-ve-turk-bayramlari.md#1 0.440`

**destan-5** — Dede Korkut kültürü UNESCO listesine hangi yıl alınmıştır?
> Dede Korkut kültürü 2018'de UNESCO İnsanlığın Somut Olmayan Kültürel Mirası listesine alınmıştır. (Kaynak: turk-destanlari.md)

Getirilen: `turk-destanlari.md#4 0.706 | bugunku-turk-dunyasi.md#7 0.663 | ozan-asik-gelenegi.md#1 0.553`

**gelenek-1** — Kut nedir?
> Kut, Türk anlatı geleneğinde ve eski Türk devletlerinde hüküm süren bir hanedanın erkek üyelerinin tümü tarafından paylaşılan yönetme yetkisidir. Bu yetkinin Tanrı tarafından verildiğine inanılırdı ve devletin sürekliliğini sağlayırken taht kavgalarına da yol açmıştır. Ayrıca, "Kutadgu Bilig" adlı eserde "mutluluk veren bilgi" veya "devlet olma bilgisi" anlamına gelen bir terim de kullanılmıştır. (Kaynak: turk-kulturunde-kurt.md, turk-devlet-gelenegi.md, ilk-turk-islam-eserleri.md)

Getirilen: `turk-kulturunde-kurt.md#6 0.559 | turk-kulturunde-kurt.md#0 0.519 | turk-devlet-gelenegi.md#0 0.485 | ilk-turk-islam-eserleri.md#1 0.430`

**gelenek-2** — Töre nedir?
> Töre, yazılı olmayan hukuk düzenidir. Hükümdar bile töreye uymak zorundaydı ve töre, değiştirilmesi için kurultayın onayını gerektirirdi. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#1 0.642 | turk-devlet-gelenegi.md#4 0.414`

**gelenek-3** — Kurultayda hangi konular görüşülürdü?
> Kurultayda savaş, barış ve hükümdar seçimi gibi konular görüşülürdü. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#2 0.663 | turk-kulturunde-kurt.md#2 0.589 | turk-kulturunde-kurt.md#4 0.555`

**gelenek-4** — İkili teşkilat nedir?
> İkili teşkilat, ülkenin doğu ve batı olmak üzere iki idari kanada ayrılmasıdır. Doğu kanadı daha üstün sayılır ve büyük kağan orada bulunurdu; batı kanadını genellikle hanedandan bir başka üye yönetirdi. Bu düzen, geniş bozkır coğrafyasının tek merkezden yönetilmesinin zorluğuna verilmiş pratik bir cevaptır. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#3 0.455 | turk-kulturunde-at.md#2 0.406 | oguz-boylari-ve-turk-boy-yapisi.md#0 0.404 | oguz-boylari-ve-turk-boy-yapisi.md#2 0.397 | osmanli-devlet-teskilati.md#4 0.396`

**gelenek-5** — Tuğ nedir?
> Tuğ, at kılından yapılan ve sırık üzerinde taşınan bayrak niteliğindeki semboldür; sayısı hükümdarın rütbesine göre değişebilir. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#4 0.552 | oguz-boylari-ve-turk-boy-yapisi.md#0 0.491 | oguz-boylari-ve-turk-boy-yapisi.md#2 0.484 | turk-destanlari.md#1 0.477 | turk-devlet-gelenegi.md#0 0.465`

**at-1** — Turan taktiği nasıl uygulanır?
> Turan taktiği, merkez birlikler sahte bir geri çekilme yaparak uygulanır. Bu strateji, düşmanın takibe geçmesini sağlar. Düşman takibe başladığında, kanatlar hilal biçiminde kapanarak düşmana kuşatma oluştururlar. Bu yöntem, Türk ordularının askeri stratejilerinde önemli bir yer tutar ve Malazgirt Savaşı'nda da başarılı bir şekilde uygulanmıştır. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#1 0.656 | turk-devlet-gelenegi.md#1 0.501 | osmanli-devlet-teskilati.md#3 0.497 | osmanli-devlet-teskilati.md#4 0.496 | turk-mitolojisi-ve-gok-tanri.md#2 0.490`

**at-2** — Kımız nedir?
> Kımız, Türkçede at kırsaklarının mayalanmasıyla elde edilen içecektir. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-mitolojisi-ve-gok-tanri.md#5 0.351 | turk-kulturunde-at.md#3 0.346 | turk-kulturunde-kurt.md#6 0.330 | bozkir-gocebe-yasami.md#2 0.305 | nevruz-ve-turk-bayramlari.md#7 0.303`

**at-3** — Üzengi atlı savaşa ne kazandırmıştır?
> Üzengi atlı savaşa şu avantajları kazandırmıştır:  - Binicinin at üstünde dengeli durabilmesi - İki elini birden kullanabilmesi - Mızrak darbesine vücut ağırlığını verebilmesi  Bu buluş, atlı savaşın daha etkili bir şekilde yürütülmesine olanak sağlaymıştır. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#2 0.740 | turk-kulturunde-at.md#1 0.629 | turklerin-islamiyeti-kabulu.md#1 0.524 | osmanli-islahat-ve-mesrutiyet.md#0 0.522`

**at-4** — Hangi at ırkları dayanıklılıklarıyla bilinir?
> Ahal Teke ve Türkmen atı dayanıklılıklarıyla bilinir. Bu atlar bozkır kökenli ırklar dayanıklılıkları ve uzun mesafe performanslarıyla bilinir. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#4 0.582 | turk-kulturunde-at.md#0 0.531 | turk-mitolojisi-ve-gok-tanri.md#4 0.453 | oguz-boylari-ve-turk-boy-yapisi.md#2 0.438 | turk-mitolojisi-ve-gok-tanri.md#6 0.432`

**kurt-1** — Eski Türkçede kurdun adı neydi?
> Eski Türkçede kurdun adı "böri" idi. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.725 | turk-kulturunde-kurt.md#6 0.612`

**kurt-2** — böri nedir
> Eski Türkçede kurdun adı "böri" idi. Bu sözcük Orhun Yazıtları'nda ve on birinci yüzyılda Kaşgarlı Mahmud'un yazdığı Dîvânu Lugâti't-Türk'te geçer. Bugün de Kazakçada börı, Kırgızcada börü, Özbekçede bo'ri olarak kullanılmaktadır. Türkiye Türkçesinde ise sözcük yalnızca "bozkurt" ve destan kahramanı "Börteçine" gibi kalıplarda korunmuştur. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.563 | bozkir-gocebe-yasami.md#0 0.484 | bozkir-gocebe-yasami.md#2 0.467 | turk-kulturunde-kurt.md#6 0.456 | turk-kulturunde-at.md#0 0.442`

**kurt-3** — Aşina hanedanının soyu nereden gelir?
> Aşina hanedanının soyu bir dişi kurttan gelir. Göktürklerin türeyiş anlatısına göre, hanedanın adı Aşina'dır ve soyun dişi bir kurttan olduğu aktarılır. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#1 0.520 | oguz-boylari-ve-turk-boy-yapisi.md#4 0.433 | ozan-asik-gelenegi.md#3 0.371`

**kurt-4** — Eski Türkçede kurt kelimesinin anlamı neydi?
> Eski Türkçede kurt kelimesinin anlamı böriydü. Bu terim, solucan, kurtçuk veya böcek larvasının adını ifade ediyordu. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#6 0.830 | turk-kulturunde-kurt.md#5 0.724`

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
> Ziya Gökalp'in eseridir. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `ilk-turk-islam-eserleri.md#0 0.649 | ilk-turk-islam-eserleri.md#3 0.613 | turk-milliyetciliginin-dogusu.md#2 0.579 | turk-destanlari.md#0 0.557`

**dogus-3** — İsmail Gaspıralı hangi ilkeyi savunmuştur?
> İsmail Gaspıralı, "Dilde, fikirde, işte birlik" ilkesini savunmuştur. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#3 0.773 | osmanli-islahat-ve-mesrutiyet.md#7 0.525`

**dogus-4** — Türk Ocağı ne zaman kurulmuştur?
> Türk Ocağı 25 Mart 1912'de kurulmuştur. (Kaynak: turk-milliyetciliginin-dogusu.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.750 | bugunku-turk-dunyasi.md#5 0.615 | ilk-turk-devletleri.md#1 0.603 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.592 | bugunku-turk-dunyasi.md#4 0.581`

**alfabe-1** — Göktürk alfabesi kaç işaretten oluşur?
> Göktürk alfabesi otuz sekiz işaretten oluşur. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.719 | turkcenin-tarihi-ve-alfabeleri.md#3 0.648 | bugunku-turk-dunyasi.md#6 0.617 | ilk-turk-devletleri.md#4 0.534 | turk-kulturunde-kurt.md#1 0.524`

**alfabe-2** — Harf Devrimi hangi tarihte kabul edilmiştir?
> Harf Devrimi 1 Kasım 1928'de kabul edilmiştir. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#3 0.712 | turkcenin-tarihi-ve-alfabeleri.md#4 0.555 | bugunku-turk-dunyasi.md#6 0.550 | cumhuriyet-inkilaplari.md#5 0.550 | ilk-turk-devletleri.md#3 0.530`

**alfabe-3** — Türk Dil Kurumu ne zaman kurulmuştur?
> Türk Dil Kurumu, 12 Temmuz 1932'de kurulan Türk Dili Tetkik Cemiyeti olarak başlamış ve bugüne kadar faaliyet göstermektedir. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turk-milliyetciliginin-dogusu.md#4 0.760 | turkcenin-tarihi-ve-alfabeleri.md#4 0.760 | bugunku-turk-dunyasi.md#4 0.671 | bugunku-turk-dunyasi.md#5 0.645 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#4 0.637`

**alfabe-4** — Uygur alfabesi hangi yazıdan uyarlanmıştır?
> Uygur alfabesi Soğd yazısından uyarlanmıştır. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#1 0.816 | turkcenin-tarihi-ve-alfabeleri.md#0 0.663 | bugunku-turk-dunyasi.md#6 0.627`

**alfabe-5** — Kutadgu Bilig hangi yüzyılda yazılmıştır?
> Kutadgu Bilig, 11. yüzyılda yazılmıştır. Yazarı Yusuf Has Hâcib tarafından 1069-1070 yıllarında tamamlanmış ve Karahanlı hükümdarı Tabgaç Buğra Han'a sunulmuştur. (Kaynak: ilk-turk-islam-eserleri.md)

Getirilen: `ilk-turk-islam-eserleri.md#1 0.788 | ilk-turk-islam-eserleri.md#2 0.700`

**cevapsiz-1** — Fatih Sultan Mehmed'in annesinin adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-padisahlari.md#2 0.652 | osmanli-devlet-teskilati.md#9 0.511 | osmanli-padisahlari.md#4 0.508 | mustafa-kemal-ataturk.md#0 0.500 | milli-semboller.md#4 0.476`

**cevapsiz-2** — Malazgirt Savaşı'nda Selçuklu ordusu kaç askerden oluşuyordu?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `selcuklular-ve-malazgirt.md#0 0.691 | selcuklular-ve-malazgirt.md#1 0.675 | oguz-boylari-ve-turk-boy-yapisi.md#7 0.504 | selcuklu-ve-osmanli-mimarisi.md#1 0.503 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#1 0.501`

**cevapsiz-3** — Kanuni Sultan Süleyman'ın eşinin adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `osmanli-padisahlari.md#4 0.575 | osmanli-devlet-teskilati.md#9 0.532 | osmanli-islahat-ve-mesrutiyet.md#0 0.521 | selcuklu-ve-osmanli-mimarisi.md#5 0.519 | osmanli-padisahlari.md#2 0.497`

**cevapsiz-4** — Lozan Antlaşması'nı Türk heyeti adına kim imzalamıştır?
> Lozan Antlaşması'nı Türk heyeti adına İsmet İnönü imzalamıştır. (Kaynak: canakkale-ve-kurtulus-savasi.md)

Getirilen: `osmanli-islahat-ve-mesrutiyet.md#7 0.533 | osmanli-islahat-ve-mesrutiyet.md#3 0.531 | bugunku-turk-dunyasi.md#4 0.526 | canakkale-ve-kurtulus-savasi.md#4 0.521 | ilk-turk-islam-eserleri.md#7 0.472`

**cevapsiz-5** — Orhun Yazıtları bugün hangi müzede sergilenmektedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `ilk-turk-devletleri.md#2 0.659 | turkcenin-tarihi-ve-alfabeleri.md#0 0.568 | bugunku-turk-dunyasi.md#7 0.474 | turk-devlet-gelenegi.md#1 0.463`

**cevapsiz-6** — Mete Han'ın babasının adı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `ilk-turk-devletleri.md#0 0.516 | ozan-asik-gelenegi.md#8 0.438 | milli-semboller.md#3 0.409 | mustafa-kemal-ataturk.md#0 0.393 | turklerin-islamiyeti-kabulu.md#2 0.383`

**cevapsiz-7** — Bugün hava nasıl olacak?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `bugunku-turk-dunyasi.md#0 0.381 | bozkir-gocebe-yasami.md#1 0.323 | turk-kulturunde-kurt.md#6 0.317 | bugunku-turk-dunyasi.md#6 0.297 | turk-kulturunde-at.md#3 0.297`

**cevapsiz-8** — Python'da bir liste nasıl sıralanır?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.367 | bugunku-turk-dunyasi.md#6 0.338 | turk-denizciligi.md#6 0.320 | ozan-asik-gelenegi.md#4 0.307 | turk-mitolojisi-ve-gok-tanri.md#6 0.307`

**cevapsiz-9** — Futbolda ofsayt kuralı nedir?
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `oguz-boylari-ve-turk-boy-yapisi.md#1 0.368 | oguz-boylari-ve-turk-boy-yapisi.md#2 0.353 | bozkir-gocebe-yasami.md#1 0.330 | milli-semboller.md#5 0.326 | turk-kulturunde-kurt.md#6 0.321`

**cevapsiz-10** — asdf qwerty zxcv
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `bugunku-turk-dunyasi.md#6 0.372 | turkcenin-tarihi-ve-alfabeleri.md#0 0.369 | turkcenin-tarihi-ve-alfabeleri.md#1 0.326 | ilk-turk-devletleri.md#3 0.326 | turk-kulturunde-kurt.md#6 0.313`

**takip-1#1** — Malazgirt Savaşı ne zaman yapılmıştır?
> Malazgirt Savaşı 26 Ağustos 1071'de yapılmıştır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.663 | selcuklular-ve-malazgirt.md#2 0.660 | turklerin-islamiyeti-kabulu.md#1 0.486`

**takip-1#2** — sonucu ne oldu?  
_Önceki soru: Malazgirt Savaşı ne zaman yapılmıştır?_
> Bölgedeki Karluk Türklerinin Abbasîlerin yanında yer alması sonucunda Abbasî ordusu zafer elde etmiş ve Talas Savaşı'nda Çin'in Tang hanedanı orduları yenilmiştir. (Kaynak: turklerin-islamiyeti-kabulu.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.681 | selcuklular-ve-malazgirt.md#2 0.668 | turklerin-islamiyeti-kabulu.md#6 0.483 | turklerin-islamiyeti-kabulu.md#1 0.482`

**takip-2#1** — Orhun Yazıtları'nın alfabesini kim çözmüştür?
> Yazıtaların dili uzun süre çözülememişti. Danimarkalı dilbilimci Vilhelm Thomsen 1893'te alfabeyi çözmüş ve metinler böylece okunabilir hale gelmiştir. (Kaynak: ilk-turk-devletleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.742 | ilk-turk-devletleri.md#2 0.663 | turkcenin-tarihi-ve-alfabeleri.md#1 0.580 | ilk-turk-devletleri.md#3 0.567 | bugunku-turk-dunyasi.md#6 0.543`

**takip-2#2** — hangi yılda?  
_Önceki soru: Orhun Yazıtları'nın alfabesini kim çözmüştür?_
> 1 Kasım 1928'de kabul edilen Harf Devrimi ile Latin alfabesine dayalı yeni Türk alfabesine geçilmiştir. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#0 0.734 | ilk-turk-devletleri.md#2 0.673 | turkcenin-tarihi-ve-alfabeleri.md#3 0.586 | ilk-turk-devletleri.md#3 0.570 | bugunku-turk-dunyasi.md#6 0.547`

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
> Eski Türkçede kurdun adı "böri" idi. Bu sözcük Orhun Yazıtları'nda ve on birinci yüzyılda Kaşgarlı Mahmud'un yazdığı Dîvânu Lugâti't-Türk'te geçer. Bugün de Kazakçada börı, Kırgızcada börü, Özbekçede bo'ri olarak kullanılmaktadır. Türkiye Türkçesinde ise sözcük yalnızca "bozkurt" ve destan kahramanı "Börteçine" gibi kalıplarda korunmuştur. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.563 | bozkir-gocebe-yasami.md#0 0.484 | bozkir-gocebe-yasami.md#2 0.467 | turk-kulturunde-kurt.md#6 0.456 | turk-kulturunde-at.md#0 0.442`

**degisim-1#2** — fatih kimdir  
_Önceki soru: böri nedir_
> Fatih Sultan Mehmed, 29 Mayıs 1453'te İstanbul'u fethettiğinde yirmi bir yaşındaydı. Fetihle birlikte Doğu Roma İmparatorluğu sona ermiş, Osmanlı Devleti imparatorluğa dönüşmüştür. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#2 0.566 | turk-islam-dunyasinda-bilim.md#2 0.474 | mustafa-kemal-ataturk.md#6 0.465 | mustafa-kemal-ataturk.md#0 0.463 | milli-semboller.md#4 0.461`

**degisim-2#1** — Orhan Gazi kimdir
> Orhan Gazi, Osmanlı Padişahlarının kuruluş döneminin belirleyici hükümdarıdır. Bursa'yı alarak Rumeli'ye geçişin yapıp Osmanlı Devleti'nin temelini attığı için önemli bir rol oynamıştır. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#1 0.574 | ozan-asik-gelenegi.md#0 0.530 | ozan-asik-gelenegi.md#1 0.485 | osmanli-padisahlari.md#0 0.465 | turkcenin-tarihi-ve-alfabeleri.md#0 0.456`

**degisim-2#2** — böri nedir  
_Önceki soru: Orhan Gazi kimdir_
> Eski Türkçede kurdun adı "böri" idi. Bu sözcük Orhun Yazıtları'nda ve on birinci yüzyılda Kaşgarlı Mahmud'un yazdığı Dîvânu Lugâti't-Türk'te geçer. Bugün de Kazakçada börı, Kırgızcada börü, Özbekçede bo'ri olarak kullanılmaktadır. Türkiye Türkçesinde ise sözcük yalnızca "bozkurt" ve destan kahramanı "Börteçine" gibi kalıplarda korunmuştur. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.563 | bozkir-gocebe-yasami.md#0 0.484 | bozkir-gocebe-yasami.md#2 0.467 | turk-kulturunde-kurt.md#6 0.456 | turk-kulturunde-at.md#0 0.442`

**degisim-3#1** — Turan taktiği nasıl uygulanır?
> Turan taktiği, merkez birlikler sahte bir geri çekilme yaparak uygulanır. Bu strateji, düşmanın takibe geçmesini sağlar. Düşman takibe başladığında, kanatlar hilal biçiminde kapanarak düşmana kuşatma oluştururlar. Bu yöntem, Türk ordularının askeri stratejilerinde önemli bir yer tutar ve Malazgirt Savaşı'nda da başarılı bir şekilde uygulanmıştır. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#1 0.656 | turk-devlet-gelenegi.md#1 0.501 | osmanli-devlet-teskilati.md#3 0.497 | osmanli-devlet-teskilati.md#4 0.496 | turk-mitolojisi-ve-gok-tanri.md#2 0.490`

**degisim-3#2** — Kımız nedir?  
_Önceki soru: Turan taktiği nasıl uygulanır?_
> Kımız, Türk kültüründe atların önemli bir yer aldığını gösterir. Atlı okçuluk ve Turan taktiği gibi askeri tekniklerde atın kritik rolü vurgulanmaktadır. Ayrıca, mitolojide ve törenda atın sembolik önemi de gözlemlenir. At, Türk kültüründe ölümlere ve törenlere de dahil olmak üzere çeşitli ritüellere de katılmıştır. (Kaynak: turk-kulturunde-at.md)

Getirilen: `turk-kulturunde-at.md#1 0.657 | turk-devlet-gelenegi.md#1 0.524 | osmanli-devlet-teskilati.md#4 0.512 | turk-mitolojisi-ve-gok-tanri.md#2 0.511 | osmanli-devlet-teskilati.md#3 0.509`

**degisim-4#1** — Harf Devrimi hangi tarihte kabul edilmiştir?
> Harf Devrimi 1 Kasım 1928'de kabul edilmiştir. (Kaynak: turkcenin-tarihi-ve-alfabeleri.md)

Getirilen: `turkcenin-tarihi-ve-alfabeleri.md#3 0.712 | turkcenin-tarihi-ve-alfabeleri.md#4 0.555 | bugunku-turk-dunyasi.md#6 0.550 | cumhuriyet-inkilaplari.md#5 0.550 | ilk-turk-devletleri.md#3 0.530`

**degisim-4#2** — Tuğ nedir?  
_Önceki soru: Harf Devrimi hangi tarihte kabul edilmiştir?_
> Tuğ, at kılından yapılan ve sırık üzerinde taşınan bayrak niteliğindeki semboldür; sayısı hükümdarın rütbesine göre değişebilir. (Kaynak: turk-devlet-gelenegi.md)

Getirilen: `turk-devlet-gelenegi.md#4 0.552 | oguz-boylari-ve-turk-boy-yapisi.md#0 0.491 | oguz-boylari-ve-turk-boy-yapisi.md#2 0.484 | turk-destanlari.md#1 0.477 | turk-devlet-gelenegi.md#0 0.465`

**disi-1#1** — Osman Gazi kimdir
> Osman Gazi, Osmanlı Devleti'nin kurucusudur. Devletin kuruluşu geleneksel olarak 1299 yılında tarihlenmektedir. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#0 0.676 | osmanli-padisahlari.md#1 0.659 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.586 | ozan-asik-gelenegi.md#0 0.584 | osmanli-devlet-teskilati.md#0 0.555`

**disi-1#2** — Bugün hava nasıl olacak?  
_Önceki soru: Osman Gazi kimdir_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `bugunku-turk-dunyasi.md#0 0.381 | bozkir-gocebe-yasami.md#1 0.323 | turk-kulturunde-kurt.md#6 0.317 | bugunku-turk-dunyasi.md#6 0.297 | turk-kulturunde-at.md#3 0.297`

**disi-2#1** — Eski Türkçede kurdun adı neydi?
> Eski Türkçede kurdun adı "böri" idi. (Kaynak: turk-kulturunde-kurt.md)

Getirilen: `turk-kulturunde-kurt.md#5 0.725 | turk-kulturunde-kurt.md#6 0.612`

**disi-2#2** — asdf qwerty zxcv  
_Önceki soru: Eski Türkçede kurdun adı neydi?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `turk-kulturunde-kurt.md#5 0.719 | turk-kulturunde-kurt.md#6 0.615`

**disi-3#1** — Osman Gazi kimdir
> Osman Gazi, Osmanlı Devleti'nin kurucusudur. Devletin kuruluşu geleneksel olarak 1299 yılında tarihlenmektedir. (Kaynak: osmanli-padisahlari.md)

Getirilen: `osmanli-padisahlari.md#0 0.676 | osmanli-padisahlari.md#1 0.659 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.586 | ozan-asik-gelenegi.md#0 0.584 | osmanli-devlet-teskilati.md#0 0.555`

**disi-3#2** — Python listesi nasıl sıralanır?  
_Önceki soru: Osman Gazi kimdir_
> Python listesi sıralanırken genellikle aşağıdaki adımlar izlenir:  - Liste oluşturmak için [] kullanılır. - Liste elemanlarına index numaralarıyla erişilir. - Elemanları sırayla eklemek için .append() metodu kullanılır. - Listeyi istediğimiz şekilde sıralayabiliriz.  Örnek:  ```python liste = [] liste.append("elma") liste.append("armut") liste.append("portakal") print(liste) ```  (Cay: osmanli-padisahlari.md) (Kaynak: oguz-boylari-ve-turk-boy-yapisi.md)

Getirilen: `osmanli-padisahlari.md#0 0.599 | osmanli-padisahlari.md#1 0.581 | ozan-asik-gelenegi.md#0 0.550 | oguz-boylari-ve-turk-boy-yapisi.md#3 0.549 | anadolu-beylikleri-ve-osmanlinin-kurulusu.md#5 0.528`

**disi-4#1** — Malazgirt Savaşı ne zaman yapılmıştır?
> Malazgirt Savaşı 26 Ağustos 1071'de yapılmıştır. (Kaynak: selcuklular-ve-malazgirt.md)

Getirilen: `selcuklular-ve-malazgirt.md#1 0.663 | selcuklular-ve-malazgirt.md#2 0.660 | turklerin-islamiyeti-kabulu.md#1 0.486`

**disi-4#2** — Futbolda ofsayt kuralı nedir?  
_Önceki soru: Malazgirt Savaşı ne zaman yapılmıştır?_
> Bu bilgi elimdeki dokümanlarda yok.

Getirilen: `oguz-boylari-ve-turk-boy-yapisi.md#1 0.368 | oguz-boylari-ve-turk-boy-yapisi.md#2 0.353 | bozkir-gocebe-yasami.md#1 0.330 | milli-semboller.md#5 0.326 | turk-kulturunde-kurt.md#6 0.321`

