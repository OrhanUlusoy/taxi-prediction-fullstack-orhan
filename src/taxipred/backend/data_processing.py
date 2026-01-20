from __future__ import annotations

"""Datainläsning och små hjälpfunktioner för API:t.

Den här modulen är medvetet enkel:
- `load_raw_data` läser in rå-CSV:n
- `sample_rows` används av /data/sample för att kunna visa exempelrader i frontend

Vi håller den separerad från `api.py` för att API-filen ska vara lätt att läsa i en presentation.
"""

from pathlib import Path

import pandas as pd


def repo_root() -> Path:
    # Hitta repo-rooten robust, oavsett var processen startas ifrån.
    # .../src/taxipred/backend/data_processing.py -> repo root är parents[3]
    return Path(__file__).resolve().parents[3]

# sanity check
def load_raw_data(csv_path: Path | None = None) -> pd.DataFrame:
    # Standard: läs projektets CSV i src/taxipred/data
    if csv_path is None:
        csv_path = repo_root() / "src" / "taxipred" / "data" / "taxi_trip_pricing.csv"
    return pd.read_csv(csv_path)


def sample_rows(n: int = 10) -> list[dict]:
    # Tar ut de första n raderna och returnerar som list[dict] (enkelt att JSON:a)
    df = load_raw_data().head(max(1, n))
    return df.to_dict(orient="records")
