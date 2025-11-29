# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Excel data cleaning tool (Excel 資料清洗工具) that removes duplicate records from Excel files. The project is modularized with v2.0, featuring a command-line interface, comprehensive type hints, logging system, and unit tests.

## Running the Application

### Main execution command
```bash
python -m src.main -i <input.xlsx> -o <output.xlsx>
```

### Common usage patterns
```bash
# Basic usage with default columns (Date and Machine No.)
python -m src.main -i input.xlsx -o output.xlsx

# Custom columns for duplicate detection
python -m src.main -i data.xlsx -o clean.xlsx -c "Date" "Product ID"

# Keep last duplicate instead of first
python -m src.main -i data.xlsx -o clean.xlsx -k last

# Remove all duplicates (keep none)
python -m src.main -i data.xlsx -o clean.xlsx -k none

# Enable debug logging with file output
python -m src.main -i data.xlsx -o clean.xlsx --log-level DEBUG --log-file app.log
```

### Legacy single-file version
```bash
python "Data Clean.py" -i input.xlsx -o output.xlsx
```

## Testing

### Run all tests
```bash
python -m pytest tests/
# or
python -m unittest discover tests/
```

### Run specific test file
```bash
python -m pytest tests/test_validators.py
python -m unittest tests.test_validators
```

### Run with coverage
```bash
python -m pytest --cov=src --cov=utils tests/
```

## Development Tools

### Code formatting
```bash
black src/ utils/ tests/
```

### Type checking
```bash
mypy src/ utils/
```

### Linting
```bash
flake8 src/ utils/ tests/
```

## Architecture

### Module Structure

The codebase follows a modular architecture with clear separation of concerns:

- **src/main.py**: Orchestration layer that coordinates the entire data cleaning workflow (CLI parsing → logging setup → data loading → duplicate removal → saving)
- **src/cli.py**: Command-line argument parsing using argparse
- **src/data_processor.py**: Core business logic for Excel I/O and duplicate detection
- **utils/logger.py**: Centralized logging configuration supporting both console and file output
- **utils/validators.py**: Input validation for file paths and DataFrame columns
- **tests/**: Unit tests using unittest framework

### Data Processing Flow

1. CLI arguments parsed via `parse_arguments()` in src/cli.py
2. Logging system initialized via `setup_logging()` in utils/logger.py
3. Input file loaded with `load_excel_data()` (validates file exists and is not empty)
4. Columns validated with `validate_columns()` (ensures required columns exist in DataFrame)
5. Duplicates removed with `remove_duplicate_records()` using pandas `drop_duplicates()`
6. Output saved with `save_excel_data()` (creates parent directories if needed)

### Key Design Decisions

- **Engine specification**: Uses openpyxl engine explicitly for Excel I/O (performance optimization)
- **Type safety**: All functions have complete type hints using typing module and pandas types
- **Error handling**: Specific exception handling for FileNotFoundError, ValueError, PermissionError
- **Zero hardcoding**: All default values (columns, keep strategy) configurable via CLI
- **Index handling**: Uses `ignore_index=True` in drop_duplicates to reset row indices

### Keep Strategy Types

The `keep_strategy` parameter accepts:
- `'first'`: Keep first occurrence of duplicate
- `'last'`: Keep last occurrence of duplicate
- `False`: Remove all duplicates (converted from CLI arg `'none'`)

Note: Type conversion happens in src/main.py:66-68 using `Literal['first', 'last', False]`

### Logging Levels

- DEBUG: Shows memory usage, field validation details
- INFO: Standard progress and statistics (default)
- WARNING/ERROR/CRITICAL: Issues and failures

## Known Issues

Reference BUG_REPORT.md for detailed bug analysis. Critical issues to be aware of:

1. **Input/output file collision**: No check prevents overwriting input file if paths are the same
2. **Log directory creation**: Log file parent directory must exist or FileHandler fails
3. **Excel format support**: Only .xlsx supported via openpyxl (not .xls)
4. **Preview output**: Uses `print()` instead of logging, so previews don't appear in log files

## Important Implementation Notes

### When modifying data processing:
- Always validate columns before accessing DataFrame columns
- Use `engine='openpyxl'` for consistency
- Reset index with `ignore_index=True` to avoid non-sequential indices
- Log statistics (count, percentage) for user feedback

### When adding CLI arguments:
- Add to `parse_arguments()` in src/cli.py
- Update main() in src/main.py to use the new argument
- Consider adding validation if needed
- Update version string if significant change

### When writing tests:
- Place in tests/ directory with test_*.py naming
- Add `sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))` for imports
- Test both success and failure cases
- Validate error messages contain expected Chinese text

### Path handling:
- Always use `pathlib.Path` objects (not strings)
- Convert CLI args to Path immediately after parsing
- Use `.absolute()` for logging paths
- Create parent directories with `parent.mkdir(parents=True, exist_ok=True)`

## Language and Localization

- All user-facing messages (logs, errors, docstrings) are in Traditional Chinese (繁體中文)
- Code comments and variable names use English
- Documentation (README.md, CLI_GUIDE.md) in Traditional Chinese
