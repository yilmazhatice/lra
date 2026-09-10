"""Soruyu al, ilgili parcalari getir, yerel LLM ile cevap uret."""

import re
import sys
import time

from foundry_client import client, find_model
from search import search

TOP_K = 3
MIN_SCORE = 0.42      # bu esigin altinda en iyi parca varsa hic cevap uretme
CHAT_KEYWORD = "qwen2.5-7b"
MAX_TOKENS = 350

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


def strip_thinking(text):
    """Bazi modeller <think>...</think> blogu uretebilir; guvenlik agi.

    Cikti token sinirinda kesilirse kapanis etiketi hic gelmez; o durumda
    <think>'ten sonrasinin tamami dusunme metnidir.
    """
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"<think>.*$", "", text, flags=re.DOTALL)
    return text.strip()


def build_context(hits):
    return "\n\n".join(
        f"[{doc_name} / parca {chunk_idx}]\n{text}"
        for _score, _cid, doc_name, chunk_idx, text in hits
    )


def answer(question, top_k=TOP_K, search_query=None):
    """(cevap, getirilen_parcalar, gecen_sure) dondur.

    search_query verilirse arama onunla yapilir, cevap yine question'a gore
    uretilir. Kisa takip sorularinda onceki soruyu baglam olarak tasimak icin.
    """
    started = time.perf_counter()
    hits = search(search_query or question, top_k=top_k)

    # Esik korumasi: alakali hicbir sey bulunamadiysa modele hic sormuyoruz.
    # Boylece model alakasiz baglamdan cevap uydurma firsati bulamiyor.
    if not hits or hits[0][0] < MIN_SCORE:
        return (
            "Bu bilgi elimdeki dokümanlarda yok.",
            hits,
            time.perf_counter() - started,
        )

    resp = client().chat.completions.create(
        model=find_model(CHAT_KEYWORD),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"BAĞLAM:\n{build_context(hits)}\n\n"
                    f"SORU: {question}\n\n"
                    "Türkçe cevap ver."
                ),
            },
        ],
        temperature=0.0,
        max_tokens=MAX_TOKENS,
    )

    text = strip_thinking(resp.choices[0].message.content or "")
    if not text:
        text = (
            "Model bu soru için bir yanıt üretemedi. "
            "Soruyu biraz daha açık yazmayı deneyin."
        )

    return text, hits, time.perf_counter() - started


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