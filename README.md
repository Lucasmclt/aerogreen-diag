# AeroGreen V4 — Secure Local SaaS Demo

## Lancement

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Nouveautés V4

- Authentification locale avec email / mot de passe
- Mots de passe hashés avec PBKDF2-HMAC-SHA256 + sel unique
- Base SQLite locale dans `data/aerogreen.db`
- Requêtes SQL paramétrées
- Historique des audits persistant par utilisateur
- Dashboard exécutif alimenté par la base
- Suppression d’audits depuis le dashboard
- Interface en vouvoiement

## Important sécurité

Cette version est fiable pour une démonstration locale ou un MVP étudiant.
Pour une production réelle, ajoutez impérativement :
- HTTPS
- gestion avancée des sessions
- politique de mot de passe plus stricte
- sauvegardes chiffrées
- chiffrement au repos si données sensibles
- logs d’audit
- déploiement derrière un serveur sécurisé


## V6
- Landing client ultra premium
- Sidebar simplifiée
- Cartes avec icônes
- Timeline visuelle
- Hero animé avec éléments flottants
- Transition plus claire entre mode gratuit et professionnel


## V7
- Boutons d’accueil plus légers
- Cartes d’une même ligne harmonisées en hauteur
- Sidebar nettoyée pour retirer l’espace avant les libellés


## V8
- Navigation sidebar corrigée avec boutons réels
- Suppression des textes non orientés client dans l’interface
- Boutons et cartes harmonisés


## V10
- Topbar nettoyée
- Suppression du bug d’affichage du </div>
- Boutons de navigation mieux stylés
- Boutons du hero fonctionnels et cohérents


## V11
- Navigation intégrée dans la topbar
- Boutons du hero intégrés dans la bulle visuelle
- Navigation par query params
- Boutons lisibles et cohérents


## V12
- Correction du bug d’affichage HTML dans la topbar
- Navigation topbar rendue proprement via HTML dédenté


## V13
- Topbar réécrite en composants Streamlit natifs
- Suppression du risque d’affichage des balises HTML en texte brut


## V14
- Correction de lisibilité du bouton actif dans la topbar
- Forçage de la couleur du texte blanc sur le bouton primaire


## V15
- Refonte totale de la topbar
- Carte d’identité plus premium
- Navigation plus lisible et cohérente
- Bouton actif clair et lisible


## V16
- Retour à une barre latérale gauche
- Suppression de la topbar haute
- Navigation entièrement déplacée dans la sidebar
- Carte de statut et dossier actif dans la sidebar


## V17
- Refonte Stripe-like de la page de connexion
- Mise en page en deux colonnes
- Indicateur visuel de robustesse du mot de passe
- Couleur dynamique selon la complexité


## V18
- Correction du rectangle vide sur la page de connexion
- Suppression du wrapper visuel vide à droite
- Ajout d’un petit bloc d’introduction plus propre au-dessus du formulaire


## V19
- Suppression du kicker au-dessus du titre de connexion
- Suppression de la barre rouge/slider sous les tabs
- Renforcement du feedback visuel en direct sur le mot de passe
