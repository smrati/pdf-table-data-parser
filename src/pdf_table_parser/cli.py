import argparse
import sys

from pdf_table_parser.extractor import extract_tables, to_flat, to_json


def main():
    parser = argparse.ArgumentParser(
        prog="pdf-table-parser",
        description="Extract tables from PDF files and output as JSON",
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("-o", "--output", help="Output JSON file path (default: stdout)")
    parser.add_argument(
        "-f",
        "--format",
        choices=["by-page", "flat"],
        default="by-page",
        help="Output format (default: by-page)",
    )
    parser.add_argument(
        "-p",
        "--pages",
        help="Pages to extract (e.g. 1,3,5-7). Default: all pages",
    )
    args = parser.parse_args()

    try:
        data = extract_tables(args.pdf_path, pages=args.pages)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.format == "flat":
        data = to_flat(data)

    output = to_json(data)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Output written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
