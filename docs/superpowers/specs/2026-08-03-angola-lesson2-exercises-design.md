# Angola Lesson 2 Exercise Series: Design

**Date:** 2026-08-03
**Branch:** `angola`
**Status:** Approved, ready for implementation planning

## Goal

Build a five-notebook exercise series (plus five matching solution notebooks) that
lets learners practise Lesson 2 of the Python course on real Angolan statistical
data, rather than on the simulated Datania household file used by the existing
`exercise_221` to `exercise_225` series.

## Source material

The exercises follow the course content in Notion, "Book Version 2" under
Lesson 2 (Data loading & quality control):

| Section | Title | Notion page |
|---|---|---|
| 2.0 | Learning Objectives | `7d8d0a89ce6940f7953601f21e1081f2` |
| 2.1 | Loading Data & First Diagnostics | `84780b4313df41eb973f55774914092f` |
| 2.2 | Data Types and Subsetting | `077a054873594570bca57b186ffb1d68` |
| 2.3 | Cleaning, Missing Values & Duplicates | `99c0efeced5c4b6ebd23d170059ece7e` |
| 2.4 | Transforming data and creating new features | `285251f576804fc09dfc4557d2a4b3a2` |
| 2.5 | Merging & Combining Datasets | `b7f98c04e0614a319e44ab1e4f41f41a` |

Structure and tone follow the existing notebooks:
`exercise_221_data_loading_datania.ipynb`, `exercise_222_data_types_and_subsetting.ipynb`,
`solution_223_cleaning_missing_duplicates.ipynb`, `exercise_224_transforming_features.ipynb`,
`exercise_225_merging_combining.ipynb`.

## Constraints

These are non-negotiable and apply to every notebook.

1. **Library allowlist.** Only libraries discussed in the Lesson 2 content:
   `os`, `pandas as pd`, `numpy as np`, `matplotlib.pyplot as plt`.
   `pyreadstat` is permitted in exactly one task of a21 (section 2.1 names it as
   the SPSS reader and teaches the equivalent codebook idea for Stata via
   `variable_labels()`); everywhere else SPSS loading goes through `pd.read_spss`.
   No other imports. No `seaborn`, `plotly`, `duckdb`, `geopandas`, `sklearn`.
2. **Paths.** Always `os.path.join`. Never `pathlib.Path`. Path constants are
   relative to the notebook, in the existing style: `DATA_RAW_DIR = '../../data/0_raw'`.
3. **Testing.** Every exercise notebook has a corresponding solution notebook in
   `notebooks/solutions/`. Each solution is executed end to end; a non-zero exit
   is a failure. Outputs are committed.
4. **No em dashes** in any authored markdown or code comment in the new notebooks.
   Use colons, commas, or hyphens. (This differs deliberately from the existing
   221 to 225 series, which uses em dashes; those are not being retrofitted.)
5. **Raw data is read-only.** Nothing writes into `data/0_raw/`.

## Data sources

### Primary: Angola employment survey (the pipeline spine)

`data/0_raw/angola/employment_survey/IEA_2025_IV_TRIM_IND.sav`

SPSS file, 20 MB, UTF-8, **53,353 rows x 206 columns**. Individual-level records
from the Inquérito ao Emprego em Angola, Q4 2025. Variable and value labels are in
Portuguese.

Verified characteristics that the exercises are built on:

| Fact | Value | Used in |
|---|---|---|
| Person key | `NIDF` + `PPNO`, with **8 duplicate pairs** | a23 |
| Household count | 13,036 households, mean 4.09 persons, max 20 | a24 |
| `G_12`, `G_13` (household size, adults) | **100% missing** in all 53,353 rows | a21, a23 |
| `DEM_AGE` | range 0 to 120; 6 people aged 98+; 1,532 aged 0 | a21, a23 |
| `WKT_USHRSTOT` (usual hours) | 3 rows coded `997`; real max 120 | a21, a23 |
| `MJT_SYR` (job start year) | **1,673 rows coded `9997`**; mean 3164 vs real range 1965 to 2025 | a21, a23 |
| `GHVEDT` (interview date) | float `20251204.0`, i.e. YYYYMMDD | a22 |
| Employment columns | ~78% missing **by survey skip pattern**, not by error | a23 |
| Household heads | 6 households have **two** `DEM_REL == 1` rows | a23 |
| `PROV` | codes 10 to 31, 21 distinct, labelled | a24, a25 |
| `AREA_RESID` | 1 = Urbana (34,173), 2 = Rural (19,180) | a24 |
| `DEM_SEX` | 1 = Masculino (25,601), 2 = Feminino (27,752) | a24 |

