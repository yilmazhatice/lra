"""Bir soruya en yakin dokuman parcalarini bulur."""

import re
import sys
import sqlite3

import numpy as np

from foundry_client import client, find_model

DB_PATH = "knowledge.db"
TOP_K = 5
EMBED_MODEL = "qwen3-embedding-0.6b"

# qwen3-embedding aileleri sorgu tarafinda bir yonerge oneki bekler; parcalar
# ise oneksiz gomulur. Onek olmadan skorlar yaklasik 0.09 puan dusuyor ve
# dogru belge daha sik ucuncu siranin disinda kaliyor (olcum: recall@3 %91 ->
# %97). Onek degisirse knowledge.db'yi yeniden gommek GEREKMEZ; yalnizca
# sorgu tarafini etkiler.
QUERY_PREFIX = (
    "Instruct: Given a web search query, retrieve relevant passages that "
    "answer the query\nQuery: "
)

# Anlamsal skora karistirilan sozcuksel ortusme payi. Ozel adlarda ("Dokuz
# Isik", "Dandanakan") gomme vektorleri zayif kaliyor; kaba bir kok eslesmesi
# bu sorulari ilk siraya tasiyor (recall@1 %84 -> %91).
LEXICAL_WEIGHT = 0.15
KOK_UZUNLUK = 5          # Turkce ekleri kabaca atmak icin kelime koku uzunlugu

_chunks = None           # (meta, normalize matris, kok kumeleri) onbellegi


def kokler(metin):
    """Metni kaba kelime koklerine ayirir (sozcuksel ortusme icin).

    Kucultme Turkceye gore yapiliyor: Python'da "İ".lower() iki karakterli
    "i̇" uretiyor ve "İlimcilik" ile "ilimcilik" ayri kelime gibi gorunuyor.
    """
    duz = metin.replace("İ", "i").replace("I", "ı").lower()
    return {k[:KOK_UZUNLUK] for k in re.findall(r"\w+", duz) if len(k) > 3}


def embed_query(question):
    """Soruyu, parcalarla ayni modelle vektore cevir."""
    model_id = find_model(EMBED_MODEL)
    resp = client().embeddings.create(
        model=model_id, input=[QUERY_PREFIX + question]
    )
    return np.asarray(resp.data[0].embedding, dtype=np.float32)


def load_chunks():
    """Tum parcalari, vektorlerini ve koklerini bellege oku (bir kez)."""
    global _chunks
    if _chunks is not None:
        return _chunks

    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, doc_name, chunk_idx, text, embedding "
        "FROM chunks WHERE embedding IS NOT NULL"
    ).fetchall()
    conn.close()

    if not rows:
        raise RuntimeError("Vektor yok. Once 'python embed.py' calistirin.")

    matrix = np.stack([np.frombuffer(r[4], dtype=np.float32) for r in rows])
    matrix = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
    meta = [(r[0], r[1], r[2], r[3]) for r in rows]
    _chunks = (meta, matrix, [kokler(r[3]) for r in rows])
    return _chunks


def search(question, top_k=TOP_K):
    """En benzer top_k parcayi (skor, id, dosya, sira, metin) olarak dondur."""
    meta, matrix, govdeler = load_chunks()
    query = embed_query(question)

    # Kosinus benzerligi: vektorler normalize oldugu icin ic carpim yeterli.
    # Bu olcekte kaba kuvvet fazlasiyla hizli; buyuk koleksiyonlarda
    # yerine yaklasik en yakin komsu indeksi gerekirdi.
    scores = matrix @ (query / np.linalg.norm(query))

    if LEXICAL_WEIGHT:
        soru_kok = kokler(question)
        ortusme = np.array([
            len(soru_kok & g) / max(1, len(soru_kok)) for g in govdeler
        ])
        scores = (1 - LEXICAL_WEIGHT) * scores + LEXICAL_WEIGHT * ortusme

    order = np.argsort(scores)[::-1][:top_k]
    return [(float(scores[i]), *meta[i]) for i in order]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Kullanim: python search.py "sorunuz"')
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    print(f"Soru: {question}\n")

    for rank, (score, _cid, doc_name, chunk_idx, text) in enumerate(
        search(question), 1
    ):
        print(f"--- {rank}. {doc_name} (parca {chunk_idx})  benzerlik={score:.3f}")
        print(text[:300].replace("\n", " "))
        print()
