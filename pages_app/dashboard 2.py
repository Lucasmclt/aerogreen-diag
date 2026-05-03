
import streamlit as st
import pandas as pd

from components.cards import render_page_header, render_kpi_card
from components.charts import render_score_bars
from services.database import list_audits, delete_audit, list_deep_audits, delete_deep_audit


def _clear_deleted_diagnostic_session(public_code: str):
    if st.session_state.get("current_audit_public_code") == public_code or st.session_state.get("last_saved_diagnostic_id") == public_code:
        st.session_state.diagnostic_done = False
        st.session_state.diagnostic_result = None
        st.session_state.diagnostic_inputs = {}
        st.session_state.report_ready = False
        st.session_state.last_saved_diagnostic_key = ""
        st.session_state.last_saved_diagnostic_id = None
        st.session_state.current_audit_public_code = ""


def _clear_deleted_deep_session(public_code: str):
    if st.session_state.get("current_deep_public_code") == public_code:
        st.session_state.current_deep_public_code = ""


def _build_history_df():
    audits = list_audits(st.session_state.user_id)
    if not audits:
        return pd.DataFrame(columns=["ID", "Code", "Entreprise", "Ville", "Score", "Grade", "Empreinte", "Date"])

    rows = []
    for audit in audits:
        rows.append({
            "ID": audit["id"],
            "Code": audit.get("public_code") or "—",
            "Entreprise": audit["company_name"],
            "Ville": audit["company_city"],
            "Score": round(audit["global_score"] or 0, 0),
            "Grade": audit["grade"],
            "Empreinte": round(audit["total_tonnes"] or 0, 2),
            "Date": audit["created_at"][:10],
        })

    return pd.DataFrame(rows)


def _build_deep_df():
    audits = list_deep_audits(st.session_state.user_id)
    if not audits:
        return pd.DataFrame(columns=["ID", "Code", "Entreprise", "Ville", "Objectif", "Score approfondi", "Documents", "REEN", "CAO/PLM", "Date"])

    rows = []
    for audit in audits:
        rows.append({
            "ID": audit["id"],
            "Code": audit.get("public_code") or "—",
            "Entreprise": audit["company_name"],
            "Ville": audit["company_city"],
            "Objectif": audit["target_level"] or "Non défini",
            "Score approfondi": round(audit["global_score"] or 0, 0),
            "Documents": round(audit["documents_score"] or 0, 0),
            "REEN": round(audit["reen_score"] or 0, 0),
            "CAO/PLM": round(audit["plm_score"] or 0, 0),
            "Date": audit["created_at"][:10],
        })

    return pd.DataFrame(rows)


def render_dashboard():
    render_page_header(
        "Démonstrateur de suivi",
        "Synthèse indicative des diagnostics et dossiers de travail RSE enregistrés dans le prototype.",
        "Suivi des cas d’étude"
    )

    history_df = _build_history_df()
    deep_df = _build_deep_df()

    total_audits = len(history_df)
    total_deep = len(deep_df)
    has_audits = total_audits > 0

    avg_score = history_df["Score"].mean() if has_audits else None
    avg_emissions = history_df["Empreinte"].mean() if has_audits else None
    best_grade = history_df["Grade"].mode().iloc[0] if has_audits and not history_df["Grade"].mode().empty else "—"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Diagnostics enregistrés", f"{total_audits}", "Cas d’étude sauvegardés", "#6366f1")
    with c2:
        render_kpi_card(
            "Score moyen",
            "—" if avg_score is None else f"{avg_score:.0f}/100",
            "Aucun score enregistré" if avg_score is None else "Maturité moyenne",
            "#64748b" if avg_score is None else "#10b981" if avg_score >= 70 else "#f59e0b" if avg_score >= 40 else "#ef4444"
        )
    with c3:
        render_kpi_card(
            "Empreinte moyenne",
            "—" if avg_emissions is None else f"{avg_emissions:.2f} tCO₂e",
            "Aucune empreinte enregistrée" if avg_emissions is None else "Synthèse indicative",
            "#64748b" if avg_emissions is None else "#0f172a"
        )
    with c4:
        render_kpi_card("Dossiers de travail RSE", f"{total_deep}", "Analyses approfondies sauvegardées", "#8b5cf6")

    st.markdown("## Diagnostics enregistrés dans le prototype")
    if history_df.empty:
        st.info("Lancez un diagnostic pour générer un premier cas d’étude enregistré.")
    else:
        st.dataframe(history_df, use_container_width=True, hide_index=True)

        st.markdown("### Comparaison indicative des cas enregistrés")
        score_rows = pd.DataFrame({
            "Pilier": history_df["Entreprise"].tolist(),
            "Score": history_df["Score"].tolist(),
            "Poids": [100] * len(history_df),
        })
        render_score_bars(score_rows)

        st.markdown("### Gestion des diagnostics")
        audit_labels = [f"{row['Code']} · {row['Entreprise']} · {row['Date']}" for _, row in history_df.iterrows()]
        audit_map = {label: (int(row["ID"]), str(row["Code"])) for label, (_, row) in zip(audit_labels, history_df.iterrows())}
        selected_audit_label = st.selectbox("Diagnostic à supprimer", audit_labels, key="delete_basic_audit")
        if st.button("Supprimer le diagnostic sélectionné"):
            audit_id, audit_code = audit_map[selected_audit_label]
            if delete_audit(st.session_state.user_id, audit_id):
                _clear_deleted_diagnostic_session(audit_code)
                st.success("Diagnostic supprimé.")
                st.rerun()
            else:
                st.error("Suppression impossible.")

    st.markdown("## Dossiers de travail RSE")
    if deep_df.empty:
        st.info("Aucun dossier de travail RSE enregistré. Complétez l’analyse approfondie pour créer un premier cas.")
    else:
        st.dataframe(deep_df, use_container_width=True, hide_index=True)

        st.markdown("### Gestion des dossiers RSE")
        deep_labels = [f"{row['Code']} · {row['Entreprise']} · {row['Date']}" for _, row in deep_df.iterrows()]
        deep_map = {label: (int(row["ID"]), str(row["Code"])) for label, (_, row) in zip(deep_labels, deep_df.iterrows())}
        selected_deep_label = st.selectbox("Dossier de travail à supprimer", deep_labels, key="delete_deep_audit")
        if st.button("Supprimer le dossier de travail sélectionné"):
            deep_id, deep_code = deep_map[selected_deep_label]
            if delete_deep_audit(st.session_state.user_id, deep_id):
                _clear_deleted_deep_session(deep_code)
                st.success("Dossier de travail supprimé.")
                st.rerun()
            else:
                st.error("Suppression impossible.")
