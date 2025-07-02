import csv
import os
import json

def save_measurements_to_csv(path, filename, data):
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, filename)
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["datetime", "value"])
        writer.writerows(data)

def save_stations_to_json(path, filename, stations):
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(stations, f, ensure_ascii=False, indent=4)

def save_sensors_to_json(path, filename, sensors):
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(sensors, f, ensure_ascii=False, indent=4)
