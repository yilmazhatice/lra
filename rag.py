"""Soruyu al, ilgili parcalari getir, yerel LLM ile cevap uret."""

import os
import re
import sys
import time

from foundry_client import client, set_primary, with_model
from search import load_chunks, search_details

TOP_K = int(os.environ.get("LRA_TOP_K", 3))   # ortam degiskeni yalnizca deneyler icin
# Guvenlik tabani: en iyi parca bu skorun altindaysa modele hic sorulmaz.
# Olcum (esik_takip_analiz.py, Turkce sorgu talimatiyla): konuya yakin ama
# belgede olmayan sorular 0.52-0.69 skor aliyor, cevaplanabilirlerin cogundan
# yuksek; tek bir esik iki grubu ayiramiyor, onlari model reddediyor. Esik
# yalnizca acikca konu disi sorulari (0.32-0.37) ayiklar. En dusuk
# cevaplanabilir soru 0.346 ("Kımız nedir?").
MIN_SCORE = 0.33
CHAT_KEYWORD = os.environ.get("LRA_CHAT_MODEL", "qwen2.5-7b")   # ortam degiskeni yalnizca deneyler icin
MAX_TOKENS = 350
FOLLOW_UP_MAX_WORDS = 8
# Takip sorusunda onceki soruyla birlesik arama, tek basina aramadan en az bu
# kadar yuksek skor verirse kullanilir. Olcum (muhammet_ws/olcum_betikleri/
# esik_takip_analiz.py): gercek takip sorularinda fark +0.23..+0.35, konu
# degisimlerinde medyan -0.015. Esikten bagimsiz oldugu icin esik degisince
# bozulmuyor.
FOLLOW_UP_MARGIN = 0.20
# Takip sorusunda onceki soruyu modele de gostermek (H9). Kapali: olcumde
# (Faz 5b) model "SORU, ÖNCEKİ SORU'nun devamıdır" yonlendirmesiyle belgede
# olmayan sebep uydurdu ve anlamsiz girdiye onceki soruyu cevapladi; tam
# basari %93.3 -> %91.1 (rag_iyilestirme_plani.md Bolum 2.11).
FOLLOW_UP_CONTEXT_TO_MODEL = False
REFUSAL = "Bu bilgi elimdeki dokümanlarda yok."
# Cevap dogrulama adimi (H13): uretilen cevap, ayni modele ikinci ve kisa bir
# istekle "BAGLAM bu cevabi soru icin acikca destekliyor mu?" diye sorulur;
# HAYIR ise reddedilir. Eslik bu uydurmalari ayiramiyor (konuya yakin tuzak
# 0.66, yanlis konuyu cevaplayan takip sorusu 0.44; Bolum 2.13).
ANSWER_VERIFICATION = os.environ.get("LRA_VERIFY", "0") == "1"   # ortam degiskeni yalnizca deneyler icin
# Turkce olmayan yazi korumasi (H12): model bazen cevabin ortasinda Cince'ye
# geciyor (kontrol seti "Toy nedir?"). Bu karakterlerden once gelen son tam
# cumlede kesilir; geriye bu kadardan kisa bir sey kalirsa reddedilir.
FOREIGN_SCRIPT = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힯＀-￯]")
MIN_ANSWER_CHARS = 20

SYSTEM_PROMPT = """Sen bir doküman asistanısın. Sana BAĞLAM olarak birkaç
paragraf ve bir SORU verilir. Görevin, sorunun cevabını BAĞLAM'da bulup
Türkçe yazmaktır.

BAĞLAM soruyla ilgili bilgi içeriyorsa cevap ver. Kısmen içeriyorsa elindeki
kadarını yaz. Hiç ilgili bilgi yoksa yalnızca şu cümleyi yaz:
Bu bilgi elimdeki dokümanlarda yok.

Kurallar:
- Yalnızca BAĞLAM'daki bilgiyi kullan, kendi genel bilgini ekleme.
- Kısa yaz: en fazla dört cümle.
- Bağlamdaki köşeli parantezli etiketleri cevabına yazma.
- Cevabın son satırında kaynağı belirt.

Cevap biçimi şöyle olmalı:

Kurdun eski Türkçedeki adı böri idi.
(Kaynak: turk-kulturunde-kurt.md)"""
# Istem kaynak satiri istemeye devam ediyor ama modelin yazdigi kaynak
# kullanilmiyor: satir silinip kaynagi pick_source belirliyor. Kaynak kurali
# istemden cikarilinca model basit sorulari da reddetmeye basladi (Faz 5a:
# 3 soru kaybi); bu bicimi tanidigi icin istem korunuyor.

