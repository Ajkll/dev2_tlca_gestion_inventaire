import argparse
from module_perso.csv_manager import CSVManager


def secluded_parser():
    """Crée et retourne un parser argparse pour gérer les sous-commandes et options."""

    parser = argparse.ArgumentParser(
        description="Un outil pour consolider, rechercher et générer des rapports à partir de fichiers CSV.",
        epilog=f"Répertoires par défaut :\n"
        f"  - Entrée : {CSVManager.INPUT_DIR}\n"
        f"  - Sortie : {CSVManager.OUTPUT_DIR}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Sous-commandes disponibles")

    # Commande "consolidate"
    consolidate_parser = subparsers.add_parser(
        "consolidate", help="Consolider plusieurs fichiers CSV en un seul fichier"
    )
    consolidate_parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Liste des noms de fichiers CSV dans le répertoire 'input'",
    )
    consolidate_parser.add_argument(
        "--output",
        default="consolidated.csv",
        help="Nom du fichier CSV consolidé dans le répertoire 'output'",
    )

    # Commande "search"
    search_parser = subparsers.add_parser(
        "search", help="Rechercher des informations dans un fichier CSV"
    )
    search_parser.add_argument(
        "--file", required=True, help="Nom du fichier CSV dans le répertoire 'input'"
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
        "report", help="Générer un rapport récapitulatif à partir d'un fichier CSV"
    )
    report_parser.add_argument(
        "--file", required=True, help="Nom du fichier CSV dans le répertoire 'input'"
    )
    report_parser.add_argument(
        "--output", default="report.txt", help="Nom du fichier texte dans le répertoire 'output'"
    )
    report_parser.add_argument(
        "--summary", action="store_true", help="Inclure un résumé dans le rapport"
    )

    return parser
