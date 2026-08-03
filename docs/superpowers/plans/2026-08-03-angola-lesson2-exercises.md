# Angola Lesson 2 Exercise Series Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build five exercise notebooks and five matching solution notebooks that teach Lesson 2 (data loading and quality control) on the real Angola IEA employment survey and INE international trade data.

**Architecture:** One linear pipeline over the Q4 2025 SPSS survey. a21 diagnoses the raw file and writes nothing; a22 types it and writes a checkpoint to `10_cleaned/`; a23 cleans that checkpoint in place; a24 derives features into `20_processed/`; a25 merges a province lookup, appends the Q3 2025 wave, and separately joins the trade workbooks. Each solution notebook is authored by a throwaway Python builder script in the scratchpad, executed with `jupyter nbconvert`, then mechanically gapped to produce the exercise version.

**Tech Stack:** Python 3.12+, pandas 3.0, numpy 2.4, matplotlib 3.10, pyreadstat (SPSS reader), openpyxl (xlsx reader), jupyter nbconvert.

**Spec:** `docs/superpowers/specs/2026-08-03-angola-lesson2-exercises-design.md`

## Global Constraints

Every task inherits these. They are not repeated per task.

- **Library allowlist.** Only `os`, `pandas as pd`, `numpy as np`, `matplotlib.pyplot as plt` inside notebooks. `pyreadstat` is permitted in **exactly one task of a21** and nowhere else. No `seaborn`, `plotly`, `duckdb`, `geopandas`, `sklearn`, `pathlib`.
- **Paths.** Always `os.path.join`. Never `pathlib.Path`, never a bare `Path(`. Notebook path constants are relative to the notebook: `'../../data/0_raw'`.
- **No em dashes** (`—`) in any authored markdown, code comment, or string in the new notebooks. Use colons, commas, or hyphens.
- **Raw data is read-only.** Nothing writes into `data/0_raw/`.
- **Exercise notebooks carry no outputs.** Every code cell has `"outputs": []` and `"execution_count": null`.
- **Solution notebooks carry outputs.** They are committed after a successful execution.
- **Notebook titles** use the form `Exercise 2.1: Loading Data & First Diagnostics (Angola IEA)` and `Solution 2.1: Loading Data & First Diagnostics (Angola IEA)`.
- **Working directory** for all commands is the repo root, `/Users/gabriele/App/rowsquared/py4stat-public`.
- **Python interpreter.** Use `python3` (the anaconda interpreter that already has pyreadstat and openpyxl) for builder and checker scripts. The project `.venv` gains the dependencies in Task 1.

### Reading this plan

Tasks 2 to 6 embed the full text of a notebook inside a fenced Python block. Those
blocks contain their own `## Task N` markdown headings, which are **notebook
section headings for the learner**, not steps of this plan. The plan's own units
are the `## Task N:` headings at the top level and the `- [ ] **Step N**`
checkboxes. If you are searching this file, note that `## Task 3` matches both
"Task 3 of this plan" and "Task 3 inside notebook a22".

### Scratchpad location

Builder and checker scripts are throwaway tooling, not repo files. Write them to:

```
/private/tmp/claude-501/-Users-gabriele-App-rowsquared-py4stat-public/a418965a-5ef4-4814-af5f-f1eda9f94e1e/scratchpad/
```

Referred to below as `$SCRATCH`. Set it once per shell:

```bash
export SCRATCH=/private/tmp/claude-501/-Users-gabriele-App-rowsquared-py4stat-public/a418965a-5ef4-4814-af5f-f1eda9f94e1e/scratchpad
```

## File Structure

**Committed to the repo:**

| Path | Responsibility |
|---|---|
| `notebooks/exercises/exercise_a21_loading_diagnostics.ipynb` | Section 2.1 practice, gaps unfilled |
| `notebooks/exercises/exercise_a22_types_subsetting.ipynb` | Section 2.2 practice |
| `notebooks/exercises/exercise_a23_cleaning_missing_duplicates.ipynb` | Section 2.3 practice |
| `notebooks/exercises/exercise_a24_transforming_features.ipynb` | Section 2.4 practice |
| `notebooks/exercises/exercise_a25_merging_combining.ipynb` | Section 2.5 practice |
| `notebooks/solutions/solution_a21_loading_diagnostics.ipynb` | Worked a21, executed, outputs committed |
| `notebooks/solutions/solution_a22_types_subsetting.ipynb` | Worked a22 |
| `notebooks/solutions/solution_a23_cleaning_missing_duplicates.ipynb` | Worked a23 |
| `notebooks/solutions/solution_a24_transforming_features.ipynb` | Worked a24 |
| `notebooks/solutions/solution_a25_merging_combining.ipynb` | Worked a25 |
| `pyproject.toml` | Gains `pyreadstat` and `openpyxl` |
| `notebooks/README.md` | Registers the Angola series and its run order |

**Scratchpad only, never committed:**

| Path | Responsibility |
|---|---|
| `$SCRATCH/nbbuild.py` | Shared helpers that turn cell lists into `.ipynb` JSON |
| `$SCRATCH/build_a21.py` .. `build_a25.py` | One builder per notebook pair |
| `$SCRATCH/check_series.py` | Asserts headline statistics and constraint compliance |

**Data produced by running the series** (untracked, regenerable):

```
data/10_cleaned/angola_iea_2025q4_typed.csv       written by a22
data/10_cleaned/angola_iea_2025q4_clean.csv       written by a23
data/20_processed/angola_iea_2025q4_features.csv  written by a24
data/20_processed/angola_iea_2025q4_analysis.csv  written by a25 Part A
data/20_processed/angola_iea_waves_q3_q4.csv      written by a25 Part B
data/20_processed/angola_trade_partners.csv       written by a25 Part C
```

## Verified reference values

Every number below was measured against the real files during planning. The
checker script asserts them. If a number moves, the data changed and the
notebooks must be revisited, not the assertion loosened.

| Quantity | Value |
|---|---|
| Q4 raw shape | 53,353 x 206 |
| Q4 subset loaded by a21/a22 | 53,353 x 29 |
| Entirely empty columns | `hh_size_reported`, `hh_adults_reported` |
| `job_start_year` mean before / after sentinel recode | 3164.6 / 2017.4 |
| `hours_usual` max after recode | 120.0 |
| Rows surviving `dropna()` | **0** |
| Rows in duplicate person-key groups | 16 (8 pairs) |
| Shape after dedup | 53,345 x 27 |
| Rows failing `age.between(0, 100)` | 3 |
| Rows failing `hours_usual.between(0, 98)` | 45 |
| Final cleaned shape | **53,297 x 27** |
| Households with 2+ heads, before / after dedup | 6 / 1 |
| Households with no head recorded | 35 |
| `interview_date` min / max | 2024-11-10 / 2026-01-28 |
| `interview_date` NaT count | 23,671 |
| `area_type` bytes, float64 -> category | 426,956 -> 53,609 |
| Strict unemployment, weighted / unweighted | **14.5%** / 14.4% |
| Relaxed unemployment, weighted / unweighted | **31.4%** / 33.4% |
| Labour force participation, weighted | 62.7% |
| `hh_size` mean per person / per household | 5.58 / 4.09 |
| Features shape | 53,297 x 39 |
| Province codes | 10 to 30, 21 provinces |
| Rows in the 3 provinces created in 2024 (28, 29, 30) | 6,499 (12.2%) |
| Naive `concat` of full Q3 + Q4 features | 108,260 x 298, 115 cols >99% NaN |
| Harmonised wave stack | 108,260 x 13 |
| Weighted population Q3 / Q4 | 37,337,629 / 37,604,687 (0.71% apart) |
| Harmonised strict unemployment Q3 / Q4 | 11.5% / 11.9% |
| Trade sheet rows after cleaning | 249 (248 countries plus `ZZ`) |
| Largest 2025 trade surplus / deficit partner | China / Portugal |

---

## Task 1: Dependencies, notebook builder, and the failing checker

**Files:**
- Modify: `pyproject.toml`
- Create: `$SCRATCH/nbbuild.py`
- Create: `$SCRATCH/check_series.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `nbbuild.md(source) -> dict`, `nbbuild.code(source) -> dict`,
  `nbbuild.write_notebook(path, cells) -> None`, all used by Tasks 2 to 6.
  `check_series.py` is run unchanged by every later task.

- [ ] **Step 1: Write the checker, which is the failing test**

Create `$SCRATCH/check_series.py`:

```python
"""Verification gate for the Angola Lesson 2 series.

Asserts that every notebook exists, that exercise notebooks carry no outputs
and no banned constructs, and that the solution pipeline reproduces the
statistics recorded in the plan. Exit code 0 means pass.
"""

import json
import os
import sys

REPO = "/Users/gabriele/App/rowsquared/py4stat-public"
EX_DIR = os.path.join(REPO, "notebooks", "exercises")
SOL_DIR = os.path.join(REPO, "notebooks", "solutions")

STEMS = [
    "a21_loading_diagnostics",
    "a22_types_subsetting",
    "a23_cleaning_missing_duplicates",
    "a24_transforming_features",
    "a25_merging_combining",
]

BANNED = ["pathlib", "Path(", "import seaborn", "import plotly", "import duckdb",
          "import geopandas", "sklearn", "—"]

# pyreadstat is allowed only in solution/exercise a21.
PYREADSTAT_OK = "a21_loading_diagnostics"

failures = []


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def cell_text(nb):
    return "\n".join("".join(c["source"]) for c in nb["cells"])


def check_notebooks(only=None):
    """Structural checks. `only` limits to one stem so early tasks can pass."""
    stems = [s for s in STEMS if only is None or s == only]
    for stem in stems:
        ex = os.path.join(EX_DIR, f"exercise_{stem}.ipynb")
        sol = os.path.join(SOL_DIR, f"solution_{stem}.ipynb")
        for path in (ex, sol):
            if not os.path.exists(path):
                failures.append(f"missing notebook: {path}")
                continue
            nb = load(path)
            text = cell_text(nb)
            for bad in BANNED:
                if bad in text:
                    failures.append(f"{os.path.basename(path)}: banned token {bad!r}")
            if "pyreadstat" in text and stem != PYREADSTAT_OK:
                failures.append(f"{os.path.basename(path)}: pyreadstat outside a21")
        if os.path.exists(ex):
            nb = load(ex)
            for i, c in enumerate(nb["cells"]):
                if c["cell_type"] == "code" and c.get("outputs"):
                    failures.append(f"exercise_{stem}: cell {i} has outputs")
            # An exercise with no gaps is a copy of the solution, which the
            # output and token checks above cannot detect.
            text = cell_text(nb)
            if "your code here" not in text:
                failures.append(f"exercise_{stem}: no gaps, it is a copy of the solution")
            if "**Questions:**" not in text:
                failures.append(f"exercise_{stem}: no Questions block")
            if "**Answers:**" in text:
                failures.append(f"exercise_{stem}: contains an Answers block")
        if os.path.exists(ex) and os.path.exists(sol):
            if cell_text(load(ex)) == cell_text(load(sol)):
                failures.append(f"{stem}: exercise and solution are identical")
        if os.path.exists(sol):
            nb = load(sol)
            code_cells = [c for c in nb["cells"] if c["cell_type"] == "code"]
            if code_cells and not any(c.get("outputs") for c in code_cells):
                failures.append(f"solution_{stem}: executed outputs missing")


def check_statistics():
    """Assert the pipeline outputs match the values recorded in the plan."""
    import pandas as pd

    clean = os.path.join(REPO, "data", "10_cleaned", "angola_iea_2025q4_clean.csv")
    feats = os.path.join(REPO, "data", "20_processed", "angola_iea_2025q4_features.csv")
    if not os.path.exists(clean) or not os.path.exists(feats):
        failures.append("pipeline outputs not produced yet")
        return

    str_cols = {"household_id": "string", "person_no": "string",
                "cluster_id": "string", "province_code": "string"}
    df_clean = pd.read_csv(clean, dtype=str_cols)
    if df_clean.shape != (53297, 27):
        failures.append(f"cleaned shape {df_clean.shape} != (53297, 27)")

    df = pd.read_csv(feats, dtype=str_cols)
    if df.shape[0] != 53297:
        failures.append(f"features rows {df.shape[0]} != 53297")

    weight = df["weight_ind"]
    for column, expected in [("lf_status_strict", 14.5), ("lf_status_relaxed", 31.4)]:
        unemployed = df[column] == "Unemployed"
        force = df[column].isin(["Employed", "Unemployed"])
        rate = weight[unemployed].sum() / weight[force].sum() * 100
        if abs(rate - expected) > 0.15:
            failures.append(f"{column} rate {rate:.2f} != {expected}")


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    check_notebooks(only)
    if only is None:
        check_statistics()
    if failures:
        print("FAIL")
        for line in failures:
            print("  -", line)
        raise SystemExit(1)
    print("PASS")
```

- [ ] **Step 2: Run the checker to confirm it fails**

```bash
export SCRATCH=/private/tmp/claude-501/-Users-gabriele-App-rowsquared-py4stat-public/a418965a-5ef4-4814-af5f-f1eda9f94e1e/scratchpad
python3 $SCRATCH/check_series.py
```

Expected: `FAIL`, listing 10 `missing notebook:` lines plus `pipeline outputs not produced yet`. Exit code 1.

- [ ] **Step 3: Add the two dependencies**

In `pyproject.toml`, inside the `dependencies` list, insert alphabetically:

```toml
    "openpyxl>=3.1.5",
```

immediately after `"numpy==2.4.1",`, and:

```toml
    "pyreadstat>=1.3.0",
```

immediately after `"pydantic==2.12.5",`.

- [ ] **Step 4: Install and verify both readers work in the project venv**

```bash
uv sync
.venv/bin/python -c "
import pandas as pd
sav = 'data/0_raw/angola/employment_survey/IEA_2025_IV_TRIM_IND.sav'
xlsx = 'data/0_raw/angola/international_trade/Comercio Externo de Bens por Países Parceiros.xlsx'
print('sav cols:', pd.read_spss(sav, usecols=['NIDF'], convert_categoricals=False).shape)
print('xlsx sheets:', len(pd.ExcelFile(xlsx).sheet_names))
"
```

Expected: `sav cols: (53353, 1)` and `xlsx sheets: 4`. Both must succeed; a
`ModuleNotFoundError` means the sync did not take.

- [ ] **Step 5: Write the notebook builder helpers**

Create `$SCRATCH/nbbuild.py`:

```python
"""Minimal .ipynb writer, so notebook content can be authored as Python strings."""

import json


def md(source):
    """A markdown cell."""
    return {"cell_type": "markdown", "metadata": {},
            "source": source.strip("\n").splitlines(keepends=True)}


def code(source):
    """A code cell with no outputs and no execution count."""
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": source.strip("\n").splitlines(keepends=True)}


def write_notebook(path, cells):
    """Write cells to `path` as a nbformat 4.5 notebook."""
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python",
                           "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(notebook, handle, indent=1, ensure_ascii=False)
        handle.write("\n")
    print("wrote", path)


