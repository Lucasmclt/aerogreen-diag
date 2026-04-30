import streamlit as st

from components.cards import render_progress, render_section_intro, render_page_header
from services.calculations import compute_advanced_score


TOTAL_STEPS = 6


def save_inputs(**kwargs):
    st.session_state.diagnostic_inputs.update(kwargs)


def render_nav_buttons():
    c1, c2, c3 = st.columns([1, 1, 2])

    with c1:
        if st.session_state.wizard_step > 1:
            if st.button("← Retour"):
                st.session_state.wizard_step -= 1
                st.rerun()

    with c2:
        if st.session_state.wizard_step < TOTAL_STEPS:
            if st.button("Suivant →"):
                st.session_state.wizard_step += 1
                st.rerun()

    with c3:
        if st.session_state.wizard_step == TOTAL_STEPS:
            if st.button("Calculer le score AeroGreen"):
                result = compute_advanced_score(st.session_state.diagnostic_inputs)
                st.session_state.diagnostic_result = result
                st.session_state.diagnostic_done = True
                st.session_state.report_ready = True
                st.session_state.page = "Score"
                st.query_params["page"] = "Score"
                st.rerun()


def render_diagnostic_wizard():
    render_page_header(
        "Diagnostic avancé",
        "Questionnaire multi-étapes pour structurer la collecte de données avant scoring et génération du rapport premium.",
        "Collecte"
    )

    render_progress(st.session_state.wizard_step, TOTAL_STEPS)

    inputs = st.session_state.diagnostic_inputs
    step = st.session_state.wizard_step

    if step == 1:
        st.markdown("### 1. Profil entreprise")
        render_section_intro("Profil", "Informations de cadrage", "Ces données servent à pondérer le score et l’intensité carbone.")

        employees = st.number_input("Nombre de salariés", 1, 10000, int(inputs.get("employees", 50)))
        sites = st.number_input("Nombre de sites", 1, 100, int(inputs.get("sites", 1)))
        annual_revenue = st.number_input("Chiffre d’affaires annuel estimé (€)", 0, 500_000_000, int(inputs.get("annual_revenue", 5_000_000)), step=100000)
        critical_customer = st.checkbox("Client critique type Airbus / Safran / équipementier majeur", value=inputs.get("critical_customer", False))

        save_inputs(
            employees=employees,
            sites=sites,
            annual_revenue=annual_revenue,
            critical_customer=critical_customer,
        )

    elif step == 2:
        st.markdown("### 2. Parc matériel")
        render_section_intro("Infrastructure", "Équipements utilisateurs et IT internes")

        c1, c2, c3 = st.columns(3)
        with c1:
            nb_laptops = st.number_input("Ordinateurs portables", 0, 10000, int(inputs.get("nb_laptops", 0)))
            nb_workstations = st.number_input("Stations de travail fixes", 0, 10000, int(inputs.get("nb_workstations", 0)))
        with c2:
            nb_screens = st.number_input("Écrans externes", 0, 20000, int(inputs.get("nb_screens", 0)))
            nb_servers = st.number_input("Serveurs internes", 0, 1000, int(inputs.get("nb_servers", 0)))
        with c3:
            lifecycle_years = st.slider("Durée moyenne d’usage matériel", 2, 8, int(inputs.get("lifecycle_years", 4)))
            it_inventory = st.checkbox("Inventaire IT formalisé", value=inputs.get("it_inventory", False))

        save_inputs(
            nb_laptops=nb_laptops,
            nb_workstations=nb_workstations,
            nb_screens=nb_screens,
            nb_servers=nb_servers,
            lifecycle_years=lifecycle_years,
            it_inventory=it_inventory,
        )

    elif step == 3:
        st.markdown("### 3. Données PLM / CAO")
        render_section_intro("Données", "Stockage technique, archives et nettoyage")

        c1, c2 = st.columns(2)
        with c1:
            storage_active_tb = st.number_input("Stockage actif PLM / CAO (To)", 0.0, 100000.0, float(inputs.get("storage_active_tb", 0.0)))
            storage_cold_tb = st.number_input("Stockage froid / archives (To)", 0.0, 100000.0, float(inputs.get("storage_cold_tb", 0.0)))
        with c2:
            archive_policy = st.selectbox("Politique d’archivage", ["Aucune", "Informelle", "Formalisée"], index=["Aucune", "Informelle", "Formalisée"].index(inputs.get("archive_policy", "Aucune")))
            retention_policy = st.selectbox("Politique de rétention des données", ["Non", "Partielle", "Oui"], index=["Non", "Partielle", "Oui"].index(inputs.get("retention_policy", "Non")))
            plm_cleanup = st.selectbox("Nettoyage projets PLM / CAO", ["Jamais", "Rarement", "Annuellement", "Trimestriellement"], index=["Jamais", "Rarement", "Annuellement", "Trimestriellement"].index(inputs.get("plm_cleanup", "Jamais")))

        save_inputs(
            storage_active_tb=storage_active_tb,
            storage_cold_tb=storage_cold_tb,
            archive_policy=archive_policy,
            retention_policy=retention_policy,
            plm_cleanup=plm_cleanup,
        )

    elif step == 4:
        st.markdown("### 4. Cloud, serveurs et déplacements IT")
        render_section_intro("Opérations", "Infrastructure cloud et flux de travail")

        c1, c2 = st.columns(2)
        with c1:
            nb_cloud_vm = st.number_input("Instances cloud / VM moyennes", 0, 10000, int(inputs.get("nb_cloud_vm", 0)))
            cloud_provider_score = st.selectbox("Maturité environnementale du cloud/provider", ["Inconnue", "Basique", "Documentée"], index=["Inconnue", "Basique", "Documentée"].index(inputs.get("cloud_provider_score", "Inconnue")))
        with c2:
            short_trips = st.number_input("Déplacements courts IT / AMOA par an", 0, 10000, int(inputs.get("short_trips", 0)))
            long_trips = st.number_input("Déplacements longs IT / AMOA par an", 0, 10000, int(inputs.get("long_trips", 0)))

        save_inputs(
            nb_cloud_vm=nb_cloud_vm,
            cloud_provider_score=cloud_provider_score,
            short_trips=short_trips,
            long_trips=long_trips,
        )

    elif step == 5:
        st.markdown("### 5. Gouvernance RSE numérique")
        render_section_intro("Gouvernance", "Politiques, preuves et pilotage")

        c1, c2 = st.columns(2)
        with c1:
            iso_14001 = st.checkbox("Certification ISO 14001", value=inputs.get("iso_14001", False))
            deee_management = st.checkbox("Gestion DEEE formalisée", value=inputs.get("deee_management", False))
            rse_owner = st.checkbox("Référent RSE / IT clairement identifié", value=inputs.get("rse_owner", False))
        with c2:
            responsible_sourcing = st.checkbox("Charte achats responsables IT", value=inputs.get("responsible_sourcing", False))
            supplier_policy = st.checkbox("Critères RSE fournisseurs IT", value=inputs.get("supplier_policy", False))
            rse_frequency = st.selectbox("Fréquence de suivi RSE numérique", ["Aucun suivi", "Suivi annuel", "Suivi trimestriel", "Suivi mensuel"], index=["Aucun suivi", "Suivi annuel", "Suivi trimestriel", "Suivi mensuel"].index(inputs.get("rse_frequency", "Aucun suivi")))

        save_inputs(
            iso_14001=iso_14001,
            deee_management=deee_management,
            rse_owner=rse_owner,
            responsible_sourcing=responsible_sourcing,
            supplier_policy=supplier_policy,
            rse_frequency=rse_frequency,
        )

    elif step == 6:
        st.markdown("### 6. Achats IT et pratiques de réduction")
        render_section_intro("Achats IT", "Cycle de vie, réparation et décisions fournisseurs")

        c1, c2 = st.columns(2)
        with c1:
            refurbished_policy = st.checkbox("Politique reconditionné", value=inputs.get("refurbished_policy", False))
            repair_policy = st.checkbox("Réparation avant remplacement", value=inputs.get("repair_policy", False))
        with c2:
            purchase_centralized = st.checkbox("Achats IT centralisés", value=inputs.get("purchase_centralized", False))
            reduction_target = st.selectbox("Objectif de réduction numérique", ["Aucun", "Intention", "Objectif défini", "Objectif suivi"], index=["Aucun", "Intention", "Objectif défini", "Objectif suivi"].index(inputs.get("reduction_target", "Aucun")))

        save_inputs(
            refurbished_policy=refurbished_policy,
            repair_policy=repair_policy,
            purchase_centralized=purchase_centralized,
            reduction_target=reduction_target,
        )

        st.info("Dernière étape. Lance le calcul pour générer le score, les graphes et le rapport.")

    render_nav_buttons()
