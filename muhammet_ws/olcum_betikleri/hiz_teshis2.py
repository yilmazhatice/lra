"""Yukleme sirasi hipotezinin uygulamanin gercek akisiyla testi.

A: uygulamanin bugunku sirasi (once arama -> gomme modeli ilk yuklenir)
B: once sohbet modeli yuklenip RAG boyutunda bir istemle isitilir,
   gomme modeli sonra yuklenir

Her iki senaryoda sunucu temiz baslatilir ve rag.answer() ile ard arda
5 soru sorulur (max_tokens=350, uygulamadaki gibi). Proje koduna dokunmaz.
Kullanim: python hiz_teshis2.py [A] [B]
"""
import os, subprocess, sys, time

LRA = r"C:\Workspace\microsoft_ws\lra"
sys.path.insert(0, LRA); os.chdir(LRA)

import foundry_client as fc
from rag import answer, retrieve, build_context, SYSTEM_PROMPT, CHAT_KEYWORD
from search import EMBED_MODEL

QUESTIONS = ["fatih kimdir", "böri nedir", "Osman Gazi kimdir",
             "Orhan Gazi kimdir", "Turan taktiği nasıl uygulanır?"]


def mem():
    out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                         capture_output=True, text=True).stdout.strip()
    ps = ("$p=(Get-Process foundrylocald -EA SilentlyContinue).Id; if($p){"
          "Get-Counter '\\GPU Process Memory(*)\\Shared Usage' | % CounterSamples |"
          " ? { $_.InstanceName -like \"pid_${p}_*\" } | Measure-Object CookedValue -Maximum |"
          " % { [int]($_.Maximum/1MB) } }")
    shared = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                            capture_output=True, text=True).stdout.strip()
    return f"GPU {out} MB, foundry paylasilan {shared} MB"


def fresh_server():
    subprocess.run(["foundry", "server", "stop"], capture_output=True, timeout=120)
    time.sleep(3)
    fc.get_endpoint()   # sunucuyu baslatir, onbellekleri sifirlar
    print("   temiz sunucu:", mem(), flush=True)


def run_questions(label):
    print(f"\n=== {label}", flush=True)
    times = []
    prev = None
    for q in QUESTIONS:
        arama = f"{prev} {q}" if prev else q
        text, hits, elapsed = answer(q, search_query=arama)
        times.append(elapsed)
        print(f"   [{elapsed:5.1f} sn] {q} -> {text[:70]!r}", flush=True)
        prev = q
    print(f"   ortalama {sum(times)/len(times):.1f} sn | {mem()}", flush=True)


def scenario_a():
    fresh_server()
    run_questions("A: uygulamanin bugunku sirasi (gomme modeli once)")


def scenario_b():
    fresh_server()
    chat = fc.find_model(CHAT_KEYWORD)
    fc.ensure_loaded(chat)
    # RAG boyutunda isitma: calisma bellegi gomme modelinden once ayrilsin.
    # Gomme modeli henuz yuklu olmadigi icin baglam sabit metinden kuruluyor.
    dummy = [(0, 0, "isitma.md", 0, open("docs/osmanli-padisahlari.md", encoding="utf-8").read()[:2800])]
    t = time.perf_counter()
    fc.client().chat.completions.create(model=chat, max_tokens=1, temperature=0.0, messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"BAĞLAM:\n{build_context(dummy)}\n\nSORU: test"}])
    print(f"   isitma {time.perf_counter()-t:.1f} sn | {mem()}", flush=True)
    fc.ensure_loaded(fc.find_model(EMBED_MODEL))
    print("   gomme modeli yuklendi:", mem(), flush=True)
    run_questions("B: once sohbet modeli + isitma, sonra gomme")


if __name__ == "__main__":
    which = sys.argv[1:] or ["A", "B"]
    if "A" in which: scenario_a()
    if "B" in which: scenario_b()
