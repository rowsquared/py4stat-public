# src/nodes

Contains reusable transformation functions — one function per processing step.

**PT:** Contém funções de transformação reutilizáveis: uma função por etapa de
processamento.

---

## What belongs here

## O que deve estar aqui

A **node** is a plain Python function that takes a DataFrame (and optional
parameters) and returns a transformed DataFrame. For example:

**PT:** Um **node** é uma função Python simples que recebe um DataFrame (e,
opcionalmente, alguns parâmetros) e devolve um DataFrame transformado. Por
exemplo:

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

**PT:** Guarde cada node no seu próprio ficheiro, com o nome da transformação
que executa:

```text
nodes/
├── clean_survey.py
├── compute_indicators.py
└── aggregate_by_region.py
```

---

## What does NOT belong here

## O que NÃO deve estar aqui

- File paths and data loading — that is the catalog's job.
  **PT:** Caminhos de ficheiros e carregamento de dados: essa é a função do
  catálogo.
- Configuration loading — pass values in as function parameters.
  **PT:** Leitura da configuração: passe os valores como parâmetros da função.
- Notebook-level coordination — that belongs in the notebook.
  **PT:** Coordenação ao nível do notebook: isso pertence ao notebook.

---

## How to use a node in a notebook

## Como usar um node num notebook

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

**PT:** O notebook coordena o fluxo de trabalho. O node executa a
transformação.
