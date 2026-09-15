"""Soruyu al, ilgili parcalari getir, yerel LLM ile cevap uret."""

import difflib
import re
import sys
import time

from foundry_client import client, find_model
from search import search, kokler

TOP_K = 8             # aramada getirilen aday parca sayisi
MIN_SCORE = 0.42      # bu esigin altinda en iyi parca varsa hic cevap uretme
RED_IFADESI = "elimdeki dokümanlarda yok"   # reddetme yanitinin sabit ifadesi
CHAT_KEYWORD = "qwen2.5-7b"
MAX_TOKENS = 600      # liste soran sorularda 350 token cevabi ortadan kesiyordu
GECMIS_TUR = 2        # modele tasinan onceki soru-cevap sayisi
GECMIS_CEVAP_SINIRI = 300   # gecmisteki cevaplar bu uzunluga kirpilir

YAKIN_ESIK = 0.30     # esigi gecemeyen ama "az kalsin" eslesen sorular

# Modele verilecek parcalar getirilenlerin tamami degil: yanit suresinin
# neredeyse tamami baglami okumakla geciyor (~7.7 sn / 1000 karakter). En iyi
# skorun BAGLAM_ORANI altinda kalan parcalar cevaba katkidan cok gecikme
# getiriyor. Olcum (32 soru): sabit 5 parca -> dogru belge 32/32, ~29 sn;
# asagidaki kural -> yine 32/32, ~19 sn.
BAGLAM_ORANI = 0.70
BAGLAM_EN_AZ = 2
BAGLAM_EN_COK = 5
BAGLAM_BUTCE = 2800   # karakter; en kotu durumdaki bekleyisi sinirlar
BELGE_SINIRI = 2      # ayni belgeden en fazla kac parca alinir

SYSTEM_PROMPT = """Sen Türkçe konuşan bir doküman asistanısın. Sana BAĞLAM
olarak birkaç belge parçası ve bir SORU verilir. Görevin, sorunun cevabını
BAĞLAM'da bulup akıcı bir Türkçeyle yazmaktır.

BAĞLAM soruyla ilgili bilgi içeriyorsa cevap ver. Kısmen içeriyorsa elindeki
kadarını yaz. Hiç ilgili bilgi yoksa yalnızca şu cümleyi yaz:
Bu bilgi elimdeki dokümanlarda yok.

Kurallar:
- Yalnızca BAĞLAM'daki bilgiyi kullan, kendi genel bilgini ekleme.
- Doğrudan cevapla: soruyu tekrar etme, "bağlamda", "verilen metne göre"
  gibi ifadeler kullanma.
- Kullanıcıya dosya okumasını önerme, "inceleyebilirsiniz" gibi yönlendirme
  yazma; bildiğini doğrudan aktar.
- Aynı bilgiyi iki kez yazma.
- Birbirine bağlı, tam cümleler kur; normalde üç dört cümle yeter.
- Soru bir liste istiyorsa (ilkeler, maddeler, adlar) hepsini kısa
  maddeler halinde say, yarıda bırakma.
- Kişi, yer ve kurum adlarını BAĞLAM'daki yazımıyla birebir kopyala; adı
  kendin çekimleme, BAĞLAM'da hangi biçimde geçiyorsa öyle yaz. BAĞLAM'da
  geçmeyen bir ad yazma.
- Terimleri de birebir kopyala; kelime uydurma, kısaltma, birleştirme.
- Bağlamdaki köşeli parantezli etiketleri cevabına yazma.
- Cevabın son satırında kaynağı yalnızca dosya adıyla belirt.

Cevap biçimi şöyle olmalı:

Kurdun eski Türkçedeki adı böri idi.
(Kaynak: turk-kulturunde-kurt.md)"""


def strip_thinking(text):
    """Bazi modeller <think>...</think> blogu uretebilir; guvenlik agi.

    Cikti token sinirinda kesilirse kapanis etiketi hic gelmez; o durumda
    <think>'ten sonrasinin tamami dusunme metnidir.
    """
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"<think>.*$", "", text, flags=re.DOTALL)
    return text.strip()


