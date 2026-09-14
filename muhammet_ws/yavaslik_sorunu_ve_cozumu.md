# Yavaşlık Sorunu ve Çözümü

**Tarih:** 14 Eylül 2026
**Sonuç:** Ortalama cevap süresi **48 sn → 2.3 sn**. Model (qwen2.5-7b) ve cevaplar aynı kaldı.

## Sorun

- Her soru 45–75 sn sürüyordu. Art arda sorularda süre giderek uzuyordu.
- Modelin cevaba başlaması 30–40 sn sürüyordu. Cevabı da saniyede ~4 token hızla yazıyordu.
- RTX 5070'te 7B bir modelden beklenen hız bunun 10 katından fazla.

## Sebep

Sebep modelin kendisi değildi. Sorun, **ekran kartı belleğinin hangi sırayla dolduğuydu.**

- İki model (sohbet 4.8 GB, gömme 0.5 GB) ve Windows masaüstü birlikte 8 GB belleğin sınırına dayanıyor.
- Bellek dolunca NVIDIA sürücüsü hata vermiyor. Taşan kısmı sessizce sistem RAM'ine koyuyor ve o bellekle çalışan adım 10–20 kat yavaşlıyor.
- Uygulama her soruda önce arama yapıyordu. Bu yüzden önce gömme modeli yükleniyor ve belleği alıyordu. Sohbet modeli de kalan belleğe sığmaya çalışırken bir kısmı RAM'e düşüyordu.

## Nasıl bulundu?

| Deneme | Sonuç |
|---|---|
| Süreyi adımlara ayırmak | Arama 0.03 sn. Tüm süre sohbet modelinde geçiyor. |
| Pil / güç modu | Bilgisayar prizdeydi, sebep bu değil. |
| 32K bağlam için ayrılan büyük önbellek | 40K bağlamlı qwen3-4b hızlı çalıştı, sebep bu değil. |
| Temiz sunucuda yalnızca sohbet modeli | 1 sn'de başlıyor, 43 token/sn üretiyor. **Model sağlam.** |
| Aynı 5 soru, eski sıra (önce gömme modeli) | Ortalama **48.1 sn** |
| Aynı 5 soru, önce sohbet modeli + ısıtma | Ortalama **2.5 sn** |
| Modeli bellekten boşaltıp yeniden yüklemek | Yetmiyor: üretim 21 token/sn'de kalıyor. Sunucu yeniden başlatılmalı. |

## Çözüm

**[foundry_client.py](../foundry_client.py): `set_primary()`**
1. **Doğru sıra:** Sohbet modeli belleğe her zaman ilk yükleniyor. Gömme modeli ondan sonra geliyor.
2. **Isıtma:** Uygulamanın gönderebileceği en uzun istem bir kez gönderiliyor. Böylece sohbet modeli ihtiyaç duyacağı belleği baştan alıyor.
3. **Bozuk durumu fark etme:** Foundry sunucusu uygulamadan bağımsız çalışıyor ve önceki bir çalıştırmadan bozuk düzende kalmış olabilir. Isıtma sırasında iki şey ölçülüyor:
   - İlk token 3 sn'yi aşıyorsa ya da üretim 30 token/sn'nin altındaysa sunucu yeniden başlatılıyor.
   - Model yeniden başlatmadan sonra doğru sırayla yükleniyor.
4. **Oturum ortasında model atılırsa** aynı işlem tekrarlanıyor.

**[rag.py](../rag.py): `warmup_messages()`**
- Isıtma istemini veritabanındaki en uzun parçalarla oluşturuyor.

Arayüz dosyalarında (Streamlit, masaüstü, terminal) değişiklik gerekmedi.

## Doğrulama

| Durum | İlk soru | Sonraki sorular |
|---|---|---|
| Temiz sunucu | 15.6 sn (model yükleme dahil) | 2.3 sn |
| Sağlıklı sunucuya yeniden bağlanma | 4.5 sn | 2.3 sn |
| Bozuk bellek (otomatik düzeltildi) | 22.2 sn | 2.0 sn |
| Terminal: `python rag.py "..."` | — | 4.2 sn (önceden 48–58 sn) |

## Sınırlar

- **Uygulama çalışırken** başka bir program ekran kartı belleğini doldurursa yavaşlama geri gelebilir.
- **Sunucu yeniden başlatılırsa** Foundry'yi kullanan başka uygulamaların modelleri de bellekten çıkar.
- **Eşik değerleri** (3 sn, 30 token/sn) bu makinede ölçüldü. Model ya da donanım değişirse yeniden ölçülmeli.

**Ayrıntılar ve ölçüm betikleri:** [rag_iyilestirme_plani.md](rag_iyilestirme_plani.md) (Bölüm 2.5), [olcum_betikleri/](olcum_betikleri/)
