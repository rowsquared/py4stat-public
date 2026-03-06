# PyStatFrame

Base Python project template for statisticians with a simple catalog-driven data IO layer.

## Structure

```text
PyStatFrame/
├── config/
│   ├── catalog.yml
│   └── settings.yml
├── data/
│   ├── 0_raw/
│   ├── 01_cleaned/
│   ├── 02_processed/
│   └── 03_output/
├── nodes/
├── notebooks/
└── utilities/
    ├── config_loader.py
    └── data_catalog.py
```

## Install

```bash
pip install -r requirements.txt
```

## Usage

```python
from utilities import ConfigLoader, DataCatalog

catalog = DataCatalog("catalog.yml")
config = ConfigLoader("settings.yml")

raw_df = catalog.load("raw_survey")
cleaning_cfg = config.get("cleaning")

# Example save
# cleaned_df = ...
# catalog.save("clean_survey", cleaned_df)
```