def assert_no_em_dash(cells):
    """Guard the no-em-dash constraint at build time."""
    for index, cell in enumerate(cells):
        if "—" in "".join(cell["source"]):
            raise AssertionError(f"em dash in cell {index}")
```

- [ ] **Step 6: Smoke-test the builder**

```bash
python3 -c "
import sys; sys.path.insert(0, '$SCRATCH')
import json, tempfile, os, nbbuild
cells = [nbbuild.md('# Title'), nbbuild.code('print(1)')]
nbbuild.assert_no_em_dash(cells)
p = os.path.join(tempfile.mkdtemp(), 't.ipynb')
nbbuild.write_notebook(p, cells)
nb = json.load(open(p))
print('cells:', len(nb['cells']), '| outputs empty:', nb['cells'][1]['outputs'] == [])
"
```

Expected: `cells: 2 | outputs empty: True`.

- [ ] **Step 7: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "build: add pyreadstat and openpyxl for Angola SPSS and Excel sources"
```

---

## Task 2: a21, Loading Data & First Diagnostics

**Files:**
- Create: `notebooks/solutions/solution_a21_loading_diagnostics.ipynb`
- Create: `notebooks/exercises/exercise_a21_loading_diagnostics.ipynb`
- Create: `$SCRATCH/build_a21.py`

**Interfaces:**
- Consumes: `nbbuild.md`, `nbbuild.code`, `nbbuild.write_notebook`,
  `nbbuild.assert_no_em_dash` from Task 1.
- Produces: no data file. Later notebooks do not depend on a21's output, only on
  the constants it introduces to the learner: `DATA_RAW_DIR`, `RAW_FILE`,
  and the 29-name `SPSS_COLS` list reproduced verbatim in Task 3.

- [ ] **Step 1: Write the a21 builder script**

Create `$SCRATCH/build_a21.py`. The `SOLUTION` list below is the full notebook.
The exercise version is produced in Step 4 by replacing marked cells.

```python
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbbuild import assert_no_em_dash, code, md, write_notebook

REPO = "/Users/gabriele/App/rowsquared/py4stat-public"

TITLE = """
# Solution 2.1: Loading Data & First Diagnostics (Angola IEA)

This notebook uses `IEA_2025_IV_TRIM_IND.sav`, the individual file of the
Inquerito ao Emprego em Angola (IEA), 4th quarter 2025, published by INE Angola.

It is a real SPSS export: 53,353 people, 206 columns, all variable and value
labels in Portuguese.

You will practice:
- Loading an SPSS file with `pd.read_spss()`
- Deciding whether to apply the file's value labels, and seeing what that costs
- Reading the codebook that ships inside the file
- Loading only the columns you need with `usecols`
- Running structural diagnostics with `info()`, `describe()` and `value_counts()`
- Spotting sentinel codes and empty columns before any cleaning

> **Pipeline:** this notebook only reads `0_raw/`. It writes nothing.
"""

PATHS_MD = """
### Path Setup (run first)

> Use `os.path.join` for path construction.
> Required base path: `DATA_RAW_DIR = '../../data/0_raw/angola/employment_survey'`.
"""

PATHS_CODE = """
import os

import matplotlib.pyplot as plt
import pandas as pd

DATA_RAW_DIR = '../../data/0_raw/angola/employment_survey'
RAW_FILE = 'IEA_2025_IV_TRIM_IND.sav'
raw_path = os.path.join(DATA_RAW_DIR, RAW_FILE)

pd.set_option('display.float_format', lambda x: f'{x:,.2f}')
print('Data path:', raw_path)
print('Exists?:', os.path.exists(raw_path))
"""

T1_MD = """
---

## Task 1: Load the file and take a first look

`pd.read_spss()` reads SPSS `.sav` files. By default it applies the value labels
stored in the file, so coded variables come back as readable text.
"""

T1_CODE = """
df_labelled = pd.read_spss(raw_path)

print('Shape:', df_labelled.shape)
df_labelled[['PROV', 'AREA_RESID', 'DEM_SEX', 'DEM_AGE']].head()
"""

T1B_CODE = """
df_labelled[['PROV', 'AREA_RESID', 'DEM_SEX']].tail()
"""

T1C_CODE = """
df_labelled[['PROV', 'AREA_RESID', 'DEM_SEX', 'DEM_AGE']].sample(5, random_state=0)
"""

T1_Q = """
**Answers:**

- The file holds 53,353 rows and 206 columns, one row per person interviewed.
- `PROV`, `AREA_RESID` and `DEM_SEX` arrive as readable Portuguese text
  (`Luanda`, `Urbana`, `Feminino`) rather than the numeric codes actually stored
  in the file, because `pd.read_spss` applies value labels by default.
- 206 columns is far more than any single analysis needs, which is what Task 4
  addresses.
"""

T2_MD = """
---

## Task 2: The cost of applying value labels

Value labels are convenient, but they are applied to **every** labelled variable,
including ones where the label is a sentinel rather than a category. Reload with
`convert_categoricals=False` and compare the dtypes.
"""

T2_CODE = """
df_raw = pd.read_spss(raw_path, convert_categoricals=False)

comparison = pd.DataFrame({
    'labelled': df_labelled[['PROV', 'DEM_SEX', 'MJT_SYR', 'DEM_AGE']].dtypes,
    'raw_codes': df_raw[['PROV', 'DEM_SEX', 'MJT_SYR', 'DEM_AGE']].dtypes,
})
comparison
"""

T2B_CODE = """
# MJT_SYR is the year the person started their main job.
print('Labelled, first 5 values:')
print(df_labelled['MJT_SYR'].head().tolist())
print()
print('Raw codes, describe:')
print(df_raw['MJT_SYR'].describe())
"""

T2_Q = """
**Answers:**

- `MJT_SYR` is a **year**, but the labelled load returns it as `category`. That
  happens because the value `9997` carries the label `NAO SABE`, so pandas treats
  the whole column as categorical. A year you cannot subtract is useless.
- The raw load returns `float64` and `describe()` immediately exposes the damage:
  a mean of 3164.6 against a real range of 1965 to 2025.
- The rest of this series uses `convert_categoricals=False`, so the codes stay
  numeric and we decode them ourselves in 2.4. That is the same choice the Stata
  callout in the lesson recommends with `convert_categoricals=False`.
"""

T3_MD = """
---

## Task 3: Read the codebook that ships inside the file

An SPSS file carries its own documentation: a label for every variable, and a
label for every coded value. The lesson shows this for Stata with
`variable_labels()`. For SPSS the equivalent lives in `pyreadstat`, and it can be
read **without loading the data**.

> This is the only cell in the whole series that imports `pyreadstat` directly.
"""

T3_CODE = """
import pyreadstat

_, meta = pyreadstat.read_sav(raw_path, metadataonly=True)

for name in ['PROV', 'AREA_RESID', 'DEM_SEX', 'DEM_AGE', 'WKT_USHRSTOT', 'MJT_SYR']:
    print(f'{name:15s} {meta.column_names_to_labels[name]}')
"""

T3B_CODE = """
# Value labels: the code to text mapping behind each categorical variable
label_set = meta.variable_to_label['PROV']
print('PROV has', len(meta.value_labels[label_set]), 'provinces')
print(meta.value_labels[label_set])
"""

T3_Q = """
**Answers:**

- Without the codebook, `WKT_USHRSTOT` is meaningless. With it, we know it is
  "Quantas horas o(a) nome geralmente trabalha por semana no total?", the usual
  weekly hours across all jobs.
- `PROV` maps 21 codes, 10 to 30, onto province names. Note that Angola created
  three new provinces in 2024: Icolo e Bengo (28), Moxico Leste (29) and Cuando
  (30). Any lookup table built before 2024 will be missing them, which is exactly
  the merge problem waiting in 2.5.
- Reading metadata only is fast because no data is loaded, so it is the cheapest
  possible first step with an unfamiliar file.
"""

T4_MD = """
---

## Task 4: Load only the columns you need with `usecols`

206 columns is more than this analysis needs. `usecols` tells the reader to skip
the rest entirely, so they never enter memory.

The 29 columns below carry the survey's demographic core, its labour module, the
interview date, and the survey weight.
"""

T4_CODE = """
SPSS_COLS = [
    'NIDF', 'PPNO', 'G_06_ID_IEA', 'PROV', 'AREA_RESID', 'G_15_TRIMESTRE',
    'DEM_REL', 'DEM_SEX', 'DEM_AGE', 'DEM_MRT', 'DEM_EDL', 'S03_01',
    'ATW_PAY', 'ATW_PFT', 'ATW_FAM', 'ABS_JOB',
    'SRH_JOB', 'SRH_BUS', 'SRH_AVN', 'SRH_AVL', 'SRH_DES',
    'WKT_USHRSTOT', 'WKT_ACHRSTOT', 'MJT_SYR', 'MJJ_EMP_REL', 'GHVEDT',
    'POND_IEA_IV_TRIM_2025_IND', 'G_12', 'G_13',
]

df = pd.read_spss(raw_path, usecols=SPSS_COLS, convert_categoricals=False)
print('Full file: ', df_raw.shape)
print('Subset:    ', df.shape)
df.head()
"""

T4B_CODE = """
full_mb = df_raw.memory_usage(deep=True).sum() / 1e6
subset_mb = df.memory_usage(deep=True).sum() / 1e6
print(f'Memory full:   {full_mb:8.2f} MB')
print(f'Memory subset: {subset_mb:8.2f} MB')
print(f'Saved:         {(1 - subset_mb / full_mb) * 100:8.1f}%')
"""

T4_Q = """
**Answers:**

- The subset keeps all 53,353 rows but only 29 of 206 columns, cutting memory by
  roughly 90%.
- `usecols` skips columns at read time. Loading everything and then selecting
  with `df[COLS]` produces the same table but pays the full memory and time cost
  first, which matters when the file is larger than this one.
- A misspelled name in `SPSS_COLS` raises an error rather than being ignored,
  which is what you want.
"""

T5_MD = """
---

## Task 5: Structural health check with `info()`

`df.info()` is the first diagnostic. Read the Non-Null Count column carefully:
it is where empty columns and skip patterns show up.
"""

T5_CODE = """
df.info()
"""

T5B_CODE = """
missing = pd.DataFrame({
    'n_missing': df.isna().sum(),
    'pct_missing': (df.isna().mean() * 100).round(1),
}).sort_values('pct_missing', ascending=False)
missing
"""

T5_Q = """
**Answers:**

- `G_12` and `G_13` are **100% missing**: 53,353 nulls out of 53,353 rows. They
  should hold household size and the number of adults, so they look useful in a
  column list and are worth nothing in practice. They get dropped in 2.3.
- The labour module columns (`MJT_SYR`, `WKT_USHRSTOT`, `MJJ_EMP_REL`) are around
  78% missing, and `SRH_AVL` is 98.5% missing. This is **not** damage. Those
  questions are only asked of people the questionnaire routes to them. Missing by
  design and missing by error need completely different treatment, which is the
  main lesson of 2.3.
- Everything is `float64`, including the identifiers `NIDF` and `PPNO` and the
  date `GHVEDT`. All three are wrong types, fixed in 2.2.
"""

T6_MD = """
---

## Task 6: Summary statistics with `describe()`

`describe()` exposes impossible values. Look hard at every `min` and `max`.
"""

T6_CODE = """
df[['DEM_AGE', 'WKT_USHRSTOT', 'WKT_ACHRSTOT', 'MJT_SYR', 'GHVEDT']].describe().T
"""

T6B_CODE = """
df.describe(include='all').T
"""

T6_Q = """
**Answers:**

- `MJT_SYR` has a mean of 3164.6 and a max of 9997. `9997` is the "NAO SABE"
  sentinel and there are 1,673 of them, dragging the mean nearly 1,150 years into
  the future.
- `WKT_USHRSTOT` maxes at 997, the same sentinel pattern. Its real maximum is 120
  hours a week, which is itself implausible and gets a validation rule in 2.3.
- `DEM_AGE` runs from 0 to 120. Age 0 is legitimate: 1,532 infants. Age 120 is
  not.
- `GHVEDT` has a mean around 20,251,000, which is nonsense as a number because it
  is really the date 2025-12-04 stored as the digits `20251204`.
"""

T7_MD = """
---

## Task 7: Explore categories with `value_counts()`

`value_counts()` is the fastest way to see what is actually in a coded column.
Always pass `dropna=False` so the gaps are counted too.
"""

T7_CODE = """
print(df['PROV'].value_counts(dropna=False).sort_index())
"""

T7B_CODE = """
print(df['AREA_RESID'].value_counts(dropna=False))
print()
print(df['DEM_SEX'].value_counts(dropna=False))
print()
print(df['DEM_EDL'].value_counts(dropna=False).sort_index())
"""

T7C_CODE = """
print('Distinct households:', df['NIDF'].nunique())
print('Rows per household, describe:')
print(df['NIDF'].value_counts().describe())
"""

T7_Q = """
**Answers:**

- All 21 province codes appear, from 10 to 30, with Luanda (14) the largest at
  4,424 people.
- `AREA_RESID` splits 34,173 urban and 19,180 rural. `DEM_SEX` splits 25,601 male
  and 27,752 female.
- `DEM_EDL` is 56.6% missing and its codes jump from 7 to 9, with no 8. Reading
  the codebook explains it: 9 means "Nenhum nivel", no level, so it is not an
  ordinal step above 7.
- There are 13,036 households across 53,353 people, a mean of 4.09 people each.
  Remember this number: 2.4 derives household size a different way and gets 5.58,
  for a reason worth understanding.
"""

T8_MD = """
---

## Task 8: A quick visual sweep

Histograms of every numeric column at once are a fast way to spot sentinels: they
appear as a lonely spike far to the right of everything else.
"""

T8_CODE = """
df[['DEM_AGE', 'WKT_USHRSTOT', 'WKT_ACHRSTOT', 'MJT_SYR',
    'DEM_EDL', 'POND_IEA_IV_TRIM_2025_IND']].hist(bins=30, figsize=(14, 8))
plt.tight_layout()
plt.show()
"""

T8_Q = """
**Answers:**

- `MJT_SYR` and `WKT_USHRSTOT` both show a tiny bar at the far right, isolated
  from the rest of the distribution. That shape is the visual signature of a
  sentinel code.
- `DEM_AGE` is heavily skewed towards the young, which is expected for Angola:
  the median age in this sample is 17.
- None of these columns is ready for analysis yet. 2.2 fixes the types and 2.3
  removes the sentinels.
"""

SOLUTION = [
    md(TITLE), md(PATHS_MD), code(PATHS_CODE),
    md(T1_MD), code(T1_CODE), code(T1B_CODE), code(T1C_CODE), md(T1_Q),
    md(T2_MD), code(T2_CODE), code(T2B_CODE), md(T2_Q),
    md(T3_MD), code(T3_CODE), code(T3B_CODE), md(T3_Q),
    md(T4_MD), code(T4_CODE), code(T4B_CODE), md(T4_Q),
    md(T5_MD), code(T5_CODE), code(T5B_CODE), md(T5_Q),
    md(T6_MD), code(T6_CODE), code(T6B_CODE), md(T6_Q),
    md(T7_MD), code(T7_CODE), code(T7B_CODE), code(T7C_CODE), md(T7_Q),
    md(T8_MD), code(T8_CODE), md(T8_Q),
]

if __name__ == "__main__":
    assert_no_em_dash(SOLUTION)
    write_notebook(
        os.path.join(REPO, "notebooks", "solutions",
                     "solution_a21_loading_diagnostics.ipynb"),
        SOLUTION,
    )
```

