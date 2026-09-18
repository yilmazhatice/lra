"""Yerel Belge Asistani - masaustu arayuzu (Tkinter).

Gorunum app.py'deki web arayuzunun (Borteçine) masaustu karsiligi:
dalgalanan bayrak zemini, koyu icerik paneli, kirmizi vurgular,
sohbet akisi ve acilir kaynak kartlari.
"""

import sys
import threading
import time
import tkinter as tk
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageTk

from rag import (answer, MIN_SCORE, TOP_K, CHAT_KEYWORD,
                 BAGLAM_EN_AZ, BAGLAM_EN_COK)

# ------------------------------------------------------------------ renkler
# app.py'deki CSS renkleri saydamsiz karsiliklariyla (Tk saydamlik bilmez).

ZEMIN = "#1a1114"          # en koyu taban
PANEL = "#1d1417"          # icerik paneli   (rgba(26,17,20,.90))
PANEL_CIZGI = "#5c2028"    # panel kenarligi (rgba(227,10,23,.28))
YAN_PANEL = "#150e10"
BALON = "#241c1f"          # sohbet balonu   (rgba(255,255,255,.045))
BALON_CIZGI = "#42191f"
GIRIS_ZEMIN = "#1e1417"
KIRMIZI = "#c8101f"
KIRMIZI_KOYU = "#8d0b16"
KIRMIZI_SOLUK = "#e8888f"
BASLIK_RENK = "#f3dfe1"
METIN = "#e7dcde"
SOLUK = "#b3a5a8"
COK_SOLUK = "#9c8f92"

# Arayuz macOS'ta yazildi; iki isim orada var, Windows/Linux Tk'sinde yok.
# "pointinghand" bilinmeyen bir imlec adi ve Tk pencereyi kurarken
# TclError("bad cursor spec") firlatiyor, yani uygulama hic acilmiyor.
# "Helvetica Neue" ise sessizce Tk'nin varsayilan yazi tipine dusuyor.
EL_IMLECI = "pointinghand" if sys.platform == "darwin" else "hand2"
YAZI_AILESI = "Helvetica Neue" if sys.platform == "darwin" else "Segoe UI"

BASLIK_FONT = (YAZI_AILESI, 26, "bold")
ROL_FONT = (YAZI_AILESI, 10, "bold")
ALT_FONT = (YAZI_AILESI, 12)
METIN_FONT = (YAZI_AILESI, 13)
KUCUK_FONT = (YAZI_AILESI, 11)
MINI_FONT = (YAZI_AILESI, 10)

KART_EN = 820              # icerik panelinin ust siniri (app.py ile ayni)
YAN_EN = 268

# Kaydirma, Tk'nin "unit" birimi yerine piksel uzerinden yurutuluyor: tuvalin
# yscrollincrement'i 1 piksele cekildigi icin bir birim = bir piksel.
TEKER_ADIM = 13            # tekerlek biriminin piksel karsiligi (macOS: |delta|=1)
TEKER_TIK = 52             # bir tam tik (Windows/Tk9 tarzi delta=120) kac piksel
KAYDIRMA_KARE = 12         # animasyon kare araligi (ms) ~ 80 fps
KAYDIRMA_ORAN = 0.34       # her karede hedefe yaklasma orani
KAYDIRMA_ESIK = 1.0        # bu kadar kalinca son adim atilir ve durulur
SATIR_ADIM = 58            # ok tuslariyla kaydirma

BAYRAK_YOLU = Path(__file__).parent / "varliklar" / "bayrak.jpg"

ORNEKLER = [
    "Eski Türkçede kurdun adı neydi?",
    "Dokuz Işık ilkeleri nelerdir?",
    "Bugün hava nasıl olacak?",
]

gecmis = []            # [{"soru", "cevap"}] — modele tasinan sohbet gecmisi
sarilanlar = []        # genislikle birlikte yeniden sarilacak etiketler
mesgul = False         # bir yanit uretiliyorken yeni soru alinmaz
yanit_ic = None        # uretilmekte olan yanit balonunun cercevesi
yanit_etiket = None    # canli yazilan metin etiketi
son_ciz = 0.0          # son ekran guncellemesinin zamani
kaydirma_hedef = None  # yumusatilmis kaydirmanin hedefledigi ust kenar (px)
kaydirma_isi = None    # calisan animasyon adiminin after kimligi
takip = True           # akis en alttayken yeni icerigi kendiliginden izler


# -------------------------------------------------------------------- zemin

