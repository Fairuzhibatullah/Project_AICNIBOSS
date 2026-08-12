import time
import requests
import pandas as pd
from tqdm import tqdm

# ============================================================
# CONFIG
# ============================================================

INPUT_FILE = "dataset/processed/routes.csv"
OUTPUT_FILE = "dataset/processed/routes_weather.csv"

# ============================================================
# OPEN-METEO
# ============================================================

def get_weather(latitude, longitude):
    """
    Mengambil cuaca saat ini dari Open-Meteo
    """

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "rain"
        ]
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    current = data.get("current", {})

    return {
        "temperature_c": current.get("temperature_2m"),
        "humidity_percent": current.get("relative_humidity_2m"),
        "rain_mm": current.get("rain")
    }

# ============================================================
# MAIN
# ============================================================

def main():

    df = pd.read_csv(INPUT_FILE)

    temperatures = []
    humidities = []
    rains = []

    print("Mengambil data cuaca dari Open-Meteo...")

    for _, row in tqdm(df.iterrows(), total=len(df)):

        lat = row["origin_latitude"]
        lon = row["origin_longitude"]

        try:

            weather = get_weather(lat, lon)

            temperatures.append(weather["temperature_c"])
            humidities.append(weather["humidity_percent"])
            rains.append(weather["rain_mm"])

        except Exception as e:

            print(f"Gagal mengambil cuaca: {row['origin_name']}")
            print(e)

            temperatures.append(None)
            humidities.append(None)
            rains.append(None)

        # Jeda agar tidak terlalu agresif
        time.sleep(0.2)

    df["temperature_c"] = temperatures
    df["humidity_percent"] = humidities
    df["rain_mm"] = rains

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nSelesai!")
    print(f"File disimpan: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()