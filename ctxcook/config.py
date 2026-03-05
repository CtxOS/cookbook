from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class Environment(Enum):
    COLAB = "colab"
    DOCKER = "docker"
    LOCAL = "local"


@dataclass
class EnvironmentConfig:
    """Environment-specific configuration"""

    name: Environment
    python_version: str
    gpu_support: bool
    memory_optimized: bool
    auto_install: bool
    dependencies: List[str]
    special_features: List[str]


# Environment configurations
ENVIRONMENT_CONFIGS: Dict[Environment, EnvironmentConfig] = {
    Environment.COLAB: EnvironmentConfig(
        name=Environment.COLAB,
        python_version="3.9.0",
        gpu_support=True,
        memory_optimized=True,
        auto_install=True,
        dependencies=["torch", "transformers", "datasets"],
        special_features=["gpu_detection", "memory_management", "auto_mounting"],
    ),
    Environment.DOCKER: EnvironmentConfig(
        name=Environment.DOCKER,
        python_version="3.9",
        gpu_support=False,
        memory_optimized=False,
        auto_install=False,
        dependencies=["torch", "transformers", "datasets"],
        special_features=["containerization", "portability"],
    ),
    Environment.LOCAL: EnvironmentConfig(
        name=Environment.LOCAL,
        python_version="3.9",
        gpu_support=True,
        memory_optimized=False,
        auto_install=False,
        dependencies=["torch", "transformers", "datasets"],
        special_features=["flexibility", "custom_config"],
    ),
}


def get_environment_config(env_name: str) -> EnvironmentConfig:
    """Get environment configuration by name"""
    try:
        env = Environment(env_name.lower())
        return ENVIRONMENT_CONFIGS[env]
    except (ValueError, KeyError):
        raise ValueError(
            f"Unsupported environment: {env_name}. "
            f"Supported: {[e.value for e in Environment]}"
        )


def get_dependency_versions() -> DependencyVersions:
    """Get dependency version configuration"""
    return DependencyVersions()


def get_dependencies_for_recipe(
    recipe: dict, environment: Environment
) -> List[str]:
    """Get environment-specific dependencies for a recipe"""
    base_deps = ENVIRONMENT_CONFIGS[environment].dependencies.copy()

    # Add quantization dependencies
    if recipe.get("model", {}).get("quantization") == "4bit":
        base_deps.extend(["accelerate", "bitsandbytes"])

    # Add fine-tuning dependencies
    if "finetune" in recipe.get("name", "").lower():
        base_deps.append("peft")

    # Add environment-specific dependencies
    if environment == Environment.COLAB:
        base_deps.extend(["matplotlib", "seaborn"])  # For visualization

    return list(set(base_deps))  # Remove duplicates


@dataclass
class DependencyVersions:
    """Version pinning configuration"""
    torch: str = "2.1.0"
    transformers: str = "4.36.0"
    datasets: str = "2.15.0"
    accelerate: str = "0.25.0"
    bitsandbytes: str = "0.41.0"
    peft: str = "0.7.0"
    jinja2: str = "3.1.6"
    click: str = "8.3.1"
    pyyaml: str = "6.0.3"
    nbformat: str = "5.10.4"
