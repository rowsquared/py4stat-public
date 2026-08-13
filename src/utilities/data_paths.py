"""A simple helper class for finding project data folders.

PT: Uma classe auxiliar simples para localizar as pastas de dados do projeto.

This is intentionally kept beginner-friendly: no special guards, just a class
with properties that return Path objects and a small helper to list what is
inside a folder.

PT: Foi mantida propositadamente acessível a principiantes: sem verificações
especiais, apenas uma classe com propriedades que devolvem objetos Path e uma
pequena função auxiliar para listar o conteúdo de uma pasta.

Usage / Utilização
------------------
    from src.utilities.data_paths import DataPaths

    paths = DataPaths()
    print(paths.raw)          # absolute path to data/0_raw
                              # PT: caminho absoluto para data/0_raw
    print(paths.cleaned)      # absolute path to data/10_cleaned
                              # PT: caminho absoluto para data/10_cleaned
    paths.list("cleaned")     # prints the files inside data/10_cleaned
                              # PT: imprime os ficheiros de data/10_cleaned
"""

from pathlib import Path


class DataPaths:
    """Holds paths to every data layer in the project.

    PT: Guarda os caminhos de todas as camadas de dados do projeto.

    Attributes / Atributos
    ----------------------
    root     : project root folder
               PT: pasta raiz do projeto
    data     : top-level data/ folder
               PT: pasta data/ de primeiro nível
    raw      : data/0_raw        (source files, never modified)
               PT: data/0_raw        (ficheiros de origem, nunca modificados)
    cleaned  : data/10_cleaned   (validated and cleaned data)
               PT: data/10_cleaned   (dados validados e limpos)
    processed: data/20_processed (intermediate analytical datasets)
               PT: data/20_processed (dados analíticos intermédios)
    output   : data/30_output    (final outputs ready for reporting)
               PT: data/30_output    (resultados finais para relatórios)
    """

    def __init__(self):
        # Walk up from this file (src/utilities/data_paths.py) to the project root
        # PT: Sobe a partir deste ficheiro (src/utilities/data_paths.py) até à
        # raiz do projeto
        self.root = Path(__file__).resolve().parents[2]
        self.data = self.root / "data"
        self.raw = self.data / "0_raw"
        self.cleaned = self.data / "10_cleaned"
        self.processed = self.data / "20_processed"
        self.output = self.data / "30_output"

    def list(self, layer="raw"):
        """Print the contents of one of the data layers.

        PT: Imprime o conteúdo de uma das camadas de dados.

        Parameters / Parâmetros
        -----------------------
        layer : str
            One of "raw", "cleaned", "processed", or "output".
            PT: Um de "raw", "cleaned", "processed" ou "output".
        """
        folder = getattr(self, layer)
        print(f"{layer}: {folder}")
        for item in sorted(folder.iterdir()):
            kind = "DIR " if item.is_dir() else "FILE"
            print(f"  [{kind}] {item.name}")
