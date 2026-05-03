import streamlit as st
from datetime import datetime
from fpdf import FPDF
from services.database import save_deep_audit, audit_public_code_exists


def _missing_required_company_fields() -> list[str]:
    required = {
        "company_name": "Nom de l’entreprise",
        "contact_name": "Référent / contact",
        "company_city": "Ville",
        "client_reference": "Référence dossier",
    }
    return [label for key, label in required.items() if not str(st.session_state.get(key, "")).strip()]


def _safe_text(value) -> str:
    return str(value).encode("latin-1", "replace").decode("latin-1")


def _yes_no(value: bool) -> str:
    return "Oui" if value else "Non"


def _score_ratio(values):
    if not values:
        return 0
    return round((sum(1 for value in values if value) / len(values)) * 100, 1)


class DeepAuditPDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 28, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "B", 15)
        self.cell(0, 12, "AeroGreen - Rapport RSE numerique approfondi", 0, 1, "C")
        self.set_font("Arial", "", 9)
        self.cell(0, 5, "Preparation EcoVadis, REEN, CAO/PLM et carbone numerique", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_text_color(120, 120, 120)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, "Document de travail - A consolider avec preuves et referentiels officiels", 0, 0, "C")

    def section(self, title):
        self.set_font("Arial", "B", 12)
        self.set_text_color(15, 23, 42)
        self.set_fill_color(241, 245, 249)
        self.cell(0, 9, _safe_text(title), 0, 1, "L", True)
        self.ln(2)

    def paragraph(self, text, size=9.2):
        self.set_font("Arial", "", size)
        self.set_text_color(55, 65, 81)
        self.multi_cell(0, 5.1, _safe_text(text))
        self.ln(1.5)

    def bullet(self, label, value=None):
        text = f"- {label}" if value is None else f"- {label} : {value}"
        self.paragraph(text, 9)


def build_deep_scores(data):
    doc_score = _score_ratio(data["docs"].values())
    eco_env = _score_ratio(data["environment"].values())
    eco_social = _score_ratio(data["social"].values())
    eco_ethics = _score_ratio(data["ethics"].values())
    eco_proc = _score_ratio(data["procurement"].values())
    reen_score = _score_ratio(data["reen"].values())
    plm_score = _score_ratio(data["plm"].values())

    overall = round(
        doc_score * 0.18
        + eco_env * 0.18
        + eco_social * 0.12
        + eco_ethics * 0.12
        + eco_proc * 0.15
        + reen_score * 0.15
        + plm_score * 0.10,
        1,
    )

    return {
        "Documents": doc_score,
        "Environnement": eco_env,
        "Social": eco_social,
        "Éthique": eco_ethics,
        "Achats responsables": eco_proc,
        "REEN": reen_score,
        "CAO/PLM": plm_score,
        "Global": overall,
    }



def build_recommended_actions(scores, data):
    actions = []

    if scores["Documents"] < 70:
        actions.append("Consolider les preuves documentaires : politique RSE, certificats, rapports environnementaux, charte achats et preuves datées.")
    if scores["Environnement"] < 70:
        actions.append("Structurer la partie environnement : données CO2, énergie, eau, déchets, objectifs de réduction et justificatifs associés.")
    if scores["Éthique"] < 70:
        actions.append("Formaliser les dispositifs éthiques : code de conduite, anti-corruption, formation et canal de signalement.")
    if scores["Achats responsables"] < 70:
        actions.append("Renforcer les achats responsables : critères RSE fournisseurs, cartographie des risques, preuves documentaires et suivi fournisseur.")
    if scores["REEN"] < 70:
        actions.append("Mettre sous contrôle le numérique responsable : durée de vie du parc IT, reconditionné, DEEE, effacement sécurisé et sobriété numérique.")
    if scores["CAO/PLM"] < 70:
        actions.append("Fiabiliser la gestion CAO/PLM : volumes, workflows, révisions, traçabilité, archivage et nettoyage des données techniques.")
    if not data.get("free_context"):
        actions.append("Ajouter un contexte libre : organisation, contraintes client, preuves disponibles, points bloquants et objectifs de préparation.")

    if not actions:
        actions.append("Le dossier est bien structuré. L’étape suivante consiste à vérifier la qualité des preuves, les dates, et l’alignement avec les référentiels officiels.")

    return actions

