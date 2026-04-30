import re
import streamlit as st

from services.database import create_user, authenticate_user


def password_strength(password: str):
    if not password:
        return 0, "Non défini", "#cbd5e1", "Utilisez au moins 10 caractères."

    score = 0
    checks = [
        len(password) >= 10,
        bool(re.search(r"[a-z]", password)) and bool(re.search(r"[A-Z]", password)),
        bool(re.search(r"\d", password)),
        bool(re.search(r"[^A-Za-z0-9]", password)),
        len(password) >= 14,
    ]
    score = sum(checks)

    if score <= 1:
        return 1, "Faible", "#ef4444", "Ajoutez de la longueur, des majuscules, des chiffres et un caractère spécial."
    if score == 2:
        return 2, "Correct", "#f59e0b", "Encore un peu juste. Renforcez-le avec un caractère spécial et plus de longueur."
    if score in (3, 4):
        return 3, "Solide", "#10b981", "Bon niveau de sécurité pour un compte professionnel."
    return 4, "Très solide", "#059669", "Excellent niveau de sécurité."

def render_strength_meter(password: str):
    level, label, color, tip = password_strength(password)
    pct = {0: 0, 1: 25, 2: 50, 3: 75, 4: 100}[level]

    st.markdown(
        f"""
        <div class="password-meter-card">
            <div class="password-meter-head">
                <span class="password-meter-label">Robustesse du mot de passe</span>
                <span class="password-meter-pill" style="color:{color}; border-color:{color}33; background:{color}12;">{label}</span>
            </div>
            <div class="password-meter-track">
                <div class="password-meter-fill" style="width:{pct}%; background:{color};"></div>
            </div>
            <div class="password-meter-tip">{tip}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return level

def render_login():
    st.markdown(
        """
        <div class="auth-page-shell">
            <div class="auth-page-intro">
                <div class="auth-kicker">Espace professionnel</div>
                <h1>Connectez-vous à votre espace AeroGreen.</h1>
                <p>
                    Gérez vos diagnostics, conservez vos dossiers et générez vos rapports dans
                    une interface plus complète, pensée pour un usage professionnel.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, right = st.columns([1.05, 1], gap="large")

    with left:
        st.markdown(
            """
            <div class="auth-side-panel">
                <div class="auth-panel-kicker">Pourquoi créer un compte</div>
                <h3>Déverrouillez l’ensemble du parcours avancé</h3>
                <div class="auth-benefit-grid">
                    <div class="auth-benefit-card">
                        <div class="auth-benefit-icon">📊</div>
                        <div>
                            <div class="auth-benefit-title">Diagnostic complet</div>
                            <div class="auth-benefit-text">Accédez au questionnaire multi-étapes et à une restitution plus détaillée.</div>
                        </div>
                    </div>
                    <div class="auth-benefit-card">
                        <div class="auth-benefit-icon">🗂️</div>
                        <div>
                            <div class="auth-benefit-title">Historique des dossiers</div>
                            <div class="auth-benefit-text">Conservez vos analyses et retrouvez facilement les audits enregistrés.</div>
                        </div>
                    </div>
                    <div class="auth-benefit-card">
                        <div class="auth-benefit-icon">📄</div>
                        <div>
                            <div class="auth-benefit-title">Rapport premium</div>
                            <div class="auth-benefit-text">Exportez une synthèse claire et professionnelle en PDF.</div>
                        </div>
                    </div>
                    <div class="auth-benefit-card">
                        <div class="auth-benefit-icon">🔒</div>
                        <div>
                            <div class="auth-benefit-title">Accès sécurisé</div>
                            <div class="auth-benefit-text">Votre espace est protégé et réservé à votre organisation.</div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        st.markdown(
            """
            <div class="auth-form-intro-card">
                <div class="auth-form-intro-title">Accès à votre espace</div>
                <div class="auth-form-intro-text">Connectez-vous ou créez votre compte professionnel pour poursuivre votre diagnostic.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        tab_login, tab_register = st.tabs(["Connexion", "Créer un compte"])

        with tab_login:
            st.markdown(
                """
                <div class="auth-tab-intro">
                    <div class="auth-tab-title">Connexion</div>
                    <div class="auth-tab-text">Accédez à vos diagnostics et poursuivez votre parcours.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            email = st.text_input("Email professionnel", key="login_email", placeholder="vous@entreprise.com")
            password = st.text_input("Mot de passe", type="password", key="login_password", placeholder="Votre mot de passe")

            if st.button("Se connecter", key="login_submit", use_container_width=True):
                user = authenticate_user(email, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user_id = user["id"]
                    st.session_state.user_email = user["email"]
                    st.success("Connexion réussie.")
                    st.session_state.page = "Diagnostic avancé" if st.session_state.fit_test_done else "Dashboard"
                    st.query_params["page"] = st.session_state.page
                    st.rerun()
                else:
                    st.error("Identifiants incorrects.")

        with tab_register:
            st.markdown(
                """
                <div class="auth-tab-intro">
                    <div class="auth-tab-title">Créer un compte</div>
                    <div class="auth-tab-text">Utilisez de préférence une adresse professionnelle.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            new_email = st.text_input("Email professionnel", key="register_email", placeholder="vous@entreprise.com")
            new_password = st.text_input("Mot de passe", type="password", key="register_password", placeholder="Choisissez un mot de passe robuste")
            strength_level = render_strength_meter(new_password)
            confirm_password = st.text_input("Confirmer le mot de passe", type="password", key="register_confirm", placeholder="Répétez votre mot de passe")

            if confirm_password:
                if confirm_password == new_password:
                    st.markdown(
                        """
                        <div class="password-match success">Les mots de passe correspondent.</div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        """
                        <div class="password-match error">Les mots de passe ne correspondent pas.</div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.caption("Minimum recommandé : 10 caractères, avec majuscules, chiffres et caractère spécial.")

            if st.button("Créer le compte professionnel", key="register_submit", use_container_width=True):
                if not new_email.strip():
                    st.error("Veuillez renseigner une adresse email.")
                elif not new_email.strip().lower().endswith((".fr", ".com", ".eu", ".org", ".net", ".aero")):
                    st.warning("Nous recommandons d’utiliser une adresse professionnelle.")
                elif new_password != confirm_password:
                    st.error("Les mots de passe ne correspondent pas.")
                elif strength_level < 2:
                    st.error("Le mot de passe est trop faible. Renforcez-le avant de continuer.")
                else:
                    ok, message = create_user(new_email, new_password)
                    if ok:
                        st.success("Compte créé. Vous pouvez maintenant vous connecter.")
                    else:
                        st.error(message)

