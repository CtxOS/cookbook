from typing import Dict

from .config import get_dependency_versions, get_dependencies_for_recipe, Environment

class RequirementsGenerator:
    """Generate requirements.txt files with version pinning"""

    def __init__(self):
        self.versions = get_dependency_versions()

    def generate_requirements(self, recipe: dict, environment: str = "colab") -> str:
        """Generate requirements.txt content for a specific environment"""
        try:
            env = Environment(environment.lower())
            dependencies = get_dependencies_for_recipe(recipe, env)

            requirements = []
            for dep in dependencies:
                version = getattr(self.versions, dep, None)
                if version:
                    requirements.append(f"{dep}=={version}")
                else:
                    requirements.append(dep)

            return "\n".join(requirements)
        except ValueError:
            # Fallback for unknown environments
            return self._generate_basic_requirements()

    def generate_docker_requirements(self, recipe: dict) -> str:
        """Generate requirements for Docker environment"""
        base_deps = [
            f"torch=={self.versions.torch}",
            f"transformers=={self.versions.transformers}",
            f"datasets=={self.versions.datasets}",
            f"accelerate=={self.versions.accelerate}",
            f"pyyaml=={self.versions.pyyaml}",
            f"jinja2=={self.versions.jinja2}",
            f"click=={self.versions.click}",
            f"nbformat=={self.versions.nbformat}",
        ]

        # Add conditional dependencies
        if recipe.get("model", {}).get("quantization") == "4bit":
            base_deps.append(f"bitsandbytes=={self.versions.bitsandbytes}")

        if "finetune" in recipe.get("name", "").lower():
            base_deps.append(f"peft=={self.versions.peft}")

        return "\n".join(base_deps)

    def _generate_basic_requirements(self) -> str:
        """Generate basic requirements for fallback"""
        return f"""
torch=={self.versions.torch}
transformers=={self.versions.transformers}
datasets=={self.versions.datasets}
accelerate=={self.versions.accelerate}
pyyaml=={self.versions.pyyaml}
jinja2=={self.versions.jinja2}
click=={self.versions.click}
nbformat=={self.versions.nbformat}
        """.strip()

    def get_version_info(self) -> Dict[str, str]:
        """Get all version information as dictionary"""
        return {
            "torch": self.versions.torch,
            "transformers": self.versions.transformers,
            "datasets": self.versions.datasets,
            "accelerate": self.versions.accelerate,
            "bitsandbytes": self.versions.bitsandbytes,
            "peft": self.versions.peft,
            "jinja2": self.versions.jinja2,
            "click": self.versions.click,
            "pyyaml": self.versions.pyyaml,
            "nbformat": self.versions.nbformat,
        }
