import streamlit as st

from styles.css import load_css
from components.sidebar import render_sidebar
from pages_app.home import render_home
from pages_app.fit_test import render_fit_test
from pages_app.diagnostic_wizard import render_diagnostic_wizard
from pages_app.score import render_score
from pages_app.report import render_report


st.set_page_config(
    page_title="AeroGreen",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session_state():
    defaults = {
        "page": "Accueil",

        # SaaS workspace
        "workspace_created": False,
        "company_name": "",
        "contact_name": "",
        "company_city": "Toulouse",
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
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def main():
    init_session_state()
    load_css()
    render_sidebar()

    page = st.session_state.page

    if page == "Accueil":
        render_home()
    elif page == "Test rapide":
        render_fit_test()
    elif page == "Diagnostic avancé":
        render_diagnostic_wizard()
    elif page == "Score":
        render_score()
    elif page == "Rapport":
        render_report()
    else:
        st.session_state.page = "Accueil"
        render_home()


if __name__ == "__main__":
    main()
