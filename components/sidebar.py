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

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="v16-sidebar-shell">
            <div class="v16-sidebar-brand">
                <div class="v16-sidebar-logo">✈️</div>
                <div>
                    <div class="v16-sidebar-title">AeroGreen</div>
                    <div class="v16-sidebar-sub">Pré-audit carbone numérique</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.authenticated:
            st.markdown(
                f"""
                <div class="v16-sidebar-status-card">
                    <div class="v16-status-label">Compte</div>
                    <div class="v16-status-value">{st.session_state.user_email}</div>
                    <div class="v16-status-chip success">Espace professionnel</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div class="v16-sidebar-status-card">
                    <div class="v16-status-label">Mode</div>
                    <div class="v16-status-value">Découverte</div>
                    <div class="v16-status-chip">Accès gratuit</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div class='v16-nav-group-label'>Navigation</div>", unsafe_allow_html=True)
        for label, page in PUBLIC_PAGES:
            active = st.session_state.page == page
            if st.button(label, key=f"v16_nav_public_{page}", use_container_width=True, type="primary" if active else "secondary"):
                _go(page)

        st.markdown("<div class='v16-nav-group-label'>Espace professionnel</div>", unsafe_allow_html=True)
        if st.session_state.authenticated:
            for label, page in PRIVATE_PAGES:
                active = st.session_state.page == page
                if st.button(label, key=f"v16_nav_private_{page}", use_container_width=True, type="primary" if active else "secondary"):
                    _go(page)
            if st.button("Déconnexion", key="v16_logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user_id = None
                st.session_state.user_email = ""
                st.session_state.page = "Accueil"
                st.query_params.clear()
                st.query_params["page"] = "Accueil"
                st.rerun()
        else:
            st.caption("Connectez-vous pour accéder au diagnostic avancé, au dashboard et aux rapports.")
            active = st.session_state.page == "Connexion"
            if st.button("Connexion", key="v16_nav_login", use_container_width=True, type="primary" if active else "secondary"):
                _go("Connexion")

        if st.session_state.workspace_created:
            st.markdown(
                f"""
                <div class="v16-sidebar-workspace">
                    <div class="v16-status-label">Dossier actif</div>
                    <div class="v16-status-value">{st.session_state.company_name}</div>
                    <div class="v16-sidebar-sub">{st.session_state.company_city}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
