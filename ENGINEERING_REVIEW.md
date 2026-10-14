# Engineering review: `Abdulrahman181/Malaria-prediction`

**Review scope:** all repository files present at the audit start, including `malaria-pred.ipynb`, its Python code cells, dependency declarations (none existed initially), and repository documentation (none existed initially).

## Baseline findings

The repository initially contained only one notebook. It had no README, dependency manifest, tests, validator, or ignore rules. The notebook had these engineering issues:

- It contained hard-coded Kaggle paths (`/kaggle/input/...`) and therefore could not run outside the original environment.
- It used removed or obsolete APIs and signatures: standalone `keras` imports, `Convolution2D` positional arguments, `Dense(output_dim=...)`, `fit_generator`, `evaluate_generator`, `nb_epoch`, and `nb_val_samples`.
- The notebook JSON was not schema-clean: markdown cells carried `execution_count`, and the file contained large stale outputs, including partial training logs and plots.
- The test directory was passed as `validation_data` and used for early stopping. This is test-set leakage and makes the reported test performance unsuitable as an untouched final estimate.
- The run had no explicit seed or deterministic-operation request, fixed arbitrary `steps_per_epoch`/validation sample counts, no reliable class-index handling, and accuracy was the only configured metric.
- A single-image prediction assumed class semantics instead of using a verified class-index mapping.
- The dataset, weights, and artifacts were not present, so no baseline metric can be verified or honestly reported.

## Remediation

- Added `malaria_pipeline.py`, a reusable CLI/module using current `tensorflow.keras` APIs with lazy TensorFlow imports. It validates the dataset contract, fails closed on absent/malformed data, uses a seeded validation subset from `training_set`, keeps `testing_set` untouched until final evaluation, and derives generator sizes from the data.
- Added exact byte-level cross-split duplicate detection. A duplicate raises an error rather than silently training on leaked data. Near-duplicates, patient-level overlap, and provenance remain dataset-level limitations and require domain metadata.
- Added reproducibility controls for Python, NumPy, and TensorFlow seeds, plus TensorFlow deterministic operations where supported. Reproducibility is still hardware/kernel dependent.
- Added threshold metrics (accuracy, precision, recall, specificity, F1, and confusion counts) computed from final test predictions. Undefined ratios are represented as `null`; no values are fabricated.
- Replaced `malaria-pred.ipynb` with a valid, output-free wrapper around the audited module. It has no hard-coded local/Kaggle paths and stops clearly when the configured data or TensorFlow is absent.
- Added `README.md`, `requirements.txt`, `pyproject.toml`, `.gitignore`, `validate_repository.py`, and `tests/test_repository.py`.

## Validation performed

The following checks passed in the shared Sandbox after the changes:

```text
python validate_repository.py
Repository static validation passed: notebook JSON, outputs, syntax, and legacy paths checked.

python -m compileall -q malaria_pipeline.py validate_repository.py tests
pytest -q
5 passed in 0.33s

ruff check .
All checks passed!
```

The CLI was also invoked with a nonexistent data directory. It exited with code 2 and the actionable message that `MALARIA_DATA_DIR` or `--data-dir` must point to a directory containing `training_set/` and `testing_set/`.

## Not run / limitations

A complete training and evaluation run was **not** claimed. The repository has no image data or saved artifacts, and TensorFlow is not installed in the audit environment. Consequently, there are no measured accuracy, loss, or clinical-performance claims in this review. Installing the declared dependencies and supplying an authorized dataset are prerequisites for a real run. The dataset source/provenance, patient identifiers, acquisition grouping, and semantic near-duplicate policy are not included and must be reviewed before interpreting any future metrics.
