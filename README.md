# AeroGreen Diag

AeroGreen Diag est un prototype personnel / portfolio stratégique développé avant mon entrée à TBS en L3, après un parcours prépa EPITA.

Le projet explore un sujet B2B précis : comment une PME industrielle, notamment un sous-traitant aéronautique autour de Toulouse, pourrait organiser une première lecture de maturité numérique responsable et structurer des preuves RSE avant un échange client, un questionnaire fournisseur ou une préparation de type EcoVadis / REEN.

> AeroGreen Diag est un démonstrateur pédagogique. Il ne s’agit pas d’une startup SaaS prête à vendre, d’une certification, d’un audit carbone réglementaire, d’une notation EcoVadis ou d’un outil remplaçant un consultant RSE.

---

## Positionnement du projet

AeroGreen Diag doit être compris comme un projet portfolio, pas comme une offre commerciale finalisée.

L’objectif est de démontrer une capacité à :

- identifier un problème B2B concret ;
- comprendre une cible industrielle locale ;
- transformer un sujet métier complexe en parcours utilisateur ;
- prototyper rapidement avec Streamlit ;
- construire une logique de scoring et de rapport ;
- expliciter les limites méthodologiques ;
- relier tech, business, RSE, industrie et UX.

Le projet assume donc un positionnement clair : **pré-diagnostic indicatif, pédagogique et non officiel**.

---

## Problème exploré

Les PME industrielles sont de plus en plus sollicitées sur les sujets RSE, environnement, numérique responsable, achats responsables et traçabilité documentaire.

Dans une chaîne de sous-traitance aéronautique, une entreprise peut devoir répondre à des demandes client ou fournisseur sur :

- ses politiques internes ;
- ses preuves documentaires ;
- son parc numérique ;
- ses données CAO / PLM ;
- ses pratiques d’achats IT ;
- ses déchets numériques ;
- sa capacité à structurer une réponse cohérente.

Le problème n’est pas seulement de “faire de la RSE”. Le problème est aussi de savoir **quoi collecter, comment l’organiser, comment prioriser les zones faibles et comment préparer une discussion crédible**.

---

## Pourquoi les PME industrielles / aéronautiques ?

Le choix de la cible est volontaire.

Les sous-traitants industriels et aéronautiques autour de Toulouse combinent plusieurs enjeux intéressants pour un prototype :

- pression potentielle des grands donneurs d’ordre ;
- usage important d’outils numériques techniques : CAO, PLM, stockage, postes de travail puissants ;
- besoin de structurer des preuves dans un langage compréhensible par des clients ou partenaires ;
- maturité RSE parfois hétérogène selon la taille et les ressources internes ;
- contexte local cohérent avec l’écosystème industriel toulousain.

Cette cible permet de construire un cas d’étude plus solide qu’un outil générique “RSE pour toutes les entreprises”.

---

## Ce que fait vraiment l’outil

AeroGreen Diag :

- collecte des réponses déclaratives ;
- produit un score indicatif de maturité numérique responsable ;
- estime un ordre de grandeur carbone simplifié lié au numérique ;
- identifie des zones faibles par pilier ;
- propose des recommandations non officielles ;
- génère un rapport exploratoire de travail ;
- permet de consulter un cas d’étude fictif pour comprendre le parcours ;
- sert de base de réflexion avant une discussion client, fournisseur ou pédagogique.

Le livrable généré doit être lu comme un **document de travail**, pas comme une preuve certifiée.

---

## Ce que démontre le prototype

Le prototype démontre principalement une démarche produit et business :

- cadrage d’un problème métier ;
- segmentation d’une cible B2B ;
- design d’un parcours utilisateur ;
- construction d’un dashboard ;
- persistance locale avec SQLite ;
- génération de rapports PDF ;
- scoring multicritère ;
- UX writing sobre et prudent ;
- capacité à transformer un sujet complexe en interface utilisable.

La valeur du projet n’est pas de dire “j’ai créé un outil RSE officiel”. La valeur est de montrer : **voici ce que j’ai construit, pourquoi je l’ai construit, ce que ça démontre, et ce que ça ne démontre pas**.

---

## Ce que le prototype ne prétend pas faire

