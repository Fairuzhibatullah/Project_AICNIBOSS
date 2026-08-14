from pathlib import Path
import sys


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))


from backend.services.geocoding import geocode_location
from backend.services.weather import get_weather


location_name = "Kebun Raya Bogor"


print("Mencari lokasi...")

location = geocode_location(location_name)

print()
print("Lokasi:")
print(location)

print()
print("Mengambil data cuaca...")

weather = get_weather(
    location["latitude"],
    location["longitude"]
)

print()
print("Hasil cuaca:")
print(f"Suhu      : {weather['temperature_c']} °C")
print(f"Kelembapan : {weather['humidity_percent']} %")
print(f"Hujan     : {weather['rain_mm']} mm")