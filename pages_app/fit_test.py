import streamlit as st

from components.cards import render_page_header
from services.calculations import compute_fit_score, get_fit_result


def render_fit_test():
    render_page_header(
        "Test rapide d’adéquation",
        "Qualification commerciale en moins de deux minutes pour vérifier si AeroGreen répond à un besoin réel.",
        "Qualification"
    )

    if not st.session_state.workspace_created:
        st.warning("Conseil : crée d’abord un workspace client dans l’accueil. Tu peux quand même continuer.")

    taille = st.selectbox(
        "Taille de l’entreprise",
        ["Moins de 10 salariés", "10 à 50 salariés", "50 à 250 salariés", "Plus de 250 salariés"]
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
        "Demandes RSE déjà reçues de clients / donneurs d’ordre ?",
        ["Oui, régulièrement", "Oui, ponctuellement", "Pas encore, mais c’est probable", "Non"]
    )

    donnees_plm = st.selectbox(
        "Utilisation de données techniques lourdes ?",
        ["Oui, PLM / CAO / données projets importantes", "Oui, mais volume modéré", "Peu", "Non"]
    )

    maturite_rse_initiale = st.selectbox(
        "Niveau actuel de structuration RSE",
        ["Aucune démarche structurée", "Quelques actions isolées", "Démarche en cours", "Démarche déjà avancée"]
    )

    if st.button("Analyser l’adéquation"):
        score = compute_fit_score(taille, secteur, pression_rse, donnees_plm, maturite_rse_initiale)
        label, color = get_fit_result(score)

        st.session_state.fit_score = score
        st.session_state.fit_result = label
        st.session_state.fit_test_done = True
        st.session_state.fit_answers = {
            "taille": taille,
            "secteur": secteur,
            "pression_rse": pression_rse,
            "donnees_plm": donnees_plm,
            "maturite_rse_initiale": maturite_rse_initiale,
        }

        st.markdown(f"""
        <div class='card'>
            <div class='section-title'>Résultat</div>
            <div class='kpi' style='color:{color};'>{score:.0f}%</div>
            <div class='feature-title'>{label}</div>
            <div class='feature-text'>
                Ce score sert à prioriser les prospects et à décider si un diagnostic détaillé a du sens.
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.fit_test_done:
        if st.button("Continuer vers le diagnostic avancé"):
            st.session_state.page = "Diagnostic avancé"
            st.rerun()
