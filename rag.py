"""Soruyu al, ilgili parcalari getir, yerel LLM ile cevap uret."""

import difflib
import math
import re
import sys
import time

from foundry_client import client, find_model
from search import search, kokler

TOP_K = 8             # aramada getirilen aday parca sayisi
# Bu esigin altinda en iyi parca varsa modele hic sorulmaz. Olcum (18 soru):
# belgelerden cevaplanabilen sorular 0.479-0.791, cevaplanamayanlar
# 0.179-0.577 araliginda skor aliyor. Iki kume ust uste biniyor, yani hicbir
# esik ikisini temiz ayirmiyor: esigi yukseltmek cevaplanabilir sorulari
# reddettirmeye basliyor. Ustteki bindirmeyi (ornegin "Fatih Sultan
# Mehmed'in annesi", 0.577) modelin kendi reddetmesi karsiliyor.
MIN_SCORE = 0.42
RED_IFADESI = "elimdeki dokümanlarda yok"   # reddetme yanitinin sabit ifadesi
CHAT_KEYWORD = "qwen2.5-7b"
MAX_TOKENS = 600      # liste soran sorularda 350 token cevabi ortadan kesiyordu
GECMIS_TUR = 2        # modele tasinan onceki soru-cevap sayisi
GECMIS_CEVAP_SINIRI = 180   # gecmisteki cevaplar bu uzunluga kirpilir

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

# Istem uzunlugu dogrudan bekleme suresidir: sunucu prefix onbellegi
# tutmuyor, her soruda istemin tamami bastan okunuyor ve okuma karakter
# basina ~4.2 ms suruyor. Onceki 1332 karakterlik surum her soruya ~5.5 sn
# ekliyordu; asagidaki surum ayni kurallari tasiyor, dortte bir uzunlukta.
SYSTEM_PROMPT = """Türkçe doküman asistanısın. Yalnızca BAĞLAM'daki bilgiyle
cevap ver, kendi bilgini ekleme. BAĞLAM'da ilgili bilgi yoksa tek satır yaz:
Bu bilgi elimdeki dokümanlarda yok.

- Doğrudan cevapla; soruyu tekrarlama, "bağlamda/metne göre" deme, dosya
  okumayı önerme, aynı bilgiyi iki kez yazma.
- Tam cümleler kur, üç dört cümle yeter; liste isteniyorsa hepsini kısa
  maddeler hâlinde, eksiksiz say.
- Ad ve terimleri BAĞLAM'daki yazımıyla birebir kopyala, çekimleme;
  BAĞLAM'da geçmeyen adı yazma.
- Köşeli parantezli etiketleri cevaba yazma.
- Son satır: (Kaynak: dosya.md)"""


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


# Parcalarin tamami degil, soruyla ilgili cumle penceresi gonderiliyor.
# Cevabin dayanagi cogunlukla bir iki cumle; parcanin kalani yalnizca
# okuma suresi olarak geri donuyor. Ilk siradaki parca daha genis
# birakiliyor: cevap genellikle orada.
PENCERE_ILK = 620      # en iyi parcadan alinacak en fazla karakter
PENCERE_DESTEK = 380   # destekleyici parcalardan alinacak en fazla karakter

_CUMLE_SINIRI = re.compile(r"(?<=[.!?:])\s+|\n+")


def _cumlelere_ayir(metin):
    return [c.strip() for c in _CUMLE_SINIRI.split(metin) if c.strip()]


def _kok_agirliklari(soru_kok, cumle_kokleri):
    """Soru koklerini seyrekligine gore agirliklandirir.

    Duz sayim ayirt edici kokleri siradan olanlarin altinda birakiyordu:
    "Orhun Yazitlari'nin alfabesini kim ve hangi yilda cozmustur?" sorusunda
    'orhun' ve 'yazit' baglamin yarisinda geciyor, oysa cevabi tasiyan tek
    kok 'cozmu'. Seyrek kok agir basinca dogru cumle one geliyor.
    """
    n = max(1, len(cumle_kokleri))
    return {
        kok: math.log(1 + n / (1 + sum(1 for k in cumle_kokleri if kok in k)))
        for kok in soru_kok
    }


def ilgili_pencere(cumleler, cumle_kokleri, agirlik, sinir):
    """Parcanin soruyla en cok ortusen, bitisik cumlelerden olusan bolumu.

    En yuksek puanli cumleden baslanip iki yana, puani yuksek komsu once
    olmak uzere sinira kadar genisletiliyor. Bitisiklik onemli: cevap
    cogu zaman eslesen cumlenin hemen yanindaki cumlede tamamlaniyor.
    """
    if len(cumleler) < 2:
        return " ".join(cumleler)[:sinir]

    puanlar = [sum(agirlik.get(k, 0.0) for k in kok)
               for kok in cumle_kokleri]
    sol = sag = max(range(len(cumleler)), key=puanlar.__getitem__)
    uzunluk = len(cumleler[sol])

    while True:
        adaylar = []
        if sol > 0:
            adaylar.append((puanlar[sol - 1], sol - 1, "sol"))
        if sag < len(cumleler) - 1:
            adaylar.append((puanlar[sag + 1], sag + 1, "sag"))
        adaylar.sort(reverse=True)

        for _puan, sira, yon in adaylar:
            if uzunluk + len(cumleler[sira]) + 1 <= sinir:
                uzunluk += len(cumleler[sira]) + 1
                if yon == "sol":
                    sol = sira
                else:
                    sag = sira
                break
        else:
            break            # iki komsu da sigmiyor

    metin = " ".join(cumleler[sol:sag + 1])
    if sol > 0:
        metin = "… " + metin
    if sag < len(cumleler) - 1:
        metin += " …"
    return metin


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


