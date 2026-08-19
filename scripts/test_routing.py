from backend.services.routing import get_route


origin_lat = -6.5942887
origin_lon = 106.7907695

destination_lat = -6.5983048
destination_lon = 106.7994229


print("Mengambil data rute dari OpenRouteService...")

route = get_route(
    origin_lat,
    origin_lon,
    destination_lat,
    destination_lon
)

print("\nHasil routing:")
print(f"Jarak   : {route['distance_km']} km")
print(f"Durasi  : {route['duration_min']} menit")