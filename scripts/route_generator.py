import os
import time
import random

import pandas as pd
import requests
from tqdm import tqdm
from dotenv import load_dotenv


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

ORS_API_KEY = os.getenv("ORS_API_KEY")

INPUT_FILE = "dataset/processed/locations_geocoded.csv"
OUTPUT_FILE = "dataset/processed/routes.csv"

# Untuk testing terlebih dahulu
NUMBER_OF_ROUTES = 10

# Profile kendaraan
ORS_PROFILE = "driving-car"

ORS_URL = (
    "https://api.openrouteservice.org/v2/"
    f"directions/{ORS_PROFILE}"
)

HEADERS = {
    "Authorization": ORS_API_KEY,
    "Content-Type": "application/json",
}


# ============================================================
# VALIDASI
# ============================================================

def validate_config():

    if not ORS_API_KEY:
        raise ValueError(
            "ORS_API_KEY belum ditemukan. "
            "Pastikan sudah membuat file .env"
        )


# ============================================================
# LOAD LOCATIONS
# ============================================================

def load_locations():

    df = pd.read_csv(INPUT_FILE)

    required_columns = [
        "id",
        "nama_lokasi",
        "kategori",
        "kecamatan",
        "latitude",
        "longitude",
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Kolom berikut tidak ditemukan: {missing_columns}"
        )

    # ========================================================
    # Pastikan latitude dan longitude benar-benar numerik
    # ========================================================

    df["latitude"] = pd.to_numeric(
        df["latitude"],
        errors="coerce"
    )

    df["longitude"] = pd.to_numeric(
        df["longitude"],
        errors="coerce"
    )

    # Buang lokasi yang tidak mempunyai koordinat valid
    df = df.dropna(
        subset=[
            "latitude",
            "longitude"
        ]
    ).copy()

    print(
        f"Jumlah lokasi valid: {len(df)}"
    )

    return df


# ============================================================
# GENERATE PAIR
# ============================================================

def generate_location_pairs(
    df,
    number_of_routes
):

    pairs = []

    attempts = 0
    max_attempts = number_of_routes * 10

    while len(pairs) < number_of_routes:

        attempts += 1

        if attempts > max_attempts:
            raise RuntimeError(
                "Tidak berhasil mendapatkan "
                "pasangan lokasi yang cukup."
            )

        origin = df.sample(
            n=1
        ).iloc[0]

        destination = df.sample(
            n=1
        ).iloc[0]

        # Origin dan destination tidak boleh sama
        if origin["id"] == destination["id"]:
            continue

        pairs.append(
            {
                "origin": origin,
                "destination": destination,
            }
        )

    return pairs


# ============================================================
# REQUEST ORS
# ============================================================

def get_route(
    origin,
    destination
):

    # ========================================================
    # ORS menggunakan format:
    #
    # [longitude, latitude]
    # ========================================================

    origin_longitude = float(
        origin["longitude"]
    )

    origin_latitude = float(
        origin["latitude"]
    )

    destination_longitude = float(
        destination["longitude"]
    )

    destination_latitude = float(
        destination["latitude"]
    )

    coordinates = [

        [
            origin_longitude,
            origin_latitude
        ],

        [
            destination_longitude,
            destination_latitude
        ]

    ]

    payload = {

        "coordinates": coordinates,

        "instructions": False,

        "elevation": True
    }

    response = requests.post(

        ORS_URL,

        json=payload,

        headers=HEADERS,

        timeout=30
    )

    # Jika HTTP 4xx / 5xx
    response.raise_for_status()

    data = response.json()

    # ========================================================
    # Validasi response ORS
    #
    # ORS yang kamu gunakan sekarang mengembalikan:
    #
    # {
    #     "routes": [...]
    # }
    # ========================================================

    if "routes" not in data:

        print("\nResponse ORS:")

        print(data)

        raise ValueError(
            "Response ORS tidak memiliki 'routes'."
        )

    if not data["routes"]:

        raise ValueError(
            "ORS tidak mengembalikan route."
        )

    return data


# ============================================================
# EXTRACT ROUTE DATA
# ============================================================

