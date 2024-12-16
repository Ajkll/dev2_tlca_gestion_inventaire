import pytest
from argparse import ArgumentParser
from src.module_perso.parser import secluded_parser


def test_secluded_parser_returns_argumentparser():
    """Teste si la fonction retourne bien un objet ArgumentParser."""
    parser = secluded_parser()
    assert isinstance(parser, ArgumentParser)


@pytest.mark.parametrize("args,expected", [
    (["consolidate", "--files", "file1.csv", "file2.csv"],
     {"command": "consolidate", "files": ["file1.csv", "file2.csv"], "output": "consolidated.csv"}),

    (["search", "--query", "product_name"],
     {"command": "search", "file": "data.csv", "query": "product_name", "category": None, "price_range": None}),

    (["search", "--file", "inventory.csv", "--query", "electronics", "--category", "gadgets"],
     {"command": "search", "file": "inventory.csv", "query": "electronics", "category": "gadgets", "price_range": None}),

    (["report", "--file", "inventory.csv", "--output", "report.txt", "--summary"],
     {"command": "report", "file": "inventory.csv", "output": "report.txt", "summary": True}),
])
def test_parser_arguments(args, expected):
    """Teste si le parser interprète correctement les arguments pour chaque sous-commande."""
    parser = secluded_parser()
    parsed_args = vars(parser.parse_args(args))
    assert parsed_args == expected


def test_parser_fails_with_missing_arguments():
    """Teste si le parser échoue lorsque des arguments obligatoires manquent."""
    parser = secluded_parser()

    # La commande 'consolidate' sans `--files` doit lever une erreur
    with pytest.raises(SystemExit):
        parser.parse_args(["consolidate"])

    # La commande 'search' sans `--query` doit lever une erreur
    with pytest.raises(SystemExit):
        parser.parse_args(["search"])

    # La commande 'report' avec des arguments incorrects doit lever une erreur
    with pytest.raises(SystemExit):
        parser.parse_args(["report", "--summary", "--nonexistent"])
