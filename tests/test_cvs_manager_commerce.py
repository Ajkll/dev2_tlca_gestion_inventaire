import pytest
import os
import csv
from module_perso.csv_manager import Commerce, CSVManager


@pytest.fixture
def setup_directories(tmp_path):
    """Crée des répertoires temporaires pour 'input' et 'output'."""
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()
    return input_dir, output_dir


@pytest.fixture
def sample_csv_files(setup_directories):
    """Crée plusieurs fichiers CSV d'exemple pour les tests."""
    input_dir, _ = setup_directories
    file_paths = []

    # Créer deux fichiers CSV d'exemple
    for i in range(2):
        file_path = input_dir / f"file{i + 1}.csv"
        with open(file_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "category", "price", "quantity"])
            writer.writeheader()
            writer.writerows([
                {"name": f"Product {i + 1}A", "category": "Category 1", "price": "10.0", "quantity": "5"},
                {"name": f"Product {i + 1}B", "category": "Category 2", "price": "20.0", "quantity": "3"}
            ])
        file_paths.append(file_path)
    return file_paths


@pytest.fixture
def sample_report_csv(setup_directories):
    """Crée un fichier CSV d'exemple pour les rapports."""
    input_dir, _ = setup_directories
    file_path = input_dir / "report_file.csv"
    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "category", "price", "quantity"])
        writer.writeheader()
        writer.writerows([
            {"name": "Product A", "category": "Category 1", "price": "10.0", "quantity": "5"},
            {"name": "Product B", "category": "Category 2", "price": "20.0", "quantity": "3"}
        ])
    return file_path


def test_consolidate_files(setup_directories, sample_csv_files):
    """Teste la consolidation de plusieurs fichiers CSV."""
    _, output_dir = setup_directories
    output_file = output_dir / "consolidated.csv"

    commerce = Commerce()
    commerce.consolidate_files([str(f) for f in sample_csv_files], str(output_file))

    # Vérifier que le fichier consolidé a été créé
    assert output_file.exists(), "Le fichier consolidé n'a pas été créé."

    # Vérifier le contenu du fichier consolidé
    with open(output_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 4, "La consolidation n'a pas le bon nombre de lignes."
        assert rows[0]['name'] == "Product 1A"
        assert rows[3]['name'] == "Product 2B"


def test_search_data(setup_directories, sample_report_csv, capsys):
    """Teste la recherche dans un fichier CSV."""
    commerce = Commerce()

    # Cas : recherche sans filtre
    commerce.search_data(str(sample_report_csv), query="Product A")
    captured = capsys.readouterr()
    assert "Product A" in captured.out, "Le produit recherché n'a pas été trouvé."

    # Cas : recherche avec catégorie
    commerce.search_data(str(sample_report_csv), query="Product", category="Category 2")
    captured = capsys.readouterr()
    assert "Product B" in captured.out, "Le filtre par catégorie n'a pas fonctionné."

    # Cas : recherche avec plage de prix
    commerce.search_data(str(sample_report_csv), query="Product", price_range="15,25")
    captured = capsys.readouterr()
    assert "Product B" in captured.out, "Le filtre par prix n'a pas fonctionné."


def test_generate_report(setup_directories, sample_report_csv):
    """Teste la génération d'un rapport."""
    _, output_dir = setup_directories
    output_file = "report_test.txt"

    commerce = Commerce()
    commerce.generate_report(str(sample_report_csv), output_file, summary=True)

    # Vérifier que le fichier de rapport a été créé
    report_dir = os.path.join(CSVManager.OUTPUT_DIR, "report")
    report_path = os.path.join(report_dir, output_file)
    assert os.path.exists(report_path), "Le rapport n'a pas été généré."

    # Vérifier le contenu du rapport
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "Nombre de produits : 2" in content, "Le nombre de produits est incorrect."
        assert "Quantité totale : 8" in content, "La quantité totale est incorrecte."
        assert "Valeur totale : 110.00€" in content, "La valeur totale est incorrecte."
        assert "Product A" in content, "Les détails des produits sont manquants."
        assert "Product B" in content, "Les détails des produits sont manquants."
