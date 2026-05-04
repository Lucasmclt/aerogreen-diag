from fpdf import FPDF
import pandas as pd

from services.calculations import (
    build_missing_evidence,
    build_short_term_actions,
    build_strengths,
    build_weaknesses,
)


def safe_text(value) -> str:
    return str(value).encode("latin-1", "replace").decode("latin-1")


def _as_dataframe(value) -> pd.DataFrame:
    if isinstance(value, pd.DataFrame):
        return value
    if isinstance(value, list):
        return pd.DataFrame(value)
    return pd.DataFrame()


def _pdf_output_bytes(pdf: FPDF) -> bytes:
    raw = pdf.output(dest="S")
    if isinstance(raw, bytes):
        return raw
    if isinstance(raw, bytearray):
        return bytes(raw)
    return raw.encode("latin-1", errors="replace")


class AeroGreenPDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 28, "F")
        self.set_font("Arial", "B", 15)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, safe_text("AeroGreen Diag"), 0, 1, "C")
        self.set_font("Arial", "", 9)
        self.cell(0, 6, safe_text("Rapport de pré-diagnostic indicatif - prototype portfolio"), 0, 1, "C")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, safe_text("Document de travail - non officiel - ne remplace pas un audit, une certification ou une validation réglementaire"), 0, 0, "C")

    def section_title(self, title):
        self.set_x(10)
        self.set_font("Arial", "B", 12)
        self.set_text_color(15, 23, 42)
        self.set_fill_color(241, 245, 249)
        self.cell(190, 9, safe_text(title), 0, 1, "L", True)
        self.ln(2)

    def paragraph(self, text, size=9.2):
        self.set_x(10)
        self.set_font("Arial", "", size)
        self.set_text_color(55, 65, 81)
        self.multi_cell(190, 5.2, safe_text(text))
        self.ln(1.5)

    def bullet(self, text, size=9.2):
        self.set_x(10)
        self.set_font("Arial", "", size)
        self.set_text_color(55, 65, 81)
        self.multi_cell(190, 5.2, safe_text(f"- {text}"))

    def label_value(self, label, value):
        self.set_x(10)
        self.set_font("Arial", "B", 9.5)
        self.set_text_color(75, 85, 99)
        self.cell(55, 7, safe_text(label), 0, 0)
        self.set_font("Arial", "", 9.5)
        self.set_text_color(17, 24, 39)
        self.multi_cell(135, 7, safe_text(value))


