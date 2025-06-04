# Air Quality Fetcher

Module responsible for GIOS PM 10 and PM 2.5 data downloading from sensors in Kielce. TO DO: what it outputs

## Struktura projektu

your-project/
├── pipeline/
│ ├── init.py
│ ├── main.py
│ ├── data_fetcher.py
│ └── file_writer.py
├── requirements.txt
├── .gitignore
└── README.md


## Jak uruchomić projekt

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
