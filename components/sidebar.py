import streamlit as st

from services.calculations import get_fit_result


def render_sidebar():
    with st.sidebar:
        st.markdown("## ✈️ AeroGreen")
        st.caption("Pré-audit carbone numérique pour sous-traitants aéronautiques")

        st.divider()

        if st.button("Accueil"):
            st.session_state.page = "Accueil"

        if st.button("Test rapide"):
            st.session_state.page = "Test rapide"

        if st.button("Diagnostic"):
            st.session_state.page = "Diagnostic"

        if st.button("Rapport"):
            st.session_state.page = "Rapport"

        st.divider()

        if st.session_state.fit_test_done:
            result_label, result_color = get_fit_result(st.session_state.fit_score)

            st.markdown(f"""
            <div class='card-soft'>
                <div class='section-title'>Éligibilité</div>
                <div style='font-weight:700; color:{result_color};'>
                    {st.session_state.fit_score:.0f}%
                </div>
                <div style='font-size:0.85rem; color:#6b7280;'>
                    {result_label}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.caption("Commence par le test rapide pour qualifier l’entreprise.")
