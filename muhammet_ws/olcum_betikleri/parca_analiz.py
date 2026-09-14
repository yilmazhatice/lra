"""Salt okunur analiz: parca istatistikleri ve alternatif parcalama/sorgu
bicimlerinin arama kalitesine etkisi. knowledge.db'ye yazmaz."""
import os, sys, sqlite3, re, statistics, pathlib
LRA = r"C:\Workspace\microsoft_ws\lra"
sys.path.insert(0, LRA); os.chdir(LRA)
import numpy as np
from foundry_client import client, with_model
from search import EMBED_MODEL

conn = sqlite3.connect("knowledge.db")
rows = conn.execute("SELECT id, doc_name, chunk_idx, text, embedding FROM chunks").fetchall()
lens = [len(r[3]) for r in rows]
print(f"parca sayisi={len(rows)} belge={len({r[1] for r in rows})} "
      f"uzunluk min/ort/max={min(lens)}/{int(statistics.mean(lens))}/{max(lens)}")
print("vektor boyutu:", np.frombuffer(rows[0][4], dtype=np.float32).size)
bad = [r for r in rows if r[2] > 0 and not r[3][:1].isupper()]
print(f"yarim kelime/cumleyle baslayan parca: {len(bad)}/{sum(1 for r in rows if r[2]>0)}")
for r in bad[:3]:
    print("   ornek baslangic:", repr(r[3][:70]))
docs = pathlib.Path("docs")
paras = sum(len([p for p in re.split(r"\n\s*\n", f.read_text(encoding='utf-8')) if p.strip() and not p.startswith('#')]) for f in docs.glob("*.md"))
chars = sum(len(f.read_text(encoding='utf-8')) for f in docs.glob("*.md"))
print(f"toplam paragraf={paras} toplam karakter={chars} (~{chars//4} token)")

def embed(texts):
    out = []
    for i in range(0, len(texts), 8):
        b = texts[i:i+8]
        r = with_model(EMBED_MODEL, lambda m: client().embeddings.create(model=m, input=b))
        out += [d.embedding for d in r.data]
    a = np.asarray(out, dtype=np.float32)
    return a / np.linalg.norm(a, axis=1, keepdims=True)

# Paragraf duzeyinde parcalar (belge basligi on ekli)
para_meta, para_text = [], []
for f in sorted(docs.glob("*.md")):
    t = f.read_text(encoding="utf-8")
    title = t.splitlines()[0].lstrip("# ").strip()
    for p in [p.strip() for p in re.split(r"\n\s*\n", t) if p.strip() and not p.startswith("#")]:
        para_meta.append((f.name, p)); para_text.append(f"{title}\n{p}")
P = embed(para_text)
C = np.stack([np.frombuffer(r[4], dtype=np.float32) for r in rows]); C /= np.linalg.norm(C, axis=1, keepdims=True)

# (soru, belgedeki cevap ifadesi) -> dogru parcanin sirasi
Q = [
    ("böri nedir", "böri"),
    ("fatih kimdir", "29 Mayıs 1453"),
    ("Orhan Gazi kimdir", "Orhan Gazi döneminde"),
    ("Eski Türkçede kurt kelimesinin anlamı neydi?", "solucan, kurtçuk"),
    ("Azerbaycan Türkçesinde kurda ne denir?", "canavar"),
    ("Aşina hanedanının soyu nereden gelir?", "Aşina"),
    ("Ülkü Ocakları 1978'de hangi adı aldı?", "Aralık 1978"),
    ("Ülkü Ocakları bugün hangi adla faaliyet gösteriyor?", "Eğitim ve Kültür Vakfı"),
    ("Yıldırım Bayezid Ankara Savaşı'nda kime yenildi?", "Ankara Savaşı"),
    ("Kımız nedir?", "kımız"),
    ("Manas Destanı kaç dizedir?", "yarım milyon"),
    ("Türk Dil Kurumu ne zaman kuruldu?", "12 Temmuz 1932"),
    ("Dokuz Işık ilkeleri nelerdir?", "Dokuz Işık"),
]
INSTR = "Instruct: Given a question, retrieve passages that answer the question\nQuery: "

def rank(matrix, texts, qv, needle):
    s = matrix @ qv
    order = np.argsort(s)[::-1]
    for i, j in enumerate(order):
        if needle.lower() in texts[j].lower():
            return i + 1, s[order[0]], s[j]
    return None, s[order[0]], None

chunk_texts = [r[3] for r in rows]
qplain = embed([q for q, _ in Q]); qinstr = embed([INSTR + q for q, _ in Q])
print(f"\n{'soru':52} | mevcut(900kr)      | +instruct          | paragraf+baslik    | paragraf+instruct")
for k, (q, needle) in enumerate(Q):
    cells = []
    for M, T, qv in ((C, chunk_texts, qplain[k]), (C, chunk_texts, qinstr[k]),
                     (P, para_text, qplain[k]), (P, para_text, qinstr[k])):
        r, top, own = rank(M, T, qv, needle)
        cells.append(f"sira {r if r else '-':>2} skor {own if own is not None else 0:.2f}")
    print(f"{q[:52]:52} | " + " | ".join(f"{c:18}" for c in cells))
