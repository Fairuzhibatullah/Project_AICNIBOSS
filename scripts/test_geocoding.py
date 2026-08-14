from pathlib import Path
import sys

# Tambahkan root project ke Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.services.geocoding import geocode_location


origin = "Stasiun Bogor"
destination = "Kebun Raya Bogor"


print("Mencari lokasi origin...")
origin_data = geocode_location(origin)

print("Origin:")
print(origin_data)

print()

print("Mencari lokasi destination...")
destination_data = geocode_location(destination)

print("Destination:")
print(destination_data)