- [ ] **Step 2: Build the solution notebook**

```bash
python3 $SCRATCH/build_a21.py
```

Expected: `wrote /Users/gabriele/App/rowsquared/py4stat-public/notebooks/solutions/solution_a21_loading_diagnostics.ipynb`

- [ ] **Step 3: Execute the solution and confirm the diagnostics**

```bash
cd notebooks/solutions && python3 -m jupyter nbconvert --to notebook --execute \
  --inplace --ExecutePreprocessor.timeout=600 solution_a21_loading_diagnostics.ipynb
```

Expected: exit code 0. Then confirm the key numbers appeared:

```bash
python3 -c "
import json
nb = json.load(open('notebooks/solutions/solution_a21_loading_diagnostics.ipynb'))
text = ''.join(''.join(o.get('text', '')) for c in nb['cells'] for o in c.get('outputs', []) if o.get('output_type') == 'stream')
for token in ['53353', '3164.6', '13036']:
    print(token, 'found' if token in text.replace(',', '') else 'MISSING')
"
```

Expected: all three `found`.

- [ ] **Step 4: Derive the exercise notebook**

Append to `$SCRATCH/build_a21.py` a second entry point that rewrites the marked
code cells as gaps and the `**Answers:**` blocks as `**Questions:**`:

```python
EXERCISE_TITLE = TITLE.replace("# Solution 2.1:", "# Exercise 2.1:")

GAPS = {
    PATHS_CODE: PATHS_CODE.replace(
        "DATA_RAW_DIR = '../../data/0_raw/angola/employment_survey'",
        "DATA_RAW_DIR =   # your code here",
    ).replace("RAW_FILE = 'IEA_2025_IV_TRIM_IND.sav'", "RAW_FILE =   # your code here"),
    T1_CODE: T1_CODE.replace("df_labelled = pd.read_spss(raw_path)",
                             "df_labelled =   # your code here"),
    T1B_CODE: "df_labelled[['PROV', 'AREA_RESID', 'DEM_SEX']].  # your code here",
    T1C_CODE: "# Show a random sample of 5 rows (use random_state=0)\n"
              "df_labelled[['PROV', 'AREA_RESID', 'DEM_SEX', 'DEM_AGE']].  # your code here",
    T2_CODE: T2_CODE.replace(
        "df_raw = pd.read_spss(raw_path, convert_categoricals=False)",
        "df_raw = pd.read_spss(  # your code here: convert_categoricals=False )",
    ),
    T3_CODE: T3_CODE.replace(
        "_, meta = pyreadstat.read_sav(raw_path, metadataonly=True)",
        "_, meta = pyreadstat.read_sav(  # your code here: metadataonly=True )",
    ),
    T4_CODE: T4_CODE.replace(
        "df = pd.read_spss(raw_path, usecols=SPSS_COLS, convert_categoricals=False)",
        "df = pd.read_spss(  # your code here: usecols=SPSS_COLS, convert_categoricals=False )",
    ),
    T5_CODE: "df.  # your code here",
    T6_CODE: "df[['DEM_AGE', 'WKT_USHRSTOT', 'WKT_ACHRSTOT', 'MJT_SYR', 'GHVEDT']].  # your code here",
    T6B_CODE: "df.describe(  # your code here: include='all' ).T",
    T7_CODE: "print(df['PROV'].  # your code here: value_counts(dropna=False).sort_index() )",
    T8_CODE: T8_CODE.replace("bins=30, figsize=(14, 8)", "  # your code here: bins=30, figsize=(14, 8)"),
}

ANSWER_TO_QUESTION = {
    T1_Q: """
**Questions:**

- How many rows and columns does the file have? What is one row?
- Look at `PROV` and `DEM_SEX`. Are they text or numbers? Why?
- Is 206 columns a problem? For what?
""",
    T2_Q: """
**Questions:**

- What dtype does the labelled load give `MJT_SYR`? It is a year. Is that dtype
  usable for arithmetic?
- Run `describe()` on the raw `MJT_SYR`. What is the mean, and why is it not a
  plausible year?
- Which loading mode should the rest of this pipeline use, and why?
""",
    T3_Q: """
**Questions:**

- What does `WKT_USHRSTOT` actually measure? Could you have guessed from the name?
- How many provinces does `PROV` code, and what is the code range?
- Why read the metadata without loading the data?
""",
    T4_Q: """
**Questions:**

- How much memory did `usecols` save?
- What is the difference between `usecols` and loading everything then selecting?
- What happens if you misspell a name in `SPSS_COLS`? Try it.
""",
    T5_Q: """
**Questions:**

- Which two columns are entirely empty? What were they supposed to contain?
- The labour columns are around 78% missing. Is that damage, or something else?
  What decides the answer?
- `NIDF`, `PPNO` and `GHVEDT` are all `float64`. Is that right for any of them?
""",
    T6_Q: """
**Questions:**

- `MJT_SYR` has a mean of over 3000. What value is doing that, and how many are there?
- Find the same pattern in `WKT_USHRSTOT`. What is the sentinel?
- `DEM_AGE` runs 0 to 120. Which end is a real value and which is not?
""",
    T7_Q: """
**Questions:**

- How many province codes appear, and which province is largest?
- `DEM_EDL` codes go 1 to 7 and then 9, with no 8. Check the codebook: why?
- How many households are there, and how many people per household on average?
""",
    T8_Q: """
**Questions:**

- Two histograms show an isolated bar at the far right. Which, and what is it?
- What does the shape of the `DEM_AGE` distribution tell you about Angola?
- Is any of this data ready for analysis yet?
""",
}


def normalise_keys(mapping):
    """Strip leading and trailing newlines from every key.

    nbbuild.code() and nbbuild.md() strip those newlines before storing a
    cell's source, but the GAPS and ANSWER_TO_QUESTION keys are the raw
    triple-quoted constants, which still carry them. Without this the lookup
    misses on every single cell and build_exercise() silently emits a verbatim
    copy of the solution.
    """
    return {key.strip("\n"): value for key, value in mapping.items()}


def build_exercise():
    gaps = normalise_keys(GAPS)
    answers = normalise_keys(ANSWER_TO_QUESTION)

    cells = []
    for cell in SOLUTION:
        source = "".join(cell["source"])
        if cell["cell_type"] == "code":
            cells.append(code(gaps.get(source, source)))
        elif source.startswith("# Solution 2.1:"):
            cells.append(md(EXERCISE_TITLE))
        else:
            cells.append(md(answers.get(source, source)))

    assert_no_em_dash(cells)

    # The gapping must not be a no-op. Fail loudly rather than shipping a
    # copy of the solution as the exercise.
    text = "\n".join("".join(c["source"]) for c in cells)
    gap_count = text.count("your code here")
    assert gap_count >= len(GAPS), f"only {gap_count} gaps for {len(GAPS)} entries"
    assert "**Questions:**" in text, "Answers were not converted to Questions"
    assert "**Answers:**" not in text, "an Answers block survived into the exercise"

    write_notebook(
        os.path.join(REPO, "notebooks", "exercises",
                     "exercise_a21_loading_diagnostics.ipynb"),
        cells,
    )
```

**This `normalise_keys` helper and the three assertions are required in every
builder from here on.** Tasks 3 to 6 define their own `GAPS` and
`ANSWER_TO_QUESTION` dicts and must use the identical pattern, adjusting only
the title prefix (`# Solution 2.2:` and so on) and the output path. Without the
normalisation the exercise notebook is a verbatim copy of the solution, and
because `check_series.py` only inspects outputs and banned tokens, the checker
will report PASS on that broken artifact.

Change the `__main__` block to call both `write_notebook(...)` for the solution
and `build_exercise()`. Note that `build_exercise()` must run **before** the
solution notebook is executed, or rerun from the unexecuted cell list, because
executing the solution in place adds outputs. The simplest order is: build both
files first, then execute only the solution.

Rerun:

```bash
python3 $SCRATCH/build_a21.py
```

- [ ] **Step 5: Re-execute the solution, since Step 4 overwrote it**

```bash
cd notebooks/solutions && python3 -m jupyter nbconvert --to notebook --execute \
  --inplace --ExecutePreprocessor.timeout=600 solution_a21_loading_diagnostics.ipynb
```

Expected: exit code 0.

- [ ] **Step 6: Run the checker for a21**

```bash
python3 $SCRATCH/check_series.py a21_loading_diagnostics
```

Expected: `PASS`.

- [ ] **Step 7: Commit**

```bash
git add notebooks/exercises/exercise_a21_loading_diagnostics.ipynb \
        notebooks/solutions/solution_a21_loading_diagnostics.ipynb
git commit -m "feat(notebooks): add Angola a21 loading and diagnostics exercise"
```

---

## Task 3: a22, Data Types and Subsetting

**Files:**
- Create: `notebooks/solutions/solution_a22_types_subsetting.ipynb`
- Create: `notebooks/exercises/exercise_a22_types_subsetting.ipynb`
- Create: `$SCRATCH/build_a22.py`
- Produces data: `data/10_cleaned/angola_iea_2025q4_typed.csv`

**Interfaces:**
- Consumes: `nbbuild` helpers; the `SPSS_COLS` list from Task 2, repeated verbatim
  below because the implementer may be reading tasks out of order.
- Produces: `angola_iea_2025q4_typed.csv`, 53,353 rows x 29 columns, with
  `household_id`, `person_no`, `cluster_id`, `province_code` as strings and
  `interview_date` as a datetime. Task 4 reads exactly this file. The
  `RENAME_MAP` defined here fixes the English column names used by Tasks 4, 5
  and 6.

- [ ] **Step 1: Write the a22 builder**

Create `$SCRATCH/build_a22.py` following the same shape as `build_a21.py`
(imports from `nbbuild`, a `SOLUTION` list, a `GAPS` dict, an
`ANSWER_TO_QUESTION` dict, and a `build_exercise()`). The cell sources are:

