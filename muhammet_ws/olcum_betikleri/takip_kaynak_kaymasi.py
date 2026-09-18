# -*- coding: utf-8 -*-
"""Takip sorusunda kaynak kaymasi olcumu (kod degisikligi yapmadan).

Hipotez: birlesik arama kullanilan (used_follow_up) bir takip sorusunda,
cevabin dayandigi belge onceki turun belgesinden farkliysa model konuyu
degistirmis demektir ve cevap muhtemelen uydurmadir.

Bu betik yalnizca olcer: kural uygulansaydi kac dogru cevap reddedilirdi,
kac uydurma yakalanirdi.
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, ".")
import rag, eval_set

satirlar = []
for kaynak, senaryolar in [("ana", eval_set.SENARYOLAR), ("kon", eval_set.KONTROL_SENARYOLAR)]:
    for sc in senaryolar:
        turlar = sc["sorular"]
        onceki_kaynak, onceki_soru = None, None
        for i, t in enumerate(turlar, 1):
            r = rag.answer_details(t["soru"], previous_question=onceki_soru)
            son = i == len(turlar)
            if son:
                satirlar.append(dict(
                    id=f"{kaynak}:{sc['id']}", tip=sc["tip"], soru=t["soru"],
                    cevaplanabilir=bool(t.get("belge")),
                    onceki_kaynak=onceki_kaynak, kaynak=r.get("source"),
                    birlesik=r.get("used_follow_up"),
                    reddetti=rag.RED_IFADESI in r["text"],
                ))
            onceki_kaynak, onceki_soru = r.get("source"), t["soru"]

print(f"{'id':26} {'tip':18} {'birl':5} {'red':5} {'onceki belge':34} {'cevap belgesi':34}")
for s in satirlar:
    print(f"{s['id']:26} {s['tip']:18} {str(s['birlesik']):5} {str(s['reddetti']):5} "
          f"{str(s['onceki_kaynak'])[:33]:34} {str(s['kaynak'])[:33]:34}")

# Kural: birlesik arama kullanildi VE kaynak degisti -> reddet
print("\n=== Kural uygulansaydi ===")
yakalanan_uydurma = bozulan_dogru = 0
for s in satirlar:
    if s["reddetti"] or not s["birlesik"]:
        continue
    if s["onceki_kaynak"] and s["kaynak"] and s["onceki_kaynak"] != s["kaynak"]:
        if s["cevaplanabilir"]:
            bozulan_dogru += 1
            print(f"  BOZULURDU  {s['id']:26} {s['tip']:18} {s['soru'][:34]}")
        else:
            yakalanan_uydurma += 1
            print(f"  YAKALANIR  {s['id']:26} {s['tip']:18} {s['soru'][:34]}")
print(f"\n  Yakalanan uydurma: {yakalanan_uydurma} | Bozulan dogru cevap: {bozulan_dogru}")
