import joblib
import pandas as pd
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = BASE_DIR / "models" / "fuel_consumption_model.pkl"

# Harga BBM per liter
FUEL_PRICE = 10000


# ============================================================
# LOAD MODEL
# ============================================================

print("Memuat model...")

model = joblib.load(MODEL_FILE)

print("Model berhasil dimuat.")


# ============================================================
# INPUT DATA
# ============================================================

print("\nMenyiapkan data kendaraan, rute, dan cuaca...")

input_data = pd.DataFrame([{
    # Kendaraan
    "brand": "Honda",
    "model": "Vario 125",
    "cc": 125,
    "weight_kg": 112,
    "fuel_type": "Pertalite",

    # Kondisi pengendara
    "riding_style": "Normal",
    "avg_speed_kmh": 45,
    "rider_weight": 70,
    "city_percentage": 70,

    # Rute
    "route_id": 1,
    "origin_id": 80,
    "destination_id": 99,
    "distance_km": 5.5,
    "duration_min": 10,
    "elevation_gain_m": 100,
    "min_elevation_m": 200,
    "max_elevation_m": 300,

    # Cuaca
    "temperature_c": 33.4,
    "humidity_percent": 35,
    "rain_mm": 0
}])


# ============================================================
# PREDICTION
# ============================================================

print("\nMelakukan prediksi konsumsi BBM...")

prediction = model.predict(input_data)

fuel_consumption = float(prediction[0])

print(f"Prediksi konsumsi : {fuel_consumption:.2f} km/L")


# ============================================================
# FUEL REQUIREMENT
# ============================================================

distance_km = float(input_data["distance_km"].iloc[0])

fuel_needed = distance_km / fuel_consumption


# ============================================================
# ESTIMATED COST
# ============================================================

estimated_cost = fuel_needed * FUEL_PRICE


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("=" * 60)
print("HASIL PREDIKSI DAN ESTIMASI BBM")
print("=" * 60)

print(f"Jarak rute          : {distance_km:.2f} km")
print(f"Konsumsi BBM        : {fuel_consumption:.2f} km/L")
print(f"Kebutuhan BBM       : {fuel_needed:.3f} liter")
print(f"Harga BBM           : Rp{FUEL_PRICE:,.0f}/liter")
print(f"Estimasi biaya      : Rp{estimated_cost:,.0f}")

print("=" * 60)