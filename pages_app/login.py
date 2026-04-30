import streamlit as st

from services.database import create_user, authenticate_user


def render_login():
    st.markdown("""
    <div class='hero'>
        <div class='hero-label'>Accès professionnel</div>
        <h1>Connectez-vous pour lancer le diagnostic avancé.</h1>
        <p>
            Le test rapide est accessible sans compte. L’espace professionnel permet d’enregistrer les audits,
            de générer des rapports premium et de suivre l’historique des entreprises analysées.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_register = st.tabs(["Connexion", "Créer un compte professionnel"])

    with tab_login:
        email = st.text_input("Email professionnel", key="login_email")
        password = st.text_input("Mot de passe", type="password", key="login_password")

        if st.button("Se connecter"):
            user = authenticate_user(email, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user_id = user["id"]
                st.session_state.user_email = user["email"]
                st.success("Connexion réussie.")
                st.session_state.page = "Diagnostic avancé" if st.session_state.fit_test_done else "Dashboard"
                st.rerun()
            else:
                st.error("Identifiants incorrects.")

    with tab_register:
        new_email = st.text_input("Email professionnel", key="register_email")
        new_password = st.text_input("Mot de passe", type="password", key="register_password")
        confirm_password = st.text_input("Confirmer le mot de passe", type="password", key="register_confirm")

        st.caption("Minimum recommandé : 10 caractères. Les mots de passe ne sont jamais stockés en clair.")

        if st.button("Créer le compte professionnel"):
            if not new_email.strip().lower().endswith((".fr", ".com", ".eu", ".org", ".net", ".aero")):
                st.warning("L’email semble inhabituel. Vous pouvez continuer, mais privilégiez un email professionnel.")
            if new_password != confirm_password:
                st.error("Les mots de passe ne correspondent pas.")
            else:
                ok, message = create_user(new_email, new_password)
                if ok:
                    st.success("Compte créé. Vous pouvez maintenant vous connecter.")
                else:
                    st.error(message)