if CHAT_KEYWORD.startswith("qwen3"):
    # Qwen3 varsayilan olarak cevaptan once dusunme metni uretiyor; bu hem
    # yavas hem MAX_TOKENS'i dolduruyor (rag_iyilestirme_plani.md Bolum 2.3).
    SYSTEM_PROMPT += "\n/no_think"

# Modelin yazdigi kaynak satirlari ("(Kaynak: x.md)", "Kaynak: x.md")
SOURCE_LINE = re.compile(r"\(?\s*Kaynak\s*:+[^\n]*", re.IGNORECASE)
REFUSAL_CORE = "elimdeki dokümanlarda yok"


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


VERIFY_PROMPTS = {
    # Ilk surum (Faz 5.6 H13): uc HAYIR kosulu. Kotu cevaplarin hepsini (5/5)
    # yakaladi ama dogru cevaplarin 11'ini de reddetti (Bolum 2.14).
    "genis": """Sen bir doğrulayıcısın. Sana BAĞLAM, SORU ve bir CEVAP verilir.
Görevin, CEVAP'ın SORU'yu BAĞLAM'daki bilgiyle doğru biçimde cevaplayıp
cevaplamadığına karar vermektir.

HAYIR yaz, eğer:
- SORU'da sorulan kişi, olay, kurum ya da dönem BAĞLAM'da geçmiyorsa,
- CEVAP, SORU'da sorulandan başka bir kişi, olay, kurum ya da dönemden
  bahsediyorsa,
- CEVAP'taki bilgi BAĞLAM'da yoksa ya da BAĞLAM'la çelişiyorsa.

Aksi halde EVET yaz. Yalnızca tek kelime yaz: EVET ya da HAYIR.""",
    # H13b: varsayilan EVET; yalnizca uydurmanin gorulen iki bicimi (baska bir
    # kisi/olay/doneme kayma) icin HAYIR.
    "dar": """Sen bir doğrulayıcısın. Sana BAĞLAM, SORU ve bir CEVAP verilir.

Varsayılan kararın EVET'tir. Yalnızca şu durumda HAYIR yaz:
CEVAP, SORU'da sorulan kişi, olay, kurum ya da dönem hakkında değil de
başka bir kişi, olay, kurum ya da dönem hakkındaysa.

Örnek: SORU bir devletin yıkılışını soruyor, CEVAP başka bir devletin
yıkılışını anlatıyorsa HAYIR. SORU bir savaştaki komutanı soruyor, CEVAP
başka bir savaştaki görevi anlatıyorsa HAYIR.

Yalnızca tek kelime yaz: EVET ya da HAYIR.""",
}
VERIFY_PROMPT_NAME = os.environ.get("LRA_VERIFY_PROMPT", "dar")   # ortam degiskeni yalnizca deneyler icin


def verify_answer(question, text, hits, previous_question=None):
    """Cevap baglamla soruyu destekliyorsa True. Model cagrisi yapar.

    Onceki soru yalnizca dogrulayiciya gosterilir ("ne zaman yıkıldı?" gibi
    eksik sorularda neyin soruldugunu anlamak icin). Cevabi ureten modele
    gostermek uydurma getirmisti (Faz 5b); dogrulayici ise yalnizca
    reddedebilir.
    """
    question_block = f"SORU: {question}"
    if previous_question:
        question_block = (
            f"ÖNCEKİ SORU: {previous_question}\n{question_block}\n"
            "(ÖNCEKİ SORU yalnızca SORU eksikse neyin sorulduğunu anlamak içindir; "
            "SORU kendi başına anlaşılırsa ÖNCEKİ SORU'yu dikkate alma.)"
        )
    messages = [
        {"role": "system", "content": VERIFY_PROMPTS[VERIFY_PROMPT_NAME]},
        {"role": "user", "content": (
            f"BAĞLAM:\n{build_context(hits)}\n\n{question_block}\n\n"
            f"CEVAP: {SOURCE_LINE.sub('', text).strip()}\n\nEVET mi HAYIR mı?"
        )},
    ]
    resp = with_model(CHAT_KEYWORD, lambda model_id: client().chat.completions.create(
        model=model_id, messages=messages, temperature=0.0, max_tokens=4,
    ))
    verdict = strip_thinking(resp.choices[0].message.content or "")
    verdict = verdict.replace("I", "ı").replace("İ", "i").upper()
    return not verdict.startswith("HAYIR")


