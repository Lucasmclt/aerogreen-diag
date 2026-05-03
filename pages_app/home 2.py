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
            <div class='hero-label'>Projet personnel · Prototype exploratoire</div>
            <h1>AeroGreen Diag est un prototype exploratoire de diagnostic RSE numérique pour PME industrielles.</h1>
            <p>
                Conçu comme projet personnel avant mon entrée à TBS, ce démonstrateur relie développement logiciel,
                analyse produit, enjeux RSE et contexte industriel aéronautique autour de Toulouse.
            </p>
            <div class="hero-cta-row">
                <a class="hero-cta primary" href="?page=Test%20rapide" target="_self">Commencer le test rapide</a>
                <a class="hero-cta secondary" href="?page=Connexion" target="_self">Explorer le diagnostic avancé</a>
            </div>
        </div>
        <div class='hero-visual'>
            <div class='score-orb'>
                <span>Lecture</span>
                <strong>A–E</strong>
            </div>
            <div class='mini-card floating-card one'>
                <span>Empreinte</span>
                <strong>indicative</strong>
            </div>
            <div class='mini-card floating-card two'>
                <span>Rapport</span>
                <strong>PDF</strong>
            </div>
            <div class='mini-card floating-card three'>
                <span>Preuves</span>
                <strong>RSE</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    <div class='card-soft' style='border:1px solid rgba(99,102,241,.18);'>
        <div class='section-title'>Cadre du projet</div>
        <strong>Cas d’étude personnel avant TBS · profil prépa EPITA</strong>
        <div class='feature-text'>
            Ce démonstrateur n’est pas une offre SaaS finalisée, ni une certification, ni un concurrent d’EcoVadis.
            Il sert à montrer une capacité à transformer un sujet B2B industriel en prototype numérique structuré,
            avec parcours utilisateur, scoring, dashboard et livrable PDF.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='trust-strip'>
        <div><strong>Prototype</strong><span>Projet personnel produit / tech / business</span></div>
        <div><strong>Pré-analyse</strong><span>Résultats indicatifs, non officiels</span></div>
        <div><strong>Livrable</strong><span>Rapports de travail PDF exportables</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Pourquoi ce projet ?")
    st.markdown("""
    <div class='card-soft'>
        <div class='section-title'>Intention</div>
        <strong>Explorer un besoin B2B réel avec un démonstrateur fonctionnel</strong>
        <div class='feature-text'>
            L’objectif est d’explorer comment un outil numérique peut aider une PME industrielle à structurer ses preuves RSE,
            identifier ses zones de fragilité et préparer un échange avec un client ou un référentiel. AeroGreen Diag n’est pas
            une certification, ni une notation EcoVadis, ni une solution commerciale finalisée : c’est un cas d’étude personnel.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Ce que le prototype démontre")
    c1, c2, c3 = st.columns(3)
    with c1:
        render_icon_card(
            "🧭",
            "Parcours produit complet",
            "Test rapide, diagnostic avancé, espace connecté, suivi des cas enregistrés et export PDF.",
            "#6366f1"
        )
    with c2:
        render_icon_card(
            "📊",
            "Scoring multicritère",
            "Pré-analyse des équipements, données PLM/CAO, cloud, gouvernance, achats IT et preuves RSE.",
            "#10b981"
        )
    with c3:
        render_icon_card(
            "📄",
            "Structuration des preuves",
            "Dossier de travail pour préparer une discussion client, une réflexion REEN ou une démarche de type EcoVadis.",
            "#0ea5e9"
        )

    st.markdown("## Parcours")
    render_process_timeline()

    st.markdown("## Deux niveaux d’analyse")
    left, right = st.columns([1, 1])

    with left:
        st.markdown("""
        <div class='pricing-card free'>
            <div class='section-title'>Premier niveau</div>
            <h3>Test rapide</h3>
            <p>Pour qualifier rapidement la pertinence du sujet dans un cas d’entreprise.</p>
            <ul>
                <li>Questionnaire court</li>
                <li>Score d’adéquation indicatif</li>
                <li>Orientation vers une analyse plus détaillée</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class='pricing-card pro'>
            <div class='section-title'>Analyse approfondie</div>
            <h3>Dossier RSE numérique</h3>
            <p>Pour structurer les preuves, compléter l’analyse indicative et générer un rapport de travail.</p>
            <ul>
                <li>Questionnaire multi-étapes</li>
                <li>Démonstrateur de suivi</li>
                <li>PDF de travail exportable</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
