"""Soruyu al, ilgili parcalari getir, yerel LLM ile cevap uret."""

import difflib
import math
import os
import re
import sys
import time

from foundry_client import client, set_primary, with_model
from search import kokler, load_chunks, search_details

TOP_K = int(os.environ.get("LRA_TOP_K", 8))   # ortam degiskeni yalnizca deneyler icin
# Guvenlik tabani: en iyi parca bu skorun altindaysa modele hic sorulmaz.
#
# masaustu_gui dalinda 0.42 idi; o deger karakter tabanli parcalama ve
# ingilizce sorgu onekiyle olculmustu (18 soru). Bu dalda ingest.py paragraf
# parcalama yapiyor ve search.py Turkce sorgu talimati kullaniyor; ikisi de
# skor dagilimini kaydirdi. 105 soruluk sette olculen hal (esik_takip_analiz.py,
# rag_iyilestirme_plani.md Bolum 2.9): konuya yakin ama belgede olmayan sorular
# 0.52-0.69, yani cevaplanabilirlerin cogundan yuksek; tek bir esik iki grubu
# ayiramiyor, onlari model reddediyor. Esik yalnizca acikca konu disi sorulari
# (0.32-0.37) ayikliyor. En dusuk cevaplanabilir soru 0.346 ("Kımız nedir?"),
# yani 0.42 bu parcalamada dogru cevaplari da reddettiriyordu.
MIN_SCORE = float(os.environ.get("LRA_MIN_SCORE", 0.33))   # ortam degiskeni yalnizca deneyler icin
RED_IFADESI = "elimdeki dokümanlarda yok"   # reddetme yanitinin sabit ifadesi
REFUSAL = "Bu bilgi elimdeki dokümanlarda yok."
CHAT_KEYWORD = os.environ.get("LRA_CHAT_MODEL", "qwen2.5-7b")   # ortam degiskeni yalnizca deneyler icin
MAX_TOKENS = 600      # liste soran sorularda 350 token cevabi ortadan kesiyordu
GECMIS_TUR = 2        # modele tasinan onceki soru-cevap sayisi
GECMIS_CEVAP_SINIRI = 180   # gecmisteki cevaplar bu uzunluga kirpilir
FOLLOW_UP_MAX_WORDS = 8     # bu uzunluga kadar olan sorular takip olabilir
# Isaret sozcugu tasimayan kisa sorularda birlesik arama, tek basina aramadan
# en az bu kadar yuksek skor verirse kullanilir. Olcum (esik_takip_analiz.py):
# gercek takip sorularinda fark +0.23..+0.35, konu degisimlerinde medyan
# -0.015. masaustu_gui'de karsilastirma paysizdi (alternatif > mevcut); konu
# degisimlerinde fark gurultu seviyesinde oldugu icin pay olmadan arama yaklasik
# yari yariya onceki sorunun konusuna kayiyor.
FOLLOW_UP_MARGIN = 0.20
# Takip sorusunda onceki soruyu modele de gostermek. masaustu_gui dalinda
# acikti ve istem "onu yeniden cevaplama" diye uyariyordu; bu uyari yetmiyor.
# 105 soruluk sette olculdu (degerlendirmeler/2026-09-18_0408_birlesik.json
# acik, 2026-09-18_0426_birlesik-takip-kapali.json kapali):
#
#                                 acik     kapali
#   tam basari                    %93.3    %95.6
#   cevaplanamaz soruyu reddetme  %68.8    %93.8
#   cevaplanabilir soruda basari  %98.6    %95.9
#
# Acikken model, onceki soruya dayanmayan bir soruda onceki soruyu
# cevapliyor: "asdf qwerty zxcv" sorusuna "Eski Türkçede kurdun adı böri
# idi", "Futbolda ofsayt kuralı nedir?" sorusuna once Malazgirt'i anlatiyor.
# Kapaliyken cevaplanabilir tarafta iki soru kaybediliyor; cevaplanamaz
# sorularda uydurmanin bedeli daha agir oldugu icin varsayilan kapali.
FOLLOW_UP_CONTEXT_TO_MODEL = os.environ.get("LRA_FOLLOW_UP_TO_MODEL", "0") == "1"

