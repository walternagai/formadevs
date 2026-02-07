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

## Code Style Guidelines

### Imports
- Use absolute imports: `from logic.group_formation import formar_grupos`
- Group imports: stdlib → third-party → local
- Separate groups with blank lines
- Import streamlit with try/except fallback for testing

### Formatting
- 4 spaces for indentation
- 120 character line limit
- Use f-strings for string formatting: `f"Grupo {i+1}"`
- Trailing commas in multi-line collections

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

### Error Handling
- Use try/except with specific exceptions
- Provide user-friendly error messages via UI components
- Log errors to console for debugging
- Handle ImportError for optional dependencies (e.g., streamlit in tests)

### Docstrings
- Use triple double quotes `"""`
- Brief description on first line
- More details if needed in following lines
- Keep under 100 characters per line

### UI Components
- Use Portuguese for all user-facing strings
- Prefix UI functions with action verb: `exibir_`, `importar_`, `carregar_`
- Use `st.` prefix for all Streamlit calls
- Wrap streamlit imports in try/except for testing compatibility

### Session State
- Initialize defaults in a dedicated function
- Use `st.session_state.get(key, default)` for safe access
- Keys use snake_case with Portuguese names

### Data Structures
- Students: `List[Dict[str, str]]` with keys "matricula", "nome"
- Groups: `List[List[Dict[str, str]]]` (list of student lists)
- History items: Dict with "data", "descricao", "grupos", "estudantes", "tamanho_grupo", "metodo"

### File Organization
- `app.py`: Main Streamlit entry point
- `logic/`: Business logic (group formation, validation)
- `ui/`: Streamlit UI components
- `utils/`: Utilities (persistence, exporters, helpers)
- `data/`: Persistent storage (JSON, CSV files)
- `tests/`: Test files (if exists)

### Dependencies
- streamlit: UI framework
- pandas: Data manipulation
- qrcode: QR code generation
- numpy: Numerical operations
- python-dateutil: Date handling
