import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_FILE = BASE_DIR / "dataset" / "processed" / "training_dataset.csv"

print("=" * 60)
print("CEK DATASET TRAINING")
print("=" * 60)

if not DATASET_FILE.exists():
    raise FileNotFoundError(f"File dataset tidak ditemukan: {DATASET_FILE}")

df = pd.read_csv(DATASET_FILE)

print(f"\nJumlah baris  : {len(df)}")
print(f"Jumlah kolom  : {len(df.columns)}")

print("\nKolom dataset:")
for column in df.columns:
    print(f"- {column}")

print("\nMissing value:")
missing = df.isna().sum()
missing_filtered = missing[missing > 0]

if len(missing_filtered) == 0:
    print("Tidak ada missing value.")
else:
    print(missing_filtered)

print("\nDuplikasi:")
print(f"Jumlah baris duplikat: {df.duplicated().sum()}")

print("\nTipe data:")
print(df.dtypes)

print("\nStatistik numerik:")
print(df.describe().round(2))

target_col = "fuel_consumption_kml"
if target_col in df.columns:
    print(f"\nDistribusi Target ({target_col}):")
    print(df[target_col].describe().round(2))
    print(f"Nilai target minimum : {df[target_col].min():.2f}")
    print(f"Nilai target maksimum : {df[target_col].max():.2f}")

model_features = [
    "brand", "model", "fuel_type", "riding_style",
    "cc", "weight_kg", "avg_speed_kmh", "rider_weight", "city_percentage",
    "distance_km", "duration_min", "temperature_c", "humidity_percent", "rain_mm"
]

print(f"\nPengecekan 14 Fitur Model ML:")
missing_features = [col for col in model_features if col not in df.columns]
if not missing_features:
    print("Seluruh 14 fitur model ML tersedia lengkap di dataset!")
else:
    print("Fitur model missing:", missing_features)

print("\nCek dataset selesai.")