def _ortu(en, boy):
    """app.py'deki linear-gradient(150deg, ...) ortusunu uretir."""
    duraklar = [0.0, 0.46, 1.0]
    renkler = [(0x77, 0x40, 0x4A), (0x5A, 0x2C, 0x34), (0x7D, 0x43, 0x4C)]

    # 150 derece: saat yonunde yukaridan; yon vektoru saga ve asagi bakar.
    x = np.linspace(0.0, 1.0, en)[None, :] * 0.5
    y = np.linspace(0.0, 1.0, boy)[:, None] * 0.866
    t = (x + y) / (0.5 + 0.866)

    kanallar = [
        np.interp(t, duraklar, [r[k] for r in renkler]) for k in range(3)
    ]
    dizi = np.stack(kanallar, axis=-1).astype("uint8")
    return Image.fromarray(dizi, "RGB")


def _bayrak(en, boy):
    """Bayragi pencereyi ortecek sekilde kirpar ve ortuyle karartir.

    CSS'teki `background-size: cover` ile `background-blend-mode: multiply`
    davranisinin Pillow karsiligi.
    """
    ham = Image.open(BAYRAK_YOLU).convert("RGB")
    olcek = max(en / ham.width, boy / ham.height)
    yeni = (max(1, round(ham.width * olcek)), max(1, round(ham.height * olcek)))
    buyuk = ham.resize(yeni, Image.LANCZOS)

    sol = (buyuk.width - en) // 2
    ust = (buyuk.height - boy) // 2
    kirpik = buyuk.crop((sol, ust, sol + en, ust + boy))
    return ImageChops.multiply(kirpik, _ortu(en, boy))


def zemini_ciz(en, boy):
    """Zemin tuvaline yeni boyuttaki bayragi basar."""
    global zemin_foto
    if en < 2 or boy < 2:
        return
    zemin_foto = ImageTk.PhotoImage(_bayrak(en, boy))
    zemin.delete("bayrak")
    zemin.create_image(0, 0, image=zemin_foto, anchor="nw", tags="bayrak")


# ------------------------------------------------------- cerceve ve dugmeler
# macOS'ta Tk'nin kendi kenarliklari (highlightbackground) ve kaydirma cubugu
# aqua renginde ciziliyor; koyu temayi bozmamak icin ikisi de elle kuruluyor.

def cerceveli(ana, ic_renk, cizgi_renk, **kwargs):
    """1 piksel kenarlikli bir kutu kurar; (dis, ic) cerceveyi verir."""
    dis = tk.Frame(ana, bg=cizgi_renk)
    ic = tk.Frame(dis, bg=ic_renk, **kwargs)
    ic.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
    return dis, ic


def dugme(ana, metin, islev, birincil=False, font=KUCUK_FONT, dolgu=(14, 7)):
    """Kirmizi cerceveli, uzerine gelince dolan dugme."""
    durgun_zemin = KIRMIZI if birincil else BALON
    durgun_yazi = "#ffffff" if birincil else "#eec2c6"

    cerceve = tk.Frame(ana, bg=KIRMIZI if birincil else KIRMIZI_KOYU)
    et = tk.Label(
        cerceve, text=metin, font=font, bg=durgun_zemin, fg=durgun_yazi,
        padx=dolgu[0], pady=dolgu[1], cursor=EL_IMLECI,
        disabledforeground="#c9a7ab",
    )
    et.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

    def gir(_e):
        if str(et.cget("state")) != tk.DISABLED:
            et.config(bg=KIRMIZI, fg="#ffffff")
            cerceve.config(bg=KIRMIZI)

    def cik(_e):
        et.config(bg=durgun_zemin, fg=durgun_yazi)
        cerceve.config(bg=KIRMIZI if birincil else KIRMIZI_KOYU)

    def tik(_e):
        if str(et.cget("state")) != tk.DISABLED:
            islev()

    et.bind("<Enter>", gir)
    et.bind("<Leave>", cik)
    et.bind("<Button-1>", tik)

    cerceve.et = et
    return cerceve


