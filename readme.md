# Air Quality Fetcher

Module responsible for GIOS PM 10 and PM 2.5 data downloading from sensors in Kielce.

## Module structure
```
dataDownloading/
├── pipeline/
│   ├── main.py
│   ├── data_fetcher.py
│   ├── elevation.py
│   ├── file_writer.py   
│   ├── historical.py
│   ├── main.py
│   └── stations_fetcher.py
├── config.yaml
├── .gitignore
├── requirements.txt
└── README.md
```

---

## How it works

This module downloads air quality data (PM10 and PM2.5) from sensors managed by GIOS (Polish Chief Inspectorate of Environmental Protection) for the city of Kielce.

Two main modes of operation:

- **Current data fetching** — downloads sensor measurements for a specified date range.
- **Historical data fetching** — downloads archived data from a fixed start date (e.g. 2025-01-01) up to yesterday.

---

## Configuration

The module is configured via the `config.yaml` file:

```yaml
city_id: 360             # City identifier in GIOS API (360 = Kielce)
city_name: Kielce        # City name, used for folder naming
date_from: "2025-01-01"  # Start date for data fetching (format: YYYY-MM-DD)
date_to: "2025-06-30"    # End date for data fetching (format: YYYY-MM-DD)
```

date_from and date_to define the range for sensor data downloads.

For historical data, date_from is typically fixed (e.g. start of 2025), and date_to is usually set to yesterday's date.

For current or recent data, you can set both to the desired range, for example today or the last week.


## Outputs

All output data are saved inside the `data/{city_name_lower}/` directory.

### Stations data — saved as JSON: 

### data/kielce/stations.json

Contains metadata about each station including:

- Station ID, name, city, address
- GPS coordinates (latitude, longitude)
- Elevation above sea level (added via Open-Elevation API)

### Sensors data — saved as JSON:


### data/kielce/sensors.json

Contains metadata about each sensor, including:

- Sensor ID
- Sensor type/code (e.g. PM10, PM2.5)
- Associated station name
- Elevation (copied from station)

### Measurement data — saved as CSV files per sensor and date range:

### data/kielce/measurements/sensor_{station_name}{param_code}{sensor_id}_{date_from}to{date_to}.csv


Each CSV contains:

- Timestamp (`datetime`)
- Measured value (`value`)

### Modes

- In **historical mode**, set 'date_from' and 'date_to' to whatever range you want to get data for.
- In **current mode**, set 'date_from' to yesterdays and 'date_to' to todays date to get current measurments .



## How to run the module

1. Create and activate an virtual enviroment

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```
2. Install Dependencies
```bash
pip install -r requirements.txt
```
3. Run the script from the main catalog
```bash
python -m pipeline.main
```
