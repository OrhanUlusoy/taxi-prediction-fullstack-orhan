from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from taxipred.backend.data_processing import sample_rows


def _repo_root() -> Path:
    # .../src/taxipred/backend/api.py -> repo root is parents[3]
    return Path(__file__).resolve().parents[3]


def _load_artifacts() -> tuple[Any, list[str]]:
    root = _repo_root()
    model_path = root / "linear_regression_model.pkl"
    features_path = root / "model_features.pkl"

    if not model_path.exists():
        raise FileNotFoundError(f"Missing model artifact: {model_path}")
    if not features_path.exists():
        raise FileNotFoundError(f"Missing feature list artifact: {features_path}")

    model = joblib.load(model_path)
    features = joblib.load(features_path)

    # model_features.pkl might be a pandas Index
    if hasattr(features, "tolist"):
        features = features.tolist()

    if not isinstance(features, list) or not all(isinstance(c, str) for c in features):
        raise TypeError("model_features.pkl must contain a list of column names")

    return model, features


app = FastAPI(title="Taxi Prediction API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/data/sample")
def data_sample(n: int = 5) -> dict[str, Any]:
    if n < 1 or n > 100:
        raise HTTPException(status_code=400, detail="n must be between 1 and 100")
    return {"rows": sample_rows(n)}


@app.post("/predict")
def predict(payload: dict[str, Any]) -> dict[str, float]:
    try:
        model, feature_columns = _load_artifacts()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    # Build one-row dataframe from incoming JSON
    try:
        row = {k: (0 if v is None else v) for k, v in payload.items()}
        x = pd.DataFrame([row])
        x = x.reindex(columns=feature_columns, fill_value=0)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid input payload: {exc}") from exc

    try:
        y = model.predict(x)
        pred = float(y[0])
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc

    return {"predicted_price": pred}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("taxipred.backend.api:app", host="127.0.0.1", port=8000, reload=True)
