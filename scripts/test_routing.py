from pathlib import Path
import sys

# Tambahkan root project ke Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.services.geocoding import geocode_location
from backend.services.routing import get_route


origin_name = "Stasiun Bogor"
destination_name = "Kebun Raya Bogor"


print("Mencari lokasi origin...")
origin = geocode_location(origin_name)

print("Origin:")
print(origin)

print()

print("Mencari lokasi destination...")
destination = geocode_location(destination_name)

print("Destination:")
print(destination)

print()

print("Menghitung rute...")

route = get_route(
    origin["latitude"],
    origin["longitude"],
    destination["latitude"],
    destination["longitude"]
)

print()
print("Hasil routing:")
print(f"Jarak   : {route['distance_km']} km")
print(f"Durasi  : {route['duration_min']} menit")