# Household Living Conditions and Connectivity — Census 2022 (Exercise)

## 1. What this is

This folder is the **student exercise**: two Jupyter notebooks with blanks
(`___` / `'___'` and `# your code here:` hints) for you to complete. Fill every
blank, then render the project to an HTML report. The companion
`reports_solution/` folder is the completed version and renders as-is.

## 2. Prerequisites

The Python kernel needs `pandas` and `plotly` (the styled table in Task 3 also
uses `matplotlib` for its colour gradient). Confirm Quarto is installed:

```bash
quarto --version
```

If it is missing, ask the workspace admin, or install the Quarto CLI for Linux
into your home directory (do not assume internet access).

## 3. Open a Terminal

In JupyterHub: **File > New > Terminal**.

## 4. Render

```bash
cd reports
quarto render
```

Output is written to `_output/`.

## 5. View

Open the first page (`_output/01_tables.html`) from the Jupyter file browser, or
right-click and download it; the sidebar links the two chapters. With
`echo: false`, readers see the output only — not the code.

## 6. Live preview caveat

`quarto preview` serves on a local port that is only reachable under JupyterHub
if `jupyter-server-proxy` is configured. Otherwise prefer `quarto render` and
open the HTML.

## 7. Re-rendering

When `data/20_processed/census2022_household_analysis_226.csv` is regenerated
upstream (e.g. by exercise 2.C), run `quarto render` again to refresh the report.

## 8. Version control

Add `_output/` to `.gitignore`. Commit only the notebooks,
`_quarto.yml`, `styles.css`, and this README, not the rendered output.
