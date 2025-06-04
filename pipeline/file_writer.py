import csv
import os

def save_measurements_to_csv(path, filename, data):
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, filename)
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["datetime", "value"])
        writer.writerows(data)
