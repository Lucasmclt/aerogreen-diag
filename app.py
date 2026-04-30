import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(
    page_title="AéroGreen Diag",
    page_icon="✈️",
    layout="wide"
)

# CSS personnalisé pour le thème professionnel
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stApp {
        background: linear-gradient(135deg, #1e3a5f 0%, #2c5282 100%);
    }
    h1 {
        color: #1e3a5f;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
        text-align: center;
        padding: 20px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h2 {
        color: #2c5282;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
    .stNumberInput > div > div > input {
        border: 2px solid #cbd5e0;
        border-radius: 5px;
    }
    .stCheckbox > label {
        color: #2d3748;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown("<h1>✈️ AéroGreen Diag : Pré-audit Carbone Numérique</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4a5568; font-size: 1.1em; margin-bottom: 30px;'>Outil d'auto-diagnostic pour les PME aéronautiques</p>", unsafe_allow_html=True)

# Facteurs d'émission ADEME (en kg CO2e)
FACTEURS_ADEME = {
    'laptop': 193,
    'station_fixe': 350,
    'ecran': 200,
    'stockage': 0.24  # kg CO2e par To
}

# Création des colonnes pour le questionnaire
st.markdown("## 📊 Questionnaire de diagnostic")
st.markdown("---")

col1, col2, col3 = st.columns(3)

# Colonne 1 : Inventaire
with col1:
    st.markdown("### 💻 Inventaire Matériel")
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    
    nb_laptops = st.number_input(
        "Nombre de Laptops",
        min_value=0,
        max_value=10000,
        value=0,
        step=1,
        help="Nombre total d'ordinateurs portables"
    )
    
    nb_stations = st.number_input(
        "Nombre de Stations fixes",
        min_value=0,
        max_value=10000,
        value=0,
        step=1,
        help="Nombre total de stations de travail fixes"
    )
    
    nb_ecrans = st.number_input(
        "Nombre d'Écrans",
        min_value=0,
        max_value=10000,
        value=0,
        step=1,
        help="Nombre total d'écrans externes"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

# Colonne 2 : Stockage
with col2:
    st.markdown("### 💾 Stockage de Données")
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    
    stockage_plm = st.number_input(
        "Volume de données PLM (To)",
        min_value=0.0,
        max_value=10000.0,
        value=0.0,
        step=0.1,
        help="Volume total de données PLM stockées en téraoctets"
    )
    
    st.info("📌 PLM : Product Lifecycle Management")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Colonne 3 : Maturité
with col3:
    st.markdown("### 🌱 Maturité Environnementale")
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    
    iso_14001 = st.checkbox(
        "✓ Certifié ISO 14001",
        help="Certification du système de management environnemental"
    )
    
    gestion_deee = st.checkbox(
        "✓ Gestion DEEE en place",
        help="Déchets d'Équipements Électriques et Électroniques"
    )
    
    charte_achats = st.checkbox(
        "✓ Charte achats responsables",
        help="Politique d'achats durables formalisée"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

# Calcul des émissions
st.markdown("---")
st.markdown("## 📈 Résultats du Diagnostic")

# Calculs
emission_laptops = nb_laptops * FACTEURS_ADEME['laptop']
emission_stations = nb_stations * FACTEURS_ADEME['station_fixe']
emission_ecrans = nb_ecrans * FACTEURS_ADEME['ecran']
emission_stockage = stockage_plm * FACTEURS_ADEME['stockage']

total_emissions_kg = emission_laptops + emission_stations + emission_ecrans + emission_stockage
total_emissions_tonnes = total_emissions_kg / 1000

# Calcul de la maturité (en pourcentage)
criteres_maturite = [iso_14001, gestion_deee, charte_achats]
maturite_pct = (sum(criteres_maturite) / len(criteres_maturite)) * 100

# Affichage des résultats
result_col1, result_col2 = st.columns(2)

with result_col1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("### 🌍 Empreinte Carbone Numérique Totale")
    
    # Affichage du score total
    st.markdown(f"""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #1e3a5f; font-size: 3.5em; margin: 0;'>{total_emissions_tonnes:.2f}</h1>
            <p style='color: #4a5568; font-size: 1.5em; margin-top: 0;'>tonnes CO₂e</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Détail des émissions
    st.markdown("#### Détail par catégorie :")
    
    detail_data = {
        'Catégorie': ['Laptops', 'Stations fixes', 'Écrans', 'Stockage PLM'],
        'Émissions (kg CO₂e)': [
            emission_laptops,
            emission_stations,
            emission_ecrans,
            emission_stockage
        ],
        'Pourcentage': [
            (emission_laptops / total_emissions_kg * 100) if total_emissions_kg > 0 else 0,
            (emission_stations / total_emissions_kg * 100) if total_emissions_kg > 0 else 0,
            (emission_ecrans / total_emissions_kg * 100) if total_emissions_kg > 0 else 0,
            (emission_stockage / total_emissions_kg * 100) if total_emissions_kg > 0 else 0
        ]
    }
    
    df_detail = pd.DataFrame(detail_data)
    df_detail['Émissions (kg CO₂e)'] = df_detail['Émissions (kg CO₂e)'].round(2)
    df_detail['Pourcentage'] = df_detail['Pourcentage'].round(1).astype(str) + ' %'
    
    st.dataframe(df_detail, hide_index=True, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with result_col2:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown("### 🎯 Jauge Maturité EcoVadis")
    
    # Création de la jauge avec Plotly
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=maturite_pct,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Score de Maturité", 'font': {'size': 24, 'color': '#1e3a5f'}},
        number={'suffix': "%", 'font': {'size': 48, 'color': '#1e3a5f'}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#2c5282"},
            'bar': {'color': "#1e3a5f"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#cbd5e0",
            'steps': [
                {'range': [0, 33], 'color': '#fed7d7'},
                {'range': [33, 66], 'color': '#feebc8'},
                {'range': [66, 100], 'color': '#c6f6d5'}
            ],
            'threshold': {
                'line': {'color': "#2c5282", 'width': 4},
                'thickness': 0.75,
                'value': maturite_pct
            }
        }
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="white",
        font={'color': "#2d3748", 'family': "Segoe UI"}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Interprétation du score
    if maturite_pct < 33:
        niveau = "🔴 Débutant"
        message = "Des améliorations significatives sont recommandées."
    elif maturite_pct < 66:
        niveau = "🟡 Intermédiaire"
        message = "Bonne base, continuez vos efforts !"
    else:
        niveau = "🟢 Avancé"
        message = "Excellente maturité environnementale !"
    
    st.markdown(f"""
        <div style='text-align: center; padding: 15px; background-color: #f7fafc; border-radius: 5px; margin-top: 10px;'>
            <p style='font-size: 1.2em; font-weight: 600; color: #2c5282; margin: 0;'>{niveau}</p>
            <p style='color: #4a5568; margin-top: 5px;'>{message}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Recommandations
st.markdown("---")
st.markdown("## 💡 Recommandations")

reco_col1, reco_col2, reco_col3 = st.columns(3)

with reco_col1:
    st.markdown("""
        <div class='metric-card'>
            <h4 style='color: #2c5282;'>🔄 Économie Circulaire</h4>
            <ul style='color: #4a5568;'>
                <li>Prolonger la durée de vie du matériel</li>
                <li>Favoriser le reconditionnement</li>
                <li>Mettre en place une filière DEEE</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with reco_col2:
    st.markdown("""
        <div class='metric-card'>
            <h4 style='color: #2c5282;'>📊 Optimisation Data</h4>
            <ul style='color: #4a5568;'>
                <li>Nettoyer les données obsolètes</li>
                <li>Optimiser le stockage PLM</li>
                <li>Privilégier le stockage mutualisé</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with reco_col3:
    st.markdown("""
        <div class='metric-card'>
            <h4 style='color: #2c5282;'>🎯 Certification</h4>
            <ul style='color: #4a5568;'>
                <li>Viser la certification ISO 14001</li>
                <li>Formaliser une charte achats</li>
                <li>Former les équipes aux enjeux</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #718096; padding: 20px;'>
        <p><strong>AéroGreen Diag</strong> - Outil de diagnostic carbone numérique pour PME aéronautiques</p>
        <p style='font-size: 0.9em;'>Facteurs d'émission basés sur les données ADEME 2024</p>
    </div>
""", unsafe_allow_html=True)
