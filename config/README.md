# config

Contains project configuration files. Keeping settings here — rather than
inside notebooks or transformation functions — means you only need to update
one file when a value changes.

| File               | Purpose                                                  |
|--------------------|----------------------------------------------------------|
| `parameters.yaml`  | Thresholds, filters, and other analysis settings         |
| `catalog.yaml`     | Dataset registry: paths, formats, and loading metadata   |
| `logging.yaml`     | Logging level and handler settings                       |

---

## parameters.yaml

Stores values that may change between runs, such as age filters, poverty
thresholds, or lists of required columns. Load it with `Config`:

```python
from src.utilities.config import Config

config = Config("parameters.yaml")
min_age = config.get("cleaning", {}).get("min_age", 15)
```

---

## catalog.yaml

Registers every dataset used in the project. Each entry maps a logical name
to a file path and optional loading options. Load and save datasets through
`DataCatalog` rather than hardcoding paths in notebooks:

```python
from src.utilities.data_catalog import DataCatalog

catalog = DataCatalog()
df = catalog.load("raw_survey")
catalog.save("regional_indicators", result_df)
```

Supported formats: `csv`, `parquet`, `excel`, `spss`, `stata`, `json`.

Each entry supports these optional loading keys:

| Key          | Applies to                        | Description                                      |
|--------------|-----------------------------------|--------------------------------------------------|
| `encoding`   | csv, json                         | Character encoding. Defaults to `utf-8`.         |
| `columns`    | csv, parquet, excel, spss, stata  | List of column names to load (subset of file).   |
| `sheet_name` | excel                             | Sheet name or zero-based index. Defaults to `0`. |
| `dtypes`     | csv                               | Column name → pandas dtype mapping.              |
| `parse_dates`| csv                               | List of column names to parse as dates.          |

Example with several options set:

```yaml
raw_survey:
  path: data/00_raw/qlfs_2026_q1.csv
  format: csv
  encoding: utf-8           # optional, defaults to utf-8
  columns: [hh_id, age, income, region_code]   # load only these columns
  dtypes:
    hh_id: str              # keep leading zeros in identifier columns
    region_code: str
  parse_dates:
    - survey_date

survey_excel:
  path: data/00_raw/qlfs_2026_q1.xlsx
  format: excel
  sheet_name: "Data"        # load a specific sheet by name (or use 0, 1, …)
  columns: [hh_id, age, income]
```

---

## logging.yaml

Standard Python logging configuration. Load it at the top of a script or
notebook with:

```python
import logging.config
import yaml

with open("config/logging.yaml") as f:
    logging.config.dictConfig(yaml.safe_load(f))
```
