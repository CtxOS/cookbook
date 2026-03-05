import json
from pathlib import Path
from typing import Any, Dict

import jinja2


class TemplateGenerator:
    """Enhanced generator using Jinja2 templates"""

    def __init__(self, template_dir: str = None):
        if template_dir is None:
            template_dir = Path(__file__).parent.parent / "templates"
        self.template_dir = Path(template_dir)
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.template_dir)),
            autoescape=jinja2.select_autoescape(),
        )

    def render_notebook(
        self, recipe: Dict[str, Any], environment: str = "colab"
    ) -> Dict[str, Any]:
        """Render notebook using Jinja2 template"""
        template_name = f"{environment}_notebook_template.j2"

        try:
            template = self.env.get_template(template_name)
        except jinja2.TemplateNotFound:
            # Fallback to basic template
            template = self.env.get_template("basic_notebook_template.j2")

        context = {
            "recipe": recipe,
            "environment": environment,
            "model_name": recipe.get("model", {}).get("base", "unknown"),
            "dataset_name": recipe.get("dataset", {}).get(
                "name", "local"
            ),
            "quantization": recipe.get("model", {}).get(
                "quantization", "none"
            ),
            "recipe_name": recipe.get("name", "unnamed_recipe"),
        }

        rendered = template.render(**context)

        # Parse rendered JSON as notebook
        return json.loads(rendered)

    def render_dockerfile(self, recipe: Dict[str, Any]) -> str:
        """Render Dockerfile using Jinja2 template"""
        template = self.env.get_template("docker_template.j2")

        context = {
            "recipe": recipe,
            "python_version": "3.9",
            "dependencies": self._extract_dependencies(recipe),
        }

        return template.render(**context)

    def render_hf_deploy(self, recipe: Dict[str, Any]) -> str:
        """Render Hugging Face deployment config"""
        template = self.env.get_template("hf_deploy_template.j2")

        context = {
            "recipe_name": recipe.get("name", "model"),
            "model_path": recipe.get("model", {}).get("base", ""),
            "python_version": "3.9",
        }

        return template.render(**context)

    def _extract_dependencies(self, recipe: Dict[str, Any]) -> list:
        """Extract dependencies from recipe"""
        deps = ["torch", "transformers", "datasets"]

        if recipe.get("model", {}).get("quantization") == "4bit":
            deps.extend(["bitsandbytes", "accelerate"])

        if "finetune" in recipe.get("name", "").lower():
            deps.append("peft")

        return deps
