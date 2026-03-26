"""Centralised path constants for the project.

Import these instead of constructing paths by hand in notebooks or nodes.
That way, if the folder structure changes, you only need to update this file.

Usage
-----
    from src.utilities.project_paths import RAW_DIR, FINAL_DIR

    df = pd.read_csv(RAW_DIR / "qlfs_2026_q1.csv")
    output_df.to_csv(FINAL_DIR / "regional_indicators.csv", index=False)

Note
----
All paths are resolved to absolute paths at import time, so they work
correctly regardless of which directory a notebook is run from.
"""

from pathlib import Path

# Walk up from this file (src/utilities/project_paths.py) two levels to reach
# the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Configuration files
CONFIG_DIR = PROJECT_ROOT / "config"

# Data lifecycle folders — named with numeric prefixes so they sort in order.
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "0_raw"        # original source data, never modified
CLEANED_DIR = DATA_DIR / "1_cleaned"  # validated and cleaned
DERIVED_DIR = DATA_DIR / "2_derived"  # intermediate analytical datasets
FINAL_DIR = DATA_DIR / "3_final"    # final outputs for reporting

# Other top-level folders
REPORTS_DIR = PROJECT_ROOT / "reports"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
