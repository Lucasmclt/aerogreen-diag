import streamlit as st

from components.cards import render_feature_card, render_soft_step_card


def render_home():
    st.markdown("""
    <div class='hero hero-animated'>
        <div class='hero-label'>Pré-audit carbone numérique</div>
        <h1>Évaluez rapidement l’impact numérique de votre entreprise.</h1>
        <p>
            AeroGreen vous aide à qualifier votre maturité RSE numérique, identifier vos principaux postes d’impact
            et préparer un diagnostic plus avancé, sans complexité inutile.
        </p>
    </div>
    """, unsafe_allow_html=True)

    cta_a, cta_b = st.columns([1, 1])
    with cta_a:
        if st.button("Lancer le test rapide gratuit"):
            st.session_state.page = "Test rapide"
            st.rerun()
    with cta_b:
        if st.button("Accéder à l’espace professionnel"):
            st.session_state.page = "Connexion"
            st.rerun()

    st.markdown("""
    <div class='stats-strip'>
        <div class='stats-item'>
            <div class='stats-value'>2 min</div>
            <div class='stats-label'>pour le test rapide</div>
        </div>
        <div class='stats-item'>
            <div class='stats-value'>4 étapes</div>
            <div class='stats-label'>dans le parcours complet</div>
        </div>
        <div class='stats-item'>
            <div class='stats-value'>PDF</div>
            <div class='stats-label'>rapport premium exportable</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Ce que vous obtenez")
    c1, c2, c3 = st.columns(3)
    with c1:
        render_feature_card(
            "Qualification immédiate",
            "Un test rapide pour vérifier si un pré-audit carbone numérique est pertinent pour votre structure."
        )
    with c2:
        render_feature_card(
            "Diagnostic guidé",
            "Un questionnaire structuré pour collecter les informations clés sur le matériel, les données et la gouvernance."
        )
    with c3:
        render_feature_card(
            "Restitution claire",
            "Un score global, des recommandations prioritaires et un rapport exploitable pour vos échanges internes."
        )

    st.markdown("## Comment cela fonctionne")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        render_soft_step_card("Étape 1", "Test rapide", "Obtenez une première qualification gratuitement.")
    with p2:
        render_soft_step_card("Étape 2", "Connexion", "Déverrouillez l’espace professionnel avec votre email.")
    with p3:
        render_soft_step_card("Étape 3", "Diagnostic", "Complétez le questionnaire avancé étape par étape.")
    with p4:
        render_soft_step_card("Étape 4", "Rapport", "Analysez les résultats et exportez votre synthèse PDF.")

    if st.session_state.authenticated:
        st.markdown("## Préparer un dossier")
        left, right = st.columns([1.15, 1])

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

            if st.button("Enregistrer l’espace client"):
                st.session_state.company_name = company_name.strip()
                st.session_state.contact_name = contact_name.strip()
                st.session_state.company_city = company_city.strip()
                st.session_state.company_sector = company_sector
                st.session_state.client_reference = client_reference.strip()
                st.session_state.workspace_created = True
                st.success("Espace client enregistré.")
                st.session_state.page = "Diagnostic avancé"
                st.rerun()

        with right:
            st.markdown("""
            <div class='card-dark'>
                <div class='section-title' style='color:#94a3b8;'>Espace professionnel</div>
                <h3 style='margin-top:0;'>Centralisez vos diagnostics</h3>
                <p style='color:#cbd5e1; line-height:1.65;'>
                    Préparez un dossier entreprise, conservez vos audits, comparez vos résultats et générez un rapport
                    premium prêt à partager.
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("## Espace professionnel")
        pro1, pro2 = st.columns(2)
        with pro1:
            st.markdown("""
            <div class='card'>
                <div class='section-title'>Mode gratuit</div>
                <div class='feature-title'>Commencez sans compte</div>
                <div class='feature-text'>
                    Lancez le test rapide immédiatement pour obtenir une première lecture de pertinence.
                </div>
            </div>
            """, unsafe_allow_html=True)
        with pro2:
            st.markdown("""
            <div class='card'>
                <div class='section-title'>Mode professionnel</div>
                <div class='feature-title'>Déverrouillez le parcours complet</div>
                <div class='feature-text'>
                    Connectez-vous pour accéder au diagnostic avancé, à l’historique des audits et au rapport PDF premium.
                </div>
            </div>
            """, unsafe_allow_html=True)
