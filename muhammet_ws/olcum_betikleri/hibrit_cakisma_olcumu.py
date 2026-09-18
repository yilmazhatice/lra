# -*- coding: utf-8 -*-
"""Gomme cakismalari: hibrit arama ve sozcuksel pay olculur (yalniz arama).

"Kut nedir?" sorusunda ilk siralar turk-kulturunde-kurt.md ile doluyor
(kut ~ kurt); "Tugrul Bey kimdir?" sorusunda ilk sira Ulug Bey. Anahtar
kelime eslesmesi bu iki kelimeyi tam olarak ayirir.

LLM cagrisi yok. Her ayar icin butun cevaplanabilir sorularda dogru parcanin
arama sirasi olculur.
"""
import io, sys, importlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, ".")
import eval_set


def vakalar():
    """(id, soru, onceki, kanitlar) — cevaplanabilir tekil sorular + senaryo son turlari."""
    out = []
    for kaynak, tekil, senaryolar in [
        ("ana", eval_set.SORULAR, eval_set.SENARYOLAR),
        ("kon", eval_set.KONTROL_SORULAR, eval_set.KONTROL_SENARYOLAR),
    ]:
        for s in tekil:
            if s.get("belge"):
                out.append((f"{kaynak}:{s['id']}", s["soru"], None, s["kanit"].split("|")))
        for sc in senaryolar:
            son = sc["sorular"][-1]
            if son.get("belge"):
                out.append((f"{kaynak}:{sc['id']}#son", son["soru"],
                            sc["sorular"][-2]["soru"], son["kanit"].split("|")))
    return out


def olc(ad, hibrit, lexical):
    import search, rag
    search.HYBRID_SEARCH = hibrit
    search.LEXICAL_WEIGHT = lexical
    siralar = {}
    for vid, soru, onceki, kanitlar in VAKALAR:
        hits, aranan, takip, best = rag.retrieve_details(soru, top_k=40,
                                                         previous_question=onceki)
        s = next((i for i, h in enumerate(hits, 1) if any(k in h[4] for k in kanitlar)), None)
        siralar[vid] = s
    ilk1 = sum(1 for s in siralar.values() if s == 1)
    ilk3 = sum(1 for s in siralar.values() if s and s <= 3)
    yok = sum(1 for s in siralar.values() if s is None)
    print(f"  {ad:22} 1.sira {ilk1:3}/{len(siralar)}   ilk3 {ilk3:3}/{len(siralar)}   bulunamadi {yok}")
    return siralar


VAKALAR = vakalar()
print(f"Cevaplanabilir soru: {len(VAKALAR)}\n")

temel = olc("vektor (mevcut)", False, 0.0)
hibrit = olc("hibrit FTS5", True, 0.0)
lex = olc("sozcuksel 0.15", False, 0.15)

print("\n=== Hibritin degistirdigi sorular (sira farki) ===")
for vid in temel:
    a, b = temel[vid], hibrit[vid]
    if a != b:
        yon = "IYI " if (b or 99) < (a or 99) else "KOTU"
        print(f"  {yon} {vid:28} {a} -> {b}")
