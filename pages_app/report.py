import streamlit as st
from datetime import datetime

from services.calculations import get_fit_result
from services.pdf_generator import create_pdf_bytes


def render_report():
    st.markdown("## Rapport de pré-audit")

    if st.session_state.last_total_t is None or st.session_state.last_df is None:
        st.warning("Aucun diagnostic n’a encore été généré. Lance d’abord le pré-diagnostic.")
        return

    total_tonnes = st.session_state.last_total_t
    df = st.session_state.last_df
    maturity = st.session_state.last_maturity

    fit_score = st.session_state.fit_score
    fit_result = st.session_state.fit_result if st.session_state.fit_result else "Test rapide non réalisé"

    label, color = get_fit_result(fit_score)

    st.markdown(f"""
    <div class='card'>
        <div class='section-title'>Synthèse exportable</div>
        <div style='font-size:1.1rem; font-weight:700;'>
            Empreinte estimée : {total_tonnes:.2f} tCO₂e
        </div>
        <div style='font-size:1.1rem; font-weight:700;'>
            Maturité RSE numérique : {maturity:.0f}%
        </div>
        <div style='font-size:1.1rem; font-weight:700; color:{color};'>
            Adéquation AeroGreen : {fit_score:.0f}% — {label}
        </div>
        <p class='feature-text'>
            Ce rapport constitue une base de discussion. Il ne remplace pas un audit réglementaire complet,
            mais permet d’identifier rapidement les principaux leviers d’action.
        </p>
    </div>
    """, unsafe_allow_html=True)

    pdf_bytes = create_pdf_bytes(
        total_tonnes=total_tonnes,
        df_detail=df,
        maturity_score=maturity,
        fit_score=fit_score,
        fit_result=fit_result
    )

    st.download_button(
        label="Télécharger le rapport PDF",
        data=pdf_bytes,
        file_name=f"AeroGreen_PreAudit_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
