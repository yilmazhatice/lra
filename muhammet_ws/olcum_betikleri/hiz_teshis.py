"""qwen2.5-7b yavasliginin teshisi. Proje koduna dokunmaz.

Senaryolar:
  S1  mevcut durum (gomme + sohbet modeli yuklu)
  S2  gomme modeli bellekten cikarilmis
  S3  sunucu yeniden baslatilmis, yalnizca sohbet modeli yuklu
  S4  S3'un ustune gomme modeli sonradan yuklenmis (yukleme sirasi: once sohbet)

Her senaryoda:
  - kisa istem  -> saf uretim hizi (baglam etkisi yok)
  - RAG istemi  -> ilk token suresi (bağlam okuma) + uretim hizi
  - ayni anda GPU kullanim orani ve bellek ornekleniyor
"""
import os, subprocess, sys, threading, time

LRA = r"C:\Workspace\microsoft_ws\lra"
sys.path.insert(0, LRA); os.chdir(LRA)

from foundry_client import client, find_model, _foundry
from rag import SYSTEM_PROMPT, build_context
from search import search, EMBED_MODEL

CHAT = find_model("qwen2.5-7b")
EMB = find_model(EMBED_MODEL)


def smi():
    out = subprocess.run(
        ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total",
         "--format=csv,noheader,nounits"], capture_output=True, text=True).stdout
    u, used, total = [int(x) for x in out.strip().split(",")]
    return u, used, total


def foundry_mem():
    ps = ("$p=(Get-Process foundrylocald).Id;"
          "Get-Counter '\\GPU Process Memory(*)\\Dedicated Usage','\\GPU Process Memory(*)\\Shared Usage' |"
          " % CounterSamples | ? { $_.InstanceName -like \"pid_${p}_*\" -and $_.CookedValue -gt 1MB } |"
          " % { ($_.Path.Split('\\')[-1] -replace ' usage','') + '=' + [int]($_.CookedValue/1MB) }")
    out = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                         capture_output=True, text=True).stdout.split()
    return " ".join(out)


class Sampler(threading.Thread):
    """Istek suresince saniyede bir GPU kullanim oranini topla."""
    def __init__(self):
        super().__init__(daemon=True); self.stop = False; self.util = []
    def run(self):
        while not self.stop:
            self.util.append(smi()[0]); time.sleep(0.5)


def ask(msgs, max_tokens):
    s = Sampler(); s.start()
    t0 = time.perf_counter(); first = None; n = 0
    for ch in client().chat.completions.create(
            model=CHAT, messages=msgs, temperature=0.0,
            max_tokens=max_tokens, stream=True):
        if ch.choices and ch.choices[0].delta.content:
            first = first or time.perf_counter(); n += 1
    end = time.perf_counter(); s.stop = True; s.join()
    gen = end - first
    util = sorted(s.util)
    return (first - t0, n / gen if gen > 0 else 0,
            util[len(util) // 2] if util else -1, max(util) if util else -1)


hits = search("Orhan Gazi kimdir")
RAG = [{"role": "system", "content": SYSTEM_PROMPT},
       {"role": "user", "content": f"BAĞLAM:\n{build_context(hits)}\n\nSORU: Orhan Gazi kimdir\n\nTürkçe cevap ver."}]
SHORT = [{"role": "user", "content": "Türkiye'nin başkenti neresidir? Bir cümleyle yaz."}]


def scenario(label):
    u, used, total = smi()
    print(f"\n=== {label}\n    GPU bellek {used}/{total} MB | foundrylocald: {foundry_mem()}", flush=True)
    ask(SHORT, 5)  # isitma
    ttft, tps, umed, umax = ask(SHORT, 60)
    print(f"    kisa istem : ilk token {ttft:5.2f} sn | {tps:5.1f} tok/sn | GPU kullanim medyan %{umed} maks %{umax}", flush=True)
    ttft, tps, umed, umax = ask(RAG, 80)
    print(f"    RAG istemi : ilk token {ttft:5.2f} sn | {tps:5.1f} tok/sn | GPU kullanim medyan %{umed} maks %{umax}", flush=True)
    u, used, total = smi()
    print(f"    sonra: GPU bellek {used}/{total} MB | foundrylocald: {foundry_mem()}", flush=True)


def loaded():
    return {m["displayName"] for m in _foundry("cache", "list").get("models", []) if m.get("loaded")}


if __name__ == "__main__":
    only = sys.argv[1:] or ["S1", "S2", "S3", "S4"]
    print("yuklu modeller:", loaded())

    if "S1" in only:
        for m in (EMB, CHAT):
            if m not in loaded(): _foundry("model", "load", m, timeout=600)
        scenario("S1 mevcut durum: gomme + sohbet")

    if "S2" in only:
        _foundry("model", "unload", EMB, timeout=120)
        scenario("S2 gomme modeli cikarildi")

    if "S3" in only:
        subprocess.run(["foundry", "server", "stop"], capture_output=True, timeout=120)
        time.sleep(3)
        _foundry("model", "load", CHAT, timeout=600)
        scenario("S3 temiz sunucu, yalnizca sohbet modeli")

    if "S4" in only:
        _foundry("model", "load", EMB, timeout=600)
        search("Orhan Gazi kimdir")  # gomme modeli de calismis olsun
        scenario("S4 once sohbet sonra gomme yuklendi")

    print("\nsonuc: yuklu modeller:", loaded())
