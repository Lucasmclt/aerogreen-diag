import streamlit as st

from services.database import create_user, authenticate_user, get_or_create_passwordless_user
from config.auth_config import PASSWORDLESS_EMAILS
import os


def _allowed_passwordless_emails():
    env_emails = os.getenv("AEROGREEN_PASSWORDLESS_EMAILS", "")
    from_env = {email.strip().lower() for email in env_emails.split(",") if email.strip()}
    from_config = {email.strip().lower() for email in PASSWORDLESS_EMAILS if email.strip()}
    return from_env | from_config


def _reset_workflow_after_login():
    """Avoid carrying a stale guest/previous-session wizard state into a fresh login."""
    st.session_state.wizard_step = 1
    st.session_state.diagnostic_done = False
    st.session_state.diagnostic_inputs = {}
    st.session_state.diagnostic_result = None
    st.session_state.report_ready = False
    st.session_state.last_saved_diagnostic_key = ""
    st.session_state.last_saved_diagnostic_id = None


def render_login():
    st.markdown("""
    <div class='hero'>
        <div class='hero-label'>Accès au démonstrateur</div>
        <h1>Connectez-vous pour explorer le diagnostic avancé.</h1>
        <p>
            Le test rapide est accessible sans compte. L’espace connecté permet d’enregistrer des cas d’étude,
            de suivre des diagnostics indicatifs et de générer des rapports de travail.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_register, tab_quick = st.tabs(["Connexion", "Créer un compte", "Accès rapide"])

    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Mot de passe", type="password", key="login_password")

        if st.button("Se connecter"):
            user = authenticate_user(email, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user_id = user["id"]
                st.session_state.user_email = user["email"]
                _reset_workflow_after_login()
                st.success("Connexion réussie.")
                st.session_state.page = "Diagnostic avancé" if st.session_state.fit_test_done else "Dashboard"
                st.query_params["page"] = st.session_state.page
                st.rerun()
            else:
                st.error("Identifiants incorrects.")

    with tab_register:
        new_email = st.text_input("Email", key="register_email")
        new_password = st.text_input("Mot de passe", type="password", key="register_password")
        confirm_password = st.text_input("Confirmer le mot de passe", type="password", key="register_confirm")

        st.caption("Minimum recommandé : 10 caractères. Votre accès est protégé.")

        if st.button("Créer le compte"):
            if not new_email.strip().lower().endswith((".fr", ".com", ".eu", ".org", ".net", ".aero")):
                st.warning("Une adresse liée au contexte du projet est recommandée pour la démonstration.")
            if new_password != confirm_password:
                st.error("Les mots de passe ne correspondent pas.")
            else:
                ok, message = create_user(new_email, new_password)
                if ok:
                    user = authenticate_user(new_email, new_password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user["id"]
                        st.session_state.user_email = user["email"]
                        _reset_workflow_after_login()
                        st.success("Compte créé. Vous êtes connecté.")
                        st.session_state.page = "Diagnostic avancé" if st.session_state.fit_test_done else "Dashboard"
                        st.query_params["page"] = st.session_state.page
                        st.rerun()
                    else:
                        st.success("Compte créé. Vous pouvez maintenant vous connecter.")
                else:
                    st.error(message)


    with tab_quick:
        st.markdown(
            """
            <div class="auth-tab-intro">
                <div class="auth-tab-title">Accès rapide local</div>
                <div class="auth-tab-text">Réservé aux emails autorisés dans la configuration locale.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        quick_email = st.text_input("Email autorisé", key="quick_login_email", placeholder="vous@entreprise.com")
        st.caption("Pour autoriser votre email : modifiez config/auth_config.py ou définissez AEROGREEN_PASSWORDLESS_EMAILS.")

        if st.button("Se connecter sans mot de passe", key="quick_login_submit", use_container_width=True):
            allowed = _allowed_passwordless_emails()
            if quick_email.strip().lower() in allowed:
                user = get_or_create_passwordless_user(quick_email)
                st.session_state.authenticated = True
                st.session_state.user_id = user["id"]
                st.session_state.user_email = user["email"]
                _reset_workflow_after_login()
                st.session_state.page = "Dashboard"
                st.query_params["page"] = "Dashboard"
                st.success("Connexion rapide réussie.")
                st.rerun()
            else:
                st.error("Cet email n’est pas autorisé pour la connexion rapide.")
