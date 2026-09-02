from pathlib import Path

from opengrad.registry.validate import validate


def test_registries_validate():
    assert validate(Path(__file__).parents[2]) == []
