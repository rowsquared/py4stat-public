# src/nodes

Contains reusable transformation functions — one function per processing step.

---

## What belongs here

A **node** is a plain Python function that takes a DataFrame (and optional
parameters) and returns a transformed DataFrame. For example:

```python
def clean_survey(df, min_age=15, max_age=65, required_columns=None):
    if required_columns is None:
        required_columns = ["income", "region"]

    df = df[df["age"] >= min_age]
    df = df[df["age"] <= max_age]
    df = df.dropna(subset=required_columns)
    return df
```

Store each node in its own file, named after the transformation it performs:

```text
nodes/
├── clean_survey.py
├── compute_indicators.py
└── aggregate_by_region.py
```

---

## What does NOT belong here

- File paths and data loading — that is the catalog's job.
- Configuration loading — pass values in as function parameters.
- Notebook-level coordination — that belongs in the notebook.

---

## How to use a node in a notebook

```python
from src.nodes.clean_survey import clean_survey

config = Config("parameters.yaml")
cleaning = config.get("cleaning", {})

clean_df = clean_survey(
    raw_df,
    min_age=cleaning.get("min_age", 15),
    max_age=cleaning.get("max_age", 65),
    required_columns=cleaning.get("required_columns"),
)
```

The notebook coordinates the workflow. The node performs the transformation.
