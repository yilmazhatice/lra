"""Yerel Belge Asistani - web arayuzu."""

import base64
import html
from pathlib import Path

import streamlit as st

from rag import answer, MIN_SCORE, TOP_K, CHAT_KEYWORD

st.set_page_config(
    page_title="Börteçine",
    page_icon="🐺",
    layout="centered",
)


@st.cache_data
def _bayrak_uri() -> str:
    """Dalgalanan bayrak gorselini data-URI'ye cevirir.

    Gorsel varliklar/bayrak_uret.py ile uretiliyor; degistirmek icin o
    betigin dalga tanimlari duzenlenip yeniden calistirilmasi yeterli.
    """
    yol = Path(__file__).parent / "varliklar" / "bayrak.jpg"
    ham = base64.b64encode(yol.read_bytes()).decode("ascii")
    return "data:image/jpeg;base64," + ham


STIL = """
<style>
  /* ---------------------------------------------------- bayrak arka plani */
  [data-testid="stAppViewContainer"] {
    background:
      /* bayragi koyulastiran sicak ortu; carpim oldugu icin beyaz alanlar
         grilesmeden koyu gul rengine iniyor */
      linear-gradient(150deg, #77404a 0%, #5a2c34 46%, #7d434c 100%),
      /* dalgalanan bayrak (varliklar/bayrak.jpg) */
      url("__BAYRAK__") no-repeat 50% 50% / cover;
    background-blend-mode: multiply, normal;
    background-attachment: fixed, fixed;
  }
  [data-testid="stHeader"] { background: transparent; }
  [data-testid="stBottom"] > div { background: transparent; }

  /* ------------------------------------------------------- icerik paneli */
  .block-container {
    max-width: 820px;
    margin-top: 1.2rem;
    margin-bottom: 3rem;
    padding: 2.4rem 2.6rem 2.8rem;
    background: rgba(26,17,20,0.90);
    border: 1px solid rgba(227,10,23,0.28);
    border-radius: 20px;
    box-shadow: 0 20px 55px rgba(0,0,0,0.55);
  }

  h1 { font-size: 1.9rem !important; letter-spacing: -0.02em;
       margin-bottom: 0.2rem; color: #f3dfe1; }
  .intro { color: #b3a5a8; font-size: 0.95rem; line-height: 1.55;
           margin-bottom: 1.6rem; }
  /* baslik altindaki bayrak seridi */
  .serit { height: 4px; border-radius: 3px; margin: 0.1rem 0 1.3rem 0;
           background: linear-gradient(90deg, #c8101f 0%, #c8101f 62%,
                       rgba(200,16,31,0.10) 100%); }

  .stats { color: #9c8f92; font-size: 0.78rem; letter-spacing: 0.01em;
           margin-top: 0.6rem; }
  .stats b { font-weight: 600; color: #e8888f; }
  .card { border-left: 3px solid #c8101f; padding: 0.15rem 0 0.15rem 0.9rem;
          margin: 0 0 1.1rem 0; }
  .card-head { font-size: 0.82rem; font-weight: 600; margin-bottom: 0.35rem;
               color: #e7dcde; }
  .card-score { color: #9c8f92; font-weight: 400; }
  .card-body { font-size: 0.85rem; color: #b3a5a8; line-height: 1.55; }

  /* ---------------------------------------------------------- kenar panel */
  [data-testid="stSidebar"] {
    background: rgba(21,14,16,0.94);
    border-right: 2px solid rgba(200,16,31,0.55);
  }
  [data-testid="stSidebar"] h4 { color: #f3dfe1; }
  .side-row { display: flex; justify-content: space-between; font-size: 0.85rem;
              padding: 0.4rem 0; border-bottom: 1px solid rgba(227,10,23,0.16);
              color: #c9bbbe; }
  .side-row span:last-child { font-weight: 600; color: #e8888f; }
  .side-note { font-size: 0.8rem; color: #9c8f92; line-height: 1.5;
               margin-top: 1rem; }

  /* ---------------------------------------------------------- ogeler */
  .stButton button {
    background: rgba(255,255,255,0.04); color: #eec2c6;
    border: 1px solid rgba(200,16,31,0.55); font-weight: 500;
  }
  .stButton button:hover {
    background: #c8101f; color: #ffffff; border-color: #c8101f;
  }
  [data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(227,10,23,0.16);
    border-radius: 14px;
  }
  [data-testid="stChatInput"] {
    border: 1px solid rgba(200,16,31,0.45);
    background: rgba(30,20,23,0.95);
  }
  .stExpander details {
    border: 1px solid rgba(227,10,23,0.22) !important;
    border-radius: 10px;
    background: rgba(255,255,255,0.03);
  }
  .stSpinner > div { border-top-color: #c8101f !important; }
</style>
"""

