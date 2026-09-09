"""Yerel Belge Asistani - web arayuzu."""

import html

import streamlit as st

from rag import answer, MIN_SCORE, TOP_K, CHAT_KEYWORD

st.set_page_config(
    page_title="Belge Asistanı",
    page_icon="📄",
    layout="centered",
)

st.markdown(
    """
    <style>
      .block-container { padding-top: 2.5rem; max-width: 800px; }
      h1 { font-size: 1.9rem !important; letter-spacing: -0.02em; margin-bottom: 0.2rem; }
      .intro { color: #6b7280; font-size: 0.95rem; line-height: 1.55;
               margin-bottom: 1.8rem; }
      .stats { color: #6b7280; font-size: 0.78rem; letter-spacing: 0.01em;
               margin-top: 0.6rem; }
      .stats b { font-weight: 600; }
      .card { border-left: 3px solid #4b9e96; padding: 0.15rem 0 0.15rem 0.9rem;
              margin: 0 0 1.1rem 0; }
      .card-head { font-size: 0.82rem; font-weight: 600; margin-bottom: 0.35rem; }
      .card-score { color: #6b7280; font-weight: 400; }
      .card-body { font-size: 0.85rem; color: #6b7280; line-height: 1.55; }
      .side-row { display: flex; justify-content: space-between; font-size: 0.85rem;
                  padding: 0.4rem 0; border-bottom: 1px solid rgba(128,128,128,0.18); }
      .side-row span:last-child { font-weight: 600; }
      .side-note { font-size: 0.8rem; color: #6b7280; line-height: 1.5;
                   margin-top: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

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
        '<div class="side-note">Bir soru, belgelerle yeterince eşleşmezse '
        'dil modeline hiç gönderilmez. Sistem bu durumda tahmin yürütmek '
        'yerine bilgisi olmadığını söyler.</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Konuşmayı temizle", use_container_width=True):
        st.session_state.gecmis = []
        st.rerun()

# --------------------------------------------------------------------- başlık

st.markdown("# Belge Asistanı")
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
    "RAG'in üç adımı nedir?",
    "Vektörler neden BLOB olarak saklanır?",
    "Türkiye'nin başkenti neresi?",
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
            metin, hits, sure = answer(soru)
        kayit = {"soru": soru, "metin": metin, "hits": hits, "sure": sure}
        yaniti_ciz(kayit)

    st.session_state.gecmis.append(kayit)