def render_checkbox_group(items, prefix):
    values = {}
    for item in items:
        values[item] = st.checkbox(item, key=f"{prefix}_{item}")
    return values


def pdf_key_values(pdf, title, values):
    pdf.section(title)
    for key, value in values.items():
        if isinstance(value, dict):
            pdf.paragraph(key)
            for sub_key, sub_val in value.items():
                pdf.bullet(sub_key, _yes_no(sub_val) if isinstance(sub_val, bool) else sub_val)
        else:
            pdf.bullet(key, _yes_no(value) if isinstance(value, bool) else value)


def create_deep_audit_pdf(company, diagnostic_result, data, scores):
    pdf = DeepAuditPDF()
    pdf.add_page()

    pdf_key_values(pdf, "1. Informations entreprise", {
        "Entreprise": company.get("company_name", "Non renseignee"),
        "Ville": company.get("company_city", "Non renseignee"),
        "Secteur": company.get("company_sector", "Non renseigne"),
        "Reference dossier": company.get("client_reference", "N/A"),
        "Repère de préparation visé": data["meta"]["target_level"],
        "Delai souhaite": data["meta"]["timeline"],
        "Taille entreprise": data["meta"]["company_size"],
    })

    if diagnostic_result:
        pdf_key_values(pdf, "2. Synthese du diagnostic avance", {
            "Score global initial": f"{diagnostic_result.get('global_score', 0):.0f}/100",
            "Grade initial": diagnostic_result.get("grade", "N/A"),
            "Niveau de risque initial": diagnostic_result.get("risk_label", "N/A"),
            "Empreinte estimee": f"{diagnostic_result.get('total_tonnes', 0):.2f} tCO2e",
        })

    pdf_key_values(pdf, "3. Score indicatif approfondi", {k: f"{v}/100" for k, v in scores.items()})

    pdf_key_values(pdf, "4. Documents de preuve", data["docs"])
    pdf.paragraph(data.get("docs_notes", ""))

    pdf_key_values(pdf, "5. Préparation environnement", data["environment"])
    pdf_key_values(pdf, "Indicateurs environnementaux", data["environment_metrics"])
    pdf.paragraph(data.get("environment_notes", ""))

    pdf_key_values(pdf, "6. Préparation social / RH", data["social"])
    pdf_key_values(pdf, "Indicateurs sociaux", data["social_metrics"])
    pdf.paragraph(data.get("social_notes", ""))

    pdf_key_values(pdf, "7. Préparation éthique", data["ethics"])
    pdf_key_values(pdf, "8. Préparation achats responsables", data["procurement"])
    pdf_key_values(pdf, "Indicateurs achats", data["procurement_metrics"])

    pdf_key_values(pdf, "9. Loi REEN / Numerique responsable", data["reen"])
    pdf_key_values(pdf, "Indicateurs REEN", data["reen_metrics"])
    pdf.paragraph(data.get("reen_notes", ""))

    pdf_key_values(pdf, "10. CAO / PLM / Donnees techniques", data["plm"])
    pdf_key_values(pdf, "Indicateurs PLM", data["plm_metrics"])
    pdf.paragraph(data.get("plm_notes", ""))

    pdf_key_values(pdf, "11. Facteurs d'emission et hypotheses", data["carbon_metrics"])
    pdf.paragraph(data.get("carbon_notes", ""))

    pdf.section("12. Contexte libre fourni")
    pdf.paragraph(data.get("free_context", "Aucun contexte libre fourni."))

    pdf.section("13. Actions recommandees")
    for action in data.get("recommended_actions", []):
        pdf.bullet(action)

    pdf.section("14. Usage recommande")
    pdf.paragraph(
        "Ce document peut servir de base de discussion, de support de preparation ou de demonstrateur de structuration des preuves RSE. "
        "Il doit etre relu et consolide avant tout usage externe."
    )

    pdf.section("15. Reserve methodologique")
    pdf.paragraph(
        "Document de travail - A consolider avec preuves et referentiels officiels. "
        "Ce rapport est issu d'un prototype exploratoire. Il ne constitue ni un audit officiel, ni une certification, ni une notation EcoVadis. "
        "Les resultats sont indicatifs et reposent sur les donnees declarees dans l'outil. Les preuves doivent etre verifiees, datees, "
        "documentees et alignees avec les referentiels officiels applicables."
    )

    return pdf.output(dest="S").encode("latin-1", errors="replace")