YAKIN_ESIK = 0.30     # esigi gecemeyen ama "az kalsin" eslesen sorular

# Turkce olmayan yazi korumasi (H12): model bazen cevabin ortasinda Cince'ye
# geciyor (kontrol seti "Toy nedir?"; kayitli 1586 cevabin 2'sinde goruldu).
# Bu karakterlerden once gelen son tam cumlede kesilir; geriye bu kadardan
# kisa bir sey kalirsa reddedilir.
FOREIGN_SCRIPT = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힯＀-￯]")
MIN_ANSWER_CHARS = 20
# Cevap dogrulama adimi (H13) reddedildi: iki sette de butun kotu cevaplari
# yakaladi ama 11 dogru cevabi da reddetti (Bolum 2.14). evaluate.py raporda
# bu ayari yazdigi icin sabit duruyor.
ANSWER_VERIFICATION = False
VERIFY_PROMPT_NAME = None

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
#
# Isteme reddetme yonergesi EKLEMEK DENENDI VE REDDEDILDI (2026-09-18).
# Cevaplanamaz sorularda model, baglam konuyla ilgili gorundugu icin cevap
# uydurmaya yatkin. Betik: muhammet_ws/olcum_betikleri/red_istemi_deneyi.py
# (32 cevaplanamaz soru; her olcum iki kez tekrarlandi, sonuclar ayni).
#
#   mevcut istem                                       25/32
#   "ilgili bilgi yok" -> "cevabi acikca yazmiyorsa"   24/32
#   + "tahmin etme, reddet"                            26/32
#   + "baska konuyu anlatma, reddet"                   29/32
#
# Son satir tam olcumde uygulandi ve GERI ALINDI: cevaplanamaz reddetme
# %75.0 -> %93.8 cikarken ana set %96.2 -> %93.1'e dustu; sekiz cevaplanabilir
# soru bozuldu ("Çanakkale Deniz Zaferi hangi tarihte kazanılmıştır?" artik
# reddediliyordu). Yalnizca "baska konuyu anlatma" satirini eklemek bile
# dokuz kanarya sorusunun ucunu bozdu. Modeli reddetmeye iten her yonerge
# cevaplanabilir sorulari da kaybettiriyor: 7B modelde reddetme ve cevaplama
# ayni karar, biri sikilastirilmadan digeri gevsetilemiyor.
#
# Ayni deneyde olculen diger kaldiraclar da kotu: baglami daraltmak
# (BAGLAM_ORANI 0.85) 22/32, onceki soruyu modele gostermek 20/32. Takip
# sorusunda cevabin kaynak belgesi degisince reddetme kurali da olculdu
# (takip_kaynak_kaymasi.py): iki uydurma yakaliyor, iki dogru cevabi bozuyor.
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

if CHAT_KEYWORD.startswith("qwen3"):
    # Qwen3 varsayilan olarak cevaptan once dusunme metni uretiyor; bu hem
    # yavas hem MAX_TOKENS'i dolduruyor (rag_iyilestirme_plani.md Bolum 2.3).
    SYSTEM_PROMPT += "\n/no_think"


def strip_thinking(text):
    """Bazi modeller <think>...</think> blogu uretebilir; guvenlik agi.

    Cikti token sinirinda kesilirse kapanis etiketi hic gelmez; o durumda
    <think>'ten sonrasinin tamami dusunme metnidir.
    """
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"<think>.*$", "", text, flags=re.DOTALL)
    return text.strip()


