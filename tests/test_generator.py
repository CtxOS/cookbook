

from ctxcook.generator import TemplateGenerator


def test_template_generator_init():
    """Test TemplateGenerator initialization"""
    generator = TemplateGenerator()
    assert generator.template_dir.exists()
    assert generator.env is not None


def test_render_notebook_colab():
    """Test notebook rendering for Colab environment"""
    generator = TemplateGenerator()
    recipe = {
        "name": "test_finetune",
        "model": {"base": "test/model", "quantization": "4bit"},
        "dataset": {"name": "test_dataset"},
    }

    notebook_dict = generator.render_notebook(recipe, "colab")

    assert "cells" in notebook_dict
    assert "metadata" in notebook_dict
    assert notebook_dict["nbformat"] == 4
    assert len(notebook_dict["cells"]) > 0


def test_render_notebook_basic_fallback():
    """Test fallback to basic template"""
    generator = TemplateGenerator()
    recipe = {
        "name": "test_recipe",
        "model": {"base": "test/model"},
        "dataset": {"source": "local"},
    }

    # Use environment that doesn't have specific template
    notebook_dict = generator.render_notebook(recipe, "local")

    assert "cells" in notebook_dict
    assert isinstance(notebook_dict, dict)


def test_render_dockerfile():
    """Test Dockerfile rendering"""
    generator = TemplateGenerator()
    recipe = {
        "name": "test_recipe",
        "model": {"base": "test/model"},
        "dataset": {"source": "local"},
    }

    dockerfile = generator.render_dockerfile(recipe)

    assert "FROM python:" in dockerfile
    assert "WORKDIR /app" in dockerfile
    assert "COPY" in dockerfile


def test_render_hf_deploy():
    """Test Hugging Face deployment config rendering"""
    generator = TemplateGenerator()
    recipe = {
        "name": "test_model",
        "model": {"base": "test/model"},
        "dataset": {"source": "local"},
    }

    hf_config = generator.render_hf_deploy(recipe)

    assert "api_version: 1" in hf_config
    assert "test_model" in hf_config
    assert "test/model" in hf_config


def test_extract_dependencies():
    """Test dependency extraction from recipe"""
    generator = TemplateGenerator()

    # Basic recipe
    recipe1 = {
        "name": "basic",
        "model": {"base": "test"},
        "dataset": {"source": "local"},
    }
    deps1 = generator._extract_dependencies(recipe1)
    assert "torch" in deps1
    assert "transformers" in deps1

    # Recipe with 4bit quantization
    recipe2 = {
        "name": "quantized",
        "model": {"base": "test", "quantization": "4bit"},
        "dataset": {"source": "local"},
    }
    deps2 = generator._extract_dependencies(recipe2)
    assert "bitsandbytes" in deps2
    assert "accelerate" in deps2

    # Recipe with fine-tuning
    recipe3 = {
        "name": "finetune_test",
        "model": {"base": "test"},
        "dataset": {"source": "local"},
    }
    deps3 = generator._extract_dependencies(recipe3)
    assert "peft" in deps3
