import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="AéroGreen Diag",
    page_icon="✈️",
    layout="wide"
)

# --- CLASSE PDF (LOGIQUE FPDF) ---
class AeroGreenPDF(FPDF):
    def header(self):
        self.set_fill_color(240, 244, 248)
        self.rect(0, 0, 210, 35, 'F')
        self.set_font('Arial', 'B', 18)
        self.set_text_color(30, 58, 95)
        self.cell(0, 15, 'Rapport de Pre-audit AeroGreen', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Document genere pour auto-evaluation RSE - Base ADEME', 0, 0, 'C')

def create_pdf_bytes(total_tonnes, df_detail, level, maturity_score):
    pdf = AeroGreenPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(44, 82, 130)
    pdf.cell(0, 10, '1. Resultats de l\'Empreinte Carbone', 0, 1)
    
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f'Empreinte totale : {total_tonnes:.2f} tonnes CO2e', 0, 1)
    pdf.cell(0, 8, f'Niveau de maturite : {level} ({maturity_score:.0f}%)', 0, 1)
    
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 11)
    pdf.set_fill_color(245, 245, 245)
    pdf.cell(60, 10, ' Categorie', 1, 0, 'L', True)
    pdf.cell(60, 10, ' Emissions (kg CO2e)', 1, 0, 'C', True)
    pdf.cell(40, 10, ' Part (%)', 1, 1, 'C', True)
    
    pdf.set_font('Arial', '', 10)
    for _, row in df_detail.iterrows():
        pdf.cell(60, 10, f' {row["Catégorie"]}', 1)
        pdf.cell(60, 10, f' {row["Émissions (kg CO₂e)"]}', 1, 0, 'C')
        pdf.cell(40, 10, f' {row["Pourcentage"]}', 1, 1, 'C')

    pdf.ln(10)
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(44, 82, 130)
    pdf.cell(0, 10, '2. Recommandations', 0, 1)
    
    recos = [
        ("Economie Circulaire", "Prolonger la duree de vie, favoriser le reconditionne."),
        ("Optimisation Data", "Nettoyage des serveurs, optimisation des flux PLM."),
        ("Gouvernance", "Certification ISO 14001 et formation des equipes.")
    ]
    for title, content in recos:
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 8, title, 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, content)
        pdf.ln(2)
        
    return pdf.output(dest='S').encode('latin-1', errors='replace')

# --- CSS ÉPURÉ ---
st.markdown("""
<style>

/* Fond global */
.stApp {
    background-color: #f5f5f7;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif;
}

/* Titre principal */
.main-title {
    text-align: center;
    padding: 2rem 1rem;
    margin-bottom: 2rem;
}

.main-title h1 {
    font-size: 2.4rem;
    font-weight: 600;
    color: #1d1d1f;
    margin-bottom: 0.3rem;
}

.main-title p {
    color: #6e6e73;
    font-size: 1rem;
}

/* Cartes style Apple */
.custom-card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 22px;
    border: 1px solid rgba(0,0,0,0.05);
    box-shadow: 0 8px 20px rgba(0,0,0,0.04);
    margin-bottom: 1.5rem;
}

/* Titres sections */
h3 {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: #1d1d1f !important;
    margin-bottom: 1rem !important;
}

/* Texte */
label, p {
    color: #3a3a3c !important;
    font-size: 0.95rem !important;
}

/* Inputs */
.stNumberInput input {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    border: 1px solid #d2d2d7 !important;
    padding: 8px !important;
}

/* Checkbox */
.stCheckbox > label {
    font-size: 0.95rem !important;
}

/* Tableau */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* Bouton */
.stDownloadButton button {
    background-color: #0071e3;
    color: white;
    border-radius: 12px;
    padding: 10px;
    border: none;
    font-weight: 500;
}

.stDownloadButton button:hover {
    background-color: #005bb5;
}

/* Séparateur */
hr {
    border: none;
    height: 1px;
    background: #e5e5ea;
    margin: 2rem 0;
}

</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class='main-title'>
    <h1>AéroGreen Diag</h1>
    <p>Auto-diagnostic carbone pour l'industrie aéronautique</p>
</div>
""", unsafe_allow_html=True)