def baglam_parcalari(hits):
    """Modele verilecek parcalari sec.

    Baskin bir parca varsa az, skorlar birbirine yakinsa daha cok parca
    gonderilir. Ayni belgeden en fazla BELGE_SINIRI parca alinir: "Kut
    nedir?" gibi sorularda ilk dort sira tek bir belgeyle doluyor ve dogru
    belge baglamin disinda kaliyordu.
    """
    if not hits:
        return hits

    esik = BAGLAM_ORANI * hits[0][0]
    secili, sayac, toplam = [], {}, 0
    for h in hits:
        if len(secili) >= BAGLAM_EN_COK:
            break
        if sayac.get(h[2], 0) >= BELGE_SINIRI:
            continue
        if len(secili) >= BAGLAM_EN_AZ:
            if h[0] < esik or toplam + len(h[4]) > BAGLAM_BUTCE:
                continue
        secili.append(h)
        sayac[h[2]] = sayac.get(h[2], 0) + 1
        toplam += len(h[4])
    return secili


def _dayanak_belgesi(text, hits):
    """Cevabin sozcuk olarak en cok ortustugu parcanin belgesini dondurur."""
    cevap = kokler(text)
    if not cevap:
        return None
    puanlar = {}
    for _s, _c, dosya, _i, parca in hits:
        ortusme = len(cevap & kokler(parca)) / len(cevap)
        puanlar[dosya] = max(puanlar.get(dosya, 0.0), ortusme)
    return max(puanlar.items(), key=lambda x: x[1]) if puanlar else None


