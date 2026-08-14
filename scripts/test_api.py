import requests

# ============================================================
# CONFIG
# ============================================================

API_URL = "http://127.0.0.1:8000/predict"


# ============================================================
# DATA TEST
# ============================================================

payload = {
    "origin": "Stasiun Bogor",
    "destination": "Kebun Raya Bogor",

    "brand": "Honda",
    "model": "Vario 125",
    "cc": 125,
    "weight_kg": 112,
    "fuel_type": "Pertalite",

    "riding_style": "Normal",
    "avg_speed_kmh": 40,
    "rider_weight": 70,
    "city_percentage": 80,

    "fuel_price_per_liter": 10000
}


# ============================================================
# REQUEST
# ============================================================

print("Mengirim request ke API...")
print()

try:

    response = requests.post(
        API_URL,
        json=payload,
        timeout=60
    )

    print("Status code:", response.status_code)
    print()

    # ========================================================
    # RESPONSE BERHASIL
    # ========================================================

    if response.status_code == 200:

        result = response.json()

        print("API berhasil dipanggil.")
        print()
        print("Hasil prediksi:")
        print("----------------------------------------")

        print(
            "Jarak:",
            result["route"]["distance_km"],
            "km"
        )

        print(
            "Durasi:",
            result["route"]["duration_min"],
            "menit"
        )

        print(
            "Suhu:",
            result["weather"]["temperature_c"],
            "°C"
        )

        print(
            "Kelembapan:",
            result["weather"]["humidity_percent"],
            "%"
        )

        print(
            "Hujan:",
            result["weather"]["rain_mm"],
            "mm"
        )

        print(
            "Prediksi konsumsi:",
            result["prediction"]["fuel_consumption_kml"],
            "km/L"
        )

        print(
            "Kebutuhan BBM:",
            result["fuel"]["fuel_needed_liter"],
            "liter"
        )

        print(
            "Harga BBM:",
            result["fuel"]["fuel_price_per_liter"]
        )

        print(
            "Estimasi biaya:",
            result["cost"]["estimated_cost"]
        )

        print("----------------------------------------")
        print()
        print("TEST API BERHASIL.")

    else:

        print("API mengembalikan error.")
        print(response.text)


except requests.exceptions.ConnectionError:

    print("Tidak dapat terhubung ke API.")
    print()
    print("Pastikan backend sedang berjalan:")
    print(
        "/c/Users/faiza/AppData/Local/Python/"
        "pythoncore-3.14-64/python.exe "
        "-m uvicorn backend.app:app --reload"
    )


except requests.exceptions.Timeout:

    print("Request terlalu lama dan timeout.")


except Exception as e:

    print("Terjadi error:")
    print(e)