class Kaydirici(tk.Canvas):
    """Koyu temaya uygun ince kaydirma cubugu."""

    def __init__(self, ana, tuval):
        super().__init__(ana, width=8, height=1, bg=PANEL,
                         highlightthickness=0)
        self.tuval = tuval
        self.bas, self.son = 0.0, 1.0
        self.tutma = None
        self.bind("<Configure>", lambda _e: self.ciz())
        self.bind("<Button-1>", self.bastir)
        self.bind("<B1-Motion>", self.surukle)
        self.bind("<ButtonRelease-1>", lambda _e: setattr(self, "tutma", None))

    def ayarla(self, bas, son):
        """Tuvalin yscrollcommand'i buraya baglanir."""
        self.bas, self.son = float(bas), float(son)
        self.ciz()

    def ciz(self):
        self.delete("all")
        boy = self.winfo_height()
        if boy < 2 or self.son - self.bas >= 0.999:
            return          # her sey ekrana sigiyorsa cubuk gosterilmez
        ust = round(self.bas * boy)
        alt = max(ust + 24, round(self.son * boy))
        self.create_rectangle(2, ust, 6, alt, fill="#6d2830", width=0)

    def bastir(self, olay):
        kaydirmayi_durdur()          # elle surukleme yumusatmayi devralir
        boy = max(1, self.winfo_height())
        yeni = olay.y / boy - (self.son - self.bas) / 2
        self.tuval.yview_moveto(max(0.0, min(1.0, yeni)))
        self.tutma = olay.y
        takibi_tazele()

    def surukle(self, olay):
        if self.tutma is None:
            return
        boy = max(1, self.winfo_height())
        self.tuval.yview_moveto(
            max(0.0, min(1.0, self.bas + (olay.y - self.tutma) / boy))
        )
        self.tutma = olay.y
        takibi_tazele()


# -------------------------------------------------------------- sohbet akisi

def sarmali(etiket):
    """Etiketi, panel genisligine gore yeniden sarilacaklar listesine alir."""
    sarilanlar.append(etiket)
    etiket.config(wraplength=max(240, sohbet_tuval.winfo_width() - 56))
    return etiket


def balon(rol):
    """Sohbet akisina bos bir mesaj balonu ekler ve icerik cercevesini verir."""
    dis = tk.Frame(sohbet_ic, bg=PANEL)
    dis.pack(fill=tk.X, pady=(0, 12))

    cerceve, ic = cerceveli(dis, BALON, BALON_CIZGI, padx=16, pady=12)
    cerceve.pack(fill=tk.X)

    tk.Label(
        ic, text=rol, font=ROL_FONT, bg=BALON, fg=KIRMIZI_SOLUK, anchor="w",
    ).pack(fill=tk.X, pady=(0, 6))
    return dis, ic


def soruyu_ciz(soru):
    _dis, ic = balon("SİZ")
    sarmali(tk.Label(
        ic, text=soru, font=METIN_FONT, bg=BALON, fg=METIN,
        anchor="w", justify="left",
    )).pack(fill=tk.X)
    asagi_kaydir(zorla=True)


def olcumleri_ciz(ana, sure, en_iyi, sayi):
    """Yanit altindaki olcum satiri: etiketler soluk, degerler kirmizi."""
    satir = tk.Frame(ana, bg=BALON)
    satir.pack(fill=tk.X, pady=(10, 0))

    parcalar = [
        ("Yanıt süresi", f"{sure:.1f} sn"),
        ("En yüksek eşleşme", f"{en_iyi:.3f}"),
        ("Taranan bölüm", str(sayi)),
    ]
    for sira, (etiket, deger) in enumerate(parcalar):
        if sira:
            tk.Label(satir, text="·", font=MINI_FONT, bg=BALON,
                     fg="#6d5f62", padx=8).pack(side=tk.LEFT)
        tk.Label(satir, text=etiket, font=MINI_FONT, bg=BALON,
                 fg=COK_SOLUK).pack(side=tk.LEFT)
        tk.Label(satir, text=deger, font=(YAZI_AILESI, 10, "bold"),
                 bg=BALON, fg=KIRMIZI_SOLUK, padx=4).pack(side=tk.LEFT)


