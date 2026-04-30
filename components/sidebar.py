import streamlit as st

from services.calculations import get_fit_result, get_grade


def _nav_button(label: str, page: str):
    if st.button(label):
        st.session_state.page = page
        st.rerun()


def render_sidebar():
    with st.sidebar:
        st.markdown("## ✈️ AeroGreen")
        st.caption("ESG digital pre-audit platform")

        if st.session_state.workspace_created:
            st.markdown(f"""
            <div class='card-soft'>
                <div class='section-title'>Workspace</div>
                <strong>{st.session_state.company_name}</strong>
                <div class='feature-text small'>{st.session_state.company_city}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.caption("Aucun workspace client créé.")

        st.divider()

        _nav_button("Accueil", "Accueil")
        _nav_button("Test rapide", "Test rapide")
        _nav_button("Diagnostic avancé", "Diagnostic avancé")
        _nav_button("Score", "Score")
        _nav_button("Rapport", "Rapport")

        st.divider()

        if st.session_state.fit_test_done:
            result_label, result_color = get_fit_result(st.session_state.fit_score)
            st.markdown(f"""
            <div class='card-soft'>
                <div class='section-title'>Éligibilité</div>
                <div style='font-weight:800; font-size:1.4rem; color:{result_color};'>
                    {st.session_state.fit_score:.0f}%
                </div>
                <div class='feature-text small'>{result_label}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.diagnostic_done and st.session_state.diagnostic_result:
            score = st.session_state.diagnostic_result["global_score"]
            grade, color = get_grade(score)
            st.markdown(f"""
            <div class='card-soft'>
                <div class='section-title'>Score global</div>
                <div style='font-weight:900; font-size:1.7rem; color:{color};'>
                    {grade} · {score:.0f}/100
                </div>
                <div class='feature-text small'>Pré-audit avancé complété</div>
            </div>
            """, unsafe_allow_html=True)
