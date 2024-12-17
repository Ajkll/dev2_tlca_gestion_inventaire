# Gestionnaire d'Inventaire en CLI

Ce projet vise à automatiser la gestion de stocks pour une entreprise à partir de fichiers CSV. Il permet de fusionner plusieurs fichiers en un seul, de rechercher rapidement des produits selon différents critères et de générer des rapports récapitulatifs. L'objectif était de proposer un outil simple, fonctionnel et facilement utilisable directement depuis un terminal.

## Fonctionnalités principales

- **Fusion de plusieurs fichiers CSV** en un fichier consolidé, avec une gestion robuste des erreurs.
- **Recherche d'informations** dans les fichiers selon des critères (catégorie, prix ou mot-clé).
- **Génération de rapports exportables** contenant des statistiques sur les stocks.

## Technologies Utilisées

- **Python 3** pour le développement.
- **Click** pour la gestion des commandes CLI.
- **Pytest** pour les tests unitaires.
- **Flake8** pour le linting.
- **GitHub Actions** pour l'intégration continue (CI/CD).

## Commandes Principales

### 1. Fusionner des fichiers CSV

```bash
python main.py consolidate --input dir_csv --output result/consolidated.csv
```

Fusionne tous les fichiers CSV d'un répertoire donné en un fichier consolidé.

### 2. Rechercher des informations

```bash
python main.py search --query "catégorie=Vêtements prix<50"
```

Recherche les produits selon des filtres spécifiques comme la catégorie, le prix ou d'autres critères.

### 3. Générer un rapport récapitulatif

```bash
python main.py report --input consolidated.csv --output reports/summary.txt
```

Crée un rapport avec des statistiques globales sur les stocks à partir d'un fichier CSV consolidé.

## Installation

1. **Cloner le projet**
   ```bash
   git clone https://github.com/Ajkll/dev2_tlca_gestion_inventaire.git
   ```
2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

## Tests et Qualité de Code

- **Tests unitaires** : réalisés avec Pytest pour garantir le bon fonctionnement des fonctionnalités.
- **Linting automatique** : assuré par Flake8.
- **Pipeline CI/CD** : configuré via GitHub Actions pour une intégration continue.

## Expérience et Apprentissage

Ce projet m'a permis de développer des compétences en manipulation de fichiers CSV, automatisation d'outils CLI et mise en place de workflows d'assurance qualité.

Le projet a été réalisé avec l'aide de ChatGPT (comme autorisé dans les consignes), tout en assurant une supervision personnelle pour le rendu final.

## tree (simplifier) du project

(venv) koko@koko:~/dev2_tlca$ tree -a -I ".pytest_cache|venv|.git"
.
├── .coverage
├── env.sh
├── .flake8
├── .github
│ └── workflows
│ └── test.yml
├── .gitignore
├── pytest.ini
├── README.md
├── requirements.txt
├── src
│ ├── .coverage
│ ├── main.py
│ └─── module_perso
│ ├── csv_manager.py
│ ├── **init**.py
│ ├── input
│ │ ├── products1.csv
│ │ ├── products2.csv
│ │ └── products3.csv
│ ├── output
│ │ ├── report
│ │ │ ├── rapport_test.txt
│ │ │ └── report_test.txt
│ │ └── resultat.csv
│ └─── parser.py
└── tests
├── test_csv_manager.py
├── test_cvs_manager_commerce.py
├── test_main.py
└── test_parser.py

13 directories, 44 files
(venv) koko@koko:~/dev2_tlca$

## Remerciements

Merci d'avoir consulté ce projet !

Le code source est disponible sur GitHub : [Lien du Projet](https://github.com/Ajkll/dev2_tlca_gestion_inventaire)

---

**Auteur :** Ajkll et chatgpt
