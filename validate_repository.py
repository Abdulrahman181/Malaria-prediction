"""Static checks that do not require TensorFlow or the image dataset."""

from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOTEBOOK = ROOT / "malaria-pred.ipynb"


def validate_notebook(path: Path = NOTEBOOK) -> list[str]:
    errors: list[str] = []
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read notebook: {exc}"]
    if notebook.get("nbformat") != 4:
        errors.append("notebook must use nbformat 4")
    for index, cell in enumerate(notebook.get("cells", [])):
        if cell.get("cell_type") == "code":
            if cell.get("execution_count") is not None:
                errors.append(f"cell {index} has a stale execution count")
            if cell.get("outputs"):
                errors.append(f"cell {index} has stale outputs")
            source = "".join(cell.get("source", []))
            try:
                ast.parse(source)
            except SyntaxError as exc:
                errors.append(f"cell {index} has invalid Python: {exc}")
            for forbidden in ("/kaggle/", "fit_generator", "evaluate_generator"):
                if forbidden in source:
                    errors.append(f"cell {index} contains forbidden legacy text: {forbidden}")
    return errors


def main() -> int:
    errors = validate_notebook()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(
        "Repository static validation passed: notebook JSON, outputs, syntax, and "
        "legacy paths checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
