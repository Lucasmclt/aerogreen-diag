import streamlit as st

from components.cards import render_kpi_card, render_recommendation_card
from components.charts import render_emissions_bar_chart, render_score_radar, render_score_bars
from services.calculations import build_recommendations


def render_score():
    st.markdown("## Score AeroGreen")

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

    if st.button("Générer le rapport"):
        st.session_state.page = "Rapport"
        st.rerun()
