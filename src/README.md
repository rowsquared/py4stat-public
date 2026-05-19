# src

Contains all reusable Python code for the project.

```text
src/
├── nodes/       # transformation functions (one function per step)
└── utilities/   # shared helpers used across notebooks and nodes
```

Code here does not run on its own. It is imported by notebooks.


```python
from src.utilities.config import Config
from src.nodes.clean_survey import clean_survey
```
