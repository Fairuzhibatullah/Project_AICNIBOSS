import pandas as pd


# ============================================================
# CONFIG
# ============================================================

INPUT_FILE = "dataset/processed/locations_geocoded.csv"
OUTPUT_FILE = "dataset/processed/locations_geocoded_fixed.csv"

TARGET_START_ID = 61
TARGET_END_ID = 79


# ============================================================
# FIX COORDINATE
# ============================================================

def fix_coordinate(value):
    """
    Memperbaiki koordinat yang memiliki titik desimal berlebih.

    Contoh:
        -6.570.077  -> -6.570077
        106.812.426 -> 106.812426
        -6.594.186  -> -6.594186

    Koordinat yang sudah normal tidak diubah.
    """

    value = str(value).strip()

    # Kalau tidak ada titik atau hanya punya satu titik,
    # biarkan seperti semula.
    if value.count(".") <= 1:
        return value

    # Pisahkan berdasarkan titik
    parts = value.split(".")

    # Tanda negatif tetap berada di bagian pertama
    first_part = parts[0]

    # Gabungkan bagian setelah titik
    decimal_part = "".join(parts[1:])

    return f"{first_part}.{decimal_part}"


# ============================================================
# MAIN
# ============================================================

def main():

    print("Membaca file:")
    print(INPUT_FILE)

    df = pd.read_csv(INPUT_FILE)

    print(f"\nJumlah data: {len(df)}")

    # Pastikan kolom yang diperlukan tersedia
    required_columns = [
        "id",
        "nama_lokasi",
        "latitude",
        "longitude",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Kolom tidak ditemukan: {missing_columns}"
        )

    print("\nMemperbaiki koordinat ID 61–79...\n")

    fixed_count = 0

    for index, row in df.iterrows():

        location_id = int(row["id"])

        # Hanya proses ID 61 sampai 79
        if TARGET_START_ID <= location_id <= TARGET_END_ID:

            old_latitude = str(row["latitude"])
            old_longitude = str(row["longitude"])

            new_latitude = fix_coordinate(
                old_latitude
            )

            new_longitude = fix_coordinate(
                old_longitude
            )

            # Tampilkan hanya data yang berubah
            if (
                old_latitude != new_latitude
                or old_longitude != new_longitude
            ):

                print(
                    f"ID {location_id} - "
                    f"{row['nama_lokasi']}"
                )

                if old_latitude != new_latitude:
                    print(
                        f"  Latitude : "
                        f"{old_latitude} -> "
                        f"{new_latitude}"
                    )

                if old_longitude != new_longitude:
                    print(
                        f"  Longitude: "
                        f"{old_longitude} -> "
                        f"{new_longitude}"
                    )

                print()

                df.at[index, "latitude"] = new_latitude
                df.at[index, "longitude"] = new_longitude

                fixed_count += 1

    # ========================================================
    # SAVE
    # ========================================================

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print("========================================")
    print("SELESAI")
    print("========================================")

    print(
        f"Jumlah lokasi yang diperbaiki: "
        f"{fixed_count}"
    )

    print(
        f"File hasil: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()