# AeroGreen Diag

**AeroGreen Diag est un prototype portfolio qui aide une PME industrielle à structurer un premier dossier de preuves RSE numériques avant une demande client ou fournisseur.**

Projet personnel réalisé avant mon entrée à **TBS en L3**, après un parcours **prépa EPITA**. L’objectif n’est pas de vendre un SaaS : l’objectif est de montrer ma capacité à traduire un problème industriel, RSE et business en outil numérique clair, utilisable et défendable.

---

## Pitch en une phrase

AeroGreen Diag aide une PME industrielle ou un sous-traitant aéronautique à transformer des réponses déclaratives en **pré-diagnostic indicatif**, avec score de maturité, preuves à consolider, recommandations concrètes et rapport PDF de travail.

---

## Pourquoi ce projet

Une PME industrielle peut recevoir une demande client, fournisseur ou interne sur ses pratiques RSE numériques : parc IT, données CAO/PLM, achats IT, stockage, fin de vie matériel, sobriété numérique ou preuves documentaires.

Le problème n’est pas seulement de “faire de la RSE”. Le vrai problème est souvent plus concret :

- quelles preuves faut-il rassembler ?
- qui possède ces preuves dans l’entreprise ?
- quelles pratiques sont formalisées et lesquelles restent informelles ?
- quelles zones faibles faut-il traiter avant une discussion client ?
- comment produire un premier support lisible sans prétendre faire un audit officiel ?

AeroGreen Diag explore cette situation sous forme de démonstrateur Streamlit.

---

## Ce que le projet démontre

Ce projet est conçu pour envoyer un signal professionnel supérieur à “je sais faire une app Streamlit”. Il démontre :

- cadrage d’un problème B2B concret ;
- compréhension d’une cible industrielle locale ;
- transformation d’un sujet métier flou en parcours utilisateur ;
- logique de diagnostic multicritère ;
- structuration de preuves RSE numériques ;
- génération d’un rapport PDF exploitable hors application ;
- prudence méthodologique et limites assumées ;
- articulation tech, produit, business, RSE, industrie et UX.

---

## Ce que le projet n’est pas

AeroGreen Diag ne prétend pas :

- être une startup SaaS prête à vendre ;
- certifier une entreprise ;
- produire un audit carbone réglementaire ;
- calculer un bilan GES ;
- attribuer une notation EcoVadis ;
- garantir une conformité REEN ;
- remplacer un consultant RSE, qualité ou carbone ;
- valider des preuves documentaires ;
- fournir une décision contractuelle ou réglementaire.

Le projet s’inspire de logiques de structuration de preuves et de maturité observées dans des démarches RSE, numériques responsables ou questionnaires fournisseurs, **sans reproduire ni remplacer un référentiel officiel**.

---

## Cible fictive / contexte métier

La cible simulée est une **PME industrielle / sous-traitant aéronautique autour de Toulouse**.

Ce contexte est pertinent parce que ces entreprises peuvent manipuler :

- données techniques ;
- CAO / PLM / PDM ;
- postes de travail puissants ;
- stockage actif et archives projets ;
- documentation qualité ;
- chaîne fournisseur ;
- demandes de grands donneurs d’ordre ;
- achats IT et prestataires numériques.

Le cas d’étude intégré s’appelle **AeroPart Occitanie** : PME fictive de 80 salariés située à Blagnac, sous-traitant aéronautique de rang 2, avec preuves RSE numériques partielles mais dispersées.

---

## Fonctionnalités principales

- page d’accueil avec positionnement clair ;
- test rapide d’adéquation ;
- cas d’étude fictif réaliste ;
- diagnostic guidé multi-étapes ;
- scoring indicatif par pilier ;
- dashboard qui affiche clairement le diagnostic actif ;
- matrice de preuves RSE numériques ;
- recommandations concrètes ;
- rapport PDF de travail ;
- persistance locale SQLite en mode démo.

---

## Démo en 3 minutes

1. **Problème** : une PME industrielle doit répondre à une demande client sur ses pratiques RSE numériques.
2. **Cible** : sous-traitant aéronautique fictif autour de Toulouse.
3. **Outil** : questionnaire de maturité sur parc IT, données CAO/PLM, gouvernance et achats IT.
4. **Résultat** : score indicatif global et lecture par pilier.
5. **Preuves** : l’outil liste les preuves à consolider : inventaire IT, politique d’achat, DEEE, archivage, règles PLM.
6. **Livrable** : rapport PDF avec contexte, forces, faiblesses, recommandations, actions court terme et limites.
7. **Limites** : ce n’est pas un audit, pas une certification, pas une conformité officielle.
8. **Valeur portfolio** : le projet montre ma capacité à relier tech, produit, business et industrie.

---

## Parcours utilisateur recommandé

1. Ouvrir la page **Cas d’étude fictif**.
2. Charger le cas **AeroPart Occitanie** dans la session.
3. Lire le **Dashboard** pour comprendre score, priorités, preuves et actions.
4. Ouvrir la page **Score** pour sauvegarder le diagnostic.
5. Générer le **Rapport PDF**.
6. Lire la page **Méthodologie & limites** pour comprendre ce que le score mesure et ne mesure pas.

