from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.services.geocoding import geocode_location
from backend.services.routing import get_route
from backend.services.weather import get_weather


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = BASE_DIR / "models" / "fuel_consumption_model.pkl"


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="AIC NIBOSS API",
    description="API prediksi konsumsi BBM motor berdasarkan rute dan kondisi perjalanan.",
    version="1.0.0"
)


# ============================================================
# LOAD MODEL
# ============================================================

print("Memuat model...")

if not MODEL_FILE.exists():
    raise FileNotFoundError(
        f"Model tidak ditemukan: {MODEL_FILE}"
    )

model = joblib.load(MODEL_FILE)

print("Model berhasil dimuat.")


# ============================================================
# REQUEST SCHEMA
# ============================================================

class PredictionRequest(BaseModel):

    # Lokasi
    origin: str
    destination: str

    # Kendaraan
    brand: str
    model: str
    cc: float = Field(gt=0, description="Kapasitas mesin dalam cc")
    weight_kg: float = Field(gt=0, description="Berat kendaraan dalam kg")
    fuel_type: str

    # Kondisi pengendara
    riding_style: str
    avg_speed_kmh: float = Field(gt=0, description="Kecepatan rata-rata dalam km/jam")
    rider_weight: float = Field(gt=0, description="Berat pengendara dalam kg")
    city_percentage: float = Field(ge=0, le=100, description="Persentase kondisi dalam kota (0-100)")

    # Harga BBM
    fuel_price_per_liter: float = Field(gt=0, description="Harga BBM per liter")


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "AIC NIBOSS API aktif",
        "status": "running"
    }


# ============================================================
# PREDICTION
# ============================================================

@app.post("/predict")
def predict(request: PredictionRequest):

    # Validasi input lokasi
    if not request.origin.strip() or not request.destination.strip():
        raise HTTPException(
            status_code=400,
            detail="Lokasi origin dan destination tidak boleh kosong."
        )

    # ----------------------------------------------------
    # 1. GEOCODING
    # ----------------------------------------------------
    try:
        print("Mencari lokasi origin:", request.origin)
        origin = geocode_location(request.origin)
        print("Origin:", origin)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Geocoding origin gagal: {str(e)}"
        )

    try:
        print("Mencari lokasi destination:", request.destination)
        destination = geocode_location(request.destination)
        print("Destination:", destination)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Geocoding destination gagal: {str(e)}"
        )

    if not origin or not destination:
        raise HTTPException(
            status_code=400,
            detail="Lokasi origin atau destination tidak ditemukan."
        )

    # ----------------------------------------------------
    # 2. ROUTING
    # ----------------------------------------------------
    try:
        print("Mengambil data rute...")
        route = get_route(
            origin["latitude"],
            origin["longitude"],
            destination["latitude"],
            destination["longitude"]
        )
        print("Route:", route)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Routing rute gagal: {str(e)}"
        )

    if route.get("distance_km", 0) <= 0:
        raise HTTPException(
            status_code=400,
            detail="Jarak rute tidak valid (jarak <= 0 km)."
        )

    # ----------------------------------------------------
    # 3. WEATHER
    # ----------------------------------------------------
    try:
        print("Mengambil data cuaca...")
        weather = get_weather(
            destination["latitude"],
            destination["longitude"]
        )
        print("Weather:", weather)
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Pengambilan data cuaca gagal: {str(e)}"
        )

    # ----------------------------------------------------
    # 4. DATA UNTUK MODEL (HANYA 14 FITUR VALID)
    # ----------------------------------------------------
    input_data = pd.DataFrame([
        {
            "brand": request.brand,
            "model": request.model,
            "cc": request.cc,
            "weight_kg": request.weight_kg,
            "fuel_type": request.fuel_type,

            "riding_style": request.riding_style,
            "avg_speed_kmh": request.avg_speed_kmh,
            "rider_weight": request.rider_weight,
            "city_percentage": request.city_percentage,

            "distance_km": route["distance_km"],
            "duration_min": route["duration_min"],

            "temperature_c": weather["temperature_c"],
            "humidity_percent": weather["humidity_percent"],
            "rain_mm": weather["rain_mm"]
        }
    ])

    # ----------------------------------------------------
    # 5. PREDIKSI BBM
    # ----------------------------------------------------
    try:
        print("Melakukan prediksi konsumsi BBM...")
        prediction = model.predict(input_data)
        fuel_consumption = float(prediction[0])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediksi model gagal: {str(e)}"
        )

    if fuel_consumption <= 0:
        raise HTTPException(
            status_code=500,
            detail="Hasil prediksi konsumsi BBM tidak valid (<= 0 km/L)."
        )

    fuel_consumption = round(fuel_consumption, 2)

    # ----------------------------------------------------
    # 6. HITUNG KEBUTUHAN BBM
    # ----------------------------------------------------
    distance_km = route["distance_km"]
    fuel_needed = round(distance_km / fuel_consumption, 2)

    # ----------------------------------------------------
    # 7. HITUNG BIAYA
    # ----------------------------------------------------
    estimated_cost = round(fuel_needed * request.fuel_price_per_liter)

    # ----------------------------------------------------
    # 8. RESPONSE
    # ----------------------------------------------------
    return {
        "origin": {
            "name": request.origin,
            "latitude": origin["latitude"],
            "longitude": origin["longitude"]
        },
        "destination": {
            "name": request.destination,
            "latitude": destination["latitude"],
            "longitude": destination["longitude"]
        },
        "route": {
            "distance_km": distance_km,
            "duration_min": route["duration_min"]
        },
        "weather": {
            "temperature_c": weather["temperature_c"],
            "humidity_percent": weather["humidity_percent"],
            "rain_mm": weather["rain_mm"]
        },
        "prediction": {
            "fuel_consumption_kml": fuel_consumption
        },
        "fuel": {
            "fuel_needed_liter": fuel_needed,
            "fuel_price_per_liter": request.fuel_price_per_liter
        },
        "cost": {
            "estimated_cost": estimated_cost
        }
    }