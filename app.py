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
        # En-tête bleu professionnel
        self.set_fill_color(30, 58, 95)
        self.rect(0, 0, 210, 40, 'F')
        self.set_font('Arial', 'B', 20)
        self.set_text_color(255, 255, 255)
        self.cell(0, 20, 'Rapport de Pre-audit AeroGreen', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, 'Document genere pour auto-evaluation RSE - Base ADEME', 0, 0, 'C')

def create_pdf_bytes(total_tonnes, df_detail, level, maturity_score):
    pdf = AeroGreenPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Section 1 : Score Global
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(44, 82, 130)
    pdf.cell(0, 10, '1. Resultats de l\'Empreinte Carbone Numérique', 0, 1)
    
    pdf.set_font('Arial', '', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f'Empreinte totale calculee : {total_tonnes:.2f} tonnes CO2e', 0, 1)
    pdf.cell(0, 10, f'Niveau de maturite : {level} ({maturity_score:.0f}%)', 0, 1)
    
    # Section 2 : Tableau de détail
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Detail des calculs par poste :', 0, 1)
    
    # Header du tableau
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(60, 10, ' Categorie', 1, 0, 'L', True)
    pdf.cell(60, 10, ' Emissions (kg CO2e)', 1, 0, 'C', True)
    pdf.cell(40, 10, ' Part (%)', 1, 1, 'C', True)
    
    # Lignes du tableau
    pdf.set_font('Arial', '', 10)
    for _, row in df_detail.iterrows():
        pdf.cell(60, 10, f' {row["Catégorie"]}', 1)
        pdf.cell(60, 10, f' {row["Émissions (kg CO₂e)"]}', 1, 0, 'C')
        pdf.cell(40, 10, f' {row["Pourcentage"]}', 1, 1, 'C')

    # Section 3 : Recommandations
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 16)
    pdf.set_text_color(44, 82, 130)
    pdf.cell(0, 10, '2. Recommandations Strategiques', 0, 1)
    
    recos = [
        ("Economie Circulaire", "- Prolonger la duree de vie du materiel\n- Favoriser le reconditionnement\n- Mettre en place une filiere DEEE"),
        ("Optimisation Data", "- Nettoyer les donnees obsoletes\n- Optimiser le stockage PLM\n- Privilegier le stockage mutualise"),
        ("Certification et Engagement", "- Viser la certification ISO 14001\n- Formaliser une charte achats\n- Former les equipes aux enjeux")
    ]
    
    for title, content in recos:
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, title, 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, content)
        
    return pdf.output(dest='S').encode('latin-1', errors='replace')

# --- CSS PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .stApp { background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%); }
    h1 { color: #1e3a5f; font-family: 'Segoe UI', sans-serif; font-weight: 700; text-align: center; padding: 20px; background-color: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
    h2 { color: #2c5282; font-family: 'Segoe UI', sans-serif; font-weight: 600; margin-top: 20px; }
    .metric-card { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

# --- TITRE ---
st.markdown("<h1>✈️ AéroGreen Diag : Pré-audit Carbone Numérique</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #f5f7fa; font-size: 1.1em; margin-bottom: 30px;'>Outil d'auto-diagnostic pour les PME aéronautiques</p>", unsafe_allow_html=True)

# --- FACTEURS ADEME ---
FACTEURS_ADEME = {
    'laptop': 193,
    'station_fixe': 350,
    'ecran': 200,
    'stockage': 0.24  # kg CO2e par To
}

# --- QUESTIONNAIRE ---
st.markdown("## 📊 Questionnaire de diagnostic")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 💻 Inventaire Matériel")
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    nb_laptops = st.number_input("Nombre de Laptops", 0, 10000, 0)
    nb_stations = st.number_input("Nombre de Stations fixes", 0, 10000, 0)
    nb_ecrans = st.number_input("Nombre d'Écrans", 0, 10000, 0)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("### 💾 Stockage de Données")
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    stockage_plm = st.number_input("Volume de données PLM (To)", 0.0, 10000.0, 0.0, step=0.1)
    st.info("📌 PLM : Product Lifecycle Management")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("### 🌱 Maturité Environnementale")
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    iso_14001 = st.checkbox("✓ Certifié ISO 14001")
    gestion_deee = st.checkbox("✓ Gestion DEEE en place")
    charte_achats = st.checkbox("✓ Charte achats responsables")
    st.markdown("</div>", unsafe_allow_html=True)

# --- CALCULS ---
emission_laptops = nb_laptops * FACTEURS_ADEME['laptop']
emission_stations = nb_stations * FACTEURS_ADEME['station_fixe']
emission_ecrans = nb_ecrans * FACTEURS_ADEME['ecran']
emission_stockage = stockage_plm * FACTEURS_ADEME['stockage']

total_emissions_kg = emission_laptops + emission_stations + emission_ecrans + emission_stockage
total_emissions_tonnes = total_emissions_kg / 1000

# Maturité
criteres = [iso_14001, gestion_deee, charte_achats]
maturite_pct = (sum(criteres) / len(criteres)) * 100

# --- RÉSULTATS ---
st.markdown("---")
st.markdown("## 📈 Résultats du Diagnostic")

res_col1, res_col2 = st.columns(2)

with res_col1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("### 🌍 Empreinte Carbone Totale")
    st.markdown(f"<div style='text-align: center;'><h1 style='color: #1e3a5f; font-size: 3.5em;'>{total_emissions_tonnes:.2f}</h1><p>tonnes CO₂e</p></div>", unsafe_allow_html=True)
    
    # Dataframe pour le tableau
    detail_data = {
        'Catégorie': ['Laptops', 'Stations fixes', 'Écrans', 'Stockage PLM'],
        'Émissions (kg CO₂e)': [emission_laptops, emission_stations, emission_ecrans, emission_stockage],
        'Pourcentage': [f"{(x/total_emissions_kg*100):.1f}%" if total_emissions_kg > 0 else "0%" for x in [emission_laptops, emission_stations, emission_ecrans, emission_stockage]]
    }
    df_detail = pd.DataFrame(detail_data)
    st.table(df_detail)
    st.markdown("</div>", unsafe_allow_html=True)

with res_col2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("### 🎯 Jauge Maturité")
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=maturite_pct,
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#1e3a5f"},
               'steps': [{'range': [0, 33], 'color': "#ffcccc"}, {'range': [33, 66], 'color': "#fff3cd"}, {'range': [66, 100], 'color': "#d4edda"}]}
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig, use_container_width=True)
    
    if maturite_pct < 33: level, msg = "🔴 Débutant", "Des efforts importants sont requis."
    elif maturite_pct < 66: level, msg = "🟡 Intermédiaire", "Bonne dynamique, à poursuivre."
    else: level, msg = "🟢 Avancé", "Excellente gestion environnementale !"
    
    st.markdown(f"<div style='text-align: center;'><strong>{level}</strong><br>{msg}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- RECOMMANDATIONS ---
st.markdown("---")
st.markdown("## 💡 Recommandations")
rec1, rec2, rec3 = st.columns(3)

with rec1:
    st.markdown("<div class='metric-card'><h4>🔄 Économie Circulaire</h4><ul><li>Prolonger la durée</li><li>Reconditionné</li><li>Filière DEEE</li></ul></div>", unsafe_allow_html=True)
with rec2:
    st.markdown("<div class='metric-card'><h4>📊 Optimisation Data</h4><ul><li>Nettoyage données</li><li>Compression PLM</li><li>Stockage local</li></ul></div>", unsafe_allow_html=True)
with rec3:
    st.markdown("<div class='metric-card'><h4>🎯 Certification</h4><ul><li>ISO 14001</li><li>Charte Achats</li><li>Eco-conception</li></ul></div>", unsafe_allow_html=True)

# --- BOUTON PDF ---
st.markdown("---")
col_pdf1, col_pdf2, col_pdf3 = st.columns([1,1,1])

with col_pdf2:
    try:
        # On passe le "level" sans l'émoji pour éviter les bugs d'encodage PDF
        pdf_level = level.split(" ")[1] if " " in level else level
        pdf_data = create_pdf_bytes(total_emissions_tonnes, df_detail, pdf_level, maturite_pct)
        
        st.download_button(
            label="📥 Télécharger le Rapport PDF",
            data=pdf_data,
            file_name=f"Rapport_AeroGreen_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Erreur lors de la préparation du PDF : {e}")

# --- FOOTER ---
st.markdown(f"<div style='text-align: center; color: #f5f7fa; padding: 20px;'>AéroGreen Diag v2026 - Source ADEME 2024</div>", unsafe_allow_html=True)
