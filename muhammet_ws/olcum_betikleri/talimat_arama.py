"""Sorgu talimati bicimlerinin yalnizca arama uzerindeki etkisi (model yok).

eval_set'in tekil sorulariyla her talimat bicimi icin:
  hit@1, hit@3, MRR           dogru parcanin sirasi (65 cevaplanabilir soru)
  ayrim (AUC)                 rastgele bir cevaplanabilir sorunun en iyi skoru,
                              rastgele bir cevaplanamaz sorununkinden yuksek mi
                              (1.0 = tek esikle kusursuz ayrilir, 0.5 = ayrilmaz)
  esik ustu cevapsiz          en iyi skoru MIN_SCORE'u gecen cevaplanamaz soru
  takip tek basina esik ustu  "sonucu ne oldu?" gibi takip sorularinin kendi
                              skoru MIN_SCORE'u geciyor mu (gecerse rag.retrieve
                              onceki soruyu hic kullanmaz)
Kullanim: python talimat_arama.py
"""
import os, sys

LRA = r"C:\Workspace\microsoft_ws\lra"
sys.path.insert(0, LRA); os.chdir(LRA)

import search
import eval_set

# Faz 2'deki olcum vektor sirasiyla yapildi; hibrit arama (Faz 4) kapali tutulur.
search.HYBRID_SEARCH = False
from evaluate import evidence_rank
from rag import MIN_SCORE

VARIANTS = {
    "talimat yok (Faz 1)": None,
    "resmi: ...\\nQuery:": "Instruct: Given a question, retrieve passages that answer the question\nQuery:{q}",
    "bosluklu: ...\\nQuery: ": "Instruct: Given a question, retrieve passages that answer the question\nQuery: {q}",
    "Turkce belge vurgulu": ("Instruct: Given a Turkish question about Turkish history and culture, "
                             "retrieve the paragraph that answers it\nQuery:{q}"),
    "Turkce talimat": "Instruct: Soruyu cevaplayan paragrafı bul\nQuery:{q}",
}

answerable = [c for c in eval_set.SORULAR if c.get("belge")]
unanswerable = [c for c in eval_set.SORULAR if not c.get("belge")]
followups = [s["sorular"][-1]["soru"] for s in eval_set.SENARYOLAR if s["tip"] in ("takip", "takip_cevapsiz")]

original = search.embed_query


def run(template):
    search.embed_query = (original if template is None else
                          lambda q: original.__wrapped__(template.format(q=q)))
    ranks, top_ans, top_un = [], [], []
    for case in answerable:
        hits = search.search(case["soru"], top_k=10**6)
        ranks.append(evidence_rank(hits, case))
        top_ans.append(hits[0][0])
    for case in unanswerable:
        top_un.append(search.search(case["soru"], top_k=1)[0][0])
    follow = [search.search(q, top_k=1)[0][0] for q in followups]
    n = len(answerable)
    auc = sum((a > u) + 0.5 * (a == u) for a in top_ans for u in top_un) / (len(top_ans) * len(top_un))
    return {
        "hit@1": 100 * sum(r == 1 for r in ranks) / n,
        "hit@3": 100 * sum(r is not None and r <= 3 for r in ranks) / n,
        "MRR": sum(1 / r for r in ranks if r) / n,
        "AUC": auc,
        "cevaplanabilir esik alti": sum(s < MIN_SCORE for s in top_ans),
        "cevapsiz esik ustu": sum(s >= MIN_SCORE for s in top_un),
        "takip tek basina esik ustu": f"{sum(s >= MIN_SCORE for s in follow)}/{len(follow)}",
        "skor ort (cevaplanabilir/cevapsiz)": f"{sum(top_ans)/n:.3f} / {sum(top_un)/len(top_un):.3f}",
    }


if __name__ == "__main__":
    # embed_query'nin talimat eklemeden cagrilabilen hali: QUERY_INSTRUCTION'i
    # gecici olarak kapatip orijinal fonksiyonu kullan.
    def raw(q):
        saved = search.QUERY_INSTRUCTION
        search.QUERY_INSTRUCTION = None
        try:
            return original(q)
        finally:
            search.QUERY_INSTRUCTION = saved
    original.__wrapped__ = raw
    base = raw

    print(f"{len(answerable)} cevaplanabilir, {len(unanswerable)} cevaplanamaz tekil soru, "
          f"{len(followups)} takip sorusu; esik {MIN_SCORE}\n")
    for name, template in VARIANTS.items():
        search.embed_query = base if template is None else (lambda q, t=template: raw(t.format(q=q)))
        # run() embed_query'yi yeniden atamasin diye dogrudan olc
        ranks, top_ans, top_un = [], [], []
        for case in answerable:
            hits = search.search(case["soru"], top_k=10**6)
            ranks.append(evidence_rank(hits, case)); top_ans.append(hits[0][0])
        for case in unanswerable:
            top_un.append(search.search(case["soru"], top_k=1)[0][0])
        follow = [search.search(q, top_k=1)[0][0] for q in followups]
        n = len(answerable)
        auc = sum((a > u) + 0.5 * (a == u) for a in top_ans for u in top_un) / (len(top_ans) * len(top_un))
        print(f"{name:28} hit@1 {100*sum(r == 1 for r in ranks)/n:5.1f}  "
              f"hit@3 {100*sum(r is not None and r <= 3 for r in ranks)/n:5.1f}  "
              f"MRR {sum(1/r for r in ranks if r)/n:.3f}  AUC {auc:.3f}  "
              f"cevaplanabilir<esik {sum(s < MIN_SCORE for s in top_ans):2}  "
              f"cevapsiz>=esik {sum(s >= MIN_SCORE for s in top_un):2}/{len(top_un)}  "
              f"takip>=esik {sum(s >= MIN_SCORE for s in follow)}/{len(follow)}  "
              f"skor ort {sum(top_ans)/n:.3f}/{sum(top_un)/len(top_un):.3f}", flush=True)
