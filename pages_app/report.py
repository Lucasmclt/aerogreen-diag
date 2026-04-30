import streamlit as st
from datetime import datetime

from services.calculations import build_recommendations, get_fit_result
from services.pdf_generator import create_premium_pdf_bytes


def render_report():
    st.markdown("## Rapport premium")

    if not st.session_state.diagnostic_done or not st.session_state.diagnostic_result:
        st.warning("Aucun diagnostic avancé n’a encore été généré.")
        if st.button("Aller au diagnostic avancé"):
            st.session_state.page = "Diagnostic avancé"
            st.rerun()
        return

    result = st.session_state.diagnostic_result
    recos = build_recommendations(st.session_state.diagnostic_inputs, result)

    fit_score = st.session_state.fit_score
    fit_result = st.session_state.fit_result or get_fit_result(fit_score)[0]

    company = {
        "company_name": st.session_state.company_name or "Entreprise non renseignée",
        "company_city": st.session_state.company_city or "Non renseignée",
        "company_sector": st.session_state.company_sector or "Non renseigné",
        "client_reference": st.session_state.client_reference or "N/A",
    }

    st.markdown(f"""
    <div class='card'>
        <div class='section-title'>Synthèse rapport</div>
        <div class='feature-title'>{company['company_name']}</div>
        <div class='feature-text'>
            Score global : <strong>{result['global_score']:.0f}/100</strong> ·
            Grade : <strong>{result['grade']}</strong> ·
            Empreinte estimée : <strong>{result['total_tonnes']:.2f} tCO₂e</strong>
        </div>
        <br>
        <div class='feature-text'>
            Le rapport PDF contient la synthèse exécutive, les scores par pilier,
            le détail des émissions et les recommandations prioritaires.
        </div>
    </div>
    """, unsafe_allow_html=True)

    pdf_bytes = create_premium_pdf_bytes(
        company=company,
        result=result,
        recommendations=recos,
        fit_score=fit_score,
        fit_result=fit_result,
    )

    st.download_button(
        label="Télécharger le rapport premium PDF",
        data=pdf_bytes,
        file_name=f"AeroGreen_Premium_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.markdown("### Aperçu des recommandations")
    for reco in recos:
        st.markdown(f"""
        <div class='card-soft'>
            <div class='section-title'>{reco['priority']}</div>
            <strong>{reco['title']}</strong>
            <div class='feature-text'>{reco['text']}</div>
        </div>
        """, unsafe_allow_html=True)
