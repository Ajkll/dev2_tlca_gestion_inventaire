import pytest
from unittest.mock import patch, MagicMock
from main import main
from module_perso.csv_manager import Commerce, CSVError
import sys

def test_main_no_command(capsys):
    """Teste si le script affiche l'aide lorsqu'aucune commande n'est fournie."""
    test_args = ["main.py"]
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(SystemExit):
            main()
        captured = capsys.readouterr()
        assert "usage:" in captured.out

def test_main_consolidate_success():
    """Teste la commande consolidate avec des fichiers valides."""
    test_args = ["main.py", "consolidate", "--files", "file1.csv", "file2.csv", "--output", "output.csv"]

    mock_commerce = MagicMock()
    with patch("main.Commerce", return_value=mock_commerce):
        with patch.object(sys, 'argv', test_args):
            main()

    mock_commerce.consolidate_files.assert_called_once_with(["file1.csv", "file2.csv"], "output.csv")

def test_main_search_success():
    """Teste la commande search avec une requête valide."""
    test_args = ["main.py", "search", "--file", "file.csv", "--query", "Product"]

    mock_commerce = MagicMock()
    with patch("main.Commerce", return_value=mock_commerce):
        with patch.object(sys, 'argv', test_args):
            main()

    mock_commerce.search_data.assert_called_once_with("file.csv", "Product", None, None)

def test_main_search_with_filters():
    """Teste la commande search avec une catégorie et une plage de prix."""
    test_args = ["main.py", "search", "--file", "file.csv", "--query", "Product", "--category", "Category1", "--price-range", "10,50"]

    mock_commerce = MagicMock()
    with patch("main.Commerce", return_value=mock_commerce):
        with patch.object(sys, 'argv', test_args):
            main()

    mock_commerce.search_data.assert_called_once_with("file.csv", "Product", "Category1", "10,50")

def test_main_report_success():
    """Teste la commande report avec les paramètres par défaut."""
    test_args = ["main.py", "report", "--file", "file.csv", "--output", "report.txt"]

    mock_commerce = MagicMock()
    with patch("main.Commerce", return_value=mock_commerce):
        with patch.object(sys, 'argv', test_args):
            main()

    mock_commerce.generate_report.assert_called_once_with("file.csv", "report.txt", False)

def test_main_report_with_summary():
    """Teste la commande report avec le flag --summary."""
    test_args = ["main.py", "report", "--file", "file.csv", "--output", "report.txt", "--summary"]

    mock_commerce = MagicMock()
    with patch("main.Commerce", return_value=mock_commerce):
        with patch.object(sys, 'argv', test_args):
            main()

    mock_commerce.generate_report.assert_called_once_with("file.csv", "report.txt", True)

def test_main_csv_error(capsys):
    """Teste si une erreur CSVError est correctement gérée."""
    test_args = ["main.py", "consolidate", "--files", "file1.csv", "file2.csv", "--output", "output.csv"]

    mock_commerce = MagicMock()
    mock_commerce.consolidate_files.side_effect = CSVError("Erreur simulée")
    with patch("main.Commerce", return_value=mock_commerce):
        with patch.object(sys, 'argv', test_args):
            with pytest.raises(SystemExit):
                main()

    captured = capsys.readouterr()
    assert "Erreur : Erreur simulée" in captured.err

def test_main_unexpected_error(capsys):
    """Teste si une erreur inattendue est correctement gérée."""
    test_args = ["main.py", "consolidate", "--files", "file1.csv", "file2.csv", "--output", "output.csv"]

    mock_commerce = MagicMock()
    mock_commerce.consolidate_files.side_effect = Exception("Erreur inattendue")
    with patch("main.Commerce", return_value=mock_commerce):
        with patch.object(sys, 'argv', test_args):
            with pytest.raises(SystemExit):
                main()

    captured = capsys.readouterr()
    assert "Erreur imprévue : Erreur inattendue" in captured.err
