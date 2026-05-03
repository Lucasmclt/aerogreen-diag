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

    [data-testid="stSidebar"] [data-baseweb="radio"] label {
        padding-left: 0 !important;
        margin-left: 0 !important;
        gap: 0 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="radio"] > div {
        margin-left: 0 !important;
        padding-left: 0 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="radio"] p {
        margin: 0 !important;
        padding: 0 !important;
        line-height: 1.2 !important;
    }




    /* TOPBAR */
    .topbar-shell {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 18px;
        background: linear-gradient(180deg, rgba(255,255,255,.92), rgba(248,250,252,.98));
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 18px 22px;
        box-shadow: 0 12px 28px rgba(15,23,42,0.05);
        margin-bottom: 1rem;
        animation: fadeIn .28s ease-in;
    }

    .topbar-breadcrumb {
        color: var(--muted);
        font-size: .82rem;
        font-weight: 700;
        letter-spacing: .02em;
        margin-bottom: 4px;
    }

    .topbar-breadcrumb span {
        color: #cbd5e1;
        margin: 0 5px;
    }

    .topbar-title-row {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
    }

    .topbar-title {
        font-size: 1.2rem;
        font-weight: 900;
        color: var(--text);
        letter-spacing: -0.03em;
    }

    .topbar-right {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
        justify-content: flex-end;
    }

    .topbar-chip {
        display: inline-flex;
        align-items: center;
        padding: 8px 12px;
        border-radius: 999px;
        font-size: .8rem;
        font-weight: 800;
        border: 1px solid transparent;
        white-space: nowrap;
    }

    .topbar-chip.success {
        background: rgba(16,185,129,.10);
        color: #047857;
        border-color: rgba(16,185,129,.18);
    }

    .topbar-chip.warning {
        background: rgba(245,158,11,.12);
        color: #b45309;
        border-color: rgba(245,158,11,.18);
    }

    .topbar-chip.neutral {
        background: rgba(99,102,241,.10);
        color: #4f46e5;
        border-color: rgba(99,102,241,.18);
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


    .hero-animated {
        position: relative;
        overflow: hidden;
    }

    .hero-animated::before,
    .hero-animated::after {
        content: "";
        position: absolute;
        border-radius: 999px;
        filter: blur(2px);
        pointer-events: none;
        opacity: .55;
    }

    .hero-animated::before {
        width: 180px;
        height: 180px;
        right: -30px;
        top: -30px;
        background: radial-gradient(circle, rgba(99,102,241,.25) 0%, rgba(99,102,241,0) 70%);
        animation: floatOrb 8s ease-in-out infinite;
    }

    .hero-animated::after {
        width: 150px;
        height: 150px;
        left: 12%;
        bottom: -50px;
        background: radial-gradient(circle, rgba(16,185,129,.22) 0%, rgba(16,185,129,0) 70%);
        animation: floatOrb 10s ease-in-out infinite reverse;
    }

    .stats-strip {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        margin: 1rem 0 1.25rem;
        animation: fadeIn .5s ease-in;
    }

    .stats-item {
        background: rgba(255,255,255,.86);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 18px 20px;
        box-shadow: var(--shadow);
        transition: transform .18s ease, box-shadow .18s ease;
    }

    .stats-item:hover, .card:hover, .card-soft:hover {
        transform: translateY(-3px);
        box-shadow: 0 18px 34px rgba(15,23,42,.09);
    }

    .stats-value {
        font-size: 1.4rem;
        font-weight: 900;
        color: var(--text);
        letter-spacing: -.03em;
    }

    .stats-label {
        margin-top: 4px;
        color: var(--muted);
        font-size: .9rem;
    }

    .sidebar-mini-status {
        font-size: .82rem;
        font-weight: 700;
        color: var(--muted);
        margin: .1rem 0 .65rem;
    }

    .sidebar-locked {
        color: var(--muted);
        font-size: .82rem;
        line-height: 1.45;
        padding: 10px 2px 12px;
    }

    .sidebar-workspace {
        background: linear-gradient(180deg, rgba(255,255,255,.95), rgba(248,250,252,.92));
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 14px;
        margin-top: .85rem;
        box-shadow: 0 8px 24px rgba(15,23,42,.04);
    }


    /* V6 LANDING */
    .landing-hero {
        position: relative;
        overflow: hidden;
        display: grid;
        grid-template-columns: minmax(0, 1.25fr) minmax(320px, .75fr);
        gap: 32px;
        background:
            radial-gradient(circle at top left, rgba(99,102,241,0.22), transparent 32%),
            radial-gradient(circle at 80% 20%, rgba(16,185,129,0.18), transparent 28%),
            linear-gradient(135deg, rgba(255,255,255,.96), rgba(248,250,252,.92));
        border: 1px solid var(--line);
        border-radius: 34px;
        padding: 64px;
        box-shadow: 0 26px 95px rgba(15, 23, 42, 0.09);
        animation: fadeIn .42s ease-in;
    }

    .landing-hero::before {
        content: "";
        position: absolute;
        width: 360px;
        height: 360px;
        right: -120px;
        top: -120px;
        border-radius: 999px;
        background: radial-gradient(circle, rgba(99,102,241,.18), transparent 65%);
        animation: floatOrb 9s ease-in-out infinite;
    }

    .landing-hero::after {
        content: "";
        position: absolute;
        width: 260px;
        height: 260px;
        left: 35%;
        bottom: -140px;
        border-radius: 999px;
        background: radial-gradient(circle, rgba(16,185,129,.16), transparent 68%);
        animation: floatOrb 11s ease-in-out infinite reverse;
    }

    .hero-content, .hero-visual {
        position: relative;
        z-index: 2;
    }

    .landing-hero h1 {
        font-size: 3.65rem;
        line-height: .98;
        letter-spacing: -.065em;
        margin: 0 0 22px;
        max-width: 780px;
    }

    .landing-hero p {
        font-size: 1.08rem;
        line-height: 1.75;
        color: var(--muted);
        max-width: 760px;
        margin-bottom: 26px;
    }

    .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 18px;
    }

    .hero-action-primary,
    .hero-action-secondary {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        padding: 10px 14px;
        font-size: .86rem;
        font-weight: 850;
    }

    .hero-action-primary {
        background: #0f172a;
        color: white;
    }

    .hero-action-secondary {
        background: rgba(99,102,241,.10);
        color: #4f46e5;
        border: 1px solid rgba(99,102,241,.18);
    }

    .hero-visual {
        min-height: 310px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .score-orb {
        width: 210px;
        height: 210px;
        border-radius: 999px;
        background:
            radial-gradient(circle at 30% 20%, rgba(255,255,255,.96), rgba(255,255,255,.58)),
            linear-gradient(135deg, rgba(99,102,241,.28), rgba(16,185,129,.24));
        border: 1px solid rgba(255,255,255,.75);
        box-shadow: 0 34px 80px rgba(99,102,241,.22);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        animation: floatOrb 7s ease-in-out infinite;
    }

    .score-orb span {
        color: var(--muted);
        font-size: .86rem;
        font-weight: 850;
        text-transform: uppercase;
        letter-spacing: .08em;
    }

    .score-orb strong {
        font-size: 3.4rem;
        line-height: 1;
        letter-spacing: -.08em;
        color: var(--text);
    }

    .mini-card {
        position: absolute;
        background: rgba(255,255,255,.88);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(226,232,240,.85);
        border-radius: 18px;
        padding: 14px 16px;
        box-shadow: 0 20px 50px rgba(15,23,42,.10);
        min-width: 138px;
    }

    .mini-card span {
        display: block;
        color: var(--muted);
        font-size: .76rem;
        font-weight: 750;
    }

    .mini-card strong {
        color: var(--text);
        font-size: 1.35rem;
        letter-spacing: -.04em;
    }

    .floating-card.one {
        top: 22px;
        left: 10px;
        animation: floatCard 8s ease-in-out infinite;
    }

    .floating-card.two {
        right: 0;
        bottom: 36px;
        animation: floatCard 7.5s ease-in-out infinite reverse;
    }

    .floating-card.three {
        left: 24px;
        bottom: 18px;
        animation: floatCard 9s ease-in-out infinite;
    }

    .trust-strip {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        margin: 1rem 0 1.4rem;
    }

    .trust-strip > div {
        background: rgba(255,255,255,.88);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 16px 18px;
        box-shadow: var(--shadow);
        transition: transform .18s ease, box-shadow .18s ease;
    }

    .trust-strip > div:hover {
        transform: translateY(-3px);
        box-shadow: 0 18px 34px rgba(15,23,42,.09);
    }

    .trust-strip strong {
        display: block;
        color: var(--text);
        font-size: 1rem;
        margin-bottom: 4px;
    }

    .trust-strip span {
        color: var(--muted);
        font-size: .9rem;
    }

    .icon-card {
        height: 100%;
        background: rgba(255,255,255,.94);
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 24px;
        box-shadow: var(--shadow);
        transition: transform .18s ease, box-shadow .18s ease;
        animation: fadeIn .34s ease-in;
    }

    .icon-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 18px 42px rgba(15,23,42,.10);
    }

    .icon-bubble {
        width: 44px;
        height: 44px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        margin-bottom: 16px;
        font-weight: 900;
    }

    .timeline {
        background: rgba(255,255,255,.92);
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 24px;
        box-shadow: var(--shadow);
        display: grid;
        grid-template-columns: 1fr 44px 1fr 44px 1fr 44px 1fr;
        gap: 6px;
        align-items: center;
        animation: fadeIn .36s ease-in;
    }

    .timeline-step {
        display: flex;
        gap: 12px;
        align-items: flex-start;
    }

    .timeline-dot {
        width: 34px;
        height: 34px;
        border-radius: 999px;
        background: linear-gradient(135deg, #6366f1, #10b981);
        color: white;
        font-weight: 900;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: 0 10px 22px rgba(99,102,241,.18);
    }

    .timeline-step strong {
        color: var(--text);
    }

    .timeline-step p {
        color: var(--muted);
        margin: 4px 0 0;
        font-size: .9rem;
        line-height: 1.45;
    }

    .timeline-line {
        height: 2px;
        background: linear-gradient(90deg, rgba(99,102,241,.35), rgba(16,185,129,.35));
        border-radius: 999px;
    }

    .pricing-card {
        height: 100%;
        border-radius: 24px;
        padding: 28px;
        border: 1px solid var(--line);
        box-shadow: var(--shadow);
        background: white;
        transition: transform .18s ease, box-shadow .18s ease;
    }

    .pricing-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 18px 42px rgba(15,23,42,.10);
    }

    .pricing-card.pro {
        background:
            radial-gradient(circle at top right, rgba(99,102,241,.18), transparent 35%),
            linear-gradient(180deg, #ffffff, #f8fafc);
        border-color: rgba(99,102,241,.18);
    }

    .pricing-card h3 {
        margin: 0 0 8px;
        font-size: 1.35rem;
    }

    .pricing-card p {
        color: var(--muted);
        line-height: 1.6;
    }

    .pricing-card ul {
        margin: 16px 0 0;
        padding-left: 18px;
        color: var(--text);
        line-height: 1.9;
        font-weight: 650;
    }

    .upgrade-panel {
        min-height: 280px;
        background:
            radial-gradient(circle at top left, rgba(99,102,241,0.22), transparent 40%),
            radial-gradient(circle at bottom right, rgba(16,185,129,0.20), transparent 36%),
            #0f172a;
        color: white;
        border-radius: 26px;
        padding: 30px;
        box-shadow: 0 24px 60px rgba(15,23,42,.25);
        display: flex;
        align-items: flex-end;
    }

    .upgrade-panel h3 {
        color: white;
        margin-bottom: 10px;
    }

    .upgrade-panel p {
        color: #cbd5e1;
        line-height: 1.65;
        margin: 0;
    }

    .sidebar-brand.compact {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 14px;
        border-radius: 18px;
    }

    .brand-mark {
        width: 38px;
        height: 38px;
        border-radius: 14px;
        background: linear-gradient(135deg, rgba(99,102,241,.16), rgba(16,185,129,.14));
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }

    .sidebar-result-card {
        background: rgba(255,255,255,.88);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 14px;
        margin-bottom: .65rem;
        box-shadow: 0 8px 22px rgba(15,23,42,.04);
    }

    .sidebar-result-card span,
    .sidebar-result-card small {
        display: block;
        color: var(--muted);
        font-size: .78rem;
        line-height: 1.35;
    }

    .sidebar-result-card strong {
        display: block;
        font-size: 1.28rem;
        line-height: 1.1;
        margin: 4px 0;
    }


    .uniform-card,
    .icon-card {
        min-height: 210px;
        display: flex;
        flex-direction: column;
    }

    .metric-card {
        min-height: 160px;
        display: flex;
        flex-direction: column;
    }

    .uniform-soft-card {
        min-height: 155px;
        display: flex;
        flex-direction: column;
    }

    .pricing-card {
        min-height: 255px;
        display: flex;
        flex-direction: column;
    }

    .upgrade-panel {
        min-height: 255px;
    }

    .recommendation-card {
        min-height: 190px;
        display: flex;
        flex-direction: column;
    }


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


    .uniform-card,
    .icon-card {
        min-height: 210px;
        display: flex;
        flex-direction: column;
    }

    .metric-card {
        min-height: 160px;
        display: flex;
        flex-direction: column;
    }

    .uniform-soft-card {
        min-height: 155px;
        display: flex;
        flex-direction: column;
    }

    .pricing-card {
        min-height: 255px;
        display: flex;
        flex-direction: column;
    }

    .upgrade-panel {
        min-height: 255px;
    }

    .recommendation-card {
        min-height: 190px;
        display: flex;
        flex-direction: column;
    }

    .stButton button {
        border-radius: 999px;
        padding: 0.72rem 1.08rem;
        font-weight: 800;
        transition: all .18s ease;
        border: 1px solid var(--line);
        background: rgba(255,255,255,.96);
        width: auto;
        box-shadow: 0 8px 22px rgba(15,23,42,.04);
    }

    .stButton button:hover {
        transform: translateY(-1px);
        border-color: rgba(99,102,241,.28);
        box-shadow: 0 14px 28px rgba(99,102,241,.10);
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


    @media (max-width: 980px) {
        .topbar-shell {
            flex-direction: column;
            align-items: flex-start;
        }

        .topbar-right {
            justify-content: flex-start;
        }

        .stats-strip,
        .trust-strip {
            grid-template-columns: 1fr;
        }

        .landing-hero {
            grid-template-columns: 1fr;
            padding: 38px;
        }

        .landing-hero h1 {
            font-size: 2.65rem;
        }

        .hero-visual {
            min-height: 260px;
        }

        .timeline {
            grid-template-columns: 1fr;
        }

        .timeline-line {
            width: 2px;
            height: 22px;
            margin-left: 16px;
        }
    }

    /* ANIMATION */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes floatOrb {
        0% { transform: translateY(0px) translateX(0px); }
        50% { transform: translateY(12px) translateX(-8px); }
        100% { transform: translateY(0px) translateX(0px); }
    }

    @keyframes floatCard {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    /* V8 SIDEBAR NAV BUTTONS */
    .nav-button-wrap {
        margin-bottom: 8px;
    }

    .nav-button-wrap button {
        justify-content: flex-start !important;
        text-align: left !important;
        border-radius: 14px !important;
        padding: 0.62rem 0.78rem !important;
        background: rgba(255,255,255,.86) !important;
        border: 1px solid var(--line) !important;
        box-shadow: none !important;
        color: var(--text) !important;
        font-weight: 750 !important;
        width: 100% !important;
    }

    .nav-button-wrap button:hover {
        background: #f8fafc !important;
        border-color: rgba(99,102,241,.28) !important;
        transform: translateY(-1px);
    }

    .nav-button-wrap.active button {
        background: linear-gradient(180deg, rgba(99,102,241,.12), rgba(99,102,241,.05)) !important;
        border-color: rgba(99,102,241,.34) !important;
        color: #4f46e5 !important;
        box-shadow: 0 8px 18px rgba(99,102,241,.10) !important;
    }

    [data-testid="stSidebar"] .stButton button {
        width: 100% !important;
    }

    /* Homepage CTA: pill, not square */
    .stButton button[kind="secondary"] {
        border-radius: 999px !important;
    }

    
    /* V20 SIDEBAR LOCK + DEEP AUDIT */
    [data-testid="collapsedControl"],
    button[aria-label="Close sidebar"],
    button[aria-label="Open sidebar"],
    button[title="Close sidebar"],
    button[title="Open sidebar"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }

    section[data-testid="stSidebar"] {
        min-width: 320px !important;
        width: 320px !important;
    }

    textarea {
        border-radius: 18px !important;
        border: 1px solid rgba(203,213,225,.9) !important;
        background: rgba(255,255,255,.96) !important;
        box-shadow: 0 8px 22px rgba(15,23,42,.04) !important;
    }

    textarea:focus {
        border-color: rgba(99,102,241,.45) !important;
        box-shadow: 0 0 0 4px rgba(99,102,241,.10) !important;
    }

    
    /* V21 CLEANUP */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarHeader"] button,
    button[aria-label="Close sidebar"],
    button[aria-label="Open sidebar"],
    button[title="Close sidebar"],
    button[title="Open sidebar"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        width: 0 !important;
        height: 0 !important;
    }

    .hero-actions,
    .hero-action-primary,
    .hero-action-secondary {
        display: none !important;
    }

    #home_cta_test,
    #home_cta_pro {
        width: 100%;
    }

    .stButton button[kind="primary"] {
        background: linear-gradient(90deg, #0f172a, #111827) !important;
        color: #ffffff !important;
        border: 1px solid #0f172a !important;
    }

    .stButton button[kind="primary"] *,
    .stButton button[kind="primary"] span,
    .stButton button[kind="primary"] p,
    .stButton button[kind="primary"] div {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    
    /* V22 HERO CTA + DETAILED AUDIT */
    .hero-cta-row {
        display: flex;
        flex-wrap: wrap;
        gap: 14px;
        margin-top: 24px;
        position: relative;
        z-index: 3;
    }

    .hero-cta {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        text-decoration: none !important;
        padding: 15px 22px;
        border-radius: 999px;
        font-weight: 850;
        font-size: .96rem;
        transition: all .18s ease;
        box-shadow: 0 12px 26px rgba(15,23,42,.06);
    }

    .hero-cta.primary {
        background: #0f172a;
        color: #ffffff !important;
        border: 1px solid #0f172a;
    }

    .hero-cta.secondary {
        background: rgba(99,102,241,.08);
        color: #4f46e5 !important;
        border: 1px solid rgba(99,102,241,.22);
    }

    .hero-cta:hover {
        transform: translateY(-1px);
    }

    .stExpander {
        border-radius: 18px !important;
    }

    @media (max-width: 980px) {
        .hero-cta-row {
            flex-direction: column;
        }

        .hero-cta {
            width: 100%;
        }
    }

    
    /* V24 POLISH */
    .bottom-action-card {
        margin-top: 2rem;
        background:
            radial-gradient(circle at top left, rgba(99,102,241,.10), transparent 30%),
            linear-gradient(180deg, rgba(255,255,255,.96), rgba(248,250,252,.98));
        border: 1px solid rgba(226,232,240,.95);
        border-radius: 24px;
        padding: 22px;
        box-shadow: 0 16px 34px rgba(15,23,42,.06);
    }

    .bottom-action-title {
        color: #0f172a;
        font-size: 1.12rem;
        font-weight: 900;
        letter-spacing: -.03em;
        margin-bottom: 5px;
    }

    .bottom-action-sub {
        color: #64748b;
        font-size: .92rem;
        line-height: 1.55;
        margin-bottom: 16px;
    }

    .bottom-action-card .stButton button,
    .bottom-action-card .stDownloadButton button {
        min-height: 54px !important;
        border-radius: 16px !important;
        font-weight: 850 !important;
        width: 100% !important;
    }

    .bottom-action-card .stDownloadButton button,
    .stDownloadButton button {
        background: linear-gradient(90deg, #0f172a, #111827) !important;
        color: #ffffff !important;
        border: 1px solid #0f172a !important;
    }

    .bottom-action-card .stDownloadButton button *,
    .stDownloadButton button *,
    .bottom-action-card .stDownloadButton button span,
    .stDownloadButton button span,
    .bottom-action-card .stDownloadButton button p,
    .stDownloadButton button p {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .recommendation-box {
        background: rgba(255,255,255,.92);
        border: 1px solid rgba(226,232,240,.95);
        border-radius: 20px;
        padding: 18px 22px;
        box-shadow: 0 12px 28px rgba(15,23,42,.05);
        margin-bottom: 1rem;
    }

    .method-note {
        color: #64748b;
        font-size: .9rem;
        line-height: 1.55;
        margin: 1rem 0;
    }

    [data-testid="stMetric"] {
        background: rgba(255,255,255,.92);
        border: 1px solid rgba(226,232,240,.95);
        border-radius: 18px;
        padding: 16px;
        box-shadow: 0 10px 24px rgba(15,23,42,.04);
    }

    
    /* V25 LAYOUT FIXES */
    .sidebar-brand-link,
    .sidebar-brand-link:visited,
    .sidebar-brand-link:hover,
    .sidebar-brand-link:active {
        text-decoration: none !important;
        color: inherit !important;
        display: block;
    }

    .sidebar-brand-link .sidebar-brand {
        cursor: pointer;
        transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease;
    }

    .sidebar-brand-link .sidebar-brand:hover {
        transform: translateY(-1px);
        border-color: rgba(99,102,241,.26);
        box-shadow: 0 12px 26px rgba(99,102,241,.08);
    }

    .report-download-spacer {
        height: 1rem;
    }

    .recommendation-section-spacer {
        height: 1.1rem;
    }

    .report-reco-card {
        margin-bottom: 1rem !important;
    }

    .recommendation-box ul {
        margin: 0;
        padding-left: 1.25rem;
    }

    .recommendation-box li {
        margin: .55rem 0;
        color: #334155;
        line-height: 1.55;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 24px !important;
        border-color: rgba(226,232,240,.95) !important;
        box-shadow: 0 14px 32px rgba(15,23,42,.05);
        background: rgba(255,255,255,.92);
        padding: .35rem;
        margin-top: 1.35rem;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] h3 {
        margin-top: 0 !important;
        margin-bottom: .35rem !important;
    }

    
    /* V26 GLOBAL POLISH */
    .block-container {
        padding-top: 2.6rem !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:
            radial-gradient(circle at top left, rgba(99,102,241,.08), transparent 28%),
            linear-gradient(180deg, rgba(255,255,255,.96), rgba(248,250,252,.98)) !important;
        border-radius: 24px !important;
        border-color: rgba(226,232,240,.95) !important;
        box-shadow: 0 16px 34px rgba(15,23,42,.06) !important;
    }

    .wizard-nav-title {
        font-size: 1.08rem;
        font-weight: 900;
        color: #0f172a;
        letter-spacing: -.03em;
        margin-bottom: 4px;
    }

    .wizard-nav-sub {
        color: #64748b;
        font-size: .92rem;
        line-height: 1.55;
        margin-bottom: 16px;
    }

    .wizard-nav-progress {
        height: 54px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(99,102,241,.08);
        border: 1px solid rgba(99,102,241,.18);
        color: #4f46e5;
        font-weight: 850;
    }

    .score-action-spacer {
        height: 1.5rem;
    }

    .pricing-card .section-title {
        color: #4f46e5;
    }

    
    /* V27 FIXES */
    .block-container {
        padding-top: 4.2rem !important;
    }

    .fit-next-spacer {
        height: 1.2rem;
    }

    .wizard-nav-progress {
        height: 54px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(99,102,241,.08);
        border: 1px solid rgba(99,102,241,.18);
        color: #4f46e5;
        font-weight: 850;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] .stButton button {
        min-height: 54px !important;
        border-radius: 16px !important;
    }

    .landing-hero {
        margin-top: .4rem;
    }

    
    /* V28 AIR + STATE FIXES */
    .button-spacer {
        height: 1rem;
    }

    .section-gap {
        height: 1.15rem;
    }

    .wizard-nav-empty {
        min-height: 54px;
    }

    .wizard-nav-title {
        font-size: 1.08rem;
        font-weight: 900;
        color: #0f172a;
        letter-spacing: -.03em;
        margin-bottom: 4px;
    }

    .wizard-nav-sub {
        color: #64748b;
        font-size: .92rem;
        line-height: 1.55;
        margin-bottom: 16px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        margin-top: 1.35rem !important;
        margin-bottom: 1.35rem !important;
    }

    .progress-card,
    .section-intro-card,
    .card,
    .card-soft {
        margin-bottom: 1rem;
    }

    
    /* V29 PANEL POLISH */
    .framed-panel-header {
        padding: 6px 2px 16px 2px;
    }

    .framed-panel-header strong {
        display: block;
        color: var(--text);
        font-size: 1.02rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 8px;
    }

    .framed-panel-header .feature-text.small {
        color: var(--muted);
        font-size: .95rem;
        line-height: 1.62;
        max-width: 840px;
    }

    .framed-panel-kicker {
        color: #64748b;
        font-size: .88rem;
        font-weight: 900;
        letter-spacing: .12em;
        margin-bottom: 12px;
    }

    .framed-panel-title {
        color: #0f172a;
        font-size: 1.12rem;
        font-weight: 900;
        letter-spacing: -.03em;
        margin-bottom: 8px;
    }

    .framed-panel-sub {
        color: #64748b;
        font-size: .96rem;
        line-height: 1.6;
        margin-bottom: 4px;
        max-width: 760px;
    }

    .wizard-nav-center-spacer {
        min-height: 56px;
        width: 100%;
    }

    /* Bottom action cards aligned with progress-card design */
    .ag-bottom-card-marker {
        display: block;
        width: 100%;
        height: 0;
        overflow: hidden;
    }

    .ag-bottom-card-header {
        padding: 0;
        margin: 0 0 18px 0;
    }

    .ag-bottom-card-header strong {
        display: block;
        color: var(--text);
        font-size: 1.04rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        line-height: 1.25;
        margin-bottom: 8px;
    }

    .ag-bottom-card-header .feature-text.small {
        color: var(--muted);
        font-size: .95rem;
        line-height: 1.62;
        max-width: 840px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-marker) {
        background: linear-gradient(180deg, rgba(248,250,252,.96), rgba(255,255,255,.92)) !important;
        border: 1px solid var(--line) !important;
        border-radius: 18px !important;
        padding: 24px !important;
        box-shadow: 0 8px 20px rgba(15,23,42,.03) !important;
        animation: fadeIn .34s ease-in;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-marker):hover {
        transform: translateY(-3px);
        box-shadow: 0 18px 34px rgba(15,23,42,.09) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-marker) > div {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-marker) [data-testid="stVerticalBlock"] {
        gap: 0.45rem;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-marker) [data-testid="column"] > div {
        height: 100%;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-marker) [data-testid="column"] [data-testid="stVerticalBlock"] {
        height: 100%;
        justify-content: flex-end;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-marker) .stButton,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-marker) .stDownloadButton {
        width: 100%;
        margin-top: 4px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-marker) .stButton button,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-marker) .stDownloadButton button {
        width: 100% !important;
        min-height: 58px !important;
        padding: .95rem 1.15rem !important;
        border-radius: 999px !important;
        font-size: .96rem !important;
        font-weight: 850 !important;
        letter-spacing: -0.01em !important;
        box-shadow: 0 8px 20px rgba(15,23,42,.05) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-marker) .stButton button:hover,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-marker) .stDownloadButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 14px 28px rgba(99,102,241,.10) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-nav) .stButton button {
        background: rgba(255,255,255,.98) !important;
        border: 1px solid var(--line) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-next-steps) .stButton button,
    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-finalize) .stButton button {
        background: rgba(255,255,255,.98) !important;
        border: 1px solid var(--line) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-finalize) .stDownloadButton button {
        background: linear-gradient(90deg, #0f172a, #111827) !important;
        color: #ffffff !important;
        border: 1px solid #0f172a !important;
    }


    /* V39: key-scoped diagnostic navigation card.
       This recreates the progress-card look without selecting the whole form/page. */
    div.st-key-diagnostic_nav_card,
    [class*="st-key-diagnostic_nav_card"] {
        background: linear-gradient(180deg, rgba(248,250,252,.96), rgba(255,255,255,.92)) !important;
        border: 1px solid var(--line) !important;
        border-radius: 20px !important;
        padding: 24px !important;
        box-shadow: 0 14px 36px rgba(15,23,42,.06) !important;
        animation: fadeIn .34s ease-in;
        margin-bottom: 1.15rem !important;
    }

    div.st-key-diagnostic_nav_card:hover,
    [class*="st-key-diagnostic_nav_card"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 18px 34px rgba(15,23,42,.09) !important;
    }

    div.st-key-diagnostic_nav_card [data-testid="stVerticalBlock"],
    [class*="st-key-diagnostic_nav_card"] [data-testid="stVerticalBlock"] {
        gap: 0.45rem;
    }

    div.st-key-diagnostic_nav_card [data-testid="stColumn"] > div,
    [class*="st-key-diagnostic_nav_card"] [data-testid="stColumn"] > div {
        height: 100%;
    }

    div.st-key-diagnostic_nav_card [data-testid="stColumn"] [data-testid="stVerticalBlock"],
    [class*="st-key-diagnostic_nav_card"] [data-testid="stColumn"] [data-testid="stVerticalBlock"] {
        height: 100%;
        justify-content: flex-end;
    }

    div.st-key-diagnostic_nav_card .stButton,
    [class*="st-key-diagnostic_nav_card"] .stButton {
        width: 100%;
        margin-top: 4px;
    }

    div.st-key-diagnostic_nav_card .stButton button,
    [class*="st-key-diagnostic_nav_card"] .stButton button {
        width: 100% !important;
        min-height: 58px !important;
        padding: .95rem 1.15rem !important;
        border-radius: 999px !important;
        font-size: .96rem !important;
        font-weight: 850 !important;
        letter-spacing: -0.01em !important;
        background: rgba(255,255,255,.98) !important;
        border: 1px solid var(--line) !important;
        color: var(--text) !important;
        box-shadow: 0 8px 20px rgba(15,23,42,.05) !important;
    }

    div.st-key-diagnostic_nav_card .stButton button:hover,
    [class*="st-key-diagnostic_nav_card"] .stButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 14px 28px rgba(99,102,241,.10) !important;
    }

    /* Make action buttons in these framed panels match */
    div[data-testid="stVerticalBlockBorderWrapper"] .stButton button,
    div[data-testid="stVerticalBlockBorderWrapper"] .stDownloadButton button {
        border-radius: 999px !important;
        min-height: 56px !important;
        font-weight: 850 !important;
    }

    #wizard_back_btn, #wizard_next_btn, #wizard_score_btn, #deep_save_btn {
        scroll-margin-top: 120px;
    }

    /* Keep download button visually aligned with save button */
    div[data-testid="stVerticalBlockBorderWrapper"] .stDownloadButton button {
        background: linear-gradient(90deg, #0f172a, #111827) !important;
        color: #ffffff !important;
        border: 1px solid #0f172a !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] .stDownloadButton button * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }


    /* V31 STABILITY + BUTTON HARMONY */
    .block-container {
        padding-top: 4.2rem !important;
    }

    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarHeader"] button,
    button[aria-label="Close sidebar"],
    button[aria-label="Open sidebar"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    .stButton button,
    .stDownloadButton button {
        border-radius: 999px !important;
        min-height: 50px !important;
        font-weight: 850 !important;
        letter-spacing: -0.01em !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px !important;
        border-color: var(--line) !important;
        background: var(--panel-soft) !important;
        box-shadow: none !important;
        padding: 8px !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] .stButton button,
    div[data-testid="stVerticalBlockBorderWrapper"] .stDownloadButton button {
        width: 100% !important;
        min-height: 56px !important;
    }

    .report-download-spacer { height: 1.25rem; }
    .recommendation-section-spacer { height: 1.35rem; }
    .report-reco-card { margin-bottom: .95rem; }

    /* V35 GLOBAL UI POLISH */
    .page-header,
    .topbar-shell,
    .sidebar-workspace,
    .icon-card,
    .stats-item,
    .upgrade-panel,
    .pricing-card,
    .timeline-step,
    .card,
    .card-soft,
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
    }

    .page-header,
    .topbar-shell,
    .card,
    .icon-card,
    .stats-item,
    .sidebar-workspace {
        box-shadow: 0 14px 36px rgba(15, 23, 42, 0.06) !important;
    }

    .card,
    .card-soft,
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--line) !important;
    }

    .feature-title,
    .framed-panel-title,
    .ag-bottom-card-header strong {
        letter-spacing: -0.025em !important;
    }

    .feature-text,
    .page-header-sub,
    .framed-panel-sub,
    .ag-bottom-card-header .feature-text.small {
        color: #5b6b80 !important;
    }

    .stButton button,
    .stDownloadButton button {
        border-radius: 999px !important;
        min-height: 52px !important;
        padding: 0.82rem 1.12rem !important;
        font-weight: 850 !important;
        letter-spacing: -0.01em !important;
        transition: all .18s ease !important;
    }

    .stButton button {
        background: rgba(255,255,255,.98) !important;
        border: 1px solid var(--line) !important;
        color: var(--text) !important;
        box-shadow: 0 8px 22px rgba(15,23,42,.04) !important;
    }

    .stButton button:hover,
    .stDownloadButton button:hover {
        transform: translateY(-1px) !important;
    }

    .stButton button[kind="primary"] {
        background: linear-gradient(90deg, #0f172a, #111827) !important;
        color: #ffffff !important;
        border: 1px solid #0f172a !important;
        box-shadow: 0 10px 24px rgba(15,23,42,.10) !important;
    }

    .stButton button[kind="secondary"] {
        background: rgba(255,255,255,.98) !important;
        border: 1px solid var(--line) !important;
        color: var(--text) !important;
    }

    .stDownloadButton button {
        background: linear-gradient(90deg, #0f172a, #111827) !important;
        color: #ffffff !important;
        border: 1px solid #0f172a !important;
        box-shadow: 0 10px 24px rgba(15,23,42,.10) !important;
    }

    .stDownloadButton button *,
    .stButton button[kind="primary"] *,
    .stButton button[kind="primary"] span,
    .stButton button[kind="primary"] p,
    .stButton button[kind="primary"] div {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    div[data-testid="stTextInputRootElement"],
    div[data-testid="stTextArea"] textarea,
    div[data-baseweb="select"] > div,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stNumberInputContainer"],
    div[data-testid="stDateInputField"] {
        border-radius: 16px !important;
    }

    div[data-testid="stTextInputRootElement"],
    div[data-baseweb="select"] > div,
    div[data-testid="stNumberInputContainer"],
    div[data-testid="stDateInputField"],
    .stTextArea textarea {
        border: 1px solid var(--line) !important;
        background: rgba(255,255,255,.96) !important;
        box-shadow: 0 2px 8px rgba(15,23,42,.02) !important;
        transition: border-color .18s ease, box-shadow .18s ease !important;
    }

    div[data-testid="stTextInputRootElement"]:focus-within,
    div[data-baseweb="select"]:focus-within > div,
    div[data-testid="stNumberInputContainer"]:focus-within,
    .stTextArea textarea:focus {
        border-color: rgba(99,102,241,.34) !important;
        box-shadow: 0 0 0 4px rgba(99,102,241,.08) !important;
    }

    .stTextInput label,
    .stSelectbox label,
    .stMultiSelect label,
    .stTextArea label,
    .stNumberInput label {
        font-weight: 700 !important;
        color: var(--text) !important;
    }

    .streamlit-expanderHeader {
        font-weight: 800 !important;
        color: var(--text) !important;
    }

    [data-testid="stExpander"] {
        border: 1px solid var(--line) !important;
        border-radius: 18px !important;
        background: linear-gradient(180deg, rgba(255,255,255,.96), rgba(248,250,252,.92)) !important;
        box-shadow: 0 10px 24px rgba(15,23,42,.04) !important;
        overflow: hidden;
        margin-bottom: 1rem !important;
    }

    [data-testid="stExpander"] details > summary {
        padding-top: .35rem !important;
        padding-bottom: .35rem !important;
    }

    [data-testid="stMetric"] {
        background: rgba(255,255,255,.88);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 16px 18px;
        box-shadow: 0 8px 24px rgba(15,23,42,.04);
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: var(--text) !important;
    }

    hr {
        background: linear-gradient(90deg, transparent, var(--line), transparent) !important;
    }

    @media (max-width: 900px) {
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-marker) {
            padding: 20px !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-marker) .stButton button,
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.ag-bottom-card-marker) .stDownloadButton button {
            min-height: 54px !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)
