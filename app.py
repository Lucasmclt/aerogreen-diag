import streamlit as st

from styles.css import load_css
from services.database import init_db, get_or_create_passwordless_user
from components.sidebar import render_sidebar
from pages_app.home import render_home
from pages_app.fit_test import render_fit_test
from pages_app.dashboard import render_dashboard
from pages_app.diagnostic_wizard import render_diagnostic_wizard
from pages_app.score import render_score
from pages_app.report import render_report
from pages_app.methodology import render_methodology
from pages_app.case_study import render_case_study


st.set_page_config(
    page_title="AeroGreen Diag",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

VALID_PAGES = [
    "Accueil",
    "Test rapide",
    "Dashboard",
    "Diagnostic avancé",
    "Score",
    "Rapport",
    "Méthodologie & limites",
    "Cas d’étude fictif",
]

DEMO_EMAIL = "demo@aerogreen.local"


def init_session_state():
    defaults = {
        "page": "Accueil",

        # Workspace de démonstration local
        "workspace_created": False,
        "company_name": "",
        "contact_name": "",
        "company_city": "",
        "company_sector": "",
        "client_reference": "",

        # Fit test
        "fit_test_done": False,
        "fit_score": 0,
        "fit_result": "",
        "fit_answers": {},

        # Wizard
        "wizard_step": 1,
        "diagnostic_done": False,
        "diagnostic_inputs": {},
        "diagnostic_result": None,

        # Report
        "report_ready": False,
        "last_saved_diagnostic_key": "",
        "last_saved_diagnostic_id": None,
        "current_audit_public_code": "",

        # Démo locale : pas de friction d’authentification pour un projet portfolio.
        "authenticated": True,
        "user_id": None,
        "user_email": DEMO_EMAIL,
        "demo_mode": True,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def ensure_demo_user():
    if st.session_state.get("user_id") is None:
        user = get_or_create_passwordless_user(DEMO_EMAIL)
        st.session_state.user_id = user["id"]
        st.session_state.user_email = user["email"]
        st.session_state.authenticated = True
        st.session_state.demo_mode = True


def sync_query_params():
    page = st.query_params.get("page")
    if page in VALID_PAGES:
        st.session_state.page = page


def main():
    init_db()
    init_session_state()
    ensure_demo_user()
    sync_query_params()
    load_css()
    render_sidebar()

    page = st.session_state.page

    if page == "Accueil":
        render_home()
    elif page == "Test rapide":
        render_fit_test()
    elif page == "Dashboard":
        render_dashboard()
    elif page == "Diagnostic avancé":
        render_diagnostic_wizard()
    elif page == "Score":
        render_score()
    elif page == "Rapport":
        render_report()
    elif page == "Méthodologie & limites":
        render_methodology()
    elif page == "Cas d’étude fictif":
        render_case_study()
    else:
        st.session_state.page = "Accueil"
        render_home()


if __name__ == "__main__":
    main()
