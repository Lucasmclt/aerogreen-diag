import streamlit as st
import pandas as pd

from components.cards import render_page_header, render_kpi_card, render_recommendation_card
from components.charts import render_score_bars
from services.calculations import (
    build_missing_evidence,
    build_recommendations,
    build_short_term_actions,
    build_strengths,
    build_weaknesses,
    compute_advanced_score,
)
from services.database import list_audits, delete_audit
from pages_app.case_study import CASE_STUDY_COMPANY, CASE_STUDY_INPUTS, _load_case_study_in_session


def _clear_deleted_diagnostic_session(public_code: str):
    if st.session_state.get("current_audit_public_code") == public_code or st.session_state.get("last_saved_diagnostic_id") == public_code:
        st.session_state.diagnostic_done = False
        st.session_state.diagnostic_result = None
        st.session_state.diagnostic_inputs = {}
        st.session_state.report_ready = False
        st.session_state.last_saved_diagnostic_key = ""
        st.session_state.last_saved_diagnostic_id = None
        st.session_state.current_audit_public_code = ""


def _build_history_df():
    audits = list_audits(st.session_state.user_id)
    if not audits:
        return pd.DataFrame(columns=["ID", "Code", "Entreprise", "Ville", "Score", "Grade", "Empreinte indicative", "Date"])

    rows = []
    for audit in audits:
        rows.append({
            "ID": audit["id"],
            "Code": audit.get("public_code") or "—",
            "Entreprise": audit["company_name"],
            "Ville": audit["company_city"],
            "Score": round(audit["global_score"] or 0, 0),
            "Grade": audit["grade"],
            "Empreinte indicative": round(audit["total_tonnes"] or 0, 2),
            "Date": audit["created_at"][:10],
        })

    return pd.DataFrame(rows)


def _active_company_label() -> str:
    if st.session_state.get("workspace_created") and st.session_state.get("company_name"):
        city = st.session_state.get("company_city") or "ville non renseignée"
        return f"{st.session_state.company_name} · {city}"
    return "Aucun diagnostic actif dans la session"


