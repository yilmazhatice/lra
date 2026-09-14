import sys, os
sys.path.insert(0, r"C:\Workspace\microsoft_ws\lra")
os.chdir(r"C:\Workspace\microsoft_ws\lra")
from search import search

pairs = [("fatih kimdir", "böri nedir"), ("böri nedir", "fatih kimdir"),
         ("Osman Gazi kimdir", "Orhan Gazi kimdir"), ("böri nedir", "Osman Gazi kimdir"),
         ("Eski Türkçede kurdun adı neydi?", "Dokuz Işık ilkeleri nelerdir?"),
         ("Dokuz Işık ilkeleri nelerdir?", "Malazgirt savaşı ne zaman oldu?")]
for a, b in pairs:
    for q in (b, a + " " + b):
        hits = search(q)
        print(f"{q!r:60} " + " | ".join(f"{h[2][:22]}#{h[3]} {h[0]:.3f}" for h in hits))
    print()
