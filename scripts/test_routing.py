from backend.services.routing import get_route

def test_routing():
    print("Mulai routing...")

    # Stasiun Bogor (Origin)
    origin_lat = -6.5942887
    origin_lon = 106.7907695

    # Kebun Raya Bogor (Destination)
    destination_lat = -6.5983048
    destination_lon = 106.7994229

    print(f"Origin (Stasiun Bogor): lat={origin_lat}, lon={origin_lon}")
    print(f"Destination (Kebun Raya Bogor - unroutable test): lat={destination_lat}, lon={destination_lon}")

    print("\nMengambil data rute dari OpenRouteService (termasuk step resolve routable point)...")

    try:
        route = get_route(
            origin_lat,
            origin_lon,
            destination_lat,
            destination_lon
        )

        print("\nHasil routing sukses:")
        print(f"Jarak    : {route['distance_km']} km")
        print(f"Durasi   : {route['duration_min']} menit")
    except Exception as e:
        print(f"\nRouting gagal: {e}")

if __name__ == "__main__":
    test_routing()
