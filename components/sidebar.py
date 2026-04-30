import streamlit as st

from services.calculations import get_fit_result, get_grade


PUBLIC_PAGES = ["Accueil", "Test rapide"]
PRIVATE_PAGES = ["Dashboard", "Diagnostic avancé", "Score", "Rapport"]


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class='sidebar-brand'>
            <div class='sidebar-brand-title'>✈️ AeroGreen</div>
            <div class='sidebar-brand-sub'>Plateforme de pré-audit carbone numérique.</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.authenticated:
            st.markdown(f"<div class='sidebar-mini-status'>Connecté · {st.session_state.user_email}</div>", unsafe_allow_html=True)
            if st.button("Déconnexion"):
                st.session_state.authenticated = False
                st.session_state.user_id = None
                st.session_state.user_email = ""
                st.session_state.page = "Accueil"
                st.rerun()
        else:
            st.markdown("<div class='sidebar-mini-status'>Mode invité</div>", unsafe_allow_html=True)
            if st.button("Connexion professionnelle"):
                st.session_state.page = "Connexion"
                st.rerun()

        st.markdown("<div class='sidebar-section-label'>Navigation</div>", unsafe_allow_html=True)
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

        st.markdown("<div class='sidebar-section-label'>Espace professionnel</div>", unsafe_allow_html=True)
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
            st.markdown("<div class='sidebar-locked'>Diagnostic avancé, score, dashboard et rapport disponibles après connexion.</div>", unsafe_allow_html=True)

        if st.session_state.workspace_created:
            st.markdown(f"""
            <div class='sidebar-workspace'>
                <div class='section-title'>Dossier actif</div>
                <div class='feature-title' style='margin-bottom:2px;'>{st.session_state.company_name}</div>
                <div class='feature-text small'>{st.session_state.company_city}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.fit_test_done or (st.session_state.diagnostic_done and st.session_state.diagnostic_result):
            st.markdown("<div class='sidebar-section-label'>Indicateurs</div>", unsafe_allow_html=True)

        if st.session_state.fit_test_done:
            result_label, result_color = get_fit_result(st.session_state.fit_score)
            st.markdown(f"""
            <div class='card-soft' style='margin-bottom:.7rem;'>
                <div class='section-title'>Test rapide</div>
                <div style='font-weight:800; font-size:1.25rem; color:{result_color};'>{st.session_state.fit_score:.0f}%</div>
                <div class='feature-text small'>{result_label}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.diagnostic_done and st.session_state.diagnostic_result:
            score = st.session_state.diagnostic_result["global_score"]
            grade, color = get_grade(score)
            st.markdown(f"""
            <div class='card-soft'>
                <div class='section-title'>Diagnostic</div>
                <div style='font-weight:900; font-size:1.4rem; color:{color};'>{grade} · {score:.0f}/100</div>
                <div class='feature-text small'>{st.session_state.diagnostic_result['risk_label']}</div>
            </div>
            """, unsafe_allow_html=True)
