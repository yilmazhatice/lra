# Nihai Ölçüm Raporu: Başlangıç ve Son Durum

**Tarih:** 15 Eylül 2026
**Kapsam:** Faz 0–5.6 sonundaki durum. Proje sahibinin bağımsız testi henüz yapılmadı; bu rapor o testten sonra güncellenmeli.
**Ayrıntılar:** [rag_iyilestirme_plani.md](rag_iyilestirme_plani.md) (her fazın ölçümleri, gerekçeleri ve karar kuralları)

## Kısaca

- **Tam başarı %67.8'den %95.6'ya çıktı.** 105 soruluk ana sette, aynı model (qwen2.5-7b) ve aynı donanımla.
- **Cevabı belgede olan soruları reddetme %20.3'ten %2.7'ye indi.** Doğru kaynak gösterme %91.5'ten %98.6'ya çıktı.
- **Yanıt süresi ~48 sn'den ~2 sn'ye indi.** Sebep model değil, ekran kartı belleğinin yükleme sırasıydı.
- **Sonuçları görülmemiş 43 soruluk kontrol setinde tam başarı %88.4.**
- **Kalan zayıflık uydurma:** Kontrol setinde cevaplanamaz 16 sorudan 2'sine uydurma yanıt geldi. Bu, qwen2.5-7b'nin 8 GB ekran kartındaki sınırından geliyor; denenen çözümler başka bir şeyi bozdu.

## Ölçüm düzeni

| | |
|---|---|
| Donanım | Windows 11, RTX 5070 Laptop GPU (8 GB) |
| Dil modeli | `qwen2.5-7b-instruct-cuda-gpu` (Foundry Local) |
| Gömme modeli | `qwen3-embedding-0.6b-cuda-gpu` |
| Belgeler | 13 belge, 86 paragraf |
| Ana set | 105 soru (90 puanlanan): 65 cevaplanabilir, 10 cevaplanamaz, 15 senaryo. Ayarlar bu sete bakılarak yapıldı |
| Kontrol seti | 58 soru (43 puanlanan). Sonuçları görülmeden yazılıp donduruldu, ayar için kullanılmadı |
| Tekrarlanabilirlik | `temperature = 0`. Aynı ayarlarla iki çalıştırmada 105 cevabın 2'sinin metni farklı çıktı, sonuç değişmedi |
| Başlangıç ölçümü | [2026-09-14_0351_baslangic.md](../degerlendirmeler/2026-09-14_0351_baslangic.md) |
| Son ölçüm | [2026-09-15_0119_nihai.md](../degerlendirmeler/2026-09-15_0119_nihai.md), [2026-09-15_0124_kontrol_nihai.md](../degerlendirmeler/2026-09-15_0124_kontrol_nihai.md) |

**Başlangıçtaki yavaşlık:** Faz 0'dan önce yanıtlar 48–58 sn sürüyordu. Bellek yükleme sırası düzeltildikten sonra başlangıç ölçümü alındı. Bu yüzden aşağıdaki başlangıç süresi (1.8 sn) düzeltme sonrasına ait ([yavaslik_sorunu_ve_cozumu.md](yavaslik_sorunu_ve_cozumu.md)).

## Başlangıç ve son durum (ana set, 90 puanlanan soru)

| Ölçüt | Başlangıç | Son | Fark |
|---|---|---|---|
| **Tam başarı** | %67.8 | **%95.6** | +27.8 puan |
| Doğru bölüm 1. sırada (hit@1) | %68.9 | %87.8 | +18.9 |
| Doğru bölüm ilk 3'te (hit@3) | %87.8 | %95.9 | +8.1 |
| MRR | 0.796 | 0.919 | +0.123 |
| Cevaplanabilir sorularda başarı | %66.2 | %94.6 | +28.4 |
| **Yanlış red** (cevap belgede varken) | %20.3 | **%2.7** | −17.6 |
| bunun eşikte olanı | %17.6 | %0 | −17.6 |
| Anahtar ifadelerin tamamı | %91.5 | %97.2 | +5.7 |
| Kaynak satırı var / doğru belge | %96.6 / %91.5 | %100 / **%98.6** | |
| Cevaplanamaz soruları reddetme | %93.8 | **%100** | +6.2 |
| Red yanıtına eklenmiş kaynak satırı | 4 | 0 | |
| Süre ortalaması / ilk token | 1.8 / 1.0 sn | 2.2 / 0.9 sn | +0.4 sn |
| Eski 12 soruluk set | 10/12 | 12/12 | |

