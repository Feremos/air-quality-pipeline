import requests
import time

BASE_SLEEP = 15  
MAX_RETRIES = 3  

def safe_get(url, params=None):
    """Wysyła bezpieczne zapytanie GET z obsługą błędów i retry."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"Requesting: {url} (attempt {attempt})")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            time.sleep(BASE_SLEEP)  
            return response.json()
        except requests.RequestException as e:
            print(f"Błąd przy próbie {attempt}: {e}")
            if attempt == MAX_RETRIES:
                print("Maksymalna liczba prób przekroczona. Pomijam.")
                return {}
            else:
                sleep_time = BASE_SLEEP * attempt
                print(f"Oczekiwanie {sleep_time}s przed ponowną próbą ")
                time.sleep(sleep_time)

def get_stations_by_city_id(city_id, page_size=500):
    """Zwraca listę stacji pomiarowych dla podanego ID miasta."""
    stations = []
    page = 0

    while True:
        url = f"https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?page={page}&size={page_size}"
        data = safe_get(url)
        if not data:
            break

        
        all_stations = data if isinstance(data, list) else data.get("Lista stacji pomiarowych", data)
        filtered = [s for s in all_stations if s.get("Identyfikator miasta") == city_id]
        stations.extend(filtered)

        if len(all_stations) < page_size:
            break  
        page += 1

    return stations

def get_sensors_for_station(station_id, page_size=500):
    """Zwraca listę sensorów dla danej stacji."""
    url = f"https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/{station_id}?page=0&size={page_size}"
    data = safe_get(url)
    
    return data if isinstance(data, list) else data.get("Lista stanowisk pomiarowych dla podanej stacji", [])

def get_sensor_measurements(sensor_id, date_from, date_to, page_size=500):
    """Zwraca pełne dane pomiarowe (ze wszystkich stron) dla sensora i zakresu dat."""
    all_measurements = []
    page = 0

    while True:
        url = (
            f"https://api.gios.gov.pl/pjp-api/v1/rest/archivalData/getDataBySensor/"
            f"{sensor_id}?page={page}&size={page_size}&dateFrom={date_from}%2000%3A00&dateTo={date_to}%2000%3A00"
        )
        data = safe_get(url)
        if not data:
            break

        measurements = data.get("Lista archiwalnych wyników pomiarów", [])
        all_measurements.extend(measurements)

        total_pages = data.get("totalPages")
        if total_pages is None or page >= int(total_pages) - 1:
            break


        page += 1

    return all_measurements
