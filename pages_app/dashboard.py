import streamlit as st
import pandas as pd

from components.cards import render_page_header, render_kpi_card, render_feature_card
from components.charts import render_score_bars
from services.calculations import get_grade


def _build_history_df():
    history = st.session_state.get("audit_history", [])
    if not history:
        return pd.DataFrame(columns=["Entreprise", "Ville", "Score", "Grade", "Empreinte", "Date"])
    return pd.DataFrame(history)


def render_dashboard():
    render_page_header(
        "Dashboard exécutif",
        "Vue d’ensemble orientée décision pour démonstration jury, investisseur ou client B2B.",
        "Executive view"
    )

    history_df = _build_history_df()
    total_audits = len(history_df)
    avg_score = history_df["Score"].mean() if total_audits else 0
    avg_emissions = history_df["Empreinte"].mean() if total_audits else 0
    best_grade = history_df["Grade"].mode().iloc[0] if total_audits and not history_df["Grade"].mode().empty else "-"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Dossiers analysés", f"{total_audits}", "Historique du workspace", "#6366f1")
    with c2:
        render_kpi_card("Score moyen", f"{avg_score:.0f}/100", "Maturité moyenne des dossiers", "#10b981" if avg_score >= 70 else "#f59e0b" if avg_score >= 40 else "#ef4444")
    with c3:
        render_kpi_card("Empreinte moyenne", f"{avg_emissions:.2f} tCO₂e", "Pré-audit numérique", "#0f172a")
    with c4:
        render_kpi_card("Grade dominant", best_grade, "Lecture synthétique portfolio", "#8b5cf6")

    st.markdown("## Positionnement produit")
    a, b, c = st.columns(3)
    with a:
        render_feature_card(
            "Cible claire",
            "PME aéronautiques de rang 2 ou 3 soumises à une pression RSE croissante de la chaîne de sous-traitance."
        )
    with b:
        render_feature_card(
            "Valeur business",
            "Transformer des exigences ESG complexes en outil simple, rapide et actionnable sans audit lourd."
        )
    with c:
        render_feature_card(
            "Traction possible",
            "Offre locale à Toulouse, facilement démontrable, extensible en SaaS de niche ou mission AMOA."
        )

    st.markdown("## Historique des audits")
    if history_df.empty:
        st.info("Aucun audit enregistré. Termine un diagnostic puis enregistre-le depuis la page Score.")
    else:
        # Display last audits
        st.dataframe(history_df.sort_values("Date", ascending=False), use_container_width=True, hide_index=True)

        score_rows = pd.DataFrame({
            "Pilier": history_df["Entreprise"].tolist(),
            "Score": history_df["Score"].tolist(),
            "Poids": [100] * len(history_df),
        })
        st.markdown("### Benchmark interne des dossiers")
        render_score_bars(score_rows.rename(columns={"Entreprise": "Pilier"}))
