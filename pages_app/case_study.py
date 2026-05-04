import streamlit as st
import pandas as pd

from components.cards import render_page_header, render_kpi_card, render_recommendation_card
from components.charts import render_score_bars, render_emissions_bar_chart
from services.calculations import (
    build_missing_evidence,
    build_recommendations,
    build_short_term_actions,
    build_strengths,
    build_weaknesses,
    compute_advanced_score,
)


CASE_STUDY_COMPANY = {
    "company_name": "AeroPart Occitanie",
    "contact_name": "Responsable méthodes / SI",
    "company_city": "Blagnac",
    "company_sector": "PME industrielle fictive · sous-traitant aéronautique rang 2",
    "client_reference": "CAS-FICTIF-AERO-01",
}


CASE_STUDY_INPUTS = {
    "employees": 80,
    "sites": 2,
    "annual_revenue": 11_500_000,
    "critical_customer": True,
    "nb_laptops": 52,
    "nb_workstations": 30,
    "nb_screens": 88,
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
    "reduction_target": "Intention",
    "short_trips": 9,
    "long_trips": 2,
}


def _go_to(page: str) -> None:
    st.session_state.page = page
    st.query_params["page"] = page
    st.rerun()


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
    st.session_state.current_audit_public_code = ""
    st.session_state.last_saved_diagnostic_key = ""
    st.session_state.last_saved_diagnostic_id = None
    st.session_state.case_study_loaded = True


def render_case_study():
    result = compute_advanced_score(CASE_STUDY_INPUTS)
    recos = build_recommendations(CASE_STUDY_INPUTS, result)
    missing = build_missing_evidence(CASE_STUDY_INPUTS, result, limit=6)
    actions = build_short_term_actions(CASE_STUDY_INPUTS, result)
    strengths = build_strengths(CASE_STUDY_INPUTS, result)
    weaknesses = build_weaknesses(CASE_STUDY_INPUTS, result)

    render_page_header(
        "Cas d’étude fictif",
        "AeroPart Occitanie illustre le parcours attendu : contexte, diagnostic, preuves, recommandations et limites.",
        "Simulation non officielle"
    )

    st.markdown("""
    <div class='card-soft' style='border:1px solid rgba(99,102,241,.22);'>
        <div class='section-title'>Prototype portfolio — non officiel</div>
        <strong>Ce cas est volontairement fictif.</strong>
        <div class='feature-text'>
            Il sert à montrer comment une PME industrielle pourrait structurer un premier dossier de preuves RSE numériques
            avant une demande client ou fournisseur. Il ne constitue ni audit, ni certification, ni notation officielle.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get("case_study_loaded"):
        st.success("Cas d’étude chargé. Vous pouvez maintenant consulter le dashboard.")
        if st.button("Aller au Dashboard", key="case_loaded_go_dashboard", use_container_width=True):
            _go_to("Dashboard")

    st.markdown("## Contexte simulé")
    st.markdown("""
    <div class='card'>
        <p class='feature-text'>
            AeroPart Occitanie est une PME fictive de 80 salariés située autour de Toulouse. Elle fabrique des composants
            pour un donneur d’ordre aéronautique, utilise des stations CAO, un environnement PLM/PDM, des archives techniques
            et un parc informatique mixte. L’entreprise reçoit une demande client sur ses pratiques RSE / numérique responsable.
            Elle dispose de preuves partielles, mais elles sont dispersées entre DSI, méthodes, qualité et achats.
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
            <strong>Le signal intéressant n’est pas le score : c’est la traduction en preuves et actions.</strong>
            <div class='feature-text'>
                Ici, l’entreprise a déjà un inventaire IT et une gestion DEEE, mais elle reste fragile sur les critères
                fournisseurs, la formalisation des achats IT et la conservation des données CAO/PLM.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("**Forces identifiées**")
        for item in strengths:
            st.markdown(f"- {item}")
        st.markdown("**Faiblesses principales**")
        for item in weaknesses:
            st.markdown(f"- {item}")
    with right:
        render_score_bars(result["score_rows"])

    st.markdown("## Preuves à consolider")
    missing_df = pd.DataFrame(missing)[["criterion", "expected", "example", "limit"]]
    missing_df.columns = ["Critère", "Preuve attendue", "Exemple concret", "Limite"]
    st.dataframe(missing_df, use_container_width=True, hide_index=True)

    st.markdown("## Répartition carbone indicative")
    render_emissions_bar_chart(result["df"])
    st.dataframe(result["df"], use_container_width=True, hide_index=True)

    st.markdown("## Recommandations de travail")
    cols = st.columns(min(3, len(recos)))
    for index, reco in enumerate(recos):
        with cols[index % len(cols)]:
            render_recommendation_card(reco["priority"], reco["title"], reco["text"])

    st.markdown("## Actions court terme")
    for action in actions:
        st.markdown(f"- {action}")

    st.markdown("""
    <div class='card-soft'>
        <div class='section-title'>À retenir</div>
        <strong>Ce cas d’étude sert à éviter le dashboard vide.</strong>
        <div class='feature-text'>
            Il peut être chargé dans la session pour générer un score, afficher les preuves manquantes et produire un rapport PDF.
        </div>
    </div>
    """, unsafe_allow_html=True)

    cta1, cta2, cta3 = st.columns(3)
    with cta1:
        if st.button("Charger ce cas dans la session", key="case_load_score", use_container_width=True):
            _load_case_study_in_session(result)
            st.rerun()
    with cta2:
        if st.button("Voir le Dashboard", key="case_go_dashboard", use_container_width=True):
            if not st.session_state.get("diagnostic_done") or not st.session_state.get("diagnostic_result"):
                _load_case_study_in_session(result)
            _go_to("Dashboard")
    with cta3:
        if st.button("Lancer mon propre diagnostic", key="case_start_real_diag", use_container_width=True):
            _go_to("Diagnostic avancé")
