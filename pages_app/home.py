import streamlit as st

from components.cards import (
    render_icon_card,
    render_process_timeline,
)


def _go_to(page: str):
    st.session_state.page = page
    st.query_params["page"] = page
    st.rerun()


def render_home():
    st.markdown("""
    <div class='landing-hero'>
        <div class='hero-content'>
            <div class='hero-label'>Prototype portfolio — non officiel</div>
            <h1>AeroGreen Diag aide une PME industrielle à structurer un premier dossier de preuves RSE numériques.</h1>
            <p>
                Prototype portfolio construit avant TBS L3 depuis un profil prépa EPITA : traduire un problème industriel et RSE flou
                en outil numérique compréhensible, avec diagnostic indicatif, preuves, rapport et limites assumées.
            </p>
            <div class="hero-cta-row">
                <a class="hero-cta primary" href="?page=Cas%20d%E2%80%99%C3%A9tude%20fictif" target="_self">Tester avec le cas fictif</a>
                <a class="hero-cta secondary" href="?page=Diagnostic%20avanc%C3%A9" target="_self">Remplir le diagnostic</a>
            </div>
        </div>
        <div class='hero-visual'>
            <div class='score-orb'>
                <span>Score</span>
                <strong>A–E</strong>
            </div>
            <div class='mini-card floating-card one'>
                <span>Données</span>
                <strong>déclaratives</strong>
            </div>
            <div class='mini-card floating-card two'>
                <span>Rapport</span>
                <strong>exploratoire</strong>
            </div>
            <div class='mini-card floating-card three'>
                <span>Preuves</span>
                <strong>à structurer</strong>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='card-soft' style='margin-top:1.35rem; border:1px solid rgba(245,158,11,.28); background:rgba(255,251,235,.72);'>
        <div class='section-title'>Prototype portfolio — non officiel</div>
        <strong>Pré-diagnostic indicatif, pas audit ni certification.</strong>
        <div class='feature-text'>
            AeroGreen Diag collecte des réponses déclaratives, produit une lecture indicative de maturité numérique responsable,
            aide à identifier des zones faibles et génère un rapport de travail. Les résultats ne remplacent ni EcoVadis,
            ni un bilan GES, ni un consultant RSE, ni une validation réglementaire.
        </div>
        <br>
        <div class='feature-text'>
            Pour une lecture portfolio rapide, commencez par le cas d’étude fictif : il charge une PME industrielle simulée
            et permet de tester immédiatement le dashboard, le score et le rapport PDF sans remplir tout le questionnaire.
        </div>
    </div>
    """, unsafe_allow_html=True)

    cta1, cta2, cta3 = st.columns(3)
    with cta1:
        if st.button("Voir le cas d’étude fictif", key="home_case_study", use_container_width=True):
            _go_to("Cas d’étude fictif")
    with cta2:
        if st.button("Lancer le diagnostic", key="home_start_diagnostic", use_container_width=True):
            _go_to("Diagnostic avancé")
    with cta3:
        if st.button("Méthodologie & limites", key="home_methodology", use_container_width=True):
            _go_to("Méthodologie & limites")

    st.markdown("""
    <div class='trust-strip'>
        <div><strong>Portfolio</strong><span>Démonstrateur produit / tech / business</span></div>
        <div><strong>Pré-diagnostic</strong><span>Score indicatif, non officiel</span></div>
        <div><strong>Rapport</strong><span>Pièce maîtresse exportable</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Pourquoi ce sujet existe")
    st.markdown("""
    <div class='card-soft'>
        <div class='section-title'>Problème exploré</div>
        <strong>Les PME industrielles doivent de plus en plus rendre leurs pratiques RSE lisibles.</strong>
        <div class='feature-text'>
            Dans une chaîne de sous-traitance aéronautique, une PME peut être sollicitée sur ses pratiques environnementales,
            ses preuves documentaires, ses achats responsables, sa gestion des équipements numériques ou ses données PLM/CAO.
            Le prototype explore comment organiser ces informations avant un échange client, un questionnaire fournisseur,
            une préparation interne inspirée de logiques de maturité ou une réflexion autour du numérique responsable.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Ce que le prototype démontre")
    c1, c2, c3 = st.columns(3)
    with c1:
        render_icon_card(
            "🧭",
            "Parcours produit complet",
            "Test rapide, diagnostic guidé, dashboard, cas fictif, score et rapport exploratoire.",
            "#6366f1"
        )
    with c2:
        render_icon_card(
            "📊",
            "Scoring transparent",
            "Pondérations simples sur carbone numérique, gouvernance, données et achats IT.",
            "#10b981"
        )
    with c3:
        render_icon_card(
            "📄",
            "Lucidité méthodologique",
            "Le projet explicite ce qu’il fait, ce qu’il ne fait pas et pourquoi ses limites sont assumées.",
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
            <p>Qualifier rapidement si le cas d’entreprise est pertinent pour ce type de pré-diagnostic.</p>
            <ul>
                <li>Questionnaire court</li>
                <li>Score d’adéquation indicatif</li>
                <li>Orientation vers le diagnostic guidé</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class='pricing-card pro'>
            <div class='section-title'>Analyse guidée</div>
            <h3>Pré-diagnostic numérique responsable</h3>
            <p>Structurer des informations déclaratives et produire un rapport exploratoire lisible.</p>
            <ul>
                <li>Questionnaire multi-étapes</li>
                <li>Score indicatif de maturité</li>
                <li>Recommandations non officielles</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
