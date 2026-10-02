# Malaria cell image classification (CNN notebook)

This repository contains a notebook that trains a binary CNN classifier on malaria-cell images. **The image dataset is not included**, so the notebook cannot be trained or evaluated from this repository alone. No model weights or validated performance measurements are provided.

## Requirements

Use Python 3.11 and install the pinned notebook dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Open `malaria-pred.ipynb` in Jupyter and run its cells in order.

## Dataset

Obtain the image dataset from its authorized source; it is intentionally not redistributed here. Set `MALARIA_DATA_DIR` to the directory containing `training_set` and `testing_set`. The default is `data/Malaria Cells` relative to the notebook's working directory. Expected structure:

```text
<dataset-root>/
  training_set/
    <class-1>/ ... image files ...
    <class-2>/ ... image files ...
  testing_set/
    <class-1>/ ... image files ...
    <class-2>/ ... image files ...
```

Both splits must contain the same two class subdirectories. Keras derives class indices alphabetically from the subdirectory names; the notebook maps predictions back through those indices instead of assuming a specific spelling or index. A separate image can optionally be classified by setting `MALARIA_IMAGE_FILE` to its path. The notebook rescales that image the same way as the training data.

## Reproducibility and limitations

The notebook uses TensorFlow/Keras APIs compatible with the pinned environment and derives epoch/step counts from the available images. The test split is evaluated after training and is not used for early stopping. For model selection or tuning, create a separate validation split rather than repeatedly consulting the test results. Results depend on the dataset, runtime, and random initialization; this repository does not assert clinical validity or any level of accuracy. This educational example is not a diagnostic tool.

No Kaggle API credentials are needed by the notebook. If you independently use Kaggle tooling, keep its credential file outside this repository and never commit it.