---

## Méthodologie de scoring

Le score repose sur quatre piliers indicatifs :

| Pilier | Poids | Rôle |
|---|---:|---|
| Carbone numérique | 35 % | Ordre de grandeur simplifié lié au parc matériel, serveurs, cloud, stockage et déplacements IT/AMOA |
| Gouvernance | 25 % | Capacité à nommer un responsable, suivre le parc, documenter les règles et centraliser les preuves |
| Données PLM / CAO | 20 % | Gestion du stockage actif, archives, rétention, nettoyage et règles de conservation |
| Achats IT responsables | 20 % | Cycle de vie matériel, réparation, reconditionné, centralisation et critères fournisseurs |

Le score mesure une **maturité indicative**. Il ne mesure pas l’empreinte carbone réelle de l’entreprise.

---

## Exemples de preuves RSE numériques

| Critère | Preuve attendue | Exemple concret | Limite |
|---|---|---|---|
| Inventaire du parc numérique | Liste datée des postes, écrans, serveurs, VM/cloud | Export GLPI, Excel de parc IT | Ne prouve pas l’empreinte carbone réelle |
| Gestion DEEE | Preuve de collecte, recyclage, effacement ou reprise | Bordereau DEEE, contrat prestataire | Doit être daté et rattaché au parc concerné |
| Achats IT responsables | Critère d’achat formalisé | Politique achats IT, facture reconditionné | Une intention ne suffit pas |
| Données CAO / PLM | Cartographie outils, volumes, règles d’archivage | Liste CATIA/PLM/PDM, volume par projet | Le volume ne dit rien sur la criticité |
| Conservation des données | Règle projets actifs, terminés, archives | Procédure qualité, note DSI | À aligner avec qualité, client et propriété intellectuelle |

---

## Rapport PDF

Le rapport PDF est la pièce maîtresse du projet. Il est conçu pour être compris sans ouvrir l’application.

Structure du rapport :

1. contexte du diagnostic ;
2. objectif du pré-diagnostic ;
3. score global indicatif ;
4. lecture par pilier ;
5. forces identifiées ;
6. faiblesses principales ;
7. preuves manquantes ou à consolider ;
8. recommandations prioritaires ;
9. actions court terme ;
10. répartition carbone indicative ;
11. limites méthodologiques ;
12. prochaines étapes possibles.

Le rapport répète explicitement qu’il s’agit d’un **document de travail indicatif**.

---

## Limites assumées

- données déclaratives non vérifiées ;
- pondérations construites pour un démonstrateur, pas validées par un organisme ;
- facteurs d’émission simplifiés ;
- périmètre carbone incomplet ;
- aucune preuve documentaire auditée ;
- aucun organisme officiel n’a validé la méthode ;
- pas de garantie de préparation EcoVadis, REEN, client ou réglementaire ;
- résultats utiles pour cadrer et discuter, pas pour certifier.

Ces limites ne sont pas cachées : elles font partie de la crédibilité du projet.

---

## Stack technique

- Python
- Streamlit
- pandas
- Plotly
- FPDF
- SQLite

---

## Lancer le projet

```bash
pip install -r requirements.txt
streamlit run app.py
```

L’application fonctionne en **mode démo local**. Aucun compte n’est nécessaire pour parcourir le diagnostic, charger le cas fictif et produire un rapport.

---

## Structure du repo

```text
.
├── app.py
├── README.md
├── requirements.txt
├── components/
│   ├── cards.py
│   ├── charts.py
│   └── sidebar.py
├── pages_app/
│   ├── home.py
│   ├── fit_test.py
│   ├── case_study.py
│   ├── diagnostic_wizard.py
│   ├── dashboard.py
│   ├── score.py
│   ├── report.py
│   └── methodology.py
├── services/
│   ├── calculations.py
│   ├── database.py
│   └── pdf_generator.py
├── styles/
│   └── css.py
└── data/
    └── __init__.py
```

---

## Améliorations possibles

Améliorations réalistes, sans transformer le projet en faux SaaS :

- tester le rapport avec 2 ou 3 profils : recruteur, manager produit, responsable qualité/RSE ;
- comparer les questions avec de vraies demandes fournisseurs publiques ou anonymisées ;
- affiner les pondérations avec retours terrain ;
- ajouter des captures d’écran propres au README ;
- ajouter un exemple de rapport PDF généré dans le repo ;
- simplifier encore le wording si la démo dépasse 3 minutes.

---

## Positionnement personnel EPITA → TBS

AeroGreen Diag raconte une transition :

> Je viens d’un parcours tech. Avant TBS, j’ai construit un prototype qui traduit un problème industriel et RSE complexe en outil numérique compréhensible, avec une logique de diagnostic, une structuration des preuves, un rapport final et des limites assumées.

Le projet sert donc de support de discussion pour un profil hybride : tech, produit, business, industrie et RSE.
