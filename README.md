# Bibliothèque Intelligente

Ce projet est une application Django de gestion de bibliothèque avec une interface moderne, une authentification utilisateur et un chatbot IA.

## Fonctionnalités principales

- Authentification par utilisateur (connexion, inscription, profil)
- Dashboard avec statistiques principales (livres, disponibilité, emprunts, réservations)
- Gestion des livres (ajout, modification, suppression, détail)
- Gestion des emprunts (création, retour de livre)
- Gestion des catégories de livres
- Export CSV des livres
- Chatbot IA intégré pour poser des questions au système

## Pages principales

- `/` : Dashboard principal et catalogue des livres
- `/emprunts/` : Liste et gestion des emprunts
- `/categories/` : Ajout et consultation des catégories
- `/chatbot/` : Interface du chatbot IA
- `/accounts/login/` : Page de connexion
- `/accounts/signup/` : Page d'inscription
- `/accounts/profile/` : Gestion du profil utilisateur

## Base de données

La base utilise SQLite (`db.sqlite3`) et contient les principales tables suivantes :

- `library_categorie`
  - `id` : identifiant
  - `nom` : nom de la catégorie

- `library_livre`
  - `id` : identifiant
  - `titre` : titre du livre
  - `auteur` : nom de l'auteur
  - `categorie_id` : référence à `library_categorie`
  - `annee_publication` : année de publication
  - `quantite_disponible` : quantité disponible
  - `statut` : état du livre (`disponible`, `emprunte`, `reserve`)

- `library_emprunt`
  - `id` : identifiant
  - `livre_id` : référence à `library_livre`
  - `nom_emprunteur` : nom de l'emprunteur
  - `date_emprunt` : date d'emprunt
  - `date_retour` : date de retour prévue
  - `retourne` : booléen indiquant si le livre est retourné

- `auth_user`
  - table Django d'authentification utilisateur
  - gère les comptes, mots de passe, email, prénom, nom

## Installation et exécution

1. Créez un environnement virtuel :

   ```bash
   python -m venv venv
   source venv/Scripts/activate   # Windows
   pip install -r requirements.txt
   ```

2. Appliquez les migrations :

   ```bash
   python manage.py migrate
   ```

3. Créez un superutilisateur si nécessaire :

   ```bash
   python manage.py createsuperuser
   ```

4. Lancez le serveur local :

   ```bash
   python manage.py runserver
   ```

5. Ouvrez le site à l'adresse :
   ```
   http://127.0.0.1:8000/
   ```

## Notes

- L'utilisateur doit se connecter pour accéder aux pages principales.
- Le site est pensé comme un tableau de bord de gestion rapide pour la bibliothèque.
- Le chatbot IA est intégré pour enrichir l'expérience et répondre aux questions liées à la bibliothèque.
