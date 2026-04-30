import streamlit as st

from services.calculations import get_fit_result, get_grade


PAGES = ["Accueil", "Test rapide", "Diagnostic avancé", "Score", "Rapport"]


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class='sidebar-brand'>
            <div class='sidebar-brand-title'>✈️ AeroGreen</div>
            <div class='sidebar-brand-sub'>Pré-audit carbone numérique B2B pour les sous-traitants aéronautiques.</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.workspace_created:
            st.markdown(f"""
            <div class='card-soft' style='margin-bottom:.85rem;'>
                <div class='section-title'>Workspace actif</div>
                <div class='feature-title' style='margin-bottom:3px;'>{st.session_state.company_name}</div>
                <div class='feature-text small'>{st.session_state.company_city} · {st.session_state.company_sector}</div>
                <div class='feature-text small'>Réf. {st.session_state.client_reference or 'N/A'}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='sidebar-section-label'>Navigation</div>", unsafe_allow_html=True)
        current = st.session_state.page if st.session_state.page in PAGES else PAGES[0]
        selected = st.radio(
            "Navigation",
            options=PAGES,
            index=PAGES.index(current),
            label_visibility="collapsed",
        )
        if selected != st.session_state.page:
            st.session_state.page = selected

        st.markdown("<div class='sidebar-section-label'>Statut</div>", unsafe_allow_html=True)

        if st.session_state.fit_test_done:
            result_label, result_color = get_fit_result(st.session_state.fit_score)
            st.markdown(f"""
            <div class='card-soft' style='margin-bottom:.7rem;'>
                <div class='section-title'>Éligibilité</div>
                <div style='font-weight:800; font-size:1.35rem; color:{result_color};'>{st.session_state.fit_score:.0f}%</div>
                <div class='feature-text small'>{result_label}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.diagnostic_done and st.session_state.diagnostic_result:
            score = st.session_state.diagnostic_result["global_score"]
            grade, color = get_grade(score)
            st.markdown(f"""
            <div class='card-soft'>
                <div class='section-title'>Score global</div>
                <div style='font-weight:900; font-size:1.55rem; color:{color};'>{grade} · {score:.0f}/100</div>
                <div class='feature-text small'>{st.session_state.diagnostic_result['risk_label']}</div>
            </div>
            """, unsafe_allow_html=True)
        elif not st.session_state.fit_test_done:
            st.caption("Commence par le test rapide pour lancer le parcours complet.")

        st.markdown("""
        <div class='card-soft sidebar-process' style='margin-top:.8rem;'>
            <div class='section-title'>Workflow</div>
            <div class='feature-text small'>1. Workspace</div>
            <div class='feature-text small'>2. Qualification</div>
            <div class='feature-text small'>3. Diagnostic</div>
            <div class='feature-text small'>4. Score & rapport</div>
        </div>
        """, unsafe_allow_html=True)