def kaynaklari_ciz(ana, hits):
    """Web arayuzundeki acilir kaynak listesinin karsiligi."""
    baslik_metni = f"Yanıtın dayandığı bölümler ({len(hits)})"

    baslik = tk.Label(
        ana, text="▸  " + baslik_metni, font=KUCUK_FONT, bg=BALON,
        fg=KIRMIZI_SOLUK, anchor="w", cursor=EL_IMLECI, pady=6,
    )
    baslik.pack(fill=tk.X, pady=(12, 0))

    govde = tk.Frame(ana, bg=BALON)

    for skor, _cid, dosya, sira, parca in hits:
        kart = tk.Frame(govde, bg=BALON)
        kart.pack(fill=tk.X, pady=(0, 12))

        # karta soldan kirmizi serit (CSS'teki border-left)
        tk.Frame(kart, bg=KIRMIZI, width=3).pack(side=tk.LEFT, fill=tk.Y)

        yazi = tk.Frame(kart, bg=BALON, padx=10)
        yazi.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ust = tk.Frame(yazi, bg=BALON)
        ust.pack(fill=tk.X)
        tk.Label(ust, text=dosya, font=(YAZI_AILESI, 11, "bold"),
                 bg=BALON, fg="#e7dcde").pack(side=tk.LEFT)
        tk.Label(ust, text=f"· bölüm {sira} · eşleşme {skor:.3f}",
                 font=MINI_FONT, bg=BALON, fg=COK_SOLUK,
                 padx=6).pack(side=tk.LEFT)

        onizleme = parca[:420] + ("…" if len(parca) > 420 else "")
        sarmali(tk.Label(
            yazi, text=onizleme.replace("\n", " "), font=KUCUK_FONT,
            bg=BALON, fg=SOLUK, anchor="w", justify="left",
        )).pack(fill=tk.X, pady=(3, 0))

    def gecis(_e):
        if govde.winfo_ismapped():
            govde.pack_forget()
            baslik.config(text="▸  " + baslik_metni)
        else:
            govde.pack(fill=tk.X, pady=(8, 0))
            baslik.config(text="▾  " + baslik_metni)
        asagi_kaydir()

    baslik.bind("<Button-1>", gecis)


def yaniti_tamamla(ic, etiket, metin, hits, sure):
    """Canli yazilan balonu son metin, olcumler ve kaynaklarla kapatir."""
    etiket.config(text=metin, fg=METIN)
    olcumleri_ciz(ic, sure, hits[0][0] if hits else 0.0, len(hits))
    if hits:
        kaynaklari_ciz(ic, hits)
    asagi_kaydir()


# -------------------------------------------------------- yumusak kaydirma
# Tuval piksel adimiyla kaydirildigi icin tekerlek olaylari dogrudan
# uygulanmak yerine bir hedefe yaziliyor; her karede hedefe bir miktar
# yaklasilarak hareket suruklenmeden akitiliyor.

def kaydirma_araligi():
    """Gorunen ust kenarin alabilecegi (en kucuk, en buyuk) piksel degeri."""
    bolge = sohbet_tuval.tk.splitlist(sohbet_tuval.cget("scrollregion"))
    if len(bolge) != 4:
        return 0.0, 0.0
    ust, alt = float(bolge[1]), float(bolge[3])
    return ust, max(ust, alt - sohbet_tuval.winfo_height())


def _uste_koy(y):
    """Gorunen ust kenari verilen piksele tasir."""
    bolge = sohbet_tuval.tk.splitlist(sohbet_tuval.cget("scrollregion"))
    if len(bolge) != 4:
        return
    ust, alt = float(bolge[1]), float(bolge[3])
    sohbet_tuval.yview_moveto((y - ust) / max(1.0, alt - ust))


def kaydirmayi_durdur():
    """Suren animasyonu iptal eder (elle surukleme ya da sifirlama icin)."""
    global kaydirma_hedef, kaydirma_isi
    if kaydirma_isi is not None:
        pencere.after_cancel(kaydirma_isi)
    kaydirma_isi = None
    kaydirma_hedef = None


def takibi_tazele():
    """Kullanici en alttaysa akis yeni icerigi izlemeye devam eder."""
    global takip
    _ust, en_alt = kaydirma_araligi()
    takip = sohbet_tuval.canvasy(0) >= en_alt - 6


def kaydir(piksel):
    """Akisi verilen kadar kaydirmayi hedefler; hareketi yumusatarak isler."""
    global kaydirma_hedef, takip
    en_ust, en_alt = kaydirma_araligi()
    if en_alt <= en_ust:
        return                      # her sey ekrana sigiyor
    simdi = kaydirma_hedef if kaydirma_hedef is not None \
        else sohbet_tuval.canvasy(0)
    kaydirma_hedef = min(en_alt, max(en_ust, simdi + piksel))
    takip = kaydirma_hedef >= en_alt - 6
    _animasyonu_surdur()


def _animasyonu_surdur():
    global kaydirma_isi
    if kaydirma_isi is None:
        kaydirma_isi = pencere.after(KAYDIRMA_KARE, _kaydirma_adimi)


