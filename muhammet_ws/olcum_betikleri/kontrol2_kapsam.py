import io, sys, sqlite3
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, ".")
import eval_set

kanitlar = []
for liste in (eval_set.SORULAR, eval_set.KONTROL_SORULAR):
    for s in liste:
        if s.get("kanit"): kanitlar += s["kanit"].split("|")
for liste in (eval_set.SENARYOLAR, eval_set.KONTROL_SENARYOLAR):
    for sc in liste:
        for t in sc["sorular"]:
            if t.get("kanit"): kanitlar += t["kanit"].split("|")

conn = sqlite3.connect("knowledge.db")
rows = conn.execute("SELECT doc_name, chunk_idx, text FROM chunks ORDER BY doc_name, chunk_idx").fetchall()
son_belge = None
for doc, idx, metin in rows:
    if doc != son_belge:
        print(f"\n### {doc}")
        son_belge = doc
    kapsanan = any(k in metin for k in kanitlar)
    if not kapsanan:
        govde = metin.split("\n", 1)[1] if "\n" in metin else metin
        print(f"  [{idx}] BOS  {govde[:96]}")