```python
TITLE = """
# Solution 2.2: Data Types and Subsetting (Angola IEA)

This notebook continues with the Q4 2025 IEA file. Using only the tools from
Lesson 2.2, you fix the data types and save a **typed checkpoint** that the
cleaning step (2.3) picks up.

You will practice:
- Telling a DataFrame from a Series, and checking dtypes
- Renaming 29 Portuguese variable names to readable English ones
- Keeping identifiers as text, including the float to int to string route
- Converting a YYYYMMDD number into a real date with `pd.to_datetime()`
- Saving memory with the `category` dtype
- Subsetting to inspect problems, not yet to fix them
- Saving a typed checkpoint to `10_cleaned/`

> **Pipeline:** reads `0_raw/`, writes `10_cleaned/angola_iea_2025q4_typed.csv`.
> Exercise 2.3 reads that file.
"""

PATHS_CODE = """
import os

import numpy as np
import pandas as pd

DATA_RAW_DIR = '../../data/0_raw/angola/employment_survey'
DATA_CLEAN_DIR = '../../data/10_cleaned'
RAW_FILE = 'IEA_2025_IV_TRIM_IND.sav'
raw_path = os.path.join(DATA_RAW_DIR, RAW_FILE)

SPSS_COLS = [
    'NIDF', 'PPNO', 'G_06_ID_IEA', 'PROV', 'AREA_RESID', 'G_15_TRIMESTRE',
    'DEM_REL', 'DEM_SEX', 'DEM_AGE', 'DEM_MRT', 'DEM_EDL', 'S03_01',
    'ATW_PAY', 'ATW_PFT', 'ATW_FAM', 'ABS_JOB',
    'SRH_JOB', 'SRH_BUS', 'SRH_AVN', 'SRH_AVL', 'SRH_DES',
    'WKT_USHRSTOT', 'WKT_ACHRSTOT', 'MJT_SYR', 'MJJ_EMP_REL', 'GHVEDT',
    'POND_IEA_IV_TRIM_2025_IND', 'G_12', 'G_13',
]

df = pd.read_spss(raw_path, usecols=SPSS_COLS, convert_categoricals=False)

pd.set_option('display.float_format', lambda x: f'{x:,.2f}')
print('Loaded:', df.shape)
df.head()
"""

T1_MD = """
---

## Task 1: DataFrame vs Series

Selecting one column returns a **Series**, a one dimensional object with its own
dtype and its own methods. `.str`, `.dt` and `.value_counts()` all belong to
Series, not to the whole DataFrame.
"""

T1_CODE = """
print(type(df))
print(type(df['DEM_AGE']))
"""

T1B_CODE = """
df.dtypes
"""

T1_Q = """
**Answers:**

- Every one of the 29 columns is `float64`, because SPSS stores everything
  numerically and we asked for raw codes.
- `NIDF` is a household identifier, so `float64` is wrong: identifiers are labels,
  not quantities.
- `GHVEDT` is a date stored as the number 20251204. Nothing date-like works on it
  until it is converted.
"""

T2_MD = """
---

## Task 2: Rename the columns

The SPSS names come from the questionnaire, not from the analysis. `PROV` and
`ATW_PAY` are precise but unreadable. Rename once, here, and every later notebook
is easier to follow.
"""

T2_CODE = """
RENAME_MAP = {
    'NIDF': 'household_id', 'PPNO': 'person_no', 'G_06_ID_IEA': 'cluster_id',
    'PROV': 'province_code', 'AREA_RESID': 'area_type', 'G_15_TRIMESTRE': 'quarter',
    'DEM_REL': 'rel_to_head', 'DEM_SEX': 'sex', 'DEM_AGE': 'age',
    'DEM_MRT': 'marital_status', 'DEM_EDL': 'education_level',
    'S03_01': 'school_attendance', 'ATW_PAY': 'worked_for_pay',
    'ATW_PFT': 'worked_own_account', 'ATW_FAM': 'worked_family_business',
    'ABS_JOB': 'absent_from_job', 'SRH_JOB': 'sought_work',
    'SRH_BUS': 'sought_business', 'SRH_AVN': 'available_now',
    'SRH_AVL': 'available_2wk', 'SRH_DES': 'wants_work',
    'WKT_USHRSTOT': 'hours_usual', 'WKT_ACHRSTOT': 'hours_actual',
    'MJT_SYR': 'job_start_year', 'MJJ_EMP_REL': 'employment_relation',
    'GHVEDT': 'interview_date', 'POND_IEA_IV_TRIM_2025_IND': 'weight_ind',
    'G_12': 'hh_size_reported', 'G_13': 'hh_adults_reported',
}

df = df.rename(columns=RENAME_MAP)
print(df.columns.tolist())
"""

T2_Q = """
**Answers:**

- All 29 names changed. `rename` only touches keys it finds, so a typo in the
  dictionary fails silently: the old name simply survives. Printing the result is
  the check.
- `available_now` and `available_2wk` are deliberately distinguished. They are two
  different questions and 2.4 needs both.
"""

T3_MD = """
---

## Task 3: Keep identifiers as text

`household_id` arrives as `9250068.0`. Converting straight to string would keep
the `.0`, so the route is float to integer to string.

`province_code` gets the same treatment plus `zfill(2)`. Angola's province codes
run 10 to 30, so `zfill(2)` changes nothing today. It is a documented safeguard,
the same way you would pad any code that could gain a single digit value later.
"""

T3_CODE = """
print('Before:', df['household_id'].head(3).tolist())

for col in ['household_id', 'person_no', 'cluster_id']:
    df[col] = df[col].astype('int64').astype('string')

df['province_code'] = df['province_code'].astype('int64').astype('string').str.zfill(2)

print('After: ', df['household_id'].head(3).tolist())
print('Provinces:', sorted(df['province_code'].unique()))
"""

T3_Q = """
**Answers:**

- Without the `int64` step you get `'9250068.0'`, which will not join to anything.
- The codes are `'10'` through `'30'`, 21 provinces. `zfill(2)` is a no-op on this
  file and that is fine: it documents the intent and protects a future extract.
- You never add or average an identifier, so storing it as a number invites
  exactly one kind of bug and prevents none.
"""

T4_MD = """
---

## Task 4: Convert the interview date

`interview_date` is the float `20251204.0`, meaning 2025-12-04. Convert through
`Int64` (which tolerates the missing values) to string, then parse with an
explicit format.
"""

T4_CODE = """
print('Raw values:', df['interview_date'].dropna().head(3).tolist())

date_text = df['interview_date'].astype('Int64').astype('string')
df['interview_date'] = pd.to_datetime(date_text, format='%Y%m%d', errors='raise')

print('dtype:', df['interview_date'].dtype)
print('Range:', df['interview_date'].min(), 'to', df['interview_date'].max())
print('Missing (NaT):', df['interview_date'].isna().sum())
"""

T4B_CODE = """
# The .dt accessor unlocks date parts
print(df['interview_date'].dt.month.value_counts(dropna=False).sort_index())
"""

T4_Q = """
**Answers:**

- The range is **2024-11-10 to 2026-01-28**. For a survey labelled 4th quarter
  2025, both ends are impossible: they fall outside October to December 2025. The
  month counts show the bulk in October, November and December 2025 with a thin
  tail outside. This is a genuine data quality finding to report, and 2.3 adds a
  rule for it.
- 23,671 rows have `NaT`. The date is only recorded for the labour module
  respondents, not for every household member.
- `NaT` is the datetime equivalent of `NaN`. Arithmetic on it propagates rather
  than raising.
"""

T5_MD = """
---

## Task 5: Save memory with `category`

`area_type` holds two distinct values repeated 53,353 times. The `category` dtype
stores each label once and keeps small integer codes alongside.
"""

T5_CODE = """
before = df['area_type'].memory_usage(deep=True)
after = df['area_type'].astype('category').memory_usage(deep=True)

print(f'float64:  {before:,} bytes')
print(f'category: {after:,} bytes')
print(f'Saved:    {(1 - after / before) * 100:.1f}%')
"""

T5_Q = """
**Answers:**

- 426,956 bytes down to 53,609, an 87% saving on that one column.
- We do **not** persist the category conversion here. The checkpoint is a CSV, and
  CSV has no dtype system, so the saving would be thrown away on the next read.
  It is worth doing in memory on a wide file.
"""

T6_MD = """
---

## Task 6: Subset to inspect the problems

Filtering here is for **looking**, not fixing. 2.3 makes the removal decisions.
"""

T6_CODE = """
# Implausible working weeks
print('hours_usual > 100:', (df['hours_usual'] > 100).sum())
df[df['hours_usual'] > 100][['household_id', 'hours_usual', 'hours_actual']].head()
"""

T6B_CODE = """
# Combine conditions: each one needs its own parentheses
old_and_working = df[(df['age'] >= 65) & (df['hours_usual'] > 40)]
print('People 65+ working over 40 hours:', len(old_and_working))
old_and_working[['household_id', 'age', 'hours_usual']].head()
"""

T6C_CODE = """
# isin() for a set of provinces: Luanda and Benguela
target = df[df['province_code'].isin(['14', '23'])]
print('Rows in Luanda or Benguela:', len(target))

# str.contains() is safe with missing values when na=False
print('Codes containing "1":', df[df['province_code'].str.contains('1', na=False)]['province_code'].nunique())
"""

T6_Q = """
**Answers:**

- 45 people report more than 100 usual hours a week. That is over 14 hours every
  day with no day off. Not impossible to record, but implausible enough for a rule.
- 6,900 rows fall in Luanda or Benguela.
- Each condition needs parentheses because `&` binds tighter than `>` in Python,
  so `df['age'] >= 65 & df['hours_usual'] > 40` parses in the wrong order and
  raises.
- `na=False` makes a missing value count as "does not match" instead of
  propagating `NaN` into the mask, which would raise on indexing.
"""

T7_MD = """
---

## Task 7: Save the typed checkpoint

Types are fixed. Save so 2.3 starts from a stable baseline.

> Never write into `0_raw/`. This goes to `10_cleaned/`.
"""

T7_CODE = """
os.makedirs(DATA_CLEAN_DIR, exist_ok=True)
out_path = os.path.join(DATA_CLEAN_DIR, 'angola_iea_2025q4_typed.csv')

df.to_csv(out_path, index=False)
print('Saved:', out_path, '|', df.shape)
"""

T7B_CODE = """
check = pd.read_csv(out_path, dtype={
    'household_id': 'string', 'person_no': 'string',
    'cluster_id': 'string', 'province_code': 'string',
})
print('Reloaded:', check.shape)
print('interview_date dtype after reload:', check['interview_date'].dtype)
check[['household_id', 'province_code', 'interview_date']].head()
"""

T7_Q = """
**Answers:**

- The checkpoint is 53,353 rows by 29 columns. Nothing has been removed yet: this
  step fixed types only.
- `interview_date` reloads as `object`, plain text. CSV cannot store a datetime,
  so every notebook that reads this file must parse it again. That is the price
  of a portable format, and it is why the `dtype=` argument is needed for the
  identifier columns too.
- `index=False` stops pandas writing the row numbers as a nameless first column,
  which would reappear as `Unnamed: 0` on the next read.
"""
```

Assemble as:

```python
SOLUTION = [
    md(TITLE), md("### Path Setup (run first)"), code(PATHS_CODE),
    md(T1_MD), code(T1_CODE), code(T1B_CODE), md(T1_Q),
    md(T2_MD), code(T2_CODE), md(T2_Q),
    md(T3_MD), code(T3_CODE), md(T3_Q),
    md(T4_MD), code(T4_CODE), code(T4B_CODE), md(T4_Q),
    md(T5_MD), code(T5_CODE), md(T5_Q),
    md(T6_MD), code(T6_CODE), code(T6B_CODE), code(T6C_CODE), md(T6_Q),
    md(T7_MD), code(T7_CODE), code(T7B_CODE), md(T7_Q),
]
```

Gaps to apply in `GAPS` (each replaces the full solution line with a prompt):

| Cell | Solution line | Exercise line |
|---|---|---|
| `T1B_CODE` | `df.dtypes` | `df.  # your code here` |
| `T2_CODE` | `df = df.rename(columns=RENAME_MAP)` | `df = df.  # your code here: rename with RENAME_MAP` |
| `T3_CODE` | `df[col] = df[col].astype('int64').astype('string')` | `df[col] = df[col].  # your code here: int64 then string` |
| `T3_CODE` | the `province_code` line | `df['province_code'] =   # your code here: int64, string, then .str.zfill(2)` |
| `T4_CODE` | the `pd.to_datetime` line | `df['interview_date'] = pd.to_datetime(  # your code here: format='%Y%m%d', errors='raise' )` |
| `T5_CODE` | `after = df['area_type'].astype('category')...` | `after = df['area_type'].  # your code here: astype('category').memory_usage(deep=True)` |
| `T6C_CODE` | `df['province_code'].isin(['14', '23'])` | `df['province_code'].  # your code here: isin(['14', '23'])` |
| `T7_CODE` | `df.to_csv(out_path, index=False)` | `df.  # your code here: to_csv with index=False` |

- [ ] **Step 2: Build both notebooks**

```bash
python3 $SCRATCH/build_a22.py
```

Expected: two `wrote ...` lines, solution then exercise.

- [ ] **Step 3: Execute the solution**

```bash
cd notebooks/solutions && python3 -m jupyter nbconvert --to notebook --execute \
  --inplace --ExecutePreprocessor.timeout=600 solution_a22_types_subsetting.ipynb
```

Expected: exit code 0.

- [ ] **Step 4: Verify the checkpoint it produced**

```bash
python3 -c "
import pandas as pd
p = 'data/10_cleaned/angola_iea_2025q4_typed.csv'
df = pd.read_csv(p, dtype={'household_id':'string','province_code':'string'})
print('shape:', df.shape)
print('household_id sample:', df['household_id'].head(2).tolist())
print('provinces:', df['province_code'].nunique())
assert df.shape == (53353, 29), df.shape
assert not df['household_id'].str.contains(r'\\.').any(), 'float residue in ids'
assert df['province_code'].nunique() == 21
print('OK')
"
```

Expected:

```
shape: (53353, 29)
household_id sample: ['9250068', '12870026']
provinces: 21
OK
```

- [ ] **Step 5: Run the checker for a22**

```bash
python3 $SCRATCH/check_series.py a22_types_subsetting
```

Expected: `PASS`.

- [ ] **Step 6: Commit**

```bash
git add notebooks/exercises/exercise_a22_types_subsetting.ipynb \
        notebooks/solutions/solution_a22_types_subsetting.ipynb
git commit -m "feat(notebooks): add Angola a22 data types and subsetting exercise"
```

---

## Task 4: a23, Cleaning, Missing Values and Duplicates

**Files:**
- Create: `notebooks/solutions/solution_a23_cleaning_missing_duplicates.ipynb`
- Create: `notebooks/exercises/exercise_a23_cleaning_missing_duplicates.ipynb`
- Create: `$SCRATCH/build_a23.py`
- Reads data: `data/10_cleaned/angola_iea_2025q4_typed.csv`
- Produces data: `data/10_cleaned/angola_iea_2025q4_clean.csv`

**Interfaces:**
- Consumes: the typed checkpoint from Task 3, 53,353 x 29, with `household_id`,
  `person_no`, `cluster_id`, `province_code` read back as `string` via `dtype=`.
- Produces: `angola_iea_2025q4_clean.csv`, **53,297 rows x 27 columns**, with
  `hh_size_reported` and `hh_adults_reported` dropped and sentinels recoded.
  Task 5 reads exactly this file.

- [ ] **Step 1: Write the a23 builder**

Create `$SCRATCH/build_a23.py`. Cell sources:

