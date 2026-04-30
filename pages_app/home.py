import streamlit as st

from components.cards import render_feature_card, render_soft_step_card


def render_home():
    st.markdown("""
    <div class='hero'>
        <div class='hero-label'>Aerospace ESG Intelligence</div>
        <h1>Le pré-audit carbone numérique pensé pour les PME aéronautiques.</h1>
        <p>
            AeroGreen aide les sous-traitants aéronautiques de rang 2 et 3 à mesurer rapidement
            leur empreinte numérique, qualifier leur maturité RSE et générer un rapport exploitable
            face aux exigences croissantes des grands donneurs d’ordre.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Mode SaaS")

    c1, c2, c3 = st.columns(3)

    with c1:
        render_feature_card(
            "Workspace client",
            "Crée un dossier d’entreprise avec secteur, ville, référent et référence de mission."
        )

    with c2:
        render_feature_card(
            "Diagnostic multi-étapes",
            "Collecte structurée : profil, matériel, données, cloud, gouvernance et achats IT."
        )

    with c3:
        render_feature_card(
            "Score + PDF premium",
            "Calcul d’un score global, grade A-E, risques, recommandations et export PDF."
        )

    st.markdown("### Créer un workspace client")

    left, right = st.columns([1.2, 1])

    with left:
        company_name = st.text_input("Nom de l’entreprise", value=st.session_state.company_name)
        contact_name = st.text_input("Référent / contact", value=st.session_state.contact_name)
        company_city = st.text_input("Ville", value=st.session_state.company_city)
        company_sector = st.selectbox(
            "Secteur",
            [
                "Sous-traitant aéronautique rang 2 ou 3",
                "Bureau d’études / ingénierie",
                "Fournisseur industriel hors aéronautique",
                "Autre"
            ],
            index=0
        )
        client_reference = st.text_input("Référence dossier", value=st.session_state.client_reference)

        if st.button("Créer le workspace"):
            st.session_state.company_name = company_name.strip()
            st.session_state.contact_name = contact_name.strip()
            st.session_state.company_city = company_city.strip()
            st.session_state.company_sector = company_sector
            st.session_state.client_reference = client_reference.strip()
            st.session_state.workspace_created = True
            st.success("Workspace client créé.")
            st.session_state.page = "Test rapide"
            st.rerun()

    with right:
        st.markdown("""
        <div class='card-dark'>
            <div class='section-title' style='color:#94a3b8;'>Positionnement</div>
            <h3 style='margin-top:0;'>Alternative légère aux audits lourds</h3>
            <p style='color:#cbd5e1; line-height:1.6;'>
                L’objectif n’est pas de remplacer un audit réglementaire, mais de donner une première lecture
                structurée, rapide et exploitable commercialement.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Parcours")

    p1, p2, p3, p4 = st.columns(4)
    with p1:
        render_soft_step_card("Étape 1", "Qualification", "Vérifier si AeroGreen est pertinent pour l’entreprise.")
    with p2:
        render_soft_step_card("Étape 2", "Collecte", "Saisir les données clés par blocs métier.")
    with p3:
        render_soft_step_card("Étape 3", "Scoring", "Obtenir un score global et des scores par pilier.")
    with p4:
        render_soft_step_card("Étape 4", "Rapport", "Exporter un PDF premium pour discussion AMOA.")
