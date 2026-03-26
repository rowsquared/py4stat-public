import logging
import yaml
import pandas as pd
from pathlib import Path

# Use a module-level logger so warning messages show which file they come from.
logger = logging.getLogger(__name__)


class DataCatalog:
    """Load and save datasets by logical name using a YAML catalog.

    Instead of hardcoding file paths in every notebook, you register datasets
    once in `config/catalog.yaml` and then refer to them by name:

        catalog = DataCatalog()
        df = catalog.load("raw_survey")
        catalog.save("regional_indicators", df)

    The catalog file stores the path, format, and optional loading details
    for each dataset. The class resolves paths relative to the project root
    automatically.

    Optional keys supported per catalog entry
    ------------------------------------------
    encoding   : str  — character encoding for text-based formats (csv,
                        json).
                        Defaults to "utf-8". Not applicable to binary formats
                        (parquet, excel, stata).
    columns    : list — column names to load. Supported by csv, parquet,
                        excel, spss, and stata.
    sheet_name : str or int — sheet to load from an Excel file. Defaults to 0
                        (the first sheet).
    dtypes     : dict — column → pandas dtype, applied when loading csv.
    parse_dates: list — column names to parse as dates, csv only.

    Parameters
    ----------
    filename : str
        Name of the catalog YAML file. Defaults to "catalog.yaml".
    config_dir : str
        Folder that contains the catalog file. Defaults to "config".
    file_path : str or None
        Full path to the catalog file. Use this only if the catalog lives
        outside the default config directory.
    """

    def __init__(
        self, filename="catalog.yaml", config_dir="config", file_path=None
    ):
        if file_path is None:
            # Walk up from this file (src/utilities/data_catalog.py) two levels
            # to reach the project root, then add the config directory.
            project_root = Path(__file__).resolve().parents[2]
            self.path = project_root / config_dir / filename
        else:
            self.path = Path(file_path)

        # Store the project root so dataset paths can be resolved later.
        self._project_root = Path(__file__).resolve().parents[2]

        # Start with an empty dict so methods work even if loading fails.
        self._catalog = {}

        if not self.path.exists():
            logger.warning("Catalog file not found: %s", self.path)
            return

        # yaml.safe_load returns None for an empty file, so fall back to {}.
        with open(self.path, "r", encoding="utf-8") as f:
            self._catalog = yaml.safe_load(f) or {}

        if not isinstance(self._catalog, dict):
            logger.warning(
                "Catalog file should contain a top-level dictionary"
            )
            self._catalog = {}

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def get(self, name, default=None):
        """Return the catalog entry for a dataset by logical name.

        The entry is a dictionary with keys like path, format, description,
        dtypes, parse_dates, encoding, columns, and sheet_name as defined
        in catalog.yaml.

        Example
        -------
        >>> catalog.get("raw_survey")
        {'path': 'data/00_raw/qlfs_2026_q1.csv', 'format': 'csv', ...}
        """
        return self._catalog.get(name, default)

    def list_datasets(self):
        """Return the names of all datasets declared in the catalog.

        Example
        -------
        >>> catalog.list_datasets()
        ['clean_survey', 'raw_households_sample', 'raw_survey', ...]
        """
        return list(self._catalog.keys())

    # ------------------------------------------------------------------
    # Loading
    # ------------------------------------------------------------------

    def load(self, name):
        """Load a dataset by logical name and return a pandas DataFrame.

        All loading options (format, encoding, columns, sheet_name, dtypes,
        parse_dates) are read from the catalog entry in catalog.yaml —
        the notebook only needs to pass the dataset name.

        Supported formats: csv, parquet, excel, spss, stata, json.

        Example
        -------
        >>> df = catalog.load("raw_survey")
        """
        entry = self.get(name, {})
        path = self._resolve_path(entry.get("path", ""))
        file_format = entry.get("format", "csv")

        if not path.exists():
            logger.warning("Dataset '%s' not found at: %s", name, path)
            return pd.DataFrame()

        # encoding — used by text-based formats (csv, json).
        # Defaults to utf-8. Override per dataset in catalog.yaml:
        #   encoding: latin-1
        encoding = entry.get("encoding", "utf-8")

        # columns — load only a subset of columns.
        # Supported by csv, parquet, excel, spss, stata.
        # Set in catalog.yaml as a list:
        #   columns: [hh_id, region_code, income]
        columns = entry.get("columns")

        if file_format == "csv":
            return pd.read_csv(
                path,
                dtype=entry.get("dtypes"),
                parse_dates=entry.get("parse_dates"),
                encoding=encoding,
                usecols=columns,
            )

        if file_format == "parquet":
            # parquet is a binary format — encoding is handled by the file
            # itself and does not need to be specified.
            return pd.read_parquet(path, columns=columns)

        if file_format == "excel":
            # sheet_name defaults to 0 (the first sheet). Use a sheet name
            # string or a zero-based integer index.
            #   sheet_name: "Data"   or   sheet_name: 1
            sheet_name = entry.get("sheet_name", 0)
            return pd.read_excel(path, sheet_name=sheet_name, usecols=columns)

        if file_format == "spss":
            # SPSS (.sav) files store encoding metadata internally.
            # The pandas API does not expose an encoding parameter for SPSS;
            # the underlying pyreadstat library reads it from the file header.
            return pd.read_spss(path, usecols=columns)

        if file_format == "stata":
            # Stata (.dta) files are binary and self-describing.
            return pd.read_stata(path, columns=columns)

        if file_format == "json":
            # JSON is text-based, so encoding applies.
            # Column selection is not supported by read_json directly;
            # filter columns after loading if needed.
            return pd.read_json(path, encoding=encoding)

        logger.warning("Unsupported format: %s", file_format)
        return pd.DataFrame()

    # ------------------------------------------------------------------
    # Saving
    # ------------------------------------------------------------------

    def save(self, name, df):
        """Save a DataFrame by logical name.

        The output path, format, and encoding come from the catalog entry.
        Parent directories are created automatically if they do not exist.

        Supported formats: csv, parquet, excel, stata, json.

        Example
        -------
        >>> catalog.save("regional_indicators", indicators_df)
        """
        entry = self.get(name, {})
        path = self._resolve_path(entry.get("path", ""))
        file_format = entry.get("format", "csv")

        # Create the output folder if it does not exist yet.
        path.parent.mkdir(parents=True, exist_ok=True)

        if file_format == "csv":
            encoding = entry.get("encoding", "utf-8")
            df.to_csv(path, index=False, encoding=encoding)
            return

        if file_format == "parquet":
            df.to_parquet(path, index=False)
            return

        if file_format == "excel":
            df.to_excel(path, index=False)
            return

        if file_format == "stata":
            df.to_stata(path, write_index=False)
            return

        if file_format == "json":
            encoding = entry.get("encoding", "utf-8")
            df.to_json(path, orient="records", indent=2)
            return

        logger.warning("Unsupported format for saving: %s", file_format)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_path(self, dataset_path):
        # If the path in the catalog is absolute (e.g. /data/...) use it
        # directly. Otherwise treat it as relative to the project root.
        path = Path(dataset_path)
        if path.is_absolute():
            return path
        return (self._project_root / path).resolve()
