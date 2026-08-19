import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_FILE = BASE_DIR / "dataset" / "processed" / "training_dataset.csv"

print("=" * 60)
print("CEK DATASET TRAINING")
print("=" * 60)

df = pd.read_csv(DATASET_FILE)

print(f"\nJumlah baris : {len(df)}")
print(f"Jumlah kolom: {len(df.columns)}")

print("\nKolom:")
for column in df.columns:
    print(f"- {column}")

print("\nMissing value:")
missing = df.isna().sum()
missing = missing[missing > 0]

if len(missing) == 0:
    print("Tidak ada missing value.")
else:
    print(missing)

print("\nDuplikasi:")
print(f"Jumlah baris duplikat: {df.duplicated().sum()}")

print("\nTipe data:")
print(df.dtypes)

print("\nStatistik numerik:")
print(df.describe().round(2))

print("\nDistribusi target:")
print(df["fuel_consumption_kml"].describe().round(2))

print("\nNilai target minimum:",
      df["fuel_consumption_kml"].min())

print("Nilai target maksimum:",
      df["fuel_consumption_kml"].max())

print("\nCek selesai.")