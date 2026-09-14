"""Bir soruya en yakin dokuman parcalarini bulur."""

import os
import re
import sys
import sqlite3
import warnings

import numpy as np

from foundry_client import client, with_model
from ingest import fold

DB_PATH = "knowledge.db"
TOP_K = 3
EMBED_MODEL = "qwen3-embedding-0.6b"

# Qwen3-Embedding sorgulari bir gorev talimatiyla gommeyi oneriyor; belgeler
# talimatsiz gomulur (embed.py). Olcum (muhammet_ws/olcum_betikleri/
# talimat_arama.py): ingilizce genel talimat ("Given a question, retrieve
# passages...") hit@1'i 83.1'den 78.5'e dusurdu, Turkce talimat 89.2'ye
# cikardi. Talimat tum skorlari yukselttigi icin rag.MIN_SCORE ile birlikte
# degerlendirilmeli. None: talimatsiz.
QUERY_INSTRUCTION = "Soruyu cevaplayan paragrafı bul"

# Hibrit arama: vektor sirasi ile anahtar kelime (FTS5) sirasi Reciprocal Rank
# Fusion ile birlestirilir. Ozel adlarda ("Kut nedir?") vektor aramasi dogru
# paragrafi asagida birakabiliyor. Olcum (muhammet_ws/olcum_betikleri/
# hibrit_prototip.py): 5 harflik onekle hit@1 58 -> 61/65, kotulesen yok; tam
# kelimeyle Turkce ekler yuzunden bir soru 3. siradan 9. siraya dustu.
# Yalnizca siralamayi degistirir; esik ve takip karari en iyi vektor skoruyla
# verilir (search_details).
# Varsayilan KAPALI: uctan uca olcumde (Faz 4) arama belirgin iyilesti (hit@3
# %100) ama gozle kontrolde yanlis bilgi iceren cevap 3'ten 5'e cikti ve bir
# cevaplanamaz takip sorusuna uydurma geldi. Karar Faz 5.5'teki kontrol setiyle
# verilecek (rag_iyilestirme_plani.md Bolum 2.12).
HYBRID_SEARCH = os.environ.get("LRA_HYBRID", "0") == "1"   # ortam degiskeni yalnizca deneyler icin
RRF_K = 60
KEYWORD_PREFIX = 5
# Anahtar kelime aramasinda kullanilmayan soru kelimeleri
QUESTION_WORDS = {
    "nedir", "kimdir", "neydi", "hangi", "nasıl", "nerede", "zaman", "kaç", "olarak",
    "için", "ile", "bir", "adı", "adını", "olmuştur", "yılda", "yıl", "tarihte",
    "kimin", "kimler", "nelerdir", "hangileridir", "tarafından", "sonra", "önce",
    "göre", "gibi", "vardır", "mıdır", "midir", "bugün", "neyi", "nereden", "kim",
}
_fts_warned = False


def embed_query(question):
    """Soruyu, parcalarla ayni modelle vektore cevir."""
    text = f"Instruct: {QUERY_INSTRUCTION}\nQuery:{question}" if QUERY_INSTRUCTION else question
    resp = with_model(
        EMBED_MODEL,
        lambda model_id: client().embeddings.create(
            model=model_id, input=[text]
        ),
    )
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


def keyword_ranks(question):
    """Parca id -> anahtar kelime aramasindaki sira (1'den baslar).

    Soru kelimeleri atilir; 5 harften uzun kelimeler 5 harflik onekle aranir
    ("aşina'dır" -> "aşina*") ki Turkce ekler eslesmeyi bozmasin.
    """
    global _fts_warned
    words = [w for w in re.findall(r"\w+", fold(question))
             if len(w) >= 3 and w not in QUESTION_WORDS]
    if not words:
        return {}
    terms = [f'"{w[:KEYWORD_PREFIX]}"*' if len(w) > KEYWORD_PREFIX else f'"{w}"'
             for w in words]
    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute(
            "SELECT rowid FROM chunks_fts WHERE chunks_fts MATCH ? ORDER BY bm25(chunks_fts)",
            (" OR ".join(terms),),
        ).fetchall()
    except sqlite3.OperationalError as err:
        if "no such table" not in str(err):
            raise
        if not _fts_warned:
            warnings.warn("Anahtar kelime indeksi yok; yalnizca vektor aramasi yapiliyor. "
                          "Kurmak icin: python ingest.py --fts")
            _fts_warned = True
        return {}
    finally:
        conn.close()
    return {chunk_id: rank for rank, (chunk_id,) in enumerate(rows, 1)}


def search_details(question, top_k=TOP_K):
    """(parcalar, en_iyi_vektor_skoru) dondur.

    Parcalar (vektor skoru, id, dosya, sira, metin); hibrit aramada sira
    birlestirilmis siradir, skor yine parcanin kendi vektor skorudur. Esik ve
    takip karari icin en_iyi_vektor_skoru kullanilmali: hibrit sirada ilk
    parca en yuksek vektor skorlu parca olmayabilir.
    """
    meta, matrix = load_chunks()
    query = embed_query(question)

    # Kosinus benzerligi: vektorleri normalize edip ic carpim aliyoruz.
    # Bu olcekte kaba kuvvet fazlasiyla hizli; buyuk koleksiyonlarda
    # yerine yaklasik en yakin komsu indeksi gerekirdi.
    matrix_norm = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
    query_norm = query / np.linalg.norm(query)
    scores = matrix_norm @ query_norm
    order = [int(i) for i in np.argsort(scores)[::-1]]
    best = float(scores[order[0]])

    if HYBRID_SEARCH:
        kw = keyword_ranks(question)
        if kw:
            fused = {}
            for rank, i in enumerate(order, 1):
                fused[i] = 1 / (RRF_K + rank) + (1 / (RRF_K + kw[meta[i][0]]) if meta[i][0] in kw else 0)
            order = sorted(order, key=lambda i: fused[i], reverse=True)

    return [(float(scores[i]), *meta[i]) for i in order[:top_k]], best


def search(question, top_k=TOP_K):
    """En uygun top_k parcayi (vektor skoru, id, dosya, sira, metin) olarak dondur."""
    return search_details(question, top_k=top_k)[0]


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