```python
TITLE = """
# Solution 2.3: Cleaning, Missing Values & Duplicates (Angola IEA)

This notebook reads the typed checkpoint from 2.2 and turns it into a defensible
cleaned dataset.

You will practice:
- Working on a copy, never on the loaded data
- Telling missing by design apart from missing by error
- Recoding sentinel codes that pandas cannot see are missing
- Resolving duplicates on a compound key
- Writing validation rules that actually remove something
- Catching a cross column problem that `info()` and `describe()` cannot see

> **Pipeline:** run Exercise 2.2 first. Reads and overwrites `10_cleaned/`.
"""

PATHS_CODE = """
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA_CLEAN_DIR = '../../data/10_cleaned'
typed_path = os.path.join(DATA_CLEAN_DIR, 'angola_iea_2025q4_typed.csv')

STR_COLS = {
    'household_id': 'string', 'person_no': 'string',
    'cluster_id': 'string', 'province_code': 'string',
}
df = pd.read_csv(typed_path, dtype=STR_COLS)

pd.set_option('display.float_format', lambda x: f'{x:,.2f}')
print('Loaded typed checkpoint:', df.shape)
df.head()
"""

T1_MD = """
---

## Task 1: Never destroy the input

Every change goes on a copy. The loaded frame stays untouched so you can compare
before and after at any point, and restart when an assumption turns out wrong.
"""

T1_CODE = """
df_clean = df.copy()
print('Working copy:', df_clean.shape)
"""

T2_MD = """
---

## Task 2: Detect missing values

Count them, express them as a share, and look at the shape of the problem before
deciding anything.
"""

T2_CODE = """
missing = pd.DataFrame({
    'n_missing': df_clean.isna().sum(),
    'pct_missing': (df_clean.isna().mean() * 100).round(1),
})
missing.sort_values('pct_missing', ascending=False)
"""

T2B_CODE = """
counts = df_clean.isna().sum()
counts[counts > 0].sort_values().plot(kind='barh', color='coral', figsize=(9, 7))
plt.title('Missing values by column')
plt.xlabel('Count')
plt.tight_layout()
plt.show()
"""

T2_Q = """
**Answers:**

- Two columns are 100% missing, and a large block sits between 44% and 98.5%.
- The 78% group is the labour module: only people routed into it answer. The
  98.5% column is `available_2wk`, asked only of those who said no to
  `available_now`.
- The chart makes the two groups obvious: a cluster of skip pattern columns, and
  two bars at the full height of the dataset.
"""

T3_MD = """
---

## Task 3: Drop the columns that hold nothing

`hh_size_reported` and `hh_adults_reported` should hold household size and the
number of adults. In this file they are empty in all 53,353 rows.
"""

T3_CODE = """
empty_cols = df_clean.columns[df_clean.isna().all()].tolist()
print('Entirely empty columns:', empty_cols)

print('Before:', df_clean.shape)
df_clean = df_clean.drop(columns=empty_cols)
print('After: ', df_clean.shape)
"""

T3_Q = """
**Answers:**

- Both columns go, leaving 27. Detecting them with `isna().all()` rather than
  naming them means the same code catches a different empty column next quarter.
- Household size is genuinely useful, so 2.4 rebuilds it from the roster instead.
- Worth knowing: the **Q3 2025** file has both columns fully populated. The newer
  file is not simply the better one, which is why you check every extract rather
  than trusting the most recent.
"""

T4_MD = """
---

## Task 4: Coded missing values

pandas only recognises blanks and `NaN`. Survey files also use sentinel codes
that look like ordinary numbers and silently corrupt every statistic they touch.

| Column | Sentinel | Meaning |
|---|---|---|
| `hours_usual`, `hours_actual` | 997 | NAO SABE, does not know |
| `job_start_year` | 9997 | NAO SABE, does not know |
"""

T4_CODE = """
def recode_coded_missing(series, codes):
    \"\"\"Replace coded missing values with NaN.\"\"\"
    return series.replace(codes, np.nan)


print('job_start_year mean BEFORE:', round(df_clean['job_start_year'].mean(), 1))
print('hours_usual max BEFORE:    ', df_clean['hours_usual'].max())

df_clean['hours_usual'] = recode_coded_missing(df_clean['hours_usual'], [997, 998, 999])
df_clean['hours_actual'] = recode_coded_missing(df_clean['hours_actual'], [997, 998, 999])
df_clean['job_start_year'] = recode_coded_missing(df_clean['job_start_year'], [9997, 9998, 9999])

print('job_start_year mean AFTER: ', round(df_clean['job_start_year'].mean(), 1))
print('hours_usual max AFTER:     ', df_clean['hours_usual'].max())
"""

T4_Q = """
**Answers:**

- The mean start year falls from **3164.6 to 2017.4**. The first number is not a
  year at all; it is 1,673 sentinels averaged in with real data.
- `hours_usual` drops from 997 to 120. 120 is still implausible and Task 6 deals
  with it, but it is at least a number of hours rather than a code.
- Zero is the hard case. A zero income can mean "no income" or "not collected",
  and only the questionnaire documentation tells you which, so never recode 0
  without checking.
"""

T5_MD = """
---

## Task 5: Missing by design is not missing by error

The textbook first move is `dropna()`. On a survey with skip patterns it is a
catastrophe. Measure it before you trust it.
"""

T5_CODE = """
print('Rows now:                   ', len(df_clean))
print('Rows if we called dropna(): ', len(df_clean.dropna()))
"""

T5B_CODE = """
# The right rule: only the identifiers are non negotiable
print('Before:', df_clean.shape)
df_clean = df_clean.dropna(subset=['household_id', 'person_no'])
print('After: ', df_clean.shape)
"""

T5_Q = """
**Answers:**

- `dropna()` leaves **0 rows**. Every single person is missing at least one field,
  because nobody answers every module. A whole dataset destroyed by one habit.
- Dropping on the identifiers removes nothing here, and that is still worth
  running: it states the assumption that a record without an identifier is
  unusable, and it protects you on a dirtier extract.
- Filling the labour columns would be much worse than leaving them empty. A person
  outside the labour force has no usual hours; inventing a median would fabricate
  employment.
"""

T6_MD = """
---

## Task 6: Duplicates on a compound key

No two rows here are identical, so `duplicated()` alone finds nothing. The real
key is the pair `household_id` plus `person_no`: one row per person per household.
"""

T6_CODE = """
print('Exact duplicate rows:', df_clean.duplicated().sum())

dup_mask = df_clean.duplicated(subset=['household_id', 'person_no'], keep=False)
print('Rows sharing a person key:', dup_mask.sum())
df_clean[dup_mask].sort_values(['household_id', 'person_no'])[
    ['household_id', 'person_no', 'age', 'sex', 'rel_to_head', 'hours_usual']]
"""

T6B_CODE = """
# Keep the most complete record in each group
df_clean['missing_count'] = df_clean.isna().sum(axis=1)

print('Before:', df_clean.shape)
df_clean = (
    df_clean
    .sort_values(['household_id', 'person_no', 'missing_count'])
    .drop_duplicates(subset=['household_id', 'person_no'], keep='first')
    .drop(columns='missing_count')
)
print('After: ', df_clean.shape)
"""

T6_Q = """
**Answers:**

- Zero exact duplicates, but **16 rows in 8 duplicate pairs**. Only the compound
  key finds them, which is why picking the key matters more than the method.
- 8 rows are removed, 53,353 down to 53,345.
- `keep=False` marks every member of a duplicate group, which is what you want
  when inspecting. The default `keep='first'` hides the first occurrence and makes
  the groups impossible to compare.
"""

T7_MD = """
---

## Task 7: Validation rules

Some values are not missing, they are impossible. A rule that removes nothing is
not a rule, so check the count each time.
"""

T7_CODE = """
print('age above 100:', (df_clean['age'] > 100).sum())
print('Before:', df_clean.shape)
df_clean = df_clean[df_clean['age'].between(0, 100)]
print('After: ', df_clean.shape)
"""

T7B_CODE = """
df_clean.boxplot(column='hours_usual', figsize=(6, 5))
plt.title('Usual weekly hours, after sentinel recode')
plt.tight_layout()
plt.show()
"""

T7C_CODE = """
# 98 hours is 14 hours a day, every day. Keep the missing values.
print('Before:', df_clean.shape)
hours_ok = df_clean['hours_usual'].isna() | df_clean['hours_usual'].between(0, 98)
df_clean = df_clean[hours_ok]
print('After: ', df_clean.shape)
"""

T7_Q = """
**Answers:**

- The age rule removes **3** people, aged 102, 103 and 120.
- The hours rule removes **45**. Note the `isna() |` guard: without it, every
  person outside the labour force would be dropped, because `NaN.between()` is
  `False`. That single omission would have cost about 41,000 rows.
- A rule with a bound of 120 would have removed nothing at all, because the real
  maximum after recoding is exactly 120. Always check that a rule bites.
"""

T8_MD = """
---

## Task 8: A rule that `info()` and `describe()` cannot catch

Every household should have exactly one head, `rel_to_head == 1`. No summary
statistic will tell you whether that holds, because it is a relationship between
rows.
"""

T8_CODE = """
heads = df_clean[df_clean['rel_to_head'] == 1]
heads_per_household = heads['household_id'].value_counts()

print('Households with two or more heads:', (heads_per_household > 1).sum())
print('Households with no head recorded: ',
      df_clean['household_id'].nunique() - heads_per_household.index.nunique())
"""

T8_Q = """
**Answers:**

- **1** household still has two heads, and **35** have none.
- On the raw file, before Task 6 removed the duplicate person records, **6**
  households had two heads. Five of those were caused by the duplicates
  themselves, so deduplication fixed most of the problem. That is a good argument
  for running structural checks after cleaning, not before.
- Neither number is visible in `info()` or `describe()`. Cross row and cross
  column rules need their own checks, which is why the lesson lists them as a
  known blind spot.
"""

T9_MD = """
---

## Task 9: Save the cleaned dataset

Overwrite nothing in `0_raw/`. Write the result to `10_cleaned/` and reload it to
confirm it survives the round trip.
"""

T9_CODE = """
df_clean = df_clean.reset_index(drop=True)
out_path = os.path.join(DATA_CLEAN_DIR, 'angola_iea_2025q4_clean.csv')

df_clean.to_csv(out_path, index=False)
print('Saved:', out_path, '|', df_clean.shape)
"""

T9B_CODE = """
check = pd.read_csv(out_path, dtype=STR_COLS)
print('Reloaded:', check.shape)
print()
print('Rows removed in total:', 53353 - len(check))
check.head()
"""

T9_Q = """
**Answers:**

- The cleaned file is **53,297 rows by 27 columns**. From 53,353: minus 8
  duplicates, minus 3 impossible ages, minus 45 implausible working weeks.
- Every removal is justifiable and countable, which is what makes the cleaning
  defensible to somebody who did not do it.
- 56 rows out of 53,353 is 0.1%. The sentinel recoding, which changed no row
  count at all, mattered far more to the results than any deletion did.
"""
```

Assemble as:

```python
SOLUTION = [
    md(TITLE), md("### Path Setup (run first)"), code(PATHS_CODE),
    md(T1_MD), code(T1_CODE),
    md(T2_MD), code(T2_CODE), code(T2B_CODE), md(T2_Q),
    md(T3_MD), code(T3_CODE), md(T3_Q),
    md(T4_MD), code(T4_CODE), md(T4_Q),
    md(T5_MD), code(T5_CODE), code(T5B_CODE), md(T5_Q),
    md(T6_MD), code(T6_CODE), code(T6B_CODE), md(T6_Q),
    md(T7_MD), code(T7_CODE), code(T7B_CODE), code(T7C_CODE), md(T7_Q),
    md(T8_MD), code(T8_CODE), md(T8_Q),
    md(T9_MD), code(T9_CODE), code(T9B_CODE), md(T9_Q),
]
```

Gaps for `GAPS`:

| Cell | Exercise line |
|---|---|
| `T1_CODE` | `df_clean = df.  # your code here` |
| `T3_CODE` | `empty_cols =   # your code here: columns where isna().all()` |
| `T4_CODE` | body of `recode_coded_missing` becomes `# your code here: return series.replace(codes, np.nan)` plus `return` |
| `T5B_CODE` | `df_clean = df_clean.dropna(  # your code here: subset=['household_id', 'person_no'] )` |
| `T6_CODE` | `dup_mask = df_clean.duplicated(  # your code here: subset and keep=False )` |
| `T6B_CODE` | the `.drop_duplicates(...)` line becomes `.drop_duplicates(  # your code here: subset and keep='first' )` |
| `T7_CODE` | `df_clean = df_clean[df_clean['age'].  # your code here: between(0, 100) ]` |
| `T7C_CODE` | `hours_ok = df_clean['hours_usual'].isna() \|   # your code here: between(0, 98)` (the `\|` is an escaped pipe; write a single `\|` character in the notebook) |
| `T8_CODE` | `heads_per_household = heads['household_id'].  # your code here` |
| `T9_CODE` | `df_clean.  # your code here: to_csv with index=False` |

- [ ] **Step 2: Build both notebooks**

```bash
python3 $SCRATCH/build_a23.py
```

- [ ] **Step 3: Execute the solution**

```bash
cd notebooks/solutions && python3 -m jupyter nbconvert --to notebook --execute \
  --inplace --ExecutePreprocessor.timeout=600 solution_a23_cleaning_missing_duplicates.ipynb
```

Expected: exit code 0.

- [ ] **Step 4: Assert the cleaned output**

```bash
python3 -c "
import pandas as pd
df = pd.read_csv('data/10_cleaned/angola_iea_2025q4_clean.csv',
                 dtype={'household_id':'string','person_no':'string'})
assert df.shape == (53297, 27), df.shape
assert df.duplicated(subset=['household_id','person_no']).sum() == 0
assert df['age'].max() <= 100, df['age'].max()
assert df['hours_usual'].max() <= 98, df['hours_usual'].max()
assert round(df['job_start_year'].mean(), 1) == 2017.4
print('OK', df.shape)
"
```

Expected: `OK (53297, 27)`.

- [ ] **Step 5: Run the checker for a23**

```bash
python3 $SCRATCH/check_series.py a23_cleaning_missing_duplicates
```

Expected: `PASS`.

- [ ] **Step 6: Commit**

```bash
git add notebooks/exercises/exercise_a23_cleaning_missing_duplicates.ipynb \
        notebooks/solutions/solution_a23_cleaning_missing_duplicates.ipynb
git commit -m "feat(notebooks): add Angola a23 cleaning and duplicates exercise"
```

---

## Task 5: a24, Transforming Data and Creating New Features

**Files:**
- Create: `notebooks/solutions/solution_a24_transforming_features.ipynb`
- Create: `notebooks/exercises/exercise_a24_transforming_features.ipynb`
- Create: `$SCRATCH/build_a24.py`
- Reads data: `data/10_cleaned/angola_iea_2025q4_clean.csv`
- Produces data: `data/20_processed/angola_iea_2025q4_features.csv`

**Interfaces:**
- Consumes: the cleaned file from Task 4, 53,297 x 27.
- Produces: `angola_iea_2025q4_features.csv`, **53,297 rows x 39 columns**. Task 6
  Part A reads this file and relies on these added column names:
  `age_group`, `province_name`, `sex_label`, `area_label`, `education_label`,
  `lf_status_strict`,
  `lf_status_relaxed`, `full_time`, `job_tenure_years`, `tenure_band`, `hh_size`,
  `hours_per_day`. The function `unemployment_rate(status, weights) -> float`
  defined here returns a percentage.

- [ ] **Step 1: Write the a24 builder**

Create `$SCRATCH/build_a24.py`. Cell sources:

