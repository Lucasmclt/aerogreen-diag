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
from pages_app.deep_audit import render_deep_audit
from pages_app.methodology import render_methodology
from pages_app.case_study import render_case_study


st.set_page_config(
    page_title="AeroGreen",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


PUBLIC_PAGES = ["Accueil", "Test rapide", "Connexion", "Méthodologie & limites", "Cas d’étude fictif"]


def init_session_state():
    defaults = {
        "page": "Accueil",

        # Workspace de démonstration
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
        "current_deep_public_code": "",

        # Auth
        "authenticated": False,
        "user_id": None,
        "user_email": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def sync_query_params():
    page = st.query_params.get("page")
    valid_pages = [
        "Accueil",
        "Test rapide",
        "Connexion",
        "Dashboard",
        "Diagnostic avancé",
        "Score",
        "Rapport",
        "Audit approfondi",
        "Méthodologie & limites",
        "Cas d’étude fictif",
        "Dossier RSE",
    ]
    if page in valid_pages:
        st.session_state.page = page


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
    elif page in ["Audit approfondi", "Dossier RSE"]:
        if require_auth():
            render_deep_audit()
        else:
            render_login()
    elif page == "Méthodologie & limites":
        render_methodology()
    elif page == "Cas d’étude fictif":
        render_case_study()
    else:
        st.session_state.page = "Accueil"
        render_home()


if __name__ == "__main__":
    main()