def _render_active_diagnostic():
    st.markdown("## Diagnostic actif")

    if not st.session_state.get("diagnostic_done") or not st.session_state.get("diagnostic_result"):
        st.markdown("""
        <div class='card-soft section-intro-card' style='border:1px solid rgba(99,102,241,.22);'>
            <div class='section-title'>Point de départ</div>
            <strong>Aucun diagnostic actif dans la session.</strong>
            <div class='feature-text'>
                Le dashboard ne cache rien : aucun score ne peut être affiché tant qu’un diagnostic n’a pas été lancé
                ou qu’un cas d’étude fictif n’a pas été chargé.
            </div>
        </div>
        """, unsafe_allow_html=True)
        col_start, col_case = st.columns(2)
        with col_start:
            if st.button("Lancer un diagnostic", key="dashboard_active_start", use_container_width=True):
                st.session_state.page = "Diagnostic avancé"
                st.query_params["page"] = "Diagnostic avancé"
                st.rerun()
        with col_case:
            if st.button("Charger le cas d’étude exemple", key="dashboard_active_case", use_container_width=True):
                result = compute_advanced_score(CASE_STUDY_INPUTS)
                _load_case_study_in_session(result)
                st.session_state.page = "Dashboard"
                st.query_params["page"] = "Dashboard"
                st.rerun()
        return

    result = st.session_state.diagnostic_result
    inputs = st.session_state.diagnostic_inputs
    recommendations = build_recommendations(inputs, result)
    missing = build_missing_evidence(inputs, result, limit=5)
    actions = build_short_term_actions(inputs, result)
    strengths = build_strengths(inputs, result)
    weaknesses = build_weaknesses(inputs, result)

    st.markdown(f"""
    <div class='card'>
        <div class='section-title'>Diagnostic affiché</div>
        <div class='feature-title'>{_active_company_label()}</div>
        <div class='feature-text'>
            Ce dashboard affiche le diagnostic actuellement chargé dans la session. Il peut s’agir d’un cas fictif
            ou d’un diagnostic saisi dans le questionnaire. Le score est une grille de maturité indicative, pas une conformité.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Score global", f"{result['global_score']:.0f}/100", result["risk_label"], result["grade_color"])
    with c2:
        render_kpi_card("Grade", result["grade"], "Lecture synthétique A-E", result["grade_color"])
    with c3:
        render_kpi_card("Empreinte indicative", f"{result['total_tonnes']:.2f} tCO₂e", "Ordre de grandeur", "#6366f1")
    with c4:
        render_kpi_card("Preuves à prioriser", str(len(missing)), "Éléments documentaires", "#f59e0b")

    left, right = st.columns([1, 1])
    with left:
        render_score_bars(result["score_rows"])
    with right:
        st.markdown("### Priorités concrètes")
        for reco in recommendations[:3]:
            render_recommendation_card(reco["priority"], reco["title"], reco["text"])

    st.markdown("### Forces / faiblesses")
    f_col, w_col = st.columns(2)
    with f_col:
        st.markdown("**Forces identifiées**")
        for item in strengths:
            st.markdown(f"- {item}")
    with w_col:
        st.markdown("**Points faibles à traiter**")
        for item in weaknesses:
            st.markdown(f"- {item}")

    st.markdown("### Preuves manquantes ou à consolider")
    missing_df = pd.DataFrame(missing)[["criterion", "expected", "example", "limit"]]
    missing_df.columns = ["Critère", "Preuve attendue", "Exemple concret", "Limite"]
    st.dataframe(missing_df, use_container_width=True, hide_index=True)

    st.markdown("### Actions court terme")
    for action in actions:
        st.markdown(f"- {action}")

    cta1, cta2 = st.columns(2)
    with cta1:
        if st.button("Générer / télécharger le rapport", key="dashboard_to_report", use_container_width=True):
            target_page = "Rapport" if st.session_state.get("current_audit_public_code") else "Score"
            st.session_state.page = target_page
            st.query_params["page"] = target_page
            st.rerun()
    with cta2:
        if st.button("Modifier / relancer le diagnostic", key="dashboard_to_diag", use_container_width=True):
            st.session_state.page = "Diagnostic avancé"
            st.query_params["page"] = "Diagnostic avancé"
            st.rerun()


def render_dashboard():
    render_page_header(
        "Dashboard du prototype",
        "Lecture du diagnostic actif, historique local et preuves à prioriser.",
        "Suivi portfolio"
    )

    history_df = _build_history_df()
    has_audits = not history_df.empty

    avg_score = history_df["Score"].mean() if has_audits else None
    avg_emissions = history_df["Empreinte indicative"].mean() if has_audits else None

    c1, c2, c3 = st.columns(3)
    with c1:
        render_kpi_card("Pré-diagnostics enregistrés", f"{len(history_df)}", "Cas sauvegardés localement", "#6366f1")
    with c2:
        render_kpi_card(
            "Score moyen",
            "—" if avg_score is None else f"{avg_score:.0f}/100",
            "Aucun score enregistré" if avg_score is None else "Maturité moyenne indicative",
            "#64748b" if avg_score is None else "#10b981" if avg_score >= 70 else "#f59e0b" if avg_score >= 40 else "#ef4444"
        )
    with c3:
        render_kpi_card(
            "Empreinte indicative moyenne",
            "—" if avg_emissions is None else f"{avg_emissions:.2f} tCO₂e",
            "Aucune empreinte enregistrée" if avg_emissions is None else "Ordre de grandeur moyen",
            "#64748b" if avg_emissions is None else "#0f172a"
        )

    _render_active_diagnostic()

    st.markdown("## Historique local")
    if history_df.empty:
        st.info("Aucun pré-diagnostic enregistré. Le cas d’étude peut être chargé pour comprendre le parcours, puis un diagnostic réel peut être lancé.")
    else:
        st.dataframe(history_df, use_container_width=True, hide_index=True)

        st.markdown("### Gestion des diagnostics enregistrés")
        audit_labels = [f"{row['Code']} · {row['Entreprise']} · {row['Date']}" for _, row in history_df.iterrows()]
        audit_map = {label: (int(row["ID"]), str(row["Code"])) for label, (_, row) in zip(audit_labels, history_df.iterrows())}
        selected_audit_label = st.selectbox("Pré-diagnostic à supprimer", audit_labels, key="delete_basic_audit")
        if st.button("Supprimer le pré-diagnostic sélectionné"):
            audit_id, audit_code = audit_map[selected_audit_label]
            if delete_audit(st.session_state.user_id, audit_id):
                _clear_deleted_diagnostic_session(audit_code)
                st.success("Pré-diagnostic supprimé.")
                st.rerun()
            st.error("Suppression impossible.")
