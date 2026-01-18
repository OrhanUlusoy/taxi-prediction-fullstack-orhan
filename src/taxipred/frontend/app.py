from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st


def _api_base() -> str:
    return os.environ.get("TAXIPRED_API_BASE", "http://127.0.0.1:8000")


st.set_page_config(page_title="Taxi Price Prediction", layout="centered")
st.title("Taxi Price Prediction")
st.caption("Frontend (Streamlit) that calls the FastAPI backend")

with st.sidebar:
    st.subheader("API")
    api = st.text_input(
        "API base URL",
        value=_api_base(),
        help="Base URL to the FastAPI backend, e.g. http://127.0.0.1:8001",
    ).rstrip("/")
    st.write(api)

    try:
        health = requests.get(f"{api}/health", timeout=1.5)
        if health.ok:
            st.success("Backend reachable (/health OK)")
        else:
            st.warning(f"Backend responded with {health.status_code}")
    except Exception:
        st.error("Backend NOT reachable (start API or fix URL/port)")

st.subheader("Input features")

trip_distance_km = st.number_input("Trip_Distance_km", min_value=0.0, value=10.0, step=0.1)
passenger_count = st.number_input("Passenger_Count", min_value=1, value=2, step=1)
base_fare = st.number_input("Base_Fare", min_value=0.0, value=3.0, step=0.1)
per_km_rate = st.number_input("Per_Km_Rate", min_value=0.0, value=1.2, step=0.1)
per_minute_rate = st.number_input("Per_Minute_Rate", min_value=0.0, value=0.3, step=0.05)
trip_duration_minutes = st.number_input("Trip_Duration_Minutes", min_value=0.0, value=20.0, step=1.0)

# Simple one-hot-ish flags (match your notebook example)
time_of_day_afternoon = st.selectbox("Time_of_Day_Afternoon", [0, 1], index=1)
day_of_week_weekend = st.selectbox("Day_of_Week_Weekend", [0, 1], index=0)
traffic_conditions_medium = st.selectbox("Traffic_Conditions_Medium", [0, 1], index=1)
weather_clear = st.selectbox("Weather_Clear", [0, 1], index=1)

payload: dict[str, Any] = {
    "Trip_Distance_km": trip_distance_km,
    "Passenger_Count": passenger_count,
    "Base_Fare": base_fare,
    "Per_Km_Rate": per_km_rate,
    "Per_Minute_Rate": per_minute_rate,
    "Trip_Duration_Minutes": trip_duration_minutes,
    "Time_of_Day_Afternoon": time_of_day_afternoon,
    "Day_of_Week_Weekend": day_of_week_weekend,
    "Traffic_Conditions_Medium": traffic_conditions_medium,
    "Weather_Clear": weather_clear,
}

if st.button("Predict"):
    try:
        resp = requests.post(f"{api}/predict", json=payload, timeout=10)
        resp.raise_for_status()
        predicted = resp.json()["predicted_price"]
        st.success(f"Predicted price: {predicted:.2f}")
    except Exception as exc:
        st.error(f"Prediction failed: {exc}")

st.divider()

with st.expander("Try backend sample data"):
    if st.button("Fetch /data/sample"):
        try:
            resp = requests.get(f"{api}/data/sample?n=5", timeout=10)
            resp.raise_for_status()
            st.json(resp.json())
        except Exception as exc:
            st.error(f"Fetch failed: {exc}")