```python
TITLE = """
# Solution 2.4: Transforming Data & Creating New Features (Angola IEA)

This notebook turns the cleaned file into an analysis ready dataset, and ends by
producing Angola's headline labour market statistic two different ways.

You will practice:
- Banding a continuous variable with `pd.cut()`
- Decoding numeric codes with `.map()` and a dictionary
- Building a three way category with `np.select()`
- Binary flags with `np.where()` and updates with `.loc[]`
- Chained, dependent columns with `assign()` and lambdas
- Custom row logic with `apply()`
- Weighting a statistic, and seeing why the definition matters more than the code

> **Pipeline:** run Exercise 2.3 first. Writes to `20_processed/`.
"""

PATHS_CODE = """
import os

import numpy as np
import pandas as pd

DATA_CLEAN_DIR = '../../data/10_cleaned'
DATA_PROC_DIR = '../../data/20_processed'
clean_path = os.path.join(DATA_CLEAN_DIR, 'angola_iea_2025q4_clean.csv')

STR_COLS = {
    'household_id': 'string', 'person_no': 'string',
    'cluster_id': 'string', 'province_code': 'string',
}
df = pd.read_csv(clean_path, dtype=STR_COLS)

pd.set_option('display.float_format', lambda x: f'{x:,.2f}')
print('Loaded:', df.shape)
df.head()
"""

T1_MD = """
---

## Task 1: Age bands with `pd.cut()`

The labour statistics that follow all rest on the working age population, which
Angola defines as 15 and over. Band the ages accordingly.

Note `right=False`, which makes each interval closed on the left: a 15 year old
belongs to Youth, not Child.
"""

T1_CODE = """
df['age_group'] = pd.cut(
    df['age'],
    bins=[0, 15, 25, 65, 120],
    labels=['Child', 'Youth', 'Adult', 'Elderly'],
    right=False,
)
df['age_group'].value_counts(dropna=False)
"""

T1_Q = """
**Answers:**

- Child 23,526, Youth 10,890, Adult 17,199, Elderly 1,682. They sum to 53,297,
  so nothing fell outside the bins.
- With the default `right=True` the intervals would close on the right, putting
  15 year olds in Child and quietly shrinking the working age population by
  everyone aged exactly 15.
- Children are 44% of this sample. That is the single most important fact about
  Angola's labour market and it is visible before any modelling.
"""

T2_MD = """
---

## Task 2: Decode the numeric codes with `.map()`

The codebook read in 2.1 gives the code to label mapping. `.map()` applies a
dictionary element by element and returns `NaN` for anything not in it, which
doubles as a check.
"""

T2_CODE = """
PROVINCE_MAP = {
    '10': 'Cabinda', '11': 'Zaire', '12': 'Uíge', '13': 'Bengo', '14': 'Luanda',
    '15': 'Cuanza-Norte', '16': 'Cuanza-Sul', '17': 'Malanje', '18': 'Lunda-Norte',
    '19': 'Lunda-Sul', '20': 'Moxico', '21': 'Bié', '22': 'Huambo', '23': 'Benguela',
    '24': 'Namibe', '25': 'Huila', '26': 'Cunene', '27': 'Cubango',
    '28': 'Icolo e Bengo', '29': 'Moxico Leste', '30': 'Cuando',
}
SEX_MAP = {1: 'Masculino', 2: 'Feminino'}
AREA_MAP = {1: 'Urbana', 2: 'Rural'}
EDUCATION_MAP = {
    1: 'Primário', 2: 'I Ciclo Secundário', 3: 'II Ciclo Secundário',
    4: 'Bacharelato', 5: 'Licenciatura', 6: 'Mestrado', 7: 'Doutoramento',
    9: 'Nenhum nível',
}

df['province_name'] = df['province_code'].map(PROVINCE_MAP)
df['sex_label'] = df['sex'].map(SEX_MAP)
df['area_label'] = df['area_type'].map(AREA_MAP)
df['education_label'] = df['education_level'].map(EDUCATION_MAP)

print('Unmapped provinces:', df['province_name'].isna().sum())
print(df['area_label'].value_counts(dropna=False))
print()
print(df['education_label'].value_counts(dropna=False))
"""

T2_Q = """
**Answers:**

- Zero unmapped provinces, because the dictionary was built from the file's own
  codebook rather than from memory.
- 34,129 urban and 19,168 rural.
- `education_label` is `NaN` for the majority of rows, because `education_level`
  is 56.6% missing: the question is only asked of people the questionnaire routes
  to it. `.map()` returns `NaN` both for a genuinely missing input and for a code
  absent from the dictionary, so the two causes look identical in the output. That
  is why the unmapped count above is worth printing separately.
- Note that the education codes run 1 to 7 and then jump to 9, with no 8. Code 9
  means "Nenhum nível", no level at all, so it is not a rank above 7. Sorting or
  averaging this column as if it were ordinal would put the least educated group
  at the top.
- The three most recent provinces, Icolo e Bengo, Moxico Leste and Cuando, were
  created in 2024. A mapping copied from an older publication would leave 6,499
  people, 12.2% of the sample, with a missing province name. 2.5 shows exactly
  that failure as a merge.
"""

T3_MD = """
---

## Task 3: Labour force status with `np.select()`

`np.select()` takes conditions in order and applies the first match. This is the
heart of the notebook, and the definitions matter more than the syntax.

**Employed:** worked for pay, or worked on own account, or has a job they were
absent from. **Unemployed (strict ILO):** not employed, actively looked for work,
and available to start. Everyone else of working age is outside the labour force.
"""

T3_CODE = """
working_age = df['age'] >= 15
employed = (
    (df['worked_for_pay'] == 1)
    | (df['worked_own_account'] == 1)
    | (df['absent_from_job'] == 1)
)
seeking = (df['sought_work'] == 1) | (df['sought_business'] == 1)
available = (df['available_now'] == 1) | (df['available_2wk'] == 1)

strict_conditions = [working_age & employed, working_age & seeking & available]
df['lf_status_strict'] = np.select(
    strict_conditions, ['Employed', 'Unemployed'], default='Outside labour force')

df['lf_status_strict'].value_counts()
"""

T3B_CODE = """
# The relaxed definition also counts people who want work but have stopped
# looking: the discouraged, who a strict measure treats as economically inactive.
relaxed_conditions = [
    working_age & employed,
    working_age & ((seeking & available) | (df['wants_work'] == 1)),
]
df['lf_status_relaxed'] = np.select(
    relaxed_conditions, ['Employed', 'Unemployed'], default='Outside labour force')

df['lf_status_relaxed'].value_counts()
"""

T3_Q = """
**Answers:**

- Strict: 15,697 employed, 2,632 unemployed, 34,968 outside the labour force.
- Relaxed: the same 15,697 employed, but 7,858 unemployed. Around 5,200 people
  move from "outside the labour force" to "unemployed" purely because the
  definition changed.
- `available_now` and `available_2wk` are combined with `|` because they are two
  stages of one question: `available_2wk` is only asked of people who answered no
  to `available_now`, which is why it is 98.5% missing. Using it alone would
  discard almost every unemployed person.
- Order matters. Employment is tested first, so somebody who is both working and
  looking for a better job counts as employed, which is the standard convention.
"""

T4_MD = """
---

## Task 4: Weight the result

Each person in the sample stands for many people in Angola, and `weight_ind`
records how many. An unweighted rate describes the sample; a weighted rate
describes the country. Published statistics are always weighted.
"""

T4_CODE = """
def unemployment_rate(status, weights):
    \"\"\"Unemployment as a percentage of the labour force.\"\"\"
    unemployed = status == 'Unemployed'
    labour_force = status.isin(['Employed', 'Unemployed'])
    return weights[unemployed].sum() / weights[labour_force].sum() * 100


weight = df['weight_ind']
ones = pd.Series(1, index=df.index)

for name in ['lf_status_strict', 'lf_status_relaxed']:
    print(f'{name:20s} weighted: {unemployment_rate(df[name], weight):5.1f}%'
          f'   unweighted: {unemployment_rate(df[name], ones):5.1f}%')
"""

T4B_CODE = """
in_labour_force = df['lf_status_strict'].isin(['Employed', 'Unemployed'])
participation = weight[in_labour_force].sum() / weight[working_age].sum() * 100
print(f'Labour force participation rate: {participation:.1f}%')
print(f'Weighted working age population: {weight[working_age].sum():,.0f}')
"""

T4_Q = """
**Answers:**

- Strict unemployment is **14.5%** weighted. Relaxed unemployment is **31.4%**.
  Same data, same day, same people: a 17 point spread produced entirely by a
  definition.
- INE Angola publishes a figure around 29 to 30%, so the relaxed measure is the
  national headline. The strict measure is the internationally comparable one.
  Neither is wrong, and a table that does not say which it used is useless.
- The weights barely move this particular estimate (14.5% against 14.4%), because
  unemployment happens to be spread evenly across the weighting strata. That is
  luck, not a reason to skip them: the participation rate and every population
  total depend on them entirely.
- Which number goes in a press release? Whichever one the publication has always
  used, stated explicitly, with the other in a footnote. Switching silently
  between them is how a statistical office loses trust.
"""

T5_MD = """
---

## Task 5: Binary flags with `np.where()` and `.loc[]`

`np.where()` is a vectorised if/else. `.loc[]` updates values that match a
condition, which is how you add a third state afterwards.
"""

T5_CODE = """
df['full_time'] = np.where(df['hours_usual'] >= 35, 'Full time', 'Part time')

# np.where has no idea what a missing value means: it lands in the else branch.
# Make the unknown explicit instead of letting it masquerade as part time.
df.loc[df['hours_usual'].isna(), 'full_time'] = 'Unknown'

df['full_time'].value_counts()
"""

T5_Q = """
**Answers:**

- 9,054 full time, 2,534 part time, 41,709 unknown.
- Without the `.loc[]` line, all 41,709 people with no recorded hours would be
  labelled "Part time", and a headline about part time work would be off by a
  factor of sixteen. `np.where()` treats `NaN >= 35` as `False` and says nothing.
- The 41,709 are overwhelmingly people outside the labour force, who have no
  usual hours to report. Unknown is the honest label.
"""

T6_MD = """
---

## Task 6: Dependent columns with `assign()`

`assign()` returns a new DataFrame, so it chains. A lambda inside it sees the
frame **as it is being built**, which is how the second column below can use the
first one created in the same call.
"""

T6_CODE = """
df = df.assign(
    job_tenure_years=lambda x: 2025 - x['job_start_year'],
    tenure_band=lambda x: np.select(
        [x['job_tenure_years'] < 1,
         x['job_tenure_years'] < 5,
         x['job_tenure_years'] >= 5],
        ['Under 1 year', '1 to 4 years', '5 years or more'],
        default='Unknown',
    ),
)
df['tenure_band'].value_counts()
"""

T6_Q = """
**Answers:**

- 5,331 people have been in their job five years or more, 3,324 one to four
  years, 1,269 under a year, and 43,373 are Unknown.
- `tenure_band` must reference `lambda x: x['job_tenure_years']` rather than
  `df['job_tenure_years']`, because at that moment `df` is still the old frame and
  the column does not exist on it yet. `x` is the frame under construction.
- Unknown dominates because tenure only exists for people with a main job, and
  because `job_start_year` lost 1,673 sentinel values in 2.3. `np.select` routes
  every `NaN` to `default`, which is exactly what you want here.
"""

T7_MD = """
---

## Task 7: Household size, without `groupby`

`hh_size_reported` was dropped in 2.3 because it was empty. Rebuild it from the
roster: count how many rows share each `household_id`, then map that count back
onto every person.

`value_counts()` comes from 2.1 and `.map()` from 2.4, so no new tool is needed.
"""

T7_CODE = """
df['hh_size'] = df['household_id'].map(df['household_id'].value_counts())

print('Mean household size per person:   ', round(df['hh_size'].mean(), 2))
print('Mean household size per household:',
      round(df.drop_duplicates('household_id')['hh_size'].mean(), 2))
df['hh_size'].describe()
"""

T7_Q = """
**Answers:**

- Per person the mean is **5.58**; per household it is **4.09**. Both are correct
  and they answer different questions.
- The gap exists because a household of 10 contributes 10 rows and a household of
  1 contributes one, so averaging over rows over-weights large households. "The
  average person lives in a household of 5.58" and "the average household has 4.09
  people" are both true statements.
- Publishing the per person figure as "average household size" is a classic error.
  Deduplicate to the household before averaging a household level attribute.
"""

T8_MD = """
---

## Task 8: Custom logic with `apply()`

When built in operations cannot express the rule, `apply()` runs your own
function. It processes rows one at a time and is much slower than a vectorised
operation, so reach for it last, not first.
"""

T8_CODE = """
def hours_per_day(row):
    \"\"\"Usual weekly hours spread over 7 days, or NaN when the input is unusable.\"\"\"
    hours = row['hours_usual']
    if pd.isna(hours) or hours <= 0:
        return np.nan
    return round(hours / 7, 2)


df['hours_per_day'] = df.apply(hours_per_day, axis=1)
print('Mean hours per day:', round(df['hours_per_day'].mean(), 2))
df[['household_id', 'hours_usual', 'hours_per_day']].dropna().head()
"""

T8_Q = """
**Answers:**

- The mean is 6.52 hours a day across those who report any hours.
- `axis=1` passes a whole row, so the function can read several columns. Without
  it, `apply` would pass one column at a time.
- This particular calculation is a single division and would be far faster as
  `df['hours_usual'] / 7`. The guards are the only reason to use a function, and
  even they could be written as a vectorised `.where()`. On 53,000 rows the
  difference is invisible; on 5 million it is not.
"""

T9_MD = """
---

## Task 9: Save the feature table

Cleaned data lives in `10_cleaned/`. Derived, analysis ready tables go in
`20_processed/`.
"""

T9_CODE = """
os.makedirs(DATA_PROC_DIR, exist_ok=True)
out_path = os.path.join(DATA_PROC_DIR, 'angola_iea_2025q4_features.csv')

df.to_csv(out_path, index=False)
print('Saved:', out_path, '|', df.shape)
"""

T9B_CODE = """
check = pd.read_csv(out_path, dtype=STR_COLS)
print('Reloaded:', check.shape)
print('Columns added since the cleaned file:', check.shape[1] - 27)
check[['household_id', 'age_group', 'province_name',
       'lf_status_strict', 'lf_status_relaxed', 'hh_size']].head()
"""

T9_Q = """
**Answers:**

- 53,297 rows by 39 columns: 12 new columns on top of the 27 that came in.
- The vectorised ones (`pd.cut`, `.map`, `np.select`, `np.where`, the `assign`
  arithmetic) all operate on whole columns. Only `hours_per_day` uses `apply`
  with `axis=1`, so it is the first thing to rewrite if this ever runs on a
  census sized file.
- Row count is unchanged, which is the point: 2.3 decides what to remove, 2.4 only
  adds.
"""
```

Assemble as:

```python
SOLUTION = [
    md(TITLE), md("### Path Setup (run first)"), code(PATHS_CODE),
    md(T1_MD), code(T1_CODE), md(T1_Q),
    md(T2_MD), code(T2_CODE), md(T2_Q),
    md(T3_MD), code(T3_CODE), code(T3B_CODE), md(T3_Q),
    md(T4_MD), code(T4_CODE), code(T4B_CODE), md(T4_Q),
    md(T5_MD), code(T5_CODE), md(T5_Q),
    md(T6_MD), code(T6_CODE), md(T6_Q),
    md(T7_MD), code(T7_CODE), md(T7_Q),
    md(T8_MD), code(T8_CODE), md(T8_Q),
    md(T9_MD), code(T9_CODE), code(T9B_CODE), md(T9_Q),
]
```

Gaps for `GAPS`:

| Cell | Exercise line |
|---|---|
| `T1_CODE` | `labels=  # your code here: Child, Youth, Adult, Elderly` and `right=  # your code here` |
| `T2_CODE` | `df['province_name'] = df['province_code'].  # your code here: map(PROVINCE_MAP)` |
| `T3_CODE` | `available = (df['available_now'] == 1)   # your code here: also allow available_2wk` |
| `T3_CODE` | `df['lf_status_strict'] = np.select(  # your code here: conditions, choices, default )` |
| `T3B_CODE` | the second condition becomes `working_age & (  # your code here: seeking & available, or wants_work )` |
| `T4_CODE` | body of `unemployment_rate` becomes `# your code here: weighted unemployed over weighted labour force` plus `return` |
| `T5_CODE` | `df.loc[  # your code here: rows where hours_usual is missing , 'full_time'] = 'Unknown'` |
| `T6_CODE` | `job_tenure_years=lambda x:   # your code here` |
| `T7_CODE` | `df['hh_size'] = df['household_id'].  # your code here: map with value_counts()` |
| `T8_CODE` | function body becomes `# your code here: guard NaN and non positive, then round(hours / 7, 2)` |
| `T9_CODE` | `df.  # your code here: to_csv with index=False` |

- [ ] **Step 2: Build both notebooks**

```bash
python3 $SCRATCH/build_a24.py
```

- [ ] **Step 3: Execute the solution**

```bash
cd notebooks/solutions && python3 -m jupyter nbconvert --to notebook --execute \
  --inplace --ExecutePreprocessor.timeout=600 solution_a24_transforming_features.ipynb
```

Expected: exit code 0.

- [ ] **Step 4: Assert the headline statistics**

