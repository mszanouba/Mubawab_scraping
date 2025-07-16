# 🏘️ Mubawab Scraping - Location

Ce projet a pour objectif de scraper les annonces de **location immobilière** depuis le site **[Mubawab](https://www.mubawab.ma/)**.  
Il extrait les informations essentielles sur les biens à louer (titre, prix, localisation, description, etc.), puis les structure dans un format exploitable (ex. : CSV ou DataFrame).

## 📁 Structure du projet

mubawab_scraping/
│
├── mubawab_scraper.py # Contient la logique principale de scraping
├── app.py # Point d'entrée (main) pour exécuter le scraper
├── sample_data.csv # Échantillon des données extraites (location uniquement)
└── README.md # Ce fichier

## 🚀 Lancement rapide

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
