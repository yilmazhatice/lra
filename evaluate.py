"""12 soruluk degerlendirme setini calistirir, sonuclari eval_results.md'ye yazar."""

import time

from rag import answer, MIN_SCORE

REDDETME = "elimdeki dokümanlarda yok"

# (soru, beklenen_kaynak_dosya) — None ise soru dokumanlarda cevaplanamaz
CASES = [
    ("Orhun Yazıtları'nın alfabesini kim ve hangi yılda çözmüştür?",
     "ilk-turk-devletleri.md"),
    ("Turan taktiği nasıl uygulanır?",
     "turk-kulturunde-at.md"),
    ("Eski Türkçede kurdun adı neydi?",
     "turk-kulturunde-kurt.md"),
    ("Anadolu Selçuklu Devleti hangi savaşta Moğollara yenilmiştir?",
     "selcuklular-ve-malazgirt.md"),
    ("Yavuz Sultan Selim hangi savaşlarla Mısır'ı Osmanlı topraklarına katmıştır?",
     "osmanli-padisahlari.md"),
    ("Sakarya Meydan Muharebesi kaç gün sürmüştür?",
     "canakkale-ve-kurtulus-savasi.md"),
    ("Üç Tarz-ı Siyaset yazısı nerede ve hangi yıl yayımlanmıştır?",
     "turk-milliyetciliginin-dogusu.md"),
    ("Milliyetçi Hareket Partisi adı hangi kongrede kabul edilmiştir?",
     "milliyetci-hareketin-isimleri.md"),
    ("Ülkü Ocakları 12 Mart 1971'den sonra hangi adla yeniden kurulmuştur?",
     "ulku-ocaklari.md"),
    ("Fatih Sultan Mehmed'in annesinin adı nedir?", None),
    ("Bugün hava nasıl olacak?", None),
    ("asdf qwerty zxcv", None),
]


def run():
    rows = []
    details = []

    for i, (question, expected) in enumerate(CASES, 1):
        text, hits, elapsed = answer(question)

        top_score = hits[0][0] if hits else 0.0
        retrieved = [h[2] for h in hits]
        reddetti = REDDETME in text

        if expected is None:
            # Cevaplanamaz soru: dogru davranis reddetmektir
            basarili = reddetti
            hit = "-"
        else:
            hit = "evet" if expected in retrieved else "HAYIR"
            basarili = (expected in retrieved) and not reddetti

        rows.append({
            "no": i,
            "soru": question,
            "beklenen": expected or "(cevaplanamaz)",
            "hit": hit,
            "reddetti": "evet" if reddetti else "hayir",
            "skor": top_score,
            "sure": elapsed,
            "basarili": basarili,
        })
        details.append((i, question, text, retrieved, top_score))
        print(f"{i:2}. {'OK ' if basarili else 'HATA'} [{elapsed:5.1f}s] {question}")

    write_report(rows, details)
    ok = sum(r["basarili"] for r in rows)
    print(f"\nBasarili: {ok}/{len(rows)}")


def write_report(rows, details):
    lines = []
    lines.append("# Değerlendirme Sonuçları\n")
    lines.append(f"Eşik değeri (MIN_SCORE): {MIN_SCORE}\n")

    ok = sum(r["basarili"] for r in rows)
    ort = sum(r["sure"] for r in rows) / len(rows)
    lines.append(f"- Başarılı: **{ok}/{len(rows)}**")
    lines.append(f"- Ortalama yanıt süresi: **{ort:.1f} sn**\n")

    lines.append("## Özet tablo\n")
    lines.append("| # | Soru | Beklenen kaynak | hit@3 | Reddetti | En yüksek skor | Süre (sn) | Sonuç |")
    lines.append("|---|------|-----------------|-------|----------|----------------|-----------|-------|")
    for r in rows:
        lines.append(
            f"| {r['no']} | {r['soru']} | {r['beklenen']} | {r['hit']} | "
            f"{r['reddetti']} | {r['skor']:.3f} | {r['sure']:.1f} | "
            f"{'OK' if r['basarili'] else 'HATA'} |"
        )

    lines.append("\n## Cevaplar\n")
    for i, question, text, retrieved, score in details:
        lines.append(f"### {i}. {question}\n")
        lines.append(f"Getirilen: `{', '.join(retrieved)}` — en yüksek skor: {score:.3f}\n")
        lines.append(f"> {text}\n")

    with open("eval_results.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\neval_results.md yazildi.")


if __name__ == "__main__":
    run()