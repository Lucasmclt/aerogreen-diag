from fpdf import FPDF


def safe_text(value) -> str:
    return str(value).encode("latin-1", "replace").decode("latin-1")


class AeroGreenPDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42)
        self.rect(0, 0, 210, 28, "F")
        self.set_font("Arial", "B", 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 14, "AeroGreen", 0, 1, "C")
        self.set_font("Arial", "", 9)
        self.cell(0, 6, "Rapport premium de pre-audit carbone numerique", 0, 1, "C")
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, "Document genere automatiquement - Non substitut a un audit reglementaire complet", 0, 0, "C")

    def section_title(self, title):
        self.set_font("Arial", "B", 13)
        self.set_text_color(15, 23, 42)
        self.set_fill_color(241, 245, 249)
        self.cell(0, 10, safe_text(title), 0, 1, "L", True)
        self.ln(2)

    def label_value(self, label, value):
        self.set_font("Arial", "B", 10)
        self.set_text_color(75, 85, 99)
        self.cell(60, 7, safe_text(label), 0, 0)
        self.set_font("Arial", "", 10)
        self.set_text_color(17, 24, 39)
        self.cell(0, 7, safe_text(value), 0, 1)


def create_premium_pdf_bytes(company: dict, result: dict, recommendations: list[dict], fit_score: float, fit_result: str):
    pdf = AeroGreenPDF()
    pdf.add_page()

    # Cover summary
    pdf.section_title("1. Synthese executive")

    pdf.label_value("Entreprise", company.get("company_name", "Non renseignee"))
    pdf.label_value("Ville", company.get("company_city", "Non renseignee"))
    pdf.label_value("Secteur", company.get("company_sector", "Non renseigne"))
    pdf.label_value("Reference dossier", company.get("client_reference", "N/A"))

    pdf.ln(4)

    pdf.set_fill_color(248, 250, 252)
    pdf.rect(10, pdf.get_y(), 190, 34, "F")
    y = pdf.get_y() + 5

    pdf.set_xy(14, y)
    pdf.set_font("Arial", "B", 11)
    pdf.set_text_color(75, 85, 99)
    pdf.cell(55, 6, "Score global", 0, 0)
    pdf.cell(55, 6, "Grade", 0, 0)
    pdf.cell(55, 6, "Empreinte", 0, 1)

    pdf.set_x(14)
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(17, 24, 39)
    pdf.cell(55, 12, f"{result['global_score']:.0f}/100", 0, 0)
    pdf.cell(55, 12, result["grade"], 0, 0)
    pdf.cell(55, 12, f"{result['total_tonnes']:.2f} tCO2e", 0, 1)

    pdf.set_x(14)
    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(55, 6, safe_text(result["risk_label"]), 0, 0)
    pdf.cell(55, 6, "Pre-audit simplifie", 0, 0)
    pdf.cell(55, 6, "Estimation numerique", 0, 1)

    pdf.ln(8)

    pdf.section_title("2. Scores par pilier")
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(241, 245, 249)
    pdf.cell(70, 9, "Pilier", 1, 0, "L", True)
    pdf.cell(40, 9, "Score", 1, 0, "C", True)
    pdf.cell(40, 9, "Poids", 1, 1, "C", True)

    pdf.set_font("Arial", "", 10)
    for _, row in result["score_rows"].iterrows():
        pdf.cell(70, 9, safe_text(row["Pilier"]), 1)
        pdf.cell(40, 9, f"{row['Score']:.0f}/100", 1, 0, "C")
        pdf.cell(40, 9, f"{row['Poids']}%", 1, 1, "C")

    pdf.ln(5)

    pdf.section_title("3. Detail des emissions")
    pdf.set_font("Arial", "B", 9)
    pdf.set_fill_color(241, 245, 249)
    pdf.cell(78, 8, "Categorie", 1, 0, "L", True)
    pdf.cell(55, 8, "Emissions kgCO2e", 1, 0, "C", True)
    pdf.cell(35, 8, "Part", 1, 1, "C", True)

    pdf.set_font("Arial", "", 8)
    for _, row in result["df"].iterrows():
        pdf.cell(78, 8, safe_text(row["Catégorie"])[:36], 1)
        pdf.cell(55, 8, f"{row['Émissions (kg CO₂e)']:.2f}", 1, 0, "C")
        pdf.cell(35, 8, safe_text(row["Part"]), 1, 1, "C")

    pdf.ln(5)

    pdf.section_title("4. Recommandations prioritaires")
    pdf.set_font("Arial", "", 10)
    for reco in recommendations:
        pdf.set_font("Arial", "B", 10)
        pdf.set_text_color(15, 23, 42)
        pdf.multi_cell(0, 6, safe_text(f"[{reco['priority']}] {reco['title']}"))
        pdf.set_font("Arial", "", 9)
        pdf.set_text_color(75, 85, 99)
        pdf.multi_cell(0, 5, safe_text(reco["text"]))
        pdf.ln(2)

    pdf.section_title("5. Adequation AeroGreen")
    pdf.label_value("Score d'adequation", f"{fit_score:.0f}%")
    pdf.label_value("Conclusion", fit_result)

    pdf.ln(3)
    pdf.set_font("Arial", "", 9)
    pdf.set_text_color(100, 116, 139)
    pdf.multi_cell(
        0,
        5,
        safe_text(
            "Ce document constitue un pre-audit simplifie. Les facteurs d'emission et scores sont indicatifs "
            "et doivent etre consolides avec des donnees internes et referentiels officiels avant usage contractuel."
        )
    )

    return pdf.output(dest="S").encode("latin-1", errors="replace")
