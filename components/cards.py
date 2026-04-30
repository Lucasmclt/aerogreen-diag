import streamlit as st


def render_kpi_card(title: str, value: str, subtitle: str, color: str = "#111827"):
    st.markdown(f"""
    <div class='card'>
        <div class='section-title'>{title}</div>
        <div class='kpi' style='color:{color};'>{value}</div>
        <div class='kpi-sub'>{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def render_feature_card(title: str, text: str):
    st.markdown(f"""
    <div class='card'>
        <div class='feature-title'>{title}</div>
        <div class='feature-text'>{text}</div>
    </div>
    """, unsafe_allow_html=True)


def render_soft_step_card(step: str, title: str, text: str):
    st.markdown(f"""
    <div class='card-soft'>
        <div class='section-title'>{step}</div>
        <strong>{title}</strong>
        <p class='feature-text'>{text}</p>
    </div>
    """, unsafe_allow_html=True)


def render_section_intro(label: str, title: str):
    st.markdown(f"""
    <div class='card-soft'>
        <div class='section-title'>{label}</div>
        <strong>{title}</strong>
    </div>
    """, unsafe_allow_html=True)
