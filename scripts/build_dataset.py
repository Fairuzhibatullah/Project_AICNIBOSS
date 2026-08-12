import pandas as pd
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FUEL_FILE = BASE_DIR / "dataset" / "processed" / "fuel_training.csv"
ROUTE_FILE = BASE_DIR / "dataset" / "processed" / "routes_weather.csv"
OUTPUT_FILE = BASE_DIR / "dataset" / "processed" / "training_dataset.csv"

# ============================================================
# LOAD DATA
# ============================================================

print("📥 Membaca dataset...")

fuel_df = pd.read_csv(FUEL_FILE)
route_df = pd.read_csv(ROUTE_FILE)

print(f"Fuel training : {len(fuel_df)} baris")
print(f"Routes weather: {len(route_df)} baris")

if len(fuel_df) == 0:
    raise ValueError("fuel_training.csv kosong.")

if len(route_df) == 0:
    raise ValueError("routes_weather.csv kosong.")

# ============================================================
# VALIDASI KOLOM
# ============================================================

required_fuel_columns = [
    "training_id",
    "brand",
    "model",
    "cc",
    "weight_kg",
    "fuel_type",
    "riding_style",
    "avg_speed_kmh",
    "rider_weight",
    "city_percentage",
    "fuel_consumption_kml"
]

required_route_columns = [
    "route_id",
    "origin_id",
    "destination_id",
    "distance_km",
    "duration_min",
    "elevation_gain_m",
    "min_elevation_m",
    "max_elevation_m",
    "temperature_c",
    "humidity_percent",
    "rain_mm"
]

missing_fuel = [
    col for col in required_fuel_columns
    if col not in fuel_df.columns
]

missing_route = [
    col for col in required_route_columns
    if col not in route_df.columns
]

if missing_fuel:
    raise ValueError(
        f"Kolom fuel_training.csv tidak ditemukan: {missing_fuel}"
    )

if missing_route:
    raise ValueError(
        f"Kolom routes_weather.csv tidak ditemukan: {missing_route}"
    )

# ============================================================
# PASTIKAN DATA NUMERIK
# ============================================================

print("🔢 Memastikan kolom numerik menggunakan titik desimal...")

fuel_numeric = [
    "training_id",
    "cc",
    "weight_kg",
    "avg_speed_kmh",
    "rider_weight",
    "city_percentage",
    "fuel_consumption_kml"
]

route_numeric = [
    "route_id",
    "origin_id",
    "destination_id",
    "distance_km",
    "duration_min",
    "elevation_gain_m",
    "min_elevation_m",
    "max_elevation_m",
    "temperature_c",
    "humidity_percent",
    "rain_mm"
]

for col in fuel_numeric:
    fuel_df[col] = (
        fuel_df[col]
        .astype(str)
        .str.strip()
        .str.replace(",", ".", regex=False)
    )

    fuel_df[col] = pd.to_numeric(
        fuel_df[col],
        errors="coerce"
    )

for col in route_numeric:
    route_df[col] = pd.to_numeric(
        route_df[col],
        errors="coerce"
    )

# ============================================================
# CEK DATA SEBELUM DIGABUNGKAN
# ============================================================

print("\n🔍 Mengecek missing value...")

fuel_missing = fuel_df[required_fuel_columns].isna().sum()
route_missing = route_df[required_route_columns].isna().sum()

print("\nFuel training:")
print(fuel_missing[fuel_missing > 0])

print("\nRoutes weather:")
print(route_missing[route_missing > 0])

if fuel_df[required_fuel_columns].isna().any().any():
    raise ValueError(
        "fuel_training.csv memiliki nilai kosong/invalid."
    )

if route_df[required_route_columns].isna().any().any():
    raise ValueError(
        "routes_weather.csv memiliki nilai kosong/invalid."
    )

# ============================================================
# MEMASANGKAN VEHICLE DENGAN ROUTE
# ============================================================

print("\n🔗 Menggabungkan data kendaraan dengan rute/cuaca...")

fuel_df = fuel_df.reset_index(drop=True)
route_df = route_df.reset_index(drop=True)

# Setiap kendaraan mendapat route secara berulang:
#
# training 1  -> route 1
# training 2  -> route 2
# ...
# training 10 -> route 10
# training 11 -> route 1
# training 12 -> route 2
# dst.

fuel_df["route_index"] = fuel_df.index % len(route_df)

route_features = route_df[
    [
        "route_id",
        "origin_id",
        "destination_id",
        "distance_km",
        "duration_min",
        "elevation_gain_m",
        "min_elevation_m",
        "max_elevation_m",
        "temperature_c",
        "humidity_percent",
        "rain_mm"
    ]
].copy()

route_features["route_index"] = route_features.index

# ============================================================
# MERGE
# ============================================================

training_df = fuel_df.merge(
    route_features,
    on="route_index",
    how="left"
)

# ============================================================
# VALIDASI HASIL MERGE
# ============================================================

print(f"\n📊 Jumlah data setelah merge: {len(training_df)}")

if len(training_df) != len(fuel_df):
    raise ValueError(
        "Jumlah data berubah setelah merge!"
    )

# ============================================================
# PILIH FITUR FINAL
# ============================================================

final_columns = [
    "training_id",

    # Kendaraan
    "brand",
    "model",
    "cc",
    "weight_kg",
    "fuel_type",

    # Kondisi pengendara
    "riding_style",
    "avg_speed_kmh",
    "rider_weight",
    "city_percentage",

    # Rute
    "route_id",
    "origin_id",
    "destination_id",
    "distance_km",
    "duration_min",
    "elevation_gain_m",
    "min_elevation_m",
    "max_elevation_m",

    # Cuaca
    "temperature_c",
    "humidity_percent",
    "rain_mm",

    # Target AI
    "fuel_consumption_kml"
]

training_df = training_df[final_columns]

# ============================================================
# FINAL CHECK
# ============================================================

print("\n🔍 Final checking...")

missing_final = training_df.isna().sum()

if missing_final.sum() > 0:
    print("\n❌ Ditemukan missing value:")
    print(missing_final[missing_final > 0])

    raise ValueError(
        "Dataset belum aman disimpan karena terdapat missing value."
    )

# ============================================================
# SAVE
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

training_df.to_csv(
    OUTPUT_FILE,
    index=False,
    decimal="."
)

# ============================================================
# INFO
# ============================================================

print("\n" + "=" * 60)
print("✅ DATASET BERHASIL DIBUAT")
print("=" * 60)

print(f"📁 Output        : {OUTPUT_FILE}")
print(f"📊 Jumlah data   : {len(training_df)}")
print(f"📌 Jumlah fitur  : {len(training_df.columns)}")

print("\nKolom training_dataset.csv:")

for column in training_df.columns:
    print(f"- {column}")

print("\n🔍 Sample hasil:")

print(
    training_df.head(5).to_string(index=False)
)