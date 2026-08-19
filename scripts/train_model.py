import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_FILE = (
    BASE_DIR
    / "dataset"
    / "processed"
    / "training_dataset.csv"
)

MODEL_DIR = BASE_DIR / "models"
MODEL_FILE = MODEL_DIR / "fuel_consumption_model.pkl"


# ============================================================
# LOAD DATASET
# ============================================================

print("Membaca training dataset...")

df = pd.read_csv(DATASET_FILE)

print(f"Jumlah data : {len(df)}")
print(f"Jumlah kolom: {len(df.columns)}")


# ============================================================
# VALIDASI DATASET
# ============================================================

target = "fuel_consumption_kml"

if target not in df.columns:
    raise ValueError(
        f"Kolom target '{target}' tidak ditemukan."
    )

if df.empty:
    raise ValueError("training_dataset.csv kosong.")

if df.isna().any().any():
    raise ValueError(
        "Dataset masih memiliki missing value."
    )

print("Dataset valid.")


# ============================================================
# DEFINISI FITUR & TARGET
# ============================================================

categorical_features = [
    "brand",
    "model",
    "fuel_type",
    "riding_style"
]

numeric_features = [
    "cc",
    "weight_kg",
    "avg_speed_kmh",
    "rider_weight",
    "city_percentage",
    "distance_km",
    "duration_min",
    "temperature_c",
    "humidity_percent",
    "rain_mm"
]

required_features = categorical_features + numeric_features

missing_features = [
    col for col in required_features
    if col not in df.columns
]

if missing_features:
    raise ValueError(
        f"Fitur tidak ditemukan di dataset: {missing_features}"
    )

X = df[required_features]
y = df[target]

print(f"Jumlah fitur yang digunakan: {len(required_features)}")


# ============================================================
# PREPROCESSING
# ============================================================

print("\nMenyiapkan preprocessing...")

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)


# ============================================================
# MODEL
# ============================================================

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1
)


# ============================================================
# PIPELINE
# ============================================================

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# ============================================================
# TRAIN TEST SPLIT
# ============================================================

print("\nMembagi dataset train/test...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print(f"Training data : {len(X_train)}")
print(f"Testing data  : {len(X_test)}")


# ============================================================
# TRAINING
# ============================================================

print("\nMelatih model Random Forest...")

pipeline.fit(
    X_train,
    y_train
)

print("Training selesai.")


# ============================================================
# PREDICTION
# ============================================================

print("\nMelakukan prediksi pada data testing...")

y_pred = pipeline.predict(X_test)


# ============================================================
# EVALUATION
# ============================================================

mae = mean_absolute_error(
    y_test,
    y_pred
)

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

r2 = r2_score(
    y_test,
    y_pred
)


print("\n" + "=" * 60)
print("HASIL EVALUASI MODEL")
print("=" * 60)

print(f"MAE  : {mae:.4f} km/L")
print(f"RMSE : {rmse:.4f} km/L")
print(f"R²   : {r2:.4f}")

print("=" * 60)


# ============================================================
# SAVE MODEL
# ============================================================

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    pipeline,
    MODEL_FILE
)

print("\nModel berhasil disimpan!")
print(f"Model : {MODEL_FILE}")