AeroGreen Diag ne prétend pas :

- certifier une entreprise ;
- produire un audit carbone officiel ;
- calculer un bilan GES réglementaire ;
- attribuer une notation EcoVadis ;
- garantir une conformité REEN ;
- remplacer un consultant RSE ;
- remplacer une analyse terrain ;
- valider des preuves documentaires ;
- fournir une décision contractuelle ou réglementaire.

Cette limite est volontaire. Elle évite de survendre le projet et renforce sa crédibilité comme démonstrateur portfolio.

---

## Méthodologie simplifiée

Le score indicatif repose sur quatre piliers :

| Pilier | Poids indicatif | Rôle |
|---|---:|---|
| Carbone numérique | 35 % | Ordre de grandeur simplifié sur matériel, serveurs, cloud, stockage et déplacements IT |
| Gouvernance | 25 % | Référent, inventaire, suivi, politiques internes, structuration des preuves |
| Données PLM / CAO | 20 % | Archivage, rétention, stockage actif/froid, nettoyage des données techniques |
| Achats IT | 20 % | Durée de vie matériel, réparation, reconditionné, centralisation, critères fournisseurs |

Les recommandations sont déclenchées lorsque certains piliers passent sous des seuils de maturité. Elles servent à prioriser une réflexion, pas à prescrire une action officielle.

---

## Limites assumées

Les limites sont explicites :

- les données sont déclaratives ;
- les pondérations sont indicatives ;
- les facteurs d’émission sont simplifiés ;
- le périmètre carbone est incomplet ;
- les preuves ne sont pas vérifiées ;
- aucun organisme officiel n’a validé la méthode ;
- le diagnostic ne remplace pas une analyse terrain ;
- les résultats ne doivent pas être utilisés comme preuve réglementaire.

Le projet est crédible précisément parce qu’il annonce ces limites au lieu de les cacher.

---

## Valeur portfolio EPITA → TBS

AeroGreen Diag sert à montrer une trajectoire hybride :

- **EPITA / tech** : développement Python, Streamlit, logique de données, structure applicative, PDF, SQLite ;
- **Produit** : parcours utilisateur, dashboard, cas d’étude, UX writing, priorisation ;
- **Business** : cible B2B, problème industriel, proposition de valeur prudente ;
- **RSE / industrie** : compréhension des enjeux de preuves, maturité, numérique responsable et sous-traitance ;
- **TBS** : capacité à relier analyse stratégique, produit numérique et contexte marché.

Le projet devient donc un support de discussion sérieux pour expliquer un profil tech qui se dirige vers le business.

---

## Prochaines validations terrain

Pour aller plus loin, les prochaines étapes réalistes seraient :

1. interroger 3 à 5 PME industrielles ou sous-traitants autour de Toulouse ;
2. vérifier quelles questions RSE reviennent réellement dans les échanges client / fournisseur ;
3. comparer le questionnaire avec des documents publics EcoVadis, REEN et numérique responsable ;
4. tester si le rapport est compréhensible par un dirigeant de PME ou un responsable qualité / RSE ;
5. ajuster les pondérations avec des retours terrain ;
6. clarifier les preuves réellement utiles à collecter ;
7. décider si le projet reste portfolio ou devient un outil d’aide interne plus sérieux.

---

## Fonctionnalités

- page d’accueil avec positionnement clair ;
- test rapide d’adéquation ;
- pré-diagnostic guidé multi-étapes ;
- score indicatif de maturité numérique responsable ;
- dashboard de suivi ;
- cas d’étude fictif ;
- page méthodologie & limites ;
- rapport exploratoire PDF ;
- dossier RSE numérique de travail ;
- authentification locale ;
- persistance SQLite.

---

## Stack

Python, Streamlit, pandas, Plotly, FPDF, SQLite.

---

## Lancement local

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## Connexion rapide optionnelle

Le fichier `config/auth_config.py` permet d’autoriser certains emails à utiliser un accès rapide sans mot de passe dans un contexte de démonstration locale.

```python
PASSWORDLESS_EMAILS = {"votre-email@exemple.com"}
```

Il est aussi possible d’utiliser la variable d’environnement `AEROGREEN_PASSWORDLESS_EMAILS`.