Verified loader behaviour:

- `pd.read_spss(path, usecols=[...], convert_categoricals=True)` applies the
  Portuguese value labels and returns `category` dtype for labelled variables.
  Notably it turns `MJT_SYR`, a **year**, into a `category`, because its `9997`
  sentinel carries a label. This is a teaching point in a21.
- `pd.read_spss(path, usecols=[...], convert_categoricals=False)` returns raw
  numeric codes as `float64`. The pipeline uses this form so that a22 and a24 can
  teach `.replace()` and `.map()`.
- `pyreadstat.read_sav(path, metadataonly=True)` exposes `column_names_to_labels`
  and `value_labels` without loading the data. This is the codebook.

### Secondary: Angola international trade (a25 only)

`data/0_raw/angola/international_trade/*.xlsx`, seven workbooks, 5.8 MB total.

a25 uses `Comercio Externo de Bens por Países Parceiros.xlsx`, which has four
sheets: `Exportação por Países (Kz)`, `Exportação por Países (USD)`,
`Importação por Países (Kz)`, `Importação por Países (USD)`.

Verified structure of each sheet (255 rows x 24 columns raw):

- Rows 0 and 1: title (`Quadro n.º 1 ...`) and unit (`U.M.: Em milhares de USD`)
- Row 2: the real header, `Código`, `País`, `Ano\n2004` ... `Ano\n2025`
- Row 3: blank
- Row 4: `Total Geral`, with `País` empty
- Rows 5 to 253: 248 countries by ISO2 code, plus `ZZ` = `Desconhecido`
- Row 254: footer, `Fonte: INE, Direcção de Estatísticas Económicas`

Loading with `pd.read_excel(f, sheet_name=..., skiprows=2, dtype={'Código': str})`
yields a 252 x 24 frame with 2 null `Código` values (blank row and footer) and
year columns already `float64`. Column names carry an embedded newline
(`'Ano\n2004'`) that must be stripped.

Verified: a single `df[df['País'].notna()]` filter removes the blank row, the
`Total Geral` row and the `Fonte` footer in one step, leaving exactly 249 rows,
248 countries plus `ZZ`.

There is no meaningful semantic join between an individual-level labour survey and
country-level trade totals. a25 therefore presents them as **two independent join
problems** in two clearly separated parts, and says so in the notebook text.

## File structure

```
notebooks/exercises/
  exercise_a21_loading_diagnostics.ipynb
  exercise_a22_types_subsetting.ipynb
  exercise_a23_cleaning_missing_duplicates.ipynb
  exercise_a24_transforming_features.ipynb
  exercise_a25_merging_combining.ipynb

notebooks/solutions/
  solution_a21_loading_diagnostics.ipynb
  solution_a22_types_subsetting.ipynb
  solution_a23_cleaning_missing_duplicates.ipynb
  solution_a24_transforming_features.ipynb
  solution_a25_merging_combining.ipynb
```

Naming rationale: `a` marks Angola, `21` to `25` map onto Notion sections 2.1 to
2.5. This scales if Malawi, Zambia, Tanzania or South Africa get their own series
later, and keeps the existing flat folder layout, so the `'../../data/...'`
relative paths are unchanged.

Notebook titles use the form `Exercise 2.1: Loading Data & First Diagnostics (Angola IEA)`.

## Data flow

