import pandas as pd


EMISSION_FACTORS = {
    # Facteurs simplifiés utilisés comme proxys pédagogiques, pas comme base réglementaire.
    "laptop": 193,
    "workstation": 350,
    "screen": 200,
    "storage_tb_active": 0.24,
    "storage_tb_cold": 0.06,
    "server": 850,
    "cloud_vm": 90,
    "business_trip_short": 250,
    "business_trip_long": 1200,
}

WEIGHTS = {
    "carbon": 35,
    "governance": 25,
    "data": 20,
    "procurement": 20,
}

PILLAR_EXPLANATIONS = {
    "Carbone numérique": "Ordre de grandeur simplifié lié au parc matériel, aux serveurs, au cloud, au stockage et aux déplacements IT/AMOA.",
    "Gouvernance": "Capacité à nommer un responsable, suivre le parc, documenter les règles et préparer des preuves exploitables.",
    "Données PLM / CAO": "Maîtrise des données techniques : stockage actif, archives, rétention, nettoyage et règles de conservation.",
    "Achats IT responsables": "Cycle de vie du matériel, réparation, reconditionné, centralisation des achats et critères fournisseurs.",
}

EVIDENCE_MATRIX = [
    {
        "criterion": "Inventaire du parc numérique",
        "expected": "Liste datée des postes, écrans, serveurs, VM/cloud et responsables internes.",
        "example": "Export GLPI, Excel de parc IT, inventaire DSI, bon de renouvellement matériel.",
        "limit": "Ne prouve pas l’empreinte carbone réelle ; sert à cadrer le périmètre.",
    },
    {
        "criterion": "Gestion DEEE / fin de vie",
        "expected": "Procédure ou preuve de collecte, recyclage, effacement ou reprise des équipements.",
        "example": "Contrat prestataire DEEE, bordereau de collecte, certificat d’effacement.",
        "limit": "La preuve doit être datée et rattachée au parc concerné.",
    },
    {
        "criterion": "Achats IT responsables",
        "expected": "Critère d’achat formalisé : durée de vie, réparation, reconditionné, fournisseur, énergie.",
        "example": "Politique achats IT, grille de sélection fournisseur, facture de matériel reconditionné.",
        "limit": "Une intention ne suffit pas ; il faut une trace utilisable dans un dossier fournisseur.",
    },
    {
        "criterion": "Données CAO / PLM",
        "expected": "Cartographie des outils, volumes, règles d’archivage et séparation actif/archive.",
        "example": "Liste CATIA/PLM/PDM, volume de stockage par projet, règle de conservation.",
        "limit": "Le volume seul ne dit rien sur la criticité ni sur l’obligation de conservation.",
    },
    {
        "criterion": "Règle de conservation des données techniques",
        "expected": "Règle claire sur les projets actifs, projets terminés, archives et données dormantes.",
        "example": "Procédure qualité, règle PLM, note DSI, convention projet.",
        "limit": "Doit être compatible avec les contraintes qualité, client et propriété intellectuelle.",
    },
    {
        "criterion": "Gouvernance numérique responsable",
        "expected": "Référent identifié, fréquence de suivi, responsabilités et preuves centralisées.",
        "example": "Fiche mission, compte-rendu trimestriel, tableau de suivi des actions.",
        "limit": "Nommer un référent ne prouve pas la maturité ; il faut des actions suivies.",
    },
    {
        "criterion": "Sensibilisation interne",
        "expected": "Trace de sensibilisation ou de consignes sur sobriété numérique et usage des données.",
        "example": "Support de formation, feuille d’émargement, note interne, guide utilisateur.",
        "limit": "La sensibilisation doit être contextualisée aux usages industriels réels.",
    },
    {
        "criterion": "Preuves fournisseurs numériques",
        "expected": "Contrats, engagements, critères ou attestations liés aux fournisseurs IT/cloud/prestataires.",
        "example": "Questionnaire fournisseur, clause achat, attestation hébergeur, contrat de maintenance.",
        "limit": "Ne remplace pas une vérification documentaire ou contractuelle complète.",
    },
]


def clamp(value, min_value=0, max_value=100):
    return max(min_value, min(max_value, value))


