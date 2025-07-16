# 🏘️ Mubawab Scraping - Location

Ce projet a pour objectif de scraper les annonces de **location immobilière** depuis le site [Mubawab](https://www.mubawab.ma/).  
Il extrait les informations essentielles sur les biens à louer (titre, prix, localisation, description, etc.), puis les structure dans un format exploitable (CSV).

---

## 📁 Structure du projet

```
mubawab_scraping/
│
├── mubawab_scraper.py     # Contient la logique principale de scraping
├── app.py                 # Point d'entrée (main) pour exécuter le scraper
├── sample_data.csv        # Échantillon des données extraites (location uniquement)
├── requirements.txt       # Liste des dépendances nécessaires
└── README.md              # Ce fichier
```

---

## 🚀 Lancement rapide

### ✅ Prérequis

- Python 3.7+
- Les bibliothèques suivantes :
  - `requests`
  - `beautifulsoup4`
  - `pandas`
  - `urllib3`

### ⚙️ Installation des dépendances

Assurez-vous d’être dans l’environnement virtuel, puis installez les dépendances :

```bash
pip install -r requirements.txt
```

---

### ▶️ Exécution

Lancez le scraper avec la commande suivante :

```bash
python app.py
```



## 📌 Remarques

- Ce projet se concentre uniquement sur les annonces **de location** et dépend du format actuel du site Mubawab.
- Le site peut bloquer l'accès en cas de scraping trop fréquent. Il est conseillé d’ajouter des délais (`time.sleep`) entre les requêtes pour éviter d’être banni.
- Ce projet est à but **éducatif uniquement**.

---
