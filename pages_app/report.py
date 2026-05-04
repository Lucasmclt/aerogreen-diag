import streamlit as st
from datetime import datetime

from components.cards import render_page_header
from services.calculations import build_recommendations, get_fit_result
from services.pdf_generator import create_working_report_pdf_bytes
from services.database import list_audits, get_audit_by_public_code


def _go_to(page: str) -> None:
    st.session_state.page = page
    st.query_params["page"] = page
    st.rerun()


def render_report():
    render_page_header(
        "Rapport de travail",
        "Export PDF indicatif : contexte, score, preuves manquantes, recommandations et limites.",
        "Pièce maîtresse"
    )

    saved_audits = list_audits(st.session_state.user_id) if st.session_state.authenticated else []

    if not saved_audits:
        if st.session_state.get("diagnostic_done") and st.session_state.get("diagnostic_result"):
            st.markdown("""
            <div class='card-soft section-intro-card' style='border:1px solid rgba(99,102,241,.22);'>
                <div class='section-title'>Rapport pas encore enregistré</div>
                <strong>Un diagnostic est actif, mais aucun rapport PDF n’est encore disponible.</strong>
                <div class='feature-text'>
                    Passez par la page Score pour enregistrer le diagnostic, puis le rapport PDF pourra être généré.
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Enregistrer depuis la page Score", key="report_no_saved_score", use_container_width=True):
                _go_to("Score")
        else:
            st.markdown("""
            <div class='card-soft section-intro-card' style='border:1px solid rgba(99,102,241,.22);'>
                <div class='section-title'>Aucun rapport disponible</div>
                <strong>Aucun diagnostic chargé. Lancez un diagnostic ou chargez le cas d’étude fictif.</strong>
                <div class='feature-text'>
                    Pour vérifier le parcours PDF rapidement, chargez le cas d’étude fictif, consultez le dashboard, puis enregistrez
                    le diagnostic depuis la page Score.
                </div>
            </div>
            """, unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Aller au cas d’étude fictif", key="report_no_diag_case", use_container_width=True):
                    _go_to("Cas d’étude fictif")
            with c2:
                if st.button("Lancer le diagnostic guidé", key="report_no_diag_start", use_container_width=True):
                    _go_to("Diagnostic avancé")
        return

    audit_options = {
        f"{audit.get('public_code') or 'DIAG-SANS-CODE'} · {audit['company_name']} · {audit['created_at'][:10]}": audit.get("public_code")
        for audit in saved_audits
    }
    labels = list(audit_options.keys())
    current_code = st.session_state.get("current_audit_public_code", "")
    default_index = 0
    if current_code:
        for idx, label in enumerate(labels):
            if audit_options[label] == current_code:
                default_index = idx
                break
    selected_label = st.selectbox("Pré-diagnostic enregistré à exporter", labels, index=default_index)
    selected_code = audit_options[selected_label]
    selected_audit = get_audit_by_public_code(st.session_state.user_id, selected_code)

    if selected_audit is None:
        st.warning("Le pré-diagnostic sélectionné n’existe plus. Retournez au dashboard ou relancez un pré-diagnostic guidé.")
        return

    st.session_state.current_audit_public_code = selected_audit.get("public_code") or ""

    result = selected_audit["result"]
    inputs = selected_audit["inputs"]
    recos = build_recommendations(inputs, result)

    fit_score = selected_audit.get("fit_score") or 0
    fit_result = selected_audit.get("fit_result") or get_fit_result(fit_score)[0]

    company = {
        "company_name": selected_audit.get("company_name") or "—",
        "company_city": selected_audit.get("company_city") or "—",
        "company_sector": selected_audit.get("company_sector") or "—",
        "client_reference": selected_audit.get("client_reference") or "—",
    }
    public_code = selected_audit.get("public_code") or "DIAG-SANS-CODE"

    st.markdown(f"""
    <div class='card'>
        <div class='section-title'>Synthèse rapport</div>
        <div class='feature-title'>{company['company_name']}</div>
        <div class='feature-text'>
            Dossier : <strong>{public_code}</strong> ·
            Score indicatif : <strong>{result['global_score']:.0f}/100</strong> ·
            Grade : <strong>{result['grade']}</strong> ·
            Empreinte indicative : <strong>{result['total_tonnes']:.2f} tCO₂e</strong>
        </div>
        <br>
        <div class='feature-text'>
            Le rapport PDF contient le contexte, l’objectif du pré-diagnostic, le score indicatif,
            la lecture par pilier, les forces, les faiblesses, les preuves manquantes,
            les recommandations, les actions court terme et les limites méthodologiques.
        </div>
        <br>
        <div class='feature-text'>
            <strong>Document de travail indicatif — aucune certification, aucune conformité garantie.</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    pdf_bytes = create_working_report_pdf_bytes(
        company=company,
        result=result,
        recommendations=recos,
        fit_score=fit_score,
        fit_result=fit_result,
        inputs=inputs,
    )

    st.markdown("<div class='report-download-spacer'></div>", unsafe_allow_html=True)
    st.download_button(
        label="Télécharger le rapport exploratoire PDF",
        data=pdf_bytes,
        file_name=f"AeroGreen_Rapport_Travail_{public_code}_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.markdown("<div class='recommendation-section-spacer'></div>", unsafe_allow_html=True)
    st.markdown("### Aperçu des recommandations")
    for reco in recos:
        st.markdown(f"""
        <div class='card-soft report-reco-card'>
            <div class='section-title'>{reco['priority']}</div>
            <strong>{reco['title']}</strong>
            <div class='feature-text'>{reco['text']}</div>
        </div>
        """, unsafe_allow_html=True)
