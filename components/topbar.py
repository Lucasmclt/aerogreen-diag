import streamlit as st


PUBLIC_PAGES = [("Accueil", "Accueil"), ("Test rapide", "Test rapide")]
PRIVATE_PAGES = [
    ("Dashboard", "Dashboard"),
    ("Diagnostic avancé", "Diagnostic avancé"),
    ("Score", "Score"),
    ("Rapport", "Rapport"),
]


def _go_to(page: str):
    st.session_state.page = page
    st.rerun()


def render_topbar():
    company_name = st.session_state.company_name if st.session_state.workspace_created else "Mode invité"
    status_chip = "Connecté" if st.session_state.authenticated else "Accès gratuit"

    fit_chip = ""
    if st.session_state.fit_test_done:
        fit_chip = f"<span class='topbar-chip neutral'>Test rapide {st.session_state.fit_score:.0f}%</span>"

    score_chip = ""
    if st.session_state.diagnostic_done and st.session_state.diagnostic_result:
        result = st.session_state.diagnostic_result
        score_chip = f"<span class='topbar-chip success'>Score {result['grade']} · {result['global_score']:.0f}/100</span>"

    st.markdown(
        f"""
        <div class='topbar-shell topbar-shell-clean'>
            <div class='topbar-left-block'>
                <div class='topbar-logo-row'>
                    <div class='topbar-brand-mark'>✈️</div>
                    <div>
                        <div class='topbar-brand-name'>AeroGreen</div>
                        <div class='topbar-brand-sub'>{company_name}</div>
                    </div>
                </div>
            </div>
            <div class='topbar-right'>
                <span class='topbar-chip warning'>{status_chip}</span>
                {fit_chip}
                {score_chip}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nav_items = PUBLIC_PAGES[:]
    if st.session_state.authenticated:
        nav_items += PRIVATE_PAGES

    if not st.session_state.authenticated:
        nav_items += [("Connexion", "Connexion")]

    nav_cols = st.columns([1] * len(nav_items))
    for col, (label, page) in zip(nav_cols, nav_items):
        with col:
            btn_type = "primary" if st.session_state.page == page else "secondary"
            if st.button(label, key=f"topnav_{page}", use_container_width=True, type=btn_type):
                _go_to(page)

    if st.session_state.authenticated:
        auth_cols = st.columns([6, 1.2])
        with auth_cols[1]:
            if st.button("Déconnexion", key="top_logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user_id = None
                st.session_state.user_email = ""
                st.session_state.page = "Accueil"
                st.rerun()

    st.markdown("<div style='height: 0.65rem;'></div>", unsafe_allow_html=True)
