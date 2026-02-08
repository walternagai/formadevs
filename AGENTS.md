# Agent Instructions

## Commands

### Running the Application
```bash
streamlit run app.py
```

### Dependencies
```bash
pip install -r requirements.txt
```

### Linting & Formatting
```bash
# Check code style with ruff
ruff check .

# Format code with ruff
ruff format .

# Check specific file
ruff check logic/group_formation.py
```

### Type Checking
```bash
mypy .
mypy app.py
mypy logic/
```

 ### Testing
```bash
# Run all tests
pytest

# Run single test file
pytest tests/test_group_formation.py

# Run specific test
pytest tests/test_group_formation.py::test_formar_grupos_aleatorio

# Run with coverage
pytest --cov=. --cov-report=term-missing
```

### Running a Single Test (Recommended Format)
```bash
pytest tests/ -k "test_function_name"
pytest -v tests/test_group_formation.py::test_formar_grupos_aleatorio
```

## Code Style Guidelines

### Imports
- Use absolute imports: `from logic.group_formation import formar_grupos`
- Group imports: stdlib → third-party → local
- Separate groups with blank lines
- Import streamlit with try/except fallback for testing
- Import order example:
  ```python
  from datetime import datetime
  import random
  
  import pandas as pd
  import streamlit as st
  
  from logic.group_formation import formar_grupos
  ```

### Formatting
- 4 spaces for indentation (no tabs)
- 120 character line limit
- Use f-strings for string formatting: `f"Grupo {i+1}"`
- Trailing commas in multi-line collections:
  ```python
  defaults = {
      'chave1': valor1,
      'chave2': valor2,
  }
  ```

### Naming Conventions
- Functions: `snake_case` (e.g., `formar_grupos`, `exibir_grupos`)
- Classes: `PascalCase` (e.g., `ValidadorDeDados`)
- Constants: `UPPER_CASE` (e.g., `TAMANHO_PADRAO`)
- Private functions: `_prefix_with_underscore`

### Types
- Use type hints for function parameters and returns
- Use `Optional[T]` for nullable values
- Use `List[Dict[str, Any]]` for complex structures
- Streamlit session state uses `Dict[str, Any]`
- Example:
  ```python
  def formar_grupos(
      estudantes: List[Dict[str, str]],
      tamanho_grupo: int,
      metodo: str = "Aleatório"
  ) -> List[List[Dict[str, str]]]:
  ```

### Error Handling
- Use try/except with specific exceptions
- Provide user-friendly error messages via UI components
- Log errors to console for debugging
- Handle ImportError for optional dependencies (e.g., streamlit in tests)
  ```python
  try:
      import streamlit as st
  except ImportError:
      st = None
  ```

### Docstrings
- Use triple double quotes `"""`
- Brief description on first line
- More details if needed in following lines
- Keep under 100 characters per line
- Use Google-style format for parameters and returns

### UI Components
- Use Portuguese for all user-facing strings
- Prefix UI functions with action verb: `exibir_`, `importar_`, `carregar_`, `salvar_`
- Use `st.` prefix for all Streamlit calls
- Wrap streamlit imports in try/except for testing compatibility
- Follow pattern: `ui/function_name.py` for UI components

### Session State
- Initialize defaults in a dedicated function (e.g., `inicializar_sessao()`)
- Use `st.session_state.get(key, default)` for safe access
- Keys use snake_case with Portuguese names
- Document all session state keys in initialization function

### Data Structures
- Students: `List[Dict[str, str]]` with keys "matricula", "nome"
- Groups: `List[List[Dict[str, str]]]` (list of student lists)
- History items: Dict with "data", "descricao", "grupos", "estudantes", "tamanho_grupo", "metodo"
- Group formation results: Dict with "grupos", "estudantes", "tamanho", "metodo", "data"

### File Organization
- `app.py`: Main Streamlit entry point
- `logic/`: Business logic (group formation, validation, data processing)
- `ui/`: Streamlit UI components (forms, displays, views)
- `utils/`: Utilities (persistence, exporters, helpers, QR generation)
- `data/`: Persistent storage (JSON, CSV files)
- `tests/`: Test files (when tests are available)
- Use `__init__.py` files to expose module-level functions: `from logic import *`

### Dependencies
- streamlit: UI framework
- pandas: Data manipulation
- qrcode: QR code generation  
- Pillow: Image processing for QR codes
- xlsxwriter: Excel export functionality
- python-dateutil: Date handling
