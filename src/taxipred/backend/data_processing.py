from __future__ import annotations

from pathlib import Path

import pandas as pd


def repo_root() -> Path:
    # .../src/taxipred/backend/data_processing.py -> repo root is parents[3]
    return Path(__file__).resolve().parents[3]


def load_raw_data(csv_path: Path | None = None) -> pd.DataFrame:
    if csv_path is None:
        csv_path = repo_root() / "src" / "taxipred" / "data" / "taxi_trip_pricing.csv"
    return pd.read_csv(csv_path)


def sample_rows(n: int = 10) -> list[dict]:
    df = load_raw_data().head(max(1, n))
    return df.to_dict(orient="records")
