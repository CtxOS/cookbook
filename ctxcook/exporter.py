from pathlib import Path

import nbformat


def export_notebook(nb, output_path: str):
    """Export a notebook object to a file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        nbformat.write(nb, f)