def get_score_color(score: float) -> str:
    if score < 33:
        return "#ef4444"
    if score < 66:
        return "#f59e0b"
    return "#10b981"


def get_grade(score: float) -> tuple[str, str]:
    if score >= 85:
        return "A", "#10b981"
    if score >= 70:
        return "B", "#22c55e"
    if score >= 55:
        return "C", "#f59e0b"
    if score >= 40:
        return "D", "#f97316"
    return "E", "#ef4444"


def get_risk_label(score: float) -> tuple[str, str]:
    if score >= 75:
        return "Maturité indicative élevée", "#10b981"
    if score >= 55:
        return "Maturité indicative intermédiaire", "#f59e0b"
    return "Maturité indicative fragile", "#ef4444"


def get_maturity_label(score: float) -> str:
    if score < 33:
        return "Faible"
    if score < 66:
        return "Intermédiaire"
    return "Avancée"


def get_fit_result(score: float) -> tuple[str, str]:
    if score >= 70:
        return "Cas fortement pertinent pour ce pré-diagnostic", "#10b981"
    if score >= 40:
        return "Cas potentiellement pertinent", "#f59e0b"
    return "Cas peu prioritaire à ce stade", "#ef4444"


def compute_fit_score(
    taille: str,
    secteur: str,
    pression_rse: str,
    donnees_plm: str,
    maturite_rse_initiale: str
) -> int:
    score = 0

    size_scores = {
        "Moins de 10 salariés": 10,
        "10 à 50 salariés": 20,
        "50 à 250 salariés": 25,
        "Plus de 250 salariés": 12,
    }

    sector_scores = {
        "Sous-traitant aéronautique rang 2 ou 3": 30,
        "Bureau d’études / ingénierie": 22,
        "Fournisseur industriel hors aéronautique": 12,
        "Entreprise sans lien direct": 0,
    }

    pressure_scores = {
        "Oui, régulièrement": 25,
        "Oui, ponctuellement": 18,
        "Pas encore, mais c’est probable": 12,
        "Non": 0,
    }

    data_scores = {
        "Oui, PLM / CAO / données projets importantes": 15,
        "Oui, mais volume modéré": 10,
        "Peu": 4,
        "Non": 0,
    }

    maturity_scores = {
        "Aucune démarche structurée": 10,
        "Quelques actions isolées": 8,
        "Démarche en cours": 5,
        "Démarche déjà avancée": 2,
    }

    score += size_scores.get(taille, 0)
    score += sector_scores.get(secteur, 0)
    score += pressure_scores.get(pression_rse, 0)
    score += data_scores.get(donnees_plm, 0)
    score += maturity_scores.get(maturite_rse_initiale, 0)

    return min(score, 100)


def compute_emissions(inputs: dict) -> dict:
    nb_laptops = inputs.get("nb_laptops", 0)
    nb_workstations = inputs.get("nb_workstations", 0)
    nb_screens = inputs.get("nb_screens", 0)
    storage_active_tb = inputs.get("storage_active_tb", 0.0)
    storage_cold_tb = inputs.get("storage_cold_tb", 0.0)
    nb_servers = inputs.get("nb_servers", 0)
    nb_cloud_vm = inputs.get("nb_cloud_vm", 0)
    short_trips = inputs.get("short_trips", 0)
    long_trips = inputs.get("long_trips", 0)

    rows = [
        ("Ordinateurs portables", nb_laptops * EMISSION_FACTORS["laptop"]),
        ("Stations fixes", nb_workstations * EMISSION_FACTORS["workstation"]),
        ("Écrans", nb_screens * EMISSION_FACTORS["screen"]),
        ("Stockage actif PLM / CAO", storage_active_tb * EMISSION_FACTORS["storage_tb_active"]),
        ("Stockage froid / archives", storage_cold_tb * EMISSION_FACTORS["storage_tb_cold"]),
        ("Serveurs internes", nb_servers * EMISSION_FACTORS["server"]),
        ("Instances cloud", nb_cloud_vm * EMISSION_FACTORS["cloud_vm"]),
        ("Déplacements courts IT/AMOA", short_trips * EMISSION_FACTORS["business_trip_short"]),
        ("Déplacements longs IT/AMOA", long_trips * EMISSION_FACTORS["business_trip_long"]),
    ]

    df = pd.DataFrame(rows, columns=["Catégorie", "Émissions (kg CO₂e)"])
    total_kg = float(df["Émissions (kg CO₂e)"].sum())
    total_tonnes = total_kg / 1000

    if total_kg > 0:
        df["Part"] = df["Émissions (kg CO₂e)"].apply(lambda x: f"{(x / total_kg) * 100:.1f}%")
    else:
        df["Part"] = "0%"

    df = df[df["Émissions (kg CO₂e)"] > 0].reset_index(drop=True)
    if df.empty:
        df = pd.DataFrame({
            "Catégorie": ["Aucune donnée saisie"],
            "Émissions (kg CO₂e)": [0.0],
            "Part": ["0%"],
        })

    return {
        "df": df,
        "total_kg": total_kg,
        "total_tonnes": total_tonnes,
    }


