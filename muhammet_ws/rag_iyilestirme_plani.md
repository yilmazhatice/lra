# RAG İyileştirme Planı: Ölçümler, Çıkarımlar ve Uygulama Fazları

**Tarih:** 14 Eylül 2026 (aynı gün doğrulama testleriyle güncellendi, Bölüm 2.6; Faz 0 tamamlandı, Bölüm 2.7; Faz 1 tamamlandı, Bölüm 2.8; Faz 2 tamamlandı, Bölüm 2.9; Faz 3 tamamlandı, Bölüm 2.10; Faz 5 tamamlandı ve Faz 4 prototiplendi, Bölüm 2.11; Faz 4 uygulandı, varsayılan kapalı, Bölüm 2.12)
**Kapsam:** Yerel RAG asistanının (lra) yanıt süresi, "dokümanda yok" hataları ve arama kalitesi.
**İlgili dokümanlar:** [proje_uygunluk_raporu.md](proje_uygunluk_raporu.md), [yavaslik_sorunu_ve_cozumu.md](yavaslik_sorunu_ve_cozumu.md)

## Kısaca

- **Yavaşlığın sebebi bulundu ve çözüldü (Bölüm 2.5).** Sebep model değil, ekran kartı belleğinin **hangi sırayla** dolduğuydu. Sohbet modeli belleği gömme modelinden sonra alınca cevaplar ~50 sn, önce alınca ~2.3 sn sürüyor. Düzeltmeden sonra aynı qwen2.5-7b modeliyle ortalama cevap süresi **48 sn'den 2.3 sn'ye** indi.
- **Yanlış "dokümanda yok" cevaplarının asıl sebebi arama katmanı.** Model bu hataların kaynağı değil. Başlıca sebep sabit eşik değeri (`MIN_SCORE = 0.42`), ikincisi paragrafları birbirine karıştıran parçalama.
- **Belgeler iyi yazılmış.** Sorun onları parçalayan kodda.
- **Hız artık model seçiminde bir etken değil.** Temiz bellekte qwen2.5-7b ortalama 1.6 sn, qwen3-4b 1.7 sn. qwen3-4b 14 cevabın 5'inde yanlış ya da uydurma bilgi verdi ve neredeyse hiç kaynak yazmadı. qwen2.5-7b'de hatalı cevap sayısı 2.
- **Mevcut durum (Bölüm 2.6):**
  - 12 soruluk değerlendirme seti otomatik kontrolde 12/12 geçiyor, cevaplar gözle kontrol edilince 10/12. Ortalama süre 2.0 sn.
  - Streamlit arayüzünde art arda sorular çalışıyor.
- **Doğrulama testlerinde bulunan yeni sorunlar:**
  - Model bazen **yanlış belgeyi kaynak** gösteriyor.
  - Takip sorularında önceki soru aramaya ekleniyor ama **modele iletilmiyor**, bu da yanlış cevaba yol açabiliyor.
  - Konu dışı bir soru, bir önceki soruyla birleşince **eşik korumasını aşıyor**.
- **Faz 0 tamamlandı (Bölüm 2.7).** 105 soruluk değerlendirme setiyle başlangıç ölçümü alındı:
  - Tam başarı %67.8. Arama hit@1 %68.9, hit@3 %87.8. Ortalama süre 1.8 sn.
  - **En büyük kayıp yanlış red.** Cevabı belgede olan soruların %20.3'ü reddediliyor, çoğu eşikte. Kısa "X nedir?" sorularında 10 sorudan sadece 3'ü başarılı.
  - Eski 12 soruluk set bu ölçümde 10/12. Önceki "12/12" sonucu, puanlamanın cevabın doğruluğuna ve kaynağa bakmamasından geliyordu.
- **Faz 1 tamamlandı (Bölüm 2.8).** Parçalar paragraf düzeyine indirildi ve başına başlık yolu eklendi.
  - Tam başarı %67.8 → **%76.7**, hit@1 %68.9 → **%81.1**, doğru kaynak %91.5 → %98.4.
  - Cevaplanamaz soruların tamamı reddedildi. Kısa kavram sorularında başarı 3/10'dan 7/10'a çıktı.
  - **Eşikte reddedilen 8 sorunun hepsinde doğru parça artık 1. ya da 2. sırada.** Bu sorularda kalan tek engel eşik.
  - Bir soruda paragraf, önceki paragraftaki bağlamı kaybettiği için arama kötüleşti ("Orhun alfabesini kim çözdü?", doğru parça 2. sıradan 5. sıraya).
- **Faz 2 tamamlandı (Bölüm 2.9).** Sorgulara Türkçe görev talimatı eklendi.
  - Tam başarı %76.7 → **%85.6**, hit@1 %81.1 → %85.1, yanlış red %16.2 → **%5.4**. Cevaplanamaz soruların hepsi hâlâ reddediliyor. Süre değişmedi (1.8 sn).
  - **Planda yazan İngilizce talimat aramayı kötüleştirdi** (hit@1 %81.1 → %74.3). Türkçe talimat seçildi.
  - Kazancın büyük kısmı, skorların eşiğin üstüne çıkmasından geliyor: 11 kazanımın 7'si böyle.
  - Talimat skorları yükselttiği için kısa takip soruları da tek başına eşiği geçmeye başladı. Önceki soruyu kullanan kural bu yüzden daha az devreye giriyor. Takip sorusu sorunu (H10) büyüdü.
- **Faz 3 tamamlandı (Bölüm 2.10).**
  - **Takip sorusu kuralı değişti.** Birleşik arama artık skoru tek başına aramadan en az 0.20 yüksekse kullanılıyor.
  - **Eşik 0.42'den 0.33'e indi.** Eşik artık yalnızca açıkça konu dışı soruları ayıklayan bir güvenlik tabanı. Konuya yakın ama belgede olmayan soruları model reddediyor, çünkü skorları cevaplanabilir soruların çoğundan yüksek ve hiçbir eşik değeri bu iki grubu ayıramıyor.
  - **Sonuçlar:** Tam başarı %85.6 → **%87.8**, yanlış red %5.4 → **%2.7**, cevaplanamaz soruları reddetme %100.
- **Toplam ilerleme (başlangıç → Faz 3):** Tam başarı %67.8 → %87.8, hit@1 %68.9 → %87.8, yanlış red %20.3 → %2.7. Süre 1.8 sn'den 2.0 sn'ye çıktı.
- **Kalan 11 hatanın 7'si kaynak satırıyla ilgili** (yanlış belge ya da red cevabına kaynak eklenmesi), 1'i takip sorusunun modele eksik gitmesiyle. İkisi de Faz 5'in konusu.
- **Faz 5 tamamlandı (Bölüm 2.11).** 6 değişiklik ayrı ayrı ölçüldü, 2'si tutuldu.
  - **Tutulan:** Kaynak satırını kod belirliyor (H5). Sistem komutu Faz 3'teki haliyle korunuyor, model kaynak satırı yazmaya devam ediyor ama kod bu satırı silip kendi bulduğu kaynağı ekliyor.
  - **Reddedilen:**
    - Takip sorusunda önceki soruyu modele göstermek (H9): uydurma getirdi.
    - `TOP_K = 5`: başarı düştü, süre 7 sn'ye çıktı.
    - Kaynak kuralını sistem komutundan çıkarmak: 3 soru kaybettirdi.
    - qwen3-4b: aynı 62 soruda 52'ye karşı 60 başarı, üstelik Foundry'yi çökertti.
  - **Sonuç:** Tam başarı %87.8 → **%95.6**. Eski 12 soruluk set **12/12**. Kaynak satırı hataları 7'den 0'a indi. Cevaplanamaz soruları reddetme %100. Gözle kontrolde yanlış bilgi içeren cevap oranı %4.1. Ortalama süre 1.95 sn.
- **Toplam ilerleme (başlangıç → Faz 5):** Tam başarı %67.8 → %95.6, hit@1 %68.9 → %87.8, yanlış red %20.3 → %2.7, doğru kaynak %91.5 → %98.6.
- **Faz 4 uygulandı ama varsayılan olarak kapalı (Bölüm 2.12).**
  - **Hibrit arama ölçütleri belirgin iyileştirdi:** Tam başarı %95.6 → %96.7, hit@1 %87.8 → %91.9, hit@3 %100, yanlış red %0. Eşik ve takip kararları hiç değişmedi.
  - **Ama gözle kontrolde yanlış bilgi içeren cevap 3'ten 5'e çıktı.** Cevaplanamaz bir takip sorusuna uydurma cevap geldi ve Faz 4'ün "hiçbir kategoride başarı düşmesin" ölçütü karşılanmadı.
  - Veri karar için yetersiz: bu kategoride yalnızca 2 soru var. Hibrit aramanın açılıp açılmayacağına Faz 5.5'teki kontrol seti karar verecek. Karar kuralları ölçümden önce yazıldı (Bölüm 6).
- **Faz 5.5 tamamlandı (Bölüm 2.13).** 43 yeni soruluk kontrol seti, sonuçları görülmeden yazıldı. Kararlar önceden yazılan kurallarla verildi.
  - **Tam başarı %88.4.** Ana setten 7 puan düşük, 10 puanlık sınırın içinde ✅.
  - **Cevaplanamaz soruları reddetme %87.5.** %90 sınırının altında ❌. 16 sorudan 2'sine uydurma geldi, biri bilerek konan tuzak.
  - **Hibrit arama kapalı kalıyor.** Kör incelemede uydurmayı 2'den 4'e çıkardı.
  - **Gözle kontrolde cevaplanabilir sorularda yanlış bilgi %11** (ana sette %4.1). Bir cevapta Çince metin var.
- **Durum:** Arama, kaynak gösterme ve hız hedefte. **Uydurmama vaadi, sonuçları görülmemiş sorularda henüz yeterince güvenilir değil.**
- **Faz 5.6 tamamlandı (Bölüm 2.14).**
  - **Türkçe olmayan yazı koruması eklendi.**
  - **Cevap doğrulama adımı iki talimatla denendi.** Uydurmaları sıfırladı ama 10–11 doğru cevabı da reddetti. qwen2.5-7b kendi cevabını güvenilir doğrulayamıyor, bu yüzden kapalı.
- **Durum:** Bu model ve donanımla, başka bir şeyi bozmadan yapılabilecek iyileştirmeler denendi. Kalan zayıflık konuya yakın tuzak sorulardaki uydurma: kontrol setinde 16'da 2.
- **Önerilen yol:** Proje sahibinin bağımsız testi ([bagimsiz_test_rehberi.md](bagimsiz_test_rehberi.md)) → sonuca göre model/donanım kararı ve Faz 6 (belgeleme).

---

## 1. Ortam

| Bileşen | Değer |
|---|---|
| Donanım | Windows 11, RTX 5070 Laptop GPU (8 GB), NPU yok |
| Çalıştırma ortamı | Foundry Local, CUDA varyantları |
| Sohbet modeli | `qwen2.5-7b-instruct-cuda-gpu` (4.7 GB) |
| Gömme modeli | `qwen3-embedding-0.6b-cuda-gpu` (478 MB, 1024 boyutlu vektör) |
| Veri | 13 belge, 86 paragraf, ~30.000 karakter (~7.500 token). Parça sayısı: Faz 0'da 53, Faz 1'den sonra 86 |
| Ayarlar | `TOP_K = 3`, `MAX_TOKENS = 350`, `temperature = 0`. `MIN_SCORE`: Faz 0–2'de 0.42, Faz 3'ten sonra 0.33. Faz 2'den sonra Türkçe sorgu talimatı, Faz 3'ten sonra takip sorusu farkı `FOLLOW_UP_MARGIN = 0.20`. Parçalama: Faz 0'da `CHUNK_SIZE = 900` + `OVERLAP = 200`, Faz 1'den sonra paragraf başına bir parça + başlık yolu, `CHUNK_SIZE = 1000` (paragraf üst sınırı) |

> **Not:** Bölüm 2.1–2.6'daki ölçümler 13–14 soruluk küçük örneklerle yapıldı. Yönü gösterirler ama kesin sonuç değildirler. Sonraki kararlar için Bölüm 2.7'deki 105 soruluk başlangıç ölçümü esas alınmalı.

---

## 2. Yapılan deneyler ve sonuçları

### 2.1 Yanıt süresinin nereye gittiği

Tek bir soru ("Orhan Gazi kimdir", ~1000 token bağlam) adım adım ölçüldü:

