import streamlit as st

from components.cards import (
    render_icon_card,
    render_process_timeline,
    render_upgrade_panel,
)


def render_home():
    st.markdown("""
    <div class='landing-hero'>
        <div class='hero-content'>
            <div class='hero-label'>Pré-audit carbone numérique</div>
            <h1>Mesurez votre maturité numérique responsable en quelques minutes.</h1>
            <p>
                AeroGreen aide les PME industrielles et aéronautiques à obtenir une première lecture claire
                de leur impact numérique : équipements, données techniques, cloud, gouvernance et achats IT.
            </p>        </div>
        <div class='hero-visual'>
            <div class='score-orb'>
                <span>Score</span>
                <strong>A–E</strong>
            </div>
            <div class='mini-card floating-card one'>
                <span>Empreinte estimée</span>
                <strong>tCO₂e</strong>
            </div>
            <div class='mini-card floating-card two'>
                <span>Rapport</span>
                <strong>PDF</strong>
            </div>
            <div class='mini-card floating-card three'>
                <span>Risque</span>
                <strong>RSE</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cta1, cta2, cta3 = st.columns([1.15, 1.55, 4.3])
    with cta1:
        if st.button("Test rapide gratuit", key="hero_test_btn", type="primary", use_container_width=True):
            st.session_state.page = "Test rapide"
            st.rerun()
    with cta2:
        if st.button("Diagnostic avancé sur compte pro", key="hero_pro_btn", use_container_width=True):
            st.session_state.page = "Connexion"
            st.rerun()

    st.markdown("""
    <div class='trust-strip'>
        <div><strong>Sans compte</strong><span>Test rapide accessible immédiatement</span></div>
        <div><strong>Compte pro</strong><span>Historique, scoring et rapport PDF</span></div>
        <div><strong>Historique</strong><span>Vos diagnostics sauvegardés</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Ce que vous obtenez")
    c1, c2, c3 = st.columns(3)
    with c1:
        render_icon_card(
            "⚡",
            "Qualification immédiate",
            "Identifiez rapidement si un diagnostic carbone numérique est pertinent pour votre entreprise.",
            "#6366f1"
        )
    with c2:
        render_icon_card(
            "📊",
            "Analyse structurée",
            "Mesurez les principaux postes : parc informatique, stockage PLM/CAO, serveurs, cloud et achats IT.",
            "#10b981"
        )
    with c3:
        render_icon_card(
            "📄",
            "Restitution exploitable",
            "Obtenez un score, un niveau de risque, des recommandations et un rapport PDF prêt à partager.",
            "#0ea5e9"
        )

    st.markdown("## Parcours")
    render_process_timeline()

    st.markdown("## Mode gratuit ou professionnel")
    left, right = st.columns([1, 1])

    with left:
        st.markdown("""
        <div class='pricing-card free'>
            <div class='section-title'>Gratuit</div>
            <h3>Test rapide</h3>
            <p>Pour obtenir une première qualification sans créer de compte.</p>
            <ul>
                <li>Questionnaire court</li>
                <li>Score d’adéquation</li>
                <li>Orientation vers la suite</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class='pricing-card pro'>
            <div class='section-title'>Professionnel</div>
            <h3>Diagnostic complet</h3>
            <p>Pour créer des dossiers, conserver les audits et produire un rapport premium.</p>
            <ul>
                <li>Questionnaire multi-étapes</li>
                <li>Dashboard exécutif</li>
                <li>PDF premium exportable</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.authenticated:
        st.markdown("## Préparer un dossier client")
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

            if st.button("Enregistrer l’espace client", use_container_width=True):
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
            render_upgrade_panel()
