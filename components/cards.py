import streamlit as st


def render_page_header(title: str, subtitle: str, tag: str | None = None):
    tag_html = f"<div class='page-header-tag'>{tag}</div>" if tag else ""
    st.markdown(f"""
    <div class='page-header'>
        {tag_html}
        <h2>{title}</h2>
        <div class='page-header-sub'>{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def render_kpi_card(title: str, value: str, subtitle: str, color: str = "#111827"):
    st.markdown(f"""
    <div class='card uniform-card'>
        <div class='section-title'>{title}</div>
        <div class='kpi' style='color:{color};'>{value}</div>
        <div class='kpi-sub'>{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def render_feature_card(title: str, text: str):
    st.markdown(f"""
    <div class='card metric-card'>
        <div class='feature-title'>{title}</div>
        <div class='feature-text'>{text}</div>
    </div>
    """, unsafe_allow_html=True)


def render_soft_step_card(step: str, title: str, text: str):
    st.markdown(f"""
    <div class='card-soft uniform-soft-card'>
        <div class='section-title'>{step}</div>
        <strong>{title}</strong>
        <p class='feature-text'>{text}</p>
    </div>
    """, unsafe_allow_html=True)


def render_section_intro(label: str, title: str, text: str = ""):
    extra = f"<div class='feature-text'>{text}</div>" if text else ""
    st.markdown(f"""
    <div class='card-soft section-intro-card'>
        <div class='section-title'>{label}</div>
        <strong>{title}</strong>
        {extra}
    </div>
    """, unsafe_allow_html=True)


def render_progress(current_step: int, total_steps: int):
    percentage = int((current_step / total_steps) * 100)
    st.markdown(f"""
    <div class='card-soft progress-card'>
        <div class='section-title'>Progression diagnostic</div>
        <strong>Étape {current_step} / {total_steps}</strong>
        <div class='progress-track'>
            <div class='progress-fill' style='width:{percentage}%;'></div>
        </div>
        <div class='feature-text small'>{percentage}% complété</div>
    </div>
    """, unsafe_allow_html=True)


def render_recommendation_card(priority: str, title: str, text: str):
    color = "#ef4444" if priority == "Haute" else "#f59e0b" if priority == "Moyenne" else "#10b981"
    st.markdown(f"""
    <div class='card recommendation-card'>
        <span class='pill' style='background:{color}18; color:{color};'>{priority}</span>
        <div style='height:10px;'></div>
        <div class='feature-title'>{title}</div>
        <div class='feature-text'>{text}</div>
    </div>
    """, unsafe_allow_html=True)


def render_icon_card(icon: str, title: str, text: str, accent: str = "#6366f1"):
    st.markdown(f"""
    <div class='icon-card'>
        <div class='icon-bubble' style='background:{accent}18; color:{accent};'>{icon}</div>
        <div class='feature-title'>{title}</div>
        <div class='feature-text'>{text}</div>
    </div>
    """, unsafe_allow_html=True)


def render_process_timeline():
    st.markdown("""
    <div class='timeline'>
        <div class='timeline-step'>
            <div class='timeline-dot'>1</div>
            <div>
                <strong>Test rapide</strong>
                <p>Qualification immédiate sans compte.</p>
            </div>
        </div>
        <div class='timeline-line'></div>
        <div class='timeline-step'>
            <div class='timeline-dot'>2</div>
            <div>
                <strong>Espace professionnel</strong>
                <p>Connexion pour créer un dossier et enregistrer les audits.</p>
            </div>
        </div>
        <div class='timeline-line'></div>
        <div class='timeline-step'>
            <div class='timeline-dot'>3</div>
            <div>
                <strong>Diagnostic avancé</strong>
                <p>Collecte guidée : matériel, PLM, cloud, gouvernance et achats IT.</p>
            </div>
        </div>
        <div class='timeline-line'></div>
        <div class='timeline-step'>
            <div class='timeline-dot'>4</div>
            <div>
                <strong>Rapport</strong>
                <p>Score, recommandations et PDF premium.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_upgrade_panel():
    st.markdown("""
    <div class='upgrade-panel'>
        <div>
            <div class='section-title' style='color:#cbd5e1;'>Espace professionnel</div>
            <h3>Déverrouillez le diagnostic complet</h3>
            <p>
                Accédez au questionnaire avancé, à l’historique des audits, au dashboard exécutif
                et au rapport PDF premium.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
