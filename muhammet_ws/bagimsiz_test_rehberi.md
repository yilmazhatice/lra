# Bağımsız Test Rehberi

Bu testin sonuçları hiçbir ayar yapılırken görülmedi. Bu yüzden sistemin gerçek başarısını en doğru bu test gösterecek. Sonraki planlama (model ya da donanım değişikliği, Faz 6) bu teste göre yapılacak.

## Hazırlık

1. Açık Streamlit ya da masaüstü uygulaması varsa kapatın.
2. Foundry sunucusunu temiz başlatın:
   ```
   foundry server stop
   ```
3. Uygulamayı açın (`lra` klasöründe):
   ```
   streamlit run app.py
   ```
4. **İlk soru ~15 sn sürer.** Model belleğe yükleniyor ve ısıtılıyor. Sonraki sorular 2–4 sn sürmeli. Sürekli 5 sn'yi aşıyorsa not edin: ekran kartı belleği bozuk düzende olabilir (plan Bölüm 2.5).

Test sırasında ekran kartını yoğun kullanan başka program (oyun, video düzenleme) çalıştırmamanız süreleri güvenilir tutar.

## Nasıl test edilmeli?

**Önce doğal kullanım.** Sistemi, bu belgeleri merak eden bir kullanıcı gibi kullanın. Aklınıza gelen soruları, aklınıza gelen biçimde sorun. Soruları belgelerde önceden aramayın. Karışık sırada şunları deneyin:
- Belgelerde cevabı olan sorular (kısa, uzun, "neden", "nasıl", "kimdir", "ne demektir"...).
- Konuya yakın ama belgelerde olmayan sorular. Örneğin belgede bir kişi geçiyor ama sorduğunuz ayrıntı geçmiyor.
- Aynı sohbette art arda sorular: "sonra ne oldu?", "kaç yıl sürdü?" gibi takip soruları ve konu değiştiren sorular.
- Tamamen konu dışı sorular.

**Sonra bilinen zayıf noktalar** (ayrı not alın ki doğal kullanım sonucunu etkilemesin):
- **Tuzak sorular:** Belgede benzer ama farklı bir olay varken sorulan sorular. Örneğin başka bir savaştaki bir görevi, başka bir devletin başkentini sormak. Kontrol setinde 16 cevaplanamaz sorudan 2'si bu türden uydurmayla cevaplandı.
- **Eksik takip soruları:** "ne zaman yıkıldı?", "başkenti neresiydi?" gibi, soru tek başına başka bir konuya da uyabiliyorsa.
- **Farklı soru kalıpları:** Kontrol setinde "neden?", "kim, hangi yılda?" gibi kalıplarda yanlış bilgi oranı arttı (%4'ten %11'e).

## Her soru için ne kaydedilmeli?

Cevabın doğruluğunu, ilgili belgeyi (`docs/` klasörü ya da cevabın altındaki kaynak kartı) açarak kontrol edin.

| # | Soru | Önceki soru (varsa) | Sonuç | Süre (sn) | Not |
|---|---|---|---|---|---|
| 1 | | | | | |

**Sonuç sütunu için etiketler:**

| Etiket | Anlamı |
|---|---|
| **D** | Doğru, belgeyle uyumlu, kaynak doğru |
| **E** | Eksik ama yanlış bilgi yok |
| **Y** | Yanlış ya da belgeyle çelişen bilgi, yanlış kaynak ya da Türkçe olmayan metin |
| **R-doğru** | "Bu bilgi elimdeki dokümanlarda yok" dedi ve gerçekten yok |
| **R-yanlış** | Reddetti ama cevap belgede var |
| **U** | Belgede olmayan bir soruya cevap verdi (uydurma) |

En önemli sayılar, sistemin vaadine göre sırasıyla:
1. **U sayısı** (uydurma)
2. **Y sayısı** (yanlış bilgi)
3. **R-yanlış sayısı** (gereksiz red)

## Karşılaştırma için mevcut ölçümler

| | Ana set (105 soru, ayar yapılan) | Kontrol seti (43 soru, asistanın yazdığı) |
|---|---|---|
| Cevaplanabilir sorularda yanlış bilgi (Y) | %4.1 | %7.4 |
| Cevaplanamaz sorularda uydurma (U) | %0 | %12.5 |
| Ortalama süre | 2.0 sn | 2.1 sn |

Sonuçlarınızı bu dosyaya ya da ayrı bir dosyaya yazıp paylaşırsanız, soruları `eval_set.py` içine yeni bir test grubu olarak ekleyebilirim. Böylece sonraki her değişiklik sizin sorularınızla da ölçülür.
