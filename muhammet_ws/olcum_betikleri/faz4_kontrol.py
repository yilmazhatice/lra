"""Faz 4c: hibrit aramanin gercek kodla modelsiz kontrolu.

search.HYBRID_SEARCH acik/kapali iki durum karsilastirilir:
  1) tekil sorular: dogru parca sirasi (prototip: vektor 58/64, hibrit 61/65)
  2) karar degismezligi: en iyi vektor skoru ve takip aramasi secimi iki
     durumda ayni mi (esik ve takip farki kurali bunlarla calisiyor)
  3) senaryolardaki takip ve konu degisimi sorulari
  4) yapay konu degisimleri (her soru baska belgeden bir sorudan sonra)
Kullanim: python faz4_kontrol.py
"""
import os, sys

LRA = r"C:\Workspace\microsoft_ws\lra"
sys.path.insert(0, LRA); os.chdir(LRA)

import eval_set
import search
from evaluate import evidence_rank
from rag import follow_up_query, retrieve_details

ALL = 10**6
answerable = [c for c in eval_set.SORULAR if c.get("belge")]
unanswerable = [c for c in eval_set.SORULAR if not c.get("belge")]
ozel_ids = {c["id"] for c in answerable if c.get("kategori") == "ozel_ad"}

scenario = [(sc["id"], sc["tip"], sc["sorular"][-1], sc["sorular"][-2]["soru"])
            for sc in eval_set.SENARYOLAR]
synthetic = []
for i, c in enumerate(answerable):
    for j in range(1, len(answerable)):
        prev = answerable[(i + 7 * j) % len(answerable)]
        if prev["belge"].split("|")[0] not in c["belge"]:
            synthetic.append((c["id"], c, prev["soru"]))
            break


def run(hybrid):
    search.HYBRID_SEARCH = hybrid
    out = {"tekil": {}, "cevapsiz": {}, "senaryo": {}, "yapay": {}}
    for c in answerable:
        hits, used, best = retrieve_details(c["soru"], top_k=ALL)
        out["tekil"][c["id"]] = (evidence_rank(hits, c), used, round(best, 6))
    for c in unanswerable:
        hits, used, best = retrieve_details(c["soru"], top_k=ALL)
        out["cevapsiz"][c["id"]] = (None, used, round(best, 6))
    for sid, tip, last, prev in scenario:
        hits, used, best = retrieve_details(last["soru"], top_k=ALL,
                                            search_query=follow_up_query(last["soru"], prev))
        rank = evidence_rank(hits, last) if last.get("belge") else None
        out["senaryo"][sid] = (rank, used, round(best, 6))
    for sid, c, prev in synthetic:
        hits, used, best = retrieve_details(c["soru"], top_k=ALL, search_query=follow_up_query(c["soru"], prev))
        out["yapay"][sid] = (evidence_rank(hits, c), used, round(best, 6))
    return out


def summary(group, ids=None):
    rows = [v for k, v in group.items() if ids is None or k in ids]
    ranks = [r for r, _u, _b in rows]
    return (sum(r == 1 for r in ranks), sum(r is not None and r <= 3 for r in ranks), len(ranks))


vec, hyb = run(False), run(True)

print("== 1) Dogru parca sirasi (hit@1 / hit@3 / n)")
for label, key, ids in [("tekil cevaplanabilir", "tekil", None), ("  ozel_ad", "tekil", ozel_ids),
                        ("senaryo takip", "senaryo", {s[0] for s in scenario if s[1] == "takip"}),
                        ("senaryo konu degisimi", "senaryo", {s[0] for s in scenario if s[1] == "konu_degisimi"}),
                        ("yapay konu degisimi", "yapay", None)]:
    print(f"   {label:24} vektor {summary(vec[key], ids)}   hibrit {summary(hyb[key], ids)}")

print("\n== 2) Karar degismezligi (en iyi vektor skoru ve takip aramasi secimi)")
for key in ("tekil", "cevapsiz", "senaryo", "yapay"):
    diff = [k for k in vec[key] if vec[key][k][1:] != hyb[key][k][1:]]
    print(f"   {key:10} {len(vec[key])} soru, farkli karar: {len(diff)} {diff[:5]}")

print("\n== 3) Sira degisen sorular (vektor -> hibrit)")
for key in ("tekil", "senaryo", "yapay"):
    better = [(k, vec[key][k][0], hyb[key][k][0]) for k in vec[key]
              if (hyb[key][k][0] or 99) < (vec[key][k][0] or 99)]
    worse = [(k, vec[key][k][0], hyb[key][k][0]) for k in vec[key]
             if (hyb[key][k][0] or 99) > (vec[key][k][0] or 99)]
    print(f"   {key:8} iyilesen {better}")
    print(f"   {'':8} kotulesen {worse}")
