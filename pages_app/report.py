import streamlit as st
from datetime import datetime

from components.cards import render_page_header
from services.calculations import build_recommendations, get_fit_result
from services.pdf_generator import create_working_report_pdf_bytes
from services.database import list_audits, get_audit_by_public_code


def render_report():
    render_page_header(
        "Rapport de travail",
        "Export PDF indicatif : synthèse, score, émissions estimées et recommandations prioritaires.",
        "Document de travail"
    )

    saved_audits = list_audits(st.session_state.user_id) if st.session_state.authenticated else []

    if not saved_audits:
        st.warning("Aucun pré-diagnostic enregistré n’est disponible pour générer un rapport de travail.")
        if st.button("Aller au pré-diagnostic guidé"):
            st.session_state.page = "Diagnostic avancé"
            st.query_params["page"] = "Diagnostic avancé"
            st.rerun()
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
            Le rapport PDF contient la synthèse indicative, les scores par pilier,
            le détail des émissions estimées, les recommandations prioritaires et une réserve méthodologique visible.
        </div>
        <br>
        <div class='feature-text'>
            <strong>Document de travail - À consolider avec preuves et référentiels officiels.</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    pdf_bytes = create_working_report_pdf_bytes(
        company=company,
        result=result,
        recommendations=recos,
        fit_score=fit_score,
        fit_result=fit_result,
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
