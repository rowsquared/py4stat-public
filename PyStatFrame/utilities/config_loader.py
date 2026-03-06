from pathlib import Path
from typing import Any

import yaml


class ConfigLoader:
    """Load YAML configuration files from a project config directory.

    Defaults assume a local project structure:
    - project root: parent of `utilities/`
    - config directory: `<project_root>/config`
    - default config file: `<config_dir>/settings.yml`
    """

    def __init__(
        self,
        config_file: str | Path = "settings.yml",
        project_root: str | Path | None = None,
        config_dir: str | Path | None = None,
    ) -> None:
        # Keep path defaults aligned with DataCatalog for consistent usage.
        self.project_root = self._resolve_project_root(project_root)
        self.config_dir = self._resolve_config_dir(config_dir)
        self.default_config_file = Path(config_file)

        if not self.config_dir.exists():
            raise FileNotFoundError(f"Config directory not found: {self.config_dir}")

    def load(self, file_name: str | Path | None = None) -> dict[str, Any]:
        """Load one YAML config file and return it as a dictionary."""
        path = self._resolve_config_file_path(file_name)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(config, dict):
            raise ValueError(f"Config file '{path.name}' must contain a YAML mapping.")
        return config

    def get(self, key: str, file_name: str | Path | None = None, default: Any = None) -> Any:
        """Read a nested config value using dot notation (for example `a.b.c`)."""
        config = self.load(file_name=file_name)

        current: Any = config
        for part in key.split("."):
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        return current

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

    def _resolve_config_file_path(self, file_name: str | Path | None) -> Path:
        """Resolve config file from absolute, relative, or filename-only input."""
        candidate = Path(file_name) if file_name is not None else self.default_config_file
        candidate = candidate.expanduser()

        if candidate.is_absolute():
            return candidate.resolve()
        if len(candidate.parts) == 1:
            return (self.config_dir / candidate).resolve()
        return (self.project_root / candidate).resolve()
