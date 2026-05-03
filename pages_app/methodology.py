import streamlit as st

from components.cards import render_page_header, render_icon_card


def render_methodology():
    render_page_header(
        "Méthodologie & limites",
        "Mode d’emploi du score, périmètre du prototype et interprétation correcte des résultats.",
        "Cadre du démonstrateur"
    )

    st.markdown("""
    <div class='card-soft' style='border:1px solid rgba(245,158,11,.28); background:rgba(255,251,235,.72);'>
        <div class='section-title'>Avertissement court</div>
        <strong>AeroGreen Diag est un prototype pédagogique.</strong>
        <div class='feature-text'>
            Les scores et recommandations sont indicatifs et ne constituent ni un audit officiel, ni une certification,
            ni une évaluation EcoVadis, ni un bilan carbone réglementaire.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Fonctionnement du scoring")
    st.markdown("""
    <div class='card'>
        <p class='feature-text'>
            Le diagnostic collecte des réponses déclaratives : effectif, parc informatique, postes CAO/PLM, stockage,
            gouvernance RSE numérique, politique d’achats IT, gestion des équipements et déplacements liés aux projets numériques.
            Ces réponses sont converties en quatre scores intermédiaires puis agrégées en un score indicatif sur 100.
        </p>
        <ul>
            <li><strong>Carbone numérique — 35 % :</strong> ordre de grandeur simplifié lié au matériel, serveurs, cloud, stockage et déplacements IT.</li>
            <li><strong>Gouvernance — 25 % :</strong> référent, inventaire, suivi, formalisation et politiques internes.</li>
            <li><strong>Données — 20 % :</strong> archivage, rétention, stockage actif/froid et nettoyage des données PLM/CAO.</li>
            <li><strong>Achats IT — 20 % :</strong> durée de vie, réparation, reconditionné, centralisation et critères fournisseurs.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Dimensions évaluées")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_icon_card("🌱", "Carbone numérique", "Estimation simplifiée des principaux postes numériques.", "#10b981")
    with c2:
        render_icon_card("🧭", "Gouvernance", "Capacité à piloter, documenter et suivre le sujet.", "#6366f1")
    with c3:
        render_icon_card("🗃️", "Données PLM/CAO", "Hygiène documentaire, archivage et rétention des données techniques.", "#0ea5e9")
    with c4:
        render_icon_card("🔧", "Achats IT", "Cycle de vie matériel, réparation, fournisseurs et achats responsables.", "#8b5cf6")

    st.markdown("## Logique des recommandations")
    st.markdown("""
    <div class='card-soft'>
        <div class='section-title'>Règle simple</div>
        <strong>Une recommandation apparaît lorsqu’un pilier descend sous un seuil de maturité.</strong>
        <div class='feature-text'>
            Les recommandations ne sont pas des prescriptions d’expert. Elles servent à transformer le score en pistes de travail :
            mieux inventorier le parc IT, formaliser les preuves, structurer les achats, nettoyer les données dormantes ou préparer
            une discussion avec un client industriel.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Ce que le prototype ne prétend pas faire")
    c1, c2, c3 = st.columns(3)
    with c1:
        render_icon_card("⚠️", "Pas EcoVadis", "Aucune médaille, notation ou reconnaissance EcoVadis n’est calculée.", "#ef4444")
    with c2:
        render_icon_card("📉", "Pas bilan carbone", "Les facteurs d’émission sont simplifiés et ne couvrent pas un périmètre GES réglementaire.", "#f59e0b")
    with c3:
        render_icon_card("👤", "Pas consultant RSE", "Le diagnostic ne remplace pas une analyse terrain, documentaire ou réglementaire.", "#64748b")

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
            <li>pas de garantie de préparation REEN, EcoVadis ou client ;</li>
            <li>résultats utiles pour apprendre, cadrer et discuter, pas pour certifier.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Pourquoi cette limite rend le projet crédible")
    st.info(
        "Le projet gagne en crédibilité parce qu’il annonce clairement son périmètre : démontrer une démarche produit, "
        "un raisonnement business et une capacité de prototypage, sans survendre une expertise réglementaire ou RSE officielle."
    )
