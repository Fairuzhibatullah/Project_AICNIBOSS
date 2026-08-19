import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = BASE_DIR / "models" / "fuel_consumption_model.pkl"
DATASET_FILE = (
    BASE_DIR
    / "dataset"
    / "processed"
    / "training_dataset.csv"
)

print("=" * 60)
print("CEK MODEL")
print("=" * 60)

print("\nMemuat model...")

if not MODEL_FILE.exists():
    raise FileNotFoundError(f"Model file tidak ditemukan: {MODEL_FILE}")

model = joblib.load(MODEL_FILE)

print("Model berhasil dimuat.")

df = pd.read_csv(DATASET_FILE)

model_features = [
    "brand", "model", "fuel_type", "riding_style",
    "cc", "weight_kg", "avg_speed_kmh", "rider_weight", "city_percentage",
    "distance_km", "duration_min", "temperature_c", "humidity_percent", "rain_mm"
]

target = "fuel_consumption_kml"

sample = df.iloc[[0]].copy()
X_sample = sample[model_features]
actual = sample[target].iloc[0]

prediction = model.predict(X_sample)[0]

print("\nHasil pengecekan:")
print(f"Fitur yang diuji : {len(model_features)} fitur bersih (tanpa ID/elevasi dummy)")
print(f"Nilai aktual     : {actual:.2f} km/L")
print(f"Prediksi         : {prediction:.2f} km/L")
print(f"Selisih          : {abs(actual - prediction):.2f} km/L")

print("\nModel dapat menerima 14 fitur terbaru dan menghasilkan prediksi dengan sukses.")

print("\nCek model selesai.")