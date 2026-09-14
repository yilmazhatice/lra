"""Faz 4 karari icin: hibrit arama (SQLite FTS5 + vektor) prototipi, modelsiz.

knowledge.db'ye yazmaz; FTS5 indeksi bellekte kurulur. eval_set'in tekil
cevaplanabilir sorulariyla dogru parcanin sirasi olculur.

Birlestirme: Reciprocal Rank Fusion, puan = 1/(k + vektor_sirasi) + 1/(k + kelime_sirasi).
Kelime aramasi degiskenleri:
  tam kelime : sorudaki kelimeler oldugu gibi (OR)
  onek-5     : ilk 5 harf + * (Turkce ekleri tolere etmek icin; "Aşina'dır" -> "aşina*")
Kullanim: python hibrit_prototip.py
"""
import os, re, sqlite3, sys

LRA = r"C:\Workspace\microsoft_ws\lra"
sys.path.insert(0, LRA); os.chdir(LRA)

import eval_set
from evaluate import evidence_rank, norm
from search import DB_PATH, search

ALL = 10**6
STOP = {"nedir", "kimdir", "neydi", "hangi", "nasıl", "nerede", "zaman", "kaç", "olarak", "için",
        "ile", "bir", "adı", "adını", "olmuştur", "yılda", "yıl", "tarihte", "kimin", "kimler",
        "nelerdir", "hangileridir", "tarafından", "sonra", "önce", "göre", "gibi", "vardır",
        "mıdır", "midir", "bugün", "neyi", "nereden", "kim"}

conn = sqlite3.connect(DB_PATH)
chunks = conn.execute("SELECT id, doc_name, chunk_idx, text FROM chunks").fetchall()
by_id = {c[0]: c for c in chunks}
mem = sqlite3.connect(":memory:")
mem.execute("CREATE VIRTUAL TABLE f USING fts5(body, tokenize='unicode61 remove_diacritics 0')")
for cid, _d, _i, text in chunks:
    mem.execute("INSERT INTO f(rowid, body) VALUES (?, ?)", (cid, norm(text)))


def keyword_ranks(question, prefix):
    words = [w for w in re.findall(r"\w+", norm(question)) if len(w) >= 3 and w not in STOP]
    if not words:
        return {}
    terms = [f'"{w[:5]}"*' if prefix and len(w) > 5 else f'"{w}"' for w in words]
    rows = mem.execute("SELECT rowid FROM f WHERE f MATCH ? ORDER BY bm25(f)", (" OR ".join(terms),)).fetchall()
    return {rowid: rank for rank, (rowid,) in enumerate(rows, 1)}


def fused(question, prefix, k):
    vec = search(question, top_k=ALL)
    kw = keyword_ranks(question, prefix)
    scored = []
    for rank, hit in enumerate(vec, 1):
        s = 1 / (k + rank)
        if hit[1] in kw:
            s += 1 / (k + kw[hit[1]])
        scored.append((s, hit))
    return [h for _s, h in sorted(scored, key=lambda x: x[0], reverse=True)]


answerable = [c for c in eval_set.SORULAR if c.get("belge")]
ozel = [c for c in answerable if c.get("kategori") == "ozel_ad"]
scen = [(sc["sorular"][-1]) for sc in eval_set.SENARYOLAR if sc["tip"] == "konu_degisimi"]
vec_cache = {}


def metrics(cases, ranker):
    rs = [evidence_rank(ranker(c["soru"]), c) for c in cases]
    n = len(rs)
    return (sum(r == 1 for r in rs), sum(r is not None and r <= 3 for r in rs),
            sum(1 / r for r in rs if r) / n, rs)


variants = {"yalniz vektor (su an)": lambda q: search(q, top_k=ALL)}
for prefix in (False, True):
    for k in (10, 60):
        name = f"hibrit {'onek-5' if prefix else 'tam kelime'} k={k}"
        variants[name] = (lambda q, p=prefix, kk=k: fused(q, p, kk))

print(f"{len(answerable)} cevaplanabilir tekil soru, {len(ozel)} ozel_ad, "
      f"{len(scen)} konu degisimi sorusu (tek basina)\n")
base_ranks = None
for name, ranker in variants.items():
    h1, h3, mrr, rs = metrics(answerable, ranker)
    o1, o3, _m, _r = metrics(ozel, ranker)
    s1, s3, _m, _r = metrics(scen, ranker)
    print(f"{name:26} hepsi hit@1 {h1:2}/{len(answerable)} hit@3 {h3:2} MRR {mrr:.3f} | "
          f"ozel_ad hit@1 {o1}/{len(ozel)} hit@3 {o3} | degisim hit@1 {s1}/{len(scen)} hit@3 {s3}")
    if base_ranks is None:
        base_ranks = rs
    else:
        worse = [(c["id"], b, r) for c, b, r in zip(answerable, base_ranks, rs) if (r or 99) > (b or 99)]
        better = [(c["id"], b, r) for c, b, r in zip(answerable, base_ranks, rs) if (r or 99) < (b or 99)]
        print(f"{'':26} iyilesen {better}")
        print(f"{'':26} kotulesen {worse}")