def _kaydirma_adimi():
    """Bir kare: hedefle aradaki farkin bir bolumu kadar ilerler."""
    global kaydirma_isi, kaydirma_hedef
    kaydirma_isi = None
    if kaydirma_hedef is None:
        return

    en_ust, en_alt = kaydirma_araligi()
    hedef = min(en_alt, max(en_ust, kaydirma_hedef))   # icerik degismis olabilir
    kaydirma_hedef = hedef
    fark = hedef - sohbet_tuval.canvasy(0)

    if abs(fark) <= KAYDIRMA_ESIK:
        _uste_koy(hedef)
        kaydirma_hedef = None
        return

    _uste_koy(sohbet_tuval.canvasy(0) + fark * KAYDIRMA_ORAN)
    kaydirma_isi = pencere.after(KAYDIRMA_KARE, _kaydirma_adimi)


def en_alta(ani=False):
    """Akisi en alta getirir; `ani` ise beklemeden, degilse kayarak."""
    global kaydirma_hedef, takip
    takip = True
    _ust, en_alt = kaydirma_araligi()
    if ani:
        kaydirmayi_durdur()
        _uste_koy(en_alt)
        return
    kaydirma_hedef = en_alt
    _animasyonu_surdur()


def asagi_kaydir(zorla=False):
    """Paneli yeni icerige gore uzatir; kullanici en alttaysa akisi izler.

    Yukari kaydirilmissa yerinde birakilir — yanit yazilirken okunan yer
    artik elden kacmiyor. `zorla` yalnizca yeni soru/temizleme gibi
    kullanicinin kendi baslattigi anlarda kullaniliyor.
    """
    sohbet_tuval.update_idletasks()
    yerlestir()
    sohbet_tuval.configure(scrollregion=sohbet_tuval.bbox("all"))
    if zorla:
        en_alta(ani=True)
    elif takip:
        en_alta()


# ------------------------------------------------------------------- akis

def sor(soru=None):
    """Girisdeki soruyu al ve arka planda isle."""
    global mesgul, yanit_ic, yanit_etiket, son_ciz
    if mesgul:
        return

    soru = (soru or giris.get()).strip()
    if not soru:
        return

    if ornek_cerceve.winfo_ismapped():
        ornek_cerceve.pack_forget()

    giris.delete(0, tk.END)
    soruyu_ciz(soru)

    mesgul = True
    gonder.et.config(state=tk.DISABLED, bg="#7c2029", fg="#c9a7ab")
    giris.config(state=tk.DISABLED)

    _dis, yanit_ic = balon("BÖRTEÇİNE")
    yanit_etiket = sarmali(tk.Label(
        yanit_ic, text="Belgeler taranıyor ve yanıt hazırlanıyor…",
        font=METIN_FONT, bg=BALON, fg=COK_SOLUK, anchor="w", justify="left",
    ))
    yanit_etiket.pack(fill=tk.X)
    son_ciz = 0.0
    asagi_kaydir(zorla=True)

    # Sohbet gecmisi rag.answer'a veriliyor: takip sorularinin aranmasinda ve
    # modele baglam olarak kullaniliyor.
    threading.Thread(target=isle, args=(soru, list(gecmis)), daemon=True).start()


def isle(soru, oncekiler):
    """Arka plan is parcacigi: modeli cagirir, sonucu ana dongude gosterir."""
    try:
        metin, hits, sure = answer(soru, history=oncekiler, stream_cb=akit)
    except Exception as hata:  # baglanti kopmasi vb.
        metin, hits, sure = f"Hata: {hata}", [], 0.0
    pencere.after(0, bitti, soru, metin, hits, sure)


def akit(simdiye_kadar):
    """Model uretirken cagrilir (arka plan is parcacigindan).

    Tk yalnizca ana dongude guvenli oldugu icin guncelleme after ile
    siraya aliniyor; her token yerine saniyede ~8 kez ciziliyor.
    """
    global son_ciz
    simdi = time.monotonic()
    if simdi - son_ciz < 0.12:
        return
    son_ciz = simdi
    pencere.after(0, yaziyi_guncelle, simdiye_kadar)


def yaziyi_guncelle(metin):
    if yanit_etiket is not None and yanit_etiket.winfo_exists():
        yanit_etiket.config(text=metin, fg=METIN)
        asagi_kaydir()


def bitti(soru, metin, hits, sure):
    """Sonucu ekrana bas ve arayuzu tekrar kullanilabilir yap."""
    global mesgul
    yaniti_tamamla(yanit_ic, yanit_etiket, metin, hits, sure)

    gecmis.append({"soru": soru, "cevap": metin})
    mesgul = False
    giris.config(state=tk.NORMAL)
    gonder.et.config(state=tk.NORMAL, bg=KIRMIZI, fg="#ffffff")
    giris.focus_set()