def _content_words(text):
    """Kaba Turkce kok kumesi: kucuk harf, 5 harflik onek, sayilar oldugu gibi.

    "yenilmiştir" ve "yenilgi" ayni koke duser; ekli ozel adlar ("Timur'a")
    kesme isaretinden bolunur.
    """
    text = text.replace("İ", "i").replace("I", "ı").lower()
    words = re.findall(r"\w+", text)
    return {w if w.isdigit() else w[:5] for w in words if w.isdigit() or len(w) >= 3}


def pick_source(text, question, hits):
    """Cevabin dayandigi parcanin belgesini bul.

    Model kaynagi kendisi yazinca yanlis belgeyi gosterebiliyor ya da red
    cevabina kaynak ekliyordu (rag_iyilestirme_plani.md Bolum 2.10). Burada
    cevabin getirilen parcalarla ortusmesine bakiliyor; sorunun kendi
    kelimeleri sayilmiyor, cevabin ekledigi bilgi nereden geldiyse o secilir.
    Esitlikte arama sirasi daha iyi olan parca kazanir.
    """
    answer_words = _content_words(text) - _content_words(question) or _content_words(text)
    best_doc, best_overlap = None, 0
    for _score, _cid, doc_name, _idx, chunk in hits:
        overlap = len(answer_words & _content_words(chunk))
        if overlap > best_overlap:
            best_doc, best_overlap = doc_name, overlap
    return best_doc


def build_context(hits):
    return "\n\n".join(
        f"[{doc_name} / parca {chunk_idx}]\n{text}"
        for _score, _cid, doc_name, chunk_idx, text in hits
    )


def warmup_messages():
    """Uygulamanin gonderebilecegi en uzun istem (foundry_client.set_primary).

    Sohbet modeli baglam okuma icin gereken calisma bellegini istemin
    boyutuna gore ayiriyor; bunun gomme modelinden once olmasi gerekiyor.
    Gomme modeli henuz yuklu olmadigindan arama yapilmaz, veritabanindaki
    en uzun parcalar kullanilir.
    """
    meta, _ = load_chunks()
    longest = sorted(meta, key=lambda m: len(m[3]), reverse=True)[:TOP_K]
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
    """Arayuzlerin aramaya gonderecegi metin.

    Kisa takip sorulari ("bunun sebebi ne?") tek baslarina aranamaz; arama
    icin bir onceki soru da eklenir. Cevap yine yalnizca yeni soruya gore
    uretilir. app.py, masaustu.py ve evaluate.py ayni kurali kullansin diye
    burada.
    """
    if previous_question and len(question.split()) <= FOLLOW_UP_MAX_WORDS:
        return f"{previous_question} {question}"
    return question


def retrieve(question, top_k=TOP_K, search_query=None):
    """retrieve_details'in yalnizca parcalari donduren hali."""
    return retrieve_details(question, top_k=top_k, search_query=search_query)[0]


def retrieve_details(question, top_k=TOP_K, search_query=None):
    """Soruyu tek basina ve (verildiyse) search_query ile ara, uygun olani sec.

    (parcalar, birlesik_arama_kullanildi_mi, en_iyi_vektor_skoru) dondurur.
    Karar hep en iyi vektor skoruyla verilir; hibrit aramada ilk parcanin
    skoru bundan dusuk olabilir (search.search_details).

    search_query her zaman kullanilirsa yeni konuya gecildiginde arama onceki
    sorunun konusuna kayiyor: "böri nedir" sonrasi "fatih kimdir" sorulunca
    kurt belgesi geliyor. Onceki soru yalnizca soru tek basina eksik kaldiginda
    ("sonucu ne oldu?") gerekli; bu durumda birlesik arama belirgin bicimde
    daha iyi eslesir. Eskiden karar "tek basina skor esigin altinda mi" diye
    veriliyordu; sorgu talimati skorlari yukseltince kisa takip sorulari da
    esigi gecip onceki soruyu kullanmaz olmustu.
    """
    hits, best = search_details(question, top_k=top_k)
    if search_query and search_query != question:
        combined, combined_best = search_details(search_query, top_k=top_k)
        if combined and combined_best - best >= FOLLOW_UP_MARGIN:
            return combined, True, combined_best
    return hits, False, best


