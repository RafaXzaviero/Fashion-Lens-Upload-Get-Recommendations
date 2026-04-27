import streamlit as st
import requests
from PIL import Image
import io
from datetime import datetime

st.set_page_config(page_title="Fashion Lens", layout="wide", page_icon="📸")

# ══════════════════════════════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════════════════════════════
if 'upload_count' not in st.session_state:
    st.session_state.upload_count = 0

# ══════════════════════════════════════════════════════════════════
#  TEMA GELAP
# ══════════════════════════════════════════════════════════════════
bg_main        = "#0d0a18"
bg_card        = "rgba(255,255,255,0.05)"
bg_sidebar     = "rgba(255,255,255,0.03)"
border_color   = "rgba(192,132,252,0.2)"
border_input   = "rgba(192,132,252,0.45)"
text_primary   = "#ffffff"
text_secondary = "#cdc0f0"
text_muted     = "#9080c0"
input_bg       = "rgba(255,255,255,0.1)"
success_bg     = "rgba(34,197,94,0.09)"
success_border = "rgba(34,197,94,0.3)"
success_title  = "#86efac"
error_bg       = "rgba(239,68,68,0.09)"
error_border   = "rgba(239,68,68,0.3)"
error_title    = "#fca5a5"
upload_hover   = "rgba(232,67,147,0.04)"
badge_color_bg = "rgba(232,67,147,0.18)"; badge_color_bd = "rgba(232,67,147,0.4)";  badge_color_tx = "#f9b8d8"
badge_cat_bg   = "rgba(139,92,246,0.18)"; badge_cat_bd   = "rgba(139,92,246,0.4)";  badge_cat_tx   = "#d4bbff"
badge_sea_bg   = "rgba(34,211,238,0.12)"; badge_sea_bd   = "rgba(34,211,238,0.3)";  badge_sea_tx   = "#9aeef8"
badge_use_bg   = "rgba(255,255,255,0.08)";badge_use_bd   = "rgba(255,255,255,0.15)";badge_use_tx   = "#cdc0f0"
gradient_bg    = f"radial-gradient(ellipse 90% 55% at 75% -5%, rgba(232,67,147,0.25) 0%, transparent 58%), radial-gradient(ellipse 65% 50% at 5% 90%, rgba(139,92,246,0.20) 0%, transparent 55%), {bg_main}"

# ══════════════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;700&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{
    background: {bg_main} !important;
    color: {text_primary} !important;
    font-family: 'DM Sans', sans-serif !important;
}}
[data-testid="stAppViewContainer"] {{
    background: {gradient_bg} !important;
    min-height: 100vh;
}}

header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu, footer {{ display: none !important; }}

.block-container {{ padding: 2.5rem 3rem 4rem !important; max-width: 1280px !important; }}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {{
    color: {text_secondary} !important; font-size: 16px !important; line-height: 1.75 !important;
}}
[data-testid="stMarkdownContainer"] strong {{ color: {text_primary} !important; font-weight: 700 !important; }}

/* ══ SIDEBAR ══ */
[data-testid="stSidebar"] {{
    background: {bg_sidebar} !important;
    border-right: 1px solid {border_color} !important;
}}
[data-testid="stSidebar"] label {{
    color: {text_secondary} !important; font-size: 14px !important; font-weight: 500 !important;
}}
[data-testid="stSidebar"] input {{
    background: {input_bg} !important;
    border: 1.5px solid {border_input} !important;
    border-radius: 10px !important; color: {text_primary} !important;
}}
[data-testid="stSidebar"] .stCaption p {{ color: {text_muted} !important; font-size: 12px !important; }}

