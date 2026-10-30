"""Command-line entry point for analyzing one document."""

import argparse
import json
from pathlib import Path

from analysis import analyze_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze one UTF-8 document.")
    parser.add_argument("document", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()
    try:
        result = analyze_file(args.document, args.top)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except (OSError, UnicodeError, ValueError) as error:
        parser.exit(1, f"Analysis failed: {error}\n")
    print(f"{result['source']}: {result['total_words']} words -> {args.output}")


if __name__ == "__main__":
    main()
