import pandas as pd
import streamlit as st

from components.cards import render_page_header, render_icon_card
from services.calculations import EVIDENCE_MATRIX, PILLAR_EXPLANATIONS, WEIGHTS


def render_methodology():
    render_page_header(
        "Méthodologie & limites",
        "Lecture du score, logique des preuves, périmètre du prototype et interprétation correcte des résultats.",
        "Anti-bullshit"
    )

    st.markdown("""
    <div class='card-soft' style='border:1px solid rgba(245,158,11,.28); background:rgba(255,251,235,.72);'>
        <div class='section-title'>Avertissement court</div>
        <strong>AeroGreen Diag est un prototype pédagogique, pas un outil de conformité.</strong>
        <div class='feature-text'>
            Les scores et recommandations sont indicatifs. Le projet s’inspire de logiques de structuration de preuves
            et de maturité observées dans des démarches RSE, numériques responsables ou questionnaires fournisseurs,
            sans reproduire ni remplacer un référentiel officiel.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Ce que l’outil peut faire")
    st.markdown("""
    <div class='card'>
        <ul>
            <li>transformer des réponses déclaratives en lecture de maturité numérique responsable ;</li>
            <li>identifier les piliers faibles : carbone numérique, gouvernance, données CAO/PLM, achats IT ;</li>
            <li>proposer des recommandations concrètes et compréhensibles ;</li>
            <li>lister des preuves RSE numériques à rassembler ;</li>
            <li>générer un rapport de travail exploitable en discussion.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Ce que l’outil ne peut pas faire")
    c1, c2, c3 = st.columns(3)
    with c1:
        render_icon_card("⚠️", "Pas certification", "Aucune conformité, médaille ou reconnaissance officielle n’est produite.", "#ef4444")
    with c2:
        render_icon_card("📉", "Pas bilan carbone", "Les facteurs d’émission sont simplifiés et ne couvrent pas un périmètre GES réglementaire.", "#f59e0b")
    with c3:
        render_icon_card("👤", "Pas audit consultant", "Le diagnostic ne vérifie pas les preuves et ne remplace pas une analyse terrain.", "#64748b")

    st.markdown("## Fonctionnement du scoring")
    st.markdown("""
    <div class='card'>
        <p class='feature-text'>
            Le diagnostic collecte des réponses déclaratives : effectif, parc informatique, postes CAO/PLM, stockage,
            gouvernance RSE numérique, politique d’achats IT, gestion des équipements et déplacements liés aux projets numériques.
            Ces réponses sont converties en quatre scores intermédiaires puis agrégées en un score indicatif sur 100.
        </p>
    </div>
    """, unsafe_allow_html=True)

    pillar_df = pd.DataFrame([
        {
            "Pilier": pillar,
            "Poids indicatif": f"{WEIGHTS[key]}%",
            "Pourquoi c’est pertinent": explanation,
        }
        for key, pillar, explanation in [
            ("carbon", "Carbone numérique", PILLAR_EXPLANATIONS["Carbone numérique"]),
            ("governance", "Gouvernance", PILLAR_EXPLANATIONS["Gouvernance"]),
            ("data", "Données PLM / CAO", PILLAR_EXPLANATIONS["Données PLM / CAO"]),
            ("procurement", "Achats IT responsables", PILLAR_EXPLANATIONS["Achats IT responsables"]),
        ]
    ])
    st.dataframe(pillar_df, use_container_width=True, hide_index=True)

    st.markdown("## Matrice de preuves RSE numériques")
    evidence_df = pd.DataFrame(EVIDENCE_MATRIX)
    evidence_df.columns = ["Critère / question", "Preuve attendue", "Exemple concret", "Limite"]
    st.dataframe(evidence_df, use_container_width=True, hide_index=True)

    st.markdown("## Comment interpréter le score")
    st.markdown("""
    <div class='card'>
        <ul>
            <li><strong>80–100 :</strong> maturité indicative élevée, à vérifier avec des preuves datées.</li>
            <li><strong>60–79 :</strong> base structurée, mais des zones doivent être consolidées.</li>
            <li><strong>40–59 :</strong> maturité intermédiaire, preuves et gouvernance souvent incomplètes.</li>
            <li><strong>0–39 :</strong> pré-diagnostic fragile, besoin de cadrage avant échange externe.</li>
        </ul>
        <p class='feature-text'>
            Le score doit être lu comme une boussole : il aide à prioriser un plan de travail, pas à prouver une conformité.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Limites assumées")
    st.markdown("""
    <div class='card-soft'>
        <ul>
            <li>données déclaratives non vérifiées ;</li>
            <li>pondérations construites pour un démonstrateur, pas validées par un organisme ;</li>
            <li>facteurs d’émission volontairement simplifiés ;</li>
            <li>absence d’analyse terrain et de revue documentaire réelle ;</li>
            <li>preuves non auditées, non datées automatiquement et non validées ;</li>
            <li>pas de garantie de préparation REEN, EcoVadis, client ou réglementaire ;</li>
            <li>résultats utiles pour apprendre, cadrer et discuter, pas pour certifier.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Pourquoi cette limite rend le projet plus crédible")
    st.info(
        "Un recruteur ou un manager produit doit comprendre que le projet n’essaie pas de simuler une expertise réglementaire. "
        "Il montre une capacité à cadrer un problème B2B, structurer une grille d’analyse, produire un livrable et assumer les limites."
    )
