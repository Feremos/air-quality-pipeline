import requests

def get_elevation(lat, lon):
    url = "https://api.open-elevation.com/api/v1/lookup"
    params = {"locations": f"{lat},{lon}"}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        results = response.json().get("results", [])
        if results:
            return results[0].get("elevation")
    except requests.RequestException as e:
        print(f"Błąd pobierania wysokości: {e}")
    return None
