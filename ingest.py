import sqlite3
import pathlib
import re

DOCS_DIR = pathlib.Path("docs")
DB_PATH = "knowledge.db"
CHUNK_SIZE = 900  # hedef parca uzunlugu (karakter)
OVERLAP = 200   # parcalar arasi ortusme (karakter)


def read_documents():
    """docs klasorundeki .txt ve .md dosyalarini sirayla oku."""
    for path in sorted(DOCS_DIR.glob("*")):
        if path.suffix.lower() in {".txt", ".md"}:
            yield path.name, path.read_text(encoding="utf-8")


def chunk_text(text):
    """Metni paragraf sinirlarindan ~CHUNK_SIZE karakterlik parcalara bol."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    chunks = []
    current = ""
    for p in paragraphs:
        # Bu paragraf eklenince hedefi asiyorsa mevcut parcayi kapat
        if current and len(current) + len(p) + 1 > CHUNK_SIZE:
            chunks.append(current)
            # Ortusme: yeni parca, oncekinin son OVERLAP karakteriyle baslasin
            current = current[-OVERLAP:] + " " + p
        else:
            current = (current + "\n" + p).strip()

    if current:
        chunks.append(current)
    return chunks


def build_database():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DROP TABLE IF EXISTS chunks")
    conn.execute("""
        CREATE TABLE chunks (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_name  TEXT    NOT NULL,
            chunk_idx INTEGER NOT NULL,
            text      TEXT    NOT NULL,
            embedding BLOB
        )
    """)

    total = 0
    for doc_name, text in read_documents():
        pieces = chunk_text(text)
        for i, piece in enumerate(pieces):
            conn.execute(
                "INSERT INTO chunks (doc_name, chunk_idx, text) VALUES (?, ?, ?)",
                (doc_name, i, piece),
            )
        print(f"{doc_name}: {len(pieces)} parca")
        total += len(pieces)

    conn.commit()
    conn.close()
    print(f"\nToplam {total} parca {DB_PATH} dosyasina yazildi.")


if __name__ == "__main__":
    build_database()
