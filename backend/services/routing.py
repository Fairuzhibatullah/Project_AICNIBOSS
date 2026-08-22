import os

import requests
from dotenv import load_dotenv


# CONFIG

load_dotenv()

ORS_API_KEY = os.getenv("ORS_API_KEY")

ORS_PROFILE = "driving-car"

ORS_URL = (
    "https://api.openrouteservice.org/v2/"
    f"directions/{ORS_PROFILE}"
)

ORS_SNAP_URL = (
    "https://api.openrouteservice.org/v2/"
    f"snap/{ORS_PROFILE}"
)


# HELPER: DECODE POLYLINE

def decode_polyline(polyline_str, is3d=True):
    """
    Decodes an encoded polyline string (Google Polyline Algorithm) into a list of coordinates.
    Returns: [[longitude, latitude], [longitude, latitude], ...]
    """
    index = 0
    length = len(polyline_str)
    coords = []
    lat = 0
    lon = 0
    
    while index < length:
        # Decode Latitude
        shift = 0
        result = 0
        while True:
            if index >= length:
                break
            b = ord(polyline_str[index]) - 63
            index += 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break
        lat += ~(result >> 1) if (result & 1) else (result >> 1)
        
        # Decode Longitude
        shift = 0
        result = 0
        while True:
            if index >= length:
                break
            b = ord(polyline_str[index]) - 63
            index += 1
            result |= (b & 0x1f) << shift
            shift += 5
            if b < 0x20:
                break
        lon += ~(result >> 1) if (result & 1) else (result >> 1)
        
        if is3d:
            # Decode Elevation
            shift = 0
            result = 0
            while True:
                if index >= length:
                    break
                b = ord(polyline_str[index]) - 63
                index += 1
                result |= (b & 0x1f) << shift
                shift += 5
                if b < 0x20:
                    break
                    
        coords.append([round(lon * 1e-5, 5), round(lat * 1e-5, 5)])
        
    return coords


# HELPER: RESOLVE ROUTABLE POINT

def resolve_routable_point(lat, lon, radius=10000):
    """
    Mencari titik terdekat di jaringan jalan yang routable menggunakan ORS Snap API.
    Radius diset cukup besar agar selalu menemukan titik jalan terdekat.
    """
    if not ORS_API_KEY:
        raise ValueError("ORS_API_KEY belum tersedia.")

    if lat is None or lon is None:
        raise ValueError("Latitude atau longitude tidak valid.")

    # ORS menggunakan format: [longitude, latitude]
    payload = {
        "locations": [
            [float(lon), float(lat)]
        ],
        "radius": radius
    }

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            ORS_SNAP_URL,
            json=payload,
            headers=headers,
            timeout=15
        )
        response.raise_for_status()
        data = response.json()
        
        if "locations" in data and data["locations"]:
            location = data["locations"][0].get("location")
            if location and len(location) == 2:
                # return (latitude, longitude)
                return float(location[1]), float(location[0])
                
        raise ValueError("Response ORS Snap tidak memiliki lokasi yang valid.")
    except Exception as e:
        error_msg = str(e)
        if hasattr(e, 'response') and e.response is not None:
            # e.response.text biasanya hanya JSON dari ORS
            error_msg = f"HTTP {e.response.status_code} - {e.response.text}"
        raise ValueError(f"Tidak menemukan titik routable untuk ({lat}, {lon}). Error ORS: {error_msg}")


def get_route(
    origin_lat,
    origin_lon,
    destination_lat,
    destination_lon
):

    if not ORS_API_KEY:
        raise ValueError(
            "ORS_API_KEY belum tersedia."
        )

    # Resolve origin dan destination
    resolved_origin_lat, resolved_origin_lon = resolve_routable_point(origin_lat, origin_lon)
    resolved_dest_lat, resolved_dest_lon = resolve_routable_point(destination_lat, destination_lon)

    # Koordinat routing: [longitude, latitude]
    coordinates = [
        [
            float(resolved_origin_lon),
            float(resolved_origin_lat)
        ],
        [
            float(resolved_dest_lon),
            float(resolved_dest_lat)
        ]
    ]

    payload = {
        "coordinates": coordinates,
        "instructions": False,
        "elevation": True,
        "geometry": True
    }

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(
        ORS_URL,
        json=payload,
        headers=headers,
        timeout=30
    )

    if response.status_code != 200:
        error_msg = response.text
        raise ValueError(f"Gagal mengambil rute dari ORS. HTTP {response.status_code}: {error_msg}")

    data = response.json()

    if "routes" not in data or not data["routes"]:
        raise ValueError(
            "Response ORS tidak memiliki 'routes' atau kosong."
        )

    route = data["routes"][0]
    
    if "summary" not in route:
        raise ValueError("Response ORS tidak memiliki 'summary'.")
        
    if "geometry" not in route:
        raise ValueError("Response ORS tidak memiliki 'geometry'.")

    summary = route["summary"]
    encoded_geom = route["geometry"]
    
    # Decode polyline
    decoded_geom = decode_polyline(encoded_geom, is3d=True)

    distance_km = summary.get("distance", 0) / 1000
    duration_min = summary.get("duration", 0) / 60

    return {
        "distance_km": round(distance_km, 3),
        "duration_min": round(duration_min, 2),
        "geometry": decoded_geom
    }