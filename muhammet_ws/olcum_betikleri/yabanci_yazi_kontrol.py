"""H12 (Turkce olmayan yazi korumasi) modelsiz sinamasi.

degerlendirmeler/ altindaki butun kayitli cevaplara rag.cut_foreign_script
uygulanir: kac cevapta bu karakterler var, kesilince ne kaliyor. Koruma cevap
uretimini degistirmedigi icin etkisi kayitli cevaplarda birebir gorulur.
Kullanim: python yabanci_yazi_kontrol.py
"""
import glob, json, os, sys

LRA = r"C:\Workspace\microsoft_ws\lra"
sys.path.insert(0, LRA); os.chdir(LRA)
from rag import MIN_ANSWER_CHARS, SOURCE_LINE, cut_foreign_script

# Birim kontroller
cases = [
    ("Toy, devletin meclisidir. Kurultay同类文档中 ... (Kaynak: a.md)", "Toy, devletin meclisidir."),
    ("Böri kurdun adıdır.", "Böri kurdun adıdır."),
    ("同类文档中", ""),
    ("II. Mehmed 1453'te İstanbul'u aldı. 19. Tümen 韩国", "II. Mehmed 1453'te İstanbul'u aldı."),
    ('Dedi ki "Ben Fırat." Sonra 同类', 'Dedi ki "Ben Fırat."'),
]
for text, expected in cases:
    got, cut = cut_foreign_script(text)
    print(f"{'OK ' if got == expected else 'HATA'} kesildi={cut} -> {got!r}")

total = affected = 0
for path in sorted(glob.glob("degerlendirmeler/*.json")):
    for r in json.load(open(path, encoding="utf-8"))["sonuclar"]:
        total += 1
        body = SOURCE_LINE.sub("", r["cevap"]).strip()
        new, cut = cut_foreign_script(body)
        if cut:
            affected += 1
            verdict = "red" if len(SOURCE_LINE.sub("", new).strip()) < MIN_ANSWER_CHARS else "kesildi"
            print(f"\n{os.path.basename(path)} {r['id']} ({verdict})\n  once : {body[:160]!r}\n  sonra: {new!r}")
print(f"\nToplam {total} kayitli cevap, Turkce olmayan yazi iceren {affected}.")
