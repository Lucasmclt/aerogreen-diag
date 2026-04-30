import streamlit as st

from services.calculations import get_fit_result, get_grade


PUBLIC_PAGES = [
    ("Accueil", "Accueil"),
    ("Test rapide", "Test rapide"),
]

PRIVATE_PAGES = [
    ("Dashboard", "Dashboard"),
    ("Diagnostic avancé", "Diagnostic avancé"),
    ("Score", "Score"),
    ("Rapport", "Rapport"),
]


def nav_button(label: str, page: str):
    active = st.session_state.page == page
    active_class = "active" if active else ""

    st.markdown(f"<div class='nav-button-wrap {active_class}'>", unsafe_allow_html=True)
    if st.button(label, key=f"nav_{page}", use_container_width=True):
        st.session_state.page = page
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class='sidebar-brand compact'>
            <div class='brand-mark'>✈️</div>
            <div>
                <div class='sidebar-brand-title'>AeroGreen</div>
                <div class='sidebar-brand-sub'>Pré-audit carbone numérique</div>
            </div>
        </div>
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
                st.rerun()
        else:
            st.markdown("<div class='sidebar-mini-status'>Mode invité</div>", unsafe_allow_html=True)
            if st.button("Connexion professionnelle", key="login_nav_btn", use_container_width=True):
                st.session_state.page = "Connexion"
                st.rerun()

        st.markdown("<div class='sidebar-section-label'>Navigation</div>", unsafe_allow_html=True)
        for label, page in PUBLIC_PAGES:
            nav_button(label, page)

        st.markdown("<div class='sidebar-section-label'>Espace professionnel</div>", unsafe_allow_html=True)
        if st.session_state.authenticated:
            for label, page in PRIVATE_PAGES:
                nav_button(label, page)
        else:
            st.markdown(
                "<div class='sidebar-locked'>Connectez-vous pour accéder au diagnostic complet, au dashboard et au rapport.</div>",
                unsafe_allow_html=True
            )

        if st.session_state.workspace_created:
            st.markdown(f"""
            <div class='sidebar-workspace'>
                <div class='section-title'>Dossier actif</div>
                <div class='feature-title' style='margin-bottom:2px;'>{st.session_state.company_name}</div>
                <div class='feature-text small'>{st.session_state.company_city}</div>
            </div>
            """, unsafe_allow_html=True)

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
