from pathlib import Path
from typing import Any

import pandas as pd
import yaml

class DataCatalog:
    """Load and save datasets by key using a YAML data catalog.

    How to use:
        catalog = DataCatalog("catalog.yml")
        df = catalog.load("raw_households_sample")
        catalog.save("regional_indicators", df)

    Path defaults (no manual root path needed):
    - project root -> parent of `utilities/`
    - config directory -> `<project_root>/config`
    - catalog file -> `<config_dir>/catalog.yml`
    """

    def __init__(
        self,
        catalog_file: str | Path = "catalog.yml",
        project_root: str | Path | None = None,
        config_dir: str | Path | None = None,
    ) -> None:
        self.project_root = self._resolve_project_root(project_root)
        self.config_dir = self._resolve_config_dir(config_dir)
        self.catalog_path = self._resolve_catalog_path(catalog_file)
        if not self.catalog_path.exists():
            raise FileNotFoundError(f"Catalog file not found: {self.catalog_path}")

        self._catalog = self._read_catalog()

    def _read_catalog(self) -> dict[str, dict[str, Any]]:
        """Parse the YAML catalog into typed entries."""
        raw_catalog = yaml.safe_load(self.catalog_path.read_text(encoding="utf-8")) or {}
        if not isinstance(raw_catalog, dict):
            raise ValueError("Catalog YAML must be a mapping of dataset names to settings.")

        catalog: dict[str, dict[str, Any]] = {}
        for name, spec in raw_catalog.items():
            if not isinstance(spec, dict):
                raise ValueError(f"Catalog entry '{name}' must be a mapping.")
            if "path" not in spec:
                raise ValueError(f"Catalog entry '{name}' is missing required key: 'path'.")

            # Keep entries as plain dictionaries for readability in beginner courses.
            catalog[name] = {
                "path": spec["path"],
                "format": spec.get("format"),
                "description": spec.get("description"),
                "read_only": bool(spec.get("read_only", False)),
                "dtypes": spec.get("dtypes"),
                "parse_dates": spec.get("parse_dates"),
            }
        return catalog

    def list_datasets(self) -> list[str]:
        """Return dataset names declared in the catalog."""
        return sorted(self._catalog.keys())

    def describe(self, name: str) -> dict[str, Any]:
        """Return metadata for a single dataset key."""
        entry = self._get_entry(name)
        return entry.copy()

    def load(self, name: str, **kwargs: Any) -> pd.DataFrame:
        """Load a dataset by key, dispatching to pandas by file format."""
        entry = self._get_entry(name)
        path = self._resolve_path(entry["path"])
        file_format = self._resolve_format(path, entry.get("format"))

        if not path.exists():
            raise FileNotFoundError(f"Dataset '{name}' not found at: {path}")

        if file_format == "csv":
            csv_kwargs: dict[str, Any] = {}
            if entry.get("dtypes"):
                csv_kwargs["dtype"] = entry["dtypes"]
            if entry.get("parse_dates"):
                csv_kwargs["parse_dates"] = entry["parse_dates"]
            csv_kwargs.update(kwargs)
            return pd.read_csv(path, **csv_kwargs)
        if file_format == "parquet":
            return pd.read_parquet(path, **kwargs)
        if file_format in {"xlsx", "excel"}:
            return pd.read_excel(path, **kwargs)
        if file_format in {"dta", "stata"}:
            return pd.read_stata(path, **kwargs)
        if file_format == "json":
            return pd.read_json(path, **kwargs)

        raise ValueError(
            f"Unsupported format '{file_format}' for dataset '{name}'. "
            "Supported formats: csv, parquet, xlsx/excel, dta/stata, json."
        )

    def save(self, name: str, data: pd.DataFrame, **kwargs: Any) -> Path:
        """Save a DataFrame by key while enforcing catalog read-only rules."""
        entry = self._get_entry(name)
        if entry.get("read_only", False):
            raise PermissionError(f"Dataset '{name}' is read_only and cannot be overwritten.")

        path = self._resolve_path(entry["path"])
        file_format = self._resolve_format(path, entry.get("format"))
        path.parent.mkdir(parents=True, exist_ok=True)

        if file_format == "csv":
            csv_kwargs = {"index": False}
            csv_kwargs.update(kwargs)
            data.to_csv(path, **csv_kwargs)
        elif file_format == "parquet":
            parquet_kwargs = {"index": False}
            parquet_kwargs.update(kwargs)
            data.to_parquet(path, **parquet_kwargs)
        elif file_format in {"xlsx", "excel"}:
            excel_kwargs = {"index": False}
            excel_kwargs.update(kwargs)
            data.to_excel(path, **excel_kwargs)
        elif file_format in {"dta", "stata"}:
            stata_kwargs = {"write_index": False}
            stata_kwargs.update(kwargs)
            data.to_stata(path, **stata_kwargs)
        elif file_format == "json":
            json_kwargs = {"orient": "records", "indent": 2}
            json_kwargs.update(kwargs)
            data.to_json(path, **json_kwargs)
        else:
            raise ValueError(
                f"Unsupported format '{file_format}' for dataset '{name}'. "
                "Supported formats: csv, parquet, xlsx/excel, dta/stata, json."
            )

        return path

    def _get_entry(self, name: str) -> dict[str, Any]:
        """Return one catalog entry or raise with available names."""
        if name not in self._catalog:
            available = ", ".join(self.list_datasets()) or "(empty catalog)"
            raise KeyError(f"Dataset '{name}' is not in catalog. Available: {available}")
        return self._catalog[name]

    def _resolve_path(self, dataset_path: str) -> Path:
        """Resolve dataset paths relative to project root when not absolute."""
        path = Path(dataset_path)
        if path.is_absolute():
            return path
        return (self.project_root / path).resolve()

    @staticmethod
    def _resolve_project_root(project_root: str | Path | None) -> Path:
        """Infer project root from local package structure when omitted."""
        if project_root is not None:
            return Path(project_root).expanduser().resolve()
        return Path(__file__).resolve().parents[1]

    def _resolve_config_dir(self, config_dir: str | Path | None) -> Path:
        """Resolve config directory from override or default `<project_root>/config`."""
        if config_dir is not None:
            resolved = Path(config_dir).expanduser()
            if resolved.is_absolute():
                return resolved.resolve()
            return (self.project_root / resolved).resolve()
        return (self.project_root / "config").resolve()

    def _resolve_catalog_path(self, catalog_file: str | Path) -> Path:
        """Resolve catalog file from absolute, relative, or filename-only input."""
        candidate = Path(catalog_file).expanduser()
        if candidate.is_absolute():
            return candidate.resolve()

        # If only a filename is provided, default to project_root/config.
        if len(candidate.parts) == 1:
            return (self.config_dir / candidate).resolve()
        return (self.project_root / candidate).resolve()

    @staticmethod
    def _resolve_format(path: Path, declared_format: str | None) -> str:
        """Use declared format first, then file extension."""
        if declared_format:
            return declared_format.lower()
        suffix = path.suffix.lower().lstrip(".")
        if suffix:
            return suffix
        raise ValueError(
            f"Could not infer file format from path '{path}'. Add 'format' to the catalog entry."
        )
