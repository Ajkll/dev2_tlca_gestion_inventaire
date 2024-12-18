import sys
from module_perso.csv_manager import Commerce, CSVError
from module_perso.parser import secluded_parser


def execute_command(command, commerce):
    """Exécute une commande en fonction de l'entrée de l'utilisateur."""
    try:
        if command.startswith("consolidate"):
            # Extraction des arguments pour la commande 'consolidate'
            args = command.split()
            if "--files" not in args:
                return "Erreur : Il faut spécifier --files avec des fichiers."
            files_index = args.index("--files") + 1
            output_index = args.index("--output") + 1 if "--output" in args else None
            files = args[files_index:]
            output = args[output_index] if output_index else "consolidated.csv"
            commerce.consolidate_files(files, output)
            return f"Fichiers consolidés dans : {output}"

        elif command.startswith("search"):
            # Extraction des arguments pour la commande 'search'
            args = command.split()
            file_index = args.index("--file") + 1
            query_index = args.index("--query") + 1
            file = args[file_index]
            query = args[query_index]
            category_index = args.index("--category") + 1 if "--category" in args else None
            price_range_index = args.index("--price-range") + 1 if "--price-range" in args else None
            category = args[category_index] if category_index else None
            price_range = args[price_range_index] if price_range_index else None
            results = commerce.search_data(file, query, category, price_range)
            return results

        elif command.startswith("report"):
            # Extraction des arguments pour la commande 'report'
            args = command.split()
            file_index = args.index("--file") + 1
            output_index = args.index("--output") + 1 if "--output" in args else None
            summary_index = args.index("--summary") + 1 if "--summary" in args else None
            file = args[file_index]
            output = args[output_index] if output_index else "report.txt"
            summary = True if summary_index else False
            commerce.generate_report(file, output, summary)
            return f"Rapport généré dans : {output}"

        elif command == "exit":
            return "Au revoir !"

        else:
            return "Commande inconnue. Tapez 'help' pour obtenir de l'aide."
    except CSVError as e:
        return f"Erreur : {e}"
    except Exception as e:
        return f"Erreur imprévue : {e}"


def interactive_shell():
    """Shell interactif qui permet à l'utilisateur de saisir des commandes en continu."""
    print("Bienvenue dans le shell interactif. Tapez 'exit' pour quitter ou 'help' pour obtenir de l'aide.")
    commerce = Commerce()

    while True:
        try:
            command = input(">>> ").strip()

            if command.lower() == "exit":
                print("Au revoir !")
                break
            elif command.lower() == "help":
                print("Commandes disponibles :")
                print("  consolidate --files <fichiers> --output <sortie>  : Consolider des fichiers CSV")
                print(
                    "  search --file <fichier> --query <requête> [--category <catégorie>] [--price-range <plage>] : Rechercher dans un CSV")
                print("  report --file <fichier> --output <rapport> [--summary] : Générer un rapport")
                print("  exit : Quitter le shell")
            else:
                result = execute_command(command, commerce)
                print(result)

        except KeyboardInterrupt:
            print("\nAu revoir !")
            break
        except Exception as e:
            print(f"Erreur dans le shell : {e}")


def main():
    """Point d'entrée principal du script."""
    parser = secluded_parser()
    args = parser.parse_args()

    if not args.command:
        # Si aucune commande n'est fournie, lance le shell interactif
        interactive_shell()
        sys.exit(0)

    commerce = Commerce()

    try:
        if args.command == "consolidate":
            commerce.consolidate_files(args.files, args.output)
        elif args.command == "search":
            commerce.search_data(args.file, args.query, args.category, args.price_range)
        elif args.command == "report":
            commerce.generate_report(args.file, args.output, args.summary)
    except CSVError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erreur imprévue : {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
