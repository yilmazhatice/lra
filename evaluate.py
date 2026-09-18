"""eval_set.py'deki sorulari calistirir, sonuclari tarihli dosyalara yazar.

Kullanim:
    python evaluate.py                         # tum set
    python evaluate.py --etiket baslangic      # dosya adina etiket ekle
    python evaluate.py --karsilastir degerlendirmeler/<onceki>.json
    python evaluate.py --kontrol               # yalnizca seti dogrula, model yok

Ciktilar degerlendirmeler/ klasorune <tarih>_<saat>[_etiket].md ve .json
olarak yazilir. eval_results.md eski 12 soruluk setin sonucudur, dokunulmaz.
"""

import argparse
import hashlib
import json
import re
import sqlite3
import statistics
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import eval_set
from ingest import CHUNK_SIZE, CHUNKING, DOCS_DIR

# rag.FOREIGN_SCRIPT ile ayni; rag'i ice aktarmak model ayarlarini yukledigi
# icin burada tekrar tanimli.
FOREIGN_SCRIPT = re.compile(r"[぀-ヿ㐀-䶿一-鿿가-힯＀-￯]")
import search as search_module
from search import DB_PATH, EMBED_MODEL, QUERY_INSTRUCTION

OUT_DIR = Path("degerlendirmeler")
ALL_CHUNKS = 10**6      # retrieve() icin: tum parcalari sirali getir


# ---------------------------------------------------------------- yardimcilar

def norm(text):
    """Buyuk/kucuk harf, Turkce i/I ve tirnak farklarini gozetmeyen bicim."""
    text = text.replace("İ", "i").replace("I", "ı").lower().replace("̇", "")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"')):
        text = text.replace(a, b)
    return " ".join(text.split())


def alternatives(value):
    return [norm(v) for v in value.split("|")]


def contains_any(text, value):
    text = norm(text)
    return any(alt in text for alt in alternatives(value))


def cited_docs(text):
    """Cevaptaki (Kaynak: ...) satirlarinda gecen belge adlari."""
    docs = []
    for inside in re.findall(r"\(\s*Kaynak\s*:([^)]*)\)", text, flags=re.IGNORECASE):
        docs += re.findall(r"[\w\-]+\.md", inside)
    return docs


def evidence_rank(hits, case):
    """Kanit ifadesini iceren ilk parcanin sirasi (1'den baslar)."""
    for rank, (_score, _cid, doc, _idx, text) in enumerate(hits, 1):
        if doc in case["belge"].split("|") and contains_any(text, case["kanit"]):
            return rank
    return None


def git_state():
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                                capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain"],
                               capture_output=True, text=True).stdout.strip()
        return f"{commit}{' (kaydedilmemis degisiklik var)' if dirty else ''}"
    except OSError:
        return "-"


def question_set(name):
    """(tekil sorular, senaryolar). ana: ayar yapilan set; kontrol: Faz 5.5."""
    if name == "kontrol":
        return eval_set.KONTROL_SORULAR, eval_set.KONTROL_SENARYOLAR
    return eval_set.SORULAR, eval_set.SENARYOLAR


