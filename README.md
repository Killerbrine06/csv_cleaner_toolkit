# CSV Cleaner Toolkit

A configurable command-line toolkit for **cleaning, validating, and analyzing CSV datasets**, with optional **AI-assisted explanations of data quality issues**.

The project demonstrates structured data processing pipelines, rule-driven validation, CLI tool design, and cost-efficient LLM integration.

---

# Overview

Real-world CSV datasets often contain:

* inconsistent column formatting
* missing or invalid values
* duplicate rows
* incorrect data types
* messy country/date formats

**CSV Cleaner Toolkit** provides a rule-based pipeline to automatically:

1. Clean datasets
2. Validate schema constraints
3. Detect data quality issues
4. Generate structured validation reports
5. Optionally explain issues using an AI assistant

The system is fully configurable through a **JSON rules file**, allowing it to adapt to different datasets without modifying the code.

---

# Key Features

### Data Cleaning

* Column normalization
* Whitespace removal
* Empty value handling
* Duplicate row removal
* Country code normalization (ISO3)
* Flexible datetime parsing

### Rule-Based Validation

Configurable validation rules allow enforcement of:

* schema structure
* column types
* unique constraints
* non-null requirements
* email format validation
* numeric validation

### AI-Assisted Dataset Explanation

An optional AI module can analyze dataset summaries and provide **human-readable explanations of potential data issues**.

The AI integration:

* only receives dataset metadata and small samples
* avoids sending entire datasets
* minimizes token usage and cost

---

# Example Workflow

Input dataset:

```
messy_sales.csv
```

Pipeline:

```
CSV
 ↓
Cleaner
 ↓
Validator
 ↓
Report Generator
 ↓
(Optional) AI Explanation
```

Output:

```
cleaned_sales.csv
validation_report.txt
```

Example validation summary:

```
Rows: 10 | Columns: 7

Validation summary: 0 missing headers | 1 null values across 1 columns | 0 numeric errors | 1 invalid emails | 2 duplicate rows
```

Optional AI explanation:

```
The dataset contains duplicate rows and invalid email formats.
Duplicate rows may inflate metrics such as revenue or customer counts.
Invalid email values may indicate incomplete or corrupted customer records.
```

---

# Installation

Clone the repository:

```
git clone https://github.com/Killerbrine06/csv_cleaner_toolkit.git
cd csv_cleaner_toolkit
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Basic Usage

Clean and validate a dataset:

```
python cli.py <csv_path> <rules_path> -o <output_path>
```

Example:

```
python cli.py examples/messy_sales.csv rules.json -o cleaned_sales.csv --verbose 2
```

---

# AI Dataset Explanation

To generate an explanation of detected dataset issues:

```
python ai_cli.py explain <csv_path> <rules_path>
```

The tool will:

1. Run the cleaning and validation pipeline
2. Generate a validation report
3. Send a dataset summary and sample rows to the AI model
4. Print a human-readable explanation

---

# Rules Configuration

The toolkit uses a JSON rules file to define dataset structure.

Example:

```
{
  "table": {
    "headers": {
      "customer_name": "str",
      "email": "email",
      "order_id": "int",
      "amount": "float",
      "date": "datetime",
      "country": "country"
    },
    "unique_entries": ["order_id"],
    "not_null_entries": [
      ["order_id", 0],
      ["country", "ROU"]
    ]
  }
}
```

Supported types:

* `str`
* `int`
* `float`
* `email`
* `datetime`
* `country`

---

# Project Architecture

```
csv_cleaner_toolkit
│
├── cli.py
├── ai_cli.py
│
├── toolkit/
│   ├── cleaner.py
│   ├── validator.py
│   ├── report_generator.py
│   └── openai_client.py
│
├── examples/
└── requirements.txt
```

### Core Components

**Cleaner**

Handles normalization and transformation of raw CSV data.

**Validator**

Applies schema rules and detects data integrity issues.

**Report Generator**

Produces structured summaries of validation results.

**OpenAI Client**

Handles communication with the language model for dataset explanations.

---

# Design Goals

This project focuses on demonstrating:

* modular Python architecture
* rule-driven data pipelines
* CLI tool design
* structured logging
* efficient LLM integration

The AI component is **optional** and used only for interpretation, ensuring the core data processing pipeline remains deterministic and reliable.

---

# Future Improvements

Potential enhancements include:

* strict validation mode
* dataset profiling statistics
* pip package distribution
* richer reporting formats
* interactive CLI commands

---

# Author

**Vlad George Cacenschi**
Python Backend & Automation Developer

---

# License

This project is intended for educational and portfolio purposes.
