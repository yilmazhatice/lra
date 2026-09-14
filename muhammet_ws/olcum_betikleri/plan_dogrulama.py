"""rag_iyilestirme_plani.md'deki iddialarin kontrolu. Proje dosyalarina yazmaz.

T1  takip sorusu ve konu disi soru (retrieve() davranisi)
T2  evaluate.py'nin 12 soruluk seti (eval_results.md'nin uzerine yazmadan)
T3  Streamlit arayuzunde ard arda soru (AppTest ile gercek app.py)
Kullanim: python plan_dogrulama.py [T1] [T2] [T3]
"""
import json, os, sys, time

LRA = r"C:\Workspace\microsoft_ws\lra"
sys.path.insert(0, LRA); os.chdir(LRA)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plan_dogrulama_sonuc.json")

from rag import answer, retrieve, MIN_SCORE
from search import search

results = {}
only = sys.argv[1:] or ["T1", "T2", "T3"]


def top(hits):
    return f"{hits[0][2]}#{hits[0][3]} {hits[0][0]:.3f}" if hits else "-"


if "T1" in only:
    print("=== T1 retrieve(): arayuzun gonderdigi (onceki + yeni) arama", flush=True)
    pairs = [
        # (onceki soru, yeni soru, beklenen)
        ("Malazgirt Savaşı ne zaman yapıldı?", "sonucu ne oldu?", "takip: onceki soru kullanilmali"),
        ("Sakarya Meydan Muharebesi kaç gün sürmüştür?", "bunun sebebi ne?", "takip: onceki soru kullanilmali"),
        ("Orhun Yazıtları'nın alfabesini kim çözmüştür?", "hangi yılda?", "takip: onceki soru kullanilmali"),
        ("Osman Gazi kimdir", "Bugün hava nasıl olacak?", "konu disi: reddedilmeli"),
        ("Eski Türkçede kurdun adı neydi?", "asdf qwerty zxcv", "anlamsiz: reddedilmeli"),
        ("Osman Gazi kimdir", "Python listesi nasıl sıralanır?", "konu disi: reddedilmeli"),
    ]
    rows = []
    for prev, q, expect in pairs:
        alone = search(q)
        merged = search(f"{prev} {q}")
        final = retrieve(q, search_query=f"{prev} {q}")
        passes = final[0][0] >= MIN_SCORE
        text, _, sure = answer(q, search_query=f"{prev} {q}")
        print(f"  [{expect}] {prev!r} -> {q!r}\n"
              f"     tek basina {top(alone)} | birlesik {top(merged)} | secilen {top(final)} "
              f"| esik {'GECTI' if passes else 'alti'} [{sure:.1f} sn]\n"
              f"     cevap: {text[:150]!r}", flush=True)
        rows.append(dict(onceki=prev, soru=q, beklenen=expect, tek=top(alone), birlesik=top(merged),
                         secilen=top(final), esik_gecti=passes, cevap=text, sure=round(sure, 2)))
    results["T1"] = rows

if "T2" in only:
    print("\n=== T2 evaluate.py test seti (12 soru)", flush=True)
    from evaluate import CASES, REDDETME
    rows = []
    for q, expected in CASES:
        text, hits, sure = answer(q)
        retrieved = [h[2] for h in hits]
        reddetti = REDDETME in text
        ok = reddetti if expected is None else (expected in retrieved and not reddetti)
        kaynak = "(Kaynak:" in text
        print(f"  {'OK  ' if ok else 'HATA'} [{sure:4.1f} sn] skor {hits[0][0]:.3f} kaynak={'var' if kaynak else 'yok'} | {q}\n"
              f"       {text[:160]!r}", flush=True)
        rows.append(dict(soru=q, beklenen=expected, basarili=ok, reddetti=reddetti, kaynak=kaynak,
                         skor=round(hits[0][0], 3), sure=round(sure, 2), cevap=text))
    n_ok = sum(r["basarili"] for r in rows)
    llm = [r["sure"] for r in rows if not (r["reddetti"] and r["sure"] < 1)]
    print(f"  basarili {n_ok}/{len(rows)} | ortalama {sum(r['sure'] for r in rows)/len(rows):.1f} sn "
          f"| modele giden sorularda ortalama {sum(llm)/max(len(llm),1):.1f} sn", flush=True)
    results["T2"] = rows

if "T3" in only:
    print("\n=== T3 Streamlit app.py, ard arda sorular (AppTest)", flush=True)
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(os.path.join(LRA, "app.py"), default_timeout=300)
    at.run()
    rows = []
    for q in ["böri nedir", "fatih kimdir", "Osman Gazi kimdir", "Dokuz Işık ilkeleri nelerdir?"]:
        t = time.perf_counter()
        at.chat_input[0].set_value(q).run()
        kayit = at.session_state.gecmis[-1]
        print(f"  [{time.perf_counter()-t:5.1f} sn, olculen {kayit['sure']:.1f}] {q} -> {kayit['metin'][:110]!r}"
              f"{' | HATA: ' + str([e.value for e in at.exception]) if at.exception else ''}", flush=True)
        rows.append(dict(soru=q, cevap=kayit["metin"], sure=round(kayit["sure"], 2),
                         gecmis_uzunlugu=len(at.session_state.gecmis)))
    results["T3"] = rows

json.dump(results, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nyazildi:", OUT)
