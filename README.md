# pdf-table-data-parser

A Python package that extracts tables from PDF files and outputs them as structured JSON. Handles multi-page PDFs with multiple tables per page.

## Installation

```bash
# Clone and install locally
git clone https://github.com/smrati/pdf-table-data-parser.git
cd pdf-table-data-parser
uv sync

# Or add as a dependency to your project (if published)
uv add pdf-table-data-parser

# Or install directly from a git URL
uv add git+https://github.com/smrati/pdf-table-data-parser.git
```

## Quick Start

### CLI Usage

```bash
# Extract all tables, print JSON to stdout
pdf-table-parser report.pdf

# Save output to a file
pdf-table-parser report.pdf -o tables.json

# Flat format (all tables in a single list)
pdf-table-parser report.pdf -f flat -o tables.json

# Extract tables from specific pages only
pdf-table-parser report.pdf -p 1,3,5-7

# Combine options
pdf-table-parser report.pdf -p 1-3 -f flat -o output.json
```

#### CLI Options

| Flag | Description |
|------|-------------|
| `pdf_path` | Path to the PDF file (required) |
| `-o, --output` | Output JSON file path (default: stdout) |
| `-f, --format` | `by-page` (default) or `flat` |
| `-p, --pages` | Pages to extract, e.g. `1,3,5-7` (default: all) |

### Python API

```python
from pdf_table_parser import extract_tables, to_flat, to_json

# Extract tables (returns a dict)
data = extract_tables("report.pdf")

# Convert to JSON string
json_str = to_json(data)
print(json_str)

# Get flat format instead
flat_data = to_flat(data)

# Extract from specific pages only
data = extract_tables("report.pdf", pages="1,3,5-7")
```

## Output Formats

### by-page (default)

```json
{
  "source": "report.pdf",
  "total_pages": 3,
  "pages": [
    {
      "page_number": 1,
      "tables": [
        {
          "headers": ["Name", "Age", "City"],
          "rows": [
            ["Alice", "30", "NYC"],
            ["Bob", "25", "LA"]
          ]
        }
      ]
    }
  ]
}
```

### flat

```json
{
  "source": "report.pdf",
  "total_pages": 3,
  "tables": [
    {
      "page_number": 1,
      "table_index": 0,
      "headers": ["Name", "Age", "City"],
      "rows": [["Alice", "30", "NYC"], ["Bob", "25", "LA"]]
    }
  ]
}
```

## Architecture

```
src/pdf_table_parser/
├── __init__.py      # Public API exports
├── extractor.py     # Core extraction logic using pdfplumber
└── cli.py           # CLI entry point (argparse)
```

- **extractor.py** — Opens the PDF with `pdfplumber`, iterates pages, calls `page.extract_tables()` on each, treats the first row as headers, and builds the structured output. Exposes `extract_tables()`, `to_flat()`, and `to_json()`.
- **cli.py** — Thin wrapper over the extractor. Parses CLI args and writes to file or stdout.
- **pdfplumber** — Handles the heavy lifting of detecting table boundaries, merged cells, and row/column structure from PDF page content.

## Requirements

- Python >= 3.13
- pdfplumber >= 0.11