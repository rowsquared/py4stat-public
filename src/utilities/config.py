import logging
import yaml
from pathlib import Path

# Use a module-level logger so warning messages show which file they come from.
# In a notebook you will see something like:
#   WARNING:src.utilities.config:Config file not found: config/parameters.yaml
logger = logging.getLogger(__name__)


class Config:
    """Load a single YAML configuration file and expose its values.

    The class looks for the file inside the project's `config/` directory
    by default, so you only need to pass the filename:

        config = Config("parameters.yaml")
        cleaning = config.get("cleaning")
        min_age = cleaning.get("min_age", 15)

    If the file is missing the class logs a warning and returns empty defaults
    instead of raising an error. That makes notebooks easier to run step by
    step while a project is still being set up.

    Parameters
    ----------
    filename : str
        Name of the YAML file, e.g. "parameters.yaml".
    config_dir : str
        Folder that contains the config files. Defaults to "config" which is
        resolved relative to the project root.
    file_path : str or None
        Full path to the file. Use this only if the file lives outside the
        default config directory.
    """

    def __init__(self, filename, config_dir="config", file_path=None):
        if file_path is None:
            # Walk up from this file (src/utilities/config.py) two levels to
            # reach the project root, then add the config directory.
            project_root = Path(__file__).resolve().parents[2]
            self.path = project_root / config_dir / filename
        else:
            self.path = Path(file_path)

        # Start with an empty dict so .get() always works even if loading fails.
        self._config = {}

        if not self.path.exists():
            logger.warning("Config file not found: %s", self.path)
            return

        # yaml.safe_load returns None for empty files, so fall back to {}.
        with open(self.path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f) or {}

        self._validate()

    def _validate(self):
        # A valid config file should be a YAML mapping (key: value pairs).
        # If the file contains a plain list or a scalar, reset and warn.
        if not isinstance(self._config, dict):
            logger.warning("Config file should contain a top-level dictionary")
            self._config = {}

    def get(self, key, default=None):
        """Return the value for a top-level key, or `default` if not found.

        Example
        -------
        >>> config = Config("parameters.yaml")
        >>> cleaning = config.get("cleaning")
        >>> min_age = cleaning.get("min_age", 15)
        """
        return self._config.get(key, default)
