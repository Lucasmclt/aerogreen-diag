import streamlit as st

from services.calculations import get_fit_result, get_grade


PUBLIC_PAGES = ["Accueil", "Test rapide"]
PRIVATE_PAGES = ["Dashboard", "Diagnostic avancé", "Score", "Rapport"]


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class='sidebar-brand compact'>
            <div class='brand-mark'>✈️</div>
            <div>
                <div class='sidebar-brand-title'>AeroGreen</div>
                <div class='sidebar-brand-sub'>Digital carbon audit</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.authenticated:
            st.markdown(f"<div class='sidebar-mini-status success-dot'>Connecté · {st.session_state.user_email}</div>", unsafe_allow_html=True)
            if st.button("Déconnexion"):
                st.session_state.authenticated = False
                st.session_state.user_id = None
                st.session_state.user_email = ""
                st.session_state.page = "Accueil"
                st.rerun()
        else:
            st.markdown("<div class='sidebar-mini-status'>Mode invité · test rapide disponible</div>", unsafe_allow_html=True)
            if st.button("Connexion pro"):
                st.session_state.page = "Connexion"
                st.rerun()

        st.markdown("<div class='sidebar-section-label'>Public</div>", unsafe_allow_html=True)
        public_index = PUBLIC_PAGES.index(st.session_state.page) if st.session_state.page in PUBLIC_PAGES else 0
        selected_public = st.radio(
            "Navigation publique",
            options=PUBLIC_PAGES,
            index=public_index,
            label_visibility="collapsed",
            key="public_nav"
        )
        if st.session_state.page in PUBLIC_PAGES and selected_public != st.session_state.page:
            st.session_state.page = selected_public

        st.markdown("<div class='sidebar-section-label'>Professionnel</div>", unsafe_allow_html=True)
        if st.session_state.authenticated:
            private_index = PRIVATE_PAGES.index(st.session_state.page) if st.session_state.page in PRIVATE_PAGES else 0
            selected_private = st.radio(
                "Navigation professionnelle",
                options=PRIVATE_PAGES,
                index=private_index,
                label_visibility="collapsed",
                key="private_nav"
            )
            if st.session_state.page in PRIVATE_PAGES and selected_private != st.session_state.page:
                st.session_state.page = selected_private
        else:
            st.markdown("<div class='sidebar-locked'>Connectez-vous pour accéder au diagnostic complet.</div>", unsafe_allow_html=True)

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
