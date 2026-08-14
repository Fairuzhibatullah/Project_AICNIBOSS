from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
    cc: float
    weight_kg: float
    fuel_type: str

    # Kondisi pengendara
    riding_style: str
    avg_speed_kmh: float
    rider_weight: float
    city_percentage: float

    # Harga BBM
    fuel_price_per_liter: float


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

    try:

        # ----------------------------------------------------
        # 1. GEOCODING
        # ----------------------------------------------------

        print("Mencari lokasi origin...")

        origin = geocode_location(request.origin)

        print("Origin:", origin)

        print("Mencari lokasi destination...")

        destination = geocode_location(request.destination)

        print("Destination:", destination)

        if not origin or not destination:
            raise HTTPException(
                status_code=400,
                detail="Lokasi origin atau destination tidak ditemukan."
            )


        # ----------------------------------------------------
        # 2. ROUTING
        # ----------------------------------------------------

        print("Mengambil data rute...")

        route = get_route(
            origin["latitude"],
            origin["longitude"],
            destination["latitude"],
            destination["longitude"]
        )

        print("Route:", route)


        # ----------------------------------------------------
        # 3. WEATHER
        # ----------------------------------------------------

        print("Mengambil data cuaca...")

        weather = get_weather(
            destination["latitude"],
            destination["longitude"]
        )

        print("Weather:", weather)


        # ----------------------------------------------------
        # 4. DATA UNTUK MODEL
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

                # Sementara menggunakan ID dummy.
                # Nanti dapat dihubungkan dengan dataset lokasi.
                "route_id": 0,
                "origin_id": 0,
                "destination_id": 0,

                "distance_km": route["distance_km"],
                "duration_min": route["duration_min"],

                # Jika routing service belum menyediakan elevasi,
                # gunakan nilai default terlebih dahulu.
                "elevation_gain_m": 0,
                "min_elevation_m": 0,
                "max_elevation_m": 0,

                "temperature_c": weather["temperature_c"],
                "humidity_percent": weather["humidity_percent"],
                "rain_mm": weather["rain_mm"]
            }
        ])


        # ----------------------------------------------------
        # 5. PREDIKSI BBM
        # ----------------------------------------------------

        print("Melakukan prediksi konsumsi BBM...")

        prediction = model.predict(input_data)

        fuel_consumption = float(prediction[0])

        fuel_consumption = round(
            fuel_consumption,
            2
        )


        # ----------------------------------------------------
        # 6. HITUNG KEBUTUHAN BBM
        # ----------------------------------------------------

        distance_km = route["distance_km"]

        if fuel_consumption <= 0:
            raise ValueError(
                "Hasil prediksi konsumsi BBM tidak valid."
            )

        fuel_needed = distance_km / fuel_consumption

        fuel_needed = round(
            fuel_needed,
            2
        )


        # ----------------------------------------------------
        # 7. HITUNG BIAYA
        # ----------------------------------------------------

        estimated_cost = fuel_needed * request.fuel_price_per_liter

        estimated_cost = round(
            estimated_cost
        )


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


    except HTTPException:
        raise

    except Exception as e:

        print("ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )