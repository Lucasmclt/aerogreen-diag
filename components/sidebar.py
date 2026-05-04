import streamlit as st

from services.calculations import get_fit_result, get_grade


NAV_PAGES = [
    ("Accueil", "Accueil"),
    ("Cas d’étude fictif", "Cas d’étude fictif"),
    ("Dashboard", "Dashboard"),
    ("Diagnostic avancé", "Diagnostic avancé"),
    ("Score", "Score"),
    ("Rapport", "Rapport"),
    ("Méthodologie & limites", "Méthodologie & limites"),
    ("Test rapide", "Test rapide"),
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
                    <div class='sidebar-brand-title'>AeroGreen Diag</div>
                    <div class='sidebar-brand-sub'>Prototype portfolio · pré-diagnostic indicatif</div>
                </div>
            </div>
        </a>
        """, unsafe_allow_html=True)

        st.markdown(
            "<div class='sidebar-mini-status success-dot'>Mode démo local · sans certification</div>",
            unsafe_allow_html=True
        )

        st.markdown("<div class='sidebar-section-label'>Navigation</div>", unsafe_allow_html=True)
        for label, page in NAV_PAGES:
            nav_button(label, page)

        if st.session_state.workspace_created:
            st.markdown(f"""
            <div class='sidebar-workspace'>
                <div class='section-title'>Dossier actif</div>
                <div class='feature-title' style='margin-bottom:2px;'>{st.session_state.company_name}</div>
                <div class='feature-text small'>{st.session_state.company_city}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.fit_test_done or (st.session_state.diagnostic_done and st.session_state.diagnostic_result):
            st.markdown("<div class='sidebar-section-label'>Résultats session</div>", unsafe_allow_html=True)

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
                <span>Diagnostic actif</span>
                <strong style='color:{color};'>{grade} · {score:.0f}/100</strong>
                <small>{st.session_state.diagnostic_result['risk_label']}</small>
            </div>
            """, unsafe_allow_html=True)
