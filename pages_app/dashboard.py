import streamlit as st
import pandas as pd

from components.cards import render_page_header, render_kpi_card, render_feature_card
from components.charts import render_score_bars
from services.database import list_audits, delete_audit


def _build_history_df():
    audits = list_audits(st.session_state.user_id)
    if not audits:
        return pd.DataFrame(columns=["ID", "Entreprise", "Ville", "Score", "Grade", "Empreinte", "Date"])

    rows = []
    for audit in audits:
        rows.append({
            "ID": audit["id"],
            "Entreprise": audit["company_name"],
            "Ville": audit["company_city"],
            "Score": round(audit["global_score"] or 0, 0),
            "Grade": audit["grade"],
            "Empreinte": round(audit["total_tonnes"] or 0, 2),
            "Date": audit["created_at"][:10],
        })

    return pd.DataFrame(rows)


def render_dashboard():
    render_page_header(
        "Dashboard exécutif",
        "Vue d’ensemble persistante des pré-audits enregistrés dans votre base locale.",
        "Executive view"
    )

    history_df = _build_history_df()
    total_audits = len(history_df)
    avg_score = history_df["Score"].mean() if total_audits else 0
    avg_emissions = history_df["Empreinte"].mean() if total_audits else 0
    best_grade = history_df["Grade"].mode().iloc[0] if total_audits and not history_df["Grade"].mode().empty else "-"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Dossiers enregistrés", f"{total_audits}", "Persistés en base SQLite", "#6366f1")
    with c2:
        render_kpi_card("Score moyen", f"{avg_score:.0f}/100", "Maturité moyenne", "#10b981" if avg_score >= 70 else "#f59e0b" if avg_score >= 40 else "#ef4444")
    with c3:
        render_kpi_card("Empreinte moyenne", f"{avg_emissions:.2f} tCO₂e", "Pré-audit numérique", "#0f172a")
    with c4:
        render_kpi_card("Grade dominant", best_grade, "Lecture portfolio", "#8b5cf6")

    st.markdown("## Positionnement produit")
    a, b, c = st.columns(3)
    with a:
        render_feature_card(
            "Cible claire",
            "PME aéronautiques de rang 2 ou 3 soumises à une pression RSE croissante."
        )
    with b:
        render_feature_card(
            "Valeur business",
            "Transformer des exigences ESG complexes en outil simple, rapide et actionnable."
        )
    with c:
        render_feature_card(
            "Persistance fiable",
            "Historique stocké localement avec séparation par utilisateur et requêtes paramétrées."
        )

    st.markdown("## Historique des audits")

    if history_df.empty:
        st.info("Aucun audit enregistré. Terminez un diagnostic puis enregistrez-le depuis la page Score.")
        return

    st.dataframe(history_df, use_container_width=True, hide_index=True)

    st.markdown("### Benchmark interne des dossiers")
    score_rows = pd.DataFrame({
        "Pilier": history_df["Entreprise"].tolist(),
        "Score": history_df["Score"].tolist(),
        "Poids": [100] * len(history_df),
    })
    render_score_bars(score_rows)

    st.markdown("### Gestion")
    audit_id = st.selectbox("Audit à supprimer", history_df["ID"].tolist())
    if st.button("Supprimer l’audit sélectionné"):
        if delete_audit(st.session_state.user_id, int(audit_id)):
            st.success("Audit supprimé.")
            st.rerun()
        else:
            st.error("Suppression impossible.")
