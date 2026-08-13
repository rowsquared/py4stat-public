import logging
import yaml
from pathlib import Path

# Use a module-level logger so warning messages show which file they come from.
# PT: Usa um logger ao nível do módulo para que as mensagens de aviso indiquem
# o ficheiro de onde vieram.
# In a notebook you will see something like:
# PT: Num notebook irá ver algo como:
#   WARNING:src.utilities.config:Config file not found: config/parameters.yaml
logger = logging.getLogger(__name__)


class Config:
    """Load a single YAML configuration file and expose its values.

    PT: Carrega um único ficheiro de configuração YAML e expõe os seus valores.

    The class looks for the file inside the project's `config/` directory
    by default, so you only need to pass the filename:

    PT: Por predefinição, a classe procura o ficheiro dentro da pasta `config/`
    do projeto, pelo que basta indicar o nome do ficheiro:

        config = Config("parameters.yaml")
        cleaning = config.get("cleaning")
        min_age = cleaning.get("min_age", 15)

    If the file is missing the class logs a warning and returns empty defaults
    instead of raising an error. That makes notebooks easier to run step by
    step while a project is still being set up.

    PT: Se o ficheiro não existir, a classe regista um aviso e devolve valores
    predefinidos vazios em vez de gerar um erro. Isso facilita a execução dos
    notebooks passo a passo enquanto o projeto ainda está a ser preparado.

    Parameters / Parâmetros
    -----------------------
    filename : str
        Name of the YAML file, e.g. "parameters.yaml".
        PT: Nome do ficheiro YAML, por exemplo "parameters.yaml".
    config_dir : str
        Folder that contains the config files. Defaults to "config" which is
        resolved relative to the project root.
        PT: Pasta que contém os ficheiros de configuração. O valor predefinido
        é "config", resolvido em relação à raiz do projeto.
    file_path : str or None
        Full path to the file. Use this only if the file lives outside the
        default config directory.
        PT: Caminho completo para o ficheiro. Utilize apenas se o ficheiro
        estiver fora da pasta de configuração predefinida.
    """

    def __init__(self, filename, config_dir="config", file_path=None):
        if file_path is None:
            # Walk up from this file (src/utilities/config.py) two levels to
            # reach the project root, then add the config directory.
            # PT: Sobe dois níveis a partir deste ficheiro
            # (src/utilities/config.py) até à raiz do projeto e depois
            # acrescenta a pasta de configuração.
            project_root = Path(__file__).resolve().parents[2]
            self.path = project_root / config_dir / filename
        else:
            self.path = Path(file_path)

        # Start with an empty dict so .get() always works even if loading fails.
        # PT: Começa com um dicionário vazio para que .get() funcione sempre,
        # mesmo que o carregamento falhe.
        self._config = {}

        if not self.path.exists():
            logger.warning("Config file not found: %s", self.path)
            return

        # yaml.safe_load returns None for empty files, so fall back to {}.
        # PT: yaml.safe_load devolve None para ficheiros vazios, por isso
        # usamos {} como valor alternativo.
        with open(self.path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f) or {}

        self._validate()

    def _validate(self):
        # A valid config file should be a YAML mapping (key: value pairs).
        # If the file contains a plain list or a scalar, reset and warn.
        # PT: Um ficheiro de configuração válido deve ser um mapeamento YAML
        # (pares chave: valor). Se o ficheiro contiver uma lista simples ou um
        # valor escalar, repõe o dicionário vazio e emite um aviso.
        if not isinstance(self._config, dict):
            logger.warning("Config file should contain a top-level dictionary")
            self._config = {}

    def get(self, key, default=None):
        """Return the value for a top-level key, or `default` if not found.

        PT: Devolve o valor de uma chave de primeiro nível ou `default` se a
        chave não for encontrada.

        Example / Exemplo
        -----------------
        >>> config = Config("parameters.yaml")
        >>> cleaning = config.get("cleaning")
        >>> min_age = cleaning.get("min_age", 15)
        """
        return self._config.get(key, default)