# --- QUESTIONNAIRE ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='custom-card'><h3>💻 Équipements</h3>", unsafe_allow_html=True)
    nb_laptops = st.number_input("Ordinateurs portables", 0, 5000, 0)
    nb_stations = st.number_input("Stations de travail fixes", 0, 5000, 0)
    nb_ecrans = st.number_input("Écrans externes", 0, 5000, 0)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='custom-card'><h3>💾 Données PLM</h3>", unsafe_allow_html=True)
    stockage_plm = st.number_input("Volume stockage (To)", 0.0, 5000.0, 0.0, help="Données stockées sur serveurs ou cloud")
    st.caption("Le stockage PLM représente souvent le principal levier d’optimisation.")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='custom-card'><h3>🌱 Gouvernance</h3>", unsafe_allow_html=True)
    iso_14001 = st.checkbox("Certification ISO 14001")
    gestion_deee = st.checkbox("Gestion des déchets (DEEE)")
    charte_achats = st.checkbox("Charte achats responsables")
    st.markdown("</div>", unsafe_allow_html=True)

# --- CALCULS ---
FACTEURS = {'laptop': 193, 'fixe': 350, 'ecran': 200, 'stock': 0.24}
em_l = nb_laptops * FACTEURS['laptop']
em_f = nb_stations * FACTEURS['fixe']
em_e = nb_ecrans * FACTEURS['ecran']
em_s = stockage_plm * FACTEURS['stock']

total_kg = em_l + em_f + em_e + em_s
total_t = total_kg / 1000
maturite = (sum([iso_14001, gestion_deee, charte_achats]) / 3) * 100

# --- RÉSULTATS ---
st.markdown("## 📈 Synthèse du pré-audit")
res_col1, res_col2 = st.columns([2, 1])

with res_col1:
    st.markdown("<div class='custom-card'><h3>Détail des émissions</h3>", unsafe_allow_html=True)
    data = {
        'Catégorie': ['Laptops', 'Fixes', 'Écrans', 'Stockage'],
        'Émissions (kg CO₂e)': [em_l, em_f, em_e, em_s],
        'Pourcentage': [f"{(x/total_kg*100):.1f}%" if total_kg > 0 else "0%" for x in [em_l, em_f, em_e, em_s]]
    }
    df_detail = pd.DataFrame(data)
    st.dataframe(df_detail, use_container_width=True, hide_index=True)
    st.markdown(f"**Total estimé : {total_t:.2f} tonnes CO2e**")
    st.markdown("</div>", unsafe_allow_html=True)

with res_col2:
    st.markdown("<div class='custom-card'><h3>Maturité RSE</h3>", unsafe_allow_html=True)
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=maturite,
        gauge={'axis': {'range': [0, 100], 'tickcolor': "#4a5568"},
               'bar': {'color': "#0071e3"},
               'steps': [{'range': [0, 33], 'color': "#fee2e2"}, 
                         {'range': [33, 66], 'color': "#fef3c7"}, 
                         {'range': [66, 100], 'color': "#d1fae5"}]}
    ))
    fig.update_layout(height=180, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- RECOMMANDATIONS ---
st.markdown("### 💡 Recommandations Prioritaires")
r1, r2, r3 = st.columns(3)
with r1:
    st.success("**Matériel** : Étendre la garantie à 5 ans pour réduire l'impact de fabrication.")
with r2:
    st.warning("**Données** : Archiver les projets terminés sur des stockages 'froids' peu énergivores.")
with r3:
    st.info("**Stratégie** : Intégrer des critères environnementaux dans le choix des fournisseurs IT.")

# --- BOUTON GÉNÉRATION PDF ---
st.markdown("---")
c_pdf1, c_pdf2, c_pdf3 = st.columns([1,1,1])
with c_pdf2:
    if total_kg > 0:
        pdf_bytes = create_pdf_bytes(total_t, df_detail, "Diag Effectué", maturite)
        st.download_button(
            label="📄 Télécharger le rapport complet (PDF)",
            data=pdf_bytes,
            file_name=f"AeroGreen_Rapport_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.button("📄 Télécharger le rapport (Veuillez saisir des données)", disabled=True, use_container_width=True)

st.markdown("<p style='text-align: center; color: #a0aec0; font-size: 0.8rem;'>Base de calcul : ADEME 2024 | Version épurée 2.0</p>", unsafe_allow_html=True)
