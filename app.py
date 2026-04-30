import streamlit as st

from styles.css import load_css
from components.sidebar import render_sidebar
from pages_app.home import render_home
from pages_app.fit_test import render_fit_test
from pages_app.diagnostic import render_diagnostic
from pages_app.report import render_report


st.set_page_config(
    page_title="AeroGreen",
    page_icon="✈️",
    layout="wide"
)


def init_session_state():
    defaults = {
        "page": "Accueil",
        "fit_test_done": False,
        "fit_score": 0,
        "fit_result": "",
        "last_total_t": None,
        "last_df": None,
        "last_maturity": None,
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
    elif page == "Diagnostic":
        render_diagnostic()
    elif page == "Rapport":
        render_report()
    else:
        st.session_state.page = "Accueil"
        render_home()


if __name__ == "__main__":
    main()
