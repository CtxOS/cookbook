import tempfile

import pytest
import yaml

from ctxcook.parser import load_recipe


def test_load_recipe_valid():
    """Test loading a valid YAML recipe"""
    recipe_data = {
        "name": "test_recipe",
        "model": {"base": "test/model"},
        "dataset": {"source": "test"},
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(recipe_data, f)
        temp_path = f.name

    try:
        result = load_recipe(temp_path)
        assert result == recipe_data
    finally:
        import os

        os.unlink(temp_path)


def test_load_recipe_not_found():
    """Test loading a non-existent recipe"""
    with pytest.raises(FileNotFoundError):
        load_recipe("nonexistent.yaml")
