import streamlit as st

from services.calculations import get_fit_result, get_grade


PUBLIC_PAGES = ["Accueil", "Test rapide"]
PRIVATE_PAGES = ["Dashboard", "Diagnostic avancé", "Score", "Rapport"]


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class='sidebar-brand'>
            <div class='sidebar-brand-title'>✈️ AeroGreen</div>
            <div class='sidebar-brand-sub'>Pré-audit carbone numérique B2B pour sous-traitants aéronautiques.</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.authenticated:
            st.caption(f"Connecté : {st.session_state.user_email}")
            if st.button("Déconnexion"):
                st.session_state.authenticated = False
                st.session_state.user_id = None
                st.session_state.user_email = ""
                st.session_state.page = "Accueil"
                st.rerun()
        else:
            st.markdown("""
            <div class='card-soft' style='margin-bottom:.85rem;'>
                <div class='section-title'>Accès invité</div>
                <div class='feature-text small'>
                    Vous pouvez lancer le test rapide sans compte. Le diagnostic avancé nécessite une connexion.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Connexion / compte pro"):
                st.session_state.page = "Connexion"
                st.rerun()

        if st.session_state.workspace_created:
            st.markdown(f"""
            <div class='card-soft' style='margin-bottom:.85rem;'>
                <div class='section-title'>Espace actif</div>
                <div class='feature-title' style='margin-bottom:3px;'>{st.session_state.company_name}</div>
                <div class='feature-text small'>{st.session_state.company_city} · {st.session_state.company_sector}</div>
                <div class='feature-text small'>Réf. {st.session_state.client_reference or 'N/A'}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div class='sidebar-section-label'>Navigation publique</div>", unsafe_allow_html=True)
        current_public = st.session_state.page if st.session_state.page in PUBLIC_PAGES else PUBLIC_PAGES[0]
        selected_public = st.radio(
            "Navigation publique",
            options=PUBLIC_PAGES,
            index=PUBLIC_PAGES.index(current_public),
            label_visibility="collapsed",
            key="public_nav"
        )
        if selected_public != st.session_state.page and st.session_state.page in PUBLIC_PAGES:
            st.session_state.page = selected_public

        st.markdown("<div class='sidebar-section-label'>Espace professionnel</div>", unsafe_allow_html=True)

        if st.session_state.authenticated:
            current_private = st.session_state.page if st.session_state.page in PRIVATE_PAGES else PRIVATE_PAGES[0]
            selected_private = st.radio(
                "Navigation professionnelle",
                options=PRIVATE_PAGES,
                index=PRIVATE_PAGES.index(current_private),
                label_visibility="collapsed",
                key="private_nav"
            )
            if selected_private != st.session_state.page and st.session_state.page in PRIVATE_PAGES:
                st.session_state.page = selected_private
        else:
            st.markdown("""
            <div class='card-soft'>
                <div class='section-title'>Verrouillé</div>
                <div class='feature-text small'>
                    Connectez-vous avec un email professionnel pour accéder au dashboard, au diagnostic avancé et aux rapports.
                </div>
            </div>
            """, unsafe_allow_html=True)

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
        else:
            st.caption("Commencez par le test rapide pour obtenir une première qualification.")

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

        st.markdown("""
        <div class='card-soft sidebar-process' style='margin-top:.8rem;'>
            <div class='section-title'>Parcours</div>
            <div class='feature-text small'>1. Test rapide gratuit</div>
            <div class='feature-text small'>2. Connexion professionnelle</div>
            <div class='feature-text small'>3. Diagnostic avancé</div>
            <div class='feature-text small'>4. Score & rapport</div>
        </div>
        """, unsafe_allow_html=True)
