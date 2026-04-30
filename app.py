import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="AeroGreen",
    page_icon="✈️",
    layout="wide"
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "Accueil"

if "fit_test_done" not in st.session_state:
    st.session_state.fit_test_done = False

if "fit_score" not in st.session_state:
    st.session_state.fit_score = 0

if "fit_result" not in st.session_state:
    st.session_state.fit_result = ""

# ---------------------------------------------------------
# UTILS
# ---------------------------------------------------------

def get_score_color(score):
    if score < 33:
        return "#ef4444"
    elif score < 66:
        return "#f59e0b"
    else:
        return "#10b981"


def get_maturity_label(score):
    if score < 33:
        return "Faible"
    elif score < 66:
        return "Intermédiaire"
    return "Avancée"


def get_fit_result(score):
    if score >= 70:
        return "Solution fortement pertinente", "#10b981"
    elif score >= 40:
        return "Solution potentiellement pertinente", "#f59e0b"
    return "Solution non prioritaire à ce stade", "#ef4444"


# ---------------------------------------------------------
# PDF
# ---------------------------------------------------------

class AeroGreenPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 18)
        self.set_text_color(20, 20, 20)
        self.cell(0, 15, "AeroGreen - Rapport de pre-diagnostic", 0, 1, "C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, "Document genere automatiquement - Pre-audit carbone numerique", 0, 0, "C")


def create_pdf_bytes(total_tonnes, df_detail, maturity_score, fit_score, fit_result):
    pdf = AeroGreenPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "1. Synthese", 0, 1)

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Empreinte numerique estimee : {total_tonnes:.2f} tCO2e", 0, 1)
    pdf.cell(0, 8, f"Maturite RSE numerique : {maturity_score:.0f}%", 0, 1)
    pdf.cell(0, 8, f"Score d'adequation AeroGreen : {fit_score:.0f}%", 0, 1)
    pdf.cell(0, 8, f"Conclusion : {fit_result}", 0, 1)

    pdf.ln(8)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "2. Detail des emissions", 0, 1)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(65, 9, "Categorie", 1)
    pdf.cell(65, 9, "Emissions kgCO2e", 1)
    pdf.cell(40, 9, "Part", 1)
    pdf.ln()

    pdf.set_font("Arial", "", 10)
    for _, row in df_detail.iterrows():
        pdf.cell(65, 9, str(row["Catégorie"]), 1)
        pdf.cell(65, 9, str(row["Émissions (kg CO₂e)"]), 1)
        pdf.cell(40, 9, str(row["Part"]), 1)
        pdf.ln()

    pdf.ln(8)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "3. Recommandations prioritaires", 0, 1)

    pdf.set_font("Arial", "", 10)
    recommendations = [
        "Allonger la duree de vie des postes informatiques au-dela de 5 ans.",
        "Mettre en place une politique de gestion DEEE pour le materiel obsolete.",
        "Identifier les donnees PLM dormantes et les basculer vers du stockage froid.",
        "Integrer des criteres RSE dans le choix des fournisseurs IT.",
        "Structurer une premiere feuille de route RSE numerique compatible avec les exigences donneurs d'ordre."
    ]

    for reco in recommendations:
        pdf.multi_cell(0, 6, f"- {reco}")

    return pdf.output(dest="S").encode("latin-1", errors="replace")


# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------

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

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.markdown("## ✈️ AeroGreen")
    st.caption("Pré-audit carbone numérique pour sous-traitants aéronautiques")

    st.divider()

    if st.button("Accueil"):
        st.session_state.page = "Accueil"

    if st.button("Test rapide"):
        st.session_state.page = "Test rapide"

    if st.button("Diagnostic"):
        st.session_state.page = "Diagnostic"

    if st.button("Rapport"):
        st.session_state.page = "Rapport"

    st.divider()

    if st.session_state.fit_test_done:
        result_label, result_color = get_fit_result(st.session_state.fit_score)
        st.markdown(f"""
        <div class='card-soft'>
            <div class='section-title'>Éligibilité</div>
            <div style='font-weight:700; color:{result_color};'>{st.session_state.fit_score:.0f}%</div>
            <div style='font-size:0.85rem; color:#6b7280;'>{result_label}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.caption("Commence par le test rapide pour qualifier l’entreprise.")

# ---------------------------------------------------------
# PAGE 1 - ACCUEIL
# ---------------------------------------------------------

if st.session_state.page == "Accueil":
    st.markdown("""
    <div class='hero'>
        <div class='hero-label'>Aerospace ESG Intelligence</div>
        <h1>Un pré-audit carbone numérique conçu pour les PME aéronautiques.</h1>
        <p>
            AeroGreen aide les sous-traitants aéronautiques de rang 2 et 3 à évaluer rapidement
            leur empreinte carbone numérique : matériel informatique, stockage PLM, gouvernance IT
            et maturité RSE. L’objectif : transformer des exigences complexes en un diagnostic simple,
            actionnable et exploitable auprès des donneurs d’ordre.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Pourquoi AeroGreen ?")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class='card'>
            <div class='feature-title'>Pression donneurs d’ordre</div>
            <div class='feature-text'>
                Airbus, Safran et les grands industriels renforcent leurs attentes RSE dans la chaîne de sous-traitance.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class='card'>
            <div class='feature-title'>Alternative aux audits coûteux</div>
            <div class='feature-text'>
                Les petites structures n’ont pas toujours les moyens de lancer un audit complet avec un cabinet de conseil.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class='card'>
            <div class='feature-title'>Rapport actionnable</div>
            <div class='feature-text'>
                Le service génère un pré-diagnostic clair avec des premières recommandations AMOA simples.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Parcours proposé")

    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown("""
        <div class='card-soft'>
            <div class='section-title'>Étape 1</div>
            <strong>Test rapide</strong>
            <p class='feature-text'>Qualification de l’entreprise en quelques questions.</p>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown("""
        <div class='card-soft'>
            <div class='section-title'>Étape 2</div>
            <strong>Pré-diagnostic</strong>
            <p class='feature-text'>Estimation carbone numérique sur les principaux postes.</p>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown("""
        <div class='card-soft'>
            <div class='section-title'>Étape 3</div>
            <strong>Rapport PDF</strong>
            <p class='feature-text'>Synthèse exportable avec recommandations prioritaires.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    if st.button("Lancer le test rapide"):
        st.session_state.page = "Test rapide"
        st.rerun()

# ---------------------------------------------------------
# PAGE 2 - TEST RAPIDE
# ---------------------------------------------------------

elif st.session_state.page == "Test rapide":
    st.markdown("## Test rapide d’adéquation")
    st.caption("Objectif : déterminer si AeroGreen est pertinent pour l’entreprise avant de lancer un diagnostic plus complet.")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    taille = st.selectbox(
        "Taille de l’entreprise",
        [
            "Moins de 10 salariés",
            "10 à 50 salariés",
            "50 à 250 salariés",
            "Plus de 250 salariés"
        ]
    )

    secteur = st.selectbox(
        "Lien avec l’aéronautique",
        [
            "Sous-traitant aéronautique rang 2 ou 3",
            "Fournisseur industriel hors aéronautique",
            "Bureau d’études / ingénierie",
            "Entreprise sans lien direct"
        ]
    )

    pression_rse = st.selectbox(
        "Avez-vous déjà reçu des demandes RSE de clients ou donneurs d’ordre ?",
        [
            "Oui, régulièrement",
            "Oui, ponctuellement",
            "Pas encore, mais c’est probable",
            "Non"
        ]
    )

    donnees_plm = st.selectbox(
        "Votre activité utilise-t-elle des données techniques lourdes ?",
        [
            "Oui, PLM / CAO / données projets importantes",
            "Oui, mais volume modéré",
            "Peu",
            "Non"
        ]
    )

    maturite_rse_initiale = st.selectbox(
        "Niveau actuel de structuration RSE",
        [
            "Aucune démarche structurée",
            "Quelques actions isolées",
            "Démarche en cours",
            "Démarche déjà avancée"
        ]
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Analyser l’adéquation"):
        score = 0

        if taille == "10 à 50 salariés":
            score += 20
        elif taille == "50 à 250 salariés":
            score += 25
        elif taille == "Moins de 10 salariés":
            score += 10
        else:
            score += 12

        if secteur == "Sous-traitant aéronautique rang 2 ou 3":
            score += 30
        elif secteur == "Bureau d’études / ingénierie":
            score += 22
        elif secteur == "Fournisseur industriel hors aéronautique":
            score += 12

        if pression_rse == "Oui, régulièrement":
            score += 25
        elif pression_rse == "Oui, ponctuellement":
            score += 18
        elif pression_rse == "Pas encore, mais c’est probable":
            score += 12

        if donnees_plm == "Oui, PLM / CAO / données projets importantes":
            score += 15
        elif donnees_plm == "Oui, mais volume modéré":
            score += 10
        elif donnees_plm == "Peu":
            score += 4

        if maturite_rse_initiale == "Aucune démarche structurée":
            score += 10
        elif maturite_rse_initiale == "Quelques actions isolées":
            score += 8
        elif maturite_rse_initiale == "Démarche en cours":
            score += 5

        score = min(score, 100)

        st.session_state.fit_score = score
        st.session_state.fit_test_done = True

        label, color = get_fit_result(score)
        st.session_state.fit_result = label

        st.markdown(f"""
        <div class='card'>
            <div class='section-title'>Résultat du test</div>
            <div class='kpi' style='color:{color};'>{score:.0f}%</div>
            <div style='font-weight:700; margin-bottom:8px;'>{label}</div>
            <div class='feature-text'>
                Ce score indique le niveau de pertinence d’un pré-diagnostic carbone numérique pour cette entreprise.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if score >= 70:
            st.success("AeroGreen est très pertinent pour ce profil. Le diagnostic peut apporter une vraie valeur commerciale et opérationnelle.")
        elif score >= 40:
            st.warning("AeroGreen peut être utile, mais il faut préciser les attentes client et le niveau réel de données disponibles.")
        else:
            st.error("AeroGreen n’est probablement pas prioritaire pour cette entreprise à ce stade.")

    if st.session_state.fit_test_done:
        if st.button("Passer au diagnostic"):
            st.session_state.page = "Diagnostic"
            st.rerun()

# ---------------------------------------------------------
# PAGE 3 - DIAGNOSTIC
# ---------------------------------------------------------

elif st.session_state.page == "Diagnostic":
    st.markdown("## Pré-diagnostic carbone numérique")
    st.caption("Version simplifiée. Cette étape pourra ensuite devenir un questionnaire avancé par lots : matériel, cloud, PLM, code, achats IT, conformité RSE.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='card-soft'>
            <div class='section-title'>Infrastructure</div>
            <strong>Parc informatique</strong>
        </div>
        """, unsafe_allow_html=True)

        nb_laptops = st.number_input("Ordinateurs portables", 0, 5000, 0)
        nb_stations = st.number_input("Stations de travail fixes", 0, 5000, 0)
        nb_ecrans = st.number_input("Écrans externes", 0, 5000, 0)

    with col2:
        st.markdown("""
        <div class='card-soft'>
            <div class='section-title'>Données</div>
            <strong>Stockage technique</strong>
        </div>
        """, unsafe_allow_html=True)

        stockage_plm = st.number_input("Volume PLM / CAO stocké (To)", 0.0, 5000.0, 0.0)
        st.caption("Inclure serveurs internes, cloud, données projets et archives actives.")

    with col3:
        st.markdown("""
        <div class='card-soft'>
            <div class='section-title'>Gouvernance</div>
            <strong>Maturité RSE numérique</strong>
        </div>
        """, unsafe_allow_html=True)

        iso_14001 = st.checkbox("Certification ISO 14001")
        gestion_deee = st.checkbox("Gestion DEEE formalisée")
        charte_achats = st.checkbox("Charte achats responsables IT")

    FACTEURS = {
        "laptop": 193,
        "fixe": 350,
        "ecran": 200,
        "stock": 0.24
    }

    em_l = nb_laptops * FACTEURS["laptop"]
    em_f = nb_stations * FACTEURS["fixe"]
    em_e = nb_ecrans * FACTEURS["ecran"]
    em_s = stockage_plm * FACTEURS["stock"]

    total_kg = em_l + em_f + em_e + em_s
    total_t = total_kg / 1000

    maturity = (sum([iso_14001, gestion_deee, charte_achats]) / 3) * 100

    maturity_color = get_score_color(maturity)

    if total_kg == 0:
        emissions_color = "#6b7280"
    elif total_t < 10:
        emissions_color = "#10b981"
    elif total_t < 50:
        emissions_color = "#f59e0b"
    else:
        emissions_color = "#ef4444"

    st.markdown("## Synthèse")

    k1, k2, k3 = st.columns(3)

    with k1:
        st.markdown(f"""
        <div class='card'>
            <div class='section-title'>Empreinte estimée</div>
            <div class='kpi' style='color:{emissions_color};'>{total_t:.2f} tCO₂e</div>
            <div class='kpi-sub'>Émissions numériques estimées</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class='card'>
            <div class='section-title'>Maturité RSE</div>
            <div class='kpi' style='color:{maturity_color};'>{maturity:.0f}%</div>
            <div class='kpi-sub'>{get_maturity_label(maturity)}</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        fit_score = st.session_state.fit_score if st.session_state.fit_test_done else 0
        fit_label, fit_color = get_fit_result(fit_score)
        st.markdown(f"""
        <div class='card'>
            <div class='section-title'>Adéquation service</div>
            <div class='kpi' style='color:{fit_color};'>{fit_score:.0f}%</div>
            <div class='kpi-sub'>{fit_label}</div>
        </div>
        """, unsafe_allow_html=True)

    df = pd.DataFrame({
        "Catégorie": ["Ordinateurs portables", "Stations fixes", "Écrans", "Stockage PLM"],
        "Émissions (kg CO₂e)": [em_l, em_f, em_e, em_s]
    })

    if total_kg > 0:
        df["Part"] = df["Émissions (kg CO₂e)"].apply(lambda x: f"{(x / total_kg) * 100:.1f}%")
    else:
        df["Part"] = "0%"

    st.markdown("## Répartition des émissions")

    chart_df = df.copy()

    fig = go.Figure()

    colors = ["#6366f1", "#8b5cf6", "#06b6d4", "#10b981"]

    fig.add_trace(go.Bar(
        x=chart_df["Catégorie"],
        y=chart_df["Émissions (kg CO₂e)"],
        text=[f"{v:.0f} kg" for v in chart_df["Émissions (kg CO₂e)"]],
        textposition="outside",
        marker=dict(
            color=colors,
            line=dict(width=0)
        ),
        hovertemplate="<b>%{x}</b><br>%{y:.2f} kg CO₂e<extra></extra>"
    ))

    fig.update_layout(
        height=420,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=13, color="#111827"),
        xaxis=dict(showgrid=False, title=""),
        yaxis=dict(showgrid=True, gridcolor="#eef2f7", title="kg CO₂e"),
        bargap=0.35
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("## Premières recommandations")

    reco1, reco2, reco3 = st.columns(3)

    with reco1:
        st.markdown("""
        <div class='card'>
            <div class='section-title'>Matériel</div>
            <strong>Allonger le cycle de vie</strong>
            <p class='feature-text'>
                Prioriser la réparation, le reconditionné et l’extension de garantie sur les équipements critiques.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with reco2:
        st.markdown("""
        <div class='card'>
            <div class='section-title'>Données</div>
            <strong>Réduire le stockage actif</strong>
            <p class='feature-text'>
                Identifier les projets terminés et transférer les archives vers du stockage froid moins énergivore.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with reco3:
        st.markdown("""
        <div class='card'>
            <div class='section-title'>Gouvernance</div>
            <strong>Structurer la preuve RSE</strong>
            <p class='feature-text'>
                Formaliser une politique DEEE, une charte achats IT et des indicateurs simples de suivi.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.session_state["last_total_t"] = total_t
    st.session_state["last_df"] = df
    st.session_state["last_maturity"] = maturity

# ---------------------------------------------------------
# PAGE 4 - RAPPORT
# ---------------------------------------------------------

elif st.session_state.page == "Rapport":
    st.markdown("## Rapport de pré-audit")

    if "last_total_t" not in st.session_state:
        st.warning("Aucun diagnostic n’a encore été généré. Lance d’abord le pré-diagnostic.")
    else:
        total_t = st.session_state["last_total_t"]
        df = st.session_state["last_df"]
        maturity = st.session_state["last_maturity"]
        fit_score = st.session_state.fit_score
        fit_result = st.session_state.fit_result if st.session_state.fit_result else "Test rapide non realise"

        label, color = get_fit_result(fit_score)

        st.markdown(f"""
        <div class='card'>
            <div class='section-title'>Synthèse exportable</div>
            <div style='font-size:1.1rem; font-weight:700;'>Empreinte estimée : {total_t:.2f} tCO₂e</div>
            <div style='font-size:1.1rem; font-weight:700;'>Maturité RSE numérique : {maturity:.0f}%</div>
            <div style='font-size:1.1rem; font-weight:700; color:{color};'>Adéquation AeroGreen : {fit_score:.0f}% — {label}</div>
            <p class='feature-text'>
                Ce rapport constitue une base de discussion. Il ne remplace pas un audit réglementaire complet,
                mais permet d’identifier rapidement les principaux leviers d’action.
            </p>
        </div>
        """, unsafe_allow_html=True)

        pdf_bytes = create_pdf_bytes(
            total_tonnes=total_t,
            df_detail=df,
            maturity_score=maturity,
            fit_score=fit_score,
            fit_result=fit_result
        )

        st.download_button(
            label="Télécharger le rapport PDF",
            data=pdf_bytes,
            file_name=f"AeroGreen_PreAudit_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
