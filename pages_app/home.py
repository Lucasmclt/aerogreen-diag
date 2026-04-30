import streamlit as st

from components.cards import render_feature_card, render_soft_step_card


def render_home():
    st.markdown("""
    <div class='hero'>
        <div class='hero-label'>Aerospace ESG Intelligence</div>
        <h1>Le pré-audit carbone numérique qui rend la RSE exploitable pour les PME aéronautiques.</h1>
        <p>
            AeroGreen transforme un sujet perçu comme complexe, coûteux et flou en un parcours simple :
            qualification, collecte guidée, scoring structuré, rapport premium et lecture exécutive.
            Le tout avec un positionnement B2B crédible pour Toulouse et sa chaîne de sous-traitance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Pourquoi le projet est fort")
    c1, c2, c3 = st.columns(3)
    with c1:
        render_feature_card(
            "Pain point réel",
            "Les exigences RSE d’Airbus, Safran et des grands comptes descendent progressivement vers les rangs 2 et 3."
        )
    with c2:
        render_feature_card(
            "Offre crédible",
            "Vous proposez une première couche d’analyse moins coûteuse qu’un audit Big Four, mais plus structurée qu’un simple questionnaire brut."
        )
    with c3:
        render_feature_card(
            "Démonstration produit",
            "Le MVP montre votre capacité à traduire une norme complexe en expérience utilisateur claire et vendable."
        )

    st.markdown("## Ce que voit un jury ou un investisseur")
    j1, j2, j3 = st.columns(3)
    with j1:
        render_feature_card("Marché de niche défendable", "Ciblage local, vertical clair, besoin identifié, possibilité de conseil + produit.")
    with j2:
        render_feature_card("Monétisation plausible", "Pré-audit en entrée de mission, abonnement SaaS, rapport premium ou accompagnement AMOA complémentaire.")
    with j3:
        render_feature_card("Roadmap évidente", "Historique d’audits, benchmark sectoriel, moteur de preuves, workflows client, scoring enrichi.")

    st.markdown("## Créer un workspace client")
    left, right = st.columns([1.15, 1])

    with left:
        company_name = st.text_input("Nom de l’entreprise", value=st.session_state.company_name)
        contact_name = st.text_input("Référent / contact", value=st.session_state.contact_name)
        company_city = st.text_input("Ville", value=st.session_state.company_city)
        company_sector = st.selectbox(
            "Secteur",
            [
                "Sous-traitant aéronautique rang 2 ou 3",
                "Bureau d’études / ingénierie",
                "Fournisseur industriel hors aéronautique",
                "Autre"
            ],
            index=0
        )
        client_reference = st.text_input("Référence dossier", value=st.session_state.client_reference)

        if st.button("Créer le workspace"):
            st.session_state.company_name = company_name.strip()
            st.session_state.contact_name = contact_name.strip()
            st.session_state.company_city = company_city.strip()
            st.session_state.company_sector = company_sector
            st.session_state.client_reference = client_reference.strip()
            st.session_state.workspace_created = True
            st.success("Workspace client créé.")
            st.session_state.page = "Test rapide"
            st.rerun()

    with right:
        st.markdown("""
        <div class='card-dark'>
            <div class='section-title' style='color:#94a3b8;'>Narratif produit</div>
            <h3 style='margin-top:0;'>De la contrainte réglementaire à l’outil décisionnel</h3>
            <p style='color:#cbd5e1; line-height:1.65;'>
                AeroGreen ne se contente pas de calculer des chiffres : il donne une lecture, un ordre de priorité,
                et une base de discussion client. C’est ça qui rend le produit crédible.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## Parcours")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        render_soft_step_card("Étape 1", "Qualification", "Valider rapidement si le service est pertinent pour l’entreprise.")
    with p2:
        render_soft_step_card("Étape 2", "Collecte", "Renseigner les données par blocs métier avec un parcours guidé.")
    with p3:
        render_soft_step_card("Étape 3", "Scoring", "Obtenir un score global, des sous-scores et un niveau de risque.")
    with p4:
        render_soft_step_card("Étape 4", "Restitution", "Exporter un rapport premium ou afficher une vue exécutive.")

    if st.button("Voir le dashboard exécutif"):
        st.session_state.page = "Dashboard"
        st.rerun()
