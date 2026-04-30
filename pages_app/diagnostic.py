import streamlit as st

from components.cards import render_kpi_card, render_section_intro
from components.charts import render_emissions_bar_chart
from services.calculations import (
    compute_diagnostic,
    get_score_color,
    get_maturity_label,
    get_fit_result,
    get_emissions_color
)


def render_diagnostic():
    st.markdown("## Pré-diagnostic carbone numérique")
    st.caption(
        "Version simplifiée. Cette étape pourra ensuite devenir un questionnaire avancé par lots : matériel, cloud, PLM, code, achats IT, conformité RSE."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        render_section_intro("Infrastructure", "Parc informatique")
        nb_laptops = st.number_input("Ordinateurs portables", 0, 5000, 0)
        nb_workstations = st.number_input("Stations de travail fixes", 0, 5000, 0)
        nb_screens = st.number_input("Écrans externes", 0, 5000, 0)

    with col2:
        render_section_intro("Données", "Stockage technique")
        storage_tb = st.number_input("Volume PLM / CAO stocké (To)", 0.0, 5000.0, 0.0)
        st.caption("Inclure serveurs internes, cloud, données projets et archives actives.")

    with col3:
        render_section_intro("Gouvernance", "Maturité RSE numérique")
        iso_14001 = st.checkbox("Certification ISO 14001")
        deee_management = st.checkbox("Gestion DEEE formalisée")
        responsible_sourcing = st.checkbox("Charte achats responsables IT")

    result = compute_diagnostic(
        nb_laptops=nb_laptops,
        nb_workstations=nb_workstations,
        nb_screens=nb_screens,
        storage_tb=storage_tb,
        iso_14001=iso_14001,
        deee_management=deee_management,
        responsible_sourcing=responsible_sourcing
    )

    df = result["df"]
    total_tonnes = result["total_tonnes"]
    maturity_score = result["maturity_score"]

    maturity_color = get_score_color(maturity_score)
    emissions_color = get_emissions_color(total_tonnes)

    st.markdown("## Synthèse")

    k1, k2, k3 = st.columns(3)

    with k1:
        render_kpi_card(
            "Empreinte estimée",
            f"{total_tonnes:.2f} tCO₂e",
            "Émissions numériques estimées",
            emissions_color
        )

    with k2:
        render_kpi_card(
            "Maturité RSE",
            f"{maturity_score:.0f}%",
            get_maturity_label(maturity_score),
            maturity_color
        )

    with k3:
        fit_score = st.session_state.fit_score if st.session_state.fit_test_done else 0
        fit_label, fit_color = get_fit_result(fit_score)

        render_kpi_card(
            "Adéquation service",
            f"{fit_score:.0f}%",
            fit_label,
            fit_color
        )

    st.markdown("## Répartition des émissions")
    render_emissions_bar_chart(df)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("## Premières recommandations")

    reco1, reco2, reco3 = st.columns(3)

    with reco1:
        st.markdown("""
        <div class='card'>
            <div class='section-title'>Matériel</div>
            <strong>Allonger le cycle de vie</strong>
            <p class='feature-text'>
                Prioriser la réparation, le reconditionné et l’extension de garantie sur les équipements critiques.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with reco2:
        st.markdown("""
        <div class='card'>
            <div class='section-title'>Données</div>
            <strong>Réduire le stockage actif</strong>
            <p class='feature-text'>
                Identifier les projets terminés et transférer les archives vers du stockage froid moins énergivore.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with reco3:
        st.markdown("""
        <div class='card'>
            <div class='section-title'>Gouvernance</div>
            <strong>Structurer la preuve RSE</strong>
            <p class='feature-text'>
                Formaliser une politique DEEE, une charte achats IT et des indicateurs simples de suivi.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.session_state["last_total_t"] = total_tonnes
    st.session_state["last_df"] = df
    st.session_state["last_maturity"] = maturity_score
