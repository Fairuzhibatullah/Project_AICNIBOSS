import requests


OSRM_URL = "https://router.project-osrm.org/route/v1/driving"


def get_route(
    origin_lat,
    origin_lon,
    destination_lat,
    destination_lon
):
    url = (
        f"{OSRM_URL}/"
        f"{origin_lon},{origin_lat};"
        f"{destination_lon},{destination_lat}"
    )

    params = {
        "overview": "false",
        "steps": "false"
    }

    response = requests.get(
        url,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    if data.get("code") != "Ok":
        raise ValueError("Routing gagal.")

    route = data["routes"][0]

    distance_km = route["distance"] / 1000
    duration_min = route["duration"] / 60

    return {
        "distance_km": round(distance_km, 3),
        "duration_min": round(duration_min, 2)
    }