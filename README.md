# BogoRoute

**BogoRoute** (*AI Route & Fuel Predictor*) adalah aplikasi web cerdas untuk memprediksi efisiensi dan konsumsi Bahan Bakar Minyak (BBM) sepeda motor berdasarkan rute perjalanan nyata, kondisi cuaca *real-time*, spesifikasi kendaraan, serta karakteristik pengendara (khususnya wilayah Bogor dan sekitarnya).

Proyek ini dikembangkan sebagai software MVP untuk COMPFEST 18 Artificial Intelligence Competition (AIC).

---

## 1. Deskripsi Project

BogoRoute mengintegrasikan pemodelan *Machine Learning* (Random Forest Regression) dengan layanan geospasial dan cuaca untuk memberikan estimasi konsumsi BBM yang presisi. Alur kerja aplikasi:
1. **Geocoding**: Menemukan koordinat akurat titik asal (*origin*) dan tujuan (*destination*) menggunakan OpenStreetMap / Nominatim.
2. **Routing & Road Snapping**: Menghitung rute navigasi jalan raya dan *geometry polyline* menggunakan OpenRouteService (ORS) Directions API dan ORS Snap API.
3. **Weather Fetching**: Mengambil parameter cuaca aktual (suhu, kelembapan, curah hujan) pada lokasi tujuan menggunakan Open-Meteo API.
4. **AI Inference**: Model Random Forest Regression memproses 14 fitur perjalanan untuk memprediksi efisiensi konsumsi BBM (km/L).
5. **Estimasi Kebutuhan & Biaya**: Menghitung total liter BBM yang dibutuhkan serta total estimasi biaya perjalanan dalam Rupiah (Rp).
6. **Visualisasi Interaktif**: Menampilkan rute pada peta interaktif Leaflet beserta ringkasan statistik perjalanan di frontend.

---

## 2. Tech Stack

- **Backend**:
  - Python 3.11
  - FastAPI & Uvicorn (REST API)
  - Scikit-Learn & Joblib (Random Forest Model)
  - Pandas & NumPy (Data Processing)
  - Requests & Python-Dotenv
  - Pydantic v2
- **Frontend**:
  - React 19
  - Vite 8
  - Leaflet & React-Leaflet (Interactive Map)
  - Inter Font & Material Symbols
- **Layanan Eksternal**:
  - OpenRouteService API (Routing & Road Snapping)
  - Nominatim / OpenStreetMap (Geocoding)
  - Open-Meteo API (Live Weather Data)
- **Deployment & Kontainerisasi**:
  - Docker & Docker Compose

---

## 3. Requirements

Sebelum menjalankan aplikasi, pastikan perangkat telah terinstal:
1. **Docker Desktop** (dengan Docker Compose v2 aktif)
2. **Git**

---

## 4. Clone Repository

Buka terminal / command prompt, lalu clone repository ini:

```bash
git clone <URL_REPOSITORY_BOGOROUTE>
cd project
```

*(Sesuaikan nama direktori jika berbeda).*

---

## 5. Environment Configuration

Backend memerlukan API key **OpenRouteService (ORS)** untuk menjalankan fitur routing dan pemetaan jalan.

> **PENTING UNTUK EVALUATOR:**
> Demi menjaga keamanan *credential*, API key tidak disertakan langsung dalam repositori publik. API key diberikan secara terpisah kepada panitia.

1. Salin template `.env.example` menjadi file `.env` di direktori utama (*root*):

   **Linux / macOS:**
   ```bash
   cp .env.example .env
   ```

   **Windows (PowerShell / Command Prompt):**
   ```cmd
   copy .env.example .env
   ```

2. Buka file `.env` dan masukkan API key yang telah diberikan:

   ```env
   ORS_API_KEY=masukkan_api_key_yang_diberikan
   ```

---

## 6. Menjalankan Project dengan Docker Compose

Jalankan perintah berikut pada direktori *root* proyek untuk membangun (*build*) dan menyalakan seluruh kontainer di latar belakang (*detached mode*):

```bash
docker compose up --build -d
```

Docker Compose akan otomatis mengunduh base image, menginstal seluruh dependensi backend dan frontend, serta menjalankan kedua service.

---

## 7. Mengecek Status Container

Pastikan seluruh kontainer berjalan dengan normal:

```bash
docker compose ps
```

**Output yang Diharapkan:**
- Service `backend` (`bogoroute_backend`): status **Up** / **healthy**, port `0.0.0.0:8001->8000/tcp`.
- Service `frontend` (`bogoroute_frontend`): status **Up**, port `0.0.0.0:5173->5173/tcp`.

---

## 8. Mengakses Frontend

