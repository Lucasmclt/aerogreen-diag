import streamlit as st

from components.cards import render_page_header, render_icon_card


def render_methodology():
    render_page_header(
        "Méthodologie & limites",
        "Cadre d’utilisation du prototype, limites méthodologiques et apprentissages du projet.",
        "Cadre du démonstrateur"
    )

    st.markdown("""
    <div class='card-soft'>
        <div class='section-title'>Positionnement</div>
        <strong>Projet personnel · Prototype exploratoire · Document de travail</strong>
        <div class='feature-text'>
            AeroGreen Diag est un prototype exploratoire d’outil de diagnostic RSE numérique pour PME industrielles.
            Il aide à structurer une première lecture de maturité numérique responsable, à identifier les preuves à consolider
            et à préparer un échange client, une démarche EcoVadis ou une réflexion REEN.
            <br><br>
            <strong>Document de travail - À consolider avec preuves et référentiels officiels.</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Ce que ce prototype n’est pas")
    c1, c2, c3 = st.columns(3)
    with c1:
        render_icon_card("⚠️", "Pas un audit officiel", "Le projet ne remplace pas un consultant RSE, un audit terrain ou une validation par organisme compétent.", "#f59e0b")
    with c2:
        render_icon_card("📌", "Pas une notation EcoVadis", "Les scores sont indicatifs et ne constituent pas une notation, une médaille ou une reconnaissance EcoVadis.", "#ef4444")
    with c3:
        render_icon_card("🧪", "Hypothèses simplifiées", "Les facteurs d’émission et pondérations servent au démonstrateur et doivent être consolidés avant tout usage externe.", "#6366f1")

    st.markdown("## Ce que ce projet m’a permis de travailler")
    st.markdown("""
    <div class='card'>
        <ul>
            <li>compréhension d’un besoin B2B industriel ;</li>
            <li>design d’un parcours produit complet ;</li>
            <li>scoring multicritère et pondération ;</li>
            <li>manipulation de données et restitution visuelle ;</li>
            <li>génération de rapports PDF ;</li>
            <li>authentification et gestion d’un espace connecté ;</li>
            <li>base SQLite et persistance locale ;</li>
            <li>interface Streamlit avec design cohérent ;</li>
            <li>réflexion RSE, numérique responsable et contexte aéronautique ;</li>
            <li>positionnement marché, limites produit et prudence méthodologique.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Limites du prototype")
    st.markdown("""
    <div class='card-soft'>
        <ul>
            <li>méthodologie non certifiée ;</li>
            <li>absence de validation par un organisme officiel ;</li>
            <li>scoring indicatif ;</li>
            <li>données déclaratives ;</li>
            <li>périmètre carbone simplifié ;</li>
            <li>absence d’audit terrain ;</li>
            <li>absence de garantie réglementaire ;</li>
            <li>preuves à vérifier, dater et aligner avec les référentiels officiels avant usage externe.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Usage recommandé")
    st.info(
        "Utiliser AeroGreen Diag comme support de réflexion, démonstrateur portfolio et base de discussion. "
        "Ne pas l’utiliser comme rapport officiel, certification, preuve réglementaire ou engagement contractuel."
    )