def set_fingerprint(name="ana"):
    data = json.dumps(list(question_set(name)), ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(data.encode("utf-8")).hexdigest()[:10]


# ------------------------------------------------------------ set dogrulamasi

def validate_set():
    """Setteki hatalari listele. Model gerektirmez, yalnizca belge ve DB okur."""
    errors = []
    conn = sqlite3.connect(DB_PATH)
    chunks = conn.execute("SELECT doc_name, text FROM chunks").fetchall()
    conn.close()

    all_questions = eval_set.SORULAR + eval_set.KONTROL_SORULAR
    all_scenarios = eval_set.SENARYOLAR + eval_set.KONTROL_SENARYOLAR
    cases = list(all_questions)
    for scenario in all_scenarios:
        cases += [dict(q, id=f"{scenario['id']}#{i}") for i, q in enumerate(scenario["sorular"], 1)]

    ids = [c["id"] for c in all_questions] + [s["id"] for s in all_scenarios]
    for dup in {i for i in ids if ids.count(i) > 1}:
        errors.append(f"{dup}: id birden fazla kez kullanilmis")

    for case in cases:
        if not case.get("belge"):
            continue
        if not case.get("kanit") or not case.get("anahtar"):
            errors.append(f"{case['id']}: belge var ama kanit/anahtar eksik")
            continue
        found_any = False
        for doc in case["belge"].split("|"):
            path = DOCS_DIR / doc
            if not path.exists():
                errors.append(f"{case['id']}: belge yok: {doc}")
                continue
            if contains_any(path.read_text(encoding="utf-8"), case["kanit"]):
                found_any = True
        if not found_any:
            errors.append(f"{case['id']}: kanit belgede bulunamadi: {case['kanit']!r}")
            continue
        in_chunk = any(doc in case["belge"].split("|") and contains_any(text, case["kanit"])
                       for doc, text in chunks)
        if not in_chunk:
            errors.append(f"{case['id']}: kanit hicbir parcaya tam sigmiyor "
                          f"(parca siniri kesiyor): {case['kanit']!r}")
    return errors, len(chunks)


# ------------------------------------------------------------------ calistirma

def evaluate_case(case, previous_question, answer_details, retrieve, follow_up_query):
    question = case["soru"]
    result = answer_details(question, previous_question=previous_question)
    # Arama metnini rag secti (isaret sozcugu ya da skor farki). Kanit sirasi
    # gercekte kullanilan sorguyla olculsun diye onu geri okuyoruz;
    # follow_up_query yalnizca yedek olarak duruyor.
    search_query = result.get("search_text") or follow_up_query(question, previous_question)
    text = result["text"]
    hits = result["hits"]

    refused = contains_any(text, "elimdeki dokümanlarda yok")
    cited = cited_docs(text)
    row = {
        "soru": question,
        "onceki_soru": previous_question,
        "arama_metni": search_query,
        "cevap": text,
        "getirilen": [f"{h[2]}#{h[3]} {h[0]:.3f}" for h in hits],
        "en_iyi_skor": round(result.get("best_score", hits[0][0] if hits else 0.0), 3) if hits else None,
        "esikte_red": not result["used_llm"],
        "takip_aramasi": result.get("used_follow_up", False),
        "dogrulama": result.get("verified"),
        "yabanci_yazi_kesildi": result.get("foreign_script_cut", False),
        "yabanci_yazi": bool(FOREIGN_SCRIPT.search(text)),
        "reddetti": refused,
        "kaynaklar": cited,
        "kaynak_var": bool(cited),
        "sure_arama": round(result["retrieval_sec"], 3),
        "sure_ilk_token": (round(result["first_token_sec"], 3)
                           if result["first_token_sec"] is not None else None),
        "sure_toplam": round(result["total_sec"], 3),
    }

    if case.get("belge"):
        full = retrieve(question, top_k=ALL_CHUNKS, search_query=search_query)
        rank = evidence_rank(full, case)
        missing = [k for k in case["anahtar"] if not contains_any(text, k)]
        forbidden = [k for k in case.get("yasak", []) if contains_any(text, k)]
        source_ok = any(d in case["belge"].split("|") for d in cited)
        row.update({
            "cevaplanabilir": True,
            "sira": rank,
            "hit1": rank == 1,
            "hit3": rank is not None and rank <= 3,
            "eksik_anahtar": missing,
            "yasak_bulunan": forbidden,
            "kaynak_dogru": source_ok,
            "basarili": (not refused and not missing and not forbidden and source_ok
                         and not row["yabanci_yazi"]),
        })
        reasons = []
        if refused:
            reasons.append("yanlış red" + (" (eşikte)" if row["esikte_red"] else
                                           " (doğrulama)" if row["dogrulama"] is False else " (model)"))
        if row["yabanci_yazi"]:
            reasons.append("Türkçe olmayan yazı")
        if not refused and missing:
            reasons.append("eksik: " + ", ".join(missing))
        if forbidden:
            reasons.append("yasak ifade: " + ", ".join(forbidden))
        if not refused and not source_ok:
            reasons.append("kaynak yok" if not cited else "yanlış kaynak: " + ", ".join(cited))
        if not row["hit3"]:
            reasons.append(f"doğru parça ilk 3'te değil (sıra {rank})")
    else:
        row.update({
            "cevaplanabilir": False,
            "basarili": refused and not cited,
        })
        reasons = []
        if not refused:
            reasons.append("cevaplanamaz soruya cevap verdi")
        elif cited:
            reasons.append("red cevabına kaynak eklendi")
    row["neden"] = reasons
    return row


def run_all(questions, scenarios, progress=print):
    from rag import answer_details, follow_up_query, retrieve

    # Isitma: ilk soru model yukleme suresini olcumlere katmasin. Ana setin
    # ilk sorusu kullanilir ki kontrol setinde isitma bir kontrol sorusunu
    # onceden gormus olmasin.
    progress("Isitma sorusu calisiyor...")
    answer_details(eval_set.SORULAR[0]["soru"])

    rows = []
    for case in questions:
        row = evaluate_case(case, None, answer_details, retrieve, follow_up_query)
        row.update(id=case["id"], grup="tekil",
                   kategori=case.get("kategori", "normal" if case.get("belge") else "cevapsiz"),
                   eski12=case.get("eski12", False))
        rows.append(row)
        progress(line(row))

    for scenario in scenarios:
        previous = None
        turns = scenario["sorular"]
        for i, turn in enumerate(turns, 1):
            row = evaluate_case(turn, previous, answer_details, retrieve, follow_up_query)
            last = i == len(turns)
            row.update(id=f"{scenario['id']}#{i}",
                       grup="senaryo" if last else "hazirlik",
                       kategori=scenario["tip"] if last else "hazirlik",
                       eski12=False)
            if not last:
                # Hazirlik sorusunun beklentisi tanimli degil; puanlanmaz.
                row.update(basarili=None, neden=[])
            rows.append(row)
            if last:
                progress(line(row))
            previous = turn["soru"]
    return rows


def line(row):
    mark = "OK  " if row["basarili"] else "HATA"
    rank = f"sira {row['sira']}" if row.get("sira") else ("sira -" if row["cevaplanabilir"] else "      ")
    why = f"  <- {'; '.join(row['neden'])}" if row["neden"] else ""
    return f"  {mark} [{row['sure_toplam']:4.1f} sn] {rank:7} {row['id']:18} {row['soru']}{why}"


# ------------------------------------------------------------------ ozetleme

def pct(part, whole):
    return None if whole == 0 else round(100 * part / whole, 1)


def summarize(rows):
    scored = [r for r in rows if r["grup"] != "hazirlik"]
    answerable = [r for r in scored if r["cevaplanabilir"]]
    unanswerable = [r for r in scored if not r["cevaplanabilir"]]
    llm_rows = [r for r in rows if r["sure_ilk_token"] is not None]
    totals = [r["sure_toplam"] for r in rows]
    ranks = [r["sira"] for r in answerable if r["sira"]]

    return {
        "soru_sayisi": len(scored),
        "cevaplanabilir": len(answerable),
        "cevaplanamaz": len(unanswerable),
        "basari": pct(sum(r["basarili"] for r in scored), len(scored)),
        "arama_hit1": pct(sum(r["hit1"] for r in answerable), len(answerable)),
        "arama_hit3": pct(sum(r["hit3"] for r in answerable), len(answerable)),
        "arama_mrr": round(sum(1 / r for r in ranks) / len(answerable), 3) if answerable else None,
        "cevap_basari": pct(sum(r["basarili"] for r in answerable), len(answerable)),
        "yanlis_red": pct(sum(r["reddetti"] for r in answerable), len(answerable)),
        "yanlis_red_esikte": pct(sum(r["reddetti"] and r["esikte_red"] for r in answerable), len(answerable)),
        "anahtar_tam": pct(sum(not r["eksik_anahtar"] for r in answerable if not r["reddetti"]),
                           sum(not r["reddetti"] for r in answerable)),
        "yasak_ifade_sayisi": sum(bool(r["yasak_bulunan"]) for r in answerable),
        "kaynak_var": pct(sum(r["kaynak_var"] for r in answerable if not r["reddetti"]),
                          sum(not r["reddetti"] for r in answerable)),
        "kaynak_dogru": pct(sum(r["kaynak_dogru"] for r in answerable if not r["reddetti"]),
                            sum(not r["reddetti"] for r in answerable)),
        "cevapsiz_red": pct(sum(r["reddetti"] for r in unanswerable), len(unanswerable)),
        "cevapsiz_esikte_red": pct(sum(r["esikte_red"] for r in unanswerable), len(unanswerable)),
        "red_kaynakli": sum(r["reddetti"] and r["kaynak_var"] for r in scored),
        "dogrulama_red_cevaplanabilir": sum(r.get("dogrulama") is False for r in answerable),
        "dogrulama_red_cevapsiz": sum(r.get("dogrulama") is False for r in unanswerable),
        "yabanci_yazi": sum(bool(r.get("yabanci_yazi")) for r in scored),
        "yabanci_yazi_kesildi": sum(bool(r.get("yabanci_yazi_kesildi")) for r in scored),
        "sure_ortalama": round(statistics.mean(totals), 2),
        "sure_medyan": round(statistics.median(totals), 2),
        "sure_en_uzun": round(max(totals), 2),
        "ilk_token_ortalama": (round(statistics.mean(r["sure_ilk_token"] for r in llm_rows), 2)
                               if llm_rows else None),
        "arama_ortalama": round(statistics.mean(r["sure_arama"] for r in rows), 3),
    }


METRIC_LABELS = [
    ("basari", "Tam başarı (tüm puanlanan sorular)", "%"),
    ("arama_hit1", "Arama: doğru parça 1. sırada (hit@1)", "%"),
    ("arama_hit3", "Arama: doğru parça ilk 3'te (hit@3)", "%"),
    ("arama_mrr", "Arama: MRR (1 = hep 1. sırada)", ""),
    ("cevap_basari", "Cevaplanabilir sorularda başarı", "%"),
    ("yanlis_red", "Yanlış red (cevap belgede varken)", "%"),
    ("yanlis_red_esikte", "  bunun eşikte olanı", "%"),
    ("anahtar_tam", "Anahtar ifadelerin tamamı cevapta", "%"),
    ("yasak_ifade_sayisi", "Bilinen yanlışı içeren cevap", " adet"),
    ("kaynak_var", "Kaynak satırı var", "%"),
    ("kaynak_dogru", "Kaynak doğru belge", "%"),
    ("cevapsiz_red", "Cevaplanamaz soruları reddetme", "%"),
    ("cevapsiz_esikte_red", "  bunun eşikte olanı", "%"),
    ("red_kaynakli", "Red cevabına eklenmiş kaynak satırı", " adet"),
    ("dogrulama_red_cevaplanabilir", "Doğrulamada reddedilen cevaplanabilir", " adet"),
    ("dogrulama_red_cevapsiz", "Doğrulamada reddedilen cevaplanamaz", " adet"),
    ("yabanci_yazi", "Türkçe olmayan yazı kalan cevap", " adet"),
    ("yabanci_yazi_kesildi", "Türkçe olmayan yazı kesilen cevap", " adet"),
    ("sure_ortalama", "Süre ortalaması", " sn"),
    ("sure_medyan", "Süre medyanı", " sn"),
    ("sure_en_uzun", "En uzun süre", " sn"),
    ("ilk_token_ortalama", "İlk token ortalaması (modele giden sorular)", " sn"),
    ("arama_ortalama", "Arama süresi ortalaması", " sn"),
]

CATEGORY_ORDER = ["normal", "ozel_ad", "yakin", "konu_disi", "anlamsiz",
                  "takip", "takip_cevapsiz", "konu_degisimi", "konu_disi_sonra", "hazirlik"]


def fmt(value, unit):
    return "-" if value is None else f"{value}{unit}"


def timing_warning(summary):
    """Ilk token suresi bozuk bellek duzenini gosteriyorsa uyari metni."""
    from foundry_client import SLOW_TTFT_SEC
    ttft = summary.get("ilk_token_ortalama")
    if ttft is not None and ttft > SLOW_TTFT_SEC:
        return (f"İlk token ortalaması {ttft} sn, {SLOW_TTFT_SEC} sn sınırının üstünde. "
                "Ekran kartı belleği bozuk düzende olabilir (rag_iyilestirme_plani.md Bölüm 2.5); "
                "süre ölçütleri geçersiz sayılmalı. Doğruluk ölçütleri bundan etkilenmez. "
                "Sunucuyu yeniden başlatıp (foundry server stop) tekrar ölçün.")
    return None


# ------------------------------------------------------------------- rapor

def write_report(meta, rows, summary, path, previous=None):
    for r in rows:
        if r["grup"] == "hazirlik":      # eski JSON'larda False yazili olabilir
            r["basarili"], r["neden"] = None, []
    L = []
    L.append(f"# Değerlendirme: {meta['tarih']}{' — ' + meta['etiket'] if meta['etiket'] else ''}\n")
    L.append("| Ayar | Değer |\n|---|---|")
    for key in ("soru_seti", "sohbet_modeli", "gomme_modeli", "top_k", "min_score", "takip_farki", "max_tokens",
                "parca_sayisi", "parcalama", "chunk_size", "overlap", "sorgu_talimati", "arama", "cevap_dogrulama",
                "git", "set_parmak_izi"):
        if key in meta:     # eski calismalarda parcalama, yenilerde overlap yok
            L.append(f"| {key} | {meta[key]} |")

    L.append(f"\n## Özet\n")
    warning = timing_warning(summary)
    if warning:
        L.append(f"> **Uyarı:** {warning}\n")
    L.append(f"Puanlanan soru: {summary['soru_sayisi']} "
             f"({summary['cevaplanabilir']} cevaplanabilir, {summary['cevaplanamaz']} cevaplanamaz). "
             f"Senaryoların hazırlık soruları özete katılmaz.\n")
    if previous:
        prev_summary = previous["ozet"]
        L.append(f"Karşılaştırılan çalışma: `{previous['dosya']}`"
                 + ("" if previous["meta"]["set_parmak_izi"] == meta["set_parmak_izi"]
                    else " — **uyarı: soru seti farklı, karşılaştırma kısmen geçerli**") + "\n")
        L.append("| Ölçüt | Önceki | Şimdi |\n|---|---|---|")
        for key, label, unit in METRIC_LABELS:
            L.append(f"| {label} | {fmt(prev_summary.get(key), unit)} | {fmt(summary.get(key), unit)} |")
    else:
        L.append("| Ölçüt | Değer |\n|---|---|")
        for key, label, unit in METRIC_LABELS:
            L.append(f"| {label} | {fmt(summary.get(key), unit)} |")

    L.append("\n## Kategorilere göre\n")
    L.append("| Kategori | Soru | Başarılı | hit@1 | hit@3 | Yanlış red |\n|---|---|---|---|---|---|")
    for cat in CATEGORY_ORDER:
        group = [r for r in rows if r["kategori"] == cat]
        if not group:
            continue
        if cat == "hazirlik":
            L.append(f"| {cat} (puanlanmaz) | {len(group)} | - | - | - | - |")
            continue
        ans = [r for r in group if r["cevaplanabilir"]]
        L.append(f"| {cat} | {len(group)} | {sum(r['basarili'] for r in group)} | "
                 f"{sum(r['hit1'] for r in ans) if ans else '-'} | "
                 f"{sum(r['hit3'] for r in ans) if ans else '-'} | "
                 f"{sum(r['reddetti'] for r in ans) if ans else '-'} |")
    eski = [r for r in rows if r["eski12"]]
    if eski:
        L.append(f"\nEski 12 soruluk set (eval_results.md ile aynı sorular): "
                 f"**{sum(r['basarili'] for r in eski)}/{len(eski)}** başarılı.")

    if previous:
        prev_rows = {r["id"]: r for r in previous["sonuclar"]}
        changed = [(r, prev_rows[r["id"]]) for r in rows
                   if r["grup"] != "hazirlik" and r["id"] in prev_rows
                   and r["basarili"] != prev_rows[r["id"]]["basarili"]]
        text_changed = sum(1 for r in rows if r["id"] in prev_rows and r["cevap"] != prev_rows[r["id"]]["cevap"])
        L.append(f"\n## Önceki çalışmaya göre değişen sorular\n")
        L.append(f"Cevap metni değişen soru: {text_changed}. Sonucu değişen soru: {len(changed)}.\n")
        for r, p in changed:
            L.append(f"- **{r['id']}** {'HATA → OK' if r['basarili'] else 'OK → HATA'}: {r['soru']}"
                     + (f" ({'; '.join(r['neden'])})" if r["neden"] else ""))

    L.append("\n## Başarısız sorular\n")
    failed = [r for r in rows if not r["basarili"] and r["grup"] != "hazirlik"]
    if not failed:
        L.append("Yok.")
    for r in failed:
        L.append(f"- **{r['id']}** ({r['kategori']}) {r['soru']}")
        if r["onceki_soru"]:
            L.append(f"  - Önceki soru: {r['onceki_soru']}")
        L.append(f"  - Neden: {'; '.join(r['neden'])}")
        L.append(f"  - Cevap: {r['cevap'].replace(chr(10), ' ')}")

    L.append("\n## Tüm sonuçlar\n")
    L.append("| id | Kategori | Sıra | En iyi skor | Eşikte red | Red | Anahtar | Kaynak | Süre | Sonuç |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        ans = r["cevaplanabilir"]
        L.append(
            f"| {r['id']} | {r['kategori']} | {r.get('sira') or '-' if ans else ''} | "
            f"{r['en_iyi_skor']} | {'evet' if r['esikte_red'] else ''} | {'evet' if r['reddetti'] else ''} | "
            f"{('tam' if not r['eksik_anahtar'] else 'eksik') if ans and not r['reddetti'] else ''} | "
            f"{('doğru' if r['kaynak_dogru'] else ('yanlış' if r['kaynak_var'] else 'yok')) if ans and not r['reddetti'] else ('var' if r['kaynak_var'] else '')} | "
            f"{r['sure_toplam']:.1f} | {'-' if r['basarili'] is None else ('OK' if r['basarili'] else 'HATA')} |"
        )

    L.append("\n## Cevaplar (gözle kontrol için)\n")
    for r in rows:
        L.append(f"**{r['id']}** — {r['soru']}" + (f"  \n_Önceki soru: {r['onceki_soru']}_" if r["onceki_soru"] else ""))
        L.append(f"> {r['cevap'].replace(chr(10), ' ')}\n")
        L.append(f"Getirilen: `{' | '.join(r['getirilen'])}`\n")

    path.write_text("\n".join(L) + "\n", encoding="utf-8")


# -------------------------------------------------------------------- giris

def main():
    parser = argparse.ArgumentParser(description="RAG degerlendirmesi")
    parser.add_argument("--etiket", default="", help="dosya adina ve rapora eklenecek kisa ad")
    parser.add_argument("--karsilastir", help="onceki bir calismanin .json dosyasi")
    parser.add_argument("--kontrol", action="store_true", help="yalnizca seti dogrula")
    parser.add_argument("--set", choices=["ana", "kontrol"], default="ana",
                        help="ana: ayar yapilan set; kontrol: Faz 5.5 kontrol seti (ayar icin kullanilmaz)")
    parser.add_argument("--rapor", help="model calistirmadan, bir .json sonucundan .md raporunu yeniden yaz")
    args = parser.parse_args()

    if args.rapor:
        data = json.loads(Path(args.rapor).read_text(encoding="utf-8"))
        previous = None
        if args.karsilastir:
            previous = json.loads(Path(args.karsilastir).read_text(encoding="utf-8"))
            previous["dosya"] = args.karsilastir
        md_path = Path(args.rapor).with_suffix(".md")
        write_report(data["meta"], data["sonuclar"], data["ozet"], md_path, previous)
        print(f"Yazildi: {md_path}")
        return

    errors, chunk_count = validate_set()
    for name in ("ana", "kontrol"):
        qs, scs = question_set(name)
        n_cases = len(qs) + sum(len(s["sorular"]) for s in scs)
        print(f"Set {name:7}: {len(qs)} tekil soru, {len(scs)} senaryo ({n_cases} soru), "
              f"parmak izi {set_fingerprint(name)}")
    print(f"Veritabaninda {chunk_count} parca")
    if errors:
        print("\nSet hatalari:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("Set dogrulandi.")
    if args.kontrol:
        return

    previous = None
    if args.karsilastir:
        previous = json.loads(Path(args.karsilastir).read_text(encoding="utf-8"))
        previous["dosya"] = args.karsilastir

    from foundry_client import find_model
    from rag import ANSWER_VERIFICATION, VERIFY_PROMPT_NAME, CHAT_KEYWORD, FOLLOW_UP_MARGIN, MAX_TOKENS, MIN_SCORE, TOP_K

    now = datetime.now()
    slug = re.sub(r"[^\w\-]+", "-", args.etiket).strip("-")
    stem = (now.strftime("%Y-%m-%d_%H%M") + ("_kontrol" if args.set == "kontrol" else "")
            + (f"_{slug}" if slug else ""))
    meta = {
        "tarih": now.strftime("%Y-%m-%d %H:%M"),
        "etiket": args.etiket,
        "soru_seti": args.set,
        "sohbet_modeli": find_model(CHAT_KEYWORD),
        "gomme_modeli": find_model(EMBED_MODEL),
        "top_k": TOP_K, "min_score": MIN_SCORE, "takip_farki": FOLLOW_UP_MARGIN,
        "max_tokens": MAX_TOKENS,
        "parca_sayisi": chunk_count, "parcalama": CHUNKING, "chunk_size": CHUNK_SIZE,
        "sorgu_talimati": QUERY_INSTRUCTION or "yok",
        "cevap_dogrulama": f"açık ({VERIFY_PROMPT_NAME})" if ANSWER_VERIFICATION else "kapalı",
        "arama": (f"hibrit: vektör + FTS5 ({search_module.KEYWORD_PREFIX} harf önek), RRF k={search_module.RRF_K}"
                  if search_module.HYBRID_SEARCH else "yalnız vektör"),
        "git": git_state(),
        "set_parmak_izi": set_fingerprint(args.set),
    }

    rows = run_all(*question_set(args.set))
    summary = summarize(rows)

    OUT_DIR.mkdir(exist_ok=True)
    json_path = OUT_DIR / f"{stem}.json"
    md_path = OUT_DIR / f"{stem}.md"
    json_path.write_text(json.dumps({"meta": meta, "ozet": summary, "sonuclar": rows},
                                    ensure_ascii=False, indent=1), encoding="utf-8")
    write_report(meta, rows, summary, md_path, previous)

    print()
    for key, label, unit in METRIC_LABELS:
        print(f"  {label:48} {fmt(summary.get(key), unit)}")
    if timing_warning(summary):
        print(f"\nUYARI: {timing_warning(summary)}")
    print(f"\nYazildi: {md_path}\n         {json_path}")


if __name__ == "__main__":
    main()