def extract_route_data(
    route_data
):

    # ========================================================
    # Ambil route pertama
    # ========================================================

    route = route_data["routes"][0]

    # ========================================================
    # Summary
    # ========================================================

    summary = route["summary"]

    distance_meter = summary["distance"]

    duration_second = summary["duration"]

    # ========================================================
    # Elevation
    #
    # Pada response ORS kamu:
    #
    # summary:
    #     ascent
    #     descent
    #
    # bbox:
    #     [lon, lat, elevation, ...]
    #
    # Kita gunakan ascent sebagai elevation gain.
    # ========================================================

    elevation_gain = summary.get(
        "ascent"
    )

    # ========================================================
    # Ambil minimum dan maksimum elevation
    # dari bbox jika tersedia
    #
    # bbox:
    #
    # [
    #   min_lon,
    #   min_lat,
    #   min_elevation,
    #   max_lon,
    #   max_lat,
    #   max_elevation
    # ]
    # ========================================================

    route_bbox = route.get(
        "bbox"
    )

    if (
        route_bbox
        and len(route_bbox) >= 6
    ):

        min_elevation = route_bbox[2]

        max_elevation = route_bbox[5]

    else:

        min_elevation = None

        max_elevation = None

    # ========================================================
    # RETURN
    # ========================================================

    return {

        "distance_km": round(
            distance_meter / 1000,
            3
        ),

        "duration_min": round(
            duration_second / 60,
            2
        ),

        "elevation_gain_m": round(
            elevation_gain,
            2
        ) if elevation_gain is not None else None,

        "min_elevation_m": round(
            min_elevation,
            2
        ) if min_elevation is not None else None,

        "max_elevation_m": round(
            max_elevation,
            2
        ) if max_elevation is not None else None,
    }


# ============================================================
# MAIN
# ============================================================

def main():

    # ========================================================
    # VALIDASI CONFIG
    # ========================================================

    validate_config()

    # ========================================================
    # LOAD LOCATIONS
    # ========================================================

    df = load_locations()

    # ========================================================
    # GENERATE PAIRS
    # ========================================================

    pairs = generate_location_pairs(
        df,
        NUMBER_OF_ROUTES
    )

    results = []

    print(
        "\nMulai mengambil data rute dari ORS...\n"
    )

    # ========================================================
    # REQUEST ROUTES
    # ========================================================

    for index, pair in enumerate(
        tqdm(pairs),
        start=1
    ):

        origin = pair["origin"]

        destination = pair["destination"]

        try:

            # =================================================
            # Request ORS
            # =================================================

            route_data = get_route(
                origin,
                destination
            )

            # =================================================
            # Extract route information
            # =================================================

            route_info = extract_route_data(
                route_data
            )

            # =================================================
            # Simpan hasil
            # =================================================

            results.append(

                {

                    "route_id": index,

                    "origin_id": origin["id"],

                    "origin_name": origin[
                        "nama_lokasi"
                    ],

                    "origin_kecamatan": origin[
                        "kecamatan"
                    ],

                    "origin_latitude": origin[
                        "latitude"
                    ],

                    "origin_longitude": origin[
                        "longitude"
                    ],

                    "destination_id": destination[
                        "id"
                    ],

                    "destination_name": destination[
                        "nama_lokasi"
                    ],

                    "destination_kecamatan": destination[
                        "kecamatan"
                    ],

                    "destination_latitude": destination[
                        "latitude"
                    ],

                    "destination_longitude": destination[
                        "longitude"
                    ],

                    "distance_km": route_info[
                        "distance_km"
                    ],

                    "duration_min": route_info[
                        "duration_min"
                    ],

                    "elevation_gain_m": route_info[
                        "elevation_gain_m"
                    ],

                    "min_elevation_m": route_info[
                        "min_elevation_m"
                    ],

                    "max_elevation_m": route_info[
                        "max_elevation_m"
                    ],
                }

            )

        # ====================================================
        # HTTP ERROR
        # ====================================================

        except requests.exceptions.HTTPError as e:

            print(
                f"\nGagal route "
                f"{origin['nama_lokasi']} -> "
                f"{destination['nama_lokasi']}"
            )

            print(e)

        # ====================================================
        # ERROR LAIN
        # ====================================================

        except Exception as e:

            print(
                f"\nError: "
                f"{origin['nama_lokasi']} -> "
                f"{destination['nama_lokasi']}"
            )

            print(e)

        # ====================================================
        # Delay
        # ====================================================

        time.sleep(1)

    # ========================================================
    # SAVE
    # ========================================================

    if not results:

        print(
            "\nTidak ada data route "
            "yang berhasil dibuat."
        )

        return

    result_df = pd.DataFrame(
        results
    )

    result_df.to_csv(

        OUTPUT_FILE,

        index=False,

        encoding="utf-8-sig"
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    print(
        "\n======================================"
    )

    print(
        "SELESAI"
    )

    print(
        "======================================"
    )

    print(
        f"Berhasil membuat "
        f"{len(result_df)} route"
    )

    print(
        f"File: {OUTPUT_FILE}"
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()