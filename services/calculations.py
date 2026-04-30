import pandas as pd


EMISSION_FACTORS = {
    "laptop": 193,
    "workstation": 350,
    "screen": 200,
    "storage_tb": 0.24,
}


def get_score_color(score: float) -> str:
    if score < 33:
        return "#ef4444"
    if score < 66:
        return "#f59e0b"
    return "#10b981"


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


def get_emissions_color(total_tonnes: float) -> str:
    if total_tonnes <= 0:
        return "#6b7280"
    if total_tonnes < 10:
        return "#10b981"
    if total_tonnes < 50:
        return "#f59e0b"
    return "#ef4444"


def compute_fit_score(
    taille: str,
    secteur: str,
    pression_rse: str,
    donnees_plm: str,
    maturite_rse_initiale: str
) -> int:
    score = 0

    if taille == "10 à 50 salariés":
        score += 20
    elif taille == "50 à 250 salariés":
        score += 25
    elif taille == "Moins de 10 salariés":
        score += 10
    else:
        score += 12

    if secteur == "Sous-traitant aéronautique rang 2 ou 3":
        score += 30
    elif secteur == "Bureau d’études / ingénierie":
        score += 22
    elif secteur == "Fournisseur industriel hors aéronautique":
        score += 12

    if pression_rse == "Oui, régulièrement":
        score += 25
    elif pression_rse == "Oui, ponctuellement":
        score += 18
    elif pression_rse == "Pas encore, mais c’est probable":
        score += 12

    if donnees_plm == "Oui, PLM / CAO / données projets importantes":
        score += 15
    elif donnees_plm == "Oui, mais volume modéré":
        score += 10
    elif donnees_plm == "Peu":
        score += 4

    if maturite_rse_initiale == "Aucune démarche structurée":
        score += 10
    elif maturite_rse_initiale == "Quelques actions isolées":
        score += 8
    elif maturite_rse_initiale == "Démarche en cours":
        score += 5

    return min(score, 100)


def compute_diagnostic(
    nb_laptops: int,
    nb_workstations: int,
    nb_screens: int,
    storage_tb: float,
    iso_14001: bool,
    deee_management: bool,
    responsible_sourcing: bool
) -> dict:
    laptop_emissions = nb_laptops * EMISSION_FACTORS["laptop"]
    workstation_emissions = nb_workstations * EMISSION_FACTORS["workstation"]
    screen_emissions = nb_screens * EMISSION_FACTORS["screen"]
    storage_emissions = storage_tb * EMISSION_FACTORS["storage_tb"]

    total_kg = (
        laptop_emissions
        + workstation_emissions
        + screen_emissions
        + storage_emissions
    )

    total_tonnes = total_kg / 1000

    maturity_score = (
        sum([iso_14001, deee_management, responsible_sourcing]) / 3
    ) * 100

    df = pd.DataFrame({
        "Catégorie": [
            "Ordinateurs portables",
            "Stations fixes",
            "Écrans",
            "Stockage PLM"
        ],
        "Émissions (kg CO₂e)": [
            laptop_emissions,
            workstation_emissions,
            screen_emissions,
            storage_emissions
        ]
    })

    if total_kg > 0:
        df["Part"] = df["Émissions (kg CO₂e)"].apply(
            lambda x: f"{(x / total_kg) * 100:.1f}%"
        )
    else:
        df["Part"] = "0%"

    return {
        "df": df,
        "total_kg": total_kg,
        "total_tonnes": total_tonnes,
        "maturity_score": maturity_score,
    }
