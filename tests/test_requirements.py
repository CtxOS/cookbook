
from ctxcook.requirements import RequirementsGenerator


def test_requirements_generator_init():
    """Test RequirementsGenerator initialization"""
    req_gen = RequirementsGenerator()
    assert req_gen.versions is not None
    assert req_gen.versions.torch == "2.1.0"


def test_generate_requirements_colab():
    """Test requirements generation for Colab environment"""
    req_gen = RequirementsGenerator()
    recipe = {
        "name": "test_recipe",
        "model": {"base": "test/model"},
        "dataset": {"source": "local"},
    }

    requirements = req_gen.generate_requirements(recipe, "colab")

    assert "torch==2.1.0" in requirements
    assert "transformers==4.36.0" in requirements
    assert "datasets==2.15.0" in requirements
    assert "matplotlib" in requirements  # Colab-specific


def test_generate_requirements_with_quantization():
    """Test requirements generation with quantization"""
    req_gen = RequirementsGenerator()
    recipe = {
        "name": "test_recipe",
        "model": {"base": "test/model", "quantization": "4bit"},
        "dataset": {"source": "local"},
    }

    requirements = req_gen.generate_requirements(recipe, "colab")

    assert "accelerate==0.25.0" in requirements
    assert "bitsandbytes==0.41.0" in requirements


def test_generate_requirements_with_finetuning():
    """Test requirements generation with fine-tuning"""
    req_gen = RequirementsGenerator()
    recipe = {
        "name": "finetune_test",
        "model": {"base": "test/model"},
        "dataset": {"source": "local"},
    }

    requirements = req_gen.generate_requirements(recipe, "colab")

    assert "peft==0.7.0" in requirements


def test_generate_docker_requirements():
    """Test Docker requirements generation"""
    req_gen = RequirementsGenerator()
    recipe = {
        "name": "test_recipe",
        "model": {"base": "test/model"},
        "dataset": {"source": "local"},
    }

    docker_req = req_gen.generate_docker_requirements(recipe)

    assert "torch==2.1.0" in docker_req
    assert "transformers==4.36.0" in docker_req
    assert "jinja2==3.1.6" in docker_req
    assert "click==8.3.1" in docker_req


def test_generate_docker_requirements_with_quantization():
    """Test Docker requirements generation with quantization"""
    req_gen = RequirementsGenerator()
    recipe = {
        "name": "test_recipe",
        "model": {"base": "test/model", "quantization": "4bit"},
        "dataset": {"source": "local"},
    }

    docker_req = req_gen.generate_docker_requirements(recipe)

    assert "bitsandbytes==0.41.0" in docker_req


def test_generate_basic_requirements():
    """Test basic requirements generation fallback"""
    req_gen = RequirementsGenerator()
    basic_req = req_gen._generate_basic_requirements()

    assert "torch==2.1.0" in basic_req
    assert "transformers==4.36.0" in basic_req
    assert "datasets==2.15.0" in basic_req


def test_get_version_info():
    """Test version information retrieval"""
    req_gen = RequirementsGenerator()
    versions = req_gen.get_version_info()

    assert isinstance(versions, dict)
    assert "torch" in versions
    assert "transformers" in versions
    assert versions["torch"] == "2.1.0"
    assert versions["transformers"] == "4.36.0"


def test_generate_requirements_invalid_environment():
    """Test requirements generation with invalid environment"""
    req_gen = RequirementsGenerator()
    recipe = {
        "name": "test_recipe",
        "model": {"base": "test/model"},
        "dataset": {"source": "local"},
    }

    # Should fallback to basic requirements for invalid environment
    requirements = req_gen.generate_requirements(recipe, "invalid_env")
    assert "torch==2.1.0" in requirements
