# CSV Reporter CLI

A config-driven command-line tool for reading, summarising, and analysing CSV files directly from the terminal. Built with Python using proper software engineering discipline — no hardcoded values, validated configuration, clean separation of concerns, and full test coverage.


## Overview

CSV Reporter is a terminal-based data analysis tool that lets you inspect and query any CSV file without opening a spreadsheet application. It reads all settings from external config files (`.env` and `config.yaml`), validates them with Pydantic before execution, and surfaces results through a clean, formatted CLI interface powered by Rich.


## Features

- Full CSV summary — row count, column count, data types, missing values
- Column-level statistical analysis — mean, sum, min, max, count, median
- Config-driven — zero hardcoded values, all settings live in `.env` or `config.yaml`
- Pydantic validation — config and inputs are validated before the app runs
- Graceful error handling — clear terminal messages instead of raw Python tracebacks
- Automated test suite — covers happy paths, edge cases, and error conditions
- Rich terminal output — formatted tables and coloured text


## Project Structure

```
csv-reporter/
│
├── app.py                  # CLI entry point — Typer commands
├── config.py               # Reads and combines .env + config.yaml
├── reporter.py             # CSV analysis logic
├── models.py               # Pydantic validation models
│
├── config.yaml             # Structured application settings
├── .env                    # Environment variables
├── sample.csv              # Sample data for testing
│
└── tests/
    ├── __init__.py
    └── test_reporter.py    # Pytest test suite
```

## Tech Stack

| Library | Purpose |
|---|---|
| [Typer](https://typer.tiangolo.com) | CLI argument parsing and command structure |
| [Pydantic](https://docs.pydantic.dev) | Config and input validation |
| [Pandas](https://pandas.pydata.org) | CSV loading and statistical analysis |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Reads `.env` file into environment variables |
| [PyYAML](https://pyyaml.org) | Parses `config.yaml` into Python dictionaries |
| [Rich](https://rich.readthedocs.io) | Terminal formatting, tables, and coloured output |
| [Pytest](https://pytest.org) | Automated testing framework |


## Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/csv-reporter.git
cd csv-reporter
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

> On Windows use: `venv\Scripts\activate`

**3. Install dependencies**
```bash
pip install typer pydantic pandas python-dotenv pyyaml pytest rich
```


## Configuration

The app reads settings from two config files. Neither file should contain hardcoded logic — they are configuration only.

### `.env`

```env
APP_NAME=CSV Reporter
DEFAULT_FILE=sample.csv
MAX_ROWS=1000
```

| Key | Description | Default |
|---|---|---|
| `APP_NAME` | Display name of the application | `CSV Reporter` |
| `DEFAULT_FILE` | CSV file used when no `--file` flag is passed | `sample.csv` |
| `MAX_ROWS` | Maximum number of rows the app will process | `1000` |

### `config.yaml`

```yaml
app:
  name: CSV Reporter
  version: "1.0"

defaults:
  file: sample.csv
  delimiter: ","
  encoding: utf-8

stats:
  available:
    - mean
    - sum
    - min
    - max
    - count
    - median
```

All config values are validated by Pydantic on startup. If any value is missing or invalid, the app exits immediately with a descriptive error.

## Usage

Make sure your virtual environment is active before running any commands:

```bash
source venv/bin/activate
```

### General Help

```bash
python app.py --help
```

### Command Help

```bash
python app.py summary --help
python app.py stats --help
```

---

## Commands

### `summary`

Prints a full overview of a CSV file including row count, column count, data types, and missing value counts.

```bash
python app.py summary --file sample.csv
```

**Options:**

| Flag | Shorthand | Required | Description |
|---|---|---|---|
| `--file` | `-f` | No | Path to the CSV file. Falls back to `DEFAULT_FILE` from `.env` |

**Example:**
```bash
# Use a specific file
python app.py summary --file sales_data.csv

# Use the default file from config
python app.py summary
```


### `stats`

Computes a specific statistical operation on a named column.

```bash
python app.py stats --column salary --stat mean
```

**Options:**

| Flag | Shorthand | Required | Description |
|---|---|---|---|
| `--file` | `-f` | No | Path to the CSV file. Falls back to `DEFAULT_FILE` from `.env` |
| `--column` | `-c` | **Yes** | Name of the column to analyse |
| `--stat` | `-s` | No | Statistical operation to run. Defaults to `mean` |

**Available stats:** `mean`, `sum`, `min`, `max`, `count`, `median`

**Examples:**
```bash
# Mean salary
python app.py stats --column salary --stat mean

# Maximum age
python app.py stats --column age --stat max

# Total score
python app.py stats --column score --stat sum

# Using shorthand flags
python app.py stats -c salary -s median
```


## Running Tests

The test suite uses Pytest and covers all three core modules.

```bash
# Run all tests
pytest tests/ -v

# Run a specific test
pytest tests/test_reporter.py::test_get_column_stats_mean -v
```

### Test Coverage

| Area | What Is Tested |
|---|---|
| `load_csv` | Successful load, file not found, wrong file extension |
| `get_column_stats` | mean, sum, min, max, invalid column, invalid stat, non-numeric column |
| `get_summary` | Row count, column count, numeric columns, text columns, missing values |

## Architecture

The project follows a strict separation of concerns. Each module owns exactly one responsibility.

```
.env + config.yaml
       │
       ▼
   config.py          Reads both config sources, merges them
       │
       ▼
   models.py          Pydantic validates all values before app starts
       │
       ▼
  reporter.py         Pure analysis logic — no CLI, no config awareness
       │
       ▼
    app.py            CLI layer only — calls reporter, renders results
```

The CLI layer (`app.py`) has no knowledge of how data is processed. The analysis layer (`reporter.py`) has no knowledge of how it is called. This makes each layer independently testable and replaceable.


## Example Output

### `summary` command

```
Loading file: sample.csv

Total Rows:    8
Total Columns: 5

             Columns Overview
┏━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Column Name ┃ Type    ┃ Missing Values ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ name        │ text    │ 0              │
│ age         │ numeric │ 0              │
│ department  │ text    │ 0              │
│ salary      │ numeric │ 0              │
│ score       │ numeric │ 0              │
└─────────────┴─────────┴────────────────┘
```

### `stats` command

```
File:   sample.csv
Column: salary
Stat:   mean

MEAN of 'salary': 79750.0
```

### Error handling

```
Error: Column 'wage' not found. Available: ['name', 'age', 'department', 'salary', 'score']
```

---

## License

MIT