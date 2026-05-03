import streamlit as st

from services.calculations import get_fit_result, get_grade


def render_topbar():
    page = st.session_state.page

    workspace_name = st.session_state.company_name if st.session_state.workspace_created else ("Mode invité" if not st.session_state.authenticated else "Aucun espace client")
    workspace_status = "Actif" if st.session_state.workspace_created else ("Gratuit" if not st.session_state.authenticated else "À créer")
    workspace_status_class = "success" if st.session_state.workspace_created else "warning"

    if st.session_state.fit_test_done:
        fit_label, fit_color = get_fit_result(st.session_state.fit_score)
        fit_html = f"<span class='topbar-chip neutral'>Éligibilité {st.session_state.fit_score:.0f}%</span>"
    else:
        fit_html = "<span class='topbar-chip warning'>Test rapide non lancé</span>"

    if st.session_state.diagnostic_done and st.session_state.diagnostic_result:
        global_score = st.session_state.diagnostic_result["global_score"]
        grade, color = get_grade(global_score)
        diagnostic_html = f"<span class='topbar-chip success'>Score {grade} · {global_score:.0f}/100</span>"
    else:
        diagnostic_html = "<span class='topbar-chip warning'>Diagnostic avancé incomplet</span>"

    st.markdown(
        f"""
        <div class='topbar-shell'>
            <div>
                <div class='topbar-breadcrumb'>AeroGreen <span>/</span> {page}</div>
                <div class='topbar-title-row'>
                    <div class='topbar-title'>{workspace_name}</div>
                    <span class='topbar-chip {workspace_status_class}'>{workspace_status}</span>
                </div>
            </div>
            <div class='topbar-right'>
                {fit_html}
                {diagnostic_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
