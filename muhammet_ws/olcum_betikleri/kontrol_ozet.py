"""Kontrol setinin iki modunun otomatik ozetini yan yana yazar.
Kullanim: python kontrol_ozet.py <kapali.json> <acik.json>
"""
import json, os, sys

os.chdir(r"C:\Workspace\microsoft_ws\lra")
off = json.load(open(sys.argv[1], encoding="utf-8"))
on = json.load(open(sys.argv[2], encoding="utf-8"))

for k in ["basari", "arama_hit1", "arama_hit3", "cevap_basari", "yanlis_red", "anahtar_tam",
          "kaynak_dogru", "cevapsiz_red", "cevapsiz_esikte_red", "sure_ortalama", "ilk_token_ortalama"]:
    print(f"{k:22} kapali {str(off['ozet'][k]):8} acik {on['ozet'][k]}")

cats = {}
for name, d in (("kapali", off), ("acik", on)):
    for r in d["sonuclar"]:
        if r["grup"] == "hazirlik":
            continue
        c = cats.setdefault(r["kategori"], {}).setdefault(name, [0, 0])
        c[0] += bool(r["basarili"]); c[1] += 1
for c, v in cats.items():
    print(f"  {c:16} kapali {v['kapali'][0]}/{v['kapali'][1]}  acik {v['acik'][0]}/{v['acik'][1]}")

print("HATA (kapali):")
for r in off["sonuclar"]:
    if r["grup"] != "hazirlik" and not r["basarili"]:
        print(f"   {r['id']:22} {'; '.join(r['neden'])} | skor {r['en_iyi_skor']} | takip {r.get('takip_aramasi')} | sira {r.get('sira')}")
print("HATA (acik):")
for r in on["sonuclar"]:
    if r["grup"] != "hazirlik" and not r["basarili"]:
        print(f"   {r['id']:22} {'; '.join(r['neden'])} | sira {r.get('sira')}")
