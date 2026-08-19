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

model = joblib.load(MODEL_FILE)

print("Model berhasil dimuat.")

df = pd.read_csv(DATASET_FILE)

sample = df.iloc[[0]].copy()

target = "fuel_consumption_kml"

X = sample.drop(columns=[target])

actual = sample[target].iloc[0]

prediction = model.predict(X)[0]

print("\nHasil pengecekan:")
print(f"Nilai aktual : {actual:.2f} km/L")
print(f"Prediksi     : {prediction:.2f} km/L")
print(f"Selisih      : {abs(actual - prediction):.2f} km/L")

print("\nModel dapat menerima data training_dataset.")

print("\nCek model selesai.")