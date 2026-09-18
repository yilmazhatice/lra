"""Gomme (sorgu vektoru) isteginin suresi, uygulamanin yukleme sirasinda.

Kullanim: python gomme_hizi.py   (sunucu temiz baslatilmis olmali)
"""
import os, sys, time

LRA = r"C:\Workspace\microsoft_ws\lra"
sys.path.insert(0, LRA); os.chdir(LRA)

import search
import rag  # noqa: F401  set_primary: once sohbet modeli yuklenip isitilir

search.embed_query("Kut nedir?")
xs = []
for _ in range(10):
    started = time.perf_counter()
    search.embed_query("Kut nedir?")
    xs.append(time.perf_counter() - started)
print(f"uygulama sirasi (once sohbet + isitma): {sum(xs) / len(xs) * 1000:.1f} ms")
