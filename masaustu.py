"""Yerel Belge Asistani - masaustu arayuzu (Tkinter)."""

import threading
import tkinter as tk
from tkinter import ttk

from rag import answer, MIN_SCORE, TOP_K, CHAT_KEYWORD

BG = "#f4f6f7"
CARD = "#ffffff"
INK = "#14191e"
MUTED = "#5b6d76"
ACCENT = "#0d6f68"
LINE = "#d5dcdf"

BASLIK_FONT = ("Helvetica Neue", 22, "bold")
ALT_FONT = ("Helvetica Neue", 12)
METIN_FONT = ("Helvetica Neue", 14)
KUCUK_FONT = ("Helvetica Neue", 11)

gecmis = []


def sor():
    """Giris kutusundaki soruyu al ve arka planda isle."""
    soru = giris.get().strip()
    if not soru or not buton["state"] == tk.NORMAL:
        return

    # Kisa takip sorulari ("bunun sebebi ne?") tek baslarina aranamaz;
    # arama icin bir onceki soruyu da ekliyoruz.
    arama = soru
    if gecmis and len(soru.split()) <= 8:
        arama = gecmis[-1] + " " + soru

    buton.config(state=tk.DISABLED)
    giris.config(state=tk.DISABLED)
    yaz(cevap_kutusu, "Belgeler taranıyor ve yanıt hazırlanıyor…")
    durum.config(text="")
    yaz(kaynak_kutusu, "")

    threading.Thread(
        target=isle, args=(soru, arama), daemon=True
    ).start()


def isle(soru, arama):
    """Arka plan is parcacigi: modeli cagirir, sonucu ana dongude gosterir."""
    try:
        metin, hits, sure = answer(soru, search_query=arama)
    except Exception as hata:  # baglanti kopmasi vb.
        metin, hits, sure = f"Hata: {hata}", [], 0.0
    pencere.after(0, bitti, soru, metin, hits, sure)


def bitti(soru, metin, hits, sure):
    """Sonucu ekrana bas ve arayuzu tekrar kullanilabilir yap."""
    yaz(cevap_kutusu, metin)

    en_iyi = hits[0][0] if hits else 0.0
    durum.config(
        text=f"Yanıt süresi {sure:.1f} sn     "
             f"En yüksek eşleşme {en_iyi:.3f}     "
             f"Taranan bölüm {len(hits)}"
    )

    kaynak_kutusu.config(state=tk.NORMAL)
    kaynak_kutusu.delete("1.0", tk.END)
    if hits:
        for skor, _cid, dosya, sira, parca in hits:
            kaynak_kutusu.insert(
                tk.END, f"{dosya}  ·  bölüm {sira}  ·  eşleşme {skor:.3f}\n", "bas"
            )
            onizleme = parca[:400] + ("…" if len(parca) > 400 else "")
            kaynak_kutusu.insert(tk.END, onizleme.replace("\n", " ") + "\n\n", "govde")
    else:
        kaynak_kutusu.insert(tk.END, "Getirilen bölüm yok.\n", "govde")
    kaynak_kutusu.config(state=tk.DISABLED)

    gecmis.append(soru)
    giris.config(state=tk.NORMAL)
    buton.config(state=tk.NORMAL)
    giris.delete(0, tk.END)
    giris.focus_set()


def temizle():
    gecmis.clear()
    yaz(cevap_kutusu, "")
    yaz(kaynak_kutusu, "")
    durum.config(text="")
    giris.delete(0, tk.END)
    giris.focus_set()


def yaz(kutu, metin):
    """Salt okunur bir Text bilesenine icerik yaz."""
    kutu.config(state=tk.NORMAL)
    kutu.delete("1.0", tk.END)
    if metin:
        kutu.insert(tk.END, metin)
    kutu.config(state=tk.DISABLED)


# ----------------------------------------------------------------- pencere

pencere = tk.Tk()
pencere.title("Belge Asistanı")
pencere.geometry("880x760")
pencere.configure(bg=BG)
pencere.minsize(700, 600)

dis = tk.Frame(pencere, bg=BG, padx=28, pady=24)
dis.pack(fill=tk.BOTH, expand=True)

