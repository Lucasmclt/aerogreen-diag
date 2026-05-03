import streamlit as st

from services.calculations import get_fit_result, get_grade


PUBLIC_PAGES = [
    ("Accueil", "Accueil"),
    ("Test rapide", "Test rapide"),
    ("Méthodologie & limites", "Méthodologie & limites"),
    ("Cas d’étude fictif", "Cas d’étude fictif"),
]

PRIVATE_PAGES = [
    ("Dashboard", "Dashboard"),
    ("Diagnostic avancé", "Diagnostic avancé"),
    ("Score", "Score"),
    ("Rapport", "Rapport"),
    ("Dossier RSE", "Dossier RSE"),
]


def nav_button(label: str, page: str):
    active = st.session_state.page == page
    active_class = "active" if active else ""

    st.markdown(f"<div class='nav-button-wrap {active_class}'>", unsafe_allow_html=True)
    if st.button(label, key=f"nav_{page}", use_container_width=True):
        st.session_state.page = page
        st.query_params["page"] = page
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <a class='sidebar-brand-link' href='?page=Accueil' target='_self'>
            <div class='sidebar-brand compact'>
                <div class='brand-mark'>✈️</div>
                <div>
                    <div class='sidebar-brand-title'>AeroGreen</div>
                    <div class='sidebar-brand-sub'>Prototype portfolio · non officiel</div>
                </div>
            </div>
        </a>
        """, unsafe_allow_html=True)

        if st.session_state.authenticated:
            st.markdown(
                f"<div class='sidebar-mini-status success-dot'>Connecté · {st.session_state.user_email}</div>",
                unsafe_allow_html=True
            )
            if st.button("Déconnexion", key="logout_btn", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user_id = None
                st.session_state.user_email = ""
                st.session_state.page = "Accueil"
                st.session_state.workspace_created = False
                st.session_state.company_name = ""
                st.session_state.contact_name = ""
                st.session_state.company_city = ""
                st.session_state.company_sector = ""
                st.session_state.client_reference = ""
                st.session_state.fit_test_done = False
                st.session_state.fit_score = 0
                st.session_state.fit_result = ""
                st.session_state.fit_answers = {}
                st.session_state.diagnostic_done = False
                st.session_state.diagnostic_result = None
                st.session_state.diagnostic_inputs = {}
                st.session_state.report_ready = False
                st.session_state.last_saved_diagnostic_key = ""
                st.session_state.last_saved_diagnostic_id = None
                st.query_params["page"] = "Accueil"
                st.rerun()
        else:
            st.markdown("<div class='sidebar-mini-status'>Mode invité</div>", unsafe_allow_html=True)
            if st.button("Connexion", key="login_nav_btn", use_container_width=True):
                st.session_state.page = "Connexion"
                st.query_params["page"] = "Connexion"
                st.rerun()

        st.markdown("<div class='sidebar-section-label'>Navigation</div>", unsafe_allow_html=True)
        for label, page in PUBLIC_PAGES:
            nav_button(label, page)

        st.markdown("<div class='sidebar-section-label'>Espace de démonstration</div>", unsafe_allow_html=True)
        if st.session_state.authenticated:
            for label, page in PRIVATE_PAGES:
                nav_button(label, page)
        else:
            st.markdown(
                "<div class='sidebar-locked'>Connectez-vous pour explorer le diagnostic complet, le démonstrateur de suivi et les rapports de travail.</div>",
                unsafe_allow_html=True
            )


        if st.session_state.authenticated and st.session_state.workspace_created:
            st.markdown(f"""
            <div class='sidebar-workspace'>
                <div class='section-title'>Dossier actif</div>
                <div class='feature-title' style='margin-bottom:2px;'>{st.session_state.company_name}</div>
                <div class='feature-text small'>{st.session_state.company_city}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.authenticated:
            if st.session_state.fit_test_done or (st.session_state.diagnostic_done and st.session_state.diagnostic_result):
                st.markdown("<div class='sidebar-section-label'>Résultats</div>", unsafe_allow_html=True)

            if st.session_state.fit_test_done:
                result_label, result_color = get_fit_result(st.session_state.fit_score)
                st.markdown(f"""
                <div class='sidebar-result-card'>
                    <span>Test rapide</span>
                    <strong style='color:{result_color};'>{st.session_state.fit_score:.0f}%</strong>
                    <small>{result_label}</small>
                </div>
                """, unsafe_allow_html=True)

            if st.session_state.diagnostic_done and st.session_state.diagnostic_result:
                score = st.session_state.diagnostic_result["global_score"]
                grade, color = get_grade(score)
                st.markdown(f"""
                <div class='sidebar-result-card'>
                    <span>Diagnostic</span>
                    <strong style='color:{color};'>{grade} · {score:.0f}/100</strong>
                    <small>{st.session_state.diagnostic_result['risk_label']}</small>
                </div>
                """, unsafe_allow_html=True)
