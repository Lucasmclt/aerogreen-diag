import streamlit as st

from styles.css import load_css
from services.database import init_db
from components.sidebar import render_sidebar
from pages_app.home import render_home
from pages_app.login import render_login
from pages_app.fit_test import render_fit_test
from pages_app.dashboard import render_dashboard
from pages_app.diagnostic_wizard import render_diagnostic_wizard
from pages_app.score import render_score
from pages_app.report import render_report


st.set_page_config(
    page_title="AeroGreen",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


ALL_PAGES = [
    "Accueil",
    "Test rapide",
    "Connexion",
    "Dashboard",
    "Diagnostic avancé",
    "Score",
    "Rapport",
]


def init_session_state():
    defaults = {
        "page": "Accueil",
        "workspace_created": False,
        "company_name": "",
        "contact_name": "",
        "company_city": "Toulouse",
        "company_sector": "",
        "client_reference": "",
        "fit_test_done": False,
        "fit_score": 0,
        "fit_result": "",
        "fit_answers": {},
        "wizard_step": 1,
        "diagnostic_done": False,
        "diagnostic_inputs": {},
        "diagnostic_result": None,
        "report_ready": False,
        "authenticated": False,
        "user_id": None,
        "user_email": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def sync_query_params():
    params = st.query_params
    action = params.get("action")

    if action == "logout":
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.user_email = ""
        st.session_state.page = "Accueil"
        st.query_params.clear()
        st.query_params["page"] = "Accueil"
        st.rerun()

    page = params.get("page")
    if page in ALL_PAGES:
        st.session_state.page = page
    else:
        st.query_params["page"] = st.session_state.page


def require_auth():
    if not st.session_state.authenticated:
        st.session_state.page = "Connexion"
        st.query_params["page"] = "Connexion"
        return False
    return True


def main():
    init_db()
    init_session_state()
    sync_query_params()
    load_css()
    render_sidebar()

    page = st.session_state.page

    if page == "Accueil":
        render_home()
    elif page == "Test rapide":
        render_fit_test()
    elif page == "Connexion":
        render_login()
    elif page == "Dashboard":
        if require_auth():
            render_dashboard()
        else:
            render_login()
    elif page == "Diagnostic avancé":
        if require_auth():
            render_diagnostic_wizard()
        else:
            render_login()
    elif page == "Score":
        if require_auth():
            render_score()
        else:
            render_login()
    elif page == "Rapport":
        if require_auth():
            render_report()
        else:
            render_login()
    else:
        st.session_state.page = "Accueil"
        st.query_params["page"] = "Accueil"
        render_home()


if __name__ == "__main__":
    main()
