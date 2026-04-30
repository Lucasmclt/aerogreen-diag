import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime

# --- CONFIG PAGE ---
st.set_page_config(
    page_title="AeroGreen",
    layout="wide"
)

# --- PDF ---
class AeroGreenPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 18)
        self.cell(0, 15, 'AeroGreen Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Auto-generated sustainability report', 0, 0, 'C')

def create_pdf_bytes(total_tonnes, df_detail, maturity):
    pdf = AeroGreenPDF()
    pdf.add_page()

    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Total emissions: {total_tonnes:.2f} tCO2e', 0, 1)
    pdf.cell(0, 10, f'Maturity score: {maturity:.0f}%', 0, 1)

    pdf.ln(5)

    for _, row in df_detail.iterrows():
        pdf.cell(0, 8, f"{row['Catégorie']} - {row['Émissions (kg CO₂e)']} kg", 0, 1)

    return pdf.output(dest='S').encode('latin-1', errors='replace')

# --- CSS PREMIUM ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #f7f8fa 0%, #ffffff 100%);
    font-family: Inter, -apple-system, sans-serif;
}

.main-title {
    text-align: center;
    padding: 3rem 1rem 2rem;
}

.main-title h1 {
    font-size: 2.8rem;
    font-weight: 700;
}

.main-title p {
    color: #6b7280;
}

.card {
    background: white;
    border-radius: 18px;
    padding: 24px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 10px 30px rgba(0,0,0,0.04);
    margin-bottom: 1.5rem;
}

.section-title {
    font-size: 0.9rem;
    color: #6b7280;
    margin-bottom: 10px;
    text-transform: uppercase;
}

.kpi {
    font-size: 2.2rem;
    font-weight: 600;
}

.kpi-sub {
    color: #6b7280;
}

.stDownloadButton button {
    background: black;
    color: white;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class='main-title'>
    <h1>AeroGreen</h1>
    <p>Carbon intelligence for aerospace infrastructure</p>
</div>
""", unsafe_allow_html=True)

# --- INPUTS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Infrastructure</div>", unsafe_allow_html=True)
    nb_laptops = st.number_input("Laptops", 0, 5000, 0)
    nb_stations = st.number_input("Workstations", 0, 5000, 0)
    nb_ecrans = st.number_input("Displays", 0, 5000, 0)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Data</div>", unsafe_allow_html=True)
    stockage_plm = st.number_input("Storage (TB)", 0.0, 5000.0, 0.0)
    st.caption("Main emissions driver")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Governance</div>", unsafe_allow_html=True)
    iso_14001 = st.checkbox("ISO 14001")
    gestion_deee = st.checkbox("E-waste")
    charte_achats = st.checkbox("Responsible sourcing")
    st.markdown("</div>", unsafe_allow_html=True)

# --- CALCUL ---
FACTEURS = {'laptop': 193, 'fixe': 350, 'ecran': 200, 'stock': 0.24}

em_l = nb_laptops * FACTEURS['laptop']
em_f = nb_stations * FACTEURS['fixe']
em_e = nb_ecrans * FACTEURS['ecran']
em_s = stockage_plm * FACTEURS['stock']

total_kg = em_l + em_f + em_e + em_s
total_t = total_kg / 1000

maturite = (sum([iso_14001, gestion_deee, charte_achats]) / 3) * 100

# --- KPI ---
st.markdown("## Overview")
k1, k2 = st.columns(2)

with k1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Total emissions</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='kpi'>{total_t:.2f} tCO₂e</div>", unsafe_allow_html=True)
    st.markdown("<div class='kpi-sub'>Annual estimate</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with k2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Maturity</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='kpi'>{maturite:.0f}%</div>", unsafe_allow_html=True)
    st.markdown("<div class='kpi-sub'>Governance score</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- DATA ---
data = {
    'Catégorie': ['Laptops', 'Fixes', 'Écrans', 'Stockage'],
    'Émissions (kg CO₂e)': [em_l, em_f, em_e, em_s],
}

df = pd.DataFrame(data)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- RECO ---
st.markdown("## Insights")

st.markdown("""
<div class='card'>
<p><strong>Hardware</strong><br>Extend lifespan beyond 5 years.</p>
<p><strong>Data</strong><br>Move inactive data to cold storage.</p>
<p><strong>Strategy</strong><br>Integrate sustainability into procurement.</p>
</div>
""", unsafe_allow_html=True)

# --- PDF ---
st.markdown("---")

if total_kg > 0:
    pdf_bytes = create_pdf_bytes(total_t, df, maturite)
    st.download_button(
        "Download report",
        data=pdf_bytes,
        file_name=f"AeroGreen_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
