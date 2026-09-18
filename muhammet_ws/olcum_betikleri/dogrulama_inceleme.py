"""H13 (cevap dogrulama) sonrasi gozle inceleme listesi.

Dogrulama yalnizca cevabi redde cevirebildigi icin tam kor inceleme mumkun
degil; bunun yerine iki grup listelenir:
  1) dogrulamanin reddettigi sorular: onceki (dogrulamasiz) cevap + belge paragrafi
     -> dogru cevap mi reddedildi (kayip), yanlis cevap mi (kazanc)?
  2) dogrulamali calismada cevap verilen cevaplanamaz sorular -> uydurma var mi?
  3) dogrulama disinda sonucu/metni degisen sorular (gurultu kontrolu)
Kullanim: python dogrulama_inceleme.py <dogrulamasiz.json> <dogrulamali.json>
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kor_inceleme import cases, paragraph, strip_source  # noqa: E402

off = {r["id"]: r for r in json.load(open(sys.argv[1], encoding="utf-8"))["sonuclar"]}
on = {r["id"]: r for r in json.load(open(sys.argv[2], encoding="utf-8"))["sonuclar"]}
scored = [k for k in on if on[k]["grup"] != "hazirlik"]

print("== 1) Dogrulamanin reddettigi sorular")
for k in scored:
    if on[k].get("dogrulama") is False:
        case = cases[k]
        kind = "cevaplanabilir" if case.get("belge") else "CEVAPLANAMAZ"
        print(f"\n{k} ({kind}){'  onceki: ' + on[k]['onceki_soru'] if on[k]['onceki_soru'] else ''}")
        print(f"  soru : {on[k]['soru']}")
        print(f"  dogrulamasiz cevap: {strip_source(off[k]['cevap'])}")
        if case.get("belge"):
            print(f"  belge: {paragraph(case)[:400]}")

print("\n== 2) Dogrulamali calismada cevap verilen cevaplanamaz sorular")
for k in scored:
    if not cases[k].get("belge") and not on[k]["reddetti"]:
        print(f"  {k}{'  onceki: ' + on[k]['onceki_soru'] if on[k]['onceki_soru'] else ''}\n"
              f"     soru : {on[k]['soru']}\n     cevap: {strip_source(on[k]['cevap'])}")

print("\n== 3) Dogrulama disinda metni degisen sorular")
for k in scored:
    if on[k].get("dogrulama") is not False and on[k]["cevap"] != off[k]["cevap"]:
        print(f"  {k}: sonuc {off[k]['basarili']} -> {on[k]['basarili']}\n"
              f"     once : {strip_source(off[k]['cevap'])[:200]}\n     sonra: {strip_source(on[k]['cevap'])[:200]}")
