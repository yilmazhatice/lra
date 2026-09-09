"""Bir soruya en yakin dokuman parcalarini bulur."""

import sys
import sqlite3

import numpy as np
from openai import OpenAI

from foundry_client import base_url, find_model

DB_PATH = "knowledge.db"
TOP_K = 3

_client = OpenAI(base_url=base_url(), api_key="not-needed")


def embed_query(question):
    """Soruyu, parcalarla ayni modelle vektore cevir."""
    model_id = find_model("embedding")
    resp = _client.embeddings.create(model=model_id, input=[question])
    return np.asarray(resp.data[0].embedding, dtype=np.float32)


def load_chunks():
    """Tum parcalari ve vektorlerini bellege oku."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, doc_name, chunk_idx, text, embedding "
        "FROM chunks WHERE embedding IS NOT NULL"
    ).fetchall()
    conn.close()

    if not rows:
        raise RuntimeError("Vektor yok. Once 'python embed.py' calistirin.")

    matrix = np.stack([np.frombuffer(r[4], dtype=np.float32) for r in rows])
    meta = [(r[0], r[1], r[2], r[3]) for r in rows]
    return meta, matrix


def search(question, top_k=TOP_K):
    """En benzer top_k parcayi (skor, id, dosya, sira, metin) olarak dondur."""
    meta, matrix = load_chunks()
    query = embed_query(question)

    # Kosinus benzerligi: vektorleri normalize edip ic carpim aliyoruz.
    # 20 parca icin kaba kuvvet fazlasiyla hizli; buyuk koleksiyonlarda
    # yerine yaklasik en yakin komsu indeksi gerekirdi.
    matrix_norm = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
    query_norm = query / np.linalg.norm(query)
    scores = matrix_norm @ query_norm

    order = np.argsort(scores)[::-1][:top_k]
    return [(float(scores[i]), *meta[i]) for i in order]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Kullanim: python search.py "sorunuz"')
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    print(f"Soru: {question}\n")

    for rank, (score, _cid, doc_name, chunk_idx, text) in enumerate(search(question), 1):
        print(f"--- {rank}. {doc_name} (parca {chunk_idx})  benzerlik={score:.3f}")
        print(text[:300].replace("\n", " "))
        print()