| Kategori | Başlangıç | Son |
|---|---|---|
| normal (55) | 41 | 54 |
| kısa kavram / özel ad (10) | **3** | **9** |
| konuya yakın cevaplanamaz (6) | 3 | 6 |
| konu dışı ve anlamsız (4) | 4 | 4 |
| takip (5) | 3 | 4 |
| takip, cevap belgede yok (2) | 2 | 2 |
| konu değişimi (4) | 2 | 3 |
| konu dışı, önceki sorudan sonra (4) | 3 | 4 |

Başlangıçla son ölçüm arasında 26 soru HATA'dan OK'e geçti, 1 soru OK'den HATA'ya düştü (Turan'dan sonra "Kımız nedir?").

## Kontrol seti (43 puanlanan soru)

| Ölçüt | Sonuç |
|---|---|
| Tam başarı | %88.4 (ana setten 7.2 puan düşük; önceden belirlenen sınır 10 puan) |
| hit@1 / hit@3 | %85.2 / %88.9 |
| Yanlış red | %7.4 |
| Doğru kaynak | %100 |
| Cevaplanamaz soruları reddetme | %87.5 (önceden belirlenen hedef %90) |
| Süre ortalaması | 2.2 sn |

## Gözle kontrol

Otomatik puanlama anahtar ifadelere ve kaynağa bakıyor. Anahtar ifade geçtiği halde yanıtın geri kalanı yanlış olabildiği için bütün yanıtlar ayrıca okundu.

| | Ana set | Kontrol seti |
|---|---|---|
| Cevaplanabilir sorularda yanlış ya da belgeyle çelişen bilgi | 3 / 74 (%4.1) | 2 / 27 (%7.4) |
| Cevaplanamaz sorulara uydurma yanıt | 0 / 16 | 2 / 16 (%12.5) |

**Yanlış bilgi içeren yanıtlar:**
- Ana set:
  - "Orhun alfabesini kim çözdü?" sorusundan sonra "hangi yılda?": 1893 yerine 1928 (Harf Devrimi) yazıyor.
  - "Ergenekon'dan çıkan topluluğa yolu kim gösterdi?": Börteçine yerine "Böri" yazıyor.
  - "Eski Türkçede kurt kelimesinin anlamı": "böri, yani solucan" diye iki bilgiyi karıştırıyor.
- Kontrol seti:
  - "Yeni alfabede kaç harf var?": "yirmi dokudan altı harf" diyor.
  - "Tuğrul Bey kimdir?": "Alparslan'ın babası" diyor, belgede yok.

**Uydurmalar (kontrol seti):**
- "Kurtuluş Savaşı'nda Doğu Cephesi komutanı kimdi?" (bilerek konmuş tuzak): Model, Mustafa Kemal'in Birinci Dünya Savaşı'ndaki Doğu Cephesi görevini yanıt gibi sundu.
- "Uygur Kağanlığı hangi yıl kuruldu?" sorusundan sonra "ne zaman yıkıldı?": Osmanlı'nın yıkılışını anlattı.

## Neyin ne kadar katkı verdiği

Her değişiklik tek başına uygulanıp bir önceki kabul edilen yapılandırmayla karşılaştırıldı.

| Faz | Değişiklik | Tam başarı | Karar |
|---|---|---|---|
| — | Bellek yükleme sırası ve açılışta ısıtma | (süre 48 sn → 2 sn) | Kabul |
| 0 | 105 soruluk değerlendirme seti, başlangıç ölçümü | %67.8 | — |
| 1 | Paragraf başına bölüm, başlık yolu, örtüşme yok | %76.7 | Kabul |
| 2 | Türkçe sorgu talimatı (İngilizce talimat hit@1'i düşürdü) | %85.6 | Kabul |
| 3 | Takip sorusu kuralı skor farkına bağlandı (0.20) | %86.7 | Kabul |
| 3 | Eşik 0.42 → 0.33 (güvenlik tabanı) | %87.8 | Kabul |
| 5 | Kaynak satırını kod belirliyor | %95.6 | Kabul |
| 5 | Önceki soruyu dil modeline göstermek | %91.1 | **Red** (uydurma getirdi) |
| 5 | `TOP_K = 5` | %90.0 | **Red** (süre 7 sn) |
| 5 | qwen3-4b | 62 soruda 52 (qwen2.5-7b: 60) | **Red** (Foundry çöktü) |
| 4 | Hibrit arama (anahtar kelime + vektör) | %96.7 | **Kapalı** (arama iyileşti, uydurma arttı) |
| 5.5 | Kontrol seti ile doğrulama | kontrol %88.4 | Hibrit arama kapalı kaldı |
| 5.6 | Türkçe olmayan yazı koruması | kontrol setinde 1 yanıt düzeldi | Kabul |
| 5.6 | Yanıt doğrulama adımı (iki talimat) | ana set %84.4 / %87.8 | **Red** (10–11 doğru yanıtı reddetti) |
| — | Son ölçüm | **%95.6**, kontrol %88.4 | — |

**Başlıca dersler:**
1. **Kayıpların çoğu arama katmanındaydı, model değildi.** Yanlış redlerin büyük kısmı parçalama ve eşikten geliyordu. Bu katmandaki değişiklikler (Faz 1–3) tam başarıya 20 puan ekledi.
2. **Sabit bir benzerlik eşiği, cevaplanabilir ve cevaplanamaz soruları ayıramıyor.** Konuya yakın cevaplanamaz sorular (0.52–0.69), cevaplanabilir soruların çoğundan yüksek skor alıyor.
3. **qwen2.5-7b istem değişikliklerine çok hassas.** Kaynak kuralını çıkarmak 3 soru kaybettirdi, "devamıdır" yönlendirmesi uydurma getirdi.
4. **Arama ölçütü iyileşmesi her zaman daha iyi yanıt demek değil.** Hibrit arama doğru bölümü her soruda bağlama soktu, ama modele daha çok konuyla ilişkili ve yanıltıcı olabilecek paragraf verdiği için uydurma arttı.
5. **Otomatik puanlama tek başına yeterli değil.** Çince metin ve "anahtar ifade var ama yanıt yanlış" durumlarını kaçırdı; her ölçümde yanıtlar gözle kontrol edildi.

## Kalan hatalar (son ölçüm)

**Ana set, 4 HATA:**

| Soru | Sebep |
|---|---|
| "Kut nedir?" | Doğru bölüm 4. sırada, model reddediyor |
| "Ergenekon'dan çıkan topluluğa yolu kim gösterdi?" | Bağlamda "Börteçine" var, model "Böri" yazıyor |
| Orhun'dan sonra "hangi yılda?" | Doğru bölüm 5. sırada, model bağlamdaki tek yılı (1928) yazıyor |
| Turan'dan sonra "Kımız nedir?" | Takip kuralı soruyu yanlışlıkla takip sorusu sayıyor, doğru bölüm 30. sıraya düşüyor |

**Kontrol seti, 5 HATA:** harf sayısı (yanlış bilgi), "Ülüş nedir?" ve "Otağ nedir?" (doğru bölüm 4.–5. sırada, yanlış red), Doğu Cephesi ve Uygur (uydurma).

## Bilinen sınırlar

- **Tuzak ve eksik takip sorularında uydurma.** Kontrol setinde %12.5. Eşik, istem, hibrit arama ve ikinci bir doğrulama çağrısıyla denendi, hiçbiri başka bir şeyi bozmadan çözemedi.
- **Değerlendirme setleri tarafsız değil.** Ana set üzerinde ayar yapıldı. Kontrol setini, ana setin sonuçlarını görmüş olan asistan yazdı; kontrol setinin sonuçları da Faz 5.6'da görüldü. Tamamen temiz tek ölçüm, proje sahibinin bağımsız testi olacak.
- **Dil hataları.** Bilgi doğru olsa da yanıtlarda yazım hatası ve kelime tekrarı görülüyor ("Göktürk Dev Devleti", "yirmirmi bir yaş yaşındaydı").
- **Bellek sınırı.** Ekran kartını aynı anda yoğun kullanan başka bir program yanıtları yavaşlatabilir. Uygulama bunu yalnızca açılışta ve model bellekten atıldığında denetliyor.
- **Küçük veri.** 13 belge, 86 paragraf. Sonuçlar daha büyük ya da farklı konulardaki bir belge setine doğrudan taşınamaz; eşik ve takip farkı yeniden ölçülmeli.

## Sonraki adım

1. **Proje sahibinin bağımsız testi** ([bagimsiz_test_rehberi.md](bagimsiz_test_rehberi.md)).
2. **Test sonucuna göre karar:**
   - Uydurma oranı kabul edilebilirse Faz 6'nın kalan maddesi (uygunluk raporunun güncellenmesi) ve sunum hazırlığı.
   - Kabul edilemezse daha güçlü bir model ya da ayrı bir doğrulayıcı model. Bu, 8 GB ekran kartında bellek sınırı nedeniyle donanım değişikliği gerektirebilir.
3. **Bağımsız test sorularının `eval_set.py`'ye yeni bir grup olarak eklenmesi.** Böylece sonraki her değişiklik o sorularla da ölçülür.