def score_carbon_intensity(total_tonnes: float, employees: int) -> float:
    if employees <= 0:
        return 50

    tonnes_per_employee = total_tonnes / employees

    if tonnes_per_employee <= 0.7:
        return 90
    if tonnes_per_employee <= 1.5:
        return 75
    if tonnes_per_employee <= 3:
        return 55
    if tonnes_per_employee <= 5:
        return 38
    return 20


def score_governance(inputs: dict) -> float:
    checks = [
        inputs.get("iso_14001", False),
        inputs.get("deee_management", False),
        inputs.get("responsible_sourcing", False),
        inputs.get("rse_owner", False),
        inputs.get("it_inventory", False),
        inputs.get("supplier_policy", False),
    ]

    base = (sum(checks) / len(checks)) * 100

    if inputs.get("rse_frequency") == "Suivi mensuel":
        base += 8
    elif inputs.get("rse_frequency") == "Suivi trimestriel":
        base += 5
    elif inputs.get("rse_frequency") == "Suivi annuel":
        base += 2

    return clamp(base)


def score_data_management(inputs: dict) -> float:
    score = 100

    storage_active_tb = inputs.get("storage_active_tb", 0.0)
    storage_cold_tb = inputs.get("storage_cold_tb", 0.0)
    archive_policy = inputs.get("archive_policy", "Aucune")
    retention_policy = inputs.get("retention_policy", "Non")
    plm_cleanup = inputs.get("plm_cleanup", "Jamais")

    total_storage = storage_active_tb + storage_cold_tb

    if total_storage > 0:
        active_ratio = storage_active_tb / total_storage
        score -= active_ratio * 25

    if archive_policy == "Aucune":
        score -= 25
    elif archive_policy == "Informelle":
        score -= 12

    if retention_policy == "Non":
        score -= 20
    elif retention_policy == "Partielle":
        score -= 8

    if plm_cleanup == "Jamais":
        score -= 20
    elif plm_cleanup == "Rarement":
        score -= 10
    elif plm_cleanup == "Annuellement":
        score -= 4

    return clamp(score)


def score_procurement(inputs: dict) -> float:
    score = 40
    lifecycle = inputs.get("lifecycle_years", 3)

    if lifecycle >= 6:
        score += 25
    elif lifecycle >= 5:
        score += 18
    elif lifecycle >= 4:
        score += 10
    else:
        score -= 10

    if inputs.get("refurbished_policy", False):
        score += 15
    if inputs.get("repair_policy", False):
        score += 15
    if inputs.get("supplier_policy", False):
        score += 15
    if inputs.get("purchase_centralized", False):
        score += 8

    return clamp(score)


def compute_advanced_score(inputs: dict) -> dict:
    emissions = compute_emissions(inputs)
    employees = inputs.get("employees", 0)

    carbon = score_carbon_intensity(emissions["total_tonnes"], employees)
    governance = score_governance(inputs)
    data = score_data_management(inputs)
    procurement = score_procurement(inputs)

    global_score = (
        carbon * WEIGHTS["carbon"]
        + governance * WEIGHTS["governance"]
        + data * WEIGHTS["data"]
        + procurement * WEIGHTS["procurement"]
    ) / sum(WEIGHTS.values())

    grade, grade_color = get_grade(global_score)
    risk_label, risk_color = get_risk_label(global_score)

    score_rows = pd.DataFrame({
        "Pilier": ["Carbone numérique", "Gouvernance", "Données PLM / CAO", "Achats IT responsables"],
        "Score": [carbon, governance, data, procurement],
        "Poids": [WEIGHTS["carbon"], WEIGHTS["governance"], WEIGHTS["data"], WEIGHTS["procurement"]],
    })

    return {
        **emissions,
        "score_rows": score_rows,
        "carbon_score": carbon,
        "governance_score": governance,
        "data_score": data,
        "procurement_score": procurement,
        "global_score": global_score,
        "grade": grade,
        "grade_color": grade_color,
        "risk_label": risk_label,
        "risk_color": risk_color,
    }


def build_strengths(inputs: dict, result: dict) -> list[str]:
    strengths = []
    if result.get("carbon_score", 0) >= 70:
        strengths.append("L’intensité carbone numérique déclarée reste contenue par rapport à l’effectif simulé.")
    if inputs.get("it_inventory"):
        strengths.append("Un inventaire IT existe déjà : c’est une base utile pour cadrer les preuves.")
    if inputs.get("deee_management"):
        strengths.append("La gestion DEEE est déjà identifiée, ce qui donne une première trace de fin de vie matériel.")
    if inputs.get("rse_owner"):
        strengths.append("Un référent RSE / IT est identifié, donc le sujet peut être porté par une personne claire.")
    if inputs.get("repair_policy"):
        strengths.append("La réparation avant remplacement est déjà prise en compte dans les pratiques IT.")
    if inputs.get("archive_policy") == "Formalisée" or inputs.get("retention_policy") == "Oui":
        strengths.append("Une partie des règles de conservation ou d’archivage des données techniques est formalisée.")
    if not strengths:
        strengths.append("Le diagnostic donne un premier cadrage exploitable, mais les preuves structurées restent faibles.")
    return strengths[:5]


def build_weaknesses(inputs: dict, result: dict) -> list[str]:
    weaknesses = []
    if result.get("governance_score", 100) < 65:
        weaknesses.append("La gouvernance est trop dépendante de pratiques informelles : responsable, suivi, inventaire ou critères fournisseurs incomplets.")
    if result.get("data_score", 100) < 65:
        weaknesses.append("Les données CAO/PLM ne sont pas assez cadrées : rétention, archivage, nettoyage et stockage actif/archive manquent de règles explicites.")
    if result.get("procurement_score", 100) < 65:
        weaknesses.append("Les achats IT responsables sont insuffisamment formalisés : reconditionné, réparation, critères fournisseurs ou centralisation restent partiels.")
    if not inputs.get("it_inventory"):
        weaknesses.append("Sans inventaire IT fiable, le rapport reste difficile à défendre devant un client ou un fournisseur.")
    if not inputs.get("supplier_policy"):
        weaknesses.append("L’absence de critères RSE fournisseurs IT fragilise la réponse à un questionnaire client.")
    if not weaknesses:
        weaknesses.append("Les principaux risques sont moins dans le score que dans la qualité, la date et la vérifiabilité des preuves.")
    return weaknesses[:5]


def build_missing_evidence(inputs: dict, result: dict | None = None, limit: int = 8) -> list[dict]:
    missing = []

    def add(criterion: str):
        match = next((item for item in EVIDENCE_MATRIX if item["criterion"] == criterion), None)
        if match and match not in missing:
            missing.append(match)

    if not inputs.get("it_inventory"):
        add("Inventaire du parc numérique")
    if not inputs.get("deee_management"):
        add("Gestion DEEE / fin de vie")
    if not inputs.get("responsible_sourcing") or not inputs.get("supplier_policy"):
        add("Achats IT responsables")
        add("Preuves fournisseurs numériques")
    if inputs.get("archive_policy") in ["Aucune", "Informelle"]:
        add("Données CAO / PLM")
    if inputs.get("retention_policy") in ["Non", "Partielle"] or inputs.get("plm_cleanup") in ["Jamais", "Rarement"]:
        add("Règle de conservation des données techniques")
    if not inputs.get("rse_owner") or inputs.get("rse_frequency") in ["Aucun suivi", None, ""]:
        add("Gouvernance numérique responsable")
    if inputs.get("reduction_target") in ["Aucun", "Intention", None, ""]:
        add("Sensibilisation interne")

    if not missing:
        missing.append({
            "criterion": "Preuves datées et vérifiables",
            "expected": "Rassembler les documents déjà disponibles avec date, propriétaire et périmètre.",
            "example": "Tableau de preuves : document, propriétaire, date, lien, limite, statut.",
            "limit": "Même avec un bon score, un client attendra des preuves concrètes et vérifiables.",
        })

    return missing[:limit]


