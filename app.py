import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# --- CONFIG PAGE ---
st.set_page_config(page_title="AeroGreen", layout="wide")

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

# --- SCORE COLOR ---
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
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 20px rgba(0,0,0,0.04);
    margin-bottom: 1.5rem;
}

.section-title {
    font-size: 0.8rem;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 10px;
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
    st.caption("Primary emissions driver")
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

color_emissions = get_score_color(100 - min(maturite, 100))
color_maturity = get_score_color(maturite)

# --- KPI ---
st.markdown("## Overview")

k1, k2 = st.columns(2)

with k1:
    st.markdown(f"""
    <div class='card'>
        <div class='section-title'>Total emissions</div>
        <div class='kpi' style='color:{color_emissions}'>{total_t:.2f} tCO₂e</div>
        <div class='kpi-sub'>Lower is better</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class='card'>
        <div class='section-title'>Maturity</div>
        <div class='kpi' style='color:{color_maturity}'>{maturite:.0f}%</div>
        <div class='kpi-sub'>Higher is better</div>
    </div>
    """, unsafe_allow_html=True)

# --- DATA ---
data = {
    'Catégorie': ['Laptops', 'Fixes', 'Écrans', 'Stockage'],
    'Émissions (kg CO₂e)': [em_l, em_f, em_e, em_s],
}

df = pd.DataFrame(data)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- BAR CHART ---
if total_kg > 0:
    df['%'] = df['Émissions (kg CO₂e)'] / total_kg
    st.bar_chart(df.set_index('Catégorie')['%'])

# --- INSIGHTS ---
st.markdown("## Insights")

if maturite < 33:
    reco = "Low maturity. Immediate governance improvements required."
elif maturite < 66:
    reco = "Moderate maturity. Optimization opportunities available."
else:
    reco = "Strong maturity. Focus on fine-tuning."

st.markdown(f"""
<div class='card'>
<p>{reco}</p>
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
