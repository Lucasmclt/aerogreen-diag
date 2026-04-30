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
    company_name = st.session_state.company_name if st.session_state.workspace_created else "Mode invité"
    access_label = "Connecté" if st.session_state.authenticated else "Accès gratuit"

    st.markdown("<div class='native-topbar-shell'>", unsafe_allow_html=True)

    brand_col, status_col = st.columns([6, 1.4])
    with brand_col:
        st.markdown(
            f"""
            <div class="native-brand-row">
                <div class="topbar-brand-mark">✈️</div>
                <div>
                    <div class="topbar-brand-name">AeroGreen</div>
                    <div class="topbar-brand-sub">{company_name}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with status_col:
        st.markdown(
            f"<div class='native-status-wrap'><span class='topbar-chip warning'>{access_label}</span></div>",
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
            btn_type = "primary" if st.session_state.page == page else "secondary"
            if st.button(label, key=f"native_nav_{page}", type=btn_type, use_container_width=True):
                _go(page)

    if st.session_state.authenticated:
        right_cols = st.columns([8, 1.2])
        with right_cols[1]:
            if st.button("Déconnexion", key="native_logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user_id = None
                st.session_state.user_email = ""
                st.session_state.page = "Accueil"
                st.query_params.clear()
                st.query_params["page"] = "Accueil"
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
