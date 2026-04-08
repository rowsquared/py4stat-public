# py4stat-public

Public repository for the **Python for Statistics** training. It contains the exercises and examples covered during the course sessions.

## Data setup

To run the exercises, download the data from the [Moodle learning platform](https://learning.rowsquared.org).

Go to `py4stat1-malawi -> General -> Data download links`, download the data, and save the downloaded folder to `/data/0_raw/malawi`.

## Quarto reports

The `reports/` folder contains Quarto (`.qmd`) reports. Quarto is a publishing system that lets you combine code, narrative, and outputs into reproducible documents.

To render a report:

1. Install [Quarto](https://quarto.org/docs/get-started/)
2. From the repo root, run:

```bash
quarto render reports/malawi_ihs5_report.qmd
```

The rendered output will be saved in `reports/output/`.

## Reproducible workflows: data catalog and configuration

As covered in the **Building Reproducible Workflows** module, the `src/utilities/` folder contains two utility classes:

- `data_catalog.py` — a `DataCatalog` class to manage dataset paths and metadata in a centralised, consistent way
- `config.py` — a `Config` class to load and access project configuration

A working example showing how to use both is available at [notebooks/examples/example_catalog_config_loader.ipynb](notebooks/examples/example_catalog_config_loader.ipynb).
