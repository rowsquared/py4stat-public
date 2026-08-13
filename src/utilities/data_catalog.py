import logging
import yaml
import pandas as pd
from pathlib import Path

# Use a module-level logger so warning messages show which file they come from.
# PT: Usa um logger ao nível do módulo para que as mensagens de aviso indiquem
# o ficheiro de onde vieram.
logger = logging.getLogger(__name__)


class DataCatalog:
    """Load and save datasets by logical name using a YAML catalog.

    PT: Carrega e guarda conjuntos de dados por nome lógico, através de um
    catálogo YAML.

    Instead of hardcoding file paths in every notebook, you register datasets
    once in `config/catalog.yaml` and then refer to them by name:

    PT: Em vez de escrever os caminhos dos ficheiros em cada notebook, regista
    os conjuntos de dados uma única vez em `config/catalog.yaml` e passa a
    referi-los pelo nome:

        catalog = DataCatalog()
        df = catalog.load("raw_survey")
        catalog.save("regional_indicators", df)

    The catalog file stores the path, format, and optional loading details
    for each dataset. The class resolves paths relative to the project root
    automatically.

    PT: O ficheiro de catálogo guarda o caminho, o formato e as opções de
    carregamento de cada conjunto de dados. A classe resolve automaticamente
    os caminhos em relação à raiz do projeto.

    Optional keys supported per catalog entry
    Chaves opcionais suportadas em cada entrada do catálogo
    ------------------------------------------------------
    encoding   : str  — character encoding. Behaviour depends on format:
                        csv / json  → applied directly; defaults to "utf-8".
                        spss        → passed to pyreadstat; omit to let the
                                      library auto-detect from the file header
                                      (recommended unless the header is wrong).
                        parquet / excel / stata → binary formats; encoding
                                      is embedded in the file and this key
                                      is ignored.
                 PT: codificação de caracteres. O comportamento depende do
                     formato:
                        csv / json  → aplicada diretamente; predefinição
                                      "utf-8".
                        spss        → passada ao pyreadstat; omita para que a
                                      biblioteca a detete no cabeçalho do
                                      ficheiro (recomendado, exceto se o
                                      cabeçalho estiver errado).
                        parquet / excel / stata → formatos binários; a
                                      codificação está embebida no ficheiro e
                                      esta chave é ignorada.
    columns    : list — column names to load. Supported by csv, parquet,
                        excel, spss, and stata.
                 PT: nomes das colunas a carregar. Suportado por csv, parquet,
                     excel, spss e stata.
    sheet_name : str or int — sheet to load from an Excel file. Defaults to 0
                        (the first sheet).
                 PT: folha a carregar de um ficheiro Excel. Predefinição: 0
                     (a primeira folha).
    dtypes     : dict — column → pandas dtype, applied when loading csv.
                 PT: coluna → tipo pandas, aplicado ao carregar csv.
    parse_dates: list — column names to parse as dates, csv only.
                 PT: nomes das colunas a interpretar como datas, apenas csv.

    Parameters / Parâmetros
    -----------------------
    filename : str
        Name of the catalog YAML file. Defaults to "catalog.yaml".
        PT: Nome do ficheiro YAML do catálogo. Predefinição: "catalog.yaml".
    config_dir : str
        Folder that contains the catalog file. Defaults to "config".
        PT: Pasta que contém o ficheiro de catálogo. Predefinição: "config".
    file_path : str or None
        Full path to the catalog file. Use this only if the catalog lives
        outside the default config directory.
        PT: Caminho completo para o ficheiro de catálogo. Utilize apenas se o
        catálogo estiver fora da pasta de configuração predefinida.
    """

    def __init__(
        self, filename="catalog.yaml", config_dir="config", file_path=None
    ):
        if file_path is None:
            # Walk up from this file (src/utilities/data_catalog.py) two levels
            # to reach the project root, then add the config directory.
            # PT: Sobe dois níveis a partir deste ficheiro
            # (src/utilities/data_catalog.py) até à raiz do projeto e depois
            # acrescenta a pasta de configuração.
            project_root = Path(__file__).resolve().parents[2]
            self.path = project_root / config_dir / filename
        else:
            self.path = Path(file_path)

        # Store the project root so dataset paths can be resolved later.
        # PT: Guarda a raiz do projeto para poder resolver mais tarde os
        # caminhos dos conjuntos de dados.
        self._project_root = Path(__file__).resolve().parents[2]

        # Start with an empty dict so methods work even if loading fails.
        # PT: Começa com um dicionário vazio para que os métodos funcionem
        # mesmo que o carregamento falhe.
        self._catalog = {}

        if not self.path.exists():
            logger.warning("Catalog file not found: %s", self.path)
            return

        # yaml.safe_load returns None for an empty file, so fall back to {}.
        # PT: yaml.safe_load devolve None para um ficheiro vazio, por isso
        # usamos {} como valor alternativo.
        with open(self.path, "r", encoding="utf-8") as f:
            self._catalog = yaml.safe_load(f) or {}

        if not isinstance(self._catalog, dict):
            logger.warning(
                "Catalog file should contain a top-level dictionary"
            )
            self._catalog = {}

    # ------------------------------------------------------------------
    # Inspection
    # PT: Inspeção
    # ------------------------------------------------------------------

    def get(self, name, default=None):
        """Return the catalog entry for a dataset by logical name.

        PT: Devolve a entrada do catálogo de um conjunto de dados a partir do
        seu nome lógico.

        The entry is a dictionary with keys like path, format, description,
        dtypes, parse_dates, encoding, columns, and sheet_name as defined
        in catalog.yaml.

        PT: A entrada é um dicionário com chaves como path, format,
        description, dtypes, parse_dates, encoding, columns e sheet_name,
        tal como definidas em catalog.yaml.

        Example / Exemplo
        -----------------
        >>> catalog.get("raw_survey")
        {'path': 'data/00_raw/qlfs_2026_q1.csv', 'format': 'csv', ...}
        """
        return self._catalog.get(name, default)

    def list_datasets(self):
        """Return the names of all datasets declared in the catalog.

        PT: Devolve os nomes de todos os conjuntos de dados declarados no
        catálogo.

        Example / Exemplo
        -----------------
        >>> catalog.list_datasets()
        ['clean_survey', 'raw_households_sample', 'raw_survey', ...]
        """
        return list(self._catalog.keys())

    # ------------------------------------------------------------------
    # Loading
    # PT: Carregamento
    # ------------------------------------------------------------------


    def load(self, name):
        """Load a dataset by logical name and return a pandas DataFrame.

        PT: Carrega um conjunto de dados pelo nome lógico e devolve um
        DataFrame do pandas.

        All loading options (format, encoding, columns, sheet_name, dtypes,
        parse_dates) are read from the catalog entry in catalog.yaml —
        the notebook only needs to pass the dataset name.

        PT: Todas as opções de carregamento (format, encoding, columns,
        sheet_name, dtypes, parse_dates) são lidas da entrada do catálogo em
        catalog.yaml: o notebook só precisa de indicar o nome do conjunto de
        dados.

        Supported formats: csv, parquet, excel, spss, stata, json.
        PT: Formatos suportados: csv, parquet, excel, spss, stata, json.

        Example / Exemplo
        -----------------
        >>> df = catalog.load("raw_survey")
        """
        entry = self.get(name, {})
        path = self._resolve_path(entry.get("path", ""))
        file_format = entry.get("format", "csv")

        if not path.exists():
            logger.warning("Dataset '%s' not found at: %s", name, path)
            return pd.DataFrame()

        # encoding — read from the catalog entry with no default.
        # Each format below handles the None case in the way that makes most
        # sense for that format (see comments per format).
        # PT: encoding: lido da entrada do catálogo, sem valor predefinido.
        # Cada formato abaixo trata o caso None da forma mais adequada
        # (ver os comentários de cada formato).
        encoding = entry.get("encoding")

        # columns — load only a subset of columns.
        # Supported by csv, parquet, excel, spss, stata.
        # Set in catalog.yaml as a list:
        #   columns: [hh_id, region_code, income]
        # PT: columns: carrega apenas um subconjunto de colunas.
        # Suportado por csv, parquet, excel, spss e stata.
        # Define-se em catalog.yaml como uma lista:
        #   columns: [hh_id, region_code, income]
        columns = entry.get("columns")

        if file_format == "csv":
            # Default to utf-8 when not specified.
            # PT: Usa utf-8 por predefinição quando não for indicada.
            return pd.read_csv(
                path,
                dtype=entry.get("dtypes"),
                parse_dates=entry.get("parse_dates"),
                encoding=encoding or "utf-8",
                usecols=columns,
            )

        if file_format == "parquet":
            # Parquet is a binary columnar format. Encoding is defined inside
            # the file and cannot be overridden — the catalog key is ignored.
            # PT: O Parquet é um formato binário orientado a colunas. A
            # codificação está definida dentro do ficheiro e não pode ser
            # alterada: a chave do catálogo é ignorada.
            return pd.read_parquet(path, columns=columns)

        if file_format == "excel":
            # Excel (.xlsx) is a binary format. Encoding is not applicable.
            # sheet_name defaults to 0 (first sheet). Accepts a name string
            # or a zero-based integer index:  sheet_name: "Data"  or  1
            # PT: O Excel (.xlsx) é um formato binário, pelo que a codificação
            # não se aplica. sheet_name assume 0 por predefinição (primeira
            # folha) e aceita o nome da folha ou um índice inteiro a começar
            # em zero:  sheet_name: "Data"  ou  1
            sheet_name = entry.get("sheet_name", 0)
            return pd.read_excel(path, sheet_name=sheet_name, usecols=columns)

        if file_format == "spss":
            # Use pyreadstat directly so we can pass encoding.
            # When encoding is None, pyreadstat auto-detects it from the file
            # header — correct for most SPSS files. Set it explicitly
            # only when the header metadata is wrong:  encoding: latin-1
            # PT: Usa o pyreadstat diretamente para poder passar a codificação.
            # Quando encoding é None, o pyreadstat deteta-a no cabeçalho do
            # ficheiro, o que é correto para a maioria dos ficheiros SPSS.
            # Defina-a explicitamente apenas quando os metadados do cabeçalho
            # estiverem errados:  encoding: latin-1
            import pyreadstat
            df, _ = pyreadstat.read_sav(
                str(path), encoding=encoding, usecols=columns
            )
            return df

        if file_format == "stata":
            # Stata (.dta) is a binary format. Encoding is embedded in the
            # file and is handled automatically — the catalog key is ignored.
            # PT: O Stata (.dta) é um formato binário. A codificação está
            # embebida no ficheiro e é tratada automaticamente: a chave do
            # catálogo é ignorada.
            return pd.read_stata(path, columns=columns)

        if file_format == "json":
            # Default to utf-8 when not specified.
            # Column selection is not supported by read_json directly;
            # filter columns after loading if needed.
            # PT: Usa utf-8 por predefinição quando não for indicada.
            # A seleção de colunas não é suportada diretamente por read_json:
            # filtre as colunas depois do carregamento, se for necessário.
            return pd.read_json(path, encoding=encoding or "utf-8")

        logger.warning("Unsupported format: %s", file_format)
        return pd.DataFrame()

    # ------------------------------------------------------------------
    # Saving
    # PT: Gravação
    # ------------------------------------------------------------------

    def save(self, name, df):
        """Save a DataFrame by logical name.

        PT: Guarda um DataFrame usando o seu nome lógico.

        The output path, format, and encoding come from the catalog entry.
        Parent directories are created automatically if they do not exist.

        PT: O caminho de saída, o formato e a codificação vêm da entrada do
        catálogo. As pastas superiores são criadas automaticamente se ainda
        não existirem.

        Supported formats: csv, parquet, excel, stata, json.
        PT: Formatos suportados: csv, parquet, excel, stata, json.

        Example / Exemplo
        -----------------
        >>> catalog.save("regional_indicators", indicators_df)
        """
        entry = self.get(name, {})
        path = self._resolve_path(entry.get("path", ""))
        file_format = entry.get("format", "csv")

        # Create the output folder if it does not exist yet.
        # PT: Cria a pasta de saída se ainda não existir.
        path.parent.mkdir(parents=True, exist_ok=True)

        # encoding — used by text-based formats (csv, json).
        # Defaults to utf-8 when not set in the catalog entry.
        # PT: encoding: usado pelos formatos de texto (csv, json).
        # Assume utf-8 quando não estiver definido na entrada do catálogo.
        encoding = entry.get("encoding") or "utf-8"

        if file_format == "csv":
            df.to_csv(path, index=False, encoding=encoding)
            return

        if file_format == "parquet":
            # Binary format — encoding is not applicable.
            # PT: Formato binário: a codificação não se aplica.
            df.to_parquet(path, index=False)
            return

        if file_format == "excel":
            # Binary format — encoding is not applicable.
            # PT: Formato binário: a codificação não se aplica.
            df.to_excel(path, index=False)
            return

        if file_format == "stata":
            # Binary format — encoding is not applicable.
            # PT: Formato binário: a codificação não se aplica.
            df.to_stata(path, write_index=False)
            return

        if file_format == "json":
            # to_json() has no encoding parameter, so write via open()
            # to ensure the correct encoding is applied.
            # PT: to_json() não tem parâmetro de codificação, por isso a
            # escrita é feita com open() para garantir que a codificação
            # correta é aplicada.
            json_str = df.to_json(orient="records", indent=2)
            with open(path, "w", encoding=encoding) as f:
                f.write(json_str)
            return

        logger.warning("Unsupported format for saving: %s", file_format)

    # ------------------------------------------------------------------
    # Internal helpers
    # PT: Funções auxiliares internas
    # ------------------------------------------------------------------

    def _resolve_path(self, dataset_path):
        # If the path in the catalog is absolute (e.g. /data/...) use it
        # directly. Otherwise treat it as relative to the project root.
        # PT: Se o caminho indicado no catálogo for absoluto (por exemplo
        # /data/...), é usado diretamente. Caso contrário, é tratado como
        # relativo à raiz do projeto.
        path = Path(dataset_path)
        if path.is_absolute():
            return path
        return (self._project_root / path).resolve()