```bash
python3 -c "
import pandas as pd
df = pd.read_csv('data/20_processed/angola_iea_2025q4_features.csv',
                 dtype={'household_id':'string','province_code':'string'})
assert df.shape == (53297, 39), df.shape
w = df['weight_ind']
def rate(col):
    u = df[col] == 'Unemployed'
    lf = df[col].isin(['Employed','Unemployed'])
    return w[u].sum()/w[lf].sum()*100
strict, relaxed = rate('lf_status_strict'), rate('lf_status_relaxed')
print(f'strict {strict:.1f}%  relaxed {relaxed:.1f}%')
assert abs(strict - 14.5) < 0.15, strict
assert abs(relaxed - 31.4) < 0.15, relaxed
assert df['province_name'].isna().sum() == 0
assert round(df['hh_size'].mean(), 2) == 5.58
print('OK')
"
```

Expected:

```
strict 14.5%  relaxed 31.4%
OK
```

- [ ] **Step 5: Run the checker for a24**

```bash
python3 $SCRATCH/check_series.py a24_transforming_features
```

Expected: `PASS`.

- [ ] **Step 6: Commit**

```bash
git add notebooks/exercises/exercise_a24_transforming_features.ipynb \
        notebooks/solutions/solution_a24_transforming_features.ipynb
git commit -m "feat(notebooks): add Angola a24 feature engineering exercise"
```

---

## Task 6: a25, Merging and Combining Datasets

**Files:**
- Create: `notebooks/solutions/solution_a25_merging_combining.ipynb`
- Create: `notebooks/exercises/exercise_a25_merging_combining.ipynb`
- Create: `$SCRATCH/build_a25.py`
- Reads data: `data/20_processed/angola_iea_2025q4_features.csv`,
  `data/0_raw/angola/employment_survey/IEA_III_TRIMESTRE_2025.sav`,
  `data/0_raw/angola/international_trade/Comercio Externo de Bens por Países Parceiros.xlsx`
- Produces data: `angola_iea_2025q4_analysis.csv`, `angola_iea_waves_q3_q4.csv`,
  `angola_trade_partners.csv`, all in `data/20_processed/`

**Interfaces:**
- Consumes: the feature table from Task 5, 53,297 x 39.
- Produces: three CSVs. Nothing downstream consumes them; this is the last
  notebook in the series. The helper `load_trade_sheet(path, sheet) -> DataFrame`
  is defined and used only here.

This notebook has three parts. Part A and Part C are merges on different data,
Part B is an append. The notebook says so explicitly, because there is no
meaningful join between a person level labour survey and country level trade
totals and learners should not be left guessing.

- [ ] **Step 1: Write the a25 builder, Part A**

Create `$SCRATCH/build_a25.py`. Part A cell sources:

```python
TITLE = """
# Solution 2.5: Merging & Combining Datasets (Angola IEA and INE trade)

Three separate join problems, on purpose:

- **Part A** attaches province names to the survey with a lookup table, using a
  deliberately outdated lookup so the audit tools have something to find.
- **Part B** appends the Q3 2025 wave of the same survey to the Q4 wave, where
  the two files share only 20 of their 260 and 206 columns.
- **Part C** merges Angola's export and import tables to compute a trade balance.

Part C uses a different dataset. There is no sensible join between an individual
level labour survey and country level trade totals, and pretending otherwise
would teach a bad habit.

> **Pipeline:** run Exercise 2.4 first. Writes three files to `20_processed/`.
"""

PATHS_CODE = """
import os

import numpy as np
import pandas as pd

DATA_PROC_DIR = '../../data/20_processed'
DATA_SURVEY_DIR = '../../data/0_raw/angola/employment_survey'
DATA_TRADE_DIR = '../../data/0_raw/angola/international_trade'

features_path = os.path.join(DATA_PROC_DIR, 'angola_iea_2025q4_features.csv')

STR_COLS = {
    'household_id': 'string', 'person_no': 'string',
    'cluster_id': 'string', 'province_code': 'string',
}
df = pd.read_csv(features_path, dtype=STR_COLS)

pd.set_option('display.float_format', lambda x: f'{x:,.2f}')
print('Survey:', df.shape)
df[['household_id', 'province_code', 'age', 'lf_status_strict']].head()
"""

A1_MD = """
---

# Part A: attaching province names with a lookup

## Task 1: A lookup table, as published before 2024

Angola reorganised its provinces in 2024, going from 18 to 21. Icolo e Bengo,
Moxico Leste and Cuando are new. The lookup below is the **old** 18 province
list, which is exactly what you get if you copy a reference table from an older
publication.
"""

A1_CODE = """
province_lookup_old = pd.DataFrame({
    'province_code': ['10', '11', '12', '13', '14', '15', '16', '17', '18',
                      '19', '20', '21', '22', '23', '24', '25', '26', '27'],
    'province_name_ref': ['Cabinda', 'Zaire', 'Uíge', 'Bengo', 'Luanda',
                          'Cuanza-Norte', 'Cuanza-Sul', 'Malanje', 'Lunda-Norte',
                          'Lunda-Sul', 'Moxico', 'Bié', 'Huambo', 'Benguela',
                          'Namibe', 'Huila', 'Cunene', 'Cubango'],
})
print('Lookup rows:', len(province_lookup_old))
province_lookup_old.head()
"""

A2_MD = """
## Task 2: Join key hygiene, before you merge

Most failed merges are a key that is text on one side and a number on the other,
or a stray space. Check dtypes, whitespace and missing keys on both sides first.
"""

A2_CODE = """
print('Survey key dtype:', df['province_code'].dtype)
print('Lookup key dtype:', province_lookup_old['province_code'].dtype)
print()
print('Missing keys, survey:', df['province_code'].isna().sum())
print('Missing keys, lookup:', province_lookup_old['province_code'].isna().sum())
print('Duplicate keys, lookup:', province_lookup_old['province_code'].duplicated().sum())
"""

A2_Q = """
**Answers:**

- Both keys are `string` because 2.2 converted the survey key deliberately. Had it
  stayed `float64`, every single row would fail to match a text lookup and the
  merge would return all `NaN` without any error at all.
- No missing keys on either side, and no duplicate keys in the lookup, so a left
  join should not change the row count.
"""

A3_MD = """
## Task 3: Merge, then audit with `indicator`

A left join keeps every survey row. `indicator=True` adds a `_merge` column
labelling each row `both`, `left_only` or `right_only`, which is how you find out
what silently failed to match.
"""

A3_CODE = """
merged = pd.merge(df, province_lookup_old, on='province_code',
                  how='left', indicator=True)

print('Rows:', len(df), '->', len(merged))
print(merged['_merge'].value_counts())
"""

A3B_CODE = """
unmatched = merged[merged['_merge'] == 'left_only']
print('Unmatched rows:', len(unmatched),
      f'({len(unmatched) / len(merged) * 100:.1f}%)')
print()
print(unmatched['province_code'].value_counts().sort_index())
"""

A3C_CODE = """
inner = pd.merge(df, province_lookup_old, on='province_code', how='inner')
outer = pd.merge(df, province_lookup_old, on='province_code', how='outer')
print('inner:', len(inner), '| left:', len(merged), '| outer:', len(outer))
"""

A3_Q = """
**Answers:**

- The row count is unchanged at 53,297, which is what a left join on a unique
  right key must do.
- **6,499 rows, 12.2%, are `left_only`**: province codes 28, 29 and 30. Those are
  the provinces created in 2024 and missing from the old lookup. Nothing raised an
  error; without `indicator=True` you would have shipped a table with 12% of the
  country silently unlabelled.
- The inner join drops those 6,499 rows entirely, which is worse: the data
  disappears rather than being visibly blank.
- The right response is to fix the lookup at source, not to drop the rows or
  invent names. In 2.4 the full 21 province map was already used successfully, so
  `province_name` is correct in this file and `province_name_ref` is the broken
  one. Comparing the two is the fastest way to prove a lookup is stale.
"""

A4_MD = """
## Task 4: Cardinality, and making the assumption explicit

If the right hand key is not unique, every duplicate match multiplies rows.
`validate=` states your assumption and raises instead of silently inflating.
"""

A4_CODE = """
# A lookup that accidentally lists Cabinda twice
bad_lookup = pd.concat([province_lookup_old, province_lookup_old.head(1)],
                       ignore_index=True)

exploded = pd.merge(df, bad_lookup, on='province_code', how='left')
print('Rows before:', len(df), '-> after the bad merge:', len(exploded))
print('Extra rows:', len(exploded) - len(df))
"""

A4B_CODE = """
try:
    pd.merge(df, bad_lookup, on='province_code', how='left', validate='many_to_one')
except Exception as error:
    print(type(error).__name__, '->', error)
"""

A4_Q = """
**Answers:**

- The row count grows from 53,297 to 55,602. Every person in Cabinda is duplicated
  because Cabinda appears twice on the right.
- `validate='many_to_one'` raises `MergeError`. Many survey rows to one lookup row
  is the correct description of a person to province join.
- `one_to_one` promises both sides are unique, `one_to_many` that the left is
  unique, `many_to_one` that the right is. Stating it converts a silent data
  corruption into an immediate, loud failure.
"""

A5_MD = """
## Task 5: Post merge validation, then save

A merge is finished when you have confirmed the result, not when the code ran.
"""

A5_CODE = """
final = pd.merge(df, province_lookup_old, on='province_code', how='left')

print('Row count:', len(df), '->', len(final))
print('Duplicate person keys:',
      final.duplicated(subset=['household_id', 'person_no']).sum())
print('Unmatched province rate:', round(final['province_name_ref'].isna().mean(), 4))
"""

A5B_CODE = """
final = final.reset_index(drop=True)
out_path = os.path.join(DATA_PROC_DIR, 'angola_iea_2025q4_analysis.csv')
final.to_csv(out_path, index=False)
print('Saved:', out_path, '|', final.shape)
"""

A5_Q = """
**Answers:**

- 53,297 rows in and out, no duplicate person keys, and a 0.122 unmatched rate
  that we can explain exactly.
- An unmatched rate you can explain is fine to ship with a documented caveat. An
  unmatched rate you cannot explain is a stop sign.
"""
```

- [ ] **Step 2: Write Part B, appending the two waves**

```python
B1_MD = """
---

# Part B: appending the Q3 and Q4 waves

## Task 6: Load the previous quarter

`IEA_III_TRIMESTRE_2025.sav` is the same survey, one quarter earlier. It uses the
questionnaire's own variable names rather than the ILO mnemonics of the Q4 file,
so almost nothing lines up.
"""

B1_CODE = """
q3_path = os.path.join(DATA_SURVEY_DIR, 'IEA_III_TRIMESTRE_2025.sav')
q3_full = pd.read_spss(q3_path, convert_categoricals=False)

print('Q3:', q3_full.shape)
print('Q4 features:', df.shape)
print('Column names in common:', len(set(q3_full.columns) & set(df.columns)))
"""

B2_MD = """
## Task 7: What a naive `concat` does

`pd.concat` aligns on column names and fills every gap with `NaN`, without a
single warning. Try it and measure the damage.
"""

B2_CODE = """
naive = pd.concat([q3_full, df], ignore_index=True)

print('Naive concat:', naive.shape)
mostly_empty = (naive.isna().mean() > 0.99).sum()
print(f'Columns more than 99% empty: {mostly_empty} of {naive.shape[1]}')
naive.iloc[:3, :6]
"""

B2_Q = """
**Answers:**

- The result is 108,260 rows by **298 columns**, of which 115 are more than 99%
  empty. Each wave contributed its own vocabulary and neither filled the other's.
- Nothing warned. `concat` does exactly what it was asked; the mistake was in the
  asking.
- The row count is right and everything else is wrong, which is the dangerous
  kind of failure: it looks like it worked.
"""

B3_MD = """
## Task 8: Do it properly, by harmonising first

Pick the variables that exist in both waves, rename the Q3 ones to the Q4 names,
confirm the two frames have identical columns, then stack them with a `wave`
column so no row loses its origin.
"""

B3_CODE = """
Q3_RENAME = {
    'NIDF': 'household_id', 'PROV': 'province_code', 'AREA_RESID': 'area_type',
    'S02_01': 'sex', 'S02_02': 'age', 'S4_01': 'worked_for_pay',
    'S4_02': 'worked_own_account', 'S4_03': 'worked_family_business',
    'S4_09': 'absent_from_job', 'S8_01': 'sought_work', 'S8_12': 'available_now',
    'POND_IEA_III_TRIM_2025_IND': 'weight_ind',
}

q3 = q3_full[list(Q3_RENAME)].rename(columns=Q3_RENAME)
q3['household_id'] = q3['household_id'].astype('int64').astype('string')
q3['province_code'] = q3['province_code'].astype('int64').astype('string').str.zfill(2)

print('Q3 harmonised:', q3.shape)
q3.head()
"""

B3B_CODE = """
SHARED = [
    'household_id', 'province_code', 'area_type', 'sex', 'age',
    'worked_for_pay', 'worked_own_account', 'worked_family_business',
    'absent_from_job', 'sought_work', 'available_now', 'weight_ind',
]

q3_slim = q3[SHARED].assign(wave='2025Q3')
q4_slim = df[SHARED].assign(wave='2025Q4')

print('Columns identical:', list(q3_slim.columns) == list(q4_slim.columns))

waves = pd.concat([q3_slim, q4_slim], ignore_index=True)
print('Stacked:', waves.shape)
print('Any column entirely empty:', waves.isna().all().any())
print(waves['wave'].value_counts())
"""

B3_Q = """
**Answers:**

- 108,260 rows by 13 columns instead of 298, and no column is empty.
- The `wave` column is added **before** stacking, so every row carries its origin.
  Without it the two quarters are indistinguishable and the append is
  irreversible.
- The cost is real: 12 shared variables out of 206 and 260. Harmonising across
  waves means analysing the intersection, and the intersection is small.
"""

B4_MD = """
## Task 9: Cross wave sanity checks

Two independent samples of the same population should agree on the things that do
not change quickly. If they do not, the append is wrong.
"""

B4_CODE = """
population = waves.groupby('wave')['weight_ind'].sum()
print('Weighted population by wave:')
print(population.round(0))
difference = abs(population.iloc[0] - population.iloc[1]) / population.iloc[1] * 100
print(f'Relative difference: {difference:.2f}%')
"""

B4B_CODE = """
# The harmonised definition can only use the variables both waves carry
for wave in ['2025Q3', '2025Q4']:
    sample = waves[waves['wave'] == wave]
    working_age = sample['age'] >= 15
    employed = working_age & (
        (sample['worked_for_pay'] == 1)
        | (sample['worked_own_account'] == 1)
        | (sample['absent_from_job'] == 1)
    )
    unemployed = (working_age & ~employed
                  & (sample['sought_work'] == 1)
                  & (sample['available_now'] == 1))
    weights = sample['weight_ind']
    rate = weights[unemployed].sum() / weights[employed | unemployed].sum() * 100
    print(f'{wave} harmonised strict unemployment: {rate:.1f}%')
"""

B4C_CODE = """
out_path = os.path.join(DATA_PROC_DIR, 'angola_iea_waves_q3_q4.csv')
waves.to_csv(out_path, index=False)
print('Saved:', out_path, '|', waves.shape)
"""

B4_Q = """
**Answers:**

- The weighted populations are 37,337,629 and 37,604,687, **0.71% apart**. Two
  independent samples agreeing that closely on the size of Angola is strong
  evidence that both the weights and the append are sound.
- Harmonised strict unemployment is 11.5% in Q3 and 11.9% in Q4: a small, credible
  quarter on quarter move.
- Note that Q4's harmonised 11.9% differs from the 14.5% computed in 2.4. Nothing
  is broken. The harmonised version can only use `sought_work` and
  `available_now`, because Q3 has no equivalent of `sought_business` or
  `available_2wk`. Comparability across waves costs precision within a wave, and
  that trade is the whole difficulty of producing a time series.
- Had the populations differed by 30%, the likely cause would be a weight column
  from the wrong wave, or a wave stacked twice.
"""
```

