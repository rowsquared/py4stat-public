# notebooks

Contains exploratory and analytical notebooks.
Use notebooks for analysis workflows, visual checks, and demonstrations.

## Angola series (`_ao_`, real data)

Two notebooks on real Angolan statistics: the INE Inquerito ao Emprego em Angola
(IEA) for Q4 2025, and INE's international trade of goods. Markdown is in English
with a Portuguese translation under each block.

Run them in order. The second reads what the first wrote.

| Notebook | Topic | Reads | Writes |
|---|---|---|---|
| `exercise_25_ao_loading_inspecting_cleaning` | Loading, codebook driven column choice, casting, missing values, duplicates | `0_raw/angola/employment_survey/IEA_2025_IV_TRIM_IND.sav` | `10_cleaned/angola_iea_2025q4_clean.csv` |
| `exercise_26_ao_transforming_merging` | Custom functions and `apply`, merging and stacking the trade workbooks | the cleaned file, the same `.sav` for its codebook, and `0_raw/angola/international_trade/*.xlsx` | three files in `20_processed/` |

Worked answers are in `notebooks/solutions/`, with outputs committed so you can
compare against real numbers.

Conventions in this series:

- The SPSS file is read with `convert_categoricals=True`, so coded variables
  arrive as their Portuguese labels. Columns the label conversion miscast, such
  as a year turned categorical by a `NAO SABE` sentinel, are recast explicitly.
- Column names are the questionnaire's own, lower cased. Nothing is renamed, so
  every name still matches the official codebook.
- Mappings are extracted from a source, never typed by hand: variable
  descriptions from the SPSS header, country names and category labels from the
  workbook that defines them.
- `DATA_RAW_DIR` points at `../../data/0_raw/angola`, and sub folders and file
  names are joined onto it with `os.path.join`.
- Only `os`, `pandas`, `numpy` and `matplotlib` are used, plus `pyreadstat` in
  the one cell of each notebook that reads variable descriptions, which
  `pd.read_spss` does not expose.
