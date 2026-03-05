import pytest

from ctxcook.config import (
    Environment,
    get_dependencies_for_recipe,
    get_dependency_versions,
    get_environment_config,
)


def test_environment_enum():
    """Test Environment enum values"""
    assert Environment.COLAB.value == "colab"
    assert Environment.DOCKER.value == "docker"
    assert Environment.LOCAL.value == "local"


def test_get_environment_config():
    """Test environment configuration retrieval"""
    colab_config = get_environment_config("colab")
    assert colab_config.name == Environment.COLAB
    assert colab_config.gpu_support is True
    assert colab_config.memory_optimized is True
    assert colab_config.auto_install is True

    docker_config = get_environment_config("docker")
    assert docker_config.name == Environment.DOCKER
    assert docker_config.gpu_support is False
    assert docker_config.auto_install is False

    local_config = get_environment_config("local")
    assert local_config.name == Environment.LOCAL
    assert local_config.gpu_support is True


def test_get_environment_config_invalid():
    """Test error handling for invalid environment"""
    with pytest.raises(ValueError, match="Unsupported environment"):
        get_environment_config("invalid_env")


def test_get_dependency_versions():
    """Test dependency version configuration"""
    versions = get_dependency_versions()
    assert versions.torch == "2.1.0"
    assert versions.transformers == "4.36.0"
    assert versions.datasets == "2.15.0"
    assert versions.accelerate == "0.25.0"


def test_get_dependencies_for_recipe():
    """Test dependency extraction for different environments"""
    recipe = {
        "name": "test_recipe",
        "model": {"base": "test/model"},
        "dataset": {"source": "local"},
    }

    colab_deps = get_dependencies_for_recipe(recipe, Environment.COLAB)
    assert "torch" in colab_deps
    assert "transformers" in colab_deps
    assert "matplotlib" in colab_deps  # Colab-specific

    docker_deps = get_dependencies_for_recipe(recipe, Environment.DOCKER)
    assert "torch" in docker_deps
    assert "transformers" in docker_deps
    assert "matplotlib" not in docker_deps  # Not in Docker


def test_get_dependencies_with_quantization():
    """Test dependency extraction with quantization"""
    recipe = {
        "name": "test_recipe",
        "model": {"base": "test/model", "quantization": "4bit"},
        "dataset": {"source": "local"},
    }

    deps = get_dependencies_for_recipe(recipe, Environment.COLAB)
    assert "accelerate" in deps
    assert "bitsandbytes" in deps


def test_get_dependencies_with_finetuning():
    """Test dependency extraction with fine-tuning"""
    recipe = {
        "name": "finetune_test",
        "model": {"base": "test/model"},
        "dataset": {"source": "local"},
    }

    deps = get_dependencies_for_recipe(recipe, Environment.COLAB)
    assert "peft" in deps
