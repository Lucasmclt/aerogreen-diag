import streamlit as st
import textwrap
from urllib.parse import quote

PUBLIC_PAGES = [("Accueil", "Accueil"), ("Test rapide", "Test rapide")]
PRIVATE_PAGES = [
    ("Dashboard", "Dashboard"),
    ("Diagnostic avancé", "Diagnostic avancé"),
    ("Score", "Score"),
    ("Rapport", "Rapport"),
]


def nav_link(label: str, page: str, active_page: str) -> str:
    active = "active" if active_page == page else ""
    return f"<a class=\"topnav-link {active}\" href=\"?page={quote(page)}\">{label}</a>"


def render_topbar():
    company_name = st.session_state.company_name if st.session_state.workspace_created else "Mode invité"
    access_label = "Connecté" if st.session_state.authenticated else "Accès gratuit"

    nav_items = PUBLIC_PAGES[:]
    if st.session_state.authenticated:
        nav_items += PRIVATE_PAGES
    else:
        nav_items += [("Connexion", "Connexion")]

    nav_html = "".join(nav_link(label, page, st.session_state.page) for label, page in nav_items)
    logout_html = ""
    if st.session_state.authenticated:
        logout_html = '<a class="topbar-chip logout-chip" href="?action=logout">Déconnexion</a>'

    html = textwrap.dedent(f"""    <div class="topbar-shell topbar-shell-clean final-topbar">
        <div class="topbar-main-row">
            <div class="topbar-logo-row">
                <div class="topbar-brand-mark">✈️</div>
                <div>
                    <div class="topbar-brand-name">AeroGreen</div>
                    <div class="topbar-brand-sub">{company_name}</div>
                </div>
            </div>
            <div class="topbar-right">
                <span class="topbar-chip warning">{access_label}</span>
                {logout_html}
            </div>
        </div>
        <div class="topbar-nav-row">{nav_html}</div>
    </div>
    """)

    st.markdown(html, unsafe_allow_html=True)