def kaynagi_duzelt(text, hits):
    """Kaynak satirini tek bicime sokar ve dogru belgeyi gosterir.

    Model kaynagi bazen hic yazmiyor, bazen parantezsiz yaziyor, bazen iki
    kez tekrarliyor, bazen de baglamdaki '[dosya / parca 5]' etiketini
    oldugu gibi kopyaliyor. Ayrica cevabi bir belgeden alip listenin ilk
    sirasindaki baska belgeyi gosterebiliyor ("Kut nedir?" ornegi); bu
    durumda cevabin parcalarla sozcuk ortusmesine bakip duzeltiyoruz.
    """
    # 1. Parantezsiz yazimi da tek bicime cek
    text = re.sub(r"(?<!\()Kaynak:\s*([\w.-]+\.md)\)?", r"(Kaynak: \1)", text)

    # 2. Gecen butun kaynak bildirimlerini topla ve metinden cikar
    yazilanlar = []
    for eslesme in re.findall(r"\(Kaynak:([^)]*)\)", text):
        yazilanlar += re.findall(r"[\w.-]+\.md", eslesme)
    text = re.sub(r"\s*\(Kaynak:[^)]*\)", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    # Modelin kendi reddettigi yanitlara kaynak eklenmez: dayanak yok.
    if not hits or RED_IFADESI in text:
        return text

    # 3. Cevabin gercekte hangi belgeye dayandigini bul
    dayanak = _dayanak_belgesi(text, hits)
    secilen = list(dict.fromkeys(yazilanlar)) or (
        [dayanak[0]] if dayanak else [hits[0][2]]
    )

    if dayanak and dayanak[0] not in secilen:
        cevap_kok = kokler(text)
        en_iyi_yazilan = max(
            (len(cevap_kok & kokler(parca)) / max(1, len(cevap_kok))
             for _s, _c, dosya, _i, parca in hits if dosya in secilen),
            default=0.0,
        )
        # Yalnizca belirgin fark varsa mudahale ediyoruz; cevap gercekten iki
        # belgeye dayaniyorsa modelin tercihini bozmayalim.
        if dayanak[1] > en_iyi_yazilan * 1.25:
            secilen = [dayanak[0]]

    return f"{text}\n(Kaynak: {', '.join(secilen)})"


# Buyuk harfle baslayan kelimeleri yakalar; Turkce harfler dahil.
_AD_DESENI = re.compile(r"[A-ZÇĞİÖŞÜ][\wÇĞİÖŞÜçğıöşü'’]+")


def baglamdisi_adlar(text, hits):
    """Cevapta gecip BAGLAM'da bulunmayan ozel adlari dondurur.

    7B model ozel adlari Turkce ekle cekimlerken bozabiliyor: "Türkeş'in"
    yerine "Türkş'in" ya da "Türkşeddin Esat Paşa" yazdigi goruldu. Kok
    karsilastirmasi bu bozulmalari yakaliyor.
    """
    baglam = set()
    for _s, _c, _d, _i, parca in hits:
        baglam |= kokler(parca)

    # Cumle basindaki kelimeler de taraniyor: bozulan ad cumleye de
    # baslayabiliyor ("Türkş, bu ilkeleri..."). Yanlis yakalamanin bedeli
    # dusuk; onarim yalnizca cok benzer bir karsilik varsa devreye giriyor.
    bulunan = []
    for ad in _AD_DESENI.findall(text):
        govde = ad.split("'")[0].split("’")[0]
        kok = kokler(govde)
        if kok and not (kok & baglam):
            bulunan.append(ad)
    return sorted(set(bulunan))


def adlari_onar(text, hits):
    """Baglamda karsiligi olmayan adlari en yakin gercek yazimla degistirir.

    Yalnizca cok benzer bir karsilik bulunursa (yazim bozulmasi) mudahale
    ediliyor; tamamen uydurulmus bir ad oldugu gibi birakiliyor.
    """
    sapanlar = baglamdisi_adlar(text, hits)
    if not sapanlar:
        return text

    # Adaylara hem baglamdaki bicim ("Türkeş'in") hem de eksiz govde
    # ("Türkeş") giriyor; model adi eksiz de bozabiliyor.
    adaylar = set()
    for _s, _c, _d, _i, parca in hits:
        for ad in _AD_DESENI.findall(parca):
            adaylar.add(ad)
            adaylar.add(ad.split("'")[0].split("’")[0])

    for ad in sapanlar:
        yakin = difflib.get_close_matches(ad, adaylar, n=1, cutoff=0.85)
        if yakin:
            text = re.sub(rf"(?<!\w){re.escape(ad)}(?!\w)", yakin[0], text)
    return text


def _reddet(hits):
    """Esigin altinda kalan sorulara verilen yanit.

    Skor sinira yakinsa kullaniciya hangi belgelerin ilgili gorundugunu
    soyluyoruz; tamamen alakasiz sorularda ise belge havuzunun konusunu
    hatirlatiyoruz. Ilk cumle iki durumda da ayni: reddetme davranisi
    degerlendirmede bu cumleyle olculuyor.
    """
    if hits and hits[0][0] >= YAKIN_ESIK:
        belgeler = list(dict.fromkeys(h[2] for h in hits[:3]))
        return (
            "Bu bilgi elimdeki dokümanlarda yok. En yakın bölümler şu "
            f"belgelerde geçiyor: {', '.join(belgeler)}. Soruyu biraz daha "
            "açık yazarsanız yeniden bakabilirim."
        )
    return (
        "Bu bilgi elimdeki dokümanlarda yok. Yüklü belgeler Türk tarihi, "
        "kültürü ve milliyetçi hareketin tarihi üzerine; bu konularda "
        "sorarsanız yardımcı olabilirim."
    )


def build_context(hits):
    return "\n\n".join(
        f"[{doc_name} / parca {chunk_idx}]\n{text}"
        for _score, _cid, doc_name, chunk_idx, text in hits
    )


# Bir onceki soruya isaret eden kaliplar. Bu sozcukler geciyorsa soru tek
# basina aranamaz: "Bu hayvan destanlarda hangi rollerde gecer?" tek basina
# arandiginda at belgesini getiriyor, oysa konu kurt.
ISARET_KALIPLARI = (
    "bu ", "bun", "şu ", "şun", "onun", "onlar", "ondan", "peki",
    "aynı", "söz konusu", "bahsettiğin", "dediğin", "yukarıdaki",
)


def _isaret_ediyor(question):
    """Soru bir onceki tura mi gonderme yapiyor?"""
    metin = question.lower()
    return any(k in metin for k in ISARET_KALIPLARI)


def answer(question, top_k=TOP_K, search_query=None, history=None,
           stream_cb=None):
    """(cevap, getirilen_parcalar, gecen_sure) dondur.

    history: [{"soru": ..., "cevap": ...}] seklinde onceki turlar. Hem takip
    sorularinin aranmasinda hem de modele baglam olarak kullanilir.
    search_query verilirse arama dogrudan onunla yapilir.
    stream_cb verilirse, model uretirken metnin o ana kadarki hali bu
    fonksiyona tekrar tekrar gonderilir (arayuzde canli yazim icin).
    """
    started = time.perf_counter()

    # Takip sorusu tek basina aranamaz. Isaret eden bir soruda dogrudan
    # onceki soruyla birlestiriyoruz; kisa ama isaretsiz bir soru zayif
    # kalirsa birlesigi yedek olarak deniyoruz. (Onceki surumde birlestirme
    # her kisa soruda yapiliyordu ve ilgisiz sorularda skoru dusuruyordu.)
    onceki = history[-1]["soru"] if history else None
    aranan = search_query or question
    if search_query is None and onceki and _isaret_ediyor(question):
        aranan = onceki + " " + question

    hits = search(aranan, top_k=top_k)

    if (search_query is None and onceki and aranan == question
            and len(question.split()) <= 8
            and (not hits or hits[0][0] < MIN_SCORE)):
        alternatif = search(onceki + " " + question, top_k=top_k)
        if alternatif and (not hits or alternatif[0][0] > hits[0][0]):
            hits = alternatif

    # Esik korumasi: alakali hicbir sey bulunamadiysa modele hic sormuyoruz.
    # Boylece model alakasiz baglamdan cevap uydurma firsati bulamiyor.
    if not hits or hits[0][0] < MIN_SCORE:
        return _reddet(hits), hits, time.perf_counter() - started

    # Yalnizca secilen parcalar hem modele gider hem de arayuzde "yanitin
    # dayandigi bolumler" olarak gosterilir; ikisi ayrismasin.
    hits = baglam_parcalari(hits)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for tur in (history or [])[-GECMIS_TUR:]:
        # Uzun cevaplar (ornegin dokuz maddelik bir liste) oldugu gibi
        # tasinirsa model yeni soruyu o listenin icinden cevaplamaya calisiyor
        # ve ozel adlari karistiriyordu; ozeti yetiyor.
        ozet = re.sub(r"\n?\(Kaynak:[^)]*\)", "", tur["cevap"]).strip()
        if len(ozet) > GECMIS_CEVAP_SINIRI:
            ozet = ozet[:GECMIS_CEVAP_SINIRI].rsplit(" ", 1)[0] + "…"
        messages.append({"role": "user", "content": tur["soru"]})
        messages.append({"role": "assistant", "content": ozet})
    messages.append({
        "role": "user",
        "content": (
            f"BAĞLAM:\n{build_context(hits)}\n\n"
            f"SORU: {question}\n\n"
            "Türkçe cevap ver."
        ),
    })

    istek = dict(
        model=find_model(CHAT_KEYWORD),
        messages=messages,
        temperature=0.0,
        max_tokens=MAX_TOKENS,
    )

    def uret(mesajlar):
        """Bir cevap uretir; stream_cb verilmisse akisli."""
        if stream_cb is None:
            resp = client().chat.completions.create(**{**istek, "messages": mesajlar})
            return strip_thinking(resp.choices[0].message.content or "")

        # Akisli uretim: yanit 20-30 saniye surebiliyor, kullanicinin ilk
        # kelimeleri birkac saniyede gormesi bekleyisi katlanilir kiliyor.
        parcalar = []
        akis = client().chat.completions.create(
            stream=True, **{**istek, "messages": mesajlar}
        )
        for olay in akis:
            if not olay.choices:
                continue
            yeni_parca = olay.choices[0].delta.content or ""
            if yeni_parca:
                parcalar.append(yeni_parca)
                stream_cb(strip_thinking("".join(parcalar)))
        return strip_thinking("".join(parcalar))

    text = uret(messages)

    # Ozel ad denetimi ve onarimi: model adlari Turkce ekle cekimlerken
    # bozabiliyor ("Türkeş'in" -> "Türkş'in"). Modele yeniden urettirmek bu
    # hatayi tekrarliyor, bu yuzden bozulan adi baglamdaki gercek yazimiyla
    # dogrudan degistiriyoruz.
    text = adlari_onar(text, hits)

    if not text:
        text = (
            "Model bu soru için bir yanıt üretemedi. "
            "Soruyu biraz daha açık yazmayı deneyin."
        )

    return kaynagi_duzelt(text, hits), hits, time.perf_counter() - started


def show(question, debug=False):
    text, hits, elapsed = answer(question)
    print(f"\nSoru: {question}")
    print(f"\n{text}")
    print(f"\n[{elapsed:.1f} sn]")

    if debug:
        print("\nGetirilen parcalar:")
        for score, _cid, doc_name, chunk_idx, _text in hits:
            print(f"  {doc_name} / parca {chunk_idx}  benzerlik={score:.3f}")


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--debug"]

    if args:
        show(" ".join(args), debug)
    else:
        print("Soru yazin, cikmak icin bos birakip Enter'a basin.")
        while True:
            try:
                q = input("\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not q:
                break
            show(q, debug)