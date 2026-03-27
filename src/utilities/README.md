# src/utilities

Shared helper classes used across notebooks and nodes.

| File                | Class / Contents  | Purpose                                          |
|---------------------|-------------------|--------------------------------------------------|
| `config.py`         | `Config`          | Load a YAML config file and retrieve values      |
| `data_catalog.py`   | `DataCatalog`     | Load and save datasets by logical name           |
| `project_paths.py`  | path constants    | Absolute paths to project folders                |

---

## Config

Reads `config/parameters.yaml` (or any other YAML file) and exposes values
by top-level key.

```python
from src.utilities.config import Config

config = Config("parameters.yaml")
cleaning = config.get("cleaning")       # returns a dict
min_age  = cleaning.get("min_age", 15)  # pull a value with a sensible default
```

If the file is missing, the class logs a warning instead of raising an error,
so notebooks do not break while the project is still being set up.

---

## DataCatalog

Reads `config/catalog.yaml` and lets you load or save datasets by logical name
without hardcoding paths in notebooks.

```python
from src.utilities.data_catalog import DataCatalog

catalog = DataCatalog()
df = catalog.load("raw_survey")               # reads path and format from catalog
catalog.save("regional_indicators", result)   # writes to the catalogued path
```

Supported formats: `csv`, `parquet`, `excel`, `spss`, `stata`, `json`.

The catalog entry can specify optional loading options:

| Key          | Applies to                        | Description                                                          |
|--------------|-----------------------------------|----------------------------------------------------------------------|
| `encoding`   | csv, json                         | Character encoding. Defaults to `utf-8`.                             |
|              | spss                              | Passed to pyreadstat. Omit to auto-detect from file header.          |
|              | parquet, excel, stata             | Binary formats — key is ignored.                                     |
| `columns`    | csv, parquet, excel, spss, stata  | List of column names to load (subset of file).                       |
| `sheet_name` | excel                             | Sheet name or zero-based index. Defaults to `0`.                     |
| `dtypes`     | csv                               | Column name → pandas dtype mapping.                                  |
| `parse_dates`| csv                               | List of column names to parse as dates.                              |

---

## project_paths

Provides ready-made `Path` objects for the main project folders so you do
not have to construct them by hand.

```python
from src.utilities.project_paths import RAW_DIR, FINAL_DIR

df = pd.read_csv(RAW_DIR / "qlfs_2026_q1.csv")
result.to_csv(FINAL_DIR / "report.csv", index=False)
```
