"""Centralised path constants for the project.

PT: Constantes centralizadas com os caminhos do projeto.

Import these instead of constructing paths by hand in notebooks or nodes.
That way, if the folder structure changes, you only need to update this file.

PT: Importe estas constantes em vez de escrever os caminhos à mão nos
notebooks ou nos nodes. Assim, se a estrutura de pastas mudar, basta
atualizar este ficheiro.

Usage / Utilização
------------------
    from src.utilities.project_paths import RAW_DIR, FINAL_DIR

    df = pd.read_csv(RAW_DIR / "qlfs_2026_q1.csv")
    output_df.to_csv(FINAL_DIR / "regional_indicators.csv", index=False)

Note / Nota
-----------
All paths are resolved to absolute paths at import time, so they work
correctly regardless of which directory a notebook is run from.

PT: Todos os caminhos são convertidos em caminhos absolutos no momento da
importação, pelo que funcionam corretamente independentemente da pasta a
partir da qual o notebook é executado.
"""

from pathlib import Path

# Walk up from this file (src/utilities/project_paths.py) two levels to reach
# the project root.
# PT: Sobe dois níveis a partir deste ficheiro
# (src/utilities/project_paths.py) até à raiz do projeto.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Configuration files
# PT: Ficheiros de configuração
CONFIG_DIR = PROJECT_ROOT / "config"

# Data lifecycle folders — named with numeric prefixes so they sort in order.
# PT: Pastas do ciclo de vida dos dados, com prefixos numéricos para que
# fiquem ordenadas corretamente.
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "0_raw"        # original source data, never modified
                                    # PT: dados de origem, nunca modificados
CLEANED_DIR = DATA_DIR / "10_cleaned"  # validated and cleaned
                                       # PT: dados validados e limpos
DERIVED_DIR = DATA_DIR / "20_processed"  # intermediate analytical datasets
                                         # PT: conjuntos de dados analíticos
                                         # intermédios
FINAL_DIR = DATA_DIR / "3_output"    # final outputs for reporting
                                     # PT: resultados finais para relatórios

# Other top-level folders
# PT: Outras pastas de primeiro nível
REPORTS_DIR = PROJECT_ROOT / "reports"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
