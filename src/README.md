# src

Contains all reusable Python code for the project.

**PT:** Contém todo o código Python reutilizável do projeto.

```text
src/
├── nodes/       # transformation functions (one function per step)
│                # PT: funções de transformação (uma função por etapa)
└── utilities/   # shared helpers used across notebooks and nodes
                 # PT: funções auxiliares partilhadas por notebooks e nodes
```

Code here does not run on its own. It is imported by notebooks.

**PT:** O código aqui não é executado por si só. É importado pelos notebooks.


```python
from src.utilities.config import Config
from src.nodes.clean_survey import clean_survey
```
