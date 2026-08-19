import os
import requests


ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"


def get_route(
    origin_lat,
    origin_lon,
    destination_lat,
    destination_lon
):
    api_key = os.getenv("ORS_API_KEY")

    if not api_key:
        raise ValueError("ORS_API_KEY belum tersedia.")

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    body = {
        "coordinates": [
            [origin_lon, origin_lat],
            [destination_lon, destination_lat]
        ]
    }

    response = requests.post(
        ORS_URL,
        headers=headers,
        json=body,
        timeout=30
    )

    print("ORS status:", response.status_code)

    if response.status_code != 200:
        print("ORS response:", response.text)

    response.raise_for_status()

    data = response.json()

    if "routes" not in data or not data["routes"]:
        raise ValueError("ORS tidak mengembalikan data rute.")

    route = data["routes"][0]

    distance_km = route["summary"]["distance"] / 1000
    duration_min = route["summary"]["duration"] / 60

    return {
        "distance_km": round(distance_km, 3),
        "duration_min": round(duration_min, 2)
    }