```
a21  0_raw/angola/employment_survey/IEA_2025_IV_TRIM_IND.sav  ->  (no output)
a22  same .sav                                                ->  10_cleaned/angola_iea_2025q4_typed.csv
a23  10_cleaned/angola_iea_2025q4_typed.csv                   ->  10_cleaned/angola_iea_2025q4_clean.csv
a24  10_cleaned/angola_iea_2025q4_clean.csv                   ->  20_processed/angola_iea_2025q4_features.csv
a25  20_processed/angola_iea_2025q4_features.csv              ->  20_processed/angola_iea_2025q4_analysis.csv
     0_raw/angola/international_trade/Comercio Externo de
       Bens por Países Parceiros.xlsx                         ->  20_processed/angola_trade_partners.csv
```

CSV, not parquet, is deliberate: sections 2.2 and 2.3 both teach that CSV loses
dtypes, so dates must be re-parsed on every reload. Parquet would remove that
lesson. No data files are tracked in git, so checkpoints cost the repo nothing.

## Column subset and renaming

a21 teaches `usecols` by cutting 206 columns to 24. a22 renames them to English
snake_case. Every later notebook uses the English names.

| SPSS name | English name | Notes |
|---|---|---|
| `NIDF` | `household_id` | float64 in source; becomes string |
| `PPNO` | `person_no` | second half of the person key |
| `G_06_ID_IEA` | `cluster_id` | sampling cluster |
| `PROV` | `province_code` | zero-padded 2-digit string; a25 merge key |
| `AREA_RESID` | `area_type` | 1 Urbana, 2 Rural |
| `G_15_TRIMESTRE` | `quarter` | single value 4; teaches the constant-column check |
| `DEM_REL` | `rel_to_head` | 1 = head; drives the two-head validation |
| `DEM_SEX` | `sex` | |
| `DEM_AGE` | `age` | |
| `DEM_MRT` | `marital_status` | 38.4% missing |
| `DEM_EDL` | `education_level` | 56.6% missing |
| `S03_01` | `school_attendance` | |
| `ATW_PAY` | `worked_for_pay` | ILO status input |
| `ATW_PFT` | `worked_own_account` | ILO status input |
| `ATW_FAM` | `worked_family_business` | ILO status input |
| `ABS_JOB` | `absent_from_job` | ILO status input |
| `SRH_JOB` | `sought_work` | ILO status input |
| `SRH_AVL` | `available_to_work` | ILO status input |
| `WKT_USHRSTOT` | `hours_usual` | `997` sentinel |
| `WKT_ACHRSTOT` | `hours_actual` | `997` sentinel |
| `MJT_SYR` | `job_start_year` | `9997` sentinel |
| `MJU_SIZ` | `workplace_size` | |
| `MJJ_EMP_REL` | `employment_relation` | |
| `GHVEDT` | `interview_date` | YYYYMMDD float |
| `G_12` | `hh_size_reported` | 100% empty; diagnosed in a21, dropped in a23 |
| `G_13` | `hh_adults_reported` | 100% empty; diagnosed in a21, dropped in a23 |

That is 26 entries; the two all-empty columns are loaded on purpose so learners
find and remove them, leaving 24 working columns.

## Notebook contents

Each notebook follows the house structure: a title cell listing what will be
practised, a pipeline note, a **Path Setup (run first)** cell, then numbered
`## Task N` sections. Each task is a markdown explainer, one or more code cells
with `# your code here` gaps, and a closing **Questions:** block. Solutions fill
the gaps and replace **Questions:** with **Answers:**.

### a21: Loading Data & First Diagnostics (section 2.1)

1. Load the `.sav` with `pd.read_spss`, default `convert_categoricals=True`.
   Inspect with `head()`, `tail()`, `sample()`.
2. Contrast label conversion: reload with `convert_categoricals=False` and compare
   dtypes. Observe that `MJT_SYR`, a year, is a `category` in the labelled load
   because `9997` is labelled. The pipeline continues with raw codes.
3. Read the codebook with `pyreadstat.read_sav(metadataonly=True)`:
   `column_names_to_labels` and `value_labels`. This is the SPSS counterpart to
   the Stata `variable_labels()` trick in 2.1.
4. Cut 206 columns to 26 with `usecols`. Compare `memory_usage(deep=True)` before
   and after.
5. Inspect and standardise column names (`.str.strip()`, `.str.lower()`).
6. `df.info()`: find the two 100%-empty columns and the skip-pattern missingness.
7. `df.describe()` and `df.describe(include='all').T`: find `age` max 120,
   `hours_usual` max 997, `job_start_year` mean 3164.
8. `value_counts(dropna=False)` on `PROV`, `AREA_RESID`, `DEM_SEX`, `DEM_EDL`.
9. `df.hist(bins=20, figsize=(15, 10))` for a visual sweep.

Writes no file.

### a22: Data Types and Subsetting (section 2.2)

1. DataFrame vs Series, `type()` and `.dtypes`.
2. Rename the 26 columns to the English names in the table above, via a rename
   dictionary.
3. Identifiers as text: `household_id` arrives as `float64` (`8501.0`), so it goes
   `.astype('int64').astype('string')`. Same for `person_no` and `cluster_id`.
   `province_code` takes the same route and then `.str.zfill(2)`, ready for the
   a25 merge. Angola's province codes run 10 to 31, so `zfill(2)` changes nothing
   here and the notebook must say so: it is a documented safeguard, framed the
   same way `exercise_221` frames its already-clean column names, not a fix for a
   defect in this file.
4. Dates: `interview_date` is the float `20251204.0`. Convert to int, then string,
   then `pd.to_datetime(format='%Y%m%d')`. Extract parts with `.dt`.
5. Categories: convert `area_type` and `sex` to `category` and measure the memory
   saved.
6. Subsetting to inspect, not to clean: boolean indexing on `hours_usual > 100`
   and `age >= 98`, combined conditions with `&` and parentheses, `isin()` on a
   province code list, `str.contains()` on a text column.
7. Save the typed checkpoint to `10_cleaned/angola_iea_2025q4_typed.csv`, reload,
   and confirm `interview_date` came back as `object`, since CSV cannot store a
   datetime.

### a23: Cleaning, Missing Values & Duplicates (section 2.3)

1. `df_clean = df.copy()`.
2. Detect missing: `isna().sum()`, the percentage version, and a matplotlib bar
   chart of columns with gaps.
3. Drop the two 100%-empty columns, checking shape before and after.
4. Coded missing values: recode `997` in `hours_usual` and `hours_actual`, and
   `9997` in `job_start_year`, using a reusable
   `recode_coded_missing(series, codes)` helper. Print the `job_start_year` mean
   before and after, roughly 3164 down to roughly 2019.
5. Missing by design vs missing by error: show that `dropna()` would destroy the
   dataset because employment columns are ~78% missing by skip pattern, and that
   `dropna(subset=['household_id', 'person_no'])` is the correct rule.
6. Duplicates: no exact duplicate rows exist, so the lesson is the compound key.
   `duplicated(subset=['household_id', 'person_no'], keep=False)` finds the real 8
   pairs; resolve by keeping the most complete record via a `missing_count` column.
7. Validation rules, with a boxplot of `hours_usual`. Verified effects, so the
   rules are not silently no-ops: `age.between(0, 100)` removes 3 rows (ages 102,
   103 and 120), and `hours_usual.between(0, 98)` removes 45 rows, 98 hours being
   14 hours a day, 7 days a week. Note that `between(0, 120)` would remove nothing,
   because the real post-recode maximum is exactly 120. Discuss whether `age == 97`
   is a real age or a `NÃO SABE` sentinel, given that 97 is the sentinel elsewhere
   in this file.
8. Cross-column validation: count `rel_to_head == 1` per household and find the 6
   households with two heads, the exact case 2.3 says `info()` and `describe()`
   cannot catch.
9. Save to `10_cleaned/angola_iea_2025q4_clean.csv`.

### a24: Transforming Data & Creating New Features (section 2.4)

1. Recode with `pd.cut()`: age bands `[0, 15, 25, 65, 120]` labelled
   `Child`, `Youth`, `Adult`, `Elderly`, aligned to the ILO working-age definition.
