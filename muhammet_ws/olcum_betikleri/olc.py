import sys, time
sys.path.insert(0, r"C:\Workspace\microsoft_ws\lra")
import os
os.chdir(r"C:\Workspace\microsoft_ws\lra")

from search import search
from rag import MIN_SCORE, SYSTEM_PROMPT, build_context, CHAT_KEYWORD, MAX_TOKENS
from foundry_client import client, with_model

# 1) Takip sorusu birlestirmesinin skora etkisi
for q in ["fatih kimdir", "böri nedir", "fatih kimdir böri nedir",
          "Osman Gazi kimdir", "Orhan Gazi kimdir", "Osman Gazi kimdir Orhan Gazi kimdir"]:
    t = time.perf_counter()
    hits = search(q)
    print(f"{q!r:45} en_iyi={hits[0][0]:.3f} {hits[0][2]}  esik={MIN_SCORE}  [{time.perf_counter()-t:.2f} sn]")

# 2) LLM suresi: on isleme (prefill) ve uretim hizi ayri ayri
hits = search("Orhan Gazi kimdir")
messages = [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"BAĞLAM:\n{build_context(hits)}\n\nSORU: Orhan Gazi kimdir\n\nTürkçe cevap ver."}]
print("baglam karakter:", sum(len(m["content"]) for m in messages))

def run(model_id):
    t0 = time.perf_counter(); first = None; n = 0
    stream = client().chat.completions.create(model=model_id, messages=messages,
        temperature=0.0, max_tokens=MAX_TOKENS, stream=True)
    for ch in stream:
        if ch.choices and ch.choices[0].delta.content:
            if first is None: first = time.perf_counter()
            n += 1
    end = time.perf_counter()
    print(f"ilk token: {first-t0:.1f} sn, uretim: {n} parca / {end-first:.1f} sn = {n/(end-first):.1f} tok/sn")

with_model(CHAT_KEYWORD, run)
