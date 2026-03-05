REQUIRED = ["name", "model", "dataset"]


def validate(recipe: dict):
    """Validate a recipe dictionary contains required fields."""
    for key in REQUIRED:
        if key not in recipe:
            raise ValueError(f"Missing required field: {key}")

    if "base" not in recipe["model"]:
        raise ValueError("Model base is required")

    return True