def render_deep_audit():
    st.markdown("""
    <div class="page-header">
        <div class="page-header-tag">Dossier RSE de travail</div>
        <h2>Structurer un dossier RSE numérique de travail.</h2>
        <div class="page-header-sub">
            Cette section aide à organiser des preuves déclaratives et des pistes de préparation : REEN, CAO/PLM, achats responsables et données carbone indicatives.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("diagnostic_done") or not st.session_state.get("diagnostic_result"):
        st.warning("Lancez d’abord le pré-diagnostic guidé afin d’avoir une base indicative de score et de synthèse.")
        if st.button("Aller au pré-diagnostic guidé", use_container_width=True):
            st.session_state.page = "Diagnostic avancé"
            st.query_params["page"] = "Diagnostic avancé"
            st.rerun()
        return

    current_code = st.session_state.get("current_audit_public_code") or st.session_state.get("last_saved_diagnostic_id")
    if not current_code or not audit_public_code_exists(st.session_state.user_id, current_code):
        st.warning("Aucun pré-diagnostic enregistré n’est rattaché à ce dossier. Enregistrez d’abord le pré-diagnostic depuis la page Score.")
        if st.button("Retourner au Score", use_container_width=True):
            st.session_state.page = "Score"
            st.query_params["page"] = "Score"
            st.rerun()
        return

    st.info("Cette section structure un dossier de travail. Elle ne produit pas d’évaluation officielle.")

    with st.expander("0. Cadrage de la pré-analyse", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            target_level = st.selectbox("Repère de préparation visé", ["Bronze", "Argent", "Or", "Platine", "Non défini"], key="deep_target_level")
        with c2:
            timeline = st.selectbox("Échéance souhaitée", ["< 1 mois", "1 à 3 mois", "3 à 6 mois", "> 6 mois", "Non défini"], key="deep_timeline")
        with c3:
            company_size = st.selectbox("Taille déclarée", ["Micro", "PME", "ETI", "Grand groupe", "Non défini"], key="deep_company_size")
        assessment_scope = st.multiselect(
            "Périmètre couvert",
            ["Siège", "Sites de production", "Bureau d’études", "IT interne", "Cloud / hébergement", "Achats fournisseurs", "Données PLM / CAO"],
            key="deep_scope"
        )

    with st.expander("1. Documents à rassembler", expanded=True):
        docs = render_checkbox_group([
            "Politique RSE formalisée",
            "Revues internes ou externes disponibles",
            "Certificats ISO ou équivalents disponibles",
            "Rapports environnementaux avec données chiffrées",
            "Programmes sociaux / RH documentés",
            "Code de conduite ou charte éthique",
            "Charte achats responsables",
            "Liste fournisseurs et certificats associés",
            "Preuves datées d’au moins un trimestre",
        ], "docs")
        c1, c2, c3 = st.columns(3)
        with c1:
            doc_owner = st.text_input("Responsable du dossier", key="doc_owner")
        with c2:
            doc_status = st.selectbox("État global des preuves", ["Non collectées", "Partiellement collectées", "Majoritairement prêtes", "Prêtes"], key="doc_status")
        with c3:
            evidence_age = st.selectbox("Ancienneté dominante des preuves", ["< 1 trimestre", "1 à 4 trimestres", "> 1 an", "Mixte"], key="evidence_age")
        docs_notes = st.text_area("Notes documents / preuves manquantes", height=110, key="docs_notes")

    with st.expander("2. Préparation environnement", expanded=False):
        environment = render_checkbox_group([
            "Mesure des émissions de GES / CO2",
            "Sources d’émissions identifiées",
            "Objectif ou trajectoire de réduction",
            "Actions d’efficacité énergétique",
            "Utilisation ou achat d’énergie renouvelable",
            "Suivi de la consommation d’eau",
            "Actions de réduction de consommation d’eau",
            "Typologie des déchets documentée",
            "Programme de réduction / réemploi / recyclage des déchets",
            "Gestion des déchets dangereux documentée",
        ], "env")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            co2_reduction = st.number_input("% réduction CO2 observée", 0.0, 100.0, 0.0, key="co2_reduction")
        with c2:
            energy_reduction = st.number_input("% réduction énergie", 0.0, 100.0, 0.0, key="energy_reduction")
        with c3:
            renewable_share = st.number_input("% énergie renouvelable", 0.0, 100.0, 0.0, key="renewable_share")
        with c4:
            waste_recycling = st.number_input("% déchets recyclés", 0.0, 100.0, 0.0, key="waste_recycling")
        environment_notes = st.text_area("Données chiffrées environnementales", height=130, key="environment_notes")

    with st.expander("3. Préparation social / RH", expanded=False):
        social = render_checkbox_group([
            "Mesures de santé et sécurité au travail",
            "Formations sécurité ou bien-être",
            "Politique anti-discrimination",
            "Dispositif de prévention du harcèlement",
            "Actions d’égalité des chances",
            "Formation ou sensibilisation aux droits sociaux",
            "Initiatives sociales ou communautaires",
            "Partenariats ONG / associations / actions locales",
        ], "social")
        c1, c2, c3 = st.columns(3)
        with c1:
            training_hours = st.number_input("Heures de formation / salarié / an", 0.0, 200.0, 0.0, key="training_hours")
        with c2:
            accident_rate = st.number_input("Taux ou nombre d’accidents déclaré", 0.0, 1000.0, 0.0, key="accident_rate")
        with c3:
            social_program_level = st.selectbox("Niveau des initiatives sociales", ["Aucun", "Ponctuel", "Structuré", "Piloté avec indicateurs"], key="social_program_level")
        social_notes = st.text_area("Notes sociales / RH", height=130, key="social_notes")

    with st.expander("4. Préparation éthique", expanded=False):
        ethics = render_checkbox_group([
            "Code de conduite formalisé",
            "Politique anti-corruption",
            "Formation annuelle à l’éthique",
            "Mécanisme de signalement",
            "Politique de pratiques commerciales équitables",
            "Contrôles internes ou revues documentaires",
            "Transparence des pratiques commerciales",
        ], "ethics")
        c1, c2 = st.columns(2)
        with c1:
            ethics_training = st.selectbox("Fréquence formation éthique", ["Aucune", "Ponctuelle", "Annuelle", "À l’arrivée + annuel"], key="ethics_training")
        with c2:
            whistleblowing = st.selectbox("Canal d’alerte", ["Aucun", "Email interne", "Outil dédié", "Tiers indépendant"], key="whistleblowing")
        ethics_notes = st.text_area("Notes éthique / préparation", height=130, key="ethics_notes")

    with st.expander("5. Préparation achats responsables", expanded=False):
        procurement = render_checkbox_group([
            "Critères RSE dans la sélection fournisseurs",
            "Collecte de preuves fournisseurs",
            "Revues fournisseurs régulières",
            "Engagement formel fournisseurs / charte",
            "Évaluation des risques de la chaîne d’approvisionnement",
            "Programme de sensibilisation fournisseurs",
            "Suivi de performance RSE fournisseurs",
            "Part de fournisseurs certifiés connue",
        ], "procurement")
        c1, c2, c3 = st.columns(3)
        with c1:
            certified_suppliers = st.number_input("% fournisseurs certifiés RSE/ISO", 0.0, 100.0, 0.0, key="certified_suppliers")
        with c2:
            audited_suppliers = st.number_input("% fournisseurs revus", 0.0, 100.0, 0.0, key="audited_suppliers")
        with c3:
            risk_mapping = st.selectbox("Cartographie risques fournisseurs", ["Aucune", "Partielle", "Complète", "Mise à jour annuelle"], key="risk_mapping")
        procurement_notes = st.text_area("Notes achats responsables / fournisseurs", height=130, key="procurement_notes")

    with st.expander("6. Loi REEN - Numérique responsable", expanded=False):
        reen = render_checkbox_group([
            "Nombre de postes informatiques connu",
            "Durée moyenne de conservation des équipements connue",
            "Part de matériel reconditionné mesurée",
            "Volume de DEEE produit ou collecté connu",
            "Prestataire de collecte / recyclage identifié",
            "Politique d’achats IT responsables",
            "Sensibilisation des utilisateurs au numérique responsable",
            "Procédure d’effacement sécurisé des données",
            "Politique de réduction des consommations numériques",
        ], "reen")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            avg_lifetime = st.number_input("Durée moyenne du parc IT (années)", 0.0, 10.0, 0.0, key="avg_lifetime")
        with c2:
            refurbished_share = st.number_input("% matériel reconditionné", 0.0, 100.0, 0.0, key="refurbished_share")
        with c3:
            deee_kg = st.number_input("DEEE tracés (kg/an)", 0.0, 100000.0, 0.0, key="deee_kg")
        with c4:
            secure_wipe = st.selectbox("Effacement sécurisé", ["Aucun", "Ponctuel", "Procédure formalisée", "Avec preuve"], key="secure_wipe")
        reen_notes = st.text_area("Notes REEN / sobriété numérique", height=130, key="reen_notes")

    with st.expander("7. CAO / PLM / Données techniques", expanded=False):
        plm = render_checkbox_group([
            "Outils CAO utilisés identifiés",
            "Outils PLM/PDM identifiés",
            "Volumes de données PLM / CAO mesurés",
            "Règles de version / révision documentées",
            "Workflow de validation documenté",
            "Gestion des nomenclatures / BOM maîtrisée",
            "Traçabilité des modifications disponible",
            "Politique d’archivage des projets terminés",
            "Nettoyage ou bascule en stockage froid planifiée",
            "Gestion des impacts de modification documentée",
        ], "plm")
        c1, c2, c3 = st.columns(3)
        with c1:
            plm_tool = st.selectbox("Outil PLM principal", ["Non défini", "ENOVIA", "Windchill", "Teamcenter", "Autre"], key="plm_tool")
        with c2:
            cad_tool = st.selectbox("Outil CAO principal", ["Non défini", "CATIA", "SolidWorks", "NX", "Creo", "Autre"], key="cad_tool")
        with c3:
            plm_storage = st.number_input("Volume données techniques (To)", 0.0, 100000.0, 0.0, key="plm_storage")
        c4, c5 = st.columns(2)
        with c4:
            change_process = st.selectbox("Gestion des changements", ["Informelle", "Change Request", "Change Order", "Workflow complet"], key="change_process")
        with c5:
            archive_policy = st.selectbox("Archivage PLM", ["Aucun", "Manuel", "Formalisé", "Automatisé / stockage froid"], key="archive_policy_deep")
        plm_notes = st.text_area("Notes CAO / PLM / données techniques", height=130, key="plm_notes")

    with st.expander("8. Facteurs d’émission et contexte libre", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            laptop_factor = st.number_input("Facteur laptop kgCO2e/unité", 0.0, 1000.0, 193.0, key="laptop_factor")
        with c2:
            storage_factor = st.number_input("Facteur cloud kgCO2e/To/an", 0.0, 100.0, 0.24, key="storage_factor")
        with c3:
            server_factor = st.number_input("Facteur serveur rack kgCO2e", 0.0, 5000.0, 850.0, key="server_factor")
        with c4:
            workstation_factor = st.number_input("Facteur station fixe proxy kgCO2e", 0.0, 2000.0, 350.0, key="workstation_factor")
        carbon_notes = st.text_area("Hypothèses carbone à préciser", height=130, key="carbon_notes")
        free_context = st.text_area("Contexte libre complet", height=220, key="free_context")

    data = {
        "meta": {
            "target_level": target_level,
            "timeline": timeline,
            "company_size": company_size,
            "assessment_scope": ", ".join(assessment_scope) if assessment_scope else "Non renseigné",
        },
        "docs": docs,
        "docs_notes": docs_notes,
        "environment": environment,
        "environment_metrics": {
            "% réduction CO2 observée": co2_reduction,
            "% réduction énergie": energy_reduction,
            "% énergie renouvelable": renewable_share,
            "% déchets recyclés": waste_recycling,
        },
        "environment_notes": environment_notes,
        "social": social,
        "social_metrics": {
            "Heures formation/salarié/an": training_hours,
            "Taux ou nombre accidents": accident_rate,
            "Niveau initiatives sociales": social_program_level,
        },
        "social_notes": social_notes,
        "ethics": ethics,
        "ethics_notes": ethics_notes,
        "procurement": procurement,
        "procurement_metrics": {
            "% fournisseurs certifiés": certified_suppliers,
            "% fournisseurs revus": audited_suppliers,
            "Cartographie risques": risk_mapping,
        },
        "procurement_notes": procurement_notes,
        "reen": reen,
        "reen_metrics": {
            "Durée moyenne parc IT": avg_lifetime,
            "% matériel reconditionné": refurbished_share,
            "DEEE tracés kg/an": deee_kg,
            "Effacement sécurisé": secure_wipe,
        },
        "reen_notes": reen_notes,
        "plm": plm,
        "plm_metrics": {
            "Outil PLM": plm_tool,
            "Outil CAO": cad_tool,
            "Volume données techniques To": plm_storage,
            "Gestion changements": change_process,
            "Archivage PLM": archive_policy,
        },
        "plm_notes": plm_notes,
        "carbon_metrics": {
            "Facteur laptop": laptop_factor,
            "Facteur cloud": storage_factor,
            "Facteur serveur rack": server_factor,
            "Facteur station fixe": workstation_factor,
        },
        "carbon_notes": carbon_notes,
        "free_context": free_context,
    }

    scores = build_deep_scores(data)
    recommended_actions = build_recommended_actions(scores, data)
    data["recommended_actions"] = recommended_actions

    st.markdown("## Analyse indicative approfondie")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Score indicatif approfondi", f"{scores['Global']:.0f}/100")
    c2.metric("Documents", f"{scores['Documents']:.0f}/100")
    c3.metric("Env. préparation", f"{scores['Environnement']:.0f}/100")
    c4.metric("REEN", f"{scores['REEN']:.0f}/100")

    st.markdown("## Actions recommandées automatiquement")
    actions_html = "".join([f"<li>{action}</li>" for action in recommended_actions])
    st.markdown(
        f"""
        <div class='recommendation-box'>
            <ul>{actions_html}</ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    result = st.session_state.get("diagnostic_result")
    missing_company_fields = _missing_required_company_fields()
    company = {
        "company_name": st.session_state.get("company_name", "").strip(),
        "company_city": st.session_state.get("company_city", "").strip(),
        "company_sector": st.session_state.get("company_sector") or "Non renseigné",
        "client_reference": st.session_state.get("client_reference", "").strip(),
        "contact_name": st.session_state.get("contact_name", "").strip(),
    }

    pdf_bytes = create_deep_audit_pdf(company, result, data, scores)

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("""
        <div class='ag-bottom-card-marker ag-bottom-card-finalize'></div>
        <div class='ag-bottom-card-header'>
            <div class='section-title'>Finalisation</div>
            <strong>Finaliser le dossier de travail RSE numérique</strong>
            <div class='feature-text small'>Sauvegardez le dossier dans le démonstrateur de suivi ou exportez un rapport de travail approfondi, réutilisable pour préparer les preuves à consolider.</div>
        </div>
        """, unsafe_allow_html=True)
        c_save, c_pdf = st.columns(2)
        with c_save:
            if st.button("Enregistrer le dossier RSE complet", key="deep_save_btn", use_container_width=True):
                if missing_company_fields:
                    st.error("Impossible d’enregistrer : informations du dossier obligatoires manquantes — " + ", ".join(missing_company_fields) + ".")
                    if st.button("Compléter les informations du dossier", key="deep_complete_company_info", use_container_width=True):
                        st.session_state.wizard_step = 1
                        st.session_state.page = "Diagnostic avancé"
                        st.query_params["page"] = "Diagnostic avancé"
                        st.rerun()
                else:
                    deep_code = save_deep_audit(
                        user_id=st.session_state.user_id,
                        company=company,
                        data=data,
                        scores=scores,
                    )
                    st.session_state.current_deep_public_code = deep_code
                    st.success(f"Dossier de travail RSE enregistré. Code dossier : {deep_code}.")
        with c_pdf:
            st.download_button(
                "Télécharger le rapport exploratoire PDF",
                data=pdf_bytes,
                file_name=f"AeroGreen_Rapport_Exploratoire_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
