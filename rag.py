"""Soruyu al, ilgili parcalari getir, yerel LLM ile cevap uret."""

import re
import sys
import time

from openai import OpenAI

from foundry_client import base_url, find_model
from search import search

TOP_K = 3
MIN_SCORE = 0.45      # bu esigin altinda en iyi parca varsa hic cevap uretme
CHAT_KEYWORD = "qwen3-4b"

SYSTEM_PROMPT = """Sen bir doküman asistanısın. Kullanıcının sorusunu, \
sana verilen BAĞLAM bölümündeki bilgilere dayanarak Türkçe cevaplarsın.

Kurallar:
- Yalnızca BAĞLAM'daki bilgiyi kullan. Kendi genel bilgini kullanma.
- En fazla 5 cümle yaz. Uzatma, madde madde açıklama yapma.
- BAĞLAM soruyu cevaplamaya yetmiyorsa uydurma; şunu yaz: \
"Bu bilgi elimdeki dokümanlarda yok."
- Cevabını, BAĞLAM'da kullandığın parçanın köşeli parantez içindeki \
gerçek dosya adıyla bitir. Örnek: (Kaynak: 03.md)

/no_think"""

_client = OpenAI(base_url=base_url(), api_key="not-needed")


def strip_thinking(text):
    """Qwen modelleri bazen <think>...</think> blogu uretir; onu ayikla."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def build_context(hits):
    return "\n\n".join(
        f"[{doc_name} / parca {chunk_idx}]\n{text}"
        for _score, _cid, doc_name, chunk_idx, text in hits
    )


def answer(question, top_k=TOP_K):
    """(cevap, getirilen_parcalar, gecen_sure) dondur."""
    started = time.perf_counter()
    hits = search(question, top_k=top_k)

    # Esik korumasi: alakali hicbir sey bulunamadiysa modele hic sormuyoruz.
    # Boylece model alakasiz baglamdan cevap uydurma firsati bulamiyor.
    if not hits or hits[0][0] < MIN_SCORE:
        return (
            "Bu bilgi elimdeki dokümanlarda yok.",
            hits,
            time.perf_counter() - started,
        )

    resp = _client.chat.completions.create(
        model=find_model(CHAT_KEYWORD),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"BAĞLAM:\n{build_context(hits)}\n\nSORU: {question}",
            },
        ],
        temperature=0.2,
        max_tokens=400,
    )
    text = strip_thinking(resp.choices[0].message.content or "")
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