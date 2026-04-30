import streamlit as st

from components.cards import render_feature_card, render_soft_step_card


def render_home():
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
        render_feature_card(
            "Pression donneurs d’ordre",
            "Airbus, Safran et les grands industriels renforcent leurs attentes RSE dans la chaîne de sous-traitance."
        )

    with c2:
        render_feature_card(
            "Alternative aux audits coûteux",
            "Les petites structures n’ont pas toujours les moyens de lancer un audit complet avec un cabinet de conseil."
        )

    with c3:
        render_feature_card(
            "Rapport actionnable",
            "Le service génère un pré-diagnostic clair avec des premières recommandations AMOA simples."
        )

    st.markdown("### Parcours proposé")

    p1, p2, p3 = st.columns(3)

    with p1:
        render_soft_step_card(
            "Étape 1",
            "Test rapide",
            "Qualification de l’entreprise en quelques questions."
        )

    with p2:
        render_soft_step_card(
            "Étape 2",
            "Pré-diagnostic",
            "Estimation carbone numérique sur les principaux postes."
        )

    with p3:
        render_soft_step_card(
            "Étape 3",
            "Rapport PDF",
            "Synthèse exportable avec recommandations prioritaires."
        )

    st.write("")

    if st.button("Lancer le test rapide"):
        st.session_state.page = "Test rapide"
        st.rerun()
