import sqlite3
import pathlib
import re
import sys

DOCS_DIR = pathlib.Path("docs")
DB_PATH = "knowledge.db"
CHUNK_SIZE = 1000  # bir parcanin govdesi icin ust sinir (karakter); asan paragraf cumlelere bolunur
CHUNKING = "paragraf + baslik yolu, ortusme yok"

# Cumle sonu: kucuk harf, rakam olmayan bir karakterden sonra gelen nokta,
# soru ya da unlem isareti (varsa kapanis tirnagiyla). "II. Mehmed",
# "19. Tumen" gibi sira sayilarinda bolmemek icin nokta once buyuk harf ya da
# rakamdan sonra geliyorsa cumle sonu sayilmaz.
SENTENCE_END = re.compile(r"(?<=[a-zçğıöşüâîû)][.!?])[\"”’']?\s+")


def fold(text):
    """Anahtar kelime aramasi icin Turkce kucuk harf.

    str.lower() "İ"yi "i" + birlestirici nokta yapiyor ve "I"yi "i"ye
    ceviriyor; ikisi de Turkce kelimelerde eslesmeyi bozar.
    """
    return text.replace("İ", "i").replace("I", "ı").lower().replace("̇", "")


def build_fts(conn):
    """chunks tablosundan anahtar kelime indeksi (FTS5) kur.

    rowid parca id'siyle ayni; search.py vektor ve kelime siralarini bununla
    eslestirir. Vektorlere dokunmaz, embed.py'yi yeniden calistirmak gerekmez.
    """
    conn.execute("DROP TABLE IF EXISTS chunks_fts")
    conn.execute(
        "CREATE VIRTUAL TABLE chunks_fts USING fts5("
        "body, tokenize='unicode61 remove_diacritics 0')"
    )
    rows = conn.execute("SELECT id, text FROM chunks").fetchall()
    conn.executemany(
        "INSERT INTO chunks_fts (rowid, body) VALUES (?, ?)",
        [(chunk_id, fold(text)) for chunk_id, text in rows],
    )
    conn.commit()
    return len(rows)


def read_documents():
    """docs klasorundeki .txt ve .md dosyalarini sirayla oku."""
    for path in sorted(DOCS_DIR.glob("*")):
        if path.suffix.lower() in {".txt", ".md"}:
            yield path.name, path.read_text(encoding="utf-8")


def split_long(paragraph, limit=CHUNK_SIZE):
    """Siniri asan paragrafi cumle sinirlarindan limit'i asmayan parcalara bol."""
    if len(paragraph) <= limit:
        return [paragraph]
    sentences, start = [], 0
    for match in SENTENCE_END.finditer(paragraph):
        sentences.append(paragraph[start:match.end()].strip())
        start = match.end()
    sentences.append(paragraph[start:].strip())

    pieces, current = [], ""
    for sentence in filter(None, sentences):
        if current and len(current) + 1 + len(sentence) > limit:
            pieces.append(current)
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        pieces.append(current)
    return pieces


def chunk_text(text, fallback_title=""):
    """Her paragrafi ayri bir parca yap, basina bulundugu baslik yolunu ekle.

    Paragraflar tek bir alt konuyu anlatiyor; birlestirilince farkli konular
    ayni vektore karisiyordu. Baslik yolu ("Belge — Alt baslik") paragrafin
    kime/neye ait oldugunu tasir: "Tahliye olduktan sonra..." diye baslayan
    paragraf, "Muhsin Yazicioglu" alt basligi olmadan kimi anlattigini
    soylemez.
    """
    headings = {}   # seviye -> baslik
    chunks = []
    for block in (b.strip() for b in re.split(r"\n\s*\n", text)):
        if not block:
            continue
        heading = re.match(r"^(#+)\s+(.*)$", block)
        if heading and "\n" not in block:
            level = len(heading.group(1))
            headings = {k: v for k, v in headings.items() if k < level}
            headings[level] = heading.group(2).strip()
            continue
        path = " — ".join(headings[k] for k in sorted(headings)) or fallback_title
        for piece in split_long(block):
            chunks.append(f"{path}\n{piece}" if path else piece)
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
        pieces = chunk_text(text, fallback_title=pathlib.Path(doc_name).stem)
        for i, piece in enumerate(pieces):
            conn.execute(
                "INSERT INTO chunks (doc_name, chunk_idx, text) VALUES (?, ?, ?)",
                (doc_name, i, piece),
            )
        print(f"{doc_name}: {len(pieces)} parca")
        total += len(pieces)

    conn.commit()
    build_fts(conn)
    conn.close()
    print(f"\nToplam {total} parca {DB_PATH} dosyasina yazildi (anahtar kelime indeksi dahil).")


if __name__ == "__main__":
    if "--fts" in sys.argv:
        # Yalnizca anahtar kelime indeksini mevcut parcalardan yeniden kur
        conn = sqlite3.connect(DB_PATH)
        print(f"Anahtar kelime indeksi kuruldu: {build_fts(conn)} parca.")
        conn.close()
    else:
        build_database()
