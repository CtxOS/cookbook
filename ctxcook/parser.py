from pathlib import Path

import yaml


def load_recipe(path: str) -> dict:
    """Load a YAML recipe file and return as dictionary."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} not found")

    with open(path) as f:
        return yaml.safe_load(f)
