"""Faz 5.5: iki calismanin cevaplarini mod etiketi olmadan karsilastirma.

  python kor_inceleme.py hazirla <kapali.json> <acik.json>
      kontrol_inceleme/inceleme.md  : her soru icin A/B cevaplari (sira rastgele),
                                      cevaplanabilir sorularda belgedeki paragraf
      kontrol_inceleme/eslesme.json : A/B -> mod eslesmesi (karar yazilmadan acilmaz)
      kontrol_inceleme/kararlar.json: doldurulacak sablon
  python kor_inceleme.py ac
      kararlari eslesmeyle birlestirip mod basina sayar

Karar etiketleri:
  cevaplanabilir soru : D dogru | E eksik (yanlis bilgi yok) | Y yanlis/celiskili/uydurma | R reddetti
  cevaplanamaz soru   : R dogru red | U uydurma (belgede olmayan bir bilgiyi cevap gibi sundu)
Ayni metinli iki cevap tek karar alir.
"""
import json, os, random, re, sys
from pathlib import Path

LRA = r"C:\Workspace\microsoft_ws\lra"
sys.path.insert(0, LRA); os.chdir(LRA)
import eval_set
from evaluate import contains_any

OUT = Path(__file__).resolve().parent / "kontrol_inceleme"
cases = {c["id"]: c for c in eval_set.KONTROL_SORULAR + eval_set.SORULAR}
for sc in eval_set.KONTROL_SENARYOLAR + eval_set.SENARYOLAR:
    for i, q in enumerate(sc["sorular"], 1):
        cases[f"{sc['id']}#{i}"] = q


def paragraph(case):
    for doc in case["belge"].split("|"):
        text = (Path("docs") / doc).read_text(encoding="utf-8")
        for p in re.split(r"\n\s*\n", text):
            if contains_any(p, case["kanit"]):
                return f"{doc}: {p.strip()}"
    return "-"


def strip_source(text):
    return text.split("\n\n(Kaynak")[0].replace("\n", " ")


def prepare(off_path, on_path):
    off = {r["id"]: r for r in json.load(open(off_path, encoding="utf-8"))["sonuclar"]}
    on = {r["id"]: r for r in json.load(open(on_path, encoding="utf-8"))["sonuclar"]}
    rng = random.Random(20260914)
    ids = [k for k in off if off[k]["grup"] != "hazirlik"]
    rng.shuffle(ids)
    mapping, template, lines = {}, {}, ["# Kör inceleme (A/B modu gizli)\n"]
    for k in ids:
        case = cases[k]
        a, b = (off, on) if rng.random() < 0.5 else (on, off)
        mapping[k] = {"A": "kapali" if a is off else "acik", "B": "kapali" if b is off else "acik"}
        lines.append(f"## {k}  ({'cevaplanabilir' if case.get('belge') else 'CEVAPLANAMAZ'})")
        if off[k]["onceki_soru"]:
            lines.append(f"Önceki soru: {off[k]['onceki_soru']}  ")
        lines.append(f"Soru: **{off[k]['soru']}**  ")
        if case.get("belge"):
            lines.append(f"Belge: {paragraph(case)}  ")
        if a[k]["cevap"] == b[k]["cevap"]:
            lines.append(f"- A = B: {strip_source(a[k]['cevap'])}\n")
            template[k] = {"A=B": "?"}
        else:
            lines.append(f"- A: {strip_source(a[k]['cevap'])}")
            lines.append(f"- B: {strip_source(b[k]['cevap'])}\n")
            template[k] = {"A": "?", "B": "?"}
    OUT.mkdir(exist_ok=True)
    (OUT / "inceleme.md").write_text("\n".join(lines), encoding="utf-8")
    (OUT / "eslesme.json").write_text(json.dumps(mapping, indent=1), encoding="utf-8")
    if not (OUT / "kararlar.json").exists():
        (OUT / "kararlar.json").write_text(json.dumps(template, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Yazildi: {OUT / 'inceleme.md'} ({len(ids)} soru, "
          f"{sum('A=B' in t for t in template.values())} tanesinde iki cevap ayni)")


def reveal():
    mapping = json.load(open(OUT / "eslesme.json", encoding="utf-8"))
    decisions = json.load(open(OUT / "kararlar.json", encoding="utf-8"))
    counts = {m: {} for m in ("kapali", "acik")}
    detail = []
    for k, d in decisions.items():
        if k.startswith("_"):
            continue
        per_mode = {}
        if "A=B" in d:
            per_mode = {"kapali": d["A=B"], "acik": d["A=B"]}
        else:
            per_mode = {mapping[k]["A"]: d["A"], mapping[k]["B"]: d["B"]}
        answerable = bool(cases[k].get("belge"))
        for mode, label in per_mode.items():
            key = ("cevaplanabilir " if answerable else "cevaplanamaz ") + label
            counts[mode][key] = counts[mode].get(key, 0) + 1
        if per_mode["kapali"] != per_mode["acik"]:
            detail.append(f"   {k}: kapali {per_mode['kapali']} | acik {per_mode['acik']}")
    for mode in ("kapali", "acik"):
        print(f"{mode:7}", dict(sorted(counts[mode].items())))
    print("Modlar arasinda farkli karar:")
    print("\n".join(detail) or "   yok")


if __name__ == "__main__":
    if sys.argv[1] == "hazirla":
        prepare(sys.argv[2], sys.argv[3])
    else:
        reveal()
