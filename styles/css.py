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

    </style>
    """, unsafe_allow_html=True)