/* ══ BRAND ══ */
.fl-brand {{
    display: flex; align-items: center; gap: 18px;
    padding-bottom: 28px; border-bottom: 1px solid {border_color}; margin-bottom: 4px;
    animation: fadeInUp 0.5s ease forwards;
}}
.fl-brand-icon {{
    width: 60px; height: 60px;
    background: linear-gradient(135deg, #e84393, #8b5cf6);
    border-radius: 16px; display: flex; align-items: center;
    justify-content: center; font-size: 30px; flex-shrink: 0;
    box-shadow: 0 4px 20px rgba(139,92,246,0.25);
}}
.fl-brand-title {{
    font-family: 'Playfair Display', serif; font-size: 38px; font-weight: 900;
    background: linear-gradient(135deg, #8b5cf6 20%, #e84393 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0; line-height: 1.05;
}}
.fl-brand-sub {{ font-size: 12px; letter-spacing: 3px; text-transform: uppercase; color: {text_muted}; margin: 6px 0 0; }}

/* ══ HERO ══ */
.fl-hero {{ margin: 36px 0 28px; animation: fadeInUp 0.5s ease 0.1s both; }}
.fl-hero-label {{
    font-size: 12px; letter-spacing: 3px; text-transform: uppercase;
    color: #e84393; font-weight: 700; margin-bottom: 14px;
    display: flex; align-items: center; gap: 8px;
}}
.fl-hero-label::before {{
    content: ''; display: inline-block; width: 24px; height: 2px;
    background: linear-gradient(90deg, #e84393, #8b5cf6); border-radius: 1px;
}}
.fl-hero-title {{
    font-family: 'Playfair Display', serif; font-size: 48px; font-weight: 900;
    color: {text_primary}; line-height: 1.1; margin: 0 0 16px;
}}
.fl-hero-title span {{
    background: linear-gradient(135deg, #e84393 0%, #8b5cf6 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}}
.fl-hero-desc {{ font-size: 17px; color: {text_secondary}; line-height: 1.7; margin: 0 0 28px; max-width: 680px; }}

/* ══ STATS ══ */
.stats-row {{ display: flex; gap: 24px; margin: 0 0 36px; animation: fadeInUp 0.5s ease 0.15s both; }}
.stat-num {{ font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 900; color: {text_primary}; line-height: 1; }}
.stat-num span {{
    background: linear-gradient(135deg, #e84393, #8b5cf6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}}
.stat-label {{ font-size: 13px; color: {text_muted}; margin-top: 4px; }}

/* ══ UPLOAD ══ */
[data-testid="stFileUploader"] {{
    background: {bg_card} !important;
    border: 2px dashed rgba(192,132,252,0.6) !important;
    border-radius: 24px !important; padding: 16px !important;
    animation: borderPulse 2.5s ease-in-out infinite;
}}
[data-testid="stFileUploader"]:hover {{
    border-color: rgba(232,67,147,0.8) !important; background: {upload_hover} !important;
}}
[data-testid="stFileUploader"] label {{
    color: {text_primary} !important; font-size: 16px !important; font-weight: 700 !important;
}}
[data-testid="stFileUploader"] section {{
    border: none !important; background: transparent !important;
    padding: 32px 24px !important; text-align: center;
}}
[data-testid="stFileUploader"] section p,
[data-testid="stFileUploaderDropzoneInstructions"],
[data-testid="stFileUploaderDropzoneInstructions"] span {{
    color: {text_secondary} !important; font-size: 15px !important;
}}

/* ══ FEATURE CARDS ══ */
.feat-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 32px 0 0; }}
.feat-card {{
    background: {bg_card}; border: 1px solid {border_color}; border-radius: 20px;
    padding: 24px 20px; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeInUp 0.5s ease both;
}}
.feat-card:nth-child(1) {{ animation-delay: 0.20s; }}
.feat-card:nth-child(2) {{ animation-delay: 0.25s; }}
.feat-card:nth-child(3) {{ animation-delay: 0.30s; }}
.feat-card:nth-child(4) {{ animation-delay: 0.35s; }}
.feat-card:hover {{
    border-color: rgba(232,67,147,0.4);
    box-shadow: 0 8px 30px rgba(139,92,246,0.15); transform: translateY(-4px);
}}
.feat-card-icon {{ font-size: 28px; margin-bottom: 14px; display: block; }}
.feat-card-title {{ font-size: 15px; font-weight: 700; color: {text_primary}; margin: 0 0 8px; }}
.feat-card-desc {{ font-size: 13px; color: {text_muted}; line-height: 1.6; margin: 0; }}

/* ══ EXPANDER ══ */
[data-testid="stExpander"] {{
    background: rgba(30,20,50,0.85) !important;
    border: 1.5px solid rgba(192,132,252,0.45) !important;
    border-radius: 16px !important; margin-top: 28px !important; overflow: hidden;
}}
[data-testid="stExpander"]:hover {{ border-color: rgba(232,67,147,0.5) !important; }}
[data-testid="stExpander"] summary p {{ color: #ffffff !important; font-size: 16px !important; font-weight: 800 !important; }}
[data-testid="stExpander"] svg {{ color: #c084fc !important; fill: #c084fc !important; }}
[data-testid="stExpander"] label {{ color: #e2d4ff !important; font-size: 15px !important; font-weight: 700 !important; }}
[data-testid="stExpander"] input,
[data-testid="stExpander"] [data-baseweb="base-input"] input {{
    background: #000000 !important; border: 2px solid rgba(192,132,252,0.7) !important;
    border-radius: 12px !important; color: #c084fc !important;
    font-size: 16px !important; font-weight: 700 !important; padding: 12px 16px !important;
}}
[data-testid="stExpander"] input::placeholder {{ color: rgba(192,132,252,0.4) !important; }}
[data-testid="stExpander"] [data-baseweb="base-input"] {{
    background: #000000 !important; border: 2px solid rgba(192,132,252,0.7) !important; border-radius: 12px !important;
}}
[data-testid="stExpander"] [data-baseweb="base-input"]:focus-within {{
    border-color: #c084fc !important; box-shadow: 0 0 0 3px rgba(192,132,252,0.25) !important;
}}
[data-testid="stExpander"] .stCaption p {{ color: #b8a8e0 !important; font-size: 13px !important; font-weight: 500 !important; }}
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {{ color: #d4bbff !important; font-size: 15px !important; font-weight: 600 !important; }}

/* ══ BUTTONS ══ */
.stButton > button {{
    background: linear-gradient(135deg, #e84393, #8b5cf6) !important;
    border: none !important; border-radius: 50px !important;
    color: white !important; font-weight: 700 !important; font-size: 15px !important;
    padding: 12px 32px !important; font-family: 'DM Sans', sans-serif !important;
    box-shadow: 0 4px 20px rgba(139,92,246,0.25) !important;
    transition: all 0.2s ease !important;
}}
.stButton > button:hover {{ opacity: 0.88 !important; transform: translateY(-2px) !important; }}

/* ══ IMAGE ══ */
[data-testid="stImage"] img {{
    border-radius: 20px !important; border: 1px solid {border_color} !important;
    box-shadow: 0 8px 32px rgba(139,92,246,0.12) !important;
}}

/* ══ SECTION LABEL ══ */
.fl-section-label {{
    font-size: 12px; letter-spacing: 3px; text-transform: uppercase;
    color: #8b5cf6; font-weight: 700; margin: 36px 0 18px;
    display: flex; align-items: center; gap: 10px;
}}
.fl-section-label::before {{
    content: ''; display: inline-block; width: 20px; height: 2px;
    background: linear-gradient(90deg, #e84393, #8b5cf6); border-radius: 1px;
}}
hr {{ border-color: {border_color} !important; margin: 32px 0 !important; }}

/* ══ REC CARDS — dengan gambar ══ */
.rec-card {{
    background: {bg_card};
    border: 1px solid {border_color};
    border-radius: 20px;
    overflow: hidden;
    margin-bottom: 20px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeInUp 0.4s ease both;
}}
.rec-card:nth-child(1) {{ animation-delay: 0.05s; }}
.rec-card:nth-child(2) {{ animation-delay: 0.10s; }}
.rec-card:nth-child(3) {{ animation-delay: 0.15s; }}
.rec-card:hover {{
    border-color: rgba(232,67,147,0.45);
    box-shadow: 0 12px 36px rgba(232,67,147,0.12);
    transform: translateY(-4px);
}}

/* Gambar produk */
.rec-card-img-wrap {{
    width: 100%;
    overflow: hidden;
    background: rgba(255,255,255,0.04);
    border-radius: 0;
    position: relative;
}}
/* st.image yang di-render di dalam card */
.rec-card-img-wrap [data-testid="stImage"] {{
    margin: 0 !important; padding: 0 !important;
}}
.rec-card-img-wrap [data-testid="stImage"] img {{
    width: 100% !important;
    height: 220px !important;
    object-fit: cover !important;
    object-position: top center !important;
    border-radius: 0 !important;
    border: none !important;
    box-shadow: none !important;
    transition: transform 0.4s ease;
    display: block;
}}
.rec-card:hover .rec-card-img-wrap img {{ transform: scale(1.05); }}
.rec-card-img-placeholder {{
    font-size: 52px; opacity: 0.35;
    padding: 40px 0; text-align: center;
}}

/* Body card */
.rec-card-body {{ padding: 16px 18px 18px; }}
.rec-card-name {{
    font-family: 'Playfair Display', serif; font-size: 15px; font-weight: 700;
    color: {text_primary} !important; margin: 0 0 12px; line-height: 1.35;
    border-bottom: 1px solid {border_color}; padding-bottom: 10px;
}}
.rec-card-badges {{ display: flex; flex-wrap: wrap; gap: 0; margin-top: 2px; }}

.rec-badge {{
    display: inline-block; padding: 4px 12px; border-radius: 20px;
    font-size: 12px; font-weight: 500; margin: 3px 4px 3px 0;
}}
.rec-badge-color  {{ background:{badge_color_bg}; border:1px solid {badge_color_bd}; color:{badge_color_tx} !important; }}
.rec-badge-cat    {{ background:{badge_cat_bg};   border:1px solid {badge_cat_bd};   color:{badge_cat_tx}   !important; }}
.rec-badge-season {{ background:{badge_sea_bg};   border:1px solid {badge_sea_bd};   color:{badge_sea_tx}   !important; }}
.rec-badge-usage  {{ background:{badge_use_bg};   border:1px solid {badge_use_bd};   color:{badge_use_tx}   !important; }}

/* ══ TOMBOL LIHAT PRODUK ══ */
.rec-card-footer {{
    padding: 0 18px 16px;
    display: flex; align-items: center; justify-content: space-between;
}}
.btn-lihat-produk {{
    display: inline-flex; align-items: center; gap: 6px;
    background: linear-gradient(135deg, #e84393, #8b5cf6);
    color: #ffffff !important; font-size: 13px; font-weight: 700;
    padding: 8px 18px; border-radius: 50px; text-decoration: none;
    transition: opacity 0.2s, transform 0.15s;
    box-shadow: 0 3px 12px rgba(232,67,147,0.3);
}}
.btn-lihat-produk:hover {{ opacity: 0.85; transform: translateY(-1px); }}

/* ══ FILTER BAR ══ */
.filter-bar {{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(192,132,252,0.2);
    border-radius: 16px;
    padding: 18px 22px;
    margin: 16px 0 24px;
    display: flex; flex-wrap: wrap; align-items: center; gap: 12px;
}}
.filter-label {{
    font-size: 12px; letter-spacing: 2px; text-transform: uppercase;
    color: #8b5cf6; font-weight: 700; margin-right: 4px; flex-shrink: 0;
}}

/* Multiselect Streamlit */
[data-testid="stMultiSelect"] {{
    background: transparent !important;
}}
[data-testid="stMultiSelect"] > div > div {{
    background: rgba(255,255,255,0.06) !important;
    border: 1.5px solid rgba(192,132,252,0.4) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-size: 14px !important;
}}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
    background: linear-gradient(135deg, rgba(232,67,147,0.3), rgba(139,92,246,0.3)) !important;
    border: 1px solid rgba(192,132,252,0.4) !important;
    border-radius: 20px !important;
    color: #ffffff !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}}
[data-testid="stMultiSelect"] input {{ color: #ffffff !important; }}
[data-testid="stMultiSelect"] label {{
    color: #cdc0f0 !important; font-size: 13px !important; font-weight: 600 !important;
}}
/* Dropdown list items */
li[role="option"] {{
    background: #1a0f2e !important; color: #e8e0ff !important;
    font-size: 14px !important;
}}
li[role="option"]:hover {{ background: rgba(139,92,246,0.25) !important; }}

/* Reset filter button */
.filter-reset {{
    font-size: 12px; color: #9080c0; cursor: pointer;
    text-decoration: underline; text-underline-offset: 2px;
    background: none; border: none; font-family: inherit;
    transition: color 0.2s;
}}
.filter-reset:hover {{ color: #e84393; }}

/* Hasil filter info */
.filter-info {{
    font-size: 13px; color: #9080c0; margin: 0 0 16px;
}}
.filter-info strong {{ color: #cdc0f0; }}

/* ══ FOOTER ══ */
.fl-footer {{ margin-top: 60px; padding-top: 28px; border-top: 1px solid {border_color}; text-align: center; }}
.fl-footer-text {{ font-size: 14px; color: {text_muted}; }}
.fl-footer-text span {{
    background: linear-gradient(135deg, #e84393, #8b5cf6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; font-weight: 700;
}}

[data-testid="column"] {{ padding: 0 8px !important; }}
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: rgba(192,132,252,0.3); border-radius: 3px; }}

@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(18px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes borderPulse {{
    0%, 100% {{ border-color: rgba(192,132,252,0.6) !important; }}
    50%       {{ border-color: rgba(232,67,147,0.85) !important; }}
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  BRAND HEADER
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="fl-brand">
    <div class="fl-brand-icon">📸</div>
    <div>
        <div class="fl-brand-title">Fashion Lens</div>
        <div class="fl-brand-sub">AI-Powered Style Discovery</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f'<p style="font-family:\'Playfair Display\',serif;font-size:20px;font-weight:900;color:{text_primary};margin-bottom:16px;">⚙️ Konfigurasi</p>', unsafe_allow_html=True)
    api_url = st.text_input("Flask API URL", "http://127.0.0.1:5001/upload_image", key="sidebar_api")
    st.caption("Pastikan Flask backend berjalan sebelum upload.")
    st.markdown("---")
    st.markdown(f'<p style="font-size:13px;color:{text_muted};">📊 Upload sesi ini: <strong style="color:{text_primary};">{st.session_state.upload_count}</strong></p>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="fl-hero">
    <div class="fl-hero-label">Upload &amp; Discover</div>
    <div class="fl-hero-title">Temukan <span>gaya</span> yang<br>tepat untukmu</div>
    <div class="fl-hero-desc">
        Upload foto pakaianmu dan dapatkan rekomendasi outfit serupa yang dikurasi oleh AI —
        cepat, akurat, dan <em>stylish</em>.
    </div>
</div>
<div class="stats-row">
    <div class="stat-item">
        <div class="stat-num"><span>{st.session_state.upload_count}</span></div>
        <div class="stat-label">Upload sesi ini</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  UPLOAD
# ══════════════════════════════════════════════════════════════════
uploaded_file = st.file_uploader(
    "📂  Pilih atau seret gambar pakaian ke sini",
    type=['jpg', 'png', 'jpeg'],
    accept_multiple_files=False
)

# ══════════════════════════════════════════════════════════════════
#  FEATURE CARDS
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="fl-section-label">Cara Kerja</div>
<div class="feat-grid">
    <div class="feat-card">
        <span class="feat-card-icon">📤</span>
        <div class="feat-card-title">Upload Foto</div>
        <div class="feat-card-desc">Pilih file JPG, PNG, atau JPEG. Pastikan pakaian terlihat jelas di foto.</div>
    </div>
    <div class="feat-card">
        <span class="feat-card-icon">🎨</span>
        <div class="feat-card-title">Deteksi Warna</div>
        <div class="feat-card-desc">AI mengenali warna dominan pakaianmu secara otomatis.</div>
    </div>
    <div class="feat-card">
        <span class="feat-card-icon">🔍</span>
        <div class="feat-card-title">AI Menganalisis</div>
        <div class="feat-card-desc">Kategori, gaya, musim, dan jenis penggunaan dikenali dalam detik.</div>
    </div>
    <div class="feat-card">
        <span class="feat-card-icon">✨</span>
        <div class="feat-card-title">Dapat Rekomendasi</div>
        <div class="feat-card-desc">Outfit serupa dikurasi dari database ribuan produk fashion.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  API CONFIG
# ══════════════════════════════════════════════════════════════════
with st.expander("⚙️  Konfigurasi API Backend"):
    st.markdown("**Masukkan URL Flask backend kamu:**")
    api_url_exp = st.text_input(
        "Flask API URL",
        "http://127.0.0.1:5001/upload_image",
        label_visibility="collapsed",
        key="exp_api"
    )
    st.caption("Pastikan Flask backend sudah berjalan sebelum upload gambar.")

# ══════════════════════════════════════════════════════════════════
#  PROSES GAMBAR
# ══════════════════════════════════════════════════════════════════
if uploaded_file is not None:
    st.markdown('<hr>', unsafe_allow_html=True)

    img_col, _ = st.columns([1, 2])
    with img_col:
        image = Image.open(uploaded_file)
        # ✅ Diganti dari use_column_width (deprecated) ke use_container_width
        st.image(image, caption="Gambar yang diupload", use_container_width=True)

    with st.spinner('✨ Menganalisis gaya pakaian...'):
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()
        files = {'image': (uploaded_file.name, img_bytes, 'image/jpeg')}

        try:
            response = requests.post(api_url, files=files)

            if response.status_code == 200:
                data = response.json()
                recs = data.get('recommendations', [])
                dominant_color = data.get('dominant_color', '')

                st.session_state.upload_count += 1

                st.markdown(f"""
                <div style="background:{success_bg};border:1px solid {success_border};
                    border-radius:16px;padding:18px 24px;margin:24px 0;
                    display:flex;align-items:center;gap:16px;">
                    <span style="font-size:26px;">🎯</span>
                    <div>
                        <div style="font-size:17px;font-weight:700;color:{success_title};">Analisis Berhasil!</div>
                        <div style="font-size:15px;color:{text_secondary};margin-top:4px;">
                            Warna dominan: <strong style="color:{text_primary};">{dominant_color}</strong>
                            &nbsp;·&nbsp; <strong style="color:{text_primary};">{len(recs)}</strong> produk serupa ditemukan
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown('<div class="fl-section-label">Rekomendasi Outfit</div>', unsafe_allow_html=True)

                # ══ FILTER BAR ══════════════════════════════════════
                all_cats    = sorted(set(r.get('articleType', '') for r in recs if r.get('articleType')))
                all_seasons = sorted(set(r.get('season', '')      for r in recs if r.get('season')))
                all_usages  = sorted(set(r.get('usage', '')       for r in recs if r.get('usage')))

                st.markdown('<div class="filter-bar"><span class="filter-label">🎛 Filter Rekomendasi</span></div>', unsafe_allow_html=True)

                fc1, fc2, fc3, fc4 = st.columns([2, 2, 2, 1])
                with fc1:
                    sel_cat = st.multiselect(
                        "Kategori", all_cats, placeholder="Semua kategori",
                        key=f"f_cat_{st.session_state.upload_count}", label_visibility="collapsed"
                    )
                with fc2:
                    sel_season = st.multiselect(
                        "Musim", all_seasons, placeholder="Semua musim",
                        key=f"f_sea_{st.session_state.upload_count}", label_visibility="collapsed"
                    )
                with fc3:
                    sel_usage = st.multiselect(
                        "Penggunaan", all_usages, placeholder="Semua penggunaan",
                        key=f"f_use_{st.session_state.upload_count}", label_visibility="collapsed"
                    )
                with fc4:
                    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
                    reset = st.button("↺ Reset", key=f"reset_{st.session_state.upload_count}")

                # Terapkan filter
                filtered = recs
                if not reset:
                    if sel_cat:    filtered = [r for r in filtered if r.get('articleType') in sel_cat]
                    if sel_season: filtered = [r for r in filtered if r.get('season')      in sel_season]
                    if sel_usage:  filtered = [r for r in filtered if r.get('usage')       in sel_usage]

                aktif = 0 if reset else len([x for x in [sel_cat, sel_season, sel_usage] if x])
                if aktif:
                    st.markdown(
                        f'<div class="filter-info">Menampilkan <strong>{len(filtered)}</strong> '
                        f'dari <strong>{len(recs)}</strong> produk &nbsp;·&nbsp; {aktif} filter aktif</div>',
                        unsafe_allow_html=True
                    )

                # ══ GRID CARDS ══════════════════════════════════════
                if not filtered:
                    st.markdown(
                        '<div style="text-align:center;padding:48px 24px;color:#9080c0;font-size:15px;line-height:1.9;">'
                        '😕 Tidak ada produk yang cocok.<br>'
                        '<span style="font-size:13px;">Coba reset filter atau ubah kombinasinya.</span>'
                        '</div>',
                        unsafe_allow_html=True
                    )
                else:
                    cols = st.columns(3, gap="medium")
                    for idx, item in enumerate(filtered):
                        with cols[idx % 3]:
                            name    = item.get('productDisplayName', 'Produk')
                            color   = item.get('baseColour', '-')
                            cat     = item.get('articleType', '-')
                            season  = item.get('season', '-')
                            usage   = item.get('usage', '-')
                            img_url = item.get('link', '')

                            # Card — buka wrapper
                            st.markdown(
                                '<div class="rec-card"><div class="rec-card-img-wrap">',
                                unsafe_allow_html=True
                            )

                            # Gambar via st.image (bebas HTML escape bug)
                            if img_url:
                                try:
                                    st.image(img_url, use_container_width=True)
                                except Exception:
                                    st.markdown('<div class="rec-card-img-placeholder">👕</div>', unsafe_allow_html=True)
                            else:
                                st.markdown('<div class="rec-card-img-placeholder">👕</div>', unsafe_allow_html=True)

                            # Tombol Lihat Produk
                            lihat = (
                                f'<a href="{img_url}" target="_blank" class="btn-lihat-produk">🛍 Lihat Produk ↗</a>'
                                if img_url else ''
                            )

                            # Card body + tutup wrapper
                            st.markdown(f"""
                                </div>
                                <div class="rec-card-body">
                                    <div class="rec-card-name">{name}</div>
                                    <div class="rec-card-badges">
                                        <span class="rec-badge rec-badge-color">🎨 {color}</span>
                                        <span class="rec-badge rec-badge-cat">👕 {cat}</span>
                                        <span class="rec-badge rec-badge-season">🌤 {season}</span>
                                        <span class="rec-badge rec-badge-usage">💼 {usage}</span>
                                    </div>
                                </div>
                                <div class="rec-card-footer">{lihat}</div>
                            </div>""", unsafe_allow_html=True)

                            # Rating bintang
                            rating = st.feedback("stars", key=f"rating_{idx}_{st.session_state.upload_count}")
                            if rating is not None:
                                st.markdown(
                                    '<div style="font-size:13px;color:#e84393;font-weight:600;margin:4px 0 10px;">✓ Terima kasih!</div>',
                                    unsafe_allow_html=True
                                )

            else:
                st.markdown(f"""
                <div style="background:{error_bg};border:1px solid {error_border};
                    border-radius:16px;padding:18px 24px;margin:24px 0;">
                    <div style="font-size:16px;font-weight:700;color:{error_title};">⚠️ Gagal menghubungi server</div>
                    <div style="font-size:14px;color:{text_secondary};margin-top:6px;">Status code: {response.status_code}</div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.markdown(f"""
            <div style="background:{error_bg};border:1px solid {error_border};
                border-radius:16px;padding:18px 24px;margin:24px 0;">
                <div style="font-size:16px;font-weight:700;color:{error_title};">🔌 Koneksi Backend Terputus</div>
                <div style="font-size:14px;color:{text_secondary};margin-top:6px;">{e}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="fl-footer">
    <div class="fl-footer-text">
        Dibuat dengan ❤️ menggunakan <span>Fashion Lens AI</span> · 2026
    </div>
</div>
""", unsafe_allow_html=True)
