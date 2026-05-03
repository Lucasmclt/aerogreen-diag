import streamlit as st
import pandas as pd

from components.cards import render_page_header, render_kpi_card, render_recommendation_card
from components.charts import render_score_bars, render_emissions_bar_chart
from services.calculations import compute_advanced_score, build_recommendations


CASE_STUDY_COMPANY = {
    "company_name": "Occitaero Components",
    "contact_name": "Responsable méthodes / SI",
    "company_city": "Toulouse",
    "company_sector": "Sous-traitant aéronautique rang 2",
    "client_reference": "CAS-FICTIF-AERO-01",
}


CASE_STUDY_INPUTS = {
    "employees": 85,
    "sites": 2,
    "annual_revenue": 11_500_000,
    "critical_customer": True,
    "nb_laptops": 54,
    "nb_workstations": 31,
    "nb_screens": 92,
    "nb_servers": 3,
    "nb_cloud_vm": 8,
    "lifecycle_years": 4,
    "it_inventory": True,
    "storage_active_tb": 42.0,
    "storage_cold_tb": 18.0,
    "archive_policy": "Informelle",
    "retention_policy": "Partielle",
    "plm_cleanup": "Rarement",
    "iso_14001": False,
    "deee_management": True,
    "responsible_sourcing": False,
    "rse_owner": True,
    "supplier_policy": False,
    "rse_frequency": "Suivi annuel",
    "refurbished_policy": False,
    "repair_policy": True,
    "purchase_centralized": True,
    "short_trips": 9,
    "long_trips": 2,
}


def _load_case_study_in_session(result: dict):
    st.session_state.workspace_created = True
    st.session_state.company_name = CASE_STUDY_COMPANY["company_name"]
    st.session_state.contact_name = CASE_STUDY_COMPANY["contact_name"]
    st.session_state.company_city = CASE_STUDY_COMPANY["company_city"]
    st.session_state.company_sector = CASE_STUDY_COMPANY["company_sector"]
    st.session_state.client_reference = CASE_STUDY_COMPANY["client_reference"]
    st.session_state.diagnostic_inputs = CASE_STUDY_INPUTS.copy()
    st.session_state.diagnostic_result = result
    st.session_state.diagnostic_done = True
    st.session_state.report_ready = True


def render_case_study():
    result = compute_advanced_score(CASE_STUDY_INPUTS)
    recos = build_recommendations(CASE_STUDY_INPUTS, result)

    render_page_header(
        "Cas d’étude fictif",
        "Exemple pédagogique pour comprendre ce qu’il faut lancer depuis le dashboard et comment lire un pré-diagnostic.",
        "Simulation non officielle"
    )

    st.markdown("""
    <div class='card-soft' style='border:1px solid rgba(99,102,241,.22);'>
        <div class='section-title'>Prototype portfolio — non officiel</div>
        <strong>Occitaero Components est une PME fictive.</strong>
        <div class='feature-text'>
            Ce cas sert uniquement à montrer le parcours, le type de données collectées, la restitution du score et les recommandations.
            Il ne constitue ni une preuve RSE, ni un audit carbone, ni une évaluation EcoVadis.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Contexte simulé")
    st.markdown("""
    <div class='card'>
        <p class='feature-text'>
            Occitaero Components est imaginée comme un sous-traitant aéronautique toulousain de rang 2, avec un usage important
            de postes CAO, de données PLM, d’archives techniques et quelques contraintes client sur la structuration des preuves RSE.
            L’entreprise a commencé à formaliser certains éléments, mais son suivi numérique responsable reste partiel.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Entreprise", CASE_STUDY_COMPANY["company_name"], "PME fictive", "#6366f1")
    with c2:
        render_kpi_card("Effectif", f"{CASE_STUDY_INPUTS['employees']}", "salariés simulés", "#0f172a")
    with c3:
        render_kpi_card("Score indicatif", f"{result['global_score']:.0f}/100", result["risk_label"], result["grade_color"])
    with c4:
        render_kpi_card("Empreinte estimée", f"{result['total_tonnes']:.2f} tCO₂e", "ordre de grandeur", "#8b5cf6")

    st.markdown("## Lecture du diagnostic exemple")
    left, right = st.columns([1, 1])
    with left:
        st.markdown("""
        <div class='card-soft'>
            <div class='section-title'>Interprétation</div>
            <strong>Le score sert à repérer les zones faibles, pas à classer officiellement l’entreprise.</strong>
            <div class='feature-text'>
                Dans cet exemple, les axes les plus sensibles sont la gouvernance RSE numérique, la formalisation fournisseur
                et la gestion des données PLM/CAO. La valeur du prototype est de transformer ces constats en plan de discussion.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with right:
        score_rows = pd.DataFrame(result["score_rows"])
        render_score_bars(score_rows)

    st.markdown("## Répartition carbone indicative")
    render_emissions_bar_chart(result["df"])
    st.dataframe(result["df"], use_container_width=True, hide_index=True)

    st.markdown("## Recommandations de travail")
    cols = st.columns(min(3, len(recos)))
    for index, reco in enumerate(recos):
        with cols[index % len(cols)]:
            render_recommendation_card(reco["priority"], reco["title"], reco["text"])

    st.markdown("""
    <div class='card-soft'>
        <div class='section-title'>À retenir</div>
        <strong>Ce cas d’étude montre le livrable attendu après un diagnostic.</strong>
        <div class='feature-text'>
            Depuis le dashboard, l’utilisateur doit soit lancer son premier diagnostic réel, soit consulter ce cas fictif
            pour comprendre la logique de l’application avant de saisir ses propres données.
        </div>
    </div>
    """, unsafe_allow_html=True)

    cta1, cta2 = st.columns(2)
    with cta1:
        if st.button("Lancer mon premier diagnostic", key="case_start_real_diag", use_container_width=True):
            if st.session_state.get("authenticated"):
                st.session_state.page = "Diagnostic avancé"
                st.query_params["page"] = "Diagnostic avancé"
            else:
                st.session_state.page = "Connexion"
                st.query_params["page"] = "Connexion"
            st.rerun()
    with cta2:
        if st.button("Charger ce cas dans le score", key="case_load_score", use_container_width=True):
            if not st.session_state.get("authenticated"):
                st.session_state.page = "Connexion"
                st.query_params["page"] = "Connexion"
                st.rerun()
            _load_case_study_in_session(result)
            st.session_state.page = "Score"
            st.query_params["page"] = "Score"
            st.rerun()