tk.Label(
    dis, text="Belge Asistanı", font=BASLIK_FONT, bg=BG, fg=INK, anchor="w"
).pack(fill=tk.X)

tk.Label(
    dis,
    text="Belgeleriniz hakkında soru sorun. Yanıtlar yalnızca bu belgelerden "
         "üretilir ve kaynak gösterilir.\nTüm işlem bu bilgisayarda çalışır; "
         "internet bağlantısı kullanılmaz.",
    font=ALT_FONT, bg=BG, fg=MUTED, anchor="w", justify="left",
).pack(fill=tk.X, pady=(4, 14))

tk.Label(
    dis,
    text=f"Dil modeli: {CHAT_KEYWORD}     "
         f"Getirilen bölüm: {TOP_K}     "
         f"Eşleşme alt sınırı: {MIN_SCORE:.2f}",
    font=KUCUK_FONT, bg=BG, fg=MUTED, anchor="w",
).pack(fill=tk.X, pady=(0, 16))

# --------------------------------------------------------------- soru satiri

satir = tk.Frame(dis, bg=BG)
satir.pack(fill=tk.X)

giris = tk.Entry(
    satir, font=METIN_FONT, bg=CARD, fg=INK, relief=tk.FLAT,
    highlightthickness=1, highlightbackground=LINE, highlightcolor=ACCENT,
    insertbackground=INK,
)
giris.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
giris.bind("<Return>", lambda _e: sor())

buton = tk.Button(
    satir, text="Sor", command=sor, font=("Helvetica Neue", 13, "bold"),
    bg=ACCENT, fg="white", relief=tk.FLAT, padx=22, pady=6,
    activebackground="#0a5a55", activeforeground="white",
    highlightbackground=BG,
)
buton.pack(side=tk.LEFT)

tk.Button(
    satir, text="Temizle", command=temizle, font=KUCUK_FONT,
    bg=BG, fg=MUTED, relief=tk.FLAT, padx=12, highlightbackground=BG,
).pack(side=tk.LEFT, padx=(8, 0))

# ------------------------------------------------------------------- cevap

tk.Label(
    dis, text="YANIT", font=("Helvetica Neue", 10, "bold"),
    bg=BG, fg=MUTED, anchor="w",
).pack(fill=tk.X, pady=(20, 6))

cevap_kutusu = tk.Text(
    dis, height=7, wrap=tk.WORD, font=METIN_FONT, bg=CARD, fg=INK,
    relief=tk.FLAT, padx=16, pady=14, highlightthickness=1,
    highlightbackground=LINE, state=tk.DISABLED,
)
cevap_kutusu.pack(fill=tk.X)

durum = tk.Label(dis, text="", font=KUCUK_FONT, bg=BG, fg=MUTED, anchor="w")
durum.pack(fill=tk.X, pady=(8, 0))

# ----------------------------------------------------------------- kaynaklar

tk.Label(
    dis, text="YANITIN DAYANDIĞI BÖLÜMLER", font=("Helvetica Neue", 10, "bold"),
    bg=BG, fg=MUTED, anchor="w",
).pack(fill=tk.X, pady=(20, 6))

kaynak_cerceve = tk.Frame(dis, bg=CARD, highlightthickness=1,
                          highlightbackground=LINE)
kaynak_cerceve.pack(fill=tk.BOTH, expand=True)

kaydirma = ttk.Scrollbar(kaynak_cerceve)
kaydirma.pack(side=tk.RIGHT, fill=tk.Y)

kaynak_kutusu = tk.Text(
    kaynak_cerceve, wrap=tk.WORD, font=KUCUK_FONT, bg=CARD, fg=MUTED,
    relief=tk.FLAT, padx=16, pady=14, state=tk.DISABLED,
    yscrollcommand=kaydirma.set,
)
kaynak_kutusu.pack(fill=tk.BOTH, expand=True)
kaydirma.config(command=kaynak_kutusu.yview)

kaynak_kutusu.tag_configure(
    "bas", foreground=ACCENT, font=("Helvetica Neue", 11, "bold"),
    spacing1=6, spacing3=4,
)
kaynak_kutusu.tag_configure("govde", foreground=MUTED, spacing3=8, lmargin1=2)

giris.focus_set()
pencere.mainloop()