def cut_foreign_script(text):
    """(metin, kesildi_mi). Cince/Japonca/Korece karakterden once biten son
    tam cumleyi birakir."""
    match = FOREIGN_SCRIPT.search(text)
    if not match:
        return text, False
    head = text[:match.start()]
    # Sira sayilari ("19. Tümen", "II. Mehmed") cumle sonu sayilmaz
    ends = [m.end() for m in re.finditer(r"(?<=[a-zçğıöşüâîû)\"'’”])[.!?][\"'’”]?(?=\s|$)", head)]
    return (head[:ends[-1]] if ends else "").strip(), True


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


def warmup_messages():
    """Uygulamanin gonderebilecegi en uzun istem (foundry_client.set_primary).

    Sohbet modeli baglam okuma icin gereken calisma bellegini istemin boyutuna
    gore ayiriyor; bunun gomme modelinden once olmasi gerekiyor. 8 GB'lik
    kartta sira tersine donerse ayni soru ~2.5 sn yerine ~50 sn suruyor
    (foundry_client.set_primary'deki aciklama). Gomme modeli henuz yuklu
    olmadigindan arama yapilmaz, veritabanindaki en uzun parcalar kullanilir
    ve pencereleme uygulanmaz: amac en kotu durumu ayirtmak.
    """
    meta, _matrix, _kokler = load_chunks()
    longest = sorted(meta, key=lambda m: len(m[3]), reverse=True)[:BAGLAM_EN_COK]
    hits = [(0.0, *m) for m in longest]
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"BAĞLAM:\n{build_context(hits)}\n\n"
                "SORU: Bu bölümlerde anlatılan olayların sebepleri ve "
                "sonuçları nelerdir?\n\nTürkçe cevap ver."
            ),
        },
    ]


set_primary(CHAT_KEYWORD, warmup_messages)


def follow_up_query(question, previous_question=None):
    """Kisa takip sorulari icin aramaya gonderilebilecek birlesik metin.

    Gercek secim retrieve_details icinde skorlara bakarak yapiliyor; bu
    fonksiyon dis cagrilar ve raporlama icin duruyor.
    """
    if previous_question and len(question.split()) <= FOLLOW_UP_MAX_WORDS:
        return f"{previous_question} {question}"
    return question


def retrieve_details(question, top_k=TOP_K, search_query=None,
                     previous_question=None):
    """(parcalar, arama_metni, takip_mu, en_iyi_skor) dondur.

    Takip sorusu tek basina aranamaz: "bu hayvan destanlarda hangi rollerde
    gecer?" tek basina arandiginda at belgesini getiriyor. Isaret sozcugu
    tasiyan soruda dogrudan onceki soruyla birlestiriliyor. Isaret sozcugu
    tasimayan kisa sorular da onceki tura dayanabiliyor ("neden
    degistirdiler", "hangi yil"); orada iki sorgu da denenip belirgin bicimde
    daha iyi eslesen kazaniyor.

    Karar hep en iyi skorla veriliyor; hibrit arama acikken ilk parcanin skoru
    bundan dusuk olabilir (search.search_details).
    """
    if search_query is not None:
        hits, best = search_details(search_query, top_k=top_k)
        return hits, search_query, search_query != question, best

    hits, best = search_details(question, top_k=top_k)
    if not previous_question:
        return hits, question, False, best

    birlesik = f"{previous_question} {question}"
    if _isaret_ediyor(question):
        alt_hits, alt_best = search_details(birlesik, top_k=top_k)
        return alt_hits, birlesik, True, alt_best

    # Pay olmadan karsilastirmak (masaustu_gui'deki hali) yeni bir konuya
    # gecildiginde aramayi yaklasik yari yariya onceki sorunun konusuna
    # kaydiriyor: konu degisiminde iki skor arasindaki fark gurultu
    # seviyesinde (medyan -0.015), gercek takip sorularinda +0.23..+0.35.
    if len(question.split()) <= FOLLOW_UP_MAX_WORDS:
        alt_hits, alt_best = search_details(birlesik, top_k=top_k)
        if alt_hits and alt_best - best >= FOLLOW_UP_MARGIN:
            return alt_hits, birlesik, True, alt_best

    return hits, question, False, best


