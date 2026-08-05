# notebooks

Contains exploratory and analytical notebooks.
Use notebooks for analysis workflows, visual checks, and demonstrations.

## Angola series (`_ao_`, real data)

Two notebooks on real Angolan statistics: the INE Inquerito ao Emprego em Angola
(IEA) for Q4 2025, and INE's international trade of goods. All prose and code
comments are English followed by Portuguese.

| Notebook | Topic | Reads | Writes |
|---|---|---|---|
| `exercise_26_ao_loading_inspecting_cleaning` | Codebook driven column choice, renaming, casting, missing values | `0_raw/angola/employment_survey/IEA_2025_IV_TRIM_IND.sav` | `10_cleaned/` cleaned data and codebook |
| `exercise_27_ao_transforming_merging` | Custom functions and `apply`, merging and stacking the trade workbooks | the cleaned file, its codebook, and `0_raw/angola/international_trade/*.xlsx` | three files in `20_processed/` |

Conventions:

- Columns are chosen by reading the SPSS variable descriptions, then renamed to
  readable names. The original name, new name and description are saved as
  `10_cleaned/angola_iea_2025q4_codebook.csv`, which is the bridge back to INE's
  documentation.
- `pd.read_spss` applies the file's value labels by default, so coded variables
  arrive as Portuguese text. Columns the label conversion miscast, such as a year
  turned categorical by a non numeric label, are recast explicitly.
- Mappings are extracted from a source, never typed by hand: descriptions from
  the saved codebook, country names and category labels from the workbooks.
- `DATA_RAW_DIR` points at `../../data/0_raw/angola`, with sub folders and file
  names joined onto it via `os.path.join`.
- Only `os`, `pandas`, `numpy` and `matplotlib` are used, plus `pyreadstat` in
  the single cell of 26 that reads variable descriptions.
