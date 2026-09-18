# -*- coding: utf-8 -*-
"""Reddetme deneyi: istem varyantlarini hizli karsilastir.

Tam degerlendirme 175 soru / ~7 dk. Burada
  - butun cevaplanamaz sorular (ana + kontrol, senaryolar dahil)  -> 32
  - en dusuk skorlu cevaplanabilir sorular (yanlis red riski)     -> 14
  - KANARYA: tam olcumde L varyantinin bozdugu sorular            ->  9
calistiriliyor. Kanarya sorulari yalnizca reddedildi mi diye degil, anahtar
ifadeyi iceriyor mu diye de denetleniyor: L varyantinda bozulan 8 sorunun
4'u reddedilmedi, cevaplandi ama anahtar bilgiyi yazmadi.

Kullanim: python red_deney.py <varyant_adi> [<varyant_adi> ...]
"""
import io, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, ".")
import rag, eval_set

RED = "elimdeki dokümanlarda yok"

TEMEL = rag.SYSTEM_PROMPT
BASKA_KONU = "\n- BAĞLAM başka bir kişiyi ya da olayı anlatıyorsa onu anlatma, reddet."
TAHMIN_ETME = "\n- Sorulan kişi, tarih ya da sayı BAĞLAM'da yazmıyorsa tahmin etme, reddet."

ACIK_CEVAP = TEMEL.replace(
    "Yalnızca BAĞLAM'daki bilgiyle\ncevap ver, kendi bilgini ekleme. "
    "BAĞLAM'da ilgili bilgi yoksa tek satır yaz:\nBu bilgi elimdeki dokümanlarda yok.",
    "Yalnızca BAĞLAM'daki bilgiyle\ncevap ver, kendi bilgini ekleme. "
    "Sorunun cevabı BAĞLAM'da açıkça yazmıyorsa,\nkonu ilgili görünse bile tek satır yaz:"
    "\nBu bilgi elimdeki dokümanlarda yok.",
)

VARYANTLAR = {
    "temel":               TEMEL,
    "A-acik-cevap":        ACIK_CEVAP,
    "B-tam-karsilik":      ACIK_CEVAP + TAHMIN_ETME,
    "L-baska-konu":        ACIK_CEVAP + TAHMIN_ETME + BASKA_KONU,   # tam olcumde ana seti dusurdu
    "M-yalniz-baska-konu": TEMEL + BASKA_KONU,
    "N-A+baska-konu":      ACIK_CEVAP + BASKA_KONU,
}

AYARLAR = {ad: (ad, {}) for ad in VARYANTLAR}
AYARLAR.update({
    "C-enaz1":       ("temel", {"BAGLAM_EN_AZ": 1}),
    "D-oran085":     ("temel", {"BAGLAM_ORANI": 0.85}),
    "G-oran055":     ("temel", {"BAGLAM_ORANI": 0.55}),
    "J-onceki-soru": ("temel", {"FOLLOW_UP_CONTEXT_TO_MODEL": True}),
})
_VARSAYILAN = {k: getattr(rag, k) for k in
               ("BAGLAM_EN_AZ", "BAGLAM_ORANI", "BAGLAM_EN_COK", "FOLLOW_UP_CONTEXT_TO_MODEL")}

# Tam olcumde L varyantinin bozdugu sorular. (id, soru, onceki, anahtar)
# anahtar: "a|b" = a ya da b gecmeli.
KANARYA = [
    ("canakkale-1", "Çanakkale Deniz Zaferi hangi tarihte kazanılmıştır?", None, "18 Mart 1915"),
    ("osmanli-4",   "Orhan Gazi kimdir", None, "Bursa|Rumeli"),
    ("kurt-4",      "Eski Türkçede kurt kelimesinin anlamı neydi?", None, "solucan|kurtçuk|larva"),
    ("kurt-6",      "Ergenekon'dan çıkan topluluğa yolu kim göstermiştir?", None, "Börteçine"),
    ("alfabe-1",    "Göktürk alfabesi kaç işaretten oluşur?", None, "otuz sekiz|38"),
    ("alfabe-5",    "Kutadgu Bilig hangi yüzyılda yazılmıştır?", None, "on birinci|11"),
    ("teskilat-1",  "Divan-ı Hümayun'a Fatih Sultan Mehmed'den sonra kim başkanlık etmiştir?",
     None, "veziriazam|sadrazam"),
    ("takip-3",     "kaç dizeden oluşur?", "Dünyanın en uzun destanı hangisidir?", "yarım milyon"),
    ("k-kurt-neden", "Türk kültüründe sembol olarak neden kurt seçilmiştir?", None, "evcil"),
]


