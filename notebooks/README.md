# notebooks

Contains exploratory and analytical notebooks.
Use notebooks for analysis workflows, visual checks, and demonstrations.

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
