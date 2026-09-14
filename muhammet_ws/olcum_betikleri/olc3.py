import sys, os
sys.path.insert(0, r"C:\Workspace\microsoft_ws\lra")
os.chdir(r"C:\Workspace\microsoft_ws\lra")
from rag import retrieve, MIN_SCORE

# app.py / masaustu.py ile ayni birlestirme: tek oturumda ard arda sorular
seq = ["böri nedir", "fatih kimdir", "Osman Gazi kimdir", "Orhan Gazi kimdir",
       "böri nedir", "Malazgirt savaşı ne zaman oldu?"]
prev = None
for q in seq:
    arama = prev + " " + q if prev and len(q.split()) <= 8 else q
    old = retrieve(arama)
    new = retrieve(q, search_query=arama)
    f = lambda h: f"{h[0][2][:22]}#{h[0][3]} {h[0][0]:.3f}{'' if h[0][0] >= MIN_SCORE else ' ESIK ALTI'}"
    print(f"{q!r:36} eski: {f(old):45} yeni: {f(new)}")
    prev = q
