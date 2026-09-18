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
TOP_K = 5
EMBED_MODEL = "qwen3-embedding-0.6b"

# Qwen3-Embedding sorgulari bir gorev talimatiyla gommeyi oneriyor; belgeler
# talimatsiz gomulur (embed.py). Olcum (muhammet_ws/olcum_betikleri/
# talimat_arama.py, 105 soruluk set): ingilizce genel talimat ("Given a web
# search query, retrieve relevant passages...") hit@1'i 83.1'den 78.5'e
# dusurdu, asagidaki Turkce talimat 89.2'ye cikardi. Bu yuzden masaustu_gui
# dalindaki ingilizce onek yerine Turkce talimat kullaniliyor. Talimat tum
# skorlari yukselttigi icin rag.MIN_SCORE ile birlikte degerlendirilmeli.
# None: talimatsiz. Onek degisirse knowledge.db'yi yeniden gommek GEREKMEZ;
# yalnizca sorgu tarafini etkiler.
QUERY_INSTRUCTION = "Soruyu cevaplayan paragrafı bul"

# Anlamsal skora karistirilan sozcuksel ortusme payi (masaustu_gui dalindan).
# Ozel adlarda ("Dokuz Isik", "Dandanakan") gomme vektorleri zayif kalabiliyor
# ve kaba bir kok eslesmesi yardimci oluyor. Varsayilan 0: ayni isi olculmus
# haliyle asagidaki hibrit FTS5 aramasi yapiyor ve skoru degistirmedigi icin
# rag.MIN_SCORE anlamini koruyor. Denemek icin LRA_LEXICAL=0.15.
LEXICAL_WEIGHT = float(os.environ.get("LRA_LEXICAL", "0"))   # ortam degiskeni yalnizca deneyler icin
KOK_UZUNLUK = 5          # Turkce ekleri kabaca atmak icin kelime koku uzunlugu

# Hibrit arama: vektor sirasi ile anahtar kelime (FTS5) sirasi Reciprocal Rank
# Fusion ile birlestirilir. Ozel adlarda ("Kut nedir?") vektor aramasi dogru
# paragrafi asagida birakabiliyor. Olcum (muhammet_ws/olcum_betikleri/
# hibrit_prototip.py): 5 harflik onekle hit@1 58 -> 61/65, kotulesen yok; tam
# kelimeyle Turkce ekler yuzunden bir soru 3. siradan 9. siraya dustu.
# Yalnizca siralamayi degistirir; esik ve takip karari en iyi vektor skoruyla
# verilir (search_details).
# Varsayilan KAPALI: uctan uca olcumde (Faz 4) arama belirgin iyilesti (hit@3
# %100) ama gozle kontrolde yanlis bilgi iceren cevap 3'ten 5'e cikti ve bir
# cevaplanamaz takip sorusuna uydurma geldi (rag_iyilestirme_plani.md 2.12).
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

_chunks = None           # (meta, normalize matris, kok kumeleri) onbellegi
_fts_warned = False


def kokler(metin):
    """Metni kaba kelime koklerine ayirir (sozcuksel ortusme icin).

    Kucultme Turkceye gore yapiliyor: Python'da "İ".lower() iki karakterli
    "i̇" uretiyor ve "İlimcilik" ile "ilimcilik" ayri kelime gibi gorunuyor.
    """
    duz = metin.replace("İ", "i").replace("I", "ı").lower()
    return {k[:KOK_UZUNLUK] for k in re.findall(r"\w+", duz) if len(k) > 3}


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
    """Tum parcalari, vektorlerini ve koklerini bellege oku (bir kez).

    (meta, normalize edilmis matris, parca kokleri) dondurur. Vektorler
    okunurken normalize ediliyor; her aramada yeniden bolmek gereksiz.
    """
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


def keyword_ranks(question):
    """Parca id -> anahtar kelime aramasindaki sira (1'den baslar).

    Soru kelimeleri atilir; 5 harften uzun kelimeler 5 harflik onekle aranir
    ki Turkce ekler eslesmeyi bozmasin.
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
    """(parcalar, en_iyi_skor) dondur.

    Parcalar (skor, id, dosya, sira, metin); hibrit aramada sira
    birlestirilmis siradir, skor yine parcanin kendi vektor skorudur. Esik ve
    takip karari icin en_iyi_skor kullanilmali: hibrit sirada ilk parca en
    yuksek skorlu parca olmayabilir.
    """
    meta, matrix, govdeler = load_chunks()
    query = embed_query(question)

    # Kosinus benzerligi: matris normalize oldugu icin ic carpim yeterli.
    # Bu olcekte kaba kuvvet fazlasiyla hizli; buyuk koleksiyonlarda
    # yerine yaklasik en yakin komsu indeksi gerekirdi.
    scores = matrix @ (query / np.linalg.norm(query))

    if LEXICAL_WEIGHT:
        soru_kok = kokler(question)
        ortusme = np.array([
            len(soru_kok & g) / max(1, len(soru_kok)) for g in govdeler
        ])
        scores = (1 - LEXICAL_WEIGHT) * scores + LEXICAL_WEIGHT * ortusme

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
    """En uygun top_k parcayi (skor, id, dosya, sira, metin) olarak dondur."""
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
