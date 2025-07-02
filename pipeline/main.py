import yaml
from datetime import datetime
from pipeline.data_fetcher import (
    get_stations_by_city_id,
    get_sensors_for_station,
    get_sensor_measurements
)
from pipeline.file_writer import (
    save_measurements_to_csv,
    save_stations_to_json
)
from pipeline.elevation import get_elevation  # Nowa funkcja!

def load_config(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    city_id = config["city_id"]
    city_name = config["city_name"]
    date_from = config["date_from"]
    date_to = config["date_to"]

    base_path = f"data/{city_name.lower()}"
    measurements_path = f"{base_path}/measurements"

    # --- Pobieranie listy stacji ---
    stations = get_stations_by_city_id(city_id)
    if not stations:
        print(f"Brak stacji dla miasta ID={city_id}")
        return

    # --- Dodawanie wysokości ---
      # --- Dodajemy wysokość do stacji ---
    for station in stations:
        try:
            lat = float(station["WGS84 φ N"])
            lon = float(station["WGS84 λ E"])
            elevation = get_elevation(lat, lon)
            station["Wysokość n.p.m. [m]"] = elevation
        except (ValueError, KeyError):
            station["Wysokość n.p.m. [m]"] = None

    save_stations_to_json(base_path, "stations.json", stations)
    print(f"Zapisano dane o stacjach do stations.json")

    # --- Zbierzemy wszystkie sensory ---
    all_sensors = []

    for station in stations:
        station_id = station["Identyfikator stacji"]
        station_name = station["Nazwa stacji"].replace(" ", "_")

        sensors = get_sensors_for_station(station_id)
        if not sensors:
            print(f"Brak sensorów dla stacji {station_name}")
            continue

        # Dodajemy do listy sensorów dodatkowo nazwę stacji i jej elevation
        for sensor in sensors:
            sensor_copy = sensor.copy()
            sensor_copy["Nazwa stacji"] = station["Nazwa stacji"]
            sensor_copy["Wysokość n.p.m. [m]"] = station.get("Wysokość n.p.m. [m]")
            all_sensors.append(sensor_copy)

    # --- Zapis sensorów do JSON ---
    save_stations_to_json(base_path, "sensors.json", all_sensors)
    print(f"Zapisano dane o sensorach do sensors.json")

    # --- Dalej idziemy jak wcześniej z pomiarami ---
    for station in stations:
        station_id = station["Identyfikator stacji"]
        station_name = station["Nazwa stacji"].replace(" ", "_")

        sensors_pm = [s for s in all_sensors if s.get("Identyfikator stanowiska") and s.get("Nazwa stacji") == station["Nazwa stacji"] and s["Wskaźnik - kod"] in ("PM10", "PM2.5")]

        if not sensors_pm:
            print(f"Stacja {station_name} nie ma sensorów PM10 ani PM2.5, pomijam")
            continue

        for sensor in sensors_pm:
            sensor_id = sensor["Identyfikator stanowiska"]
            param_code = sensor["Wskaźnik - kod"].replace(" ", "_")

            measurements = get_sensor_measurements(sensor_id, date_from, date_to)
            if not measurements:
                print(f"Brak danych dla sensora {sensor_id} ({param_code})")
                continue

            values = [(m["Data"], m["Wartość"]) for m in measurements if m["Wartość"] is not None]
            if not values:
                print(f"Brak niepustych wartości dla {sensor_id}")
                continue

            hours = [datetime.strptime(v[0], "%Y-%m-%d %H:%M:%S").hour for v in values]
            if all(h == 0 for h in hours):
                print(f"Pominięto nieautomatyczny sensor {sensor_id} ({param_code}) – tylko godz. 00:00")
                continue

            values.sort(key=lambda x: x[0])
            filename = f"sensor_{station_name}_{param_code}_{sensor_id}_{date_from}_to_{date_to}.csv"

            save_measurements_to_csv(measurements_path, filename, values)
            print(f"Zapisano dane do {filename}")

if __name__ == "__main__":
    main()
