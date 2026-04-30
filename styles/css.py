import streamlit as st


def load_css():
    st.markdown("""
    <style>
    /* GLOBAL */
    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    [data-testid="stSidebar"] button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        background: #ffffff;
        color: #111827;
        font-weight: 500;
    }

    [data-testid="stSidebar"] button:hover {
        background: #f3f4f6;
        border-color: #d1d5db;
    }

    /* HERO */
    .hero {
        background:
            radial-gradient(circle at top left, rgba(99,102,241,0.18), transparent 30%),
            radial-gradient(circle at top right, rgba(16,185,129,0.16), transparent 28%),
            white;
        border: 1px solid #e5e7eb;
        border-radius: 28px;
        padding: 56px;
        box-shadow: 0 24px 80px rgba(15, 23, 42, 0.08);
        animation: fadeIn 0.45s ease-in;
    }

    .hero-label {
        display: inline-block;
        background: #eef2ff;
        color: #4f46e5;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 18px;
    }

    .hero h1 {
        font-size: 3.2rem;
        line-height: 1.05;
        letter-spacing: -0.04em;
        color: #111827;
        margin-bottom: 18px;
    }

    .hero p {
        color: #4b5563;
        font-size: 1.08rem;
        line-height: 1.7;
        max-width: 780px;
    }

    /* CARDS */
    .card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
        animation: fadeIn 0.4s ease-in;
    }

    .card-soft {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 22px;
        animation: fadeIn 0.4s ease-in;
    }

    .section-title {
        color: #6b7280;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 10px;
    }

    .kpi {
        font-size: 2.3rem;
        font-weight: 700;
        letter-spacing: -0.03em;
    }

    .kpi-sub {
        color: #6b7280;
        font-size: 0.9rem;
    }

    .badge {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 700;
    }

    .feature-title {
        font-weight: 700;
        color: #111827;
        margin-bottom: 6px;
    }

    .feature-text {
        color: #6b7280;
        line-height: 1.55;
    }

    /* INPUTS */
    .stNumberInput input {
        border-radius: 10px !important;
        border: 1px solid #e5e7eb !important;
        background: #fafafa !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        border-radius: 10px !important;
        border-color: #e5e7eb !important;
    }

    /* BUTTONS */
    .stButton button {
        border-radius: 12px;
        padding: 0.65rem 1rem;
        font-weight: 600;
    }

    .stDownloadButton button {
        background: #111827;
        color: white;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        font-weight: 600;
    }

    .stDownloadButton button:hover {
        background: #1f2937;
    }

    /* TABLE */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        overflow: hidden;
    }

    /* ANIMATION */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
    """, unsafe_allow_html=True)
