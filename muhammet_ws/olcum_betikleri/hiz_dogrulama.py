"""set_primary() duzeltmesinin dogrulamasi. Uygulama tarafi yalnizca
rag.answer() kullanir; her "uygulama" ayri bir Python islemidir.

V1   temiz sunucu, uygulamanin normal akisi (duzeltme oncesi ~48 sn)
V1b  saglam bellekli sunucuya ikinci kez baglanma (yeniden baslatma olmamali)
V2   bozuk bellek: once gomme modeli calisir, sonra sohbet modeli (duzeltme
     oncesi uygulamanin sirasi); uygulama bunu fark edip duzeltmeli
V3   oturum ortasinda sohbet modeli bellekten atiliyor
"""
import os, subprocess, sys, time

LRA = r"C:\Workspace\microsoft_ws\lra"
PY = os.path.join(LRA, ".venv", "Scripts", "python.exe")
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}
QUESTIONS = ["fatih kimdir", "böri nedir", "Osman Gazi kimdir",
             "Orhan Gazi kimdir", "Turan taktiği nasıl uygulanır?"]


def app_session(unload_midway=False):
    sys.path.insert(0, LRA); os.chdir(LRA)
    from rag import answer, CHAT_KEYWORD
    import foundry_client as fc

    # Sunucunun yeniden baslatilip baslatilmadigini gormek icin izle
    original_stop = subprocess.run
    def watched(cmd, *a, **k):
        if list(cmd[:3]) == ["foundry", "server", "stop"]:
            print("   >> bellek bozuk bulundu, sunucu yeniden baslatiliyor", flush=True)
        return original_stop(cmd, *a, **k)
    fc.subprocess.run = watched

    times = []
    prev = None
    for i, q in enumerate(QUESTIONS):
        if unload_midway and i == 3:
            original_stop(["foundry", "model", "unload", fc.find_model(CHAT_KEYWORD)],
                          capture_output=True, timeout=120)
            print("   -- sohbet modeli disaridan bellekten atildi --", flush=True)
        text, hits, elapsed = answer(q, search_query=f"{prev} {q}" if prev else q)
        times.append(elapsed)
        print(f"   [{elapsed:5.1f} sn] {q} -> {text[:55]!r}", flush=True)
        prev = q
    print(f"   ilk soru {times[0]:.1f} sn, sonraki 4 sorunun ortalamasi {sum(times[1:])/4:.1f} sn", flush=True)


def break_memory():
    """Duzeltme oncesi uygulama sirasi: gomme modeli once calisir."""
    sys.path.insert(0, LRA); os.chdir(LRA)
    import foundry_client as fc
    from search import search
    from rag import build_context, SYSTEM_PROMPT, CHAT_KEYWORD
    fc._primary = None                      # duzeltmeyi devre disi birak
    hits = search("Orhan Gazi kimdir")      # gomme modeli yuklenir ve calisir
    chat = fc.find_model(CHAT_KEYWORD)
    fc.ensure_loaded(chat)
    for q in ("Orhan Gazi kimdir", "Turan taktiği nasıl uygulanır?"):
        t = time.perf_counter()
        fc.client().chat.completions.create(model=chat, max_tokens=1, temperature=0.0, messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"BAĞLAM:\n{build_context(search(q))}\n\nSORU: {q}"}])
        print(f"   bozuk durum olusturuldu, istem {time.perf_counter()-t:.1f} sn", flush=True)


def child(*args):
    subprocess.run([PY, "-u", __file__, *args], env=ENV)


if __name__ == "__main__":
    if sys.argv[1:2] == ["--app"]:
        app_session(unload_midway="--unload" in sys.argv); sys.exit()
    if sys.argv[1:2] == ["--break"]:
        break_memory(); sys.exit()

    only = sys.argv[1:] or ["V1", "V1b", "V2", "V3"]
    if "V1" in only:
        print("=== V1 temiz sunucu, normal akis", flush=True)
        subprocess.run(["foundry", "server", "stop"], capture_output=True, timeout=120); time.sleep(3)
        child("--app")
    if "V1b" in only:
        print("\n=== V1b saglam sunucuya ikinci baglanti", flush=True)
        child("--app")
    if "V2" in only:
        print("\n=== V2 bozuk bellek", flush=True)
        subprocess.run(["foundry", "server", "stop"], capture_output=True, timeout=120); time.sleep(3)
        child("--break")
        child("--app")
    if "V3" in only:
        print("\n=== V3 oturum ortasinda sohbet modeli atiliyor", flush=True)
        child("--app", "--unload")
