import math
import pandas as pd


EMISSION_FACTORS = {
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
        return "Risque faible", "#10b981"
    if score >= 55:
        return "Risque modéré", "#f59e0b"
    return "Risque élevé", "#ef4444"


def get_maturity_label(score: float) -> str:
    if score < 33:
        return "Faible"
    if score < 66:
        return "Intermédiaire"
    return "Avancée"


def get_fit_result(score: float) -> tuple[str, str]:
    if score >= 70:
        return "Solution fortement pertinente", "#10b981"
    if score >= 40:
        return "Solution potentiellement pertinente", "#f59e0b"
    return "Solution non prioritaire à ce stade", "#ef4444"


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

    # heuristic pre-audit: lower is better
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
        score -= 5

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
        "Pilier": ["Carbone", "Gouvernance", "Données", "Achats IT"],
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


def build_recommendations(inputs: dict, result: dict) -> list[dict]:
    recos = []

    if result["carbon_score"] < 60:
        recos.append({
            "priority": "Haute",
            "title": "Réduire l’intensité carbone numérique",
            "text": "Prioriser les postes dominants du bilan : matériel, serveurs, stockage actif ou déplacements liés aux projets IT."
        })

    if result["governance_score"] < 65:
        recos.append({
            "priority": "Haute",
            "title": "Structurer la gouvernance RSE numérique",
            "text": "Nommer un référent, créer un inventaire IT fiable et formaliser une politique DEEE / achats responsables."
        })

    if result["data_score"] < 65:
        recos.append({
            "priority": "Moyenne",
            "title": "Mettre sous contrôle les données PLM / CAO",
            "text": "Définir une politique de rétention, nettoyer les projets dormants et basculer les archives vers du stockage froid."
        })

    if result["procurement_score"] < 65:
        recos.append({
            "priority": "Moyenne",
            "title": "Allonger le cycle de vie matériel",
            "text": "Étendre la durée d’usage des équipements, favoriser réparation, reconditionné et achats centralisés."
        })

    if not recos:
        recos.append({
            "priority": "Optimisation",
            "title": "Passer du pré-audit au pilotage continu",
            "text": "L’entreprise dispose d’une bonne base. Prochaine étape : indicateurs trimestriels, preuves RSE et trajectoire annuelle."
        })

    return recos
