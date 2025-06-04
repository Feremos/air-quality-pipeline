# Air Quality Fetcher

Module responsible for GIOS PM 10 and PM 2.5 data downloading from sensors in Kielce. TO DO: what it outputs

## Module structure
```
dataDownloading/
├── pipeline/
│   ├── main.py
│   ├── data_fetcher.py
│   └── file_writer.py
├── config.yaml
├── .gitignore
├── requirements.txt
└── README.md
```


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
