import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="AeroGreen", layout="wide")

# --- STATE (navigation) ---
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## AeroGreen")
    st.markdown("Carbon intelligence")

    if st.button("Dashboard"):
        st.session_state.page = "Dashboard"
    if st.button("Analysis"):
        st.session_state.page = "Analysis"
    if st.button("Report"):
        st.session_state.page = "Report"

# --- UTILS ---
def get_score_color(score):
    if score < 33:
        return "#ef4444"
    elif score < 66:
        return "#f59e0b"
    else:
        return "#10b981"

# --- CSS ---
st.markdown("""
<style>

/* GLOBAL */
.stApp {
    background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
    font-family: Inter, sans-serif;
}

/* TITLE */
.title {
    font-size: 2.5rem;
    font-weight: 700;
}

/* CARD */
.card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 10px 25px rgba(0,0,0,0.04);
    animation: fadeIn 0.4s ease-in;
}

/* KPI */
.kpi {
    font-size: 2.2rem;
    font-weight: 600;
}

/* ANIMATION */
@keyframes fadeIn {
    from {opacity:0; transform: translateY(10px);}
    to {opacity:1; transform: translateY(0);}
}

</style>
""", unsafe_allow_html=True)

# --- DATA INPUT (global pour toutes pages) ---
st.markdown("<div class='title'>AeroGreen</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    nb_laptops = st.number_input("Laptops", 0, 5000, 0)
    nb_stations = st.number_input("Workstations", 0, 5000, 0)
    nb_ecrans = st.number_input("Displays", 0, 5000, 0)

with col2:
    stockage_plm = st.number_input("Storage (TB)", 0.0, 5000.0, 0.0)

with col3:
    iso_14001 = st.checkbox("ISO 14001")
    gestion_deee = st.checkbox("E-waste")
    charte_achats = st.checkbox("Responsible sourcing")

# --- CALCUL ---
FACTEURS = {'laptop': 193, 'fixe': 350, 'ecran': 200, 'stock': 0.24}

em_l = nb_laptops * FACTEURS['laptop']
em_f = nb_stations * FACTEURS['fixe']
em_e = nb_ecrans * FACTEURS['ecran']
em_s = stockage_plm * FACTEURS['stock']

total_kg = em_l + em_f + em_e + em_s
total_t = total_kg / 1000
maturite = (sum([iso_14001, gestion_deee, charte_achats]) / 3) * 100

color_emissions = get_score_color(100 - maturite)
color_maturity = get_score_color(maturite)

# --- PAGE: DASHBOARD ---
if st.session_state.page == "Dashboard":

    st.markdown("## Overview")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        <div class='card'>
            <div>Total emissions</div>
            <div class='kpi' style='color:{color_emissions}'>{total_t:.2f} tCO₂e</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='card'>
            <div>Maturity</div>
            <div class='kpi' style='color:{color_maturity}'>{maturite:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

# --- PAGE: ANALYSIS ---
elif st.session_state.page == "Analysis":

    st.markdown("## Emissions Breakdown")

    df = pd.DataFrame({
        'Category': ['Laptops', 'Workstations', 'Displays', 'Storage'],
        'Value': [em_l, em_f, em_e, em_s]
    })

    # 🔥 GRAPH PREMIUM
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df['Category'],
        y=df['Value'],
        text=[f"{v:.0f} kg" for v in df['Value']],
        textposition='outside',
        marker=dict(
            color=['#6366f1', '#8b5cf6', '#06b6d4', '#10b981'],
            line=dict(width=0)
        )
    ))

    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f1f5f9"),
        font=dict(size=12)
    )

    st.plotly_chart(fig, use_container_width=True)

# --- PAGE: REPORT ---
elif st.session_state.page == "Report":

    st.markdown("## Insights")

    if maturite < 33:
        txt = "Low maturity → urgent action required"
    elif maturite < 66:
        txt = "Moderate maturity → optimization possible"
    else:
        txt = "Strong maturity → fine tuning"

    st.markdown(f"<div class='card'>{txt}</div>", unsafe_allow_html=True)

    # PDF
    if total_kg > 0:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Emissions: {total_t:.2f} tCO2e", ln=True)
        pdf.cell(0, 10, f"Maturity: {maturite:.0f}%", ln=True)

        pdf_bytes = pdf.output(dest="S").encode("latin-1")

        st.download_button(
            "Download report",
            data=pdf_bytes,
            file_name=f"AeroGreen_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )
