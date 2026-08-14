import requests


OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,rain",
        "timezone": "Asia/Jakarta"
    }

    response = requests.get(
        OPEN_METEO_URL,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    current = data.get("current")

    if not current:
        raise ValueError("Data cuaca tidak tersedia.")

    temperature_c = current.get("temperature_2m")
    humidity_percent = current.get("relative_humidity_2m")
    rain_mm = current.get("rain")

    if (
        temperature_c is None
        or humidity_percent is None
        or rain_mm is None
    ):
        raise ValueError("Data cuaca tidak lengkap.")

    return {
        "temperature_c": float(temperature_c),
        "humidity_percent": float(humidity_percent),
        "rain_mm": float(rain_mm)
    }