Buka web browser dan akses antarmuka pengguna di:
- **URL Frontend**: [http://localhost:5173](http://localhost:5173) (atau [http://127.0.0.1:5173](http://127.0.0.1:5173))

---

## 9. Mengakses Backend / API

Backend FastAPI dapat diakses langsung melalui host pada port `8001`:
- **API Base / Healthcheck**: [http://localhost:8001/](http://localhost:8001/)
  - Mengembalikan: `{"message": "AIC NIBOSS API aktif", "status": "running"}`
- **Interactive API Documentation (Swagger UI)**: [http://localhost:8001/docs](http://localhost:8001/docs)
- **Endpoint Prediksi Utama**: `POST http://localhost:8001/predict`

---

## 10. Melihat Backend Logs (Proof of Work)

Untuk membuktikan bahwa sistem menerima request dari frontend dan menjalankan alur AI secara nyata, buka terminal terpisah dan jalankan:

```bash
docker compose logs -f backend
```

Saat Anda menekan tombol **"Buat Rute"** pada antarmuka frontend, terminal log akan menampilkan tahapan proses secara *real-time*:

```text
INFO:backend.app:BOGOROUTE - prediction request received
INFO:backend.app:Processing geocoding
INFO:backend.app:Processing route
INFO:backend.app:Fetching weather data
INFO:backend.app:Running Random Forest inference
INFO:backend.app:Prediction completed
INFO:backend.app:Returning prediction result
INFO:backend.app:POST /predict - 200 OK, distance: 5.912 km, duration: 11.93 min, predicted fuel efficiency: 40.74 km/L, estimated fuel needed: 0.15 L, estimated cost: 1950
```

---

## 11. Menghentikan Aplikasi

Untuk mematikan dan menghapus kontainer aplikasi:

```bash
docker compose down
```

---

## 12. Menjalankan Kembali

Jika kontainer sudah pernah di-build sebelumnya, Anda dapat menjalankannya kembali secara instan tanpa build ulang:

```bash
docker compose up -d
```

---

## 13. Jika Ada Perubahan Dockerfile / Dependency

Jika terdapat perubahan pada `requirements.txt`, `package.json`, kode backend/frontend, atau file `Dockerfile`, jalankan build ulang:

```bash
docker compose up --build -d
```

---

## 14. Troubleshooting Singkat

1. **Port Konflik (`Port 5173` atau `Port 8001` sudah digunakan)**:
   - Pastikan tidak ada service Vite atau Uvicorn lain yang sedang berjalan di host.
   - Hentikan proses yang memakai port tersebut atau sesuaikan pemetaan port di `docker-compose.yml`.

2. **Error Routing / Status HTTP 400 pada Prediksi**:
   - Pastikan file `.env` sudah dibuat di root project dan variabel `ORS_API_KEY` sudah terisi dengan key yang valid.
   - Pastikan kuota harian OpenRouteService masih tersedia.

3. **Backend Status Unhealthy**:
   - Periksa detail log error dengan menjalankan `docker compose logs backend`.
   - Pastikan model `models/fuel_consumption_model.pkl` tersedia di repositori.

4. **Frontend Tidak Terhubung ke Backend (CORS / Network Error)**:
   - Pastikan backend berjalan pada port `8001` di host machine (`http://127.0.0.1:8001`).
   - Jangan mengakses frontend melalui IP privat jika browser memblokir request lokal. Gunakan `http://localhost:5173` atau `http://127.0.0.1:5173`.

---

## 15. Struktur Folder Project

```text
project/
├── backend/
│   ├── services/
│   │   ├── geocoding.py       # Integrasi Geocoding Nominatim
│   │   ├── routing.py         # Integrasi OpenRouteService & Polyline Decoder
│   │   └── weather.py         # Integrasi Live Weather Open-Meteo
│   ├── app.py                 # FastAPI Application & Predict Endpoint
│   ├── Dockerfile             # Konfigurasi container Backend (Python 3.11)
│   └── requirements.txt       # Daftar dependensi Python Backend
├── dataset/
│   ├── processed/             # Dataset hasil pemrosesan
│   └── raw/                   # Dataset mentah rute perjalanan
├── frontend/
│   ├── src/
│   │   ├── components/        # Komponen UI (Sidebar, MapView, Form, dll)
│   │   ├── services/
│   │   │   └── api.js         # HTTP Client penghubung ke Backend
│   │   ├── App.jsx            # State Management & Main Layout
│   │   ├── App.css            # Desain UI BogoRoute (Navy/Teal Theme)
│   │   └── main.jsx           # Entrypoint React
│   ├── Dockerfile             # Konfigurasi container Frontend (Node 20)
│   ├── package.json           # Dependensi React & Leaflet
│   └── vite.config.js         # Konfigurasi Vite Dev Server
├── models/
│   └── fuel_consumption_model.pkl  # Pre-trained Random Forest ML Model
├── scripts/                   # Script utilitas & data pipeline
├── .dockerignore              # Filter file untuk Docker build
├── .env.example               # Template environment variable
├── .gitignore                 # Konfigurasi ignore file Git
├── docker-compose.yml         # Konfigurasi orkestrasi multi-container
└── README.md                  # Panduan setup & dokumentasi proyek
```

---

## 16. Quick Start (Panduan Kilat)

Untuk panitia yang ingin langsung menguji aplikasi dalam hitungan menit:

```bash
# 1. Masuk ke direktori project
cd project

# 2. Siapkan file .env dari template
cp .env.example .env   # (Gunakan 'copy .env.example .env' pada Windows)

# 3. Isi ORS_API_KEY di file .env dengan API key yang telah diberikan panitia

# 4. Jalankan aplikasi dengan Docker Compose
docker compose up --build -d

# 5. Pantau log backend di terminal (opsional untuk PoW)
docker compose logs -f backend

# 6. Buka aplikasi di browser
# http://localhost:5173
```
