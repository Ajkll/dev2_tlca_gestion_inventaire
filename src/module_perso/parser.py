import argparse

def secluded_parser():
    """Crée et retourne un parser argparse pour gérer les sous-commandes et options."""

    # Initialisation du parser principal
    parser = argparse.ArgumentParser(
        description="Un outil pour consolider, rechercher et générer des rapports à partir de fichiers CSV.",
        epilog="Exemple d'utilisation : python script.py consolidate --files stock1.csv stock2.csv --output consolidated.csv",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Sous-parsers pour gérer les sous-commandes
    subparsers = parser.add_subparsers(dest="command", help="Sous-commandes disponibles")

    # Commande "consolidate"
    consolidate_parser = subparsers.add_parser(
        "consolidate",
        help="Consolider plusieurs fichiers CSV en un seul fichier",
    )
    consolidate_parser.add_argument(
        "--files", nargs="+", required=True, help="Liste des fichiers CSV à consolider"
    )
    consolidate_parser.add_argument(
        "--output", default="consolidated.csv", help="Nom du fichier CSV consolidé"
    )

    # Commande "search"
    search_parser = subparsers.add_parser(
        "search",
        help="Rechercher des informations dans un fichier CSV",
    )
    search_parser.add_argument(
        "--file", default="data.csv", help="Fichier CSV à analyser pour la recherche"
    )
    search_parser.add_argument(
        "--query", required=True, help="Critère de recherche (nom du produit, catégorie, etc.)"
    )
    search_parser.add_argument(
        "--category", help="Filtrer les résultats par catégorie spécifique"
    )
    search_parser.add_argument(
        "--price-range", type=str, help="Filtrer par une plage de prix (format : min,max)"
    )

    # Commande "report"
    report_parser = subparsers.add_parser(
        "report",
        help="Générer un rapport récapitulatif à partir d'un fichier CSV",
    )
    report_parser.add_argument(
        "--file", default="data.csv", help="Fichier CSV source pour le rapport"
    )
    report_parser.add_argument(
        "--output", default="report.txt", help="Nom du fichier texte pour le rapport"
    )
    report_parser.add_argument(
        "--summary", action="store_true", help="Inclure un résumé dans le rapport"
    )

    return parser