def temizle():
    """Konusmayi ve akistaki tum balonlari sifirlar."""
    if mesgul:
        return
    gecmis.clear()
    sarilanlar.clear()
    for cocuk in sohbet_ic.winfo_children():
        if cocuk is not ornek_cerceve:
            cocuk.destroy()
    ornek_cerceve.pack(fill=tk.X, pady=(0, 12))
    giris.delete(0, tk.END)
    giris.focus_set()
    asagi_kaydir(zorla=True)


# ----------------------------------------------------------------- pencere

pencere = tk.Tk()
pencere.title("Börteçine")
pencere.geometry("1120x820")
pencere.minsize(900, 660)
pencere.configure(bg=ZEMIN)

zemin = tk.Canvas(pencere, bg=ZEMIN, highlightthickness=0)
zemin.place(x=0, y=0, relwidth=1, relheight=1)
zemin_foto = None

# ---------------------------------------------------------------- yan panel

yan = tk.Frame(pencere, bg=YAN_PANEL)
yan.place(x=0, y=0, relheight=1, width=YAN_EN)

# sag kenardaki kirmizi cizgi (CSS'teki border-right)
tk.Frame(yan, bg="#8e0b16", width=2).pack(side=tk.RIGHT, fill=tk.Y)

yan_ic = tk.Frame(yan, bg=YAN_PANEL, padx=22, pady=26)
yan_ic.pack(fill=tk.BOTH, expand=True)

tk.Label(
    yan_ic, text="Sistem yapılandırması", font=(YAZI_AILESI, 14, "bold"),
    bg=YAN_PANEL, fg=BASLIK_RENK, anchor="w",
).pack(fill=tk.X, pady=(0, 12))

for _etiket, _deger in [
    ("Dil modeli", CHAT_KEYWORD),
    ("Aday bölüm sayısı", str(TOP_K)),
    ("Yanıta giren bölüm", f"{BAGLAM_EN_AZ}–{BAGLAM_EN_COK}"),
    ("Eşleşme alt sınırı", f"{MIN_SCORE:.2f}"),
    ("Çalışma yeri", "Bu bilgisayar"),
]:
    _satir = tk.Frame(yan_ic, bg=YAN_PANEL)
    _satir.pack(fill=tk.X)
    tk.Label(_satir, text=_etiket, font=KUCUK_FONT, bg=YAN_PANEL,
             fg="#c9bbbe", anchor="w").pack(side=tk.LEFT, pady=6)
    tk.Label(_satir, text=_deger, font=(YAZI_AILESI, 11, "bold"),
             bg=YAN_PANEL, fg=KIRMIZI_SOLUK, anchor="e").pack(side=tk.RIGHT,
                                                              pady=6)
    tk.Frame(yan_ic, bg="#33161b", height=1).pack(fill=tk.X)

tk.Label(
    yan_ic,
    text="Bir soru, belgelerle yeterince eşleşmezse dil modeline hiç "
         "gönderilmez. Sistem bu durumda tahmin yürütmek yerine bilgisi "
         "olmadığını söyler.",
    font=MINI_FONT, bg=YAN_PANEL, fg=COK_SOLUK, anchor="w", justify="left",
    wraplength=YAN_EN - 52,
).pack(fill=tk.X, pady=(16, 18))

dugme(yan_ic, "Konuşmayı temizle", temizle).pack(fill=tk.X)

# ------------------------------------------------------------ icerik paneli

kart, kart_ic = cerceveli(pencere, PANEL, PANEL_CIZGI, padx=30, pady=28)

tk.Label(
    kart_ic, text="Börteçine", font=BASLIK_FONT, bg=PANEL, fg=BASLIK_RENK,
    anchor="w",
).pack(fill=tk.X)

# baslik altindaki bayrak seridi: kirmiziden panele soluklasan cizgi
serit = tk.Canvas(kart_ic, height=4, bg=PANEL, highlightthickness=0)
serit.pack(fill=tk.X, pady=(6, 14))

tk.Label(
    kart_ic,
    text="Yüklediğiniz belgeler hakkında soru sorun. Asistan yanıtını "
         "yalnızca bu belgelerden üretir ve hangi belgeden yararlandığını "
         "her yanıtın sonunda belirtir. İnternet bağlantısı kullanılmaz; "
         "tüm işlem bu bilgisayarda gerçekleşir.",
    font=ALT_FONT, bg=PANEL, fg=SOLUK, anchor="w", justify="left",
    wraplength=KART_EN - 80,
).pack(fill=tk.X, pady=(0, 18))

# --------------------------------------------------------------- soru satiri

satir = tk.Frame(kart_ic, bg=PANEL)
satir.pack(side=tk.BOTTOM, fill=tk.X, pady=(18, 0))

giris = tk.Entry(
    satir, font=METIN_FONT, bg=GIRIS_ZEMIN, fg=METIN, relief=tk.FLAT,
    highlightthickness=1, highlightbackground="#6f1f28", highlightcolor=KIRMIZI,
    insertbackground=KIRMIZI_SOLUK, disabledbackground=GIRIS_ZEMIN,
    disabledforeground=COK_SOLUK,
)
giris.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=9, padx=(0, 10))
giris.bind("<Return>", lambda _e: sor())

gonder = dugme(satir, "Sor", sor, birincil=True,
               font=(YAZI_AILESI, 12, "bold"), dolgu=(22, 8))
gonder.pack(side=tk.LEFT)

# --------------------------------------------------------------- sohbet akisi

# Akis, tum paneli kaplamak yerine icerigi kadar yer tutar; yeni sorularla
# birlikte asagi dogru uzar, pencereye sigmayinca kaydirmaya gecer.
akis = tk.Frame(kart_ic, bg=PANEL)
akis.pack(fill=tk.X)

# yscrollincrement=1: kaydirma birimi gorunen alanin %10'u degil, 1 piksel
sohbet_tuval = tk.Canvas(akis, bg=PANEL, height=1, highlightthickness=0,
                         yscrollincrement=1)
sohbet_tuval.pack(side=tk.LEFT, fill=tk.X, expand=True)

kaydirici = Kaydirici(akis, sohbet_tuval)
kaydirici.pack(side=tk.RIGHT, fill=tk.Y, padx=(6, 0))
sohbet_tuval.configure(yscrollcommand=kaydirici.ayarla)

sohbet_ic = tk.Frame(sohbet_tuval, bg=PANEL)
akis_id = sohbet_tuval.create_window((0, 0), window=sohbet_ic, anchor="nw")

# ------------------------------------------------------------ ornek sorular

ornek_cerceve = tk.Frame(sohbet_ic, bg=PANEL)
ornek_cerceve.pack(fill=tk.X, pady=(0, 12))

tk.Label(
    ornek_cerceve, text="Başlamak için bir örnek seçin",
    font=(YAZI_AILESI, 12, "bold"), bg=PANEL, fg=METIN, anchor="w",
).pack(fill=tk.X, pady=(0, 10))

ornek_satir = tk.Frame(ornek_cerceve, bg=PANEL)
ornek_satir.pack(fill=tk.X)
for _sira, _ornek in enumerate(ORNEKLER):
    dugme(ornek_satir, _ornek, lambda s=_ornek: sor(s)).pack(
        side=tk.LEFT, fill=tk.X, expand=True,
        padx=(0 if _sira == 0 else 8, 0),
    )


# --------------------------------------------------------------- yerlesim

def serit_ciz(_e=None):
    """Seridi ciz: %62'ye kadar tam kirmizi, sonra panele soluklasiyor.

    Yerlesim her tazelendiginde degil, yalnizca genislik degisince ve
    piksel piksel degil 48 basamakta ciziliyor; yanit akarken yuzlerce
    tuval ogesinin bosuna yeniden kurulmasi boylece kalkiyor.
    """
    global serit_son_en
    en = serit.winfo_width()
    if en < 2 or en == serit_son_en:
        return
    serit_son_en = en
    serit.delete("all")
    kirilma = int(en * 0.62)
    serit.create_rectangle(0, 0, kirilma, 4, fill=KIRMIZI, width=0)

    basamak = 48
    for adim in range(basamak):
        sol = kirilma + round((en - kirilma) * adim / basamak)
        sag = kirilma + round((en - kirilma) * (adim + 1) / basamak)
        oran = adim / (basamak - 1)
        renk = "#%02x%02x%02x" % tuple(
            round(a + (b - a) * oran) for a, b in
            zip((0xC8, 0x10, 0x1F), (0x1D, 0x14, 0x17))
        )
        serit.create_rectangle(sol, 0, sag + 1, 4, fill=renk, width=0)


