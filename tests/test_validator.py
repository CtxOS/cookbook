import pytest

from ctxcook.validator import validate


def test_validate_valid_recipe():
    """Test validation of a valid recipe"""
    recipe = {
        "name": "test_recipe",
        "model": {"base": "test/model"},
        "dataset": {"source": "test"},
    }
    assert validate(recipe) is True


def test_validate_missing_name():
    """Test validation fails when name is missing"""
    recipe = {"model": {"base": "test/model"}, "dataset": {"source": "test"}}
    with pytest.raises(ValueError, match="Missing required field: name"):
        validate(recipe)


def test_validate_missing_model():
    """Test validation fails when model is missing"""
    recipe = {"name": "test_recipe", "dataset": {"source": "test"}}
    with pytest.raises(ValueError, match="Missing required field: model"):
        validate(recipe)


def test_validate_missing_dataset():
    """Test validation fails when dataset is missing"""
    recipe = {"name": "test_recipe", "model": {"base": "test/model"}}
    with pytest.raises(ValueError, match="Missing required field: dataset"):
        validate(recipe)


def test_validate_missing_model_base():
    """Test validation fails when model.base is missing"""
    recipe = {
        "name": "test_recipe",
        "model": {"quantization": "4bit"},
        "dataset": {"source": "test"},
    }
    with pytest.raises(ValueError, match="Model base is required"):
        validate(recipe)
