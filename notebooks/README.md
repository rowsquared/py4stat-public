# notebooks

Contains exploratory and analytical notebooks.
Use notebooks for analysis workflows, visual checks, and demonstrations.

## Angola series (Lesson 2, real data)

Exercises `a21`, `a24` and `a25` work through Lesson 2 on real Angolan
statistics: the INE Inquerito ao Emprego em Angola (IEA) for Q3 and Q4 2025, and
INE's international trade of goods by partner country.

Run them in order. Each notebook reads the file the previous one wrote.

| Notebook | Topic | Reads | Writes |
|---|---|---|---|
| `exercise_a21_loading_inspecting_cleaning` | 2.1 Loading, inspecting, casting, missing values and duplicates | `0_raw/angola/employment_survey/IEA_2025_IV_TRIM_IND.sav` | `10_cleaned/angola_iea_2025q4_clean.csv` |
| `exercise_a24_transforming_features` | 2.4 Features | the cleaned file | `20_processed/angola_iea_2025q4_features.csv` |
| `exercise_a25_merging_combining` | 2.5 Merging and appending | the feature table, the Q3 `.sav`, the trade `.xlsx` | three files in `20_processed/` |

Worked answers are in `notebooks/solutions/`, with outputs committed so you can
compare against real numbers.

Conventions in this series:

- The SPSS file is read with `convert_categoricals=True`, so coded variables
  arrive as their Portuguese labels. Columns whose label conversion is wrong for
  the meaning, such as a year turned categorical by a `NAO SABE` sentinel, are
  recast explicitly.
- Column names are the questionnaire's own, lower cased. Nothing is renamed, so
  every name still matches the official codebook.
- `DATA_RAW_DIR` points at `../../data/0_raw/angola`, and sub folders and file
  names are joined onto it with `os.path.join`.
- Only `os`, `pandas`, `numpy` and `matplotlib` are used.
