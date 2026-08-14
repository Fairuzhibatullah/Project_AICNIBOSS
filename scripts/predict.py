import pandas as pd
import joblib
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = BASE_DIR / "models" / "fuel_consumption_model.pkl"

# ============================================================
# LOAD MODEL
# ============================================================

print("Memuat model...")

model = joblib.load(MODEL_FILE)

print("Model berhasil dimuat.")

# ============================================================
# INPUT DATA
# ============================================================

input_data = pd.DataFrame([{
    "brand": "Honda",
    "model": "PCX160",
    "cc": 160,
    "weight_kg": 132,
    "fuel_type": "Pertamax",

    "riding_style": "Normal",
    "avg_speed_kmh": 45,
    "rider_weight": 70,
    "city_percentage": 70,

    "distance_km": 5.5,
    "duration_min": 10.8,
    "elevation_gain_m": 100,
    "min_elevation_m": 230,
    "max_elevation_m": 290,

    "route_id": 1,
    "origin_id": 80,
    "destination_id": 99,
    
    "temperature_c": 33.4,
    "humidity_percent": 70,
    "rain_mm": 0.0
}])

# ============================================================
# PREDICTION
# ============================================================

print("\n Melakukan prediksi konsumsi BBM...")

prediction = model.predict(input_data)

fuel_consumption = prediction[0]

# ============================================================
# HASIL
# ============================================================

print("\n" + "=" * 60)
print(" HASIL PREDIKSI KONSUMSI BBM")
print("=" * 60)

print(f"Prediksi konsumsi : {fuel_consumption:.2f} km/L")

print("=" * 60)