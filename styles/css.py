import streamlit as st


def load_css():
    st.markdown("""
    <style>
    /* GLOBAL */
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(99,102,241,0.10), transparent 22%),
            linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        color: #111827;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        max-width: 1280px;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    [data-testid="stSidebar"] button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        background: #ffffff;
        color: #111827;
        font-weight: 600;
        transition: all 0.18s ease;
    }

    [data-testid="stSidebar"] button:hover {
        background: #f3f4f6;
        border-color: #d1d5db;
        transform: translateY(-1px);
    }

    /* HERO */
    .hero {
        background:
            radial-gradient(circle at top left, rgba(99,102,241,0.22), transparent 30%),
            radial-gradient(circle at top right, rgba(16,185,129,0.18), transparent 28%),
            white;
        border: 1px solid #e5e7eb;
        border-radius: 32px;
        padding: 62px;
        box-shadow: 0 24px 90px rgba(15, 23, 42, 0.09);
        animation: fadeIn 0.42s ease-in;
    }

    .hero-label {
        display: inline-block;
        background: #eef2ff;
        color: #4f46e5;
        padding: 7px 13px;
        border-radius: 999px;
        font-size: 0.80rem;
        font-weight: 800;
        margin-bottom: 18px;
        letter-spacing: .02em;
    }

    .hero h1 {
        font-size: 3.4rem;
        line-height: 1.02;
        letter-spacing: -0.055em;
        color: #0f172a;
        margin-bottom: 20px;
    }

    .hero p {
        color: #475569;
        font-size: 1.08rem;
        line-height: 1.75;
        max-width: 850px;
    }

    /* CARDS */
    .card {
        background: rgba(255,255,255,0.94);
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 12px 36px rgba(15, 23, 42, 0.055);
        animation: fadeIn 0.36s ease-in;
    }

    .card-soft {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 22px;
        animation: fadeIn 0.36s ease-in;
    }

    .card-dark {
        background: #0f172a;
        color: white;
        border-radius: 22px;
        padding: 26px;
        box-shadow: 0 22px 52px rgba(15, 23, 42, 0.25);
        animation: fadeIn 0.36s ease-in;
    }

    .section-title {
        color: #64748b;
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
        color: #64748b;
        font-size: 0.92rem;
        margin-top: 8px;
    }

    .feature-title {
        font-weight: 800;
        color: #111827;
        margin-bottom: 8px;
        font-size: 1.02rem;
    }

    .feature-text {
        color: #64748b;
        line-height: 1.6;
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

    .muted {
        color: #64748b;
    }

    .small {
        font-size: .86rem;
    }

    /* INPUTS */
    .stNumberInput input, .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid #e5e7eb !important;
        background: #fafafa !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border-color: #e5e7eb !important;
        background: #fafafa !important;
    }

    .stTextArea textarea {
        border-radius: 12px !important;
        border-color: #e5e7eb !important;
        background: #fafafa !important;
    }

    /* BUTTONS */
    .stButton button {
        border-radius: 13px;
        padding: 0.68rem 1rem;
        font-weight: 800;
        transition: all .18s ease;
    }

    .stButton button:hover {
        transform: translateY(-1px);
    }

    .stDownloadButton button {
        background: #111827;
        color: white;
        border-radius: 13px;
        padding: 0.78rem 1rem;
        font-weight: 800;
    }

    .stDownloadButton button:hover {
        background: #1f2937;
        transform: translateY(-1px);
    }

    /* TABLE */
    [data-testid="stDataFrame"] {
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        overflow: hidden;
    }

    hr {
        border: none;
        height: 1px;
        background: #e5e7eb;
        margin: 1.6rem 0;
    }

    /* ANIMATION */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
    """, unsafe_allow_html=True)