def fold(s):
    return s.replace("İ", "i").replace("I", "ı").lower()


def cevapla(soru, onceki=None):
    return rag.answer_details(soru, previous_question=onceki)["text"]


def cevaplanamazlar():
    out = []
    for kaynak, tekil, senaryolar in [
        ("ana", eval_set.SORULAR, eval_set.SENARYOLAR),
        ("kon", eval_set.KONTROL_SORULAR, eval_set.KONTROL_SENARYOLAR),
    ]:
        for s in tekil:
            if not s.get("belge"):
                out.append((f"{kaynak}:{s['id']}", s["soru"], None))
        for sc in senaryolar:
            turlar = sc["sorular"]
            if not turlar[-1].get("belge"):
                out.append((f"{kaynak}:{sc['id']}#son", turlar[-1]["soru"], turlar[-2]["soru"]))
    return out


def riskli(n=14):
    d = json.load(open("degerlendirmeler/2026-09-18_1950_terim-paragraflari-son.json",
                       encoding="utf-8"))
    ce = [r for r in d["sonuclar"]
          if r.get("cevaplanabilir") and r.get("grup") != "hazirlik" and r.get("en_iyi_skor")]
    ce.sort(key=lambda r: r["en_iyi_skor"])
    return [(f"ans:{r['id']}", r["soru"], r.get("onceki_soru")) for r in ce[:n]]


def calistir(ad):
    istem, ayar = AYARLAR[ad]
    for k, v in _VARSAYILAN.items():
        setattr(rag, k, v)
    for k, v in ayar.items():
        setattr(rag, k, v)
    rag.SYSTEM_PROMPT = VARYANTLAR[istem]

    dogru_red = 0
    cevaplanamaz = cevaplanamazlar()
    hatalar = []
    for vid, soru, onceki in cevaplanamaz:
        metin = cevapla(soru, onceki)
        if RED in metin:
            dogru_red += 1
        else:
            hatalar.append(f"  CEVAPLADI   {vid:26} {soru[:40]}")

    yanlis_red = 0
    riskliler = riskli()
    for vid, soru, onceki in riskliler:
        if RED in cevapla(soru, onceki):
            yanlis_red += 1
            hatalar.append(f"  YANLIS RED  {vid:26} {soru[:40]}")

    kanarya_bozuk = 0
    for vid, soru, onceki, anahtar in KANARYA:
        metin = cevapla(soru, onceki)
        if RED in metin:
            kanarya_bozuk += 1
            hatalar.append(f"  KANARYA-RED {vid:26} {soru[:40]}")
        elif not any(fold(a) in fold(metin) for a in anahtar.split("|")):
            kanarya_bozuk += 1
            hatalar.append(f"  KANARYA-EKS {vid:26} {soru[:40]}  (aranan: {anahtar})")

    print(f"\n=== {ad} ===")
    print(f"  Cevaplanamaz reddetme : {dogru_red}/{len(cevaplanamaz)} = {dogru_red/len(cevaplanamaz):.1%}")
    print(f"  Yanlis red (riskli)   : {yanlis_red}/{len(riskliler)}")
    print(f"  KANARYA bozuk         : {kanarya_bozuk}/{len(KANARYA)}")
    for h in hatalar:
        print(h)


if __name__ == "__main__":
    for ad in sys.argv[1:] or ["temel"]:
        calistir(ad)
