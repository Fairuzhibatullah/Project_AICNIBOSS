import requests


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def geocode_location(location: str):
    params = {
        "q": location,
        "format": "json",
        "limit": 1,
        "countrycodes": "id"
    }

    headers = {
        "User-Agent": "AICNIBOSS/1.0"
    }

    response = requests.get(
        NOMINATIM_URL,
        params=params,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        raise ValueError(
            f"Lokasi tidak ditemukan: {location}"
        )

    return {
        "latitude": float(data[0]["lat"]),
        "longitude": float(data[0]["lon"]),
        "display_name": data[0]["display_name"]
    }