def _render_score_box(pdf: AeroGreenPDF, result: dict):
    pdf.set_fill_color(248, 250, 252)
    pdf.rect(10, pdf.get_y(), 190, 34, "F")
    y = pdf.get_y() + 5

    pdf.set_xy(14, y)
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(75, 85, 99)
    pdf.cell(55, 6, "Score global", 0, 0)
    pdf.cell(55, 6, "Grade", 0, 0)
    pdf.cell(55, 6, "Empreinte", 0, 1)

    pdf.set_x(14)
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(17, 24, 39)
    pdf.cell(55, 12, f"{result.get('global_score', 0):.0f}/100", 0, 0)
    pdf.cell(55, 12, safe_text(result.get("grade", "N/A")), 0, 0)
    pdf.cell(55, 12, f"{result.get('total_tonnes', 0):.2f} tCO2e", 0, 1)

    pdf.set_x(14)
    pdf.set_font("Arial", "", 8.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(55, 6, safe_text(result.get("risk_label", "Score indicatif")), 0, 0)
    pdf.cell(55, 6, "Lecture A-E", 0, 0)
    pdf.cell(55, 6, "Ordre de grandeur", 0, 1)
    pdf.ln(8)


def _render_pillar_table(pdf: AeroGreenPDF, result: dict):
    score_rows = _as_dataframe(result.get("score_rows", []))
    if score_rows.empty:
        return

    pdf.set_font("Arial", "B", 9)
    pdf.set_fill_color(241, 245, 249)
    pdf.cell(82, 8, "Pilier", 1, 0, "L", True)
    pdf.cell(35, 8, "Score", 1, 0, "C", True)
    pdf.cell(35, 8, "Poids", 1, 1, "C", True)

    pdf.set_font("Arial", "", 9)
    for _, row in score_rows.iterrows():
        pdf.cell(82, 8, safe_text(row.get("Pilier", ""))[:42], 1)
        pdf.cell(35, 8, f"{float(row.get('Score', 0)):.0f}/100", 1, 0, "C")
        pdf.cell(35, 8, f"{float(row.get('Poids', 0)):.0f}%", 1, 1, "C")
    pdf.ln(4)


def _render_emission_summary(pdf: AeroGreenPDF, result: dict):
    df = _as_dataframe(result.get("df", []))
    if df.empty:
        return

    pdf.set_font("Arial", "B", 9)
    pdf.set_fill_color(241, 245, 249)
    pdf.cell(88, 8, "Catégorie", 1, 0, "L", True)
    pdf.cell(42, 8, "kgCO2e", 1, 0, "C", True)
    pdf.cell(30, 8, "Part", 1, 1, "C", True)

    pdf.set_font("Arial", "", 8.5)
    for _, row in df.head(6).iterrows():
        pdf.cell(88, 8, safe_text(row.get("Catégorie", ""))[:44], 1)
        pdf.cell(42, 8, f"{float(row.get('Émissions (kg CO₂e)', 0)):.1f}", 1, 0, "C")
        pdf.cell(30, 8, safe_text(row.get("Part", "")), 1, 1, "C")
    pdf.ln(4)


def create_working_report_pdf_bytes(
    company: dict,
    result: dict,
    recommendations: list[dict],
    fit_score: float,
    fit_result: str,
    inputs: dict | None = None,
):
    inputs = inputs or {}
    strengths = build_strengths(inputs, result)
    weaknesses = build_weaknesses(inputs, result)
    missing_evidence = build_missing_evidence(inputs, result, limit=6)
    short_actions = build_short_term_actions(inputs, result)

    pdf = AeroGreenPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    pdf.section_title("1. Contexte du diagnostic")
    pdf.label_value("Entreprise", company.get("company_name", "Non renseignée"))
    pdf.label_value("Ville", company.get("company_city", "Non renseignée"))
    pdf.label_value("Secteur", company.get("company_sector", "Non renseigné"))
    pdf.label_value("Référence dossier", company.get("client_reference", "N/A"))
    pdf.paragraph(
        "Ce rapport présente un pré-diagnostic indicatif de maturité numérique responsable. "
        "Il est conçu comme un support de discussion pour structurer des preuves avant une demande client, fournisseur ou interne."
    )

    pdf.section_title("2. Objectif du pré-diagnostic")
    pdf.paragraph(
        "L’objectif est de transformer des réponses déclaratives en une lecture structurée : score par pilier, zones faibles, "
        "preuves à consolider, recommandations prioritaires et prochaines actions. Le rapport ne prétend pas mesurer une empreinte carbone réelle."
    )

    pdf.section_title("3. Score global indicatif")
    _render_score_box(pdf, result)

    pdf.section_title("4. Lecture par pilier")
    _render_pillar_table(pdf, result)
    pdf.paragraph(
        "Les pondérations sont construites pour un démonstrateur portfolio. Elles servent à prioriser une discussion, pas à produire une notation officielle."
    )

    pdf.section_title("5. Forces identifiées")
    for item in strengths:
        pdf.bullet(item)
    pdf.ln(2)

    pdf.section_title("6. Faiblesses principales")
    for item in weaknesses:
        pdf.bullet(item)
    pdf.ln(2)

    pdf.section_title("7. Preuves manquantes ou à consolider")
    for item in missing_evidence:
        pdf.set_font("Arial", "B", 9.2)
        pdf.set_text_color(15, 23, 42)
        pdf.set_x(10)
        pdf.multi_cell(190, 5.2, safe_text(item["criterion"]))
        pdf.set_font("Arial", "", 8.7)
        pdf.set_text_color(75, 85, 99)
        pdf.set_x(10)
        pdf.multi_cell(190, 4.8, safe_text(f"Preuve attendue : {item['expected']}"))
        pdf.set_x(10)
        pdf.multi_cell(190, 4.8, safe_text(f"Exemple : {item['example']}"))
        pdf.set_x(10)
        pdf.multi_cell(190, 4.8, safe_text(f"Limite : {item['limit']}"))
        pdf.ln(1.5)

    pdf.section_title("8. Recommandations prioritaires")
    for reco in recommendations:
        pdf.set_font("Arial", "B", 9.5)
        pdf.set_text_color(15, 23, 42)
        pdf.set_x(10)
        pdf.multi_cell(190, 5.5, safe_text(f"[{reco['priority']}] {reco['title']}"))
        pdf.set_font("Arial", "", 8.8)
        pdf.set_text_color(75, 85, 99)
        pdf.set_x(10)
        pdf.multi_cell(190, 5, safe_text(reco["text"]))
        pdf.ln(1.5)

    pdf.section_title("9. Actions court terme")
    for action in short_actions:
        pdf.bullet(action, size=8.8)
    pdf.ln(2)

    pdf.section_title("10. Répartition carbone indicative")
    _render_emission_summary(pdf, result)
    pdf.paragraph(
        "Les facteurs utilisés sont des proxys simplifiés. Ils ne couvrent pas un bilan GES réglementaire et ne doivent pas être utilisés comme preuve carbone."
    )

    pdf.section_title("11. Limites méthodologiques")
    limits = [
        "Données déclaratives non vérifiées.",
        "Pondérations indicatives, non validées par un organisme externe.",
        "Facteurs d’émission simplifiés et périmètre carbone incomplet.",
        "Aucune preuve documentaire n’est auditée par l’application.",
        "Le projet s’inspire de logiques de structuration de preuves et de maturité, sans reproduire ni remplacer un référentiel officiel.",
        "Ce rapport ne constitue ni audit, ni certification, ni notation EcoVadis, ni garantie REEN ou conformité client.",
    ]
    for limit in limits:
        pdf.bullet(limit, size=8.8)

    pdf.section_title("12. Prochaines étapes possibles")
    next_steps = [
        "Rassembler les preuves listées avec propriétaire, date et périmètre.",
        "Valider les hypothèses avec DSI, qualité, achats et bureau d’études.",
        "Comparer le dossier avec les demandes réelles du client ou du fournisseur.",
        "Faire relire le rapport par un expert RSE/qualité avant tout usage externe.",
    ]
    for step in next_steps:
        pdf.bullet(step, size=8.8)

    pdf.section_title("13. Adéquation au cas d’usage")
    pdf.label_value("Score d’adéquation", f"{fit_score:.0f}%")
    pdf.label_value("Conclusion", fit_result or "Non renseigné")

    return _pdf_output_bytes(pdf)
