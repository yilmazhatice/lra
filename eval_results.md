# Değerlendirme Sonuçları

Eşik değeri (MIN_SCORE): 0.42

- Başarılı: **11/12**
- Ortalama yanıt süresi: **10.1 sn**

## Özet tablo

| # | Soru | Beklenen kaynak | hit@3 | Reddetti | En yüksek skor | Süre (sn) | Sonuç |
|---|------|-----------------|-------|----------|----------------|-----------|-------|
| 1 | RAG'in üç adımı nedir? | 01.md | evet | hayir | 0.715 | 21.8 | OK |
| 2 | RAG hangi iki pratik sorunu çözer? | 01.md | evet | hayir | 0.745 | 7.9 | OK |
| 3 | Kosinüs benzerliği hangi aralıkta değer alır? | 02.md | evet | hayir | 0.440 | 9.0 | OK |
| 4 | Anlamsal arama anahtar kelime aramasından neden üstündür? | 02.md | evet | hayir | 0.465 | 8.9 | OK |
| 5 | Vektörler neden JSON yerine BLOB olarak saklanır? | 03.md | evet | hayir | 0.690 | 14.9 | OK |
| 6 | SQLite neden ayrı bir sunucu gerektirmez? | 03.md | evet | hayir | 0.669 | 8.4 | OK |
| 7 | Foundry Local hangi API biçimini konuşur? | 04.md | evet | hayir | 0.666 | 23.0 | OK |
| 8 | Sistem mesajı ile kullanıcı mesajı arasındaki fark nedir? | 05.md | evet | hayir | 0.457 | 10.4 | OK |
| 9 | Türkiye'nin başkenti neresi? | (cevaplanamaz) | - | evet | 0.259 | 0.2 | OK |
| 10 | Bugün hava nasıl olacak? | (cevaplanamaz) | - | evet | 0.287 | 0.0 | OK |
| 11 | Python'da bir listeyi nasıl ters çeviririm? | (cevaplanamaz) | - | hayir | 0.504 | 8.6 | HATA |
| 12 | asdf qwerty zxcv | (cevaplanamaz) | - | evet | 0.459 | 8.0 | OK |

## Cevaplar

### 1. RAG'in üç adımı nedir?

Getirilen: `01.md, 01.md, 01.md` — en yüksek skor: 0.715

> [01.md / parca 0]  
RAG iki pratik sorunu çözer. Birincisi bayatlıktır: bir model eğitim tarihinden sonra yazılmış dokümanları bilemez, ama bir arama sistemi beş dakika önce eklenmiş bir dosyayı okuyabilir. İkincisi halüsinasyondur. Bilmediği bir şey sorulduğunda model akıcı ama yanlış bir cevap uydurma eğilimindedir. Doğru paragrafı vermek, doğru cevabı üretilmesi en kolay seçenek haline getirir ve cevabın hangi dokümandan geldiğini göstermeyi mümkün kılar.

(RAG'in üç adımı: Getirme, Zenginleştirme ve Üretme.)

### 2. RAG hangi iki pratik sorunu çözer?

Getirilen: `01.md, 01.md, 01.md` — en yüksek skor: 0.745

> [01.md / parca 1]

### 3. Kosinüs benzerliği hangi aralıkta değer alır?

Getirilen: `02.md, 03.md, 02.md` — en yüksek skor: 0.440

> [Kaynak: 02.md]

### 4. Anlamsal arama anahtar kelime aramasından neden üstündür?

Getirilen: `02.md, 02.md, 01.md` — en yüksek skor: 0.465

> [02.md / parca 1]

### 5. Vektörler neden JSON yerine BLOB olarak saklanır?

Getirilen: `03.md, 03.md, 02.md` — en yüksek skor: 0.690

> Vektörler JSON yerine BLOB olarak saklanır çünkü BLOB, sayısal veri olarak saklanan vektörleri daha hızlı ve daha az yer kaplayan bir veri türüdür. JSON, vektörleri saklamak için daha fazla bellek ve daha fazla işlem süresi gerektirir. BLOB, bu nedenlerden dolayı daha etkili bir veri saklama yöntemidir.

### 6. SQLite neden ayrı bir sunucu gerektirmez?

Getirilen: `03.md, 03.md, 03.md` — en yüksek skor: 0.669

> [03.md / parca 0]

### 7. Foundry Local hangi API biçimini konuşur?

Getirilen: `04.md, 04.md, 01.md` — en yüksek skor: 0.666

> [04.md / parca 0]  
Foundry Local, Microsoft'un dil modellerini doğrudan kullanıcının kendi cihazında çalıştırmak için geliştirdiği çalışma zamanıdır. Bir model kataloğu, bir indirici ve yerel bir sunucuyu bir arada sunar. Böylece bir uygulama, hiçbir veriyi bulut servisine göndermeden çıkarım yapabilir ve model diske indikten sonra ağ bağlantısına hiç ihtiyaç duymaz.

[04.md / parca 1]  
Model yüklendikten sonra Foundry Local onu bir HTTP uç noktası üzerinden sunar ve bu uç nokta OpenAI sohbet tamamlama API'siyle aynı istek-cevap biçimini konuşur. (Kaynak: 04.md)

### 8. Sistem mesajı ile kullanıcı mesajı arasındaki fark nedir?

Getirilen: `05.md, 01.md, 01.md` — en yüksek skor: 0.457

> [01.md / parca 0]

### 9. Türkiye'nin başkenti neresi?

Getirilen: `05.md, 02.md, 01.md` — en yüksek skor: 0.259

> Bu bilgi elimdeki dokümanlarda yok.

### 10. Bugün hava nasıl olacak?

Getirilen: `02.md, 01.md, 03.md` — en yüksek skor: 0.287

> Bu bilgi elimdeki dokümanlarda yok.

### 11. Python'da bir listeyi nasıl ters çeviririm?

Getirilen: `03.md, 03.md, 03.md` — en yüksek skor: 0.504

> [03.md / parca 2]

### 12. asdf qwerty zxcv

Getirilen: `03.md, 01.md, 03.md` — en yüksek skor: 0.459

> Bu bilgi elimdeki dokümanlarda yok.
