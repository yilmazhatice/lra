"""Arayuzun arka planindaki dalgalanan bayragi uretir.

Kumas, ust uste binen kivrim dalgalarindan olusan bir derinlik alani
olarak modellenir; renk bu alanin egiminden hesaplanan isikla verilir.
Ciktiyi yenilemek icin:  python varliklar/bayrak_uret.py

Bagimliliklar (requirements.txt icinde zaten var): numpy, pillow.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

W, H = 1600, 1067
SS = 2

# Kadraj: bayragin (30x20 birim) hangi bolumunun goruldugu.
# u gonderden ucus yonune, v ustten alta 0..1 arasinda ilerler.
UMIN, USPAN = 0.055, 0.84
VMIN, VSPAN = 0.08, 0.84            # oran korunsun diye VSPAN = USPAN

DERINLIK = 95.0                     # kivrimlarin isik hesabindaki derinligi
DUSEY = 34.0                        # kumasin dusey kaymasi (piksel)
YATAY = 12.0                        # kivrim araliklarindaki sikisma (piksel)
GENIS = 2                           # ilk iki dalga genis kivrim; geri kalani kirisik

KIRMIZI = np.array([227.0, 10.0, 23.0])
BEYAZ = np.array([252.0, 250.0, 250.0])

# Kivrimlar: (frekans_x, frekans_y, faz, genlik). Frekanslar kadrajin
# tamamina gore; y bilesenleri kivrimlari egik gostermek icin var.
DALGALAR = (
    (2.20, 0.75, 0.40, 1.00),
    (1.05, -0.40, -1.00, 0.55),
    (4.30, 1.45, 2.20, 0.20),
    (7.60, 2.55, 0.70, 0.06),
)


def alan(s, t, dalgalar=DALGALAR):
    """Kadraj koordinatlarinda kumas derinligi ve egimleri."""
    z = np.zeros_like(s)
    zs = np.zeros_like(s)
    zt = np.zeros_like(s)
    for fx, fy, faz, g in dalgalar:
        p = 2 * np.pi * (fx * s + fy * t) + faz
        z += g * np.sin(p)
        zs += g * 2 * np.pi * fx * np.cos(p)
        zt += g * 2 * np.pi * fy * np.cos(p)
    return z, zs, zt


def sikisma(s, t):
    """Kivrimlarin yatay sikismasi: ana dalganin ceyrek kaydirilmisi."""
    fx, fy, faz, _ = DALGALAR[0]
    return np.sin(2 * np.pi * (fx * s + fy * t) + faz + 1.55)


def yildiz_koseleri():
    """Bes koseli yildizin 10 kosesi (bayrak birimleri)."""
    R, r = 2.5, 2.5 * 0.38197
    cx, cy = 16.3, 10.0
    return np.array([
        (cx + (R if i % 2 == 0 else r) * np.cos(i * np.pi / 5),
         cy - (R if i % 2 == 0 else r) * np.sin(i * np.pi / 5))
        for i in range(10)
    ])


def yildiz_icinde(x, y):
    """Cift-tek kuraliyla nokta-icinde testi."""
    p = yildiz_koseleri()
    ic = np.zeros(x.shape, dtype=bool)
    for i in range(len(p)):
        x1, y1 = p[i]
        x2, y2 = p[(i + 1) % len(p)]
        with np.errstate(divide="ignore", invalid="ignore"):
            sinir = (x2 - x1) * (y - y1) / (y2 - y1) + x1
        ic ^= ((y1 > y) != (y2 > y)) & (x < sinir)
    return ic


def uret():
    px = (np.arange(W * SS) + 0.5) / (W * SS)
    py = (np.arange(H * SS) + 0.5) / (H * SS)
    S, T = np.meshgrid(px, py)

    # Ileri donusum X = s*W + YATAY*sikisma, Y = t*H + DUSEY*z; sabit
    # nokta yinelemesiyle tersleniyor.
    # Amblemi buken kayma yalnizca genis kivrimlardan gelir; ince
    # kirisikliklar kumasi tasimaz, sadece isigi kirar.
    s, t = S.copy(), T.copy()
    for _ in range(14):
        kz, _, _ = alan(s, t, DALGALAR[:GENIS])
        s = S - YATAY * sikisma(s, t) / W
        t = T - DUSEY * kz / H

    z, zs, zt = alan(s, t)

    # --- yuzey rengi -----------------------------------------------------
    fx = (UMIN + s * USPAN) * 30.0
    fy = (VMIN + t * VSPAN) * 20.0
    ay = (((fx - 10.0) ** 2 + (fy - 10.0) ** 2 <= 25.0)
          & ((fx - 11.25) ** 2 + (fy - 10.0) ** 2 > 16.0))
    renk = np.where((ay | yildiz_icinde(fx, fy))[..., None], BEYAZ, KIRMIZI)

    # --- isik ------------------------------------------------------------
    nx = -DERINLIK * zs / W
    ny = -DERINLIK * zt / H
    boy = np.sqrt(nx * nx + ny * ny + 1.0)
    nx, ny, nz = nx / boy, ny / boy, 1.0 / boy

    isik = np.array([-0.42, -0.56, 0.72])
    isik /= np.linalg.norm(isik)
    yayinim = np.clip(nx * isik[0] + ny * isik[1] + nz * isik[2], 0.0, 1.0)

    yari = isik + np.array([0.0, 0.0, 1.0])
    yari /= np.linalg.norm(yari)
    parlak = np.clip(nx * yari[0] + ny * yari[1] + nz * yari[2], 0.0, 1.0) ** 22

    golge = 1.0 - 0.18 * np.clip(-z - 0.4, 0.0, 1.6) / 1.6
    aydinlik = (0.40 + 0.78 * yayinim) * golge

    kx, ky = (S - 0.5) * 2.0, (T - 0.5) * 2.0
    aydinlik *= 1.0 - 0.17 * np.clip(0.55 * (kx * kx + ky * ky), 0, 1)

    kare = np.clip(renk * aydinlik[..., None] + 255.0 * 0.28 * parlak[..., None],
                   0, 255).astype(np.uint8)
    return Image.fromarray(kare).resize((W, H), Image.LANCZOS)


if __name__ == "__main__":
    varsayilan = Path(__file__).with_name("bayrak.jpg")
    hedef = Path(sys.argv[1]) if len(sys.argv) > 1 else varsayilan
    uret().save(hedef, quality=90, optimize=True)
    print(hedef, hedef.stat().st_size // 1024, "KB")
