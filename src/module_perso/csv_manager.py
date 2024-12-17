import csv
import os


class CSVError(Exception):
    """Exception de base pour les erreurs liées aux opérations CSV."""
    pass


class FileNotFoundError(CSVError):
    """Exception levée lorsqu'un fichier est introuvable."""
    pass


class DataProcessingError(CSVError):
    """Exception levée lorsqu'une erreur survient lors du traitement des données."""
    pass


class CSVManager:
    """Classe utilitaire pour gérer les opérations sur les fichiers CSV."""

    INPUT_DIR = os.path.join(os.path.dirname(__file__), "input")
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

    def __init__(self, file_name, is_output=False):
        """
        Initialise la classe en utilisant les répertoires par défaut.
        - Priorise `output` pour les fichiers consolidés ou générés.
        - Recherche aussi dans `input` si le fichier est introuvable dans `output`.
        """
        self.file_path = None

        if is_output:
            self.file_path = os.path.join(self.OUTPUT_DIR, file_name)
        else:
            # Priorité à output pour la recherche
            potential_paths = [
                os.path.join(self.OUTPUT_DIR, file_name),
                os.path.join(self.INPUT_DIR, file_name),
            ]
            for path in potential_paths:
                if os.path.exists(path):
                    self.file_path = path
                    break

        if not self.file_path:
            raise FileNotFoundError(
                f"Le fichier '{file_name}' est introuvable dans les répertoires 'input' ou 'output'.")

    def read_csv(self):
        """Lit un fichier CSV et retourne une liste de dictionnaires."""
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                data = [row for row in reader]
                if not data:  # Vérifie si le fichier est vide ou mal formé
                    raise csv.Error("Le fichier CSV est vide ou invalide.")
                return data
        except (csv.Error, KeyError) as e:
            raise DataProcessingError(f"Erreur lors de la lecture du fichier CSV : {e}")
        except Exception as e:
            raise DataProcessingError(f"Erreur inconnue : {e}")

    @staticmethod
    def write_csv(file_name, data, fieldnames, output_dir=None):
        """Écrit une liste de dictionnaires dans un fichier CSV."""
        output_dir = output_dir or CSVManager.OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)  # Crée le répertoire s'il n'existe pas
        output_path = os.path.join(output_dir, file_name)
        try:
            # Vérifie si les colonnes sont valides
            for row in data:
                missing_columns = [col for col in fieldnames if col not in row]
                if missing_columns:
                    raise ValueError(f"Colonnes manquantes : {missing_columns}")

            with open(output_path, mode='w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except (ValueError, KeyError) as e:
            raise DataProcessingError(f"Erreur lors de l'écriture du fichier CSV : {e}")
        except Exception as e:
            raise DataProcessingError(f"Erreur inconnue : {e}")


class Commerce:
    """Classe principale pour gérer les opérations commerciales."""

    def __init__(self):
        self.data = []

    def consolidate_files(self, file_paths, output_file):
        """Consolide plusieurs fichiers CSV en un seul fichier."""
        consolidated_data = []
        for file_path in file_paths:
            manager = CSVManager(file_path)
            file_data = manager.read_csv()
            consolidated_data.extend(file_data)

        if not consolidated_data:
            raise DataProcessingError("Aucune donnée n'a été consolidée.")

        # Écrire le fichier consolidé
        fieldnames = consolidated_data[0].keys() if consolidated_data else []
        CSVManager.write_csv(output_file, consolidated_data, fieldnames)
        print(f"Les fichiers {file_paths} ont été consolidés dans {output_file}.")

    def search_data(self, file_path, query, category=None, price_range=None):
        """Recherche les données dans un fichier CSV."""
        manager = CSVManager(file_path)
        data = manager.read_csv()

        # Filtrer les données
        results = [row for row in data if query.lower() in row['name'].lower()]
        if category:
            results = [row for row in results if row['category'].lower() == category.lower()]
        if price_range:
            min_price, max_price = map(float, price_range.split(','))
            results = [
                row for row in results
                if min_price <= float(row['price']) <= max_price
            ]

        if not results:
            print("Aucun résultat trouvé.")
        else:
            for result in results:
                print(result)

    def generate_report(self, file_path, output_file, summary=False):
        """Génère un rapport récapitulatif dans le répertoire 'report'."""
        # Vérifier ou créer le répertoire 'report'
        report_dir = os.path.join(CSVManager.OUTPUT_DIR, "report")
        os.makedirs(report_dir, exist_ok=True)

        # Chemin complet pour le fichier de rapport
        report_path = os.path.join(report_dir, output_file)

        # Lire les données depuis le fichier CSV
        manager = CSVManager(file_path)
        data = manager.read_csv()

        # Calculer les statistiques
        total_products = len(data)
        total_quantity = sum(int(row['quantity']) for row in data)
        total_value = sum(float(row['price']) * int(row['quantity']) for row in data)

        # Écrire les données dans le fichier de rapport
        try:
            with open(report_path, 'w', encoding='utf-8') as file:
                file.write(f"Rapport pour {file_path}\n")
                file.write(f"Nombre de produits : {total_products}\n")
                file.write(f"Quantité totale : {total_quantity}\n")
                file.write(f"Valeur totale : {total_value:.2f}€\n")
                if summary:
                    file.write("\nDétail des produits :\n")
                    for row in data:
                        file.write(
                            f"- {row['name']} (Catégorie : {row['category']}, Prix : {row['price']}€, "
                            f"Quantité : {row['quantity']})\n"
                        )

            print(f"Rapport généré avec succès dans : {report_path}")
        except Exception as e:
            raise DataProcessingError(f"Erreur lors de la génération du rapport : {e}")
