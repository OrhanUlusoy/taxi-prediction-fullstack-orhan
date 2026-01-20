from __future__ import annotations

"""FastAPI-backend för taxi-prisprognos.

Översikt:
- /health: enkel ping för att se att API:t lever
- /data/sample: visar exempelrader från CSV (snabb sanity check)
- /predict: tar emot en JSON med features och returnerar predikterat pris

Viktigt: Modellen och feature-listan laddas från artifacts i repo-roten.
Det gör att vi kan träna i notebook/script och sedan servera samma modell här.
"""

from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from taxipred.backend.data_processing import sample_rows


def _repo_root() -> Path:
    # Robust väg till repo-rooten:
    # .../src/taxipred/backend/api.py -> repo root är parents[3]
    return Path(__file__).resolve().parents[3]


def _load_artifacts() -> tuple[Any, list[str]]:
    # Laddar modellen + vilken feature-ordning modellen förväntar sig.
    root = _repo_root()
    model_path = root / "linear_regression_model.pkl"
    features_path = root / "model_features.pkl"

    if not model_path.exists(): 
        raise FileNotFoundError(f"Missing model artifact: {model_path}")
    if not features_path.exists():
        raise FileNotFoundError(f"Missing feature list artifact: {features_path}")

    model = joblib.load(model_path)
    features = joblib.load(features_path)

    # model_features.pkl kan vara en pandas Index (i notebooken sparar man ibland så)
    if hasattr(features, "tolist"):
        features = features.tolist()

    if not isinstance(features, list) or not all(isinstance(c, str) for c in features):
        raise TypeError("model_features.pkl must contain a list of column names")

    return model, features


app = FastAPI(title="Taxi Prediction API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    # Minimal endpoint för att verifiera att servern är igång.
    return {"status": "ok"}


@app.get("/data/sample")
def data_sample(n: int = 5) -> dict[str, Any]:
    # Returnerar n exempelrader från CSV:n (bra för validering).
    if n < 1 or n > 100:
        raise HTTPException(status_code=400, detail="n must be between 1 and 100")
    return {"rows": sample_rows(n)}


@app.post("/predict")
def predict(payload: dict[str, Any]) -> dict[str, float]:
    # 1) Ladda artifacts (modell + feature-lista)
    try:
        model, feature_columns = _load_artifacts()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    # 2) Bygg en en-rads DataFrame från inkommande JSON
    #    - Vi fyller None med 0
    #    - Vi reindex:ar så att kolumnerna kommer i exakt samma ordning som vid träning
    try:
        row = {k: (0 if v is None else v) for k, v in payload.items()}
        x = pd.DataFrame([row])
        x = x.reindex(columns=feature_columns, fill_value=0)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid input payload: {exc}") from exc

    # 3) Prediktera och returnera som float (lätt att konsumera i frontend)
    try:
        y = model.predict(x)
        pred = float(y[0])
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc

    return {"predicted_price": pred}


if __name__ == "__main__":
    import uvicorn

    # För lokal utveckling: starta API med auto-reload
    uvicorn.run("taxipred.backend.api:app", host="127.0.0.1", port=8000, reload=True)
