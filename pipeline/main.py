import yaml
from datetime import datetime
from pipeline.data_fetcher import (
    get_stations_by_city_id,
    get_sensors_for_station,
    get_sensor_measurements
)
from pipeline.file_writer import save_measurements_to_csv

def main():
    def load_config(config_path="config.yaml"):
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
        
    config = load_config()
    city_id = config["city_id"]
    city_name = config["city_name"]
    date_from = config["date_from"]
    date_to = config["date_to"]
    path = f"data/{city_name.lower()}/measurements"
    


    # Pobieranie listy stacji pomiarowych w mieście
    stations = get_stations_by_city_id(city_id)
    if not stations:
        print(f"Brak stacji dla miasta ID={city_id}")
        return

    # Iterujemy po każdej stacji
    for station in stations:
        station_id = station["Identyfikator stacji"]
        # Nazwę stacji przekształcamy do formatu przyjaznego plikom
        station_name = station["Nazwa stacji"].replace(" ", "_")

        # Pobranie listy sensorów (czujników) dla danej stacji
        sensors = get_sensors_for_station(station_id)

        # Filtrujemy tylko te, które mierzą PM10 lub PM2.5 (zanieczyszczenia pyłowe)
        sensors_pm = [s for s in sensors if s["Wskaźnik - kod"] in ("PM10", "PM2.5")]

        if not sensors_pm:
            print(f"Stacja {station_name} nie ma sensorów PM10 ani PM2.5, pomijam")
            continue

        for sensor in sensors_pm:
            sensor_id = sensor["Identyfikator stanowiska"]
            param_code = sensor["Wskaźnik - kod"].replace(" ", "_")

            # Pobieranie danych pomiarowych z danego sensora
            measurements = get_sensor_measurements(sensor_id, date_from, date_to)
            if not measurements:
                print(f"Brak danych dla sensora {sensor_id} ({param_code})")
                continue

            # Filtrowanie pustych wartości (None)
            values = [(m["Data"], m["Wartość"]) for m in measurements if m["Wartość"] is not None]
            if not values:
                print(f"Brak niepustych wartości dla {sensor_id}")
                continue

            # Sprawdzamy, czy dane pochodzą z pomiarów automatycznych (więcej niż 1 godzina)
            hours = [datetime.strptime(v[0], "%Y-%m-%d %H:%M:%S").hour for v in values]
            if all(h == 0 for h in hours):
                print(f"Pominięto nieautomatyczny sensor {sensor_id} ({param_code}) – tylko godz. 00:00")
                continue

            # Sortujemy dane według daty pomiaru
            values.sort(key=lambda x: x[0])

            # Tworzymy nazwę pliku wynikowego
            filename = f"sensor_{station_name}_{param_code}_{sensor_id}_{date_from}_to_{date_to}.csv"

            # Zapisujemy dane do pliku CSV
            save_measurements_to_csv(path, filename, values)
            print(f"Zapisano dane do {filename}")

if __name__ == "__main__":
    main()
