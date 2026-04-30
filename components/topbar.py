import streamlit as st

PUBLIC_PAGES = [("Accueil", "Accueil"), ("Test rapide", "Test rapide")]
PRIVATE_PAGES = [
    ("Dashboard", "Dashboard"),
    ("Diagnostic avancé", "Diagnostic avancé"),
    ("Score", "Score"),
    ("Rapport", "Rapport"),
]


def _go(page: str):
    st.session_state.page = page
    st.query_params["page"] = page
    st.rerun()


def render_topbar():
    identity = st.session_state.company_name if st.session_state.workspace_created else "Mode invité"
    status = "Espace professionnel" if st.session_state.authenticated else "Accès gratuit"
    account = st.session_state.user_email if st.session_state.authenticated else "Découverte"

    st.markdown(
        f"""
        <div class="v15-topbar-card">
            <div class="v15-topbar-left">
                <div class="v15-brand-mark">✈️</div>
                <div>
                    <div class="v15-brand-name">AeroGreen</div>
                    <div class="v15-brand-sub">{identity}</div>
                </div>
            </div>
            <div class="v15-topbar-right">
                <span class="v15-chip muted">{account}</span>
                <span class="v15-chip accent">{status}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nav_items = PUBLIC_PAGES[:]
    if st.session_state.authenticated:
        nav_items += PRIVATE_PAGES
    else:
        nav_items += [("Connexion", "Connexion")]

    nav_cols = st.columns(len(nav_items))
    for col, (label, page) in zip(nav_cols, nav_items):
        with col:
            active = st.session_state.page == page
            btn_type = "primary" if active else "secondary"
            if st.button(label, key=f"v15_nav_{page}", type=btn_type, use_container_width=True):
                _go(page)

    if st.session_state.authenticated:
        logout_cols = st.columns([8, 1.25])
        with logout_cols[1]:
            if st.button("Déconnexion", key="v15_logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user_id = None
                st.session_state.user_email = ""
                st.session_state.page = "Accueil"
                st.query_params.clear()
                st.query_params["page"] = "Accueil"
                st.rerun()

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