| Adım | Süre |
|---|---|
| Soruyu vektöre çevirme ve arama | 0.03 sn |
| Modelin bağlamı okuması (ilk token'a kadar) | 33.8 sn |
| Cevabın üretilmesi | 20 sn (4 token/sn) |

**Çıkarımlar:**
- Model "düşünmüyor", bağlamı okuyor. qwen2.5 düşünme modu olan bir model değil.
- Aynı belgeden art arda soru sormak süreyi kısaltmıyor, çünkü her soruda bağlam baştan okunuyor. Önbellek yok.
- Bu donanımda 7B bir modelin 40 token/sn civarında üretmesi beklenir. 4 token/sn anormal.
- **Sonradan netleşen nokta:** Bu ölçümdeki yavaşlık modelin kendisinden değil, belleğin yükleme sırasından kaynaklanıyordu (Bölüm 2.5). Temiz bellekte aynı soruda bağlam okuma ~0.5 sn, üretim ~60 token/sn.

### 2.2 Ard arda sorularda "dokümanda yok" hatası (düzeltildi)

**Belirti:** Streamlit ve masaüstü arayüzünde ilk soru doğru cevaplanıyor, ikinci soru belgede olsa bile "yok" deniyor. Terminalde sorun görülmüyordu, çünkü her komut yeni bir işlem başlatıyor ve geçmiş tutulmuyor.

**Sebep:** [app.py](../app.py) ve [masaustu.py](../masaustu.py), 8 kelimeden kısa her soruya aramadan önce önceki soruyu ekliyordu. Konu değişince arama eski konuda kalıyordu.

| Oturumdaki soru | Eski davranış | Yeni davranış |
|---|---|---|
| böri nedir | kurt belgesi 0.477 | kurt belgesi 0.477 |
| fatih kimdir | kurt belgesi 0.404, **eşik altı → "yok"** | Osmanlı belgesi 0.455 ✅ |
| Orhan Gazi kimdir → böri nedir | **Osmanlı belgesi** 0.525 | kurt belgesi 0.477 ✅ |

**Düzeltme:** [rag.py](../rag.py) içine `retrieve()` fonksiyonu eklendi. Soru önce tek başına aranıyor. Önceki soru yalnızca soru tek başına eşiği geçemezse ("bunun sebebi ne?" gibi) kullanılıyor. Modelle uçtan uca test edildi, iki soru da doğru cevaplandı. Streamlit arayüzünün kendisiyle yapılan test için Bölüm 2.6'ya bakın.

> **Açık kalan iki sorun** (doğrulama testinde bulundu, ayrıntı Bölüm 2.6):
> 1. Takip sorusunda arama önceki soruyla yapılıyor ama modele sadece yeni soru gidiyor.
> 2. Konu dışı bir soru önceki soruyla birleşince eşiği aşıp modele ulaşabiliyor.

### 2.3 Model karşılaştırması: qwen2.5-7b ve qwen3-4b

İki model aynı 14 soruyu, birebir aynı bağlam ve aynı sistem komutuyla cevapladı. qwen3-4b'nin düşünme modu `/no_think` ile kapatıldı.

**Hız** (temiz bellek, her model sunucuda tek başına, [karsilastir.py](olcum_betikleri/karsilastir.py) sürüm 2):

| | qwen2.5-7b | qwen3-4b |
|---|---|---|
| Ortalama cevap süresi | 1.6 sn | 1.7 sn |
| İlk token'a kadar | 0.5–0.9 sn | 0.3–0.4 sn |
| Üretim hızı | 51–62 token/sn | 59–72 token/sn |
| Ortalama cevap uzunluğu | 61 parça | 93 parça |
| Ekran kartı belleği (Foundry, sadece sohbet modeli) | 5.3 GB | 3.5 GB |

qwen3-4b token başına daha hızlı, ama daha uzun cevap yazdığı için toplam süre aynı.

> **İlk ölçüm neden farklıydı?** İlk karşılaştırmada qwen2.5-7b bozuk bellek düzeninde çalışıyordu (Bölüm 2.5). Ortalama 55.3 sn ve 3.7 token/sn ölçülmüştü. Sonuçlar [karsilastirma_sonuc_2026-09-14.json](olcum_betikleri/karsilastirma_sonuc_2026-09-14.json) dosyasında duruyor, ama hız karşılaştırması için geçersiz.

**Doğruluk** (cevaplar belgelerle tek tek karşılaştırıldı):

| Soru | qwen2.5-7b | qwen3-4b |
|---|---|---|
| fatih kimdir | ✅ (dil hatalı) | ❌ "Osmanlı'nın kurucusu ve ilk hanedanı" |
| böri nedir | ⚠️ "böcek larvasının anısına" diye uydurma ekliyor | ✅ |
| Osman Gazi kimdir | ✅ | ❌ "Bursa'da kurulmuş" (belgede yok) |
| Orhan Gazi kimdir | ✅ | ⚠️ "1323" yılı uydurma |
| Turan taktiği nasıl uygulanır? | ✅ | ❌ Taktiği anlatmıyor |
| Yavuz, Mısır'ı hangi savaşlarla aldı? | ⚠️ Yalnızca Ridaniye | ✅ Üç savaş, ama cümlede İngilizce "fought after" |
| Ülkü Ocakları 1971 sonrası adı | ✅ | ❌ 1978'deki adı veriyor |
| Fatih'in annesi (belgede yok) | ✅ Reddetti | ✅ Reddetti |
| Diğer 6 soru | ✅ | ✅ |

| Özet | qwen2.5-7b | qwen3-4b |
|---|---|---|
| Hatalı veya uydurma cevap | 2 / 14 | 5 / 14 |
| "(Kaynak: ...)" satırı (cevaplanabilir 13 soruda) | 13 / 13, ama 1'i yanlış belge (Orhun sorusu) | 1 / 13 |

**Düşünme modu açıkken qwen3-4b:** Cevap süresi ~5 sn (temiz bellekte). "fatih kimdir" sorusunda doğru bağlam verildiği halde "bağlamda yok" dedi.

**Tekrarlanabilirlik:** İki ölçümde (bozuk ve temiz bellek) her iki model de 14 sorunun 14'ünde birebir aynı cevabı verdi. Doğruluk tablosu bellek durumundan etkilenmiyor.

**Çıkarımlar:**
- İki model de hız hedefini (plan: ~1–3 sn) karşılıyor. **Model seçimi doğruluğa göre yapılmalı.** Bu testte qwen2.5-7b daha iyi.
- Ülkü Ocakları sorusunda qwen3-4b'ye doğru paragraf verildi. Paragrafta iki ad geçiyordu ve model yanlış olanı seçti. **Bu tür hatayı arama iyileştirmeleri düzeltemez.** Model kalitesi de önemli.
- Kaynak satırı, modelin yazmasına güvenilmeyecek kadar önemli bir bilgi. qwen2.5-7b bile Thomsen bilgisini `ilk-turk-devletleri.md` belgesinden (2. sıradaki parça) aldığı halde kaynak olarak 1. sıradaki `turkcenin-tarihi-ve-alfabeleri.md` belgesini yazdı.

### 2.4 Arama ve parçalama analizi

Veritabanına yazmadan, farklı parçalama ve sorgu biçimleri aynı sorularla denendi. Tabloda doğru paragrafın **kaçıncı sırada** çıktığı ve **benzerlik skoru** var.

- **Mevcut:** 900 karakterlik birleşik parçalar.
- **Talimat:** Sorgunun başına Qwen3-Embedding'in önerdiği yönerge eklendi: `Instruct: Given a question, retrieve passages that answer the question\nQuery: `.
- **Paragraf:** Her paragraf ayrı parça yapıldı ve başına belge başlığı eklendi.

| Soru | Mevcut | Talimat | Paragraf | Paragraf + talimat |
|---|---|---|---|---|
| böri nedir | 1. / 0.48 | 1. / 0.46 | 1. / 0.51 | 1. / 0.48 |
| fatih kimdir | 1. / 0.45 | 1. / 0.46 | 1. / 0.50 | 2. / 0.50 |
| Orhan Gazi kimdir | 1. / 0.53 | 1. / 0.52 | 1. / 0.59 | 1. / 0.59 |
| Eski Türkçede kurt kelimesinin anlamı | 1. / 0.69 | 1. / 0.74 | 1. / 0.75 | 1. / 0.83 |
| Azerbaycan Türkçesinde kurda ne denir? | 1. / 0.64 | 1. / 0.62 | 2. / 0.66 | 1. / 0.68 |
| **Aşina hanedanının soyu nereden gelir?** | **1. / 0.36 → "yok"** | 1. / 0.48 | 1. / 0.41 | 1. / 0.53 |
| Ülkü Ocakları 1978'de hangi adı aldı? | 2. / 0.63 | 1. / 0.56 | 1. / 0.69 | 2. / 0.60 |
| Ülkü Ocakları bugün hangi adla faaliyette? | 1. / 0.59 | 2. / 0.53 | 1. / 0.65 | 2. / 0.60 |
| Yıldırım Bayezid Ankara'da kime yenildi? | 1. / 0.57 | 1. / 0.61 | 1. / 0.58 | 1. / 0.66 |
| **Kımız nedir?** | **17. / 0.22 → "yok"** | 1. / 0.41 | 1. / 0.34 | 1. / 0.49 |
| Manas Destanı kaç dizedir? | 1. / 0.68 | 1. / 0.69 | 1. / 0.74 | 1. / 0.75 |
| Türk Dil Kurumu ne zaman kuruldu? | 2. / 0.58 | 1. / 0.74 | 2. / 0.63 | 1. / 0.78 |
| **Dokuz Işık ilkeleri nelerdir?** | **7. / 0.26 → "yok"** | 1. / 0.41 | 1. / 0.44 | 1. / 0.55 |

Analiz bellek düzeltmesinden sonra tekrar çalıştırıldı ve tablo birebir aynı çıktı ([parca_analiz.py](olcum_betikleri/parca_analiz.py)).

**Parçaların mevcut durumu:**
- 53 parça, uzunluk 416–966 karakter (ortalama 711).
- İlk parça dışındaki 40 parçanın **39'u kelimenin ortasından başlıyor**. Örnek: `'inin ardından 23 Ağustos - 13 Eylül 1921...'`. Sebep, örtüşmenin karakter sayısıyla kesilmesi ([ingest.py:29](../ingest.py#L29)).
- Belge başlığı yalnızca ilk parçada var.
- Birleşik parçalar farklı alt konuları karıştırıyor. "At" belgesinde savaş taktiği ile kımız aynı parçada, bu yüzden "Kımız nedir?" sorusunda doğru parça 17. sıraya düşüyor.

**Konuların birbirine yakınlığı:** Belgelerin hepsi Türk tarihi ve milliyetçilik üzerine. Bu yüzden alakasız parçalar da yüksek skor alıyor:

```
"fatih kimdir" → osmanli-padisahlari 0.455 | mustafa-kemal-ataturk 0.442 | milliyetci-hareket 0.439
```

**Çıkarımlar:**
- Arama çoğu soruda doğru parçayı zaten 1. sıraya koyuyor. Kayıp **eşikte** ve **karışık parçalarda** yaşanıyor.
- "Dokuz Işık ilkeleri nelerdir?" arayüzdeki örnek butonlardan biri. Cevap belgede var ama sistem şu an her tıklamada "yok" diyor.
- Sabit bir benzerlik eşiği, konuları bu kadar yakın bir belge setinde kırılgan. Doğru ve yanlış parçalar arasında bazen 0.01 fark var.
- Paragraf + başlık parçalama ile sorgu talimatı, zayıf soruları 1. sıraya ve eşiğin üstüne çıkardı. Ama tek başına talimat iki soruda sırayı 1'den 2'ye düşürdü. **Her değişiklik geniş bir test setiyle ölçülmeli.**
- Cevap kalitesi belgenin içeriğiyle sınırlı. Örneğin belgede Orhan Gazi hakkında tek bir cümle var. "Orhan Gazi kimdir" sorusuna hiçbir ayar daha zengin bir cevap üretemez.

### 2.5 Yavaşlığın asıl sebebi: bellek yükleme sırası (çözüldü)

**İlk ipucu:** Model ağırlıkları 4.84 GB ve her token'da tamamı okunuyor. Ağırlıklar ekran kartı belleğindeyse ~50–60 token/sn beklenir. Sistem RAM'inden PCIe üzerinden okunuyorsa ~3–4 token/sn beklenir. Ölçülen değer 3.7'ydi.

**Gözlenen mekanizma:** 8 GB dolunca NVIDIA sürücüsü hata vermiyor, yeni bellek ayırmalarını sessizce sistem RAM'ine yönlendiriyor. Hangi bellek RAM'e düşerse o adım yavaşlıyor:
- **Model ağırlıkları düşerse** üretim yavaşlıyor.
- **Bağlamı okurken gereken çalışma belleği düşerse** ilk token gecikiyor.

Uygulama her soruda önce arama yapıyor. Bu yüzden önce gömme modeli yükleniyor ve çalışıyor, sohbet modeli belleğin geri kalanıyla idare etmek zorunda kalıyordu.

**Senaryo ölçümleri** ([hiz_teshis.py](olcum_betikleri/hiz_teshis.py)):

| Senaryo | İlk token (RAG istemi) | Üretim hızı |
|---|---|---|
| Uzun süredir açık sunucu, iki model | 16.75 sn | 49 tok/sn |
| Gömme modeli bellekten çıkarıldı | 5.5 sn | 62 tok/sn |
| Temiz sunucu, yalnızca sohbet modeli | 1.02 sn | 43 tok/sn |
| Temiz sunucu, önce sohbet sonra gömme | 1.03 sn | 43 tok/sn |
| Modeller boşaltılıp yeniden yüklendi (sunucu açık) | 1.71 sn | **21.5 tok/sn** |
| Aynı durumda sunucu yeniden başlatıldı | 0.84 sn | 43.9 tok/sn |

**Uygulama akışıyla doğrulama** ([hiz_teshis2.py](olcum_betikleri/hiz_teshis2.py), `rag.answer()`, art arda 5 soru):

| Sıra | Soru süreleri | Ortalama |
|---|---|---|
| Uygulamanın eski sırası (önce gömme) | 18 → 51 → 41 → 57 → 73 sn | 48.1 sn |
| Önce sohbet modeli + ısıtma, sonra gömme | 2.6 → 2.2 → 1.8 → 2.6 → 3.3 sn | 2.5 sn |

Aynı model, aynı sorular ve birebir aynı cevaplar. Sadece yükleme sırası farklı.

**Ölçümle elenen olasılıklar:**
- **Pil modu:** Bilgisayar prizdeydi.
- **32K bağlam için büyük önbellek ayrılması:** qwen3-4b'nin bağlamı 40K olduğu halde hızlı çalıştı.
- **Modelin kendisi:** Temiz bellekte aynı model 43 tok/sn üretti.

**Düzeltme** ([foundry_client.py](../foundry_client.py) `set_primary()`, [rag.py](../rag.py) `warmup_messages()`):
1. Sohbet modeli "birincil model" olarak tanımlanıyor. Her sunucu oturumunda belleğe ilk o yükleniyor ve uygulamanın gönderebileceği en uzun istemle ısıtılıyor. Gömme modeli ilk aramada, ondan sonra yükleniyor.
2. Foundry sunucusu uygulamadan bağımsız açık kaldığı için modeller önceki bir çalıştırmadan bozuk düzende kalmış olabilir. Açılışta ısıtma isteminin ilk token süresi ve üretim hızı ölçülüyor. İlk token 3 sn'yi aşıyor ya da üretim 30 tok/sn'nin altında kalıyorsa sunucu yeniden başlatılıyor.
3. Modeli boşaltıp yeniden yüklemek yetmiyor (tabloda 21.5 tok/sn), bu yüzden sunucu yeniden başlatılıyor.
4. Sohbet modeli oturum ortasında bellekten atılırsa aynı işlem tekrarlanıyor.

**Doğrulama** ([hiz_dogrulama.py](olcum_betikleri/hiz_dogrulama.py), her senaryo ayrı işlem, art arda 5 soru):

| Senaryo | İlk soru | Sonraki 4 sorunun ortalaması |
|---|---|---|
| Temiz sunucu | 15.6 sn (model yükleme dahil) | 2.3 sn |
| Sağlıklı sunucuya ikinci bağlantı | 4.5 sn (yeniden başlatma yok) | 2.3 sn |
| Bozuk bellek | 22.2 sn (fark edildi, sunucu yeniden başlatıldı) | 2.0 sn |
| Oturum ortasında sohbet modeli atıldı | Kendini toparladı: 21.7 sn, sonra 4.4 sn | — |
| Terminal: `python rag.py "..."` | — | 4.2 sn (her komutta ~2 sn ısıtma kontrolü dahil) |

**Bilinen sınırlar:**
- **Kontrol yalnızca açılışta ve model atıldığında yapılıyor.** Uygulama çalışırken başka bir program (tarayıcı, oyun, video) ekran kartı belleğini doldurursa yavaşlama geri gelebilir.
- **Sunucu yeniden başlatıldığında bellekteki tüm modeller boşalıyor.** Foundry'yi aynı anda kullanan başka bir uygulama varsa etkilenir.
- **Terminal kullanımında her komut ~2 sn uzuyor**, çünkü her komut yeni bir işlem ve ısıtma kontrolü her seferinde yapılıyor.
- **Eşikler bu makinede ölçüldü** (ilk token 3 sn, üretim 30 tok/sn). Model ya da donanım değişirse yeniden ölçülmeli.

### 2.6 Doğrulama testleri: mevcut durum ve yeni bulgular

Düzeltmelerden sonra dokümandaki iddiaları kontrol etmek için yapıldı ([plan_dogrulama.py](olcum_betikleri/plan_dogrulama.py), ham sonuçlar: [plan_dogrulama_sonuc.json](olcum_betikleri/plan_dogrulama_sonuc.json)).

#### Değerlendirme seti (evaluate.py, 12 soru)

`eval_results.md` dosyasının üzerine yazmamak için aynı sorular ayrı bir betikle çalıştırıldı.

| Ölçüt | Sonuç |
|---|---|
| Başarılı | 12 / 12 |
| Ortalama süre (tüm sorular) | 2.0 sn |
| Ortalama süre (modele giden sorular) | 2.3 sn |
| Kaynak satırı (cevaplanabilir 9 soru) | 9 / 9 |
| Cevaplanamaz 3 soru | 3 / 3 reddedildi. 2'si eşikte (0.2 sn), "Fatih'in annesi" eşiği geçti (0.494) ve modelde reddedildi |

**Uyarı: "12/12" gerçek başarıyı olduğundan iyi gösteriyor.** `evaluate.py` sadece doğru belgenin ilk 3 sonuçta olmasına ve modelin reddetmemesine bakıyor. Bu yüzden şu iki cevap da "başarılı" sayıldı:
- **Yavuz sorusu:** Üç savaştan yalnızca biri yazılmış, cevap eksik.
- **Orhun sorusu:** Kaynak olarak yanlış belge gösterilmiş.

Gerçek başarı gözle kontrol edildiğinde 10/12.

#### Streamlit arayüzünde art arda sorular

Gerçek `app.py`, Streamlit'in test aracıyla (AppTest) çalıştırıldı ve aynı oturumda art arda 4 soru soruldu:

| Soru | Süre | Sonuç |
|---|---|---|
| böri nedir | 2.2 sn | ✅ Doğru, kaynaklı |
| fatih kimdir | 2.5 sn | ✅ Doğru (düzeltme öncesi "yok" diyordu) |
| Osman Gazi kimdir | 1.7 sn | ✅ Doğru, kaynaklı |
| Dokuz Işık ilkeleri nelerdir? | 1.9 sn | ❌ "yok" (bilinen eşik sorunu, Bölüm 2.4) |

Masaüstü arayüzü ([masaustu.py](../masaustu.py)) aynı `rag.answer()` çağrısını kullanıyor ama grafik arayüz olduğu için otomatik test edilmedi.

#### Takip soruları ve konu dışı sorular

Arayüzün gönderdiği biçimde test edildi: önceki soru + yeni soru.

| Önceki soru → yeni soru | Arama | Cevap | Değerlendirme |
|---|---|---|---|
| Malazgirt Savaşı ne zaman yapıldı? → sonucu ne oldu? | Tek başına 0.35, birleşik 0.59 | "Selçuklular zafer kazandı, Bizans İmparatoru esir düştü" | ✅ Doğru |
| Sakarya kaç gün sürdü? → bunun sebebi ne? | Birleşik 0.53 | "Bu bilgi elimdeki dokümanlarda yok." | ✅ Doğru (belgede sebep yok) |
| Orhun alfabesini kim çözdü? → hangi yılda? | Birleşik 0.67 | "1 Kasım 1928'de Harf Devrimi ile Latin alfabesine geçildi" | ❌ **Yanlış.** Doğru cevap 1893 |
| Osman Gazi kimdir → Bugün hava nasıl olacak? | Tek başına 0.23, birleşik **0.43, eşiği geçti** | Model reddetti | ⚠️ Eşik atlandı, model kurtardı |
| Kurdun adı neydi? → asdf qwerty zxcv | Birleşik **0.60, eşiği geçti** | Reddetti ama **sonuna kaynak satırı ekledi** | ⚠️ Eşik atlandı, biçim hatası |
| Osman Gazi kimdir → Python listesi nasıl sıralanır? | Birleşik **0.49, eşiği geçti** | Model reddetti | ⚠️ Eşik atlandı, model kurtardı |

**Bulgular:**
1. **Takip sorusunda modele bağlam eksik gidiyor.** `retrieve()` önceki soruyu sadece aramada kullanıyor. Model sadece "hangi yılda?" sorusunu görüyor, neyin yılı sorulduğunu bilmiyor ve bağlamdaki başka bir tarihi seçiyor. Bu, arama doğru olduğu halde yanlış cevap üreten bir tasarım hatası.
2. **Konu dışı sorular eşik korumasını aşıyor.** Soru tek başına eşiğin altında kalınca birleşik metinle aranıyor. Birleşik metnin skoru büyük ölçüde önceki sorudan geliyor. Testteki 3 konu dışı sorunun 3'ü de bu yolla eşiği geçti. Bu sorun [proje_uygunluk_raporu.md](proje_uygunluk_raporu.md) içinde de 2. madde olarak geçiyordu. `retrieve()` onu küçülttü (artık yalnızca tek başına eşiği geçemeyen sorular etkileniyor) ama tamamen gidermedi. Testte model 3 soruyu da reddetti, yani son savunma hattı şu an model.
3. **Reddetme cevabına kaynak satırı ekleniyor.** Uygunluk raporundaki gözlem tekrarlandı.
4. **Takip sorusu ile konu dışı soru skorla ayırt edilemiyor.** Aşağıdaki aralıklar örtüşüyor. Bu yüzden 2. bulgu tek bir eşik değeriyle çözülemez (bkz. H10).

| | Tek başına skor | Birleşik skor |
|---|---|---|
| Gerçek takip soruları (3) | 0.27 – 0.35 | 0.53 – 0.67 |
| Konu dışı / anlamsız sorular (3) | 0.23 – 0.32 | 0.43 – 0.60 |

### 2.7 Başlangıç ölçümü (Faz 0)

**Rapor:** [2026-09-14_0351_baslangic.md](../degerlendirmeler/2026-09-14_0351_baslangic.md). Tekrar ölçümü ve karşılaştırma: [2026-09-14_0358_tekrar.md](../degerlendirmeler/2026-09-14_0358_tekrar.md).

#### Ölçüm altyapısı

| Parça | Ne yapıyor |
|---|---|
| [eval_set.py](../eval_set.py) | 75 tekil soru (13 belgenin hepsinden 65 cevaplanabilir, 10 cevaplanamaz) ve 15 senaryo (takip sorusu, cevapsız takip, konu değişimi, konu dışı soru önceki sorudan sonra). Toplam 105 soru. |
| Kanıt ifadesi | Beklenen paragraf parça numarasıyla değil, paragraftan kısa bir ifadeyle tanımlanıyor. Faz 1'de parçalama değişince set geçersiz olmuyor. |
| Anahtar / yasak ifade | Cevapta geçmesi gereken ifadeler ve bilinen yanlışlar (örneğin "hangi yılda?" sorusunda "1928"). |
| [evaluate.py](../evaluate.py) | Seti çalıştırıp `degerlendirmeler/` klasörüne tarihli `.md` ve `.json` yazar. `eval_results.md` dosyasına dokunmaz. |
| `--kontrol` | Modelsiz set doğrulaması: her kanıt ifadesi belgede ve tek bir parçanın içinde mi, id'ler tekil mi. |
| `--karsilastir` | İki çalıştırmanın ölçütlerini yan yana koyar ve sonucu değişen soruları listeler. Soru seti değiştiyse uyarır. |
| `--rapor` | Modeli çalıştırmadan, bir JSON sonucundan raporu yeniden üretir. |

Değerlendirmenin arayüzlerle **aynı kod yolunu** ölçmesi için [rag.py](../rag.py) içinde iki değişiklik yapıldı:
- **`answer_details()`:** Cevapla birlikte ölçüm bilgisini de döndürüyor (arama süresi, ilk token süresi, eşikte red olup olmadığı). `answer()` bunu çağırıyor, imzası değişmedi. Model artık akışla (stream) çağrılıyor. Eski 12 sorunun 12'sinde cevap metni birebir aynı çıktı.
- **`follow_up_query()`:** Takip sorusu kuralı [app.py](../app.py) ve [masaustu.py](../masaustu.py) içinde ayrı ayrı yazılıydı. Tek yere taşındı, iki arayüz ve değerlendirme aynı kuralı kullanıyor. Davranış değişmedi.

#### Başlangıç sonuçları

| Ölçüt | Değer |
|---|---|
| Tam başarı (90 puanlanan soru) | %67.8 |
| Arama: doğru parça 1. sırada (hit@1) | %68.9 |
| Arama: doğru parça ilk 3'te (hit@3) | %87.8 |
| Arama: MRR | 0.796 |
| Cevaplanabilir sorularda başarı | %66.2 |
| **Yanlış red** (cevap belgede varken) | **%20.3** (15/74), bunun 13'ü eşikte |
| Anahtar ifadelerin tamamı cevapta | %91.5 |
| Bilinen yanlışı içeren cevap | 3 |
| Kaynak satırı var / doğru belge | %96.6 / %91.5 |
| Cevaplanamaz soruları reddetme | %93.8, **bunun yalnızca %37.5'i eşikte** |
| Red cevabına eklenmiş kaynak satırı | 4 |
| Süre ortalaması / medyan / en uzun | 1.8 / 1.9 / 3.6 sn |
| İlk token ortalaması | 1.0 sn |
| Arama süresi ortalaması | 0.29 sn |

| Kategori | Soru | Başarılı | hit@1 | hit@3 | Yanlış red |
|---|---|---|---|---|---|
| normal | 55 | 41 | 41 | 50 | 8 |
| **ozel_ad** ("Kut nedir?", "Kımız nedir?") | 10 | **3** | 5 | 7 | **6** |
| yakın (konuya yakın, belgede yok) | 6 | 3 | - | - | - |
| konu dışı / anlamsız | 4 | 4 | - | - | - |
| takip | 5 | 3 | 4 | 5 | 0 |
| takip (cevap belgede yok) | 2 | 2 | - | - | - |
| konu değişimi | 4 | 2 | 1 | 3 | 1 |
| konu dışı, önceki sorudan sonra | 4 | 3 | - | - | - |

#### Ölçümün güvenilirliği

- **Tekrarlanabilirlik:** Değerlendirme iki kez çalıştırıldı. Tüm ölçütler aynı çıktı, sonucu değişen soru yok. 105 cevabın 2'sinde metin birkaç kelime farklı. Bağlam aynı olduğu için bu fark ekran kartındaki küçük hesaplama farklarından geliyor. **Sonuç:** Sonraki fazlarda tek bir sorunun sonucunun değişmesi gürültü olabilir. Karar verirken birden fazla sorudaki değişime bakılmalı.
- **Puanlamanın doğruluğu:** Cevapların hepsi gözle kontrol edildi.
  - Otomatik "HATA" kararlarının hepsi gerçek hata.
  - 1 soruda otomatik karar fazla cömert: `osmanli-4` cevabında "Osman Gazi'nin oğlu" yazıyor. Bu doğru bir bilgi ama belgede yok, yani model kendi bilgisini eklemiş.
  - Birkaç cevapta küçük dil hataları var ("Viyanan şehir", "kısrak sta"), ama bilgiler doğru.
- **Setin tarafsızlığı:** Beklentiler ölçümden önce, belgelere bakılarak yazıldı. Sonuçlar görüldükten sonra hiçbir beklenti gevşetilmedi.

#### Bulgular

1. **Yanlış redlerin yarısı arama hatası değil, eşik hatası.** Eşikte reddedilen 13 sorunun 7'sinde doğru parça zaten ilk 3'teydi (örnekler: "Töre nedir?" 1. sıra, "İkili teşkilat nedir?" 1. sıra, "Aşina hanedanının soyu" 1. sıra). Kalan 6'sında doğru parça ilk 3'e girmiyor ("Kımız nedir?" 17. sıra, "Ergenekon'dan çıkış günü" 11. sıra). İki tür kayıp ayrı fazlarda çözülecek: parça sırası Faz 1–2'de, eşik Faz 3'te.
2. **Kısa kavram soruları en zayıf kategori.** "X nedir?" biçimindeki 10 sorudan 3'ü başarılı. Kısa sorunun vektörü, uzun ve karışık parçalarla düşük benzerlik veriyor. Faz 1 (paragraf parçalama) ve Faz 2 (sorgu talimatı) doğrudan bu kategoriyi hedefliyor.
3. **Cevaplanamaz soruları çoğunlukla model reddediyor, eşik değil.** 16 cevaplanamaz sorudan 15'i reddedildi, ama sadece 6'sı eşikte. "Konuya yakın" 6 sorunun 4'ü eşiği geçiyor. "Malazgirt'te Selçuklu ordusu kaç askerdi?" sorusunun skoru 0.645, yani cevaplanabilir soruların çoğundan yüksek. Bu da tek bir eşik değerinin iki grubu ayıramayacağını gösteriyor. Bir soru reddedilmedi: "Lozan'ı kim imzaladı?" sorusuna isim yerine tarih verildi. Eşik düşürülürse (Faz 3) bu yük modelde daha da artacak.
4. **Konu değişiminde takip kuralı zarar veriyor.** "Harf Devrimi..." sorusundan sonra "Tuğ nedir?" soruldu. Soru tek başına eşiğin altında kaldığı için önceki soruyla birleşik arandı ve doğru parça 2. sıradan 14. sıraya düştü. Bu, H10'daki konu dışı soru sorununun takip sorusu tarafındaki karşılığı.
5. **Mevcut parçalamada da bağlamsız parça sorunu var.** "Büyük Birlik Partisi'ni kim kurmuştur?" sorusunda doğru parça 3. sırada. Ama kurucunun adı bir önceki paragrafta geçiyor ve model cevaba isim yazamadı. H1'in riski olarak yazılan durum şu an da görülüyor.
   > **Faz 1 düzeltmesi:** Burada "başlık öneki bu soruyu çözmez" demiştim. Bu yanlıştı: belgede kişi adları `##` alt başlığı olarak geçiyor ve Faz 1'de parçaya alt başlık da eklendi. Ancak doğru parça bu sefer 4. sıraya düştü, dolayısıyla soru hâlâ çözülmedi (Bölüm 2.8).
6. **Kaynak hataları farklı türlerde.**
   - 3 soruda yanlış belge gösterildi.
   - 2 soruda kaynak satırı yok. Birinde satır parantezsiz yazılmış ("Kaynak: ...").
   - 4 red cevabına kaynak satırı eklendi.

   H5 (kaynağı kodun yazması) hepsini birlikte çözer.
7. **Eksik bağlam, modeli yanlış bir tarihe itiyor.** "Yurtta sulh, cihanda sulh" sorusuna 1931 yerine 1933 dedi.
   - Doğru parça 12. sıradaydı. Modele giden `mustafa-kemal-ataturk.md` parçasında 1933 (Onuncu Yıl Nutku) geçiyor, ama "Yurtta sulh" ve 1931 geçmiyor.
   - Sebep: aynı paragraftaki cümle parça sınırında kesilmiş. Model bağlamda bulduğu tek yılı yazdı.
   - Bu hem H1'in (parçalama) hem H8'in (bağlamda olmayanı yazmama) konusu.
8. **Bellek düzeltmesinin bir bedeli var: arama 30 ms'den 200 ms'ye çıktı.** Açılıştaki uzun ısıtma istemi ekran kartı belleğini kaplıyor, gömme modeli daha yavaş belleğe itiliyor ([gomme_hizi.py](olcum_betikleri/gomme_hizi.py)):
   - Gömme modeli tek başına: 28 ms
   - Sohbet modeli sonradan yüklenince: 26 ms
   - Uygulamanın sırasında: 197 ms

   Toplam 1.8 sn'lik cevap süresinde bu fark küçük. Ama takip sorularında arama iki kez yapıldığı için 0.5 sn'ye çıkıyor (H11).

### 2.8 Faz 1 sonuçları: paragraf parçalama

**Rapor:** [2026-09-14_0418_faz1-paragraf.md](../degerlendirmeler/2026-09-14_0418_faz1-paragraf.md). Başlangıç ölçümüyle karşılaştırmalı. Soru seti aynı (parmak izi `dcda3164d3`).

#### Değişiklik ([ingest.py](../ingest.py))

- **Her paragraf ayrı bir parça.** 86 paragraf → 86 parça. Karakter bazlı örtüşme kaldırıldı.
- **Parçanın başında başlık yolu var.** Örneğin: `Milliyetçi Hareketin Önemli İsimleri — Muhsin Yazıcıoğlu`. Alt başlıklar da ekleniyor.
- **Paragraf 1000 karakteri aşarsa cümle sınırından bölünüyor.** "II. Mehmed", "19. Tümen" gibi sıra sayılarında bölünmüyor. Şu anki belgelerde en uzun paragraf 765 karakter, yani bölme hiç çalışmadı.
- **Kontroller:**
  - Her parçanın gövdesi belgedeki paragrafla birebir aynı.
  - Kelime ortasından başlayan parça yok (önceden 40 parçanın 39'u).
  - `evaluate.py --kontrol` geçti: tüm kanıt ifadeleri yeni parçalara sığıyor.
- **Geri dönüş:** Önceki veritabanı `knowledge_faz0_yedek.db` olarak saklandı (git dışında).

#### Sonuçlar

| Ölçüt | Başlangıç | Faz 1 |
|---|---|---|
| Tam başarı | %67.8 | **%76.7** |
| hit@1 / hit@3 | %68.9 / %87.8 | **%81.1 / %93.2** |
| MRR | 0.796 | 0.881 |
| Cevaplanabilir sorularda başarı | %66.2 | %79.7 |
| Yanlış red (eşikte) | %20.3 (%17.6) | %16.2 (%10.8) |
| Anahtar ifadelerin tamamı | %91.5 | %95.2 |
| Bilinen yanlışı içeren cevap | 3 | 1 |
| Kaynak var / doğru belge | %96.6 / %91.5 | %100 / %98.4 |
| Cevaplanamaz soruları reddetme (eşikte) | %93.8 (%37.5) | **%100** (%31.2) |
| Red cevabına eklenmiş kaynak | 4 | **9** |
| Süre ortalaması / ilk token | 1.77 / 1.0 sn | 1.65 / 0.74 sn |

| Kategori | Başlangıç başarı | Faz 1 başarı |
|---|---|---|
| normal (55) | 41 | 45 |
| ozel_ad (10) | 3 | **7** |
| yakın (6) | 3 | 2 |
| takip (5) | 3 | 4 |
| takip, cevapsız (2) | 2 | 1 |
| konu değişimi (4) | 2 | 3 |
| konu dışı, önceki sorudan sonra (4) | 3 | 3 |
| Eski 12 soruluk set | 10/12 | 9/12 |

**Değişen sonuçlar:** 13 soru HATA → OK, 5 soru OK → HATA. İki tekrar ölçümü arasında hiç sonuç değişmediği için (Bölüm 2.7) bu fark gürültü değil.

#### Bulgular

1. **Başarı ölçütü karşılandı.** hit@1 %68.9 → %81.1 ve hit@3 %87.8 → %93.2 oldu. Kelime ortasından başlayan parça kalmadı.
2. **Eşikte kalan yanlış redler artık tamamen eşik sorunu.** Eşikte reddedilen 8 sorunun hepsinde doğru parça 1. ya da 2. sırada. Örnekler: "Kımız nedir?" 17. sıradan 1. sıraya, "Dokuz Işık ilkeleri" 7. sıradan 1. sıraya çıktı. Ama skorları 0.336–0.420 arasında, yani 0.42 eşiğinin altında. Faz 3'te eşik düzeltilirse bu 8 soru doğrudan kazanılabilir.
3. **Parçalama skor dağılımını değiştirdi, bu yüzden eşik yeniden ayarlanmalı.** "Sakarya kaç gün sürdü?" sorusunda doğru parça hâlâ 1. sırada, ama skoru 0.511'den 0.396'ya düştü ve soru eşikte reddedildi. Bu, eski 12 soruluk setteki kaybın sebebi. 0.42 değeri eski parçalamaya göre seçilmişti.
4. **Bağlamsız paragraf riski gerçekleşti.** "Orhun Yazıtları'nın alfabesini kim çözmüştür?" sorusunda doğru parça 2. sıradan 5. sıraya düştü, aynı paragrafı kullanan takip sorusu da 3. sıradan 5. sıraya. Thomsen paragrafı "Yazıtların dili uzun süre çözülememiştir" diye başlıyor, "Orhun" kelimesi bir önceki paragrafta kalıyor ve belgenin başlığı ("İlk Türk Devletleri") bu boşluğu kapatmıyor.
   - Alt başlık önekinin `isimler-5` sorusunda arama sırasını düzeltmediği görüldü: 3. sıradan 4. sıraya düştü.
   - 5 soruda doğru parça 1. sıradan 2. sıraya indi, ama bu soruların hepsi hâlâ başarılı.
5. **Kötüleşen 5 sorunun sebepleri farklı:**
   - Eşik: `canakkale-3` (3. bulgu).
   - Konu değişiminde birleşik arama: "Turan taktiği" sorusundan sonra "Kımız nedir?" soruldu ve doğru parça 2. sıradan 8. sıraya düştü (H10).
   - Modelin yanlış adı seçmesi: `ulku-2` sorusuna "Ülkü Ocakları 1978'de hangi adı aldı?" diye soruldu. Doğru paragraf 1. sıradaydı ama model 1973'teki adı yazdı.
   - Red cevabına kaynak eklenmesi: `cevapsiz-1` ve `takip-cevapsiz-2`. Red kararı doğru, sadece biçim hatası (H5).
6. **Red cevabına kaynak ekleme 4'ten 9'a çıktı.** Model artık daha çok soruyu reddediyor ve reddederken de kaynak yazıyor. Kodla çözülecek bir biçim sorunu (H5).
7. **Cevaplar kısaldı ve hızlandı.** Parçalar kısaldığı için modele giden bağlam da kısaldı. İlk token süresi 1.0 sn'den 0.74 sn'ye indi.
8. **Gözle kontrol.**
   - Otomatik "HATA" kararlarının hepsi gerçek hata.
   - Otomatik puanlamanın cömert davrandığı 2 soru var:
     - `osmanli-4`: "Osman Gazi'nin oğlu" bilgisi belgede yok, Faz 0'dan beri böyle.
     - `kurt-4`: "kurt kelimesinin anlamı böri, yani solucan..." diye iki bilgiyi karıştırıyor. Yeni çıktı.
   - `kurt-6` gerçek bir model hatası: bağlamda "Börteçine" geçtiği halde "yolu Böri gösterdi" yazdı.

#### Karar

**Faz 1 değişikliği tutuluyor.** Başarı ölçütü karşılandı ve kazanımlar kayıplardan belirgin biçimde fazla.

Bağlamsız paragraf sorunu (4. bulgu) için **H1b** önerildi. Faz 2'den ayrı ölçülmeli: iki değişiklik birlikte yapılırsa hangisinin etkili olduğu anlaşılamaz.

> **Faz 2'den sonra:** H1b'yi gerektiren iki soru (`ilkturk-1`, `isimler-5`) sorgu talimatıyla çözüldü (Bölüm 2.9). H1b şimdilik gerekli görünmüyor.

### 2.9 Faz 2 sonuçları: sorgu talimatı

**Raporlar:**
- İngilizce talimat: [2026-09-14_0442_faz2-talimat.md](../degerlendirmeler/2026-09-14_0442_faz2-talimat.md). Reddedildi. Bu çalıştırmanın süreleri geçersiz.
- Türkçe talimat: [2026-09-14_0505_faz2b-turkce-talimat.md](../degerlendirmeler/2026-09-14_0505_faz2b-turkce-talimat.md). Kabul edildi.

İki rapor da Faz 1 ile karşılaştırmalı.

#### Değişiklik ([search.py](../search.py))

- Soru vektörü oluşturulurken sorunun başına görev talimatı ekleniyor: `Instruct: Soruyu cevaplayan paragrafı bul\nQuery:<soru>`. Bu biçimi Qwen3-Embedding öneriyor.
- Belge vektörlerine dokunulmadı. Belgeler talimatsız gömülüyor ve veritabanı yeniden oluşturulmadı.
- Talimat `QUERY_INSTRUCTION` sabitinde duruyor. `None` yapılırsa talimat kapanır. Raporlar kullanılan talimatı kaydediyor.

#### Deneme sırası

**1. Planda yazan İngilizce talimat reddedildi.** Denenen talimat: `"Given a question, retrieve passages that answer the question"`.
- hit@1 %81.1 → %74.3 ve hit@3 %93.2 → %90.5 oldu, Faz 2'nin başarı ölçütü karşılanmadı.
- Tam başarı %76.7 → %78.9 ile artmış görünüyordu. Ama bunun sebebi aramanın iyileşmesi değil, skorların yükselip eşiği fiilen düşürmesiydi.
- Takip soruları bozuldu: "sonucu ne oldu?" sorusunda doğru parça 21. sıraya, "kaç dizeden oluşur?" sorusunda 37. sıraya düştü.
- Cevaplanamaz soruları reddetme %100 → %87.5 oldu. Model iki cevapsız takip sorusunda alakasız bir paragrafı anlattı.
- **Bu çalıştırmada süreler geçersiz.** İlk 3 sorudan sonra ilk token süresi ~1 sn'den 5–13 sn'ye çıktı ve Foundry 3.9 GB sistem RAM'i kullanıyordu. Sunucu kayıtlarında yeniden başlatma ya da model yükleme olayı yok. En olası sebep, ölçüm sırasında açık olan Streamlit uygulamasından gelen eşzamanlı bir istek, ama bu doğrulanamadı. Temiz sunucuda yapılan sonraki ölçümde süreler normaldi.

**2. Talimat biçimleri yalnızca arama üzerinde karşılaştırıldı** ([talimat_arama.py](olcum_betikleri/talimat_arama.py)). Model kullanılmadı. Sorular: 65 cevaplanabilir, 10 cevaplanamaz tekil soru ve 7 takip sorusu.

| Talimat | hit@1 | hit@3 | MRR | Ayrım (AUC) | Eşik altı cevaplanabilir | Eşik üstü cevaplanamaz | Tek başına eşiği geçen takip sorusu |
|---|---|---|---|---|---|---|---|
| Talimat yok (Faz 1) | 83.1 | 95.4 | 0.898 | 0.782 | 8 | 6/10 | 0/7 |
| İngilizce genel | 78.5 | 93.8 | 0.866 | 0.780 | 0 | 6/10 | 6/7 |
| İngilizce, boşluklu `Query: ` | 76.9 | 92.3 | 0.862 | 0.788 | 0 | 6/10 | 6/7 |
| İngilizce, Türk tarihi vurgulu | 89.2 | 96.9 | 0.936 | 0.791 | 1 | 6/10 | 5/7 |
| **Türkçe: "Soruyu cevaplayan paragrafı bul"** | **89.2** | **98.5** | **0.935** | **0.803** | 1 | 6/10 | **3/7** |

AUC şunu ölçüyor: rastgele seçilen bir cevaplanabilir sorunun en iyi skoru, rastgele bir cevaplanamaz sorununkinden ne sıklıkla yüksek. 1.0 tek bir eşikle kusursuz ayrım demek, 0.5 hiç ayrılmıyor demek.

**Türkçe talimat seçildi.** Sebepler:
- En yüksek hit@3 ve ayrım değeri onda.
- Tek başına eşiği geçen takip sorusu en az onda.
- Konuya özel değil, genel bir talimat.

**3. Türkçe talimatla uçtan uca ölçüm yapıldı ve kabul edildi.**

#### Sonuçlar (Faz 1 → Faz 2)

| Ölçüt | Başlangıç | Faz 1 | Faz 2 |
|---|---|---|---|
| Tam başarı | %67.8 | %76.7 | **%85.6** |
| hit@1 / hit@3 | %68.9 / %87.8 | %81.1 / %93.2 | **%85.1 / %94.6** |
| Cevaplanabilir sorularda başarı | %66.2 | %79.7 | %90.5 |
| Yanlış red (eşikte) | %20.3 (%17.6) | %16.2 (%10.8) | **%5.4 (%1.4)** |
| Kaynak doğru belge | %91.5 | %98.4 | %97.1 |
| Cevaplanamaz soruları reddetme (eşikte) | %93.8 (%37.5) | %100 (%31.2) | %100 (%25.0) |
| Red cevabına eklenmiş kaynak | 4 | 9 | 6 |
| Süre ortalaması / ilk token | 1.77 / 1.0 sn | 1.65 / 0.74 sn | 1.81 / 0.62 sn |
| Arama süresi (tekil soru, medyan) | — | 0.27 sn | 0.40 sn |
| Eski 12 soruluk set | 10/12 | 9/12 | 10/12 |

| Kategori | Faz 1 başarı | Faz 2 başarı |
|---|---|---|
| normal (55) | 45 | **53** |
| ozel_ad (10) | 7 | 8 |
| yakın (6) | 2 | 2 |
| takip (5) | 4 | **3** |
| takip, cevapsız (2) | 1 | 1 |
| konu değişimi (4) | 3 | 3 |
| konu dışı, önceki sorudan sonra (4) | 3 | 3 |

#### Bulgular

1. **Başarı ölçütü karşılandı.** hit@1 %81.1 → %85.1 oldu, Faz 1'in altına düşmedi. Zayıf soruların skoru arttı: Faz 1'de eşikte reddedilen 8 sorunun 7'si eşiği geçti (0.455–0.572). "Kımız nedir?" doğru parçası 1. sırada olduğu halde 0.346 skorla hâlâ eşiğin altında. Kalan tek eşikte red bu.
2. **Kazancın kaynağı:** HATA'dan OK'e geçen 11 soru.
   - **7'si skor kaymasından.** Doğru parça zaten 1. ya da 2. sıradaydı, sadece skor eşiğin üstüne çıktı. Bu kazanç Faz 3'teki eşik ayarıyla da elde edilebilirdi.
   - **3'ü gerçek arama iyileşmesinden.** Orhun sorusunda doğru parça 5. sıradan 3. sıraya, BBP sorusunda 4'ten 3'e, "Yurtta sulh" sorusunda 9'dan 3'e çıktı. Faz 1'deki bağlamsız paragraf sorunu bu iki soruda böylece kapandı.
   - **1'i modelin cevabındaki değişkenlikten** (`ulku-2`).
3. **Takip sorusu kuralı zayıfladı (H10).** Talimat kısa soruların skorunu da yükseltiyor.
   - "kaç dizeden oluşur?" artık tek başına eşiği geçiyor. Önceki soru ("Manas Destanı...") kullanılmıyor ve doğru parça 1. sıradan 9. sıraya düştü.
   - Konu değişiminde "Kımız nedir?" sorusu 8. sıradan 30. sıraya düştü.
   - Yalnızca aramayla yapılan ölçümde 7 takip sorusundan 3'ü tek başına eşiği geçiyor.
4. **Yeni 3 kötüleşme:**
   - Takip sorusu (`takip-3`, 3. bulgu).
   - "Kut nedir?" (`gelenek-1`): doğru parça 3. sıradan 4. sıraya düştü, model reddetti.
   - "Turan taktiği" (`at-1`): cevap doğru ama kaynak olarak kurt belgesini yazdı (H5).
5. **Arama süresi ~130 ms arttı** (tekil soru medyanı 0.27 → 0.40 sn). Talimat gömme isteğine sadece ~15 token ekliyor, bu yüzden sebep net değil. Sunucunun yeniden başlatılmasından sonraki bellek yerleşimi de etkili olabilir (H11). Toplam süre 1.65 → 1.81 sn, hâlâ hedefin içinde.
6. **Gözle kontrol.**
   - Yeni "OK" cevaplarının hepsi doğru.
   - `ulku-2` ve `isimler-2` cevaplarında anlatım bozuk, ama bilgi doğru.
   - `kurt-6` hâlâ "yolu Böri gösterdi" diyor. Doğrusu Börteçine, model hatası.

#### Uyarı: sonuç iyimser olabilir

Talimat biçimi, sonuçları görülen **aynı soru seti** üzerinde 5 biçim arasından seçildi. Bu, seçimin bu 65 soruya uyması riskini taşıyor. Riski azaltan iki etken var:
- Seçilen talimat konuya özel değil, genel ("Soruyu cevaplayan paragrafı bul").
- İngilizce genel talimattan farkı büyük: hit@1'de 11 puan.

Yine de gerçek kazanç bu ölçümden biraz düşük olabilir. **Öneri:** Model kararından önce, sonuçlar görülmeden yazılmış yeni sorulardan küçük bir kontrol seti (Faz 5.5) ile doğrulanmalı.

#### Karar

**Türkçe talimat tutuluyor.** Faz 2 ölçütü karşılandı, kazanım belirgin.

**Bundan sonraki karşılaştırma noktası:** [2026-09-14_0505_faz2b-turkce-talimat.json](../degerlendirmeler/2026-09-14_0505_faz2b-turkce-talimat.json).

**Değerlendirmeye eklenen koruma:** `evaluate.py` artık ilk token ortalaması 3 sn'yi aşarsa raporun başına "süre ölçütleri geçersiz" uyarısı koyuyor. İngilizce talimatlı çalıştırmanın raporunda bu uyarı görünüyor.

### 2.10 Faz 3 sonuçları: eşik ve takip sorusu kuralı

**Raporlar:**
- Takip kuralı: [2026-09-14_0525_faz3a-takip-farki.md](../degerlendirmeler/2026-09-14_0525_faz3a-takip-farki.md). Faz 2 ile karşılaştırmalı.
- Eşik: [2026-09-14_0530_faz3b-esik-033.md](../degerlendirmeler/2026-09-14_0530_faz3b-esik-033.md). Faz 3a ile karşılaştırmalı.

**Analiz betiği:** [esik_takip_analiz.py](olcum_betikleri/esik_takip_analiz.py). Model kullanmıyor, yaklaşık 1 dakika sürüyor.

#### Adım 1: Modelsiz analiz

**Skor dağılımı** (Türkçe talimat açık, 65 cevaplanabilir ve 10 cevaplanamaz tekil soru):

| Grup | En iyi skor aralığı |
|---|---|
| Cevaplanabilir | 0.346 ("Kımız nedir?"), sonra 0.421 ve üstü |
| **Cevaplanamaz, konuya yakın** (Fatih'in annesi, Malazgirt'teki asker sayısı…) | **0.516 – 0.691** |
| Cevaplanamaz, konu dışı / anlamsız (hava, ofsayt, Python, asdf) | 0.317 – 0.369 |

| Eşik | Eşikte reddedilen cevaplanabilir (65) | Eşiği geçen cevaplanamaz (10) |
|---|---|---|
| 0.30 | 0 | 10 |
| **0.33** | **0** | **8** |
| 0.36 | 1 | 8 |
| 0.42 (eski) | 1 | 6 |
| 0.50 | 8 | 6 |
| 0.60 | 21 | 3 |
| 0.70 | 38 | 0 |

**Takip sorusu kuralları** (hit@1 / hit@3):

| Kural | Takip (5) | Konu değişimi (4) | Yapay konu değişimi (65) | Eşiği geçen cevaplanamaz (önceki sorudan sonra) |
|---|---|---|---|---|
| Mevcut: tek başına skor eşiğin altındaysa birleşik ara | 2 / 3 | 3 / 3 | 57 / 63 | 6/6 senaryo, 9/10 yapay |
| Fark ≥ 0.10 | 4 / 4 | 2 / 2 | 53 / 58 | 6/6, 9/10 |
| Fark ≥ 0.15 | 4 / 4 | 3 / 3 | 55 / 60 | 6/6, 8/10 |
| **Fark ≥ 0.20** | **4 / 4** | **3 / 3** | **57 / 62** | 6/6, 7/10 |
| İki aramayı birleştir | 4 / 4 | 1 / 2 | 39 / 57 | 6/6, 9/10 |
| Her zaman birleşik ara (Faz 0 öncesi) | 4 / 4 | 1 / 1 | 28 / 42 | 6/6, 9/10 |

"Yapay konu değişimi" şu şekilde ölçüldü: her cevaplanabilir soru, başka bir belgeden gelen bir sorudan hemen sonra sorulmuş gibi arandı. Senaryolarda sadece 4 konu değişimi olduğu için, kuralın konu değişiminde aramayı bozup bozmadığı böylece çok daha fazla örnekle görüldü.

**Birleşik ile tek başına arama arasındaki skor farkı:**
- Gerçek takip soruları: +0.23 ile +0.35 arası.
- Yapay konu değişimleri (59): medyan -0.015. Sadece 4'ünde fark 0.15'i geçiyor.

#### Analizden çıkan kararlar

1. **Tek bir eşik değeriyle iki grubu ayırmak mümkün değil (A yaklaşımı elendi).** Konuya yakın cevaplanamaz sorular, cevaplanabilir soruların çoğundan yüksek skor alıyor. Hepsini eşikte reddetmek için eşiğin 0.70 olması gerekir, bu da 38 cevaplanabilir soruyu kaybettirir. **C yaklaşımı seçildi:** eşik düşük bir güvenlik tabanı, konuya yakın soruları model reddediyor.
2. **Takip sorusu kuralı skor farkına bakmalı.**
   - Mevcut kural, tek başına skor eşiğin altındaysa birleşik aramaya geçiyordu. Bu kuralın kararı eşiğe bağlıydı: talimat skorları yükseltince bozuldu, eşik düşürülürse daha da bozulurdu.
   - Fark kuralı eşikten bağımsız.
   - 0.20 seçildi. Gerçek takip sorularında en küçük fark 0.23, yapay konu değişimlerinde ise mevcut kuralla aynı sonucu veriyor.
3. **H10'un "konu dışı soruyu önceki sorudan sonra da eşikte reddet" hedefi skorla gerçekleştirilemez.** Hiçbir kural bunu yapamıyor. Bu sorular birleşik aramada önceki sorunun skorunu taşıyor ya da tek başına zaten eşiğin üstünde kalıyor. Kabul edilen durum: bunları model reddediyor, 4 senaryonun 4'ünde de reddetti.

#### Adım 2 ve 3: Uçtan uca ölçüm

| Ölçüt | Faz 2 | 3a: takip farkı | 3b: + eşik 0.33 |
|---|---|---|---|
| Tam başarı | %85.6 | %86.7 | **%87.8** |
| hit@1 / hit@3 | %85.1 / %94.6 | %87.8 / %95.9 | %87.8 / %95.9 |
| Cevaplanabilir sorularda başarı | %90.5 | %91.9 | %93.2 |
| Yanlış red (eşikte) | %5.4 (%1.4) | %4.1 (%1.4) | **%2.7 (%0)** |
| Cevaplanamaz soruları reddetme (eşikte) | %100 (%25) | %100 (%25) | %100 (%12.5) |
| Takip kategorisi | 3/5 | 4/5 | 4/5 |
| Süre ortalaması | 1.81 sn | 1.89 sn | 1.97 sn |
| Sonucu değişen soru | — | 1 ("kaç dizeden oluşur?" HATA → OK) | 1 ("Kımız nedir?" HATA → OK) |

İki adımın sonucu da analizin öngörüsüyle birebir örtüştü. Başka hiçbir sorunun sonucu değişmedi.

#### Bulgular

1. **Başarı ölçütü karşılandı.** Yanlış red %2.7 (hedef ≤ %5). Cevaplanamaz soruları reddetme %100, önceki bir sorudan sonra sorulduğunda da.
2. **Eşik 0.33'e inince iki konu dışı soru artık modelde reddediliyor** ("Python'da liste" ve "asdf"). Model ikisini de kaynak satırı eklemeden doğru reddetti. Bunun maliyeti soru başına ~1.7 sn: eşikte red 0.2 sn, model reddi yaklaşık 1.9 sn.
3. **Reddetme kararı artık büyük ölçüde modelde.** Cevaplanamaz soruların %87.5'ini model reddediyor. Faz 5'te model değiştirilirse bu oran mutlaka yeniden ölçülmeli.
4. **0.33 eşiğinin payı dar.** En düşük cevaplanabilir soru 0.346. Yeni bir kısa kavram sorusu tabanın altında kalabilir. Bu değer 105 soruya bakılarak seçildi, Faz 5.5'teki kontrol setinde özellikle kısa kavram sorularıyla test edilmeli.
5. **Kalan 11 hatanın sebepleri:**

| Sebep | Soru | Çözecek hamle |
|---|---|---|
| Red cevabına kaynak satırı ekleniyor | 6 (4 konuya yakın tekil soru, 1 cevapsız takip, 1 önceki sorudan sonra konu dışı) | H5 |
| Cevap doğru, kaynak yanlış belge | 1 (`at-1`, Turan taktiği) | H5 |
| Takip sorusunda model önceki soruyu görmüyor ("hangi yılda?" → 1928) | 1 (`takip-2`) | H9 |
| Doğru parça ilk 3'te değil | 2 ("Kut nedir?" 4. sıra; Turan'dan sonra "Kımız nedir?" 30. sıra) | H4 / H6 |
| Bağlamda doğru ad var, model yanlışını yazıyor ("Böri" yerine "Börteçine") | 1 (`kurt-6`) | H7 / H8 |

   Turan'dan sonra "Kımız nedir?" sorusunda kural bilinen sınırında çalışıyor: soru tek başına düşük skor aldığı için (0.346) birleşik skorla arasındaki fark büyük (+0.31), kural bunu takip sorusu sayıyor.

#### Karar

**Takip farkı 0.20 ve eşik 0.33 tutuluyor.**

**Bundan sonraki karşılaştırma noktası:** [2026-09-14_0530_faz3b-esik-033.json](../degerlendirmeler/2026-09-14_0530_faz3b-esik-033.json).

### 2.11 Faz 5 sonuçları: kaynak, takip bağlamı, bağlam boyutu, model

Faz 5'teki hamleler tek tek uygulandı. Her biri bir önceki kabul edilen yapılandırmayla karşılaştırıldı. Tüm ölçümler temiz sunucuda yapıldı.

| Adım | Değişiklik | Rapor | Tam başarı | Karar |
|---|---|---|---|---|
| Faz 3b | (karşılaştırma noktası) | [0530](../degerlendirmeler/2026-09-14_0530_faz3b-esik-033.md) | %87.8 | — |
| 5a | H5: Kaynak satırını kod belirliyor. Sistem komutundan kaynak kuralı çıkarıldı | [0557](../degerlendirmeler/2026-09-14_0557_faz5a-kaynak-kodda.md) | %93.3 | Ara adım |
| 5b | H9: Takip sorusunda önceki soru modele gösteriliyor | [0601](../degerlendirmeler/2026-09-14_0601_faz5b-takip-baglami.md) | %91.1 | **Reddedildi** |
| 5b′ | H9 kapatıldı, yeniden düzenlenen kodun 5a'yı tekrarladığı doğrulandı | [0609](../degerlendirmeler/2026-09-14_0609_faz5b-geri-alindi.md) | %93.3 (değişen sonuç 0) | Doğrulama |
| 5c | H6: `TOP_K = 5` | [0612](../degerlendirmeler/2026-09-14_0612_faz5c-topk5.md) | %90.0 | **Reddedildi** |
| 5d | H5, sistem komutu Faz 3'teki haliyle: model kaynak yazıyor, kod siliyor ve kendi kaynağını ekliyor | [0626](../degerlendirmeler/2026-09-14_0626_faz5d-eski-istem-kaynak-kodda.md) | **%95.6** | **Kabul** |
| 5e | H7: qwen3-4b (5d yapılandırmasıyla) | Rapor yok, ölçüm çöktü | 62 soruda 52 (qwen2.5-7b: 60) | **Reddedildi** |

#### 5a / 5d: Kaynak satırını kod belirliyor (H5)

**Nasıl çalışıyor** ([rag.py](../rag.py) `pick_source`):
- Modelin yazdığı kaynak satırı siliniyor.
- Cevaptaki kelimeler (5 harflik kök) getirilen 3 parçayla karşılaştırılıyor. Sorunun kendi kelimeleri sayılmıyor, böylece cevabın **eklediği** bilginin hangi parçadan geldiğine bakılıyor.
- En çok örtüşen parçanın belgesi kaynak olarak ekleniyor. Eşitlikte arama sırası daha iyi olan parça seçiliyor.
- Red cevabına kaynak eklenmiyor.

**Modelsiz ön test** ([kaynak_secimi.py](olcum_betikleri/kaynak_secimi.py)): Faz 3b cevaplarında model kaynak satırı silinip kaynak koda buldurulduğunda kod 72 sorunun 71'inde doğru kaynağı buldu, model 70'inde bulmuştu. Kodun "yanlış" bulduğu tek soru `takip-2`: modelin yanlış cevabı (1928) gerçekten alfabe belgesinden geliyor, kod da o belgeyi gösteriyor.

**5a'daki sistem komutu dersi:** İlk denemede sistem komutundan "kaynağı belirt" kuralı ve örnek kaynak satırı çıkarıldı.
- 8 soru düzeldi: 6 red cevabındaki kaynak satırı, Turan taktiğinin kaynağı ve modelin `kurt-6`'daki değişkenliği.
- 3 soru kötüleşti: Model "Çanakkale Deniz Zaferi" ve "Orhun alfabesi" sorularını reddetti. Dokuz Işık ilkelerini belgedeki kelimelerle değil kendi ifadesiyle yazdı.

5d'de sistem komutu Faz 3'teki haline döndürüldü. Kaynak satırı yine koddan geliyor ve kaybedilen 3 soru geri geldi. **Sonuç:** Bu model, sistem komutundaki küçük biçim değişikliklerine bile çok hassas.

#### 5b: Önceki soruyu modele göstermek (H9) — reddedildi

Takip kuralı birleşik aramayı seçtiğinde, kullanıcı mesajına şu eklendi: `ÖNCEKİ SORU: ...` ve "SORU, ÖNCEKİ SORU'nun devamıdır". Sonuç:

- **Uydurma geldi.** "Sakarya kaç gün sürdü?" sorusundan sonra "bunun sebebi ne?" diye sorulunca model belgede olmayan bir sebep uydurdu, cevapta "Kürt askerleri" gibi hiçbir kaynakta olmayan ifadeler var.
- "asdf qwerty zxcv" girdisine önceki soruyu cevapladı.
- Turan'dan sonra "Kımız nedir?" sorusunu reddetmek yerine "atlı savaşın temel unsuru" dedi.
- **Hedeflenen soru çözülmedi.** "hangi yılda?" sorusunda doğru parça 5. sırada kaldığı için modele hiç ulaşmadı. Model 1928 yazmak yerine reddetti, ama soru yine HATA.

Tam başarı %93.3 → %91.1 oldu, cevaplanamaz soruları reddetme %100 → %87.5. Kod `FOLLOW_UP_CONTEXT_TO_MODEL = False` olarak bırakıldı.

**Sonuç:** Modele "cevap vermesi gereken bir soru" olduğunu ima eden yönlendirmeler, reddetme davranışını zayıflatıyor.

#### 5c: `TOP_K = 5` (H6) — reddedildi

- **Modelsiz analiz:** Doğru parça `TOP_K = 3` ile 74 sorunun 71'inde, `TOP_K = 5` ile 73'ünde bağlama giriyor. Ek olarak girenler "Kut nedir?" ve "hangi yılda?".
- **Uçtan uca ölçüm:**
  - "Kut nedir?" kazanıldı.
  - 4 soru kaybedildi: Model uzun bağlamda 2 soruyu reddetti ("Anadolu Selçuklu Devleti'ni kim kurdu?", "bu gazete nerede çıkarıldı?"), 2 soruda doğru ifadeyi kaçırdı.
  - Tam başarı %93.3 → %90.0.
  - **Süre 1.75 sn'den 7.0 sn'ye çıktı**, ilk token 6.1 sn. Açılıştaki ısıtma istemi de 5 parçayla büyüdüğü için ekran kartı belleği yetmedi ve Bölüm 2.5'teki yavaşlık geri geldi.
- **Karar:** `TOP_K = 3` kalıyor. Deneyler için `LRA_TOP_K` ortam değişkeni eklendi.

#### 5d: Kabul edilen yapılandırma

| Ölçüt | Başlangıç | Faz 3b | **Faz 5 (5d)** |
|---|---|---|---|
| Tam başarı | %67.8 | %87.8 | **%95.6** |
| hit@1 / hit@3 | %68.9 / %87.8 | %87.8 / %95.9 | %87.8 / %95.9 |
| Cevaplanabilir sorularda başarı | %66.2 | %93.2 | %94.6 |
| Yanlış red | %20.3 | %2.7 | %2.7 |
| Anahtar ifadelerin tamamı | %91.5 | %97.2 | %97.2 |
| Kaynak var / doğru belge | %96.6 / %91.5 | %100 / %97.2 | %100 / **%98.6** |
| Red cevabına eklenmiş kaynak | 4 | 6 | **0** |
| Cevaplanamaz soruları reddetme | %93.8 | %100 | %100 |
| Süre ortalaması / ilk token | 1.77 / 1.0 sn | 1.97 / 0.72 sn | 1.95 / 0.74 sn |
| Eski 12 soruluk set | 10/12 | 10/12 | **12/12** |

**Gözle kontrol:** 5d'deki cevap veren her soru okundu.
- **Yanlış ya da karışık bilgi içeren 3 cevap var** (74 cevaplanabilir sorunun %4.1'i):
  - `takip-2`: "hangi yılda?" sorusuna 1928 yazıyor.
  - `kurt-6`: yolu gösterenin adını "Böri" yazıyor, doğrusu Börteçine.
  - `kurt-4`: "kurt kelimesinin anlamı böri, yani solucan..." diye iki bilgiyi karıştırıyor. Otomatik puanlama bunu kaçırıyor.
- 16 cevaplanamaz sorunun hepsi reddedildi, uydurma yok.
- Birkaç cevapta dil hatası ya da bozuk anlatım var ("Viyanan", "Manısa Destanı", "Atatürk'nün"), ama bilgiler doğru.

**Kalan 4 hata:**

| Soru | Sebep | Çözecek hamle |
|---|---|---|
| "Kut nedir?" | Doğru parça 4. sırada, model reddediyor | **H4 (hibrit arama)**: prototipte 1. sıraya çıkıyor |
| "hangi yılda?" (Orhun'dan sonra) | Birleşik aramada doğru parça 5. sırada. Model bağlamdaki tek yılı (1928) yazıyor | Arama iyileşmesi gerekli. H9 uydurma getirdiği için modele önceki soruyu göstermek çözüm değil |
| Turan'dan sonra "Kımız nedir?" | Takip kuralının bilinen sınırı: soru tek başına düşük skor aldığı için takip sorusu sayılıyor | H4 bu soruda tek başına aramayı güçlendirebilir, ölçülmeli |
| "Ergenekon'da yolu kim gösterdi?" | Bağlamda "Börteçine" var, model "Böri" yazıyor. Değişken bir soru: Faz 3b'de HATA, 5a'da OK, 5d'de HATA | Model sınırı |

#### 5e: Model karşılaştırması (H7) — qwen2.5-7b kalıyor

qwen3-4b, 5d yapılandırmasıyla ve `/no_think` ile ölçüldü. Deneyler için `LRA_CHAT_MODEL` ortam değişkeni eklendi. Qwen3 modellerinde `/no_think` kodda otomatik ekleniyor.

- **Ölçüm 62. soruda çöktü.** Foundry sunucu kaydında `CUDA failure 700: an illegal memory access was encountered` hatası var. Değerlendirme betiği bağlantı koptuğu için durdu ve rapor yazılamadı.
- **Tamamlanan aynı 62 soruda:**

| | qwen2.5-7b | qwen3-4b |
|---|---|---|
| Başarılı | **60** | 52 |
| Süre ortalaması | 2.00 sn | 1.28 sn |
| Yalnızca bu modelin başarılı olduğu soru | 9 | 1 (`kurt-6`) |

- **qwen3-4b'nin kaybettiği sorular** çoğunlukla bağlamdaki adı atladığı basit bilgi soruları: Tonyukuk, Yazıcıoğlu, Mustafa Efendi, Süleyman Şah. "Osman Gazi" sorusunda "Bursa'da kuruldu" uydurmasını, Faz 0'daki 14 soruluk testte olduğu gibi tekrarladı.
- **Karar:**
  - qwen2.5-7b kalıyor. Hız ikisinde de hedefin içinde, doğruluk ve kararlılık farkı belirgin.
  - Ölçüm tekrarlanmadı, çünkü karar net ve çökme ekran kartını kararsız bırakabiliyor.
  - qwen3-8b (5.5 GB) denenmedi. qwen2.5-7b ile aynı bellek sınırında çalışacak ve kalan tek model hatası (`kurt-6`) değişken bir soru.

#### H8 (sistem komutunu sıkılaştırmak): uygulanmadı

- **Kalan model hataları çok az.** H8'in hedefleyebileceği yalnızca `kurt-6` (değişken) ve `kurt-4` (karışık cevap) var.
- **Risk kazançtan büyük.** 5a ve 5b, bu modelin sistem komutu değişikliklerine çok hassas olduğunu gösterdi: bir kural çıkarmak 3 soru kaybettirdi, bir yönlendirme eklemek uydurma getirdi.

İleride model değişirse yeniden değerlendirilmeli.

#### Faz 4 için test: hibrit arama prototipi

**Ne yapıldı** ([hibrit_prototip.py](olcum_betikleri/hibrit_prototip.py)):
- SQLite FTS5 anahtar kelime indeksi bellekte kuruldu. Veritabanına yazılmadı, model kullanılmadı.
- Vektör sırası ve kelime sırası Reciprocal Rank Fusion ile birleştirildi: `1/(k + vektör sırası) + 1/(k + kelime sırası)`.
- Sorudaki soru kelimeleri ("nedir", "hangi", "kimdir"...) aranmadı.

**Sonuçlar** (65 cevaplanabilir tekil soru):

| Arama | hit@1 | hit@3 | MRR | Özel ad hit@1 | Konu değişimi hit@1 | İyileşen | Kötüleşen |
|---|---|---|---|---|---|---|---|
| Yalnız vektör (şu an) | 58 | 64 | 0.935 | 9/10 | 4/4 | — | — |
| Hibrit, tam kelime (k=10 ya da 60) | 60 | 64 | 0.956 | 10/10 | 4/4 | 4 | **2** ("Orhun alfabesi" 3. sıradan 9–14. sıraya) |
| **Hibrit, 5 harflik önek (k=10 ya da 60)** | **61** | **65** | **0.967** | **10/10** | 4/4 | 4 | **0** |

**İyileşen sorular:**
- "Kut nedir?" 4. sıradan 1. sıraya.
- "Yurtta sulh" 3. sıradan 1. sıraya.
- "Azerbaycan Türkçesinde kurt" 2. sıradan 1. sıraya.
- "BBP'yi kim kurdu?" 3. sıradan 2. sıraya.

**Bulgular:**
- **Önek neden önemli:** Türkçe eklerle tam kelime eşleşmesi kırılıyor. Önekli arama bu kırılmayı önlüyor ve hiçbir soruyu kötüleştirmiyor.
- **k değeri** (10 ya da 60) sonucu değiştirmedi.
- **Test edilmeyenler:** Takip sorularında birleşik metinle kelime araması ve hibrit sıralamanın eşik ile takip farkı kuralına etkisi. Prototip yalnızca tekil sorularda sıralamayı ölçtü.
- **Karar:** Faz 4 uygulanmalı. Uygulama planı Bölüm 6'da.

**Bundan sonraki karşılaştırma noktası:** [2026-09-14_0626_faz5d-eski-istem-kaynak-kodda.json](../degerlendirmeler/2026-09-14_0626_faz5d-eski-istem-kaynak-kodda.json).

### 2.12 Faz 4 sonuçları: hibrit arama

**Raporlar:**
- Hibrit açık: [2026-09-14_0702_faz4-hibrit.md](../degerlendirmeler/2026-09-14_0702_faz4-hibrit.md).
- Hibrit kapalı (doğrulama): [2026-09-14_0709_faz4-hibrit-kapali.md](../degerlendirmeler/2026-09-14_0709_faz4-hibrit-kapali.md).

İkisi de 5d ile karşılaştırmalı.

#### Değişiklik

- **[ingest.py](../ingest.py):**
  - `chunks_fts` adında bir FTS5 tablosu eklendi. Satır numarası parça id'siyle aynı. Metin Türkçe küçük harfe çevriliyor (`fold`: İ/I sorunu), tokenizer `unicode61`.
  - `python ingest.py --fts` yalnızca bu indeksi mevcut parçalardan kuruyor. Vektörlere dokunmuyor.
- **[search.py](../search.py):**
  - `search_details()` iki şey döndürüyor: parçalar (hibrit sırada) ve **en yüksek vektör skoru**.
  - Kelime aramasında soru kelimeleri atılıyor ("nedir", "hangi"...). 5 harften uzun kelimeler 5 harflik önekle aranıyor.
  - Vektör ve kelime sıraları RRF ile birleştiriliyor (`RRF_K = 60`).
  - FTS tablosu yoksa bir kez uyarı verilip yalnızca vektör aramasına dönülüyor.
  - Aç/kapat: `HYBRID_SEARCH`.
- **[rag.py](../rag.py):**
  - **Eşik ve takip farkı kararları artık `hits[0][0]` ile değil, en yüksek vektör skoruyla veriliyor.** Hibrit sırada ilk parça en yüksek vektör skorlu parça olmayabilir. Bu değişiklik yapılmasaydı Faz 3'teki eşik ayarları sessizce bozulurdu.
  - `answer_details` sonucuna `best_score` eklendi.
- **Diğer:**
  - [app.py](../app.py), [masaustu.py](../masaustu.py): "en yüksek eşleşme" göstergesi getirilen parçaların en yüksek skorunu gösteriyor.
  - [evaluate.py](../evaluate.py): Rapora arama türü yazılıyor.
  - `esik_takip_analiz.py` ve `talimat_arama.py` Faz 2–3'teki ölçümleri tekrar edebilmek için hibrit aramayı kapatarak çalışıyor.
- **Yedek:** Faz 4 öncesi veritabanı `knowledge_faz5_yedek.db`.

#### 4c: Gerçek kodla modelsiz kontrol ([faz4_kontrol.py](olcum_betikleri/faz4_kontrol.py))

| Grup | Vektör (hit@1 / hit@3 / n) | Hibrit |
|---|---|---|
| Tekil cevaplanabilir | 58 / 64 / 65 | **61 / 65 / 65** |
| Özel ad | 9 / 9 / 10 | **10 / 10 / 10** |
| Senaryo takip | 4 / 4 / 5 | 4 / **5** / 5 |
| Senaryo konu değişimi | 3 / 3 / 4 | 3 / **4** / 4 |
| Yapay konu değişimi | 57 / 62 / 65 | **59 / 63** / 65 |

- **Prototipteki sayılar gerçek koddan birebir çıktı.**
- **Karar değişmezliği:** 155 aramanın hepsinde (tekil, cevaplanamaz, senaryo ve yapay) en yüksek vektör skoru ve takip kararı iki modda aynı.
- **Kötüleşen sıralama yok.**
- **İyileşenler:**
  - "hangi yılda?": 5. sıradan 3. sıraya.
  - Turan'dan sonra "Kımız nedir?": 30. sıradan 2. sıraya.
  - "Kut nedir?": 4. sıradan 1. sıraya.

#### 4d: Uçtan uca ölçüm

| Ölçüt | 5d (hibrit yok) | Faz 4 (hibrit) |
|---|---|---|
| Tam başarı | %95.6 | **%96.7** |
| hit@1 / hit@3 | %87.8 / %95.9 | **%91.9 / %100** |
| Yanlış red | %2.7 | **%0** |
| Kaynak doğru belge | %98.6 | **%100** |
| Cevaplanamaz soruları reddetme | %100 | **%93.8** |
| Takip / cevapsız takip / konu değişimi | 4/5, 2/2, 3/4 | **5/5**, **1/2**, **4/4** |
| Süre ortalaması | 1.95 sn | 2.08 sn |
| Sonucu değişen soru | — | 3: "hangi yılda?" OK oldu, Turan'dan sonra "Kımız" OK oldu, "ilk başkanı kimdi?" HATA oldu |

**Gözle kontrol** (metni değişen 33 cevap okundu):

| | 5d | Faz 4 |
|---|---|---|
| Yanlış ya da belgeyle çelişen bilgi (cevaplanabilir) | 3: `takip-2` 1928, `kurt-6` Böri, `kurt-4` karışık | 4: `kurt-6`, `kurt-4`, **`gelenek-1`** ("Kut", belge "taht kavgalarına zemin hazırlamıştır" diyor, model "önleme amaçlıyordu" yazıyor), **`ulku-4`** ("1969–1971", belgede 1969–1970) |
| Cevaplanamaz soruya uydurma | 0 | **1:** "Türk Ocağı ne zaman kuruldu?" → "ilk başkanı kimdi?" sorusuna "Mete Han ... ilk büyük Türk devletinin başkanıydı" |

`ulku-4` cevabını otomatik puanlama kaçırıyor: anahtar ifade (1969) cevapta geçiyor.

#### Uydurmanın sebebi

- **Takip kuralı devreye girmedi.** "ilk başkanı kimdi?" tek başına arandı.
- **Mete Han paragrafı 5d'de de 1. sıradaydı.** 5d'de model aynı parçayı görüp soruyu reddetmişti.
- **Değişen tek şey 2. parça.** 5d'de 2. sırada "ilk cumhurbaşkanı" geçen Atatürk paragrafı vardı. Hibrit aramada onun yerine "ilk" kelimesi geçen Uygur paragrafı geldi. "ilk" kelimesi 86 parçanın 14'ünde, "başka*" öneki 10'unda geçiyor.

**Sonuç:** Hibrit arama yanıltıcı yeni bir parça getirmedi. Modelin reddetme kararı bağlamdaki küçük bir değişiklikle değişti. Aynı durum "Kut nedir?" sorusunda da görülüyor: doğru paragraf artık 1. sırada ama model paragrafı ters anlıyor. Modelin bu kararsızlığı Faz 5'te de görülmüştü: sistem komutu değişiklikleri 5a'da 3 soruyu kaybettirmiş, 5b'de uydurma getirmişti.

#### Doğrulama: hibrit kapalı

`HYBRID_SEARCH = False` ile yapılan ölçümde bütün ölçütler 5d ile aynı, sonucu değişen soru yok. Faz 4'teki eşik mantığı değişikliği vektör aramasında davranışı değiştirmiyor.

#### Karar

**Kod ve indeks tutuluyor, hibrit arama varsayılan olarak kapalı** (`HYBRID_SEARCH = False`).

- **Açık olmasının lehine:**
  - Arama ölçütleri açıkça daha iyi, doğru parça her soruda bağlamda.
  - 4 senaryo hatasının 2'si çözülüyor.
  - Otomatik tam başarı daha yüksek.
- **Kapalı olmasının lehine:**
  - Projenin temel vaadi "uydurmama". Gözle kontrolde yanlış bilgi içeren cevap 3'ten 5'e çıktı ve cevaplanamaz bir soruya uydurma geldi.
  - Faz 4'ün "hiçbir kategoride başarı düşmesin" ölçütü karşılanmadı.
- **Veri neden yetersiz:**
  - Cevapsız takip kategorisinde yalnızca 2 soru var.
  - Farklar model davranışındaki küçük değişikliklerden geliyor: 5d'de 3 ve Faz 4'te 5 hatalı cevap, istatistiksel olarak birbirinden ayırt edilemez.

**Karar Faz 5.5'e bırakıldı:** Sonuçları görülmemiş sorularla iki mod karşılaştırılacak. Karar kuralları ölçümden önce Bölüm 6'da yazıldı.

### 2.13 Faz 5.5: kontrol seti

#### Ölçüm öncesi kayıt (sonuçlar görülmeden yazıldı)

- **Kontrol seti:** [eval_set.py](../eval_set.py) içinde `KONTROL_SORULAR` ve `KONTROL_SENARYOLAR`. Parmak izi **`bcc0970ce7`**. Ana set parmak izi `dcda3164d3` değişmedi.
- **İçerik:** 28 tekil soru ve 15 senaryo, puanlanan 43 soru.

| Grup | Sayı |
|---|---|
| Cevaplanabilir tekil, ana sette olmayan bilgiler ve farklı kalıplar ("neyi amaçlıyordu?", "kim, hangi yılda?", "neden önemlidir?", "nasıl sona ermiştir?") | 15 |
| Kısa kavram / özel ad ("Ülüş", "Toy", "Manasçı", "Örtmece", "Asena") | 5 |
| Konuya yakın cevaplanamaz | 8 |
| Takip, cevap belgede var | 4 |
| Takip, cevap belgede yok | 6 |
| Konu değişimi, kısa soru | 3 |
| Konu dışı, önceki sorudan sonra | 2 |

- **Bilerek konan iki tuzak:**
  - "Göktürklerin başkenti neresiydi?" Belgede "Ötüken" yalnızca bir dergi adı olarak geçiyor.
  - "Kurtuluş Savaşı'nda Doğu Cephesi komutanı kimdi?" Belgede Mustafa Kemal'in Birinci Dünya Savaşı'nda Doğu Cephesi'nde görev yaptığı yazıyor.
- **Sınırlama:** Soruları, ana setin sonuçlarını görmüş olan asistan yazdı (proje sahibinin tercihi). Bu yanlılığı azaltmak için:
  - Sorular ölçümden önce donduruldu.
  - Ana sette kullanılmayan bilgiler ve farklı soru kalıpları seçildi.
  - Karar kuralları önceden yazıldı.

  Yine de sonuç, bağımsız birinin yazacağı sorulara göre iyimser olabilir.
- **Karar kuralları:** Bölüm 6, Faz 5.5'te yazıldığı gibi uygulanacak. Sonuçlara göre değiştirilmeyecek.
- **Ölçüm planı:**
  - Temiz sunucuda önce hibrit kapalı (`LRA_HYBRID=0`), sonra hibrit açık (`LRA_HYBRID=1`) ölçülecek.
  - Gözle kontrol, iki modun cevapları karışık sırada ve mod etiketi olmadan yapılacak. Kararlar bir dosyaya yazıldıktan sonra etiketler açılacak.

#### Sonuçlar

**Raporlar:**
- Hibrit kapalı: [2026-09-14_0801_kontrol_hibrit-kapali.md](../degerlendirmeler/2026-09-14_0801_kontrol_hibrit-kapali.md).
- Hibrit açık: [2026-09-14_0804_kontrol_hibrit-acik.md](../degerlendirmeler/2026-09-14_0804_kontrol_hibrit-acik.md).
- Kör inceleme ([kor_inceleme.py](olcum_betikleri/kor_inceleme.py)):
  - [inceleme.md](olcum_betikleri/kontrol_inceleme/inceleme.md): A/B etiketli cevaplar.
  - [kararlar.json](olcum_betikleri/kontrol_inceleme/kararlar.json): etiketler açılmadan yazılan kararlar ve notlar.
  - [eslesme.json](olcum_betikleri/kontrol_inceleme/eslesme.json): A/B ile mod eşleşmesi.

**Otomatik ölçütler** ([kontrol_ozet.py](olcum_betikleri/kontrol_ozet.py)):

| Ölçüt | Ana set (5d, hibrit kapalı) | Kontrol, hibrit kapalı | Kontrol, hibrit açık |
|---|---|---|---|
| Tam başarı | %95.6 | %88.4 | %88.4 |
| hit@1 / hit@3 | %87.8 / %95.9 | %85.2 / %88.9 | %92.6 / %100 |
| Cevaplanabilir sorularda başarı | %94.6 | %88.9 | %96.3 |
| Yanlış red | %2.7 | %7.4 | %0 |
| Kaynak doğru belge | %98.6 | %100 | %100 |
| **Cevaplanamaz soruları reddetme** | %100 | **%87.5** | **%75.0** |
| Süre ortalaması | 1.95 sn | 2.11 sn | 2.12 sn |

| Kategori (kontrol) | Hibrit kapalı | Hibrit açık |
|---|---|---|
| normal (15) | 14 | 14 |
| ozel_ad (5) | 4 | 5 |
| yakın (8) | 7 | 7 |
| takip (4) | 4 | 4 |
| **takip, cevapsız (6)** | **5** | **3** |
| konu değişimi (3) | 2 | 3 |
| konu dışı, önceki sorudan sonra (2) | 2 | 2 |

**Kör inceleme:** 43 sorunun 30'unda iki modun cevabı aynıydı.

| | Hibrit kapalı | Hibrit açık |
|---|---|---|
| Cevaplanabilir (27): doğru | 22 | 23 |
| Cevaplanabilir: yanlış red | 2 ("Ülüş", "Otağ") | 0 |
| **Cevaplanabilir: yanlış ya da çelişkili bilgi** | **3** | **4** |
| Cevaplanamaz (16): doğru red | 14 | 12 |
| **Cevaplanamaz: uydurma** | **2** | **4** |

**İki modda da hatalı olan cevaplar:**
- `k-harf-sayisi`: "yirmi dokudan altı harf" diye harf sayısını yanlış veriyor.
- `k-toy`: İlk cümle doğru, ardından **Çince metin** ve "toy kurdun eski adı" gibi yanlış bir ifade geliyor. **Otomatik puanlama bunu kaçırdı**, çünkü anahtar ifade (meclis) cevapta geçiyor.
- `k-degisim-tugrul`: Hibrit kapalıda "Alparslan döneminde akınlara öncülük etti", hibrit açıkta "Alparslan'ın babasıdır" yazıyor. İkisi de yanlış. **Otomatik puanlama bunu da kaçırdı** (anahtar ifade: sultan).
- **Uydurma, `k-dogu-cephesi` (tuzak tuttu):** Model, Birinci Dünya Savaşı'ndaki Doğu Cephesi görevini Kurtuluş Savaşı komutanı gibi sundu. Skor 0.662.
- **Uydurma, `k-cevapsiz-uygur`:** Uygur Kağanlığı'ndan sonra "ne zaman yıkıldı?" diye sorulunca model Osmanlı'nın yıkılışını anlattı. Takip kuralı devreye girmedi, çünkü birleşik arama yeterince yüksek skor vermedi. Skor 0.435.

**Yalnızca hibrit açıkta görülen uydurmalar:**
- `k-cevapsiz-mohac`: "IV. Romanos Diogenes karşı taraftaki kraldı".
- `k-cevapsiz-baskent` (ikinci tuzak): Göktürklerin başkenti sorulunca "Anadolu Selçuklu'nun başkenti Konya" diye cevap verdi.

#### Karar kurallarının uygulanması

| Kural | Ölçülen | Sonuç |
|---|---|---|
| 1a. Kontrol setinde tam başarı ≥ %85.6 (hibrit kapalı) | %88.4 | ✅ Karşılandı |
| 1b. Cevaplanamaz soruları reddetme ≥ %90 (hibrit kapalı) | %87.5 (16'da 14) | ❌ **C yaklaşımı yeniden değerlendirilmeli** |
| 2.1 Hibrit arama: uydurma artmamalı | Kapalı 2, açık 4 | ❌ |
| 2.2 Hibrit arama: yanlış bilgi en fazla +1 | Kapalı 3, açık 4 | ✅ |
| 2.3 Hibrit arama: tam başarı düşmemeli | %88.4 = %88.4 | ✅ |
| 3. Ana set ile aynı yönde mi? | Ana sette yanlış bilgi 3 → 5 (uydurma 0 → 1), kontrolde uydurma 2 → 4 | Aynı yönde, bu bir eğilim |

#### Kararlar

1. **Hibrit arama kapalı kalıyor.** Kural 2.1 sağlanmadı ve ana setteki eğilim kontrol setinde de görüldü. Hibrit arama aramayı iyileştiriyor (hit@3 %100), ama modele daha fazla konuyla ilişkili ve yanıltıcı olabilecek paragraf veriyor. Model de bu durumda daha sık uyduruyor. Kod ve indeks duruyor. Model değişirse ya da bir cevap doğrulama adımı eklenirse yeniden değerlendirilmeli.
2. **Kural 1b tetiklendi: reddetme kararının tamamen modelde olması, sonuçları görülmemiş sorularda yeterince güvenilir değil.**
   - Eşik bu soruları ayıramıyor: skorlar 0.662 ve 0.435. Faz 3'teki A yaklaşımının neden elendiği burada da geçerli.
   - Sorunun iki biçimi var:
     1. **Konuya yakın tuzak:** Bağlamda benzer ama farklı bir olay var, model onu cevap gibi sunuyor.
     2. **Takip kuralının yakalayamadığı eksik takip sorusu:** Soru tek başına başka bir konuyla eşleşiyor, model o konuyu cevaplıyor.
   - Önerilen yol: Faz 5.6 (Bölüm 6).
3. **Genelleşme kısmen sağlandı.** Tam başarı eşiğin üstünde, ama gözle kontrolde cevaplanabilir sorularda yanlış bilgi oranı ana sette %4.1'di, kontrol setinde %11.1 (27'de 3). Farklı soru kalıplarında ("neden?", "nasıl?", "kim, hangi yılda?") model daha fazla hata yapıyor.
4. **Otomatik puanlamanın iki kör noktası belirlendi:**
   - Cevapta Türkçe olmayan yazı (Çince).
   - Anahtar ifade geçtiği halde cevabın geri kalanının yanlış olması.

   Birincisi kodla yakalanabilir (H12). İkincisi için gözle kontrol gerekmeye devam ediyor.

> **Önemli:** Kontrol setinin sonuçları artık görüldü. Faz 5.6'da bu setteki hatalara bakılarak yapılacak her değişiklik, bu seti de "görülmüş" hale getirir. Bu yüzden bundan sonraki son doğrulama, **proje sahibinin bağımsız testiyle** yapılmalı. Temiz kalan tek kontrol verisi bu.

### 2.14 Faz 5.6 sonuçları: uydurma koruması

#### H12: Türkçe olmayan yazı koruması — kabul

- **Nasıl çalışıyor** ([rag.py](../rag.py) `cut_foreign_script`): Cevapta Çince, Japonca ya da Korece karakter varsa cevap, bu karakterlerden önce biten son tam cümlede kesiliyor. Geriye 20 karakterden kısa bir metin kalırsa soru reddediliyor.
- **Değerlendirme:** [evaluate.py](../evaluate.py) artık bu karakterleri içeren cevabı hata sayıyor ve `Türkçe olmayan yazı` olarak raporluyor.
- **Modelsiz sınama** ([yabanci_yazi_kontrol.py](olcum_betikleri/yabanci_yazi_kontrol.py)):
  - Kayıtlı 1586 cevabın yalnızca 2'sinde bu karakterler var. İkisi de kontrol setindeki "Toy nedir?" sorusu, biri hibrit kapalı, biri açık çalıştırmadan.
  - Kesildikten sonra doğru cümle kalıyor: "Toy, devletin önemli kararlarının alındığı meclisdir."
  - Birim testler iki hata yakaladı ve ikisi de düzeltildi: "19." gibi sıra sayıları cümle sonu sanılıyordu, tırnakla biten cümleler de tanınmıyordu.
- **Uçtan uca ölçüm ayrıca yapılmadı.** Koruma cevap üretimini değiştirmiyor, yalnızca ürettikten sonra kesiyor. Etkisi kayıtlı cevaplarda birebir görülüyor. H13 ölçümlerinde de "Toy nedir?" doğru kesildi.

#### H13: Cevap doğrulama adımı — reddedildi (iki varyant)

**Nasıl çalışıyor** ([rag.py](../rag.py) `verify_answer`):
- Cevap üretildikten sonra aynı modele kısa bir ikinci istek gönderiliyor, model yalnızca EVET ya da HAYIR diyor. HAYIR ise sistem reddediyor.
- Önceki soru yalnızca doğrulayıcıya gösteriliyor. Doğrulayıcı sadece reddedebildiği için Faz 5b'deki uydurma riski burada yok.
- Aç/kapat: `ANSWER_VERIFICATION` (`LRA_VERIFY`). Talimat: `LRA_VERIFY_PROMPT` (`genis` ya da `dar`).

**Ölçümler** (temiz sunucuda; doğrulamasız karşılaştırma noktaları: ana set 0709, kontrol seti 0801):

| | Ana set: tam başarı | Ana set: doğrulamada reddedilen cevaplanabilir | Kontrol: tam başarı | Kontrol: uydurma | Kontrol: doğrulamada reddedilen cevaplanabilir | Süre |
|---|---|---|---|---|---|---|
| Doğrulama yok | %95.6 | — | %88.4 | 2 | — | 2.0 / 2.1 sn |
| **Geniş talimat** (3 HAYIR koşulu) | %84.4 | 12 | %90.7 | **0** | 2 | 2.8 sn |
| **Dar talimat** (varsayılan EVET, yalnızca kişi/olay/dönem uyuşmazlığında HAYIR) | %87.8 | 10 | %86.0 | **0** | 4 | 2.7 sn |

Raporlar:
- Geniş talimat: [ana](../degerlendirmeler/2026-09-14_1949_faz56-dogrulama.md), [kontrol](../degerlendirmeler/2026-09-14_1955_kontrol_faz56-dogrulama.md).
- Dar talimat: [ana](../degerlendirmeler/2026-09-14_2000_faz56b-dar-dogrulama.md), [kontrol](../degerlendirmeler/2026-09-14_2006_kontrol_faz56b-dar-dogrulama.md).

**Doğrulayıcının reddettiği cevapların incelemesi** ([dogrulama_inceleme.py](olcum_betikleri/dogrulama_inceleme.py)):

| | Geniş | Dar |
|---|---|---|
| Yanlış ya da uydurma cevabı yakaladı | 5 ("Böri", "1928", harf sayısı, Doğu Cephesi, Uygur) | 5 (aynıları) |
| **Doğru cevabı reddetti** | **11** (örnekler: "Çanakkale Deniz Zaferi 18 Mart 1915'te kazanılmıştır", "fatih kimdir", "sonucu ne oldu?", "Atlı okçuluk") | **10** (örnekler: "Çanakkale", "Ergenekon bahar bayramı", "Asena", "kurdun neden seçildiği") |

**Kabul ölçütüne göre** (Bölüm 6, ölçümden önce yazıldı):
- Uydurma azaldı (2 → 0) ✅
- Süre ≤ 3 sn ✅
- **Yanlış red iki sette toplam en fazla 2 artmalıydı: geniş talimatta 14, dar talimatta 12 arttı ❌**

**Sonuç:**
- **Doğrulama fikri işe yarıyor:** İki talimat da gözle bulunan bütün kötü cevapları yakaladı.
- **Ama qwen2.5-7b EVET/HAYIR kararını güvenilir veremiyor.** Bağlamda harfi harfine yazan cevapları bile iki talimatta da rastgele reddediyor. Talimat değişikliği yanlış red sayısını yalnızca 11'den 10'a indirdi.
- **Kod duruyor, `ANSWER_VERIFICATION = False`.** Daha güçlü bir doğrulayıcı modelle yeniden değerlendirilmeli. Bu donanımda iki büyük model birlikte belleğe sığmıyor.

**Sınırlama:** Dar talimat, iki setin sonuçları görüldükten sonra tasarlandı. Reddedildiği için sonuçları etkilemedi.

#### Faz 5.6'dan sonraki durum

**Varsayılan yapılandırma** (değişmedi, yalnızca H12 eklendi):
- qwen2.5-7b, paragraf parçalama, Türkçe sorgu talimatı.
- Eşik 0.33, takip farkı 0.20, `TOP_K = 3`.
- Kaynağı kod belirliyor.
- Hibrit arama kapalı, cevap doğrulama kapalı.
- Türkçe olmayan yazı koruması açık.

| | Ana set (105 soru, ayar yapılan) | Kontrol seti (43 soru, sonuçları görülmüş) |
|---|---|---|
| Otomatik tam başarı | %95.6 | %88.4 |
| Gözle: yanlış ya da çelişkili bilgi (cevaplanabilir) | 3 / 74 (%4.1) | 2 / 27 ("Toy" düzeldi; harf sayısı, Tuğrul Bey kaldı) |
| Gözle: uydurma (cevaplanamaz) | 0 / 16 | **2 / 16** |
| Süre ortalaması | 2.0 sn | 2.1 sn |

**Değerlendirme:**
- Arama, kaynak gösterme, hız ve yanlış red hedefte.
- **Kalan zayıflık uydurma:** Konuya yakın tuzak sorular ve takip kuralının yakalamadığı eksik takip soruları. Bu, qwen2.5-7b modelinin bu donanımdaki sınırından geliyor.
- Eşik (Faz 3), sistem komutu (Faz 5a, 5b), bağlam boyutu (5c), hibrit arama (Faz 4) ve doğrulayıcı (5.6) ile denendi. Hiçbiri başka bir şeyi bozmadan çözemedi.
- Aynı setler üzerinde denemeye devam etmek, bu sorulara uyum sağlamak olur. **Bir sonraki karar, proje sahibinin bağımsız testiyle alınmalı.**

---

## 3. Genel çıkarımlar

### 3.1 Belge biçimi
- Belgeler RAG için uygun: Her paragraf tek bir alt konuyu anlatıyor ve tek başına anlaşılıyor.
- **Konu başına bir dosya doğru yöntem, tek dosyaya geçilmemeli.** Kaynak gösterme bu ayrıma dayanıyor.
- Aramayı dosya sayısı değil **parça birimi** belirliyor. Doğru birim, başlığı eklenmiş tek paragraf.

### 3.2 Konu yelpazesi
- 7.500 token'lık bir veri seti RAG için çok küçük. Genişlik bir sorun değil.
- Asıl dikkat edilmesi gereken **konuların benzerliği**. Bu, eşik ve sıralama kararlarını zorlaştırıyor.

### 3.3 Mimari: iyileştirme nerede aranmalı?
RAG iki adımdan oluşur: arama ve üretim. Yerel çalıştırmada bunlara modelin donanımda çalışma katmanı ekleniyor:

| Adım | Belirlediği şey | Mevcut sorun | İyileştirme maliyeti |
|---|---|---|---|
| Arama | Doğru bilgi modele ulaşıyor mu? | Eşik, parçalama, sorgu biçimi, takip sorularında eşiğin atlanması | Düşük, ölçülebilir, kalıcı |
| Üretim | Model bilgiyi sadık kalarak okuyor mu? | Yanlış kaynak, takip sorularında eksik bağlam, uydurma (özellikle 4B) | Bir kısmı kodla (kaynak, takip sorusu), bir kısmı model seçimiyle çözülür |
| Çalıştırma | Model donanımda verimli çalışıyor mu? | Çözüldü: bellek yükleme sırası (Bölüm 2.5) | — |

**Sonuç:** "Maharet ayarlarda" görüşü arama katmanı için büyük ölçüde doğru ve öncelik oraya verilmeli. Ama modelin bir alt sınırı var. Doğru bağlamı verdiğimiz halde yanlış cevap veren modeli ayarlarla düzeltemeyiz.

### 3.4 Donanım
RTX 5070 (8 GB) bu proje için yeterli: qwen2.5-7b ve gömme modeli birlikte ~2.3 sn'de cevap veriyor. Ama bellek sınırda. Ekran da bu karta bağlı olduğu için masaüstü ve tarayıcılar aynı belleği paylaşıyor. Bellek dolduğunda sürücü hata vermek yerine sessizce yavaşlıyor, bu yüzden belleğin **nasıl** dolduğu en az modelin boyutu kadar önemli (Bölüm 2.5).

---

## 4. Olası hamleler

Her hamle **tek başına** uygulanıp ölçülmeli.

| # | Hamle | Beklenen etki | Nasıl ölçülür | Risk |
|---|---|---|---|---|
| H1 ✅ | Paragraf düzeyinde parçalama, başlık öneki, karakter örtüşmesini kaldırma | Karışık parçalar biter, özel adlarda sıralama iyileşir. **Ölçüldü:** hit@1 +12 puan, tam başarı +9 puan (Bölüm 2.8) | Doğru parçanın sırası (hit@1, hit@3) | Çok kısa paragraflar bağlamsız kalabilir. **Gerçekleşti:** Orhun/Thomsen sorusu (Bölüm 2.8, 4. bulgu) |
| H1b (beklemede) | Bağlamı önceki paragrafta kalan paragrafa komşu bağlam eklemek. Faz 2'den sonra hedeflediği iki soru çözüldü, şimdilik gerekli değil. Seçenekler: (a) aramada kullanılan metne önceki paragrafın ilk cümlesini eklemek, (b) modele giden bağlama önceki paragrafı da vermek | "Yazıtların dili..." gibi paragraflar doğru soruda üst sıraya çıkar ya da model gerekli bağlamı görür | `ilkturk-1`, `takip-2`, `isimler-5` ve genel hit@1 | Parçalar yeniden karışır, H1'in kazancı azalabilir. (b) seçeneği aramayı değiştirmez, sadece modele giden bağlamı büyütür |
| H2 ✅ | Qwen3-Embedding sorgu talimatı (yalnızca sorguya, belgelere değil) | Zayıf eşleşen sorularda skor artışı. **Ölçüldü:** Türkçe talimatla tam başarı +9 puan, hit@1 +4 puan. İngilizce talimat hit@1'i 7 puan düşürdü (Bölüm 2.9) | hit@1, skor dağılımı | Bazı sorularda sıra düşebilir. **Gerçekleşti:** Talimat bütün skorları yükseltiyor, eşiğe dayalı takip sorusu kuralı zayıflıyor (H10) |
| H3 ✅ | Eşiğin yeniden ayarlanması | Yanlış "yok" cevaplarının azalması. **Ölçüldü:** 0.42 → 0.33, yanlış red %4.1 → %2.7 (Bölüm 2.10) | Yanlış red oranı, cevaplanamaz soruları reddetme oranı | Eşik düşerse alakasız sorular modele gider. **Gerçekleşti:** Cevaplanamaz soruların %87.5'ini artık model reddediyor, model değişirse yeniden ölçülmeli |
| H4 (uygulandı, varsayılan kapalı) | Hibrit arama: SQLite FTS5 (anahtar kelime) + vektör. **Uçtan uca:** hit@3 %100, tam başarı %96.7, ama gözle kontrolde yanlış bilgi 3'ten 5'e çıktı. Karar Faz 5.5'te (Bölüm 2.12) | "böri", "kımız", "Aşina" gibi özel adlarda güvenilir eşleşme. **Prototip:** 5 harflik önekle hit@1 58 → 61/65, özel ad 10/10, kötüleşme yok (Bölüm 2.11) | hit@1, özellikle özel ad soruları | Türkçe eklerde kelime eşleşmesi zayıflayabilir. **Gerçekleşti:** Tam kelime araması "Orhun alfabesi" sorusunu 3. sıradan 9–14. sıraya düşürdü, önekli aramada bu görülmedi |
| H5 ✅ | Kaynak satırını modele değil koda yazdırmak. **Uygulandı:** Cevabın parçalarla örtüşmesine göre (`pick_source`). Red cevabına kaynak eklenmesi 6'dan 0'a, doğru kaynak %98.6 (Bölüm 2.11) | Kaynak her cevapta ve doğru olur. Testte model yanlış belgeyi gösterdi ve reddetme cevabına da kaynak ekledi | Kaynaklı cevap oranı, doğru kaynak oranı | Model reddettiğinde kaynak eklenmemeli. Hangi parçanın kullanıldığını kodun bilmesi gerekir (örneğin modelden parça numarası istemek) |
| H6 ✗ (`TOP_K = 5` reddedildi) | `TOP_K` ve bağlam uzunluğunu ayarlamak. **Ölçüldü:** `TOP_K = 5` ile başarı %93.3 → %90.0, süre 1.75 → 7.0 sn (Bölüm 2.11) | Daha az dikkat dağınıklığı. Hız artık sorun değil (bağlam okuma ~0.5 sn) | Doğruluk | Çok kısa bağlam cevabı eksik bırakabilir |
| H7 ✅ (qwen2.5-7b kalıyor) | Sohbet modelini yeniden seçmek (qwen2.5-7b, qwen3-4b, gerekirse qwen3-8b). **Ölçüldü:** Aynı 62 soruda qwen3-4b 52, qwen2.5-7b 60 başarı. qwen3-4b Foundry'yi çökertti (Bölüm 2.11) | Daha az uydurma. İki model aynı hızda olduğu için seçim doğruluğa göre yapılır | Uydurma oranı, kaynak oranı | Model değişince sistem komutunun ve bellek eşiklerinin (Bölüm 2.5) yeniden ayarlanması gerekir |
| H8 (uygulanmadı) | Sistem komutunu sıkılaştırmak ("bağlamda olmayan tarih, yer ve ad yazma"). Faz 5'te model sistem komutu değişikliklerine çok hassas çıktı, hedefleyebileceği 1–2 hata kaldı | Uydurmanın azalması, özellikle küçük modelde | Uydurma oranı | Aşırı katı komut, gereksiz reddetmeye yol açabilir |
| H9 ✗ (reddedildi) | Takip sorusunda önceki soruyu modele de iletmek ya da soruyu tek başına anlaşılır hale getirmek ("hangi yılda?" → "Orhun alfabesi hangi yılda çözüldü?"). **Ölçüldü:** Önceki soruyu "devamıdır" yönlendirmesiyle göstermek uydurma getirdi, cevaplanamaz soruları reddetme %100 → %87.5 (Bölüm 2.11) | Takip sorularında doğru cevap | Takip sorusu senaryolarında doğruluk | Konu değiştiğinde önceki soru modeli yanıltabilir. **Gerçekleşti.** Soruyu yeniden yazma seçeneği denenmedi; ek model çağrısı ve aynı uydurma riski taşıyor |
| H10 ✅ (kısmen) | Takip sorularında eşik korumasını geri getirmek ve konu değişiminde yanlış birleştirmeyi önlemek. **Uygulandı:** Birleşik arama, skoru tek başına aramadan en az 0.20 yüksekse kullanılıyor. Takip 3/5 → 4/5. Konu dışı soruyu eşikte reddetme hedefi skorla gerçekleştirilemedi, bunları model reddediyor (Bölüm 2.10) | Konu dışı sorular modele gitmeden reddedilir. Kısa bir kavram sorusu önceki soruyla birleşip yanlış parçaya kaymaz (Bölüm 2.7, 4. bulgu: "Tuğ nedir?" 2. sıradan 14. sıraya düştü) | `konu_disi_sonra` ve `konu_degisimi` kategorileri | **Skorla ayırmak bu veride mümkün değil** (Bölüm 2.6, 4. bulgu). Farklı bir işaret gerekir: takip sorusunu kısa ve zamir/soru ekiyle başlayan sorularla sınırlamak ("bunun", "hangi yılda?"), ya da H9'daki yeniden yazılmış soruyu tek başına aramak. Aksi halde B yaklaşımı (red kararı modelde) fiilen uygulanmış olur |
| H11 | Açılışta gömme modelini de hızlı bellekte tutmak (örneğin sıra: sohbet modelini yükle → gömme modelini yükle ve çalıştır → uzun ısıtma istemi) | Arama 200 ms'den ~30 ms'ye iner, takip sorularında ~0.4 sn kazanç | [gomme_hizi.py](olcum_betikleri/gomme_hizi.py), `arama_ortalama` ölçütü | Sohbet modelinin hızını bozabilir. [hiz_teshis.py](olcum_betikleri/hiz_teshis.py) S4 senaryosu bu sıranın sohbet modeli için sorunsuz olduğunu gösterdi, ama gömme süresi o testte ölçülmedi. İkisi birlikte ölçülmeli |

### Karar verildi: Eşik nasıl kullanılmalı? → C (Faz 3, Bölüm 2.10)

> **Karar:** C yaklaşımı seçildi. Eşik 0.33 bir güvenlik tabanı olarak açıkça konu dışı soruları ayıklıyor, konuya yakın cevaplanamaz soruları model reddediyor.
> A yaklaşımı elendi: Konuya yakın cevaplanamaz sorular 0.52–0.69 skor alıyor. Hepsini eşikte reddetmek için eşik 0.70 olmalı, bu da 38 cevaplanabilir soruyu kaybettirir.

Karar öncesi karşılaştırma:

| Yaklaşım | Artısı | Eksisi |
|---|---|---|
| **A. Sabit eşik, veriyle yeniden ayarlanmış** | Basit, alakasız soru modele hiç gitmez, hızlı red | Konuları yakın belgelerde kırılgan |
| **B. Düşük eşik, reddetme kararı modelde** | Yanlış red azalır. Model "Fatih'in annesi" sorusunu ve eşiği atlayan 3 konu dışı soruyu doğru reddetti | Uydurma riski modele geçer, her soru modele gider (~2 sn, eşikte red ~0.2 sn) |
| **C. İki kademe:** çok düşük skorda hemen red, arada modele bırak | A ile B'nin dengesi | İki eşik ayarlamak gerekir |

---

## 5. Deneme yöntemi

1. **Önce ölç.** Değişiklikten önce mevcut sistemin sonuçları kaydedilmeli.
2. **Her seferinde tek değişiklik.** İki değişiklik birlikte yapılırsa hangisinin etkili olduğu anlaşılamaz.
3. **Hep aynı soru seti ve ayarlar.** `temperature = 0` sabit kalmalı.
4. **Sonuçlar tarihli dosyalara yazılmalı.** Sonuçlar karşılaştırılabilir kalmalı. `eval_results.md` her çalıştırmada üzerine yazılmamalı.
5. **Cevaplar gözle de kontrol edilmeli.** "Doğru belge getirildi" ile "cevap doğru" aynı şey değil.
6. **Tek sorudaki değişim gürültü olabilir.** Aynı ayarlarla iki çalıştırmada 105 cevabın 2'si farklı çıktı (Bölüm 2.7). Bir değişikliği birden fazla sorudaki etkisine bakarak değerlendirmek gerekiyor.
7. **Beklentileri sonuçlara göre gevşetmemek.** Bir sorunun beklentisi gerçekten yanlışsa düzeltilir, ama nedeni dokümana yazılır. Soru seti değişirse `--karsilastir` uyarı verir. Bu durumda başlangıç ölçümü yeni setle tekrar alınmalı.

**Standart komutlar** (`lra` klasöründe):

```
python evaluate.py --kontrol                                  # set geçerli mi (modelsiz, saniyeler)
python evaluate.py --etiket faz1-paragraf --karsilastir degerlendirmeler/2026-09-14_0351_baslangic.json
```

> `evaluate.py` modelleri kullanır. **Ölçüm sırasında Streamlit ve masaüstü uygulaması kullanılmamalı.** Faz 2'nin ilk ölçümünde süreler ortada bozuldu, en olası sebep eşzamanlı istekti (Bölüm 2.9). Süre ölçütleri önemliyse önce `foundry server stop` çalıştırılmalı. Rapor, ilk token ortalaması 3 sn'yi aşarsa uyarı veriyor.

---

## 6. Uygulama planı

### Faz 0: Ölçüm altyapısı ve başlangıç ölçümü ✅ (14.09.2026)

**Amaç:** Her sonraki değişikliği sayıyla değerlendirebilmek.

- [x] Ölçüm betiklerini projeye taşımak ([olcum_betikleri/](olcum_betikleri/)).
- [x] Test setini genişletmek ([eval_set.py](../eval_set.py)):
  - [x] 13 belgenin hepsinden, farklı paragraflara dağılmış 4–6 soru (toplam 65 cevaplanabilir).
  - [x] Her soru için beklenen belge, beklenen paragraf (kanıt ifadesi) ve anahtar ifadeler. Bilinen yanlışlar için yasak ifadeler.
  - [x] Özel ad ve kısa kavram soruları (10 soru, `ozel_ad` kategorisi).
  - [x] 10 cevaplanamaz soru: 6 konuya yakın, 3 konu dışı, 1 anlamsız.
  - [x] Ard arda soru senaryoları: 5 takip, 2 cevapsız takip, 4 konu değişimi.
  - [x] Konu dışı soruların bir önceki sorudan sonra sorulması (4 senaryo).
- [x] [evaluate.py](../evaluate.py) ölçütlerini genişletmek: hit@1, hit@3, MRR, doğru parçanın sırası, yanlış red (eşikte / modelde), anahtar ifade, yasak ifade, kaynağın doğru belge olması, red cevabında kaynak satırı, ilk token süresi, arama süresi, toplam süre. Ayrıca kategori kırılımı.
- [x] Sonuçlar tarihli dosyalara yazılıyor (`degerlendirmeler/`). `eval_results.md` dosyasına dokunulmuyor.
- [x] Çalıştırmalar arası karşılaştırma (`--karsilastir`), modelsiz set doğrulaması (`--kontrol`), rapordan yeniden üretim (`--rapor`).
- [x] Değerlendirmenin arayüzlerle aynı kod yolunu ölçmesi için `rag.answer_details()` ve `rag.follow_up_query()` eklendi.
- [x] Başlangıç ölçümü alındı ve tekrarlanabilirliği doğrulandı (Bölüm 2.7).

**Çıktı:** [2026-09-14_0351_baslangic.md](../degerlendirmeler/2026-09-14_0351_baslangic.md). Bundan sonraki her faz bu dosyaya karşı karşılaştırılır.

**Faz 0'ın sonraki fazlara etkisi:**
- **Faz 1 ve Faz 2** en çok `ozel_ad` kategorisini ve ilk 3'e girmeyen 6 yanlış redi etkilemeli.
- **Faz 3'ün başarı ölçütü şu an çok uzakta:** yanlış red %20.3, hedef ≤ %5. Ayrıca cevaplanamaz soruların çoğu eşiği geçiyor (Bölüm 2.7, 3. bulgu). Eşik kararı bu verilerle verilmeli.
- **Faz 1'de dikkat:** Paragraf parçalama `isimler-5` gibi, bilginin iki paragrafa bölündüğü soruları kötüleştirebilir.

### Faz 1: Parçalama (H1) ✅ (14.09.2026)

- [x] [ingest.py](../ingest.py): Paragraf başına bir parça, başına başlık yolu (belge başlığı ve alt başlık), karakter örtüşmesi yok.
- [x] Çok uzun paragrafları cümle sınırından bölmek (1000 karakter üstü; şu anki belgelerde gerekmedi).
- [x] `ingest.py` ve `embed.py` ile veritabanını yeniden oluşturmak (53 → 86 parça). Önceki veritabanı: `knowledge_faz0_yedek.db`.
- [x] Faz 0 setiyle ölçüp başlangıçla karşılaştırmak ([rapor](../degerlendirmeler/2026-09-14_0418_faz1-paragraf.md)).

**Başarı ölçütü:** hit@1 başlangıçtaki %68.9'dan yükselmeli, hit@3 %87.8'in altına düşmemeli, kelime ortasından başlayan parça kalmamalı.
**Sonuç:** ✅ hit@1 %81.1, hit@3 %93.2, kelime ortasından başlayan parça yok.

> Parçalama değişince `python evaluate.py --kontrol` tekrar çalıştırılmalı. Kanıt ifadeleri yeni parçalara sığmıyorsa set değil, parçalama sorunludur.

**Geri dönmek gerekirse:** `ingest.py` değişikliği geri alınır ve `knowledge_faz0_yedek.db` dosyası `knowledge.db` olarak kopyalanır.

**Bundan sonraki karşılaştırma noktası:** [2026-09-14_0418_faz1-paragraf.json](../degerlendirmeler/2026-09-14_0418_faz1-paragraf.json). Faz 2 bununla karşılaştırılmalı. Başlangıçla karşılaştırmak toplam ilerlemeyi gösterir.

### Faz 2: Sorgu talimatı (H2) ✅ (14.09.2026)

- [x] [search.py](../search.py): Yalnızca sorgu vektörüne talimat eklemek. Belge vektörleri değişmedi.
- [x] Ölçmek, sırası düşen soruları incelemek. İngilizce talimat reddedildi. 5 talimat biçimi yalnızca aramayla karşılaştırıldı ve Türkçe talimat seçildi ([talimat_arama.py](olcum_betikleri/talimat_arama.py)).
- [x] Türkçe talimatla uçtan uca ölçüm ([rapor](../degerlendirmeler/2026-09-14_0505_faz2b-turkce-talimat.md)).

**Başarı ölçütü:** hit@1 Faz 1'e göre (%81.1) düşmemeli, zayıf sorularda skor artmalı.
**Sonuç:** ✅ hit@1 %85.1. Faz 1'de eşikte reddedilen 8 sorunun 7'si eşiği geçti. Kalan tek eşikte red "Kımız nedir?" (skor 0.346).

**Bundan sonraki karşılaştırma noktası:** [2026-09-14_0505_faz2b-turkce-talimat.json](../degerlendirmeler/2026-09-14_0505_faz2b-turkce-talimat.json).

> **Faz 1'den sonra dikkat:** Bölüm 2.4'teki talimat analizi eski parçalamayla yapılmıştı. "Paragraf + talimat" sütununda 3 soru 1. sıradan 2. sıraya düşüyordu. Bu yüzden kazanç bekleniyor ama garanti değil. Ayrıca talimat skor dağılımını da değiştirecek, bu da Faz 3'teki eşik ayarını etkiler.

### Faz 3: Eşik kalibrasyonu (H3) ve karar noktası ✅ (14.09.2026)

- [x] Faz 2 sonrası test setinde iki skor dağılımını çıkarmak: cevaplanabilir ve cevaplanamaz sorularda en iyi skor ([esik_takip_analiz.py](olcum_betikleri/esik_takip_analiz.py)).
- [x] Bölüm 4'teki A, B ve C yaklaşımlarını aynı setle karşılaştırmak. A veride mümkün değil, B ile C arasındaki fark güvenlik tabanında (Bölüm 2.10).
- [x] Takip sorularında eşik atlanmasını ve takip kuralının zayıflamasını düzeltmek (H10). Takip kuralı skor farkına bağlandı. Konu dışı soruyu eşikte reddetme hedefi skorla gerçekleştirilemedi, model reddediyor.
- [x] **Karar:** C yaklaşımı. Eşik 0.33, takip farkı 0.20.

**Başarı ölçütü:** Yanlış red ≤ %5, cevaplanamaz soruları reddetme %100 (önceki bir sorudan sonra sorulduğunda da).
**Sonuç:** ✅ Yanlış red %2.7, cevaplanamaz soruları reddetme %100 (senaryolarda da).

**Bundan sonraki karşılaştırma noktası:** [2026-09-14_0530_faz3b-esik-033.json](../degerlendirmeler/2026-09-14_0530_faz3b-esik-033.json).

> **Faz 4 için karar notu:** Faz 4'ün koşulu "özel adlı sorularda hâlâ kaçırma varsa". Faz 3'ten sonra `ozel_ad` kategorisinde 10 sorudan 9'u başarılı, tek kaçırma "Kut nedir?" (4. sıra). Kalan 11 hatanın 7'sini H5, 1'ini H9 çözüyor (Bölüm 2.10). **Öneri:** Faz 4'ü şimdilik atlayıp Faz 5'e geçmek. Faz 5.5'teki kontrol seti özel adlarda kaçırma gösterirse Faz 4'e dönülür.

> **Faz 1'den sonra durum:**
> - Yanlış red %16.2. Eşikte reddedilen 8 sorunun hepsinde doğru parça 1. ya da 2. sırada, skorları 0.336–0.420 arasında (Bölüm 2.8, 2. bulgu).
> - Cevaplanamaz soruların tamamı reddediliyor, ama bunun %69'u modelde oluyor.
> - Eşik düşürülecekse bu yük modele daha da fazla geçer. Kararı C yaklaşımı (iki kademe) yönünde veriyle desteklemek gerekiyor.
>
> **Faz 2'den sonra durum:**
> - Yanlış red %5.4 (4 soru), bunun sadece 1'i eşikte. Başarı ölçütüne (≤ %5) çok yakın. Talimat skorları yükselttiği için 0.42 fiilen daha gevşek bir eşik haline geldi.
> - Cevaplanamaz soruları reddetme %100, ama bunun sadece %25'i eşikte.
> - **Faz 3'ün asıl işi artık iki şey:**
>   1. Eşiğin cevaplanamaz soruları modele göndermeden ayırıp ayıramayacağı. Yalnızca aramayla yapılan ölçümde 10 cevaplanamaz tekil sorudan 6'sı 0.42'yi geçiyor ve ayrım değeri (AUC) 0.80 (Bölüm 2.9).
>   2. Takip sorusu kuralı (H10). Talimattan sonra kısa takip soruları da eşiği geçiyor, bu yüzden önceki soru devreye girmiyor.
> - **Eşik ayarı talimat açıkken yapılmalı.** Talimat değişirse eşik yeniden ayarlanmalı.

### Faz 4: Hibrit arama (H4) — uygulandı, varsayılan kapalı (14.09.2026)

> **Sonuç (Bölüm 2.12):**
> - 4a–4d tamamlandı.
> - Özel ad hit@1 %100 ✅, hit@1 %91.9 ✅, tam başarı %96.7 ✅.
> - **"Hiçbir kategoride başarı düşmesin" ölçütü ❌:** Cevapsız takip kategorisi 2/2'den 1/2'ye düştü. Gözle kontrolde de yanlış bilgi içeren cevap 3'ten 5'e çıktı.
> - `HYBRID_SEARCH = False` ile tutuluyor. Açılıp açılmayacağına Faz 5.5 karar verecek.

Aşağıdaki plan uygulama öncesinde yazıldı ve olduğu gibi bırakıldı:

**Koşul:** Faz 1–3 sonrasında özel adlı sorularda hâlâ kaçırma varsa uygulanır.
**Durum:**
- Faz 5'ten sonra özel adlarda 1 kaçırma kaldı ("Kut nedir?").
- Modelsiz prototip ([hibrit_prototip.py](olcum_betikleri/hibrit_prototip.py)) 5 harflik önekli hibrit aramanın hit@1'i 58/65'ten 61/65'e çıkardığını, özel adlarda 10/10'a ulaştığını ve hiçbir soruyu kötüleştirmediğini gösterdi (Bölüm 2.11).
- Koşul karşılanıyor ve risk düşük görünüyor.

**Uygulama adımları:**
- [x] Prototip: FTS5 + vektör, Reciprocal Rank Fusion, tam kelime ve önek karşılaştırması (Bölüm 2.11).
- [x] **4a** [ingest.py](../ingest.py): `chunks` tablosunun yanında FTS5 tablosu oluşturmak. Metin Türkçe küçük harfe çevrilmeli (İ/I sorunu), `unicode61` tokenizer kullanılmalı.
- [x] **4b** [search.py](../search.py):
  - Sorudan soru kelimelerini ("nedir", "hangi"...) çıkarıp 5 harflik önekle kelime araması yapmak.
  - Vektör sırasıyla RRF (`k = 60`) birleştirmek.
  - **Eşik ve takip farkı kuralı vektör skoruyla karar vermeye devam etmeli.** Hibrit arama yalnızca modele giden parçaların sırasını değiştirmeli. Aksi halde Faz 3'teki eşik ayarları geçersiz olur.
- [x] **4c** Modelsiz kontrol: prototipteki sayıların gerçek koddan da çıktığını görmek. Ek olarak takip sorularında (birleşik metinle kelime araması) ve yapay konu değişimlerinde ([esik_takip_analiz.py](olcum_betikleri/esik_takip_analiz.py)) sıralamanın bozulmadığını görmek. Birleşik metindeki önceki sorunun kelimeleri parçaları o konuya çekebilir.
- [x] **4d** `evaluate.py --karsilastir` ile 5d'ye karşı uçtan uca ölçüm.

**Başarı ölçütü:**
- Özel ad sorularında hit@1 %100.
- hit@1 %87.8'in altına düşmemeli.
- Hiçbir kategoride başarı düşmemeli.
- Tam başarı %95.6'nın altına düşmemeli.

**Riskler:**
- Soru kelimeleri listesi bu soru setine bakılarak yazıldı. Faz 5.5'teki kontrol setiyle doğrulanmalı.
- Önekli arama ("kut*") farklı kelimeleri de yakalayabilir ("Kutluk", "Kutadgu"). Prototipte zarar görülmedi, ama belge sayısı arttıkça etkisi değişebilir.

### Faz 5: Üretim katmanı ve model kararı (H5–H9) ✅ (14.09.2026)

- [x] Kaynak satırını koda yazdırmak (H5). Sistem komutu Faz 3'teki haliyle korundu, model kaynak yazıyor, kod siliyor ve kendi bulduğu kaynağı ekliyor (5d).
- [x] Takip sorusunda modele önceki soruyu iletmek (H9). **Reddedildi:** Uydurma getirdi. Kod kapalı bir ayar olarak duruyor (`FOLLOW_UP_CONTEXT_TO_MODEL = False`).
- [x] Sistem komutunu uydurmayı azaltacak şekilde sıkılaştırmak (H8). **Uygulanmadı:** Hedefleyebileceği 1–2 hata kaldı ve model sistem komutuna çok hassas.
- [x] Model karşılaştırması: qwen2.5-7b ve qwen3-4b, temiz sunucuda, 5d yapılandırmasıyla. qwen3-4b 62. soruda Foundry'yi çökertti. qwen3-8b denenmedi (gerekçe Bölüm 2.11).
- [x] `TOP_K` ayarı (H6): `TOP_K = 5` reddedildi (başarı düştü, süre 7 sn'ye çıktı), `TOP_K = 3` kalıyor.
- [x] **Karar:** qwen2.5-7b kalıyor. Model değişmediği için bellek eşiklerinin yeniden ölçülmesi gerekmedi.

**Başarı ölçütü:** Uydurma ≤ %5, kaynak satırı %100 ve doğru belge, takip sorularında doğru cevap. Hız hedefi (ortalama ≤ 3 sn) korunmalı.
**Sonuç:**
- ✅ Gözle kontrolde yanlış bilgi içeren cevap oranı %4.1.
- ✅ Kaynak satırı %100, doğru belge %98.6. Tek hata, yanlış cevabın kendi kaynağı (`takip-2`).
- ✅ Süre ortalaması 1.95 sn.
- ⚠️ Takip sorularında 5'te 4. "hangi yılda?" hâlâ yanlış.

> **Faz 3'ten sonra dikkat:** Cevaplanamaz soruların %87.5'ini artık model reddediyor, çünkü eşik yalnızca güvenlik tabanı. Model ya da sistem komutu değiştirilirse (H7, H8) "cevaplanamaz soruları reddetme %100" ölçütü her adımda kontrol edilmeli. Faz 5'te bu kontrol yapıldı: 5b'de oran %87.5'e düştüğü için değişiklik reddedildi.

**Bundan sonraki karşılaştırma noktası:** [2026-09-14_0626_faz5d-eski-istem-kaynak-kodda.json](../degerlendirmeler/2026-09-14_0626_faz5d-eski-istem-kaynak-kodda.json).

### Faz 5.5: Kontrol seti ile doğrulama ✅ (14.09.2026)

> **Sonuç (Bölüm 2.13):**
> - Soruları sahibin tercihiyle asistan yazdı, bu bir sınırlama.
> - Kontrol setinde tam başarı %88.4 ✅.
> - Cevaplanamaz soruları reddetme %87.5 ❌: kural 1b tetiklendi.
> - Hibrit arama kural 2.1 nedeniyle kapalı kalıyor (uydurma 2 → 4).
> - Sıradaki: Faz 5.6.

Aşağıdaki plan ölçüm öncesinde yazıldı ve olduğu gibi bırakıldı.

**Neden gerekli?** İki sebep var:
1. **Ayarlar bu setin sonuçlarına bakılarak seçildi.** Faz 2'deki talimat biçimi, Faz 3'teki eşik (0.33) ve takip farkı (0.20), Faz 4'teki soru kelimeleri listesi hep sonuçları görülen 105 soruya göre belirlendi. Bu değerler bu sete fazla uyuyor olabilir.
2. **Faz 4'ün açık kararı bu sete bağlı.** Hibrit arama aramayı iyileştiriyor ama uydurmayı artırıyor olabilir. Mevcut sette cevapsız takip sorusu yalnızca 2 tane olduğu için bu karar verilemiyor (Bölüm 2.12).

#### Soru setinin yazılması

**Kim yazmalı?** Soruları **sistemin cevaplarını görmemiş biri** yazmalı: proje sahibi, mentor ya da bir arkadaş. 105 sorunun sonuçlarını görmüş biri, farkında olmadan sistemin iyi yaptığı soru kalıplarına kayar. Asistan soruları yalnızca biçim (`eval_set.py` girdileri) açısından düzenler, beklenen belge ve kanıt ifadesini belgeye bakarak doldurur. Soruların kendisini değiştirmez.

**İçerik (~40 soru):**

| Grup | Sayı | Neyi test ediyor |
|---|---|---|
| Cevaplanabilir tekil soru, farklı kalıplarda ("... ne demektir?", "... hakkında bilgi ver", "... neden önemlidir?") | 12 | Genelleşme, soru kelimeleri listesi (Faz 4) |
| Kısa kavram ve özel ad soruları ("Ülüş nedir?", "Ötüken nedir?") | 5 | 0.33 eşiğinin dar payı (Faz 3) |
| Konuya yakın ama belgede olmayan sorular | 8 | Modelin reddetme kararı, uydurma |
| Takip soruları, cevap belgede var | 4 senaryo | Takip farkı kuralı (Faz 3) |
| **Takip soruları, cevap belgede yok** | **6 senaryo** | **Faz 4 kararı:** "ilk başkanı kimdi?" türü uydurma |
| Konu değişimi, kısa soruyla | 3 senaryo | Takip kuralının bilinen sınırı |
| Konu dışı, önceki sorudan sonra | 2 senaryo | Modelin reddetme kararı |

#### Uygulama adımları

- [x] **5.5a** Soruları yazdırmak ve belgelerle eşleştirmek: beklenen belge, kanıt ifadesi, anahtar ifadeler. `python evaluate.py --kontrol` ile doğrulamak.
- [x] **5.5b** [eval_set.py](../eval_set.py): Kontrol sorularını ayrı bir listede tutmak (`KONTROL_SORULAR`, `KONTROL_SENARYOLAR`). [evaluate.py](../evaluate.py): `--set ana|kontrol` seçeneği. Varsayılan `ana` kalmalı ki önceki karşılaştırmalar geçerliliğini korusun. Kontrol raporu ayrı dosyaya yazılmalı.
- [x] **5.5c** Kontrol setini iki modda, temiz sunucuda ölçmek: hibrit kapalı ve hibrit açık. Deney için `LRA_HYBRID` ortam değişkeni eklenebilir.
- [x] **5.5d** Her iki modun cevaplarını gözle kontrol etmek. Otomatik puanlama belgeyle çelişen cevapları kaçırabiliyor (Bölüm 2.12, `ulku-4`). Gözle kontrol, hangi modun cevabı olduğu bilinmeden yapılmalı: cevaplar karışık sırada ve mod etiketi olmadan okunmalı.
- [x] **5.5e** Aşağıdaki karar kurallarını uygulamak ve sonucu bu dokümana yazmak.

#### Karar kuralları (ölçümden önce yazıldı, sonuçlara göre değiştirilmeyecek)

**1. Genelleşme** (hibrit kapalı, mevcut varsayılan yapılandırma):
- Kontrol setindeki tam başarı ana setten (%95.6) **10 puandan fazla** düşükse (< %85.6), ayarlar bu sete fazla uymuş sayılır. Hangi kategorinin düştüğüne bakılır: kısa kavram soruları düşüyorsa eşik, takip soruları düşüyorsa takip farkı gözden geçirilir.
- Kontrol setinde cevaplanamaz soruları reddetme **%90'ın altındaysa**, reddetme kararını modele bırakan C yaklaşımı (Faz 3) yeniden değerlendirilir.

**2. Hibrit arama** (açık ve kapalı mod karşılaştırması). Açılması için **üç koşulun hepsi** sağlanmalı:
1. **Uydurma artmamalı:** Gözle kontrolde cevaplanamaz sorulara verilen uydurma cevap sayısı kapalı moddakinden fazla olmamalı.
2. **Yanlış bilgi artmamalı:** Gözle kontrolde cevaplanabilir sorularda yanlış ya da belgeyle çelişen bilgi içeren cevap sayısı en fazla 1 fazla olabilir.
3. **Başarı düşmemeli:** Tam başarı kapalı moddakinden düşük olmamalı.

Koşullardan biri sağlanmazsa hibrit arama kapalı kalır. Kod ve indeks yine tutulur; model ya da sistem komutu değişirse yeniden değerlendirilir.

**3. Ana ve kontrol setindeki sonuçlar birlikte yorumlanır.** Ana sette (Faz 4) hibrit açık modda 2 fazla yanlış bilgi görüldü. Kontrol setinde de fark aynı yöndeyse bu bir eğilim sayılır.

#### Başarı ölçütü

- Kontrol setinde tam başarı ≥ %85.6.
- Cevaplanamaz soruları reddetme ≥ %90.
- Hibrit arama kararı yukarıdaki kurallara göre verilmiş olmalı.

### Faz 5.6: Uydurma koruması ✅ (14.09.2026)

> **Sonuç (Bölüm 2.14):**
> - **H12 kabul edildi.** Türkçe olmayan yazı koruması açık, kayıtlı 1586 cevabın 2'sini etkiliyor.
> - **H13 reddedildi.** İki doğrulayıcı talimatı da uydurmayı sıfırladı, ama 10–11 doğru cevabı da reddetti. Ölçüt en fazla 2'ydi.
> - **Sıradaki adım:** proje sahibinin bağımsız testi ([bagimsiz_test_rehberi.md](bagimsiz_test_rehberi.md)).

Aşağıdaki plan uygulama öncesinde yazıldı ve olduğu gibi bırakıldı:

**Neden gerekli?** Kontrol setinde (hibrit kapalı) cevaplanamaz 16 sorudan 2'sine uydurma cevap geldi, cevaplanabilir 27 sorudan 3'ünde yanlış bilgi var. Biri Çince metin içeriyor. Eşik bunları ayıramıyor (Bölüm 2.13). Sorun, reddetme kararının tek bir üretim adımında modele bırakılması.

**Hamleler** (her biri ayrı ölçülecek):

| # | Hamle | Hedef | Risk |
|---|---|---|---|
| H12 | **Türkçe olmayan yazı koruması** (kodla): Cevapta Çince, Japonca ya da Kore alfabesi varsa cevap o noktadan kesilir. Kalan kısım anlamlı değilse aynı istem bir kez yeniden denenir, olmazsa reddedilir. `evaluate.py` de bu karakterleri hata saysın. | `k-toy` türü çıktılar, otomatik puanlamanın kör noktası | Düşük: yalnızca bu karakterler varken devreye girer |
| H13 | **Cevap doğrulama adımı:** Cevap üretildikten sonra modele ikinci, kısa bir istek gönderilir. Model yalnızca "BAĞLAM, SORU'daki kişi/olay/kurum hakkında bu cevabı açıkça içeriyor mu? EVET/HAYIR" sorusunu cevaplar. HAYIR ise sistem reddeder. | Konuya yakın tuzaklar ve yanlış konuyu cevaplayan takip soruları | Yanlış red artabilir. Her soruya ~0.5–1 sn eklenir. Model aynı model olduğu için kendi hatasını görmeyebilir |
| H13b | H13'ün hibrit arama açıkken denenmesi | Hibrit aramanın arama kazancını uydurma olmadan almak | H13 başarılı olmadan anlamsız |

**Ölçüm ve karar:**
- Önce ana set, sonra kontrol seti ölçülmeli. Kontrol seti artık görülmüş bir set; sonuçları ancak ikincil kanıt sayılır.
- **H13 kabul ölçütü** (ölçümden önce yazıldı):
  - İki sette toplam uydurma sayısı azalmalı: ana set 5d'de 0, kontrol hibrit kapalıda 2.
  - İki sette toplam yanlış red en fazla 2 artmalı.
  - Ortalama süre ≤ 3 sn kalmalı.
- **Son doğrulama:** Faz 5.6'dan sonra proje sahibinin bağımsız testi yapılmalı. Bu ölçüm hiçbir ayar için kullanılmamış tek temiz veri.

### Faz 6: Belgeleme ve kapanış

- [ ] README'yi kodla eşitlemek: model, ayarlar, belge sayısı, Windows kurulumu, **bellek yükleme sırası ve açılıştaki ısıtma** (ilk sorunun neden ~15 sn sürdüğü).
- [ ] Nihai ölçüm raporunu hazırlamak: başlangıç ile son durumun karşılaştırması.
- [ ] [proje_uygunluk_raporu.md](proje_uygunluk_raporu.md) içindeki açık maddelerin durumunu güncellemek.

### Özet takvim

| Faz | İçerik | Bağımlılık | Karar noktası |
|---|---|---|---|
| 0 | Ölçüm altyapısı ve başlangıç ölçümü | — | — |
| 1 ✅ | Paragraf parçalama | Faz 0 | — |
| 1b (beklemede) | Bağlamsız paragraflar için komşu bağlam (H1b) | Faz 1 | Faz 2'den sonra gerekli görünmüyor |
| 2 ✅ | Sorgu talimatı (Türkçe) | Faz 1 | — |
| 3 ✅ | Eşik kalibrasyonu ve takip sorusu kuralı (H10) | Faz 2 | C yaklaşımı: eşik 0.33, takip farkı 0.20 |
| 5 ✅ | Kaynak (H5 kabul), takip bağlamı (H9 red), `TOP_K` (5 red), komut (H8 uygulanmadı), model (qwen2.5-7b kalıyor) | Faz 3 | qwen2.5-7b kalıyor |
| 4 ✅ (kapalı) | Hibrit arama: arama ölçütleri iyi (hit@3 %100), ama uydurmayı artırıyor (ana set 0 → 1, kontrol 2 → 4) | Faz 5 | Kapalı kalıyor (Faz 5.5 kural 2.1) |
| 5.5 ✅ | Kontrol seti: tam başarı %88.4 ✅, cevaplanamaz soruları reddetme %87.5 ❌ | Faz 4 | Hibrit kapalı; C yaklaşımı güçlendirilmeli |
| 5.6 ✅ | Türkçe olmayan yazı koruması (H12 kabul), cevap doğrulama (H13 iki varyantıyla red) | Faz 5.5 | Uydurma bu modelle ucuz yollarla çözülemedi |
| **Bağımsız test (sıradaki)** | Proje sahibinin kapsamlı testi (tek temiz veri), [rehber](bagimsiz_test_rehberi.md) | Faz 5.6 | Sonraki planlama: model/donanım, Faz 6 |
| 6 | Belgeleme | Faz 5 | — |

---

## Ek: Tamamlanan düzeltmeler

| Tarih | Düzeltme | Dosya |
|---|---|---|
| 14.09.2026 | Model bellekte değilse otomatik yükleme ve "not loaded" hatasında yeniden deneme (`with_model`) | [foundry_client.py](../foundry_client.py) |
| 14.09.2026 | Gömme modeli belge ve sorguda aynı adla seçiliyor (`EMBED_MODEL`) | [embed.py](../embed.py), [search.py](../search.py) |
| 14.09.2026 | Ard arda sorularda konu değişince "dokümanda yok" hatası (`retrieve()`) | [rag.py](../rag.py) |
| 14.09.2026 | Bellek yükleme sırası: cevap süresi 48 sn → 2.3 sn (`set_primary()`, `warmup_messages()`) | [foundry_client.py](../foundry_client.py), [rag.py](../rag.py) |
| 14.09.2026 | `foundry server stop` çıktısının Windows'ta kod sayfası hatası vermesi | [foundry_client.py](../foundry_client.py) |
| 14.09.2026 | Faz 5.6: Türkçe olmayan yazı koruması (açık), cevap doğrulama adımı (kod var, kapalı); değerlendirmede yabancı yazı hatası ve doğrulama sayaçları | [rag.py](../rag.py) (`cut_foreign_script`, `verify_answer`, `LRA_VERIFY`, `LRA_VERIFY_PROMPT`), [evaluate.py](../evaluate.py) |
| 14.09.2026 | Faz 5.5: 43 soruluk kontrol seti (`KONTROL_SORULAR`, `KONTROL_SENARYOLAR`), `evaluate.py --set kontrol`, `LRA_HYBRID` ortam değişkeni, kör inceleme aracı | [eval_set.py](../eval_set.py), [evaluate.py](../evaluate.py), [search.py](../search.py) |
| 14.09.2026 | Faz 4: FTS5 anahtar kelime indeksi ve hibrit arama (`HYBRID_SEARCH`, varsayılan kapalı). Eşik ve takip kararları en yüksek vektör skoruna bağlandı (`best_score`) | [ingest.py](../ingest.py) (`fold`, `build_fts`, `--fts`), [search.py](../search.py) (`search_details`, `keyword_ranks`), [rag.py](../rag.py), [app.py](../app.py), [masaustu.py](../masaustu.py), [evaluate.py](../evaluate.py) |
| 14.09.2026 | Faz 5: Kaynak satırını kod belirliyor (`pick_source`). Arayüzler önceki soruyu `previous_question` ile geçiriyor. Deney ayarları eklendi: `LRA_TOP_K`, `LRA_CHAT_MODEL`, `FOLLOW_UP_CONTEXT_TO_MODEL`. Tam başarı %87.8 → %95.6 | [rag.py](../rag.py), [app.py](../app.py), [masaustu.py](../masaustu.py), [evaluate.py](../evaluate.py) |
| 14.09.2026 | Faz 3: Takip sorusu kuralı skor farkına bağlandı (0.20), eşik 0.42 → 0.33. Tam başarı %85.6 → %87.8 | [rag.py](../rag.py) (`retrieve`, `MIN_SCORE`, `FOLLOW_UP_MARGIN`), [evaluate.py](../evaluate.py) |
| 14.09.2026 | Faz 2: Türkçe sorgu talimatı. Tam başarı %76.7 → %85.6. Değerlendirmeye bozuk bellek uyarısı eklendi | [search.py](../search.py), [evaluate.py](../evaluate.py) |
| 14.09.2026 | Faz 1: Paragraf parçalama ve başlık yolu. Tam başarı %67.8 → %76.7 | [ingest.py](../ingest.py), [evaluate.py](../evaluate.py) (rapordaki parçalama bilgisi), [.gitignore](../.gitignore) (`knowledge_*.db`) |
| 14.09.2026 | Faz 0: 105 soruluk değerlendirme seti ve ölçüm altyapısı | [eval_set.py](../eval_set.py), [evaluate.py](../evaluate.py), [rag.py](../rag.py) (`answer_details`, `follow_up_query`), [app.py](../app.py), [masaustu.py](../masaustu.py), [README.md](../README.md) |

## Ek: Çalışma ortamındaki durum

- `qwen3-4b-cuda-gpu` karşılaştırma için indirildi (2.6 GB). Uygulama hâlâ qwen2.5-7b kullanıyor. Silmek için: `foundry cache remove qwen3-4b-cuda-gpu`.
- Ölçüm betikleri ve ham sonuçlar [olcum_betikleri/](olcum_betikleri/) klasöründe:

| Dosya | Ne ölçüyor |
|---|---|
| `olc.py`, `olc2.py`, `olc3.py` | İlk süre dökümü ve takip sorusu arama skorları |
| `karsilastir.py` | İki modeli aynı bağlamla karşılaştırır (sürüm 2: temiz bellek) |
| `karsilastirma_sonuc_2026-09-14.json` | İlk karşılaştırma (qwen2.5-7b bozuk bellekte, hızı geçersiz) |
| `karsilastirma_sonuc_temiz_bellek.json` | Temiz bellekte karşılaştırma |
| `parca_analiz.py` | Parçalama ve sorgu biçimlerinin arama sırasına etkisi |
| `hiz_teshis.py`, `hiz_teshis2.py` | Bellek yükleme sırası teşhisi |
| `hiz_dogrulama.py` | `set_primary()` düzeltmesinin 4 senaryoda doğrulaması |
| `plan_dogrulama.py`, `plan_dogrulama_sonuc.json` | Değerlendirme seti, Streamlit art arda soru, takip ve konu dışı sorular |
| `gomme_hizi.py` | Uygulamanın yükleme sırasında gömme isteğinin süresi |
| `talimat_arama.py` | Sorgu talimatı biçimlerinin yalnızca arama üzerindeki etkisi (model yok, ~1 dk) |
| `esik_takip_analiz.py` | Eşik değerlerinin ve takip sorusu kurallarının etkisi, yapay konu değişimleriyle (model yok, ~1 dk) |
| `kaynak_secimi.py` | `pick_source`'u eski bir değerlendirmenin cevaplarıyla sınar (model yok, saniyeler). Yalnızca aynı parçalamayla alınmış sonuçlarda geçerli |
| `hibrit_prototip.py` | FTS5 + vektör hibrit aramasının sıralamaya etkisi (model yok, ~1 dk). Faz 4'ten önce yazıldı; artık `search()` hibrit sıralama döndürebildiği için yalnızca `HYBRID_SEARCH = False` iken anlamlı |
| `kor_inceleme.py`, `kontrol_inceleme/` | İki çalıştırmanın cevaplarını mod etiketi olmadan karşılaştırma (`hazirla`, `ac`) |
| `kontrol_ozet.py` | Kontrol setinin iki modunun otomatik özeti |
| `yabanci_yazi_kontrol.py` | Türkçe olmayan yazı korumasının birim testleri ve kayıtlı bütün cevaplara etkisi (model yok) |
| `dogrulama_inceleme.py` | Cevap doğrulamasının reddettiği cevapları ve hâlâ cevap verilen cevaplanamaz soruları listeler |
| `faz4_kontrol.py` | Hibrit aramanın gerçek kodla kontrolü: sıralama, karar değişmezliği, takip ve yapay konu değişimleri (model yok, ~1 dk) |

Faz 0'dan sonra asıl ölçüm aracı `evaluate.py`. Buradaki betikler tek seferlik teşhis içindir.

> **Dikkat:** `hiz_*` betikleri ve `karsilastir.py` Foundry sunucusunu yeniden başlatır. Uygulama açıkken çalıştırılırsa uygulamanın ilk sorusu ~15 sn sürer.