def answer(question, top_k=TOP_K, previous_question=None, search_query=None):
    """(cevap, getirilen_parcalar, gecen_sure) dondur.

    previous_question verilirse kisa takip sorulari icin arama onceki soruyla
    birlikte de yapilir (follow_up_query). search_query eski cagrilar icin.
    """
    result = answer_details(question, top_k=top_k, previous_question=previous_question,
                            search_query=search_query)
    return result["text"], result["hits"], result["total_sec"]


def answer_details(question, top_k=TOP_K, previous_question=None, search_query=None):
    """answer() ile ayni isi yapip olcum bilgilerini de dondur.

    Anahtarlar: text, hits, best_score (en iyi vektor skoru; esik bununla
    karsilastirilir), source (koda gore cevabin belgesi, red ve esikte
    redde None), used_follow_up (birlesik arama secildi mi), used_llm (esikte
    reddedildiyse False), retrieval_sec, first_token_sec (model istegi
    basindan ilk token'a kadar, model cagrilmadiysa None), total_sec.
    """
    started = time.perf_counter()
    if search_query is None:
        search_query = follow_up_query(question, previous_question)
    hits, used_follow_up, best_score = retrieve_details(question, top_k=top_k, search_query=search_query)
    result = {
        "hits": hits,
        "best_score": best_score,
        "verified": None,
        "foreign_script_cut": False,
        "source": None,
        "used_follow_up": used_follow_up,
        "used_llm": False,
        "retrieval_sec": time.perf_counter() - started,
        "first_token_sec": None,
    }

    # Esik korumasi: alakali hicbir sey bulunamadiysa modele hic sormuyoruz.
    # Boylece model alakasiz baglamdan cevap uydurma firsati bulamiyor.
    if not hits or best_score < MIN_SCORE:
        result["text"] = REFUSAL
        result["total_sec"] = time.perf_counter() - started
        return result

    # Takip sorusunda ("hangi yılda?") model neyin sorulduğunu ancak onceki
    # soruyla anlayabilir; arama zaten onunla yapildiysa modele de gosterilir.
    # Takip olmayan sorularda istem degismez.
    if FOLLOW_UP_CONTEXT_TO_MODEL and used_follow_up and previous_question:
        question_block = (
            f"ÖNCEKİ SORU: {previous_question}\n"
            f"SORU: {question}\n"
            "SORU, ÖNCEKİ SORU'nun devamıdır; SORU'da eksik kalan konuyu "
            "ÖNCEKİ SORU'dan anla."
        )
    else:
        question_block = f"SORU: {question}"
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"BAĞLAM:\n{build_context(hits)}\n\n"
                f"{question_block}\n\n"
                "Türkçe cevap ver."
            ),
        },
    ]
    def request(model_id):
        # Akisla aliniyor ki ilk token suresi olculebilsin; metin ayni.
        request_started = time.perf_counter()
        first_token = None
        parts = []
        stream = client().chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=0.0,
            max_tokens=MAX_TOKENS,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                if first_token is None:
                    first_token = time.perf_counter() - request_started
                parts.append(chunk.choices[0].delta.content)
        return "".join(parts), first_token

    raw, result["first_token_sec"] = with_model(CHAT_KEYWORD, request)
    result["used_llm"] = True

    text = SOURCE_LINE.sub("", strip_thinking(raw)).strip()
    text, result["foreign_script_cut"] = cut_foreign_script(text)
    if result["foreign_script_cut"]:
        text = SOURCE_LINE.sub("", text).strip()
        if len(text) < MIN_ANSWER_CHARS:
            text = REFUSAL
    result["verified"] = None
    if not text:
        text = (
            "Model bu soru için bir yanıt üretemedi. "
            "Soruyu biraz daha açık yazmayı deneyin."
        )
    elif REFUSAL_CORE in text.replace("İ", "i").lower():
        # Red cevabina kaynak eklenmez
        if len(text) <= len(REFUSAL) + 5:
            text = REFUSAL
    else:
        if ANSWER_VERIFICATION:
            result["verified"] = verify_answer(question, text, hits, previous_question)
        if result["verified"] is False:
            text = REFUSAL
        else:
            result["source"] = pick_source(text, question, hits)
            if result["source"]:
                text = f"{text}\n\n(Kaynak: {result['source']})"

    result["text"] = text
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