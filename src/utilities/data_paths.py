"""A simple helper class for finding project data folders.

This is intentionally kept beginner-friendly: no special guards, just a class
with properties that return Path objects and a small helper to list what is
inside a folder.

Usage
-----
    from src.utilities.data_paths import DataPaths

    paths = DataPaths()
    print(paths.raw)          # absolute path to data/0_raw
    print(paths.cleaned)      # absolute path to data/10_cleaned
    paths.list("cleaned")     # prints the files inside data/10_cleaned
"""

from pathlib import Path


class DataPaths:
    """Holds paths to every data layer in the project.

    Attributes
    ----------
    root     : project root folder
    data     : top-level data/ folder
    raw      : data/0_raw        (source files, never modified)
    cleaned  : data/10_cleaned   (validated and cleaned data)
    processed: data/20_processed (intermediate analytical datasets)
    output   : data/30_output    (final outputs ready for reporting)
    """

    def __init__(self):
        # Walk up from this file (src/utilities/data_paths.py) to the project root
        self.root = Path(__file__).resolve().parents[2]
        self.data = self.root / "data"
        self.raw = self.data / "0_raw"
        self.cleaned = self.data / "10_cleaned"
        self.processed = self.data / "20_processed"
        self.output = self.data / "30_output"

    def list(self, layer="raw"):
        """Print the contents of one of the data layers.

        Parameters
        ----------
        layer : str
            One of "raw", "cleaned", "processed", or "output".
        """
        folder = getattr(self, layer)
        print(f"{layer}: {folder}")
        for item in sorted(folder.iterdir()):
            kind = "DIR " if item.is_dir() else "FILE"
            print(f"  [{kind}] {item.name}")