def retrieve(question, top_k=TOP_K, search_query=None, previous_question=None):
    """retrieve_details'in yalnizca parcalari donduren hali."""
    return retrieve_details(question, top_k=top_k, search_query=search_query,
                            previous_question=previous_question)[0]


def answer(question, top_k=TOP_K, search_query=None, history=None,
           stream_cb=None, previous_question=None):
    """(cevap, getirilen_parcalar, gecen_sure) dondur.

    history: [{"soru": ..., "cevap": ...}] seklinde onceki turlar. Hem takip
    sorularinin aranmasinda hem de modele baglam olarak kullanilir.
    previous_question yalnizca onceki soruyu bilen cagrilar icin (evaluate.py).
    search_query verilirse arama dogrudan onunla yapilir.
    stream_cb verilirse, model uretirken metnin o ana kadarki hali bu
    fonksiyona tekrar tekrar gonderilir (arayuzde canli yazim icin).
    """
    result = answer_details(question, top_k=top_k, search_query=search_query,
                            history=history, stream_cb=stream_cb,
                            previous_question=previous_question)
    return result["text"], result["hits"], result["total_sec"]


def answer_details(question, top_k=TOP_K, search_query=None, history=None,
                   stream_cb=None, previous_question=None):
    """answer() ile ayni isi yapip olcum bilgilerini de dondur.

    Anahtarlar: text, hits (modele giden secilmis parcalar), best_score (esik
    bununla karsilastirilir), search_text (aramada kullanilan metin), source
    (cevabin dayandigi belge; redde None), used_follow_up (birlesik arama
    secildi mi), used_llm (esikte reddedildiyse False), foreign_script_cut,
    verified, retrieval_sec, first_token_sec, total_sec.
    """
    started = time.perf_counter()

    # evaluate.py yalnizca onceki soruyu tasiyor. Cevabi bos olan tur aramada
    # kullanilir, modele mesaj olarak gonderilmez (asagida ozet bosken atlanir).
    if previous_question and not history:
        history = [{"soru": previous_question, "cevap": ""}]
    onceki = history[-1]["soru"] if history else None

    hits, aranan, takip, best = retrieve_details(
        question, top_k=top_k, search_query=search_query,
        previous_question=onceki,
    )

    result = {
        "hits": hits,
        "best_score": best,
        "search_text": aranan,
        "used_follow_up": takip,
        "used_llm": False,
        "verified": None,
        "foreign_script_cut": False,
        "source": None,
        "retrieval_sec": time.perf_counter() - started,
        "first_token_sec": None,
    }

    # Esik korumasi: alakali hicbir sey bulunamadiysa modele hic sormuyoruz.
    # Boylece model alakasiz baglamdan cevap uydurma firsati bulamiyor.
    if not hits or best < MIN_SCORE:
        result["text"] = _reddet(hits)
        result["total_sec"] = time.perf_counter() - started
        return result

    # Yalnizca secilen parcalar hem modele gider hem de arayuzde "yanitin
    # dayandigi bolumler" olarak gosterilir; ikisi ayrismasin.
    hits = baglam_parcalari(hits)
    result["hits"] = hits

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for tur in (history or [])[-GECMIS_TUR:]:
        # Uzun cevaplar (ornegin dokuz maddelik bir liste) oldugu gibi
        # tasinirsa model yeni soruyu o listenin icinden cevaplamaya calisiyor
        # ve ozel adlari karistiriyordu; ozeti yetiyor.
        ozet = re.sub(r"\n?\(Kaynak:[^)]*\)", "", tur["cevap"]).strip()
        if not ozet:
            continue          # cevabi bilinmeyen tur (evaluate.py) mesaja girmez
        if len(ozet) > GECMIS_CEVAP_SINIRI:
            ozet = ozet[:GECMIS_CEVAP_SINIRI].rsplit(" ", 1)[0] + "…"
        messages.append({"role": "user", "content": tur["soru"]})
        messages.append({"role": "assistant", "content": ozet})
    # Takip sorusu tek basina anlasilmiyor: "neden degistirdiler" sorusunda
    # model dogru baglami almasina ragmen "bu bilgi dokumanlarda yok"
    # diyordu; gecmis turlarin mesaj olarak tasinmasi tek basina yetmedi.
    # Onceki soru BAGLAM/SORU gibi etiketli bir alan olarak veriliyor:
    # cumle icine gomulu yonergeyi model cevabina kopyaliyordu.
    goster_onceki = FOLLOW_UP_CONTEXT_TO_MODEL and takip and onceki
    onceki_alan = (f"ÖNCEKİ SORU: {onceki}\n" if goster_onceki else "")
    kapsam = ("Yalnızca SORU'da sorulanı yanıtla; ÖNCEKİ SORU, SORU'nun "
              "neyi kastettiğini anlaman için var, onu yeniden cevaplama.\n"
              if goster_onceki else "")

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

    def uret(model_id):
        """Bir cevap uretir; (metin, ilk_token_suresi) dondur.

        Her zaman akisla aliniyor: stream_cb verilmisse arayuze canli yazim
        icin, verilmemisse ilk token suresi olculebilsin diye. Metin ayni.
        """
        istek_basladi = time.perf_counter()
        ilk_token = None
        parcalar = []
        akis = client().chat.completions.create(
            model=model_id, messages=messages, temperature=0.0,
            max_tokens=MAX_TOKENS, stream=True,
        )
        # Akisli uretim: yanit 20-30 saniye surebiliyor, kullanicinin ilk
        # kelimeleri birkac saniyede gormesi bekleyisi katlanilir kiliyor.
        for olay in akis:
            if not olay.choices:
                continue
            yeni_parca = olay.choices[0].delta.content or ""
            if yeni_parca:
                if ilk_token is None:
                    ilk_token = time.perf_counter() - istek_basladi
                parcalar.append(yeni_parca)
                if stream_cb is not None:
                    stream_cb(strip_thinking("".join(parcalar)))
        return strip_thinking("".join(parcalar)), ilk_token

    # with_model: model bellekte degilse yuklenir, "not loaded" hatasinda
    # istek bir kez tekrarlanir. masaustu_gui dalinda bu yoktu ve bilgisayar
    # yeniden baslatildiginda her soru 400 hatasiyla dusuyordu.
    text, result["first_token_sec"] = with_model(CHAT_KEYWORD, uret)
    result["used_llm"] = True

    text, result["foreign_script_cut"] = cut_foreign_script(text)

    # Ozel ad denetimi ve onarimi: model adlari Turkce ekle cekimlerken
    # bozabiliyor ("Türkeş'in" -> "Türkş'in"). Modele yeniden urettirmek bu
    # hatayi tekrarliyor, bu yuzden bozulan adi baglamdaki gercek yazimiyla
    # dogrudan degistiriyoruz.
    text = adlari_onar(text, hits)

    if result["foreign_script_cut"] and len(text.strip()) < MIN_ANSWER_CHARS:
        # Yabanci yazi cevabin basinda basladiysa geriye anlamli bir sey
        # kalmiyor; uydurma birakmaktansa reddetmek daha dogru.
        text = REFUSAL

    if not text:
        text = (
            "Model bu soru için bir yanıt üretemedi. "
            "Soruyu biraz daha açık yazmayı deneyin."
        )

    # Dayanak belgesi kaynak satiri eklenmeden once hesaplaniyor; satirdaki
    # dosya adi sozcuk ortusmesine karismasin.
    if RED_IFADESI not in text.replace("İ", "i").lower():
        dayanak = _dayanak_belgesi(text, hits)
        result["source"] = dayanak[0] if dayanak else None

    result["text"] = kaynagi_duzelt(text, hits)
    result["total_sec"] = time.perf_counter() - started
    return result


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