"""Her parca icin gomme vektoru uretip SQLite'a yazar."""

import sqlite3

import numpy as np

from foundry_client import client, find_model, with_model
from search import EMBED_MODEL

DB_PATH = "knowledge.db"
BATCH_SIZE = 8

# Sorgular search.py'de EMBED_MODEL ile gomuluyor; belgeler de ayni modelle
# gomulmeli, yoksa vektorler farkli uzaylarda kalir.
print("Embedding modeli:", find_model(EMBED_MODEL))

conn = sqlite3.connect(DB_PATH)
rows = conn.execute("SELECT id, text FROM chunks ORDER BY id").fetchall()
print(f"{len(rows)} parca gomulecek.\n")

dim = None
for start in range(0, len(rows), BATCH_SIZE):
    batch = rows[start:start + BATCH_SIZE]
    resp = with_model(
        EMBED_MODEL,
        lambda model_id: client().embeddings.create(
            model=model_id,
            input=[text for _, text in batch],
        ),
    )
    for (chunk_id, _), item in zip(batch, resp.data):
        # float32 ham bayt olarak sakliyoruz: JSON'dan hizli ve kompakt
        vector = np.asarray(item.embedding, dtype=np.float32)
        conn.execute(
            "UPDATE chunks SET embedding = ? WHERE id = ?",
            (vector.tobytes(), chunk_id),
        )
        dim = vector.size
    conn.commit()
    print(f"  {start + len(batch)}/{len(rows)}")

conn.close()
print(f"\nTamam. Vektor boyutu: {dim}")