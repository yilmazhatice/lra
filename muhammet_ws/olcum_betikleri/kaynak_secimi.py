"""rag.pick_source'u modelsiz sinar: eski bir degerlendirmenin cevaplarinda
modelin kaynak satiri silinir, kaynak koda buldurulur ve beklenen belgeyle
karsilastirilir. Kullanim: python kaynak_secimi.py degerlendirmeler/<x>.json
"""
import json, os, sqlite3, sys

LRA = r"C:\Workspace\microsoft_ws\lra"
sys.path.insert(0, LRA); os.chdir(LRA)

import eval_set
from rag import SOURCE_LINE, pick_source
from search import DB_PATH

path = sys.argv[1] if len(sys.argv) > 1 else "degerlendirmeler/2026-09-14_0530_faz3b-esik-033.json"
rows = json.load(open(path, encoding="utf-8"))["sonuclar"]
conn = sqlite3.connect(DB_PATH)
chunk = {(d, i): (cid, t) for cid, d, i, t in conn.execute("SELECT id, doc_name, chunk_idx, text FROM chunks")}

cases = {c["id"]: c for c in eval_set.SORULAR}
for sc in eval_set.SENARYOLAR:
    for i, q in enumerate(sc["sorular"], 1):
        cases[f"{sc['id']}#{i}"] = q

model_ok = code_ok = n = 0
for r in rows:
    case = cases[r["id"]]
    if not case.get("belge") or r["reddetti"] or r["grup"] == "hazirlik":
        continue
    hits = []
    for g in r["getirilen"]:
        ref, score = g.rsplit(" ", 1)
        doc, idx = ref.rsplit("#", 1)
        cid, text = chunk[(doc, int(idx))]
        hits.append((float(score), cid, doc, int(idx), text))
    expected = case["belge"].split("|")
    code = pick_source(SOURCE_LINE.sub("", r["cevap"]).strip(), r["soru"], hits)
    n += 1
    model_ok += r["kaynak_dogru"]
    code_ok += code in expected
    if code not in expected or not r["kaynak_dogru"]:
        print(f"  {r['id']:12} beklenen {expected[0]:32} model: {'dogru' if r['kaynak_dogru'] else ','.join(r['kaynaklar']) or 'yok':32} kod: {code}")
print(f"\nCevap veren {n} cevaplanabilir soru: model dogru kaynak {model_ok}/{n}, kod dogru kaynak {code_ok}/{n}")
