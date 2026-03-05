import nbformat
from nbformat.v4 import new_code_cell, new_notebook

from .generator import TemplateGenerator


def build_notebook(recipe: dict, environment: str = "colab"):
    """Build a Jupyter notebook from a recipe dictionary using Jinja2 templates."""
    try:
        generator = TemplateGenerator()

        # Use Jinja2 template generation
        notebook_dict = generator.render_notebook(recipe, environment)
        nb = nbformat.from_dict(notebook_dict)

        return nb
    except Exception as e:
        # Fallback to basic notebook generation
        print(f"Template generation failed, using basic generation: {e}")
        return _build_basic_notebook(recipe)


def _build_basic_notebook(recipe: dict):
    """Fallback basic notebook generation (original implementation)"""
    nb = new_notebook()

    install = new_code_cell("""
!pip install transformers datasets peft accelerate
    """)

    model_cell = new_code_cell(f"""
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "{recipe['model']['base']}",
    load_in_4bit=True
)

print("Model loaded")
    """)

    nb.cells = [install, model_cell]
    return nb
