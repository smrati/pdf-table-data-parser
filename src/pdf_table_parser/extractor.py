import json
from pathlib import Path

import pdfplumber


def extract_tables(pdf_path: str, pages: str | None = None) -> dict:
    """Extract all tables from a PDF file.

    Args:
        pdf_path: Path to the PDF file.
        pages: Optional page filter (e.g. "1,3,5-7"). 1-indexed.

    Returns:
        Dict with extracted table data.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    page_numbers = _parse_pages(pages)

    with pdfplumber.open(pdf_path) as pdf:
        result_pages = []
        for i, page in enumerate(pdf.pages, start=1):
            if page_numbers is not None and i not in page_numbers:
                continue
            tables = page.extract_tables()
            page_data = {"page_number": i, "tables": []}
            for raw_table in tables:
                if not raw_table:
                    continue
                cleaned = [
                    [cell.strip() if cell else "" for cell in row]
                    for row in raw_table
                    if any(cell for cell in row)
                ]
                if not cleaned:
                    continue
                if len(cleaned) == 1:
                    # Single-row table: treat as a key-value row, no header
                    page_data["tables"].append({
                        "headers": [],
                        "rows": cleaned,
                    })
                else:
                    headers = cleaned[0]
                    rows = cleaned[1:]
                    page_data["tables"].append({"headers": headers, "rows": rows})
            result_pages.append(page_data)

        return {
            "source": pdf_path.name,
            "total_pages": len(pdf.pages),
            "pages": result_pages,
        }


def to_flat(data: dict) -> dict:
    """Convert by-page output to a flat list of tables."""
    tables = []
    for page in data["pages"]:
        for idx, table in enumerate(page["tables"]):
            tables.append({
                "page_number": page["page_number"],
                "table_index": idx,
                "headers": table["headers"],
                "rows": table["rows"],
            })
    return {"source": data["source"], "total_pages": data["total_pages"], "tables": tables}


def to_json(data: dict, indent: int = 2) -> str:
    """Convert extracted data to a JSON string."""
    return json.dumps(data, indent=indent, ensure_ascii=False)


def _parse_pages(pages: str | None) -> set[int] | None:
    """Parse a page range string like '1,3,5-7' into a set of 1-indexed page numbers."""
    if pages is None:
        return None
    result = set()
    for part in pages.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            result.update(range(int(start), int(end) + 1))
        else:
            result.add(int(part))
    return result
