import os
import pytest
import csv
from module_perso.csv_manager import CSVManager, CSV_FileNotFoundError, DataProcessingError


@pytest.fixture
def setup_directories(tmp_path):
    """Crée des répertoires temporaires pour 'input' et 'output'."""
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    return input_dir, output_dir


@pytest.fixture
def sample_csv_file(setup_directories):
    """Crée un fichier CSV d'exemple dans le répertoire 'input'."""
    input_dir, _ = setup_directories
    file_path = input_dir / "sample.csv"
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "category", "price", "quantity"])
        writer.writeheader()
        writer.writerows([
            {"name": "Product A", "category": "Category 1", "price": "10.5", "quantity": "5"},
            {"name": "Product B", "category": "Category 2", "price": "20.0", "quantity": "3"}
        ])
    return file_path


def test_file_not_found_error(setup_directories):
    """Teste si une exception est levée lorsque le fichier est introuvable."""
    _, output_dir = setup_directories
    with pytest.raises(CSV_FileNotFoundError):
        CSVManager("nonexistent.csv", is_output=False)


def test_read_csv(sample_csv_file):
    """Teste la lecture d'un fichier CSV."""
    manager = CSVManager(str(sample_csv_file))
    data = manager.read_csv()
    assert len(data) == 2
    assert data[0]["name"] == "Product A"
    assert data[1]["price"] == "20.0"


def test_read_csv_invalid_file(setup_directories):
    """Teste la levée d'une exception pour un fichier corrompu."""
    input_dir, _ = setup_directories
    invalid_file = input_dir / "corrupted.csv"
    invalid_file.write_text("Not a valid CSV content")
    with pytest.raises(DataProcessingError):
        manager = CSVManager(str(invalid_file))
        manager.read_csv()


def test_write_csv(setup_directories):
    """Teste l'écriture dans un fichier CSV."""
    _, output_dir = setup_directories  # output_dir est un répertoire temporaire isolé
    file_name = "output.csv"
    data = [
        {"name": "Product A", "category": "Category 1", "price": "10.5", "quantity": "5"},
        {"name": "Product B", "category": "Category 2", "price": "20.0", "quantity": "3"}
    ]
    fieldnames = ["name", "category", "price", "quantity"]

    # Passer le bon répertoire de sortie
    CSVManager.write_csv(file_name, data, fieldnames, output_dir=output_dir)

    # Vérifier que le fichier a bien été créé
    output_file_path = output_dir / file_name
    assert output_file_path.exists(), f"Le fichier {output_file_path} n'a pas été créé."

    # Vérifier le contenu du fichier
    with open(output_file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        written_data = list(reader)
        assert written_data == data, "Les données écrites dans le fichier ne correspondent pas aux données attendues."


def test_write_csv_invalid_data(setup_directories):
    """Teste la levée d'une exception pour des données malformées."""
    _, output_dir = setup_directories
    file_name = "invalid_output.csv"
    invalid_data = [{"name": "Incomplete"}]  # Manque des colonnes nécessaires
    fieldnames = ["name", "category", "price", "quantity"]

    with pytest.raises(DataProcessingError):
        CSVManager.write_csv(file_name, invalid_data, fieldnames)


def test_csvmanager_output_dir():
    """Teste que le chemin du fichier pointe bien vers le répertoire OUTPUT_DIR si is_output=True."""
    file_name = "output_file.csv"

    # Créer une instance de CSVManager avec is_output=True
    manager = CSVManager(file_name, is_output=True)

    # Construire le chemin attendu
    expected_path = os.path.join(CSVManager.OUTPUT_DIR, file_name)

    # Vérifier que le chemin est correct
    assert manager.file_path == expected_path, f"Le chemin attendu est {expected_path}, mais obtenu {manager.file_path}"
