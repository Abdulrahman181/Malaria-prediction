from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from malaria_pipeline import (
    classification_metrics,
    find_cross_split_duplicates,
    resolve_dataset_dir,
)

ROOT = Path(__file__).resolve().parents[1]


def _make_dataset(root: Path, *, duplicate: bool = False) -> None:
    for split in ("training_set", "testing_set"):
        for label in ("Parasitised", "Uninfected"):
            directory = root / split / label
            directory.mkdir(parents=True, exist_ok=True)
            content = (
                b"same-image"
                if duplicate and split == "testing_set"
                else f"{split}-{label}".encode()
            )
            (directory / "sample.png").write_bytes(content)
    if duplicate:
        (root / "training_set" / "Parasitised" / "duplicate.png").write_bytes(b"same-image")


def test_resolve_dataset_dir_requires_real_data(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Dataset directory not found"):
        resolve_dataset_dir(tmp_path / "missing")


def test_resolve_dataset_dir_validates_layout(tmp_path: Path) -> None:
    _make_dataset(tmp_path)
    paths = resolve_dataset_dir(tmp_path)
    assert paths.train.name == "training_set"
    assert paths.test.name == "testing_set"


def test_exact_cross_split_duplicates_are_detected(tmp_path: Path) -> None:
    _make_dataset(tmp_path, duplicate=True)
    paths = resolve_dataset_dir(tmp_path)
    duplicates = find_cross_split_duplicates(paths)
    assert duplicates


def test_classification_metrics_are_computed_without_fabricated_values() -> None:
    metrics = classification_metrics([0, 0, 1, 1], [0.1, 0.8, 0.7, 0.2])
    assert metrics["accuracy"] == pytest.approx(0.5)
    assert metrics["precision"] == pytest.approx(0.5)
    assert metrics["recall"] == pytest.approx(0.5)
    assert metrics["specificity"] == pytest.approx(0.5)
    assert metrics["f1"] == pytest.approx(0.5)


def test_notebook_is_valid_clean_and_has_no_legacy_training_apis() -> None:
    notebook = json.loads((ROOT / "malaria-pred.ipynb").read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4
    for cell in notebook["cells"]:
        if cell["cell_type"] == "code":
            assert cell["execution_count"] is None
            assert cell["outputs"] == []
            ast.parse("".join(cell["source"]))
            source = "".join(cell["source"])
            assert "/kaggle/" not in source
            assert "fit_generator" not in source
            assert "evaluate_generator" not in source