def akisi_boyutlandir(pencere_boyu):
    """Akisi icerigi kadar yap; panelin olmasi gereken yuksekligini dondurur.

    Icerik pencereye sigmadiginda akis o sinirda kalir ve kaydirilir.
    """
    icerik = sohbet_ic.winfo_reqheight()
    # akis disindaki her sey: baslik, serit, tanitim, soru satiri, dolgular
    sabit = kart_ic.winfo_reqheight() - sohbet_tuval.winfo_reqheight()
    azami = max(120, pencere_boyu - 44 - 2 - sabit)

    yeni = max(40, min(icerik, azami))
    if yeni != int(sohbet_tuval.cget("height")):
        sohbet_tuval.config(height=yeni)
    return sabit + yeni + 2


def yerlestir(olay=None):
    """Paneli ortala, zemini ve sarilan metinleri yeni boyuta uydur."""
    global son_boyut
    if olay is not None and olay.widget is not pencere:
        return

    global son_kart
    en, boy = pencere.winfo_width(), pencere.winfo_height()
    bos = en - YAN_EN
    kart_en = max(420, min(KART_EN, bos - 72))
    kart_boy = min(boy - 44, akisi_boyutlandir(boy))
    yeni_kart = (YAN_EN + (bos - kart_en) // 2, 22, kart_en, kart_boy)
    if yeni_kart != son_kart:          # yanit akarken bos yerlesim yapilmasin
        son_kart = yeni_kart
        kart.place(x=yeni_kart[0], y=yeni_kart[1],
                   width=yeni_kart[2], height=yeni_kart[3])

    if (en, boy) != son_boyut:
        son_boyut = (en, boy)
        zemini_ciz(en, boy)
    serit_ciz()


def akis_genisligi(olay):
    """Akis icerigini tuval genisligine yay ve metinleri yeniden sar."""
    global son_akis_en
    sohbet_tuval.itemconfigure(akis_id, width=olay.width)
    if olay.width != son_akis_en:
        son_akis_en = olay.width
        # silinmis balonlarin (ornegin bekleme balonu) etiketleri listede kalir
        kaydirmayi_durdur()   # eski hedef yeni sarmada anlamini yitirir
        sarilanlar[:] = [e for e in sarilanlar if e.winfo_exists()]
        for etiket in sarilanlar:
            etiket.config(wraplength=max(240, olay.width - 56))
        yerlesim_iste()       # sarma degisti, icerik yuksekligi yeniden olculur
    sohbet_tuval.configure(scrollregion=sohbet_tuval.bbox("all"))


def yerlesim_iste():
    """Yerlesimi bir sonraki bos anda, en fazla bir kez tazeler."""
    global bekleyen_yerlesim
    if not bekleyen_yerlesim:
        bekleyen_yerlesim = True
        pencere.after_idle(_yerlesimi_calistir)


def _yerlesimi_calistir():
    global bekleyen_yerlesim
    bekleyen_yerlesim = False
    yerlestir()


def tekerlek(olay):
    """Tekerlek/izleme yuzeyi: delta'yi piksele cevirip hedefe ekler.

    macOS'ta Tk her kucuk hareket icin delta=+-1 uretir (izleme yuzeyinde
    saniyede onlarca olay); Windows ve Tk 9'da bir tik 120'nin katidir.
    Ikisi de ayni piksel olcegine indiriliyor.
    """
    delta = olay.delta
    if not delta:
        return
    if abs(delta) >= 120:
        kaydir(-delta / 120.0 * TEKER_TIK)
    else:
        kaydir(-delta * TEKER_ADIM)


def tus_kaydir(olay):
    """Ok tuslari ve Page Up/Down ile kaydirma (giris tek satirlik oldugu
    icin bu tuslar orada zaten bir ise yaramiyor)."""
    sayfa = max(80, sohbet_tuval.winfo_height() - 48)
    adim = {"Up": -SATIR_ADIM, "Down": SATIR_ADIM,
            "Prior": -sayfa, "Next": sayfa}.get(olay.keysym)
    if adim is None:
        return None
    kaydir(adim)
    return "break"


son_boyut = (0, 0)
son_akis_en = 0
son_kart = None
serit_son_en = 0
bekleyen_yerlesim = False

pencere.bind("<Configure>", yerlestir)
sohbet_tuval.bind("<Configure>", akis_genisligi)
def akis_icerigi(_olay):
    sohbet_tuval.configure(scrollregion=sohbet_tuval.bbox("all"))
    yerlesim_iste()


sohbet_ic.bind("<Configure>", akis_icerigi)
sohbet_tuval.bind_all("<MouseWheel>", tekerlek)
for _tus in ("<Up>", "<Down>", "<Prior>", "<Next>"):
    pencere.bind(_tus, tus_kaydir)

pencere.update_idletasks()
yerlestir()
giris.focus_set()
pencere.mainloop()
