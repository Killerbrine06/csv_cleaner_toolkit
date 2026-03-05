# CSV Cleaner Toolkit

A configurable command-line tool for cleaning, validating, and analyzing CSV files using rule-based definitions.

This project demonstrates structured data processing, validation logic design, CLI orchestration, and logging practices in Python.

---

## Overview

CSV Cleaner Toolkit is designed to process messy CSV files by:

- Cleaning data according to defined rules
- Enforcing schema validation
- Detecting structural and data integrity issues
- Producing validation summaries via CLI logging

The tool is fully configurable through a JSON rules file, making it reusable across different datasets and use cases.

---

## Features

- Rule-based CSV schema validation
- Header type enforcement
- Email validation
- Numeric validation (int, float)
- Datetime validation
- Country validation
- Duplicate entry detection
- Not-null constraint enforcement
- Configurable uniqueness constraints
- Structured logging with verbosity levels
- CLI-based execution

---

## Tech Stack

- Python 3
- pandas
- argparse (CLI)
- logging module

---

## Installation

Clone the repository:

    git clone https://github.com/Killerbrine06/csv_cleaner_toolkit.git
    cd csv_cleaner_toolkit

Install dependencies:

    pip install -r requirements.txt

---

## Usage

Basic usage:

    python cli.py <csv_path> <rules_path> -o <output_path>

Example:

    python cli.py messy_sales.csv rules.json -o cleaned_sales.csv --verbose 2

---

## CLI Arguments

| Argument | Description |
|----------|------------|
| `csv_path` | Path to the input CSV file |
| `rules_path` | Path to the JSON rules file |
| `-o / --output_path` | Path where the cleaned CSV will be saved |
| `-r / --report` | (Optional) Generate report after validation |
| `--verbose` | Verbosity level (0 = errors only, 1 = summary, 2 = detailed debug output) |

---

## Rules File Format

The toolkit uses a JSON configuration file to define validation and cleaning rules.

Example:

    {
        "variables_format": {},
        "table": {
            "headers": {
                "customer_name": "str",
                "email": "email",
                "order_id": "int",
                "amount": "float",
                "date": "datetime",
                "country": "country",
                "notes": "str"
            },
            "unique_entries": ["order_id"],
            "not_null_entries": [
                ["order_id", 0],
                ["country", "ROU"]
            ]
        }
    }

### Explanation

#### headers

Defines expected columns and their types.

Supported types:

- str
- int
- float
- email
- datetime
- country

#### unique_entries

Defines columns that must contain unique values.

Example:

    "unique_entries": ["order_id"]

Ensures that `order_id` values are unique across the dataset.

#### not_null_entries

Defines columns that must not contain null values.

Format:

    ["column_name", default_value]

If null values are found:
- They may be replaced with the provided default value
- Or flagged during validation (depending on implementation)

---

## Validation Output

After processing, the tool logs a structured summary.

Example:

    INFO: Cleaned data loaded successfully.
    INFO: Rows: 10 | Columns: 7
    INFO: Validation summary:
    0 missing headers |
    1 null values across 1 columns |
    0 numeric errors |
    1 invalid emails |
    2 duplicate rows

Detailed validation logs are shown when running with:

    --verbose 2

---

## Exit Behavior

- Returns exit code `0` when no critical validation issues are found.
- Returns non-zero exit code when critical validation failures occur.
- Logs unexpected runtime errors and exits safely.

---

## Project Structure

    csv_cleaner_toolkit/
    ├── cli.py
    ├── toolkit/
    │   ├── cleaner.py
    │   ├── validator.py
    │   ├── report_generator.py
    ├── examples/
    ├── requirements.txt
    └── README.md

---

## Project Status

This project is maintained as a portfolio demonstration of:

- CLI tool design
- Data validation logic
- Structured logging
- Rule-driven data processing

Future improvements may include:

- Strict validation mode
- Configurable severity levels
- Packaging for pip installation
- Enhanced reporting formats

---

## Author

Vlad George Cacenschi  
Python Backend & Automation Developer  

---

## License

This project is intended for educational and portfolio purposes.