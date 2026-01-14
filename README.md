# Taxi Prediction (Lab)

This repo is set up to use a local virtual environment in `.venv` so VS Code terminals and Jupyter notebooks use the same Python + packages.

## Setup (Windows)

From the repo root:

- Create / update the virtual environment:
  - `py -m venv .venv`
  - `./.venv/Scripts/python.exe -m pip install -U pip`
  - `./.venv/Scripts/python.exe -m pip install -r requirements.txt`

## Running notebooks

- Open this folder in VS Code: `C:\Users\Orhan\git\Taxi Lab\taxi-prediction-fullstack-orhan`
- Open the notebook in `src/taxi_prediction_fullstack_orhan/model_development/`
- Select the kernel that points to `.venv`.

If you ever get `ModuleNotFoundError` in a notebook, it usually means the notebook is using a different interpreter than the one you installed packages into.
