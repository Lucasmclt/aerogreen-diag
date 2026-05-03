import streamlit as st
import hashlib
import json

from components.cards import render_kpi_card, render_recommendation_card, render_page_header
from components.charts import render_emissions_bar_chart, render_score_radar, render_score_bars
from services.calculations import build_recommendations
from services.database import save_audit, audit_public_code_exists

def _diagnostic_signature(inputs, result):
    payload = {
        "inputs": inputs,
        "global_score": result.get("global_score"),
        "grade": result.get("grade"),
        "total_tonnes": result.get("total_tonnes"),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _missing_required_company_fields() -> list[str]:
    required = {
        "company_name": "Nom de l’entreprise",
        "contact_name": "Référent / contact",
        "company_city": "Ville",
        "client_reference": "Référence dossier",
    }
    return [label for key, label in required.items() if not str(st.session_state.get(key, "")).strip()]


def _ensure_company_info_before_save() -> bool:
    missing = _missing_required_company_fields()
    if not missing:
        return True
    st.error("Impossible d’enregistrer : informations du dossier obligatoires manquantes — " + ", ".join(missing) + ".")
    if st.button("Compléter les informations du dossier", key="score_complete_company_info", use_container_width=True):
        st.session_state.wizard_step = 1
        st.session_state.page = "Diagnostic avancé"
        st.query_params["page"] = "Diagnostic avancé"
        st.rerun()
    return False


def _save_current_diagnostic_if_needed(result):
    signature = _diagnostic_signature(st.session_state.diagnostic_inputs, result)
    existing_code = st.session_state.get("last_saved_diagnostic_id")
    if (
        st.session_state.get("last_saved_diagnostic_key") == signature
        and existing_code
        and audit_public_code_exists(st.session_state.user_id, existing_code)
    ):
        st.session_state.current_audit_public_code = existing_code
        return existing_code

    if not _ensure_company_info_before_save():
        return None

    company = {
        "company_name": st.session_state.company_name.strip(),
        "company_city": st.session_state.company_city.strip(),
        "company_sector": st.session_state.company_sector or "Non renseigné",
        "client_reference": st.session_state.client_reference.strip(),
        "contact_name": st.session_state.contact_name.strip(),
    }

    audit_id = save_audit(
        user_id=st.session_state.user_id,
        company=company,
        fit_score=st.session_state.fit_score,
        fit_result=st.session_state.fit_result,
        inputs=st.session_state.diagnostic_inputs,
        result=result,
    )

    st.session_state.last_saved_diagnostic_key = signature
    st.session_state.last_saved_diagnostic_id = audit_id
    st.session_state.current_audit_public_code = audit_id
    return audit_id



def render_score():
    render_page_header(
        "Score indicatif AeroGreen",
        "Lecture de maturité numérique responsable issue du questionnaire déclaratif.",
        "Scoring indicatif"
    )

    st.caption("Score indicatif calculé à partir des réponses déclaratives. Il ne constitue pas une notation officielle.")

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
            "Score indicatif",
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
            "Empreinte indicative",
            f"{result['total_tonnes']:.2f} tCO₂e",
            "Estimation indicative",
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

    st.markdown("<div class='score-action-spacer'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("""
        <div class='ag-bottom-card-marker ag-bottom-card-next-steps'></div>
        <div class='ag-bottom-card-header'>
            <div class='section-title'>Étapes suivantes</div>
            <strong>Choisir la suite du diagnostic</strong>
            <div class='feature-text small'>Enregistrez ce cas, générez un rapport exploratoire ou structurez un dossier RSE numérique de travail.</div>
        </div>
        """, unsafe_allow_html=True)
        cta1, cta2, cta3 = st.columns(3)
        with cta1:
            if st.button("Enregistrer le diagnostic", use_container_width=True):
                audit_id = _save_current_diagnostic_if_needed(result)
                if audit_id:
                    st.success(f"Diagnostic enregistré. Code dossier : {audit_id}.")
        with cta2:
            if st.button("Générer le rapport", use_container_width=True):
                audit_id = _save_current_diagnostic_if_needed(result)
                if not audit_id:
                    return
                st.session_state.page = "Rapport"
                st.query_params["page"] = "Rapport"
                st.rerun()
        with cta3:
            if st.button("Compléter le dossier RSE", use_container_width=True):
                audit_id = _save_current_diagnostic_if_needed(result)
                if not audit_id:
                    return
                st.session_state.page = "Dossier RSE"
                st.query_params["page"] = "Dossier RSE"
                st.rerun()
