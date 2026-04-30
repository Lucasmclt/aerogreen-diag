from fpdf import FPDF


class AeroGreenPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 18)
        self.set_text_color(20, 20, 20)
        self.cell(0, 15, "AeroGreen - Rapport de pre-diagnostic", 0, 1, "C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(
            0,
            10,
            "Document genere automatiquement - Pre-audit carbone numerique",
            0,
            0,
            "C"
        )


def create_pdf_bytes(
    total_tonnes,
    df_detail,
    maturity_score,
    fit_score,
    fit_result
):
    pdf = AeroGreenPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "1. Synthese", 0, 1)

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Empreinte numerique estimee : {total_tonnes:.2f} tCO2e", 0, 1)
    pdf.cell(0, 8, f"Maturite RSE numerique : {maturity_score:.0f}%", 0, 1)
    pdf.cell(0, 8, f"Score d'adequation AeroGreen : {fit_score:.0f}%", 0, 1)
    pdf.cell(0, 8, f"Conclusion : {fit_result}", 0, 1)

    pdf.ln(8)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "2. Detail des emissions", 0, 1)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(65, 9, "Categorie", 1)
    pdf.cell(65, 9, "Emissions kgCO2e", 1)
    pdf.cell(40, 9, "Part", 1)
    pdf.ln()

    pdf.set_font("Arial", "", 10)

    for _, row in df_detail.iterrows():
        pdf.cell(65, 9, str(row["Catégorie"]).encode("latin-1", "replace").decode("latin-1"), 1)
        pdf.cell(65, 9, str(row["Émissions (kg CO₂e)"]).encode("latin-1", "replace").decode("latin-1"), 1)
        pdf.cell(40, 9, str(row["Part"]).encode("latin-1", "replace").decode("latin-1"), 1)
        pdf.ln()

    pdf.ln(8)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "3. Recommandations prioritaires", 0, 1)

    pdf.set_font("Arial", "", 10)

    recommendations = [
        "Allonger la duree de vie des postes informatiques au-dela de 5 ans.",
        "Mettre en place une politique de gestion DEEE pour le materiel obsolete.",
        "Identifier les donnees PLM dormantes et les basculer vers du stockage froid.",
        "Integrer des criteres RSE dans le choix des fournisseurs IT.",
        "Structurer une premiere feuille de route RSE numerique compatible avec les exigences donneurs d'ordre."
    ]

    for recommendation in recommendations:
        pdf.multi_cell(0, 6, f"- {recommendation}")

    return pdf.output(dest="S").encode("latin-1", errors="replace")