- [ ] **Step 3: Write Part C, the trade merge**

```python
C1_MD = """
---

# Part C: Angola's trade balance

Different dataset, different join. `Comercio Externo de Bens por Países
Parceiros.xlsx` is published by INE with four sheets: exports and imports, each
in kwanzas and in US dollars.

The sheets are formatted for human readers, so loading them takes work: two title
rows above the header, a blank row, a `Total Geral` row, and a source footer at
the bottom.
"""

C1_CODE = """
trade_path = os.path.join(DATA_TRADE_DIR,
                          'Comercio Externo de Bens por Países Parceiros.xlsx')

print(pd.ExcelFile(trade_path).sheet_names)
"""

C1B_CODE = """
# What the raw sheet looks like before any cleaning
pd.read_excel(trade_path, sheet_name='Exportação por Países (USD)',
              header=None, nrows=6).iloc[:, :5]
"""

C2_MD = """
## Task 10: Load a sheet properly

`skiprows=2` puts the real header row in place. The country code must be read as
text, the header names carry an embedded newline, and the total and footer rows
both lack a country name, which makes them easy to remove together.
"""

C2_CODE = """
def load_trade_sheet(path, sheet):
    \"\"\"Load one INE trade sheet and strip its title, total and footer rows.\"\"\"
    frame = pd.read_excel(path, sheet_name=sheet, skiprows=2, dtype={'Código': str})
    frame.columns = frame.columns.str.replace('\\n', ' ', regex=False).str.strip()
    frame = frame[frame['País'].notna()].copy()
    return frame.rename(columns={'Código': 'country_code', 'País': 'country_name'})


exports = load_trade_sheet(trade_path, 'Exportação por Países (USD)')
imports = load_trade_sheet(trade_path, 'Importação por Países (USD)')

print('Exports:', exports.shape, '| Imports:', imports.shape)
print('Columns:', list(exports.columns)[:4], '...', list(exports.columns)[-2:])
exports.head()
"""

C2_Q = """
**Answers:**

- Each sheet gives 249 rows: 248 countries plus `ZZ`, Desconhecido, meaning the
  partner was not recorded.
- The single filter `frame['País'].notna()` removes the blank row, the
  `Total Geral` row and the `Fonte: INE` footer in one step, because none of them
  has a country name. Dropping rows by position would break the moment INE adds a
  line.
- `dtype={'Código': str}` keeps codes as text. It matters for the same reason it
  mattered for province codes: they are labels, not quantities.
- The newline inside `Ano\\n2004` is invisible when printed but would make every
  later column reference fail.
"""

C3_MD = """
## Task 11: Merge exports against imports

Both tables have one row per country, so this is a one to one merge. An outer
join keeps partners that appear on only one side.
"""

C3_CODE = """
YEAR = 'Ano 2025'

trade = pd.merge(
    exports[['country_code', 'country_name', YEAR]].rename(columns={YEAR: 'exports_usd'}),
    imports[['country_code', YEAR]].rename(columns={YEAR: 'imports_usd'}),
    on='country_code',
    how='outer',
    indicator=True,
    validate='one_to_one',
)
print('Merged:', trade.shape)
print(trade['_merge'].value_counts())
"""

C3B_CODE = """
trade['balance_usd'] = trade['exports_usd'].fillna(0) - trade['imports_usd'].fillna(0)

print('Largest surpluses:')
print(trade.nlargest(5, 'balance_usd')[['country_name', 'exports_usd',
                                        'imports_usd', 'balance_usd']].to_string(index=False))
print()
print('Largest deficits:')
print(trade.nsmallest(5, 'balance_usd')[['country_name', 'exports_usd',
                                         'imports_usd', 'balance_usd']].to_string(index=False))
"""

C3C_CODE = """
print(trade[trade['country_code'] == 'ZZ'][
    ['country_code', 'country_name', 'exports_usd', 'imports_usd', 'balance_usd']])
"""

C3_Q = """
**Answers:**

- All 249 countries are `both`, and `validate='one_to_one'` passed, so each
  partner appears exactly once on each side. Confirming a clean merge is a
  result, not a wasted check.
- China is by far the largest surplus partner and Portugal the largest deficit,
  which matches Angola's oil export and consumer goods import profile.
- `ZZ`, Desconhecido, carries 229,897 thousand USD of exports with an unrecorded
  partner. It is not an error to delete: it is a real, quantified gap in the trade
  statistics, and it belongs in a footnote. Silently dropping it would make the
  export total wrong.
- `fillna(0)` before subtracting is a decision, not a formality. It treats "no
  trade recorded" as zero trade, which is reasonable here and would not be if the
  gap meant "not yet reported".
"""

C4_MD = """
## Task 12: Save the trade table
"""

C4_CODE = """
trade = trade.drop(columns='_merge').reset_index(drop=True)
out_path = os.path.join(DATA_PROC_DIR, 'angola_trade_partners.csv')
trade.to_csv(out_path, index=False)
print('Saved:', out_path, '|', trade.shape)
"""

C4_Q = """
**Answers:**

- Three files written by this notebook: the province joined survey, the two wave
  stack, and the trade balance.
- Merging combines columns and needs a key. Appending combines rows and needs a
  shared schema. Part A and Part C did the first, Part B did the second, and the
  hard part in every case was the checking rather than the call itself.
"""
```

Assemble the whole notebook as:

```python
SOLUTION = [
    md(TITLE), md("### Path Setup (run first)"), code(PATHS_CODE),
    md(A1_MD), code(A1_CODE),
    md(A2_MD), code(A2_CODE), md(A2_Q),
    md(A3_MD), code(A3_CODE), code(A3B_CODE), code(A3C_CODE), md(A3_Q),
    md(A4_MD), code(A4_CODE), code(A4B_CODE), md(A4_Q),
    md(A5_MD), code(A5_CODE), code(A5B_CODE), md(A5_Q),
    md(B1_MD), code(B1_CODE),
    md(B2_MD), code(B2_CODE), md(B2_Q),
    md(B3_MD), code(B3_CODE), code(B3B_CODE), md(B3_Q),
    md(B4_MD), code(B4_CODE), code(B4B_CODE), code(B4C_CODE), md(B4_Q),
    md(C1_MD), code(C1_CODE), code(C1B_CODE),
    md(C2_MD), code(C2_CODE), md(C2_Q),
    md(C3_MD), code(C3_CODE), code(C3B_CODE), code(C3C_CODE), md(C3_Q),
    md(C4_MD), code(C4_CODE), md(C4_Q),
]
```

Gaps for `GAPS`:

| Cell | Exercise line |
|---|---|
| `A3_CODE` | `merged = pd.merge(df, province_lookup_old, on='province_code', how=  # your code here , indicator=  # your code here )` |
| `A3B_CODE` | `unmatched = merged[merged['_merge'] ==   # your code here ]` |
| `A4B_CODE` | `pd.merge(..., validate=  # your code here )` |
| `A5_CODE` | `print('Duplicate person keys:', final.  # your code here )` |
| `B2_CODE` | `naive = pd.concat(  # your code here: q3_full and df, ignore_index=True )` |
| `B3_CODE` | `q3 = q3_full[list(Q3_RENAME)].  # your code here: rename with Q3_RENAME` |
| `B3B_CODE` | `q3_slim = q3[SHARED].  # your code here: assign wave='2025Q3'` |
| `B4_CODE` | `population = waves.groupby('wave')['weight_ind'].  # your code here` |
| `C2_CODE` | inside `load_trade_sheet`, `frame = pd.read_excel(path, sheet_name=sheet,   # your code here: skiprows and dtype )` and `frame = frame[  # your code here: rows where País is not null ].copy()` |
| `C3_CODE` | `how=  # your code here`, `indicator=  # your code here`, `validate=  # your code here` |
| `C3B_CODE` | `trade['balance_usd'] =   # your code here: exports minus imports, treating gaps as 0` |
| `C4_CODE` | `trade.  # your code here: to_csv with index=False` |

- [ ] **Step 4: Build both notebooks**

```bash
python3 $SCRATCH/build_a25.py
```

- [ ] **Step 5: Execute the solution**

```bash
cd notebooks/solutions && python3 -m jupyter nbconvert --to notebook --execute \
  --inplace --ExecutePreprocessor.timeout=900 solution_a25_merging_combining.ipynb
```

Expected: exit code 0. The Q3 SPSS read makes this the slowest notebook, hence
the 900 second timeout.

- [ ] **Step 6: Assert all three outputs**

```bash
python3 -c "
import pandas as pd
a = pd.read_csv('data/20_processed/angola_iea_2025q4_analysis.csv',
                dtype={'province_code':'string'})
assert a.shape == (53297, 40), a.shape
assert a['province_name_ref'].isna().sum() == 6499, a['province_name_ref'].isna().sum()

w = pd.read_csv('data/20_processed/angola_iea_waves_q3_q4.csv')
assert w.shape == (108260, 13), w.shape
assert set(w['wave']) == {'2025Q3', '2025Q4'}
pop = w.groupby('wave')['weight_ind'].sum()
assert abs(pop.iloc[0] - pop.iloc[1]) / pop.iloc[1] < 0.01

t = pd.read_csv('data/20_processed/angola_trade_partners.csv', dtype={'country_code':'string'})
assert t.shape == (249, 5), t.shape
assert (t['country_code'] == 'ZZ').any()
top = t.nlargest(1, 'balance_usd')['country_name'].iloc[0]
assert top == 'China', top
print('OK: analysis', a.shape, '| waves', w.shape, '| trade', t.shape)
"
```

Expected: `OK: analysis (53297, 40) | waves (108260, 13) | trade (249, 5)`.

- [ ] **Step 7: Run the checker for a25**

```bash
python3 $SCRATCH/check_series.py a25_merging_combining
```

Expected: `PASS`.

- [ ] **Step 8: Commit**

```bash
git add notebooks/exercises/exercise_a25_merging_combining.ipynb \
        notebooks/solutions/solution_a25_merging_combining.ipynb
git commit -m "feat(notebooks): add Angola a25 merging, appending and trade exercise"
```

---

## Task 7: Register the series and run the full gate

**Files:**
- Modify: `notebooks/README.md`

**Interfaces:**
- Consumes: all ten notebooks from Tasks 2 to 6.
- Produces: nothing consumed downstream.

- [ ] **Step 1: Run the full checker and confirm it now passes**

```bash
python3 $SCRATCH/check_series.py
```

Expected: `PASS`. This is the first run with no stem argument, so it checks all
ten notebooks **and** the statistics. If it fails on statistics, the pipeline
outputs are stale: rerun Tasks 3 to 6 Step 3 in order.

- [ ] **Step 2: Confirm the series runs clean from an empty state**

```bash
rm -f data/10_cleaned/angola_iea_2025q4_*.csv data/20_processed/angola_iea_*.csv \
      data/20_processed/angola_trade_partners.csv
cd notebooks/solutions && for nb in solution_a22_types_subsetting \
    solution_a23_cleaning_missing_duplicates solution_a24_transforming_features \
    solution_a25_merging_combining; do
  echo "== $nb"
  python3 -m jupyter nbconvert --to notebook --execute --inplace \
    --ExecutePreprocessor.timeout=900 $nb.ipynb || break
done
```

Expected: four `== ` lines each followed by a successful conversion, no
`FileNotFoundError`. This proves the chain has no hidden dependency on a file
left over from development.

- [ ] **Step 3: Re-run the full checker after the clean rebuild**

```bash
python3 $SCRATCH/check_series.py
```

Expected: `PASS`.

- [ ] **Step 4: Add the series to the notebooks README**

Append to `notebooks/README.md`:

```markdown
## Angola series (Lesson 2, real data)

Exercises `a21` to `a25` work through Lesson 2 on real Angolan statistics: the
INE Inquerito ao Emprego em Angola (IEA) for Q3 and Q4 2025, and INE's
international trade of goods by partner country.

Run them in order. Each notebook after `a21` reads the file the previous one
wrote.

| Notebook | Topic | Reads | Writes |
|---|---|---|---|
| `exercise_a21_loading_diagnostics` | 2.1 Loading and diagnostics | `0_raw/angola/employment_survey/IEA_2025_IV_TRIM_IND.sav` | nothing |
| `exercise_a22_types_subsetting` | 2.2 Types and subsetting | the same `.sav` | `10_cleaned/angola_iea_2025q4_typed.csv` |
| `exercise_a23_cleaning_missing_duplicates` | 2.3 Cleaning | the typed checkpoint | `10_cleaned/angola_iea_2025q4_clean.csv` |
| `exercise_a24_transforming_features` | 2.4 Features | the cleaned file | `20_processed/angola_iea_2025q4_features.csv` |
| `exercise_a25_merging_combining` | 2.5 Merging and appending | the feature table, the Q3 `.sav`, the trade `.xlsx` | three files in `20_processed/` |

Worked answers are in `notebooks/solutions/`, with outputs committed so you can
compare against real numbers.

These notebooks use only `os`, `pandas`, `numpy` and `matplotlib`, plus
`pyreadstat` in a single cell of `a21`. Paths are built with `os.path.join`.
```

- [ ] **Step 5: Commit**

```bash
git add notebooks/README.md
git commit -m "docs: register the Angola Lesson 2 exercise series"
```

---

## Self-review notes

Recorded during planning, for the implementer's benefit:

- **The spec says province codes run 10 to 31. They run 10 to 30**, 21 provinces.
  This plan uses the correct range; the spec has the off-by-one.
- **The spec quotes relaxed unemployment as 31.3%.** That was measured before
  cleaning. After a23 removes 56 rows it is **31.4%**. This plan and the checker
  use 31.4%.
- **Every code block in Tasks 3 to 6 was executed against the real files during
  planning.** The expected values are measured, not predicted. If a step's actual
  output differs, suspect the notebook, not the number.
- **Build the exercise notebook before executing the solution**, or rebuild both,
  because `nbconvert --inplace` adds outputs to the file the builder wrote and a
  later `build_exercise()` run reading `SOLUTION` from memory is unaffected but
  re-running the whole builder will overwrite the executed solution. Tasks 2 to 6
  order the steps accordingly.

