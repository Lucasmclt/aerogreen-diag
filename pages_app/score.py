import streamlit as st

from components.cards import render_kpi_card, render_recommendation_card, render_page_header
from components.charts import render_emissions_bar_chart, render_score_radar, render_score_bars
from services.calculations import build_recommendations
from services.database import save_audit


def render_score():
    render_page_header(
        "Score AeroGreen",
        "Lecture synthétique du pré-audit avec score global, grade, risques et analyse par pilier.",
        "Scoring"
    )

    if not st.session_state.diagnostic_done or not st.session_state.diagnostic_result:
        st.warning("Aucun diagnostic avancé n’a encore été calculé.")
        if st.button("Lancer le diagnostic avancé"):
            st.session_state.page = "Diagnostic avancé"
            st.rerun()
        return

    result = st.session_state.diagnostic_result
    recos = build_recommendations(st.session_state.diagnostic_inputs, result)

    c1, c2, c3 = st.columns(3)

    with c1:
        render_kpi_card(
            "Score global",
            f"{result['global_score']:.0f}/100",
            result["risk_label"],
            result["grade_color"]
        )

    with c2:
        render_kpi_card(
            "Grade",
            result["grade"],
            "Lecture synthétique A-E",
            result["grade_color"]
        )

    with c3:
        render_kpi_card(
            "Empreinte estimée",
            f"{result['total_tonnes']:.2f} tCO₂e",
            "Pré-audit numérique",
            "#6366f1"
        )

    st.markdown("## Lecture par pilier")

    left, right = st.columns([1, 1])
    with left:
        render_score_radar(result["score_rows"])
    with right:
        render_score_bars(result["score_rows"])

    st.markdown("## Répartition carbone")
    render_emissions_bar_chart(result["df"])
    st.dataframe(result["df"], use_container_width=True, hide_index=True)

    st.markdown("## Recommandations prioritaires")
    cols = st.columns(min(3, len(recos)))

    for index, reco in enumerate(recos):
        with cols[index % len(cols)]:
            render_recommendation_card(reco["priority"], reco["title"], reco["text"])

    cta1, cta2 = st.columns(2)
    with cta1:
        if st.button("Enregistrer dans le dashboard"):
            company = {
                "company_name": st.session_state.company_name or "Entreprise non renseignée",
                "company_city": st.session_state.company_city or "N/A",
                "company_sector": st.session_state.company_sector or "Non renseigné",
                "client_reference": st.session_state.client_reference or "N/A",
                "contact_name": st.session_state.contact_name or "",
            }

            audit_id = save_audit(
                user_id=st.session_state.user_id,
                company=company,
                fit_score=st.session_state.fit_score,
                fit_result=st.session_state.fit_result,
                inputs=st.session_state.diagnostic_inputs,
                result=result,
            )
            st.success(f"Audit enregistré dans la espace sécurisé. ID dossier : {audit_id}.")
    with cta2:
        if st.button("Générer le rapport"):
            st.session_state.page = "Rapport"
            st.rerun()
