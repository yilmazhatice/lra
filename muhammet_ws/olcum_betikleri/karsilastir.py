"""qwen2.5-7b ile qwen3-4b'yi ayni baglam ve ayni istemle karsilastirir.

Proje koduna dokunmaz; rag.py'deki istemi, arama ve yardimci fonksiyonlari
ice aktarip kullanir.

Surum 2 (bellek sirasi bulgusundan sonra): her model temiz bir sunucuda,
bellekte tek basina calisir. Surum 1 modelleri bosaltip yeniden yukluyordu;
bu qwen2.5-7b'yi bozuk bellek duzeninde olctu (ilk sonuc:
karsilastirma_sonuc_2026-09-14.json).
Kullanim: python karsilastir.py [cikti_dosyasi.json]
"""
import json, os, subprocess, sys, time

LRA = r"C:\Workspace\microsoft_ws\lra"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "karsilastirma_sonuc_temiz_bellek.json")
sys.path.insert(0, LRA)
os.chdir(LRA)

import foundry_client as fc
from foundry_client import client, find_model, _foundry
from rag import (SYSTEM_PROMPT, MAX_TOKENS, MIN_SCORE, build_context,
                 retrieve, strip_thinking)

QUESTIONS = [
    "fatih kimdir",
    "böri nedir",
    "Osman Gazi kimdir",
    "Orhan Gazi kimdir",
    "Orhun Yazıtları'nın alfabesini kim ve hangi yılda çözmüştür?",
    "Turan taktiği nasıl uygulanır?",
    "Eski Türkçede kurdun adı neydi?",
    "Anadolu Selçuklu Devleti hangi savaşta Moğollara yenilmiştir?",
    "Yavuz Sultan Selim hangi savaşlarla Mısır'ı Osmanlı topraklarına katmıştır?",
    "Sakarya Meydan Muharebesi kaç gün sürmüştür?",
    "Üç Tarz-ı Siyaset yazısı nerede ve hangi yıl yayımlanmıştır?",
    "Milliyetçi Hareket Partisi adı hangi kongrede kabul edilmiştir?",
    "Ülkü Ocakları 12 Mart 1971'den sonra hangi adla yeniden kurulmuştur?",
    "Fatih Sultan Mehmed'in annesinin adı nedir?",   # dokumanda yok: uydurmamali
]


def gpu_mem():
    """foundrylocald'nin ayrilmis ve paylasilan GPU bellegi (MB)."""
    ps = ("$p=(Get-Process foundrylocald).Id;"
          "Get-Counter '\\GPU Process Memory(*)\\Dedicated Usage','\\GPU Process Memory(*)\\Shared Usage' |"
          " % CounterSamples | ? { $_.InstanceName -like \"pid_${p}_*\" -and $_.CookedValue -gt 0 } |"
          " % { ($_.Path.Split('\\')[-1] -replace ' ','_') + '=' + [int]($_.CookedValue/1MB) }")
    out = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                         capture_output=True, text=True).stdout.split()
    return dict(x.split("=", 1) for x in out if "=" in x)


def messages_for(q, hits, no_think):
    system = SYSTEM_PROMPT + ("\n/no_think" if no_think else "")
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": f"BAĞLAM:\n{build_context(hits)}\n\nSORU: {q}\n\nTürkçe cevap ver."},
    ]


def ask(model_id, msgs):
    t0 = time.perf_counter(); first = None; parts = []
    stream = client().chat.completions.create(
        model=model_id, messages=msgs, temperature=0.0,
        max_tokens=MAX_TOKENS, stream=True)
    for ch in stream:
        if ch.choices and ch.choices[0].delta.content:
            if first is None:
                first = time.perf_counter()
            parts.append(ch.choices[0].delta.content)
    end = time.perf_counter()
    raw = "".join(parts)
    gen = end - (first or end)
    return {
        "ham": raw,
        "cevap": strip_thinking(raw),
        "ilk_token_sn": round((first or end) - t0, 2),
        "uretim_sn": round(gen, 2),
        "parca": len(parts),
        "tok_sn": round(len(parts) / gen, 1) if gen > 0 else None,
        "toplam_sn": round(end - t0, 2),
    }


def run_model(label, model_id, cases, no_think, limit=None):
    print(f"\n=== {label} ({model_id}) bellek: {gpu_mem()}", flush=True)
    ask(model_id, messages_for("Merhaba", [], no_think))   # isitma, sayilmaz
    rows = []
    for c in cases[:limit]:
        r = ask(model_id, messages_for(c["soru"], c["hits"], no_think))
        r["soru"] = c["soru"]
        rows.append(r)
        print(f"[{r['toplam_sn']:5.1f} sn | ilk {r['ilk_token_sn']:4.1f} | {r['tok_sn']} tok/sn] "
              f"{c['soru']}\n    {r['cevap'][:200]!r}", flush=True)
    return {"model": model_id, "bellek": gpu_mem(), "sonuclar": rows}


def load_clean(model_id):
    """Sunucuyu yeniden baslatip modeli bellekte tek basina yukle."""
    subprocess.run(["foundry", "server", "stop"], capture_output=True, timeout=120)
    time.sleep(3)
    fc.get_endpoint()
    _foundry("model", "load", model_id, timeout=600)


if __name__ == "__main__":
    old_id = find_model("qwen2.5-7b")
    new_id = find_model("qwen3-4b")

    # Baglam bir kez getiriliyor; iki model de birebir ayni parcalari goruyor.
    cases = []
    for q in QUESTIONS:
        hits = retrieve(q)
        cases.append({"soru": q, "hits": hits, "esik_alti": hits[0][0] < MIN_SCORE})
    llm_cases = [c for c in cases if not c["esik_alti"]]
    print("Modele giden soru:", len(llm_cases), "/", len(cases),
          "| esik alti:", [c["soru"] for c in cases if c["esik_alti"]])

    result = {"esik_alti": [c["soru"] for c in cases if c["esik_alti"]]}

    load_clean(old_id)
    result["qwen2.5-7b"] = run_model("qwen2.5-7b", old_id, llm_cases, no_think=False)
    json.dump(result, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    load_clean(new_id)
    result["qwen3-4b"] = run_model("qwen3-4b /no_think", new_id, llm_cases, no_think=True)
    json.dump(result, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    result["qwen3-4b-dusunme"] = run_model("qwen3-4b dusunme acik", new_id, llm_cases, no_think=False, limit=2)
    json.dump(result, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # Ortami eski haline getir: uygulama qwen2.5-7b ile calismaya devam etsin.
    load_clean(old_id)
    print("\nBitti. Ortam geri yuklendi:", gpu_mem())