st.markdown(STIL.replace("__BAYRAK__", _bayrak_uri()), unsafe_allow_html=True)

# ---------------------------------------------------------------- kenar panel

with st.sidebar:
    st.markdown("#### Sistem yapılandırması")
    rows = [
        ("Dil modeli", CHAT_KEYWORD),
        ("Getirilen bölüm sayısı", str(TOP_K)),
        ("Eşleşme alt sınırı", f"{MIN_SCORE:.2f}"),
        ("Çalışma yeri", "Bu bilgisayar"),
    ]
    for label, value in rows:
        st.markdown(
            f'<div class="side-row"><span>{label}</span><span>{value}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="side-note">Bir soru, belgelerle yeterince eşleşmezse dil '
        'modeline hiç gönderilmez. Sistem bu durumda tahmin yürütmek yerine '
        'bilgisi olmadığını söyler.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Konuşmayı temizle", use_container_width=True):
        st.session_state.gecmis = []
        st.rerun()

# --------------------------------------------------------------------- başlık

st.markdown("# Börteçine")
st.markdown('<div class="serit"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="intro">Yüklediğiniz belgeler hakkında soru sorun. '
    'Asistan yanıtını yalnızca bu belgelerden üretir ve hangi belgeden '
    'yararlandığını her yanıtın sonunda belirtir. İnternet bağlantısı '
    'kullanılmaz; tüm işlem bu bilgisayarda gerçekleşir.</div>',
    unsafe_allow_html=True,
)

if "gecmis" not in st.session_state:
    st.session_state.gecmis = []

# ------------------------------------------------------------- örnek sorular

ORNEKLER = [
    "Eski Türkçede kurdun adı neydi?",
    "Dokuz Işık ilkeleri nelerdir?",
    "Bugün hava nasıl olacak?",
]

secilen = None
if not st.session_state.gecmis:
    st.markdown("**Başlamak için bir örnek seçin**")
    kolonlar = st.columns(len(ORNEKLER))
    for kolon, ornek in zip(kolonlar, ORNEKLER):
        if kolon.button(ornek, use_container_width=True):
            secilen = ornek
    st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------------------------- yardımcı


def kaynaklari_goster(hits):
    baslik = f"Yanıtın dayandığı bölümler ({len(hits)})"
    with st.expander(baslik):
        for skor, _cid, dosya, sira, metin in hits:
            onizleme = metin[:420] + ("…" if len(metin) > 420 else "")
            st.markdown(
                f'<div class="card">'
                f'<div class="card-head">{html.escape(dosya)} '
                f'<span class="card-score">· bölüm {sira} · '
                f'eşleşme {skor:.3f}</span></div>'
                f'<div class="card-body">{html.escape(onizleme)}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


def yaniti_ciz(kayit):
    st.markdown(kayit["metin"])
    hits = kayit["hits"]
    en_iyi = hits[0][0] if hits else 0.0
    st.markdown(
        f'<div class="stats">Yanıt süresi <b>{kayit["sure"]:.1f} sn</b> &nbsp;·&nbsp; '
        f'En yüksek eşleşme <b>{en_iyi:.3f}</b> &nbsp;·&nbsp; '
        f'Taranan bölüm <b>{len(hits)}</b></div>',
        unsafe_allow_html=True,
    )
    if hits:
        kaynaklari_goster(hits)


# --------------------------------------------------------------- konuşma akışı

for kayit in st.session_state.gecmis:
    with st.chat_message("user"):
        st.markdown(kayit["soru"])
    with st.chat_message("assistant"):
        yaniti_ciz(kayit)

soru = st.chat_input("Belgeler hakkında bir soru yazın") or secilen

if soru:
    with st.chat_message("user"):
        st.markdown(soru)

    with st.chat_message("assistant"):
        with st.spinner("Belgeler taranıyor ve yanıt hazırlanıyor…"):
            # Kisa takip sorulari ("bunun sebebi ne?") tek baslarina aranamaz;
            # arama icin bir onceki soruyu da ekliyoruz. Cevap yine yalnizca
            # yeni soruya gore uretiliyor.
            arama = soru
            if st.session_state.gecmis and len(soru.split()) <= 8:
                arama = st.session_state.gecmis[-1]["soru"] + " " + soru

            metin, hits, sure = answer(soru, search_query=arama)

        kayit = {"soru": soru, "metin": metin, "hits": hits, "sure": sure}
        yaniti_ciz(kayit)

    st.session_state.gecmis.append(kayit)
