import streamlit as st

from services.calculations import compute_fit_score, get_fit_result


def render_fit_test():
    st.markdown("## Test rapide d’adéquation")
    st.caption(
        "Objectif : déterminer si AeroGreen est pertinent pour l’entreprise avant de lancer un diagnostic plus complet."
    )

    with st.container():
        taille = st.selectbox(
            "Taille de l’entreprise",
            [
                "Moins de 10 salariés",
                "10 à 50 salariés",
                "50 à 250 salariés",
                "Plus de 250 salariés"
            ]
        )

        secteur = st.selectbox(
            "Lien avec l’aéronautique",
            [
                "Sous-traitant aéronautique rang 2 ou 3",
                "Fournisseur industriel hors aéronautique",
                "Bureau d’études / ingénierie",
                "Entreprise sans lien direct"
            ]
        )

        pression_rse = st.selectbox(
            "Avez-vous déjà reçu des demandes RSE de clients ou donneurs d’ordre ?",
            [
                "Oui, régulièrement",
                "Oui, ponctuellement",
                "Pas encore, mais c’est probable",
                "Non"
            ]
        )

        donnees_plm = st.selectbox(
            "Votre activité utilise-t-elle des données techniques lourdes ?",
            [
                "Oui, PLM / CAO / données projets importantes",
                "Oui, mais volume modéré",
                "Peu",
                "Non"
            ]
        )

        maturite_rse_initiale = st.selectbox(
            "Niveau actuel de structuration RSE",
            [
                "Aucune démarche structurée",
                "Quelques actions isolées",
                "Démarche en cours",
                "Démarche déjà avancée"
            ]
        )

    if st.button("Analyser l’adéquation"):
        score = compute_fit_score(
            taille=taille,
            secteur=secteur,
            pression_rse=pression_rse,
            donnees_plm=donnees_plm,
            maturite_rse_initiale=maturite_rse_initiale
        )

        label, color = get_fit_result(score)

        st.session_state.fit_score = score
        st.session_state.fit_test_done = True
        st.session_state.fit_result = label

        st.markdown(f"""
        <div class='card'>
            <div class='section-title'>Résultat du test</div>
            <div class='kpi' style='color:{color};'>{score:.0f}%</div>
            <div style='font-weight:700; margin-bottom:8px;'>{label}</div>
            <div class='feature-text'>
                Ce score indique le niveau de pertinence d’un pré-diagnostic carbone numérique pour cette entreprise.
            </div>
        </div>
        """, unsafe_allow_html=True)

        if score >= 70:
            st.success(
                "AeroGreen est très pertinent pour ce profil. Le diagnostic peut apporter une vraie valeur commerciale et opérationnelle."
            )
        elif score >= 40:
            st.warning(
                "AeroGreen peut être utile, mais il faut préciser les attentes client et le niveau réel de données disponibles."
            )
        else:
            st.error(
                "AeroGreen n’est probablement pas prioritaire pour cette entreprise à ce stade."
            )

    if st.session_state.fit_test_done:
        if st.button("Passer au diagnostic"):
            st.session_state.page = "Diagnostic"
            st.rerun()
