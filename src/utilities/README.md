# src/utilities

Shared helper classes used across notebooks and nodes.

**PT:** Classes auxiliares partilhadas, usadas nos notebooks e nos nodes.

| File                | Class / Contents  | Purpose                                          |
|---------------------|-------------------|--------------------------------------------------|
| `config.py`         | `Config`          | Load a YAML config file and retrieve values      |
| `data_catalog.py`   | `DataCatalog`     | Load and save datasets by logical name           |
| `project_paths.py`  | path constants    | Absolute paths to project folders                |

**PT:**

| Ficheiro           | Classe / Conteúdo      | Finalidade                                                |
|--------------------|------------------------|-----------------------------------------------------------|
| `config.py`        | `Config`               | Carregar um ficheiro YAML de configuração e obter valores |
| `data_catalog.py`  | `DataCatalog`          | Carregar e guardar conjuntos de dados por nome lógico     |
| `project_paths.py` | constantes de caminhos | Caminhos absolutos para as pastas do projeto              |

---

## Config

Reads `config/parameters.yaml` (or any other YAML file) and exposes values
by top-level key.

**PT:** Lê `config/parameters.yaml` (ou qualquer outro ficheiro YAML) e expõe
os valores através das chaves de primeiro nível.

```python
from src.utilities.config import Config

config = Config("parameters.yaml")
cleaning = config.get("cleaning")       # returns a dict
                                        # PT: devolve um dicionário
min_age  = cleaning.get("min_age", 15)  # pull a value with a sensible default
                                        # PT: obtém um valor com uma
                                        # predefinição razoável
```

If the file is missing, the class logs a warning instead of raising an error,
so notebooks do not break while the project is still being set up.

**PT:** Se o ficheiro não existir, a classe regista um aviso em vez de gerar um
erro, para que os notebooks não falhem enquanto o projeto ainda está a ser
preparado.

---

## DataCatalog

Reads `config/catalog.yaml` and lets you load or save datasets by logical name
without hardcoding paths in notebooks.

**PT:** Lê `config/catalog.yaml` e permite carregar ou guardar conjuntos de
dados pelo nome lógico, sem escrever os caminhos nos notebooks.

```python
from src.utilities.data_catalog import DataCatalog

catalog = DataCatalog()
df = catalog.load("raw_survey")               # reads path and format from catalog
                                              # PT: lê o caminho e o formato
                                              # do catálogo
catalog.save("regional_indicators", result)   # writes to the catalogued path
                                              # PT: escreve no caminho
                                              # registado no catálogo
```

Supported formats: `csv`, `parquet`, `excel`, `spss`, `stata`, `json`.

**PT:** Formatos suportados: `csv`, `parquet`, `excel`, `spss`, `stata`,
`json`.

The catalog entry can specify optional loading options:

**PT:** A entrada do catálogo pode indicar opções de carregamento opcionais:

| Key          | Applies to                        | Description                                                          |
|--------------|-----------------------------------|----------------------------------------------------------------------|
| `encoding`   | csv, json                         | Character encoding. Defaults to `utf-8`.                             |
|              | spss                              | Passed to pyreadstat. Omit to auto-detect from file header.          |
|              | parquet, excel, stata             | Binary formats, key is ignored.                                      |
| `columns`    | csv, parquet, excel, spss, stata  | List of column names to load (subset of file).                       |
| `sheet_name` | excel                             | Sheet name or zero-based index. Defaults to `0`.                     |
| `dtypes`     | csv                               | Column name to pandas dtype mapping.                                 |
| `parse_dates`| csv                               | List of column names to parse as dates.                              |

**PT:**

| Chave         | Aplica-se a                      | Descrição                                                                    |
|---------------|----------------------------------|------------------------------------------------------------------------------|
| `encoding`    | csv, json                        | Codificação de caracteres. Predefinição: `utf-8`.                            |
|               | spss                             | Passada ao pyreadstat. Omita para detetar a partir do cabeçalho do ficheiro. |
|               | parquet, excel, stata            | Formatos binários, a chave é ignorada.                                       |
| `columns`     | csv, parquet, excel, spss, stata | Lista de nomes de colunas a carregar (subconjunto do ficheiro).              |
| `sheet_name`  | excel                            | Nome da folha ou índice a começar em zero. Predefinição: `0`.                |
| `dtypes`      | csv                              | Correspondência entre nome da coluna e tipo pandas.                          |
| `parse_dates` | csv                              | Lista de nomes de colunas a interpretar como datas.                          |

---

## project_paths

Provides ready-made `Path` objects for the main project folders so you do
not have to construct them by hand.

**PT:** Disponibiliza objetos `Path` já preparados para as principais pastas do
projeto, para que não tenha de os construir à mão.

```python
from src.utilities.project_paths import RAW_DIR, FINAL_DIR

df = pd.read_csv(RAW_DIR / "qlfs_2026_q1.csv")
result.to_csv(FINAL_DIR / "report.csv", index=False)
```