2. Map codes to labels with `.map()` and dictionaries taken from the codebook:
   `province_name`, `sex_label`, `area_label`, `education_label`.
3. `np.select()` for ILO labour force status, three-way
   (`Employed`, `Unemployed`, `Outside labour force`), built from
   `worked_for_pay`, `worked_own_account`, `worked_family_business`,
   `absent_from_job`, `sought_work`, `available_to_work`.
4. `np.where()` for a `full_time` flag at 35 usual hours, and `.loc[]` for a
   conditional update of an existing column.
5. `assign()` with dependent lambdas: `job_tenure_years = 2025 - job_start_year`,
   then a band derived from it in the same call.
6. Household size without `groupby`, which is not taught until Lesson 3:
   `df['household_id'].map(df['household_id'].value_counts())`. `value_counts()`
   comes from 2.1 and `.map()` from 2.4, so this stays inside the curriculum.
7. `apply()`: a named row-wise function computing hours per day with guards for
   missing and zero, plus a lambda for a simple one-liner, with the performance
   caveat stated.
8. Save to `20_processed/angola_iea_2025q4_features.csv`.

### a25: Merging & Combining Datasets (section 2.5)

**Part A, the survey.**

1. Build a `province_lookup` DataFrame from the codebook (21 provinces, codes 10
   to 31) and left-merge it on `province_code`.
2. Join key hygiene: matching dtypes on both sides, `.str.strip()`, and missing
   key counts.
3. Audit with `indicator=True`, and compare inner, left, and outer row counts.
4. Cardinality: build a deliberately duplicated lookup, show the row explosion,
   then catch it with `validate='many_to_one'`.
5. Post-merge validation: row count before and after, key uniqueness, unmatched
   rate. Save to `20_processed/angola_iea_2025q4_analysis.csv`.

**Part B, the trade data.** The notebook states plainly that this is a separate
join problem on a separate dataset, not a join to the survey.

6. Load `Exportação por Países (USD)` with `skiprows=2` and `dtype={'Código': str}`.
   Strip the `\n` from `Ano\n2004`-style headers. Drop the blank row, the
   `Total Geral` row, and the `Fonte: INE` footer, using the null `País` test.
7. Load `Importação por Países (USD)` the same way, then merge exports against
   imports on the country code with `suffixes=('_export', '_import')` and
   `indicator=True`. Compute a 2025 trade balance.
8. Audit `ZZ` (`Desconhecido`) and any `left_only` or `right_only` countries, and
   discuss reporting them back to the data producer rather than dropping them.
9. `pd.concat()` the Kwanza and USD export sheets with a `currency` column and
   `ignore_index=True`, then demonstrate schema drift by renaming a column in one
   input and observing the silently half-empty result.
10. Save to `20_processed/angola_trade_partners.csv`.

## Supporting changes

- `pyproject.toml`: add `pyreadstat` and `openpyxl`. Both are required to open
  these files and neither is currently in the project venv. Verified absent:
  `.venv/bin/python -c "import pyreadstat"` fails today.
- `notebooks/README.md`: add a short section registering the Angola series and its
  run order.

## Testing strategy

The solution notebooks are the tests.

1. Each solution notebook is executed end to end:
   `jupyter nbconvert --to notebook --execute --inplace <solution>.ipynb`.
   A non-zero exit fails the task.
2. Execution runs in pipeline order (a21, a22, a23, a24, a25), because a22
   onwards depend on the checkpoint written by the previous notebook.
3. Outputs are committed with the solution notebooks, matching
   `solution_221`, `solution_222` and `solution_226`.
4. Each exercise notebook is checked to be valid JSON with every code cell's
   `outputs` empty, and to contain no `pathlib`, no `Path(`, and no import outside
   the allowlist.

## Out of scope

- Retrofitting the existing 221 to 225 notebooks (em dashes, or anything else).
- Series for Malawi, Zambia, Tanzania, or South Africa.
- Lesson 2.6 (SQL with DuckDB) and the Daily Recap page.
- The six trade workbooks other than the partner-countries one.
- A pytest or nbmake harness. Execution is a manual gate per task.
