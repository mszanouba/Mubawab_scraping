# 🏘️ Mubawab Scraping - Location

Ce projet a pour objectif de scraper les annonces de **location immobilière** depuis le site **[Mubawab](https://www.mubawab.ma/)**.  
Il extrait les informations essentielles sur les biens à louer (titre, prix, localisation, description, etc.), puis les structure dans un format exploitable (CSV).

## 📁 Structure du projet

mubawab_scraping/
│
├── mubawab_scraper.py # Contient la logique principale de scraping
├── app.py # Point d'entrée (main) pour exécuter le scraper
├── sample_data.csv # Échantillon des données extraites (location uniquement)
└── README.md # Ce fichier

### 🚀 Lancement rapide

### ✅ Prérequis

- Python 3.7+
- Les bibliothèques suivantes :
  - `requests`
  - `beautifulsoup4`
  - `pandas`
  - `urllib`

### ⚙️ Installation des dépendances

```bash
pip install -r requirements.txt

###  ▶️ Exécution
Lance le scraper avec la commande suivante :

```bash
python app.py

### 🧪 Exemple de données
Un extrait des données collectées se trouve dans le fichier sample_data.csv.
Il contient des colonnes comme :

Titre

Prix

Localisation

Description

Superficie

Nombre de pièces

Lien de l’annonce

### 📌 Remarques
    -Ce projet se concentre uniquement sur les annonces de location, il se concentre sur le format actuel du site.

    -Le site Mubawab peut limiter ou bloquer l’accès en cas de scraping intensif. Utilise des délais (time.sleep) pour limiter la fréquence des requêtes.

    -Pour usage éducatif uniquement.