def build_context(hits, question=None):
    """Modele gidecek BAGLAM metni.

    question verilirse her parca o soruyla ilgili penceresine kirpilir;
    verilmezse (degerlendirme, hata ayiklama) parcalar oldugu gibi gecer.
    Takip sorularinda buraya birlesik sorgu (onceki soru + soru) gelir:
    "neden degistirdiler" tek basina hangi cumlenin ilgili oldugunu
    soylemeye yetmiyor. Guncel soruyu agir bastirmayi denedim; yazim
    hatasi ya da cok kisa sorularda guncel sorunun kokleri hic
    tutmadigi icin pencere daha da kotulesiyor, esit agirlik daha
    saglam.
    """
    if not question:
        return "\n\n".join(
            f"[{doc_name} / parca {chunk_idx}]\n{text}"
            for _score, _cid, doc_name, chunk_idx, text in hits
        )

    # Agirliklar butun baglamdaki cumleler uzerinden hesaplaniyor: bir kok
    # yalnizca kendi parcasinda degil, baglamin tamaminda seyrekse degerli.
    cumleler = [_cumlelere_ayir(h[4]) for h in hits]
    kokleri = [[kokler(c) for c in grup] for grup in cumleler]

    agirlik = _kok_agirliklari(
        kokler(question), [k for grup in kokleri for k in grup]
    )

    bolumler = []
    for sira, (_score, _cid, doc_name, chunk_idx, text) in enumerate(hits):
        sinir = PENCERE_ILK if sira == 0 else PENCERE_DESTEK
        if len(text) > sinir:
            text = ilgili_pencere(cumleler[sira], kokleri[sira], agirlik, sinir)
        bolumler.append(f"[{doc_name} / parca {chunk_idx}]\n{text}")
    return "\n\n".join(bolumler)


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

    # Takip sorusu tek basina aranamaz: "bu hayvan destanlarda hangi
    # rollerde gecer?" tek basina arandiginda at belgesini getiriyor.
    # Isaret eden soruda dogrudan onceki soruyla birlestiriyoruz; kisa ama
    # isaretsiz sorularda ise iki sorgu da denenip iyi eslesen kazaniyor.
    onceki = history[-1]["soru"] if history else None
    aranan = search_query or question
    takip = False          # soru onceki tura mi dayaniyor
    if search_query is None and onceki and _isaret_ediyor(question):
        aranan = onceki + " " + question
        takip = True

    hits = search(aranan, top_k=top_k)

    # Isaret sozcugu tasimayan kisa sorular da onceki tura dayanabiliyor:
    # "neden degistirdiler", "hangi yil", "amaci neydi". Bunlarda birlesik
    # sorgu da deneniyor ve daha iyi eslesen kazaniyor. Onceki surumde
    # birlesik sorgu yalnizca kendi basina arama esigin ALTINDA kalirsa
    # deneniyordu; esigi geciyor ama yanlis belgeye giden takip sorulari
    # (0.42-0.60 bandi) boylece elden kaciyordu. Gercekten yeni bir soruda
    # birlesik sorgu seyreldigi icin kendi basina arama zaten one cikiyor.
    if (search_query is None and onceki and not takip
            and len(question.split()) <= 8):
        birlesik = onceki + " " + question
        alternatif = search(birlesik, top_k=top_k)
        if alternatif and (not hits or alternatif[0][0] > hits[0][0]):
            hits, aranan, takip = alternatif, birlesik, True

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
    # Takip sorusu tek basina anlasilmiyor: "neden degistirdiler" sorusunda
    # model dogru baglami almasina ragmen "bu bilgi dokumanlarda yok"
    # diyordu; gecmis turlarin mesaj olarak tasinmasi tek basina yetmedi.
    # Onceki soru BAGLAM/SORU gibi etiketli bir alan olarak veriliyor:
    # cumle icine gomulu yonergeyi model cevabina kopyaliyordu.
    onceki_alan = (f"ÖNCEKİ SORU: {onceki}\n" if takip and onceki else "")
    kapsam = ("Yalnızca SORU'da sorulanı yanıtla; ÖNCEKİ SORU, SORU'nun "
              "neyi kastettiğini anlaman için var, onu yeniden cevaplama.\n"
              if takip and onceki else "")

    messages.append({
        "role": "user",
        "content": (
            # Pencereler, aramada kullanilan sorguyla seciliyor: takip
            # sorusu tek basina ("peki bu partinin genel baskani kimdi")
            # hangi cumlenin ilgili oldugunu soylemeye yetmiyor.
            f"BAĞLAM:\n{build_context(hits, aranan)}\n\n"
            f"{onceki_alan}"
            f"SORU: {question}\n\n"
            f"{kapsam}"
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