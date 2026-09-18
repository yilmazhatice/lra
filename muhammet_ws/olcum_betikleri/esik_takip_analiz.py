"""Faz 3 icin modelsiz analiz: esik degeri ve takip sorusu kurali.

1) Skor dagilimi: tekil sorularda en iyi parca skoru. Her esik degeri icin
   kac cevaplanabilir soru esikte reddedilir, kac cevaplanamaz soru esigi gecer.
2) Takip kurali: onceki soru olan aramada hangi aramanin kullanilacagi.
   - mevcut   : soru tek basina esigi gecemezse birlesik arama (rag.retrieve)
   - fark m   : birlesik aramanin en iyi skoru tek basina aramadan en az m
                yuksekse birlesik arama, degilse tek basina arama
   - birlesim : iki aramanin sonuclari birlestirilir (parca basina en yuksek skor)
   - hep birl.: her zaman birlesik arama (Faz 0 oncesi arayuz davranisi)
   Olculen gruplar:
   - takip       : senaryolardaki 5 gercek takip sorusu (dogru parca sirasi)
   - degisim     : senaryolardaki 4 konu degisimi (dogru parca sirasi)
   - yapay deg.  : 65 cevaplanabilir tekil soru, baska belgeden bir sorudan
                   sonra sorulmus gibi (kural konu degisiminde aramayi bozuyor mu)
   - cevapsiz son: cevaplanamaz sorular, belgeden bir sorudan sonra (esigi geciyor mu)
Kullanim: python esik_takip_analiz.py
"""
import os, sys

LRA = r"C:\Workspace\microsoft_ws\lra"
sys.path.insert(0, LRA); os.chdir(LRA)

import eval_set
import search as search_module
from evaluate import evidence_rank
from rag import MIN_SCORE, follow_up_query
from search import search

# Bu analiz Faz 3'te vektor sirasiyla yapildi; skor = ilk parcanin skoru
# varsayimi hibrit aramada gecerli degil (Faz 4). Tekrari icin vektor sirasi.
search_module.HYBRID_SEARCH = False

ALL = 10**6
cache = {}


def s(text):
    if text not in cache:
        cache[text] = search(text, top_k=ALL)
    return cache[text]


def merge(a, b):
    best = {}
    for hit in a + b:
        if hit[1] not in best or hit[0] > best[hit[1]][0]:
            best[hit[1]] = hit
    return sorted(best.values(), key=lambda h: h[0], reverse=True)


def choose(rule, question, previous):
    query = follow_up_query(question, previous)
    alone = s(question)
    if query == question:
        return alone
    combined = s(query)
    if rule == "mevcut":
        return alone if alone[0][0] >= MIN_SCORE else combined
    if rule == "birlesim":
        return merge(alone, combined)
    if rule == "hep birlesik":
        return combined
    margin = float(rule.split()[1])
    return combined if combined[0][0] - alone[0][0] >= margin else alone


answerable = [c for c in eval_set.SORULAR if c.get("belge")]
unanswerable = [c for c in eval_set.SORULAR if not c.get("belge")]

# ------------------------------------------------------------ 1) skor dagilimi
print("== 1) Tekil sorularda en iyi skor (Turkce talimat acik)\n")
ans_scores = sorted((s(c["soru"])[0][0], c["id"], evidence_rank(s(c["soru"]), c)) for c in answerable)
un_scores = sorted(((s(c["soru"])[0][0], c["id"], c.get("kategori")) for c in unanswerable), reverse=True)
print("En dusuk 8 cevaplanabilir (skor, id, dogru parca sirasi):")
for x in ans_scores[:8]:
    print(f"   {x[0]:.3f}  {x[1]:12} sira {x[2]}")
print("Cevaplanamaz, yuksekten dusuge (skor, id, kategori):")
for x in un_scores:
    print(f"   {x[0]:.3f}  {x[1]:12} {x[2]}")

print("\nEsik | cevaplanabilir esikte red (65) | cevaplanamaz esigi gecen (10)")
for t in [0.30, 0.32, 0.34, 0.36, 0.38, 0.40, 0.42, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70]:
    fr = sum(x[0] < t for x in ans_scores)
    fp = sum(x[0] >= t for x in un_scores)
    print(f"{t:.2f} | {fr:2} | {fp:2}")

# --------------------------------------------------------- 2) takip kurali
scen_follow = [(sc["sorular"][-1], sc["sorular"][-2]["soru"]) for sc in eval_set.SENARYOLAR if sc["tip"] == "takip"]
scen_change = [(sc["sorular"][-1], sc["sorular"][-2]["soru"]) for sc in eval_set.SENARYOLAR if sc["tip"] == "konu_degisimi"]
scen_unans = [(sc["sorular"][-1], sc["sorular"][-2]["soru"]) for sc in eval_set.SENARYOLAR
              if sc["tip"] in ("takip_cevapsiz", "konu_disi_sonra")]

# Yapay konu degisimi: her soruyu, farkli belgeden gelen bir sorudan sonra sor
synthetic = []
for i, c in enumerate(answerable):
    for j in range(1, len(answerable)):
        prev = answerable[(i + 7 * j) % len(answerable)]
        if prev["belge"].split("|")[0] not in c["belge"]:
            synthetic.append((c, prev["soru"]))
            break
synthetic_un = [(c, answerable[(i * 5 + 3) % len(answerable)]["soru"]) for i, c in enumerate(unanswerable)]


def ranks(pairs, rule):
    rs = [evidence_rank(choose(rule, c["soru"], p), c) for c, p in pairs]
    return (sum(r == 1 for r in rs), sum(r is not None and r <= 3 for r in rs), len(rs))


def passes(pairs, rule):
    return sum(choose(rule, c["soru"], p)[0][0] >= MIN_SCORE for c, p in pairs), len(pairs)


print(f"\n== 2) Takip kurali (esik {MIN_SCORE}); hit@1/hit@3/n, esigi gecen/n\n")
print(f"{'kural':14} | {'takip (5)':10} | {'degisim (4)':11} | {'yapay deg. (65)':15} | "
      f"{'cevapsiz son (senaryo)':22} | {'cevapsiz son (yapay 10)':22}")
for rule in ["mevcut", "fark 0.05", "fark 0.08", "fark 0.10", "fark 0.12", "fark 0.15", "fark 0.20",
             "birlesim", "hep birlesik"]:
    f1, f3, fn = ranks(scen_follow, rule)
    c1, c3, cn = ranks(scen_change, rule)
    y1, y3, yn = ranks(synthetic, rule)
    u, un = passes(scen_unans, rule)
    v, vn = passes(synthetic_un, rule)
    print(f"{rule:14} | {f1}/{f3}/{fn:<6} | {c1}/{c3}/{cn:<7} | {y1:2}/{y3:2}/{yn:<9} | {u}/{un:<20} | {v}/{vn}")

print("\n== Takip ve degisim sorularinda skorlar (tek basina / birlesik / fark)")
for c, p in scen_follow + scen_change:
    a, b = s(c["soru"])[0][0], s(follow_up_query(c["soru"], p))[0][0]
    print(f"   {c['soru'][:32]:32} tek {a:.3f}  birlesik {b:.3f}  fark {b - a:+.3f}")
print("Yapay degisimlerde fark dagilimi (birlesik - tek basina):")
diffs = sorted(s(follow_up_query(c["soru"], p))[0][0] - s(c["soru"])[0][0]
               for c, p in synthetic if follow_up_query(c["soru"], p) != c["soru"])
print(f"   n={len(diffs)} min {diffs[0]:+.3f} medyan {diffs[len(diffs)//2]:+.3f} max {diffs[-1]:+.3f}; "
      f">=0.10: {sum(d >= 0.10 for d in diffs)}, >=0.15: {sum(d >= 0.15 for d in diffs)}")