def build_short_term_actions(inputs: dict, result: dict) -> list[str]:
    actions = []
    if not inputs.get("it_inventory"):
        actions.append("Créer un inventaire simple du parc numérique : postes, écrans, serveurs, VM/cloud, propriétaire et date d’achat.")
    if inputs.get("archive_policy") in ["Aucune", "Informelle"]:
        actions.append("Distinguer les données CAO/PLM actives des archives et écrire une règle de bascule vers stockage froid.")
    if inputs.get("retention_policy") in ["Non", "Partielle"]:
        actions.append("Documenter une règle de conservation des données techniques avec le responsable qualité/BE/DSI.")
    if not inputs.get("supplier_policy"):
        actions.append("Ajouter un critère d’achat IT responsable dans la grille fournisseur : durée de vie, réparation, reconditionné ou preuve environnementale.")
    if not inputs.get("deee_management"):
        actions.append("Rassembler les preuves de reprise, recyclage ou effacement des équipements en fin de vie.")
    if not inputs.get("rse_owner"):
        actions.append("Nommer un référent interne chargé de centraliser les preuves RSE numériques pour les demandes client/fournisseur.")
    if not actions:
        actions.append("Passer d’un pré-diagnostic ponctuel à un tableau trimestriel de suivi : preuves, propriétaire, date de mise à jour et statut.")
    return actions[:6]


def build_recommendations(inputs: dict, result: dict) -> list[dict]:
    recos = []

    if result["carbon_score"] < 60:
        recos.append({
            "priority": "Haute",
            "title": "Cibler les postes numériques dominants",
            "text": "Identifier les 3 premiers postes du tableau d’émissions, puis relier chacun à une action vérifiable : durée de vie matériel, serveurs, stockage actif ou déplacements IT/AMOA."
        })

    if result["governance_score"] < 65:
        recos.append({
            "priority": "Haute",
            "title": "Centraliser les preuves RSE numériques",
            "text": "Créer une liste de preuves avec propriétaire, date, lien et limite : inventaire IT, DEEE, achats IT, règles de stockage, fournisseurs et sensibilisation interne."
        })

    if result["data_score"] < 65:
        recos.append({
            "priority": "Moyenne",
            "title": "Mettre sous contrôle les données CAO / PLM",
            "text": "Identifier les projets dormants depuis plus de 24 mois, distinguer stockage actif et archive, puis formaliser une règle de conservation validée avec qualité/BE/DSI."
        })

    if result["procurement_score"] < 65:
        recos.append({
            "priority": "Moyenne",
            "title": "Formaliser un critère d’achat IT responsable",
            "text": "Ajouter dans la grille d’achat : durée d’usage cible, réparation avant remplacement, option reconditionnée, preuve fournisseur et procédure de fin de vie."
        })

    if not inputs.get("it_inventory"):
        recos.append({
            "priority": "Haute",
            "title": "Créer l’inventaire numérique minimal",
            "text": "Lister postes, écrans, serveurs, cloud/VM, date d’achat, propriétaire et statut. Sans cette base, le rapport reste difficile à défendre."
        })

    if not recos:
        recos.append({
            "priority": "Optimisation",
            "title": "Passer du pré-diagnostic au pilotage continu",
            "text": "Conserver les preuves datées, vérifier leur périmètre et suivre les indicateurs tous les trimestres avant toute demande client ou fournisseur."
        })

    return recos[:5]
