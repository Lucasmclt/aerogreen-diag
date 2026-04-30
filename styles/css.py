import streamlit as st


def load_css():
    st.markdown("""
    <style>
    :root {
        --bg: #f8fafc;
        --panel: rgba(255,255,255,0.94);
        --panel-soft: #f8fafc;
        --line: #e5e7eb;
        --text: #0f172a;
        --muted: #64748b;
        --primary: #6366f1;
        --primary-soft: #eef2ff;
        --secondary: #10b981;
        --shadow: 0 14px 36px rgba(15, 23, 42, 0.06);
        --radius-lg: 22px;
        --radius-md: 18px;
        --radius-sm: 14px;
    }

    /* GLOBAL */
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(99,102,241,0.10), transparent 24%),
            radial-gradient(circle at top right, rgba(16,185,129,0.08), transparent 22%),
            linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color: var(--text);
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 4.8rem;
        max-width: 1280px;
    }

    h1, h2, h3 {
        color: var(--text);
        letter-spacing: -0.03em;
        font-weight: 800;
    }

    h2 {
        font-size: 1.85rem;
        margin-bottom: .35rem;
    }

    p, label, .stMarkdown, .stCaption {
        color: var(--text);
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background:
            radial-gradient(circle at top left, rgba(99,102,241,0.10), transparent 26%),
            #ffffff;
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .sidebar-brand {
        background:
            radial-gradient(circle at top left, rgba(99,102,241,0.18), transparent 44%),
            linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 18px 18px 16px;
        box-shadow: 0 10px 26px rgba(15,23,42,0.04);
        margin-bottom: 12px;
    }

    .sidebar-brand-title {
        font-size: 1.05rem;
        font-weight: 900;
        color: var(--text);
        letter-spacing: -0.03em;
    }

    .sidebar-brand-sub {
        color: var(--muted);
        font-size: .83rem;
        margin-top: 4px;
        line-height: 1.45;
    }

    .sidebar-section-label {
        color: var(--muted);
        font-size: .76rem;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin: .2rem 0 .55rem;
    }

    /* Sidebar radio navigation */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div {
        gap: .5rem;
    }

    [data-testid="stSidebar"] [data-baseweb="radio"] {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 10px 12px;
        transition: all .18s ease;
        box-shadow: 0 1px 0 rgba(15,23,42,0.02);
    }

    [data-testid="stSidebar"] [data-baseweb="radio"]:hover {
        transform: translateY(-1px);
        border-color: #cbd5e1;
        background: #f8fafc;
    }

    [data-testid="stSidebar"] [data-baseweb="radio"]:has(input:checked) {
        background: linear-gradient(180deg, rgba(99,102,241,0.10), rgba(99,102,241,0.04));
        border-color: rgba(99,102,241,0.34);
        box-shadow: 0 8px 18px rgba(99,102,241,0.12);
    }

    [data-testid="stSidebar"] [data-baseweb="radio"] > div:first-child {
        display: none;
    }

    [data-testid="stSidebar"] [data-baseweb="radio"] label,
    [data-testid="stSidebar"] [data-baseweb="radio"] span,
    [data-testid="stSidebar"] [data-baseweb="radio"] p {
        font-weight: 700 !important;
        color: var(--text) !important;
    }

    /* HERO + PAGE INTRO */
    .hero {
        background:
            radial-gradient(circle at top left, rgba(99,102,241,0.22), transparent 30%),
            radial-gradient(circle at top right, rgba(16,185,129,0.16), transparent 28%),
            white;
        border: 1px solid var(--line);
        border-radius: 32px;
        padding: 62px;
        box-shadow: 0 24px 90px rgba(15, 23, 42, 0.08);
        animation: fadeIn .42s ease-in;
    }

    .page-header {
        background:
            linear-gradient(180deg, rgba(255,255,255,.88), rgba(248,250,252,.92));
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 28px 28px 24px;
        box-shadow: var(--shadow);
        animation: fadeIn .32s ease-in;
        margin-bottom: 1rem;
    }

    .page-header-tag {
        display: inline-block;
        background: var(--primary-soft);
        color: #4f46e5;
        padding: 7px 12px;
        border-radius: 999px;
        font-size: .78rem;
        font-weight: 800;
        margin-bottom: 12px;
        letter-spacing: .02em;
    }

    .page-header h1, .page-header h2, .page-header h3 {
        margin: 0;
        line-height: 1.05;
    }

    .page-header-sub {
        color: var(--muted);
        font-size: 1rem;
        line-height: 1.65;
        margin-top: 10px;
        max-width: 860px;
    }

    .hero-label {
        display: inline-block;
        background: var(--primary-soft);
        color: #4f46e5;
        padding: 7px 13px;
        border-radius: 999px;
        font-size: 0.80rem;
        font-weight: 800;
        margin-bottom: 18px;
        letter-spacing: .02em;
    }

    .hero h1 {
        font-size: 3.35rem;
        line-height: 1.02;
        letter-spacing: -0.055em;
        color: var(--text);
        margin-bottom: 20px;
    }

    .hero p {
        color: #475569;
        font-size: 1.06rem;
        line-height: 1.75;
        max-width: 860px;
    }

    /* CARDS */
    .card {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: 20px;
        padding: 24px;
        box-shadow: var(--shadow);
        animation: fadeIn .34s ease-in;
    }

    .card-soft {
        background: var(--panel-soft);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 22px;
        animation: fadeIn .34s ease-in;
    }

    .card-dark {
        background:
            radial-gradient(circle at top left, rgba(99,102,241,0.16), transparent 40%),
            #0f172a;
        color: white;
        border-radius: 22px;
        padding: 26px;
        box-shadow: 0 22px 52px rgba(15, 23, 42, 0.22);
        animation: fadeIn .34s ease-in;
        border: 1px solid rgba(255,255,255,.08);
    }

    .section-title {
        color: var(--muted);
        font-size: 0.76rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.095em;
        margin-bottom: 10px;
    }

    .kpi {
        font-size: 2.55rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        line-height: 1.0;
    }

    .kpi-sub {
        color: var(--muted);
        font-size: 0.92rem;
        margin-top: 8px;
    }

    .feature-title {
        font-weight: 800;
        color: var(--text);
        margin-bottom: 8px;
        font-size: 1.02rem;
    }

    .feature-text {
        color: var(--muted);
        line-height: 1.62;
        font-size: 0.95rem;
    }

    .pill {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        font-size: .82rem;
        font-weight: 800;
    }

    .progress-track {
        width: 100%;
        height: 10px;
        background: #e5e7eb;
        border-radius: 999px;
        overflow: hidden;
        margin: 12px 0 4px;
    }

    .progress-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #6366f1, #10b981);
        transition: width .3s ease;
    }

    .muted { color: var(--muted); }
    .small { font-size: .86rem; }

    /* INPUTS */
    .stNumberInput input, .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid var(--line) !important;
        background: #fafafa !important;
    }

    .stSelectbox div[data-baseweb="select"] > div,
    .stMultiSelect div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border-color: var(--line) !important;
        background: #fafafa !important;
    }

    .stTextArea textarea {
        border-radius: 12px !important;
        border-color: var(--line) !important;
        background: #fafafa !important;
    }

    .stCheckbox label, .stRadio label {
        color: var(--text) !important;
    }

    /* BUTTONS */
    .stButton button {
        border-radius: 13px;
        padding: 0.7rem 1rem;
        font-weight: 800;
        transition: all .18s ease;
        border: 1px solid var(--line);
        background: white;
    }

    .stButton button:hover {
        transform: translateY(-1px);
        border-color: #cbd5e1;
    }

    .stDownloadButton button {
        background: linear-gradient(90deg, #111827, #1f2937);
        color: white;
        border-radius: 13px;
        padding: 0.78rem 1rem;
        font-weight: 800;
    }

    .stDownloadButton button:hover {
        transform: translateY(-1px);
    }

    /* TABLE */
    [data-testid="stDataFrame"] {
        border-radius: 14px;
        border: 1px solid var(--line);
        overflow: hidden;
        background: white;
    }

    hr {
        border: none;
        height: 1px;
        background: var(--line);
        margin: 1.4rem 0;
    }

    /* ANIMATION */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)
