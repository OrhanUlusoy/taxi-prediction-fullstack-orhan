# Taxi Prediction (Fullstack Lab)

End-to-end lab project: train a taxi price model, export artifacts, serve predictions via a backend API, and consume the API from a simple frontend UI.

## Architecture

- **Model development**: Jupyter notebook(s) under `src/taxipred/model_development/`
- **Model artifacts**: exported to repo root
  - `linear_regression_model.pkl`
  - `model_features.pkl`
- **Backend (FastAPI)**: `src/taxipred/backend/api.py`
- **Frontend (Streamlit)**: `src/taxipred/frontend/app.py`

## Setup (recommended: uv)

From the repo root:

- Install dependencies + create/refresh `.venv`:
  - `uv sync`

Notes:
- This repo contains `requirements.txt`, but the primary workflow here is `uv` (via `pyproject.toml` + `uv.lock`).
- In VS Code notebooks, choose the kernel that points to `taxi-prediction-fullstack-orhan\.venv\Scripts\python.exe`.

## Run backend (FastAPI)

- Start API (Windows-friendly):
  - `.\.venv\Scripts\python.exe -m uvicorn taxipred.backend.api:app --app-dir src --host 127.0.0.1 --port 8001`

Endpoints:
- `GET /health` → `{ "status": "ok" }`
- `GET /data/sample?n=5` → returns a few rows from the CSV
- `POST /predict` → returns `{ "predicted_price": <float> }`

Example request:

```bash
curl -X POST http://127.0.0.1:8001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Trip_Distance_km": 10,
    "Passenger_Count": 2,
    "Base_Fare": 3,
    "Per_Km_Rate": 1.2,
    "Per_Minute_Rate": 0.3,
    "Trip_Duration_Minutes": 20,
    "Time_of_Day_Afternoon": 1,
    "Day_of_Week_Weekend": 0,
    "Traffic_Conditions_Medium": 1,
    "Weather_Clear": 1
  }'
```

## Run frontend (Streamlit)

Start the UI:

```bash
.\.venv\Scripts\python.exe -m streamlit run src/taxipred/frontend/app.py
```

The frontend calls the backend at `http://127.0.0.1:8000` by default.
If you want to point it somewhere else:

```bash
set TAXIPRED_API_BASE=http://127.0.0.1:8001
.\.venv\Scripts\python.exe -m streamlit run src/taxipred/frontend/app.py
```

## Run notebooks

- Open `src/taxipred/model_development/01_eda.ipynb`
- Select the kernel from `.venv`

If you ever get `ModuleNotFoundError`, it usually means the notebook is using the wrong interpreter.


### Backend running

![Backend running in terminal (Uvicorn on http://127.0.0.1:8001)](docs/screenshots/image-3.png)

Note: `GET /favicon.ico 404` in the terminal is normal (browser requesting an icon).

### Backend health

![Health check in browser: GET /health returns {"status":"ok"}](docs/screenshots/image-1.png)

### Frontend Running
![Streamlit started (Local URL http://localhost:8501)](docs/screenshots/image-2.png)

### Frontend prediction

![Streamlit UI: backend reachable and a successful prediction](docs/screenshots/image.png)