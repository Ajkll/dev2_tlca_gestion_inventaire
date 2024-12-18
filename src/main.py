from module_perso.parser import secluded_parser
from module_perso.csv_manager import Commerce , CSVError
import sys
from module_perso.logging_config import configure_logging
import logging


def main():
    """Point d'entrée principal du script."""
    configure_logging()
    parser = secluded_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)
    logging.info("Application démarrée")
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
    configure_logging()
    main()
