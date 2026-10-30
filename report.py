"""Build an offline HTML report from TextLab JSON records."""

import argparse
import json
from html import escape
from pathlib import Path


def render_report(records: list[dict]) -> str:
    """Render statistics as an HTML table and per-document bar charts.

    Input must follow the schema produced by analyze_file. All textual
    values are escaped. Word totals include duplicates between documents.

    :param records: Analysis records in the desired display order.
    :returns: A complete, self-contained HTML page.
    """
    total = sum(record["total_words"] for record in records)
    rows = []
    cards = []
    for record in records:
        name = escape(record["source"])
        rows.append(
            f"<tr><td>{name}</td><td>{record['total_words']}</td>"
            f"<td>{record['unique_words']}</td></tr>"
        )
        maximum = max((item["count"] for item in record["top_words"]), default=1)
        bars = []
        for item in record["top_words"]:
            width = item["count"] / maximum * 100
            word = escape(item["word"])
            bars.append(
                f'<li><span>{word}</span><div class="track">'
                f'<div class="bar" style="width:{width:.2f}%"></div></div>'
                f'<strong>{item["count"]}</strong></li>'
            )
        chart = "<ul>" + "".join(bars) + "</ul>" if bars else "<p>No words found.</p>"
        cards.append(f"<section><h2>{name}</h2>{chart}</section>")
    return """<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>TextLab — document report</title><style>
body{font:17px/1.6 system-ui,sans-serif;color:#153b45;background:#f2f5f3;margin:0}
main{max-width:1050px;margin:auto;padding:40px 24px}h1{font-size:42px;margin:0}
.lead{color:#4d666c}table{width:100%;border-collapse:collapse;background:white}
th,td{text-align:left;padding:12px;border-bottom:1px solid #dae4df}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:24px}
section{background:white;border:1px solid #dae4df;border-radius:12px;padding:18px}
h2{font-size:21px}ul{list-style:none;padding:0}li{display:grid;grid-template-columns:90px 1fr 30px;gap:8px;align-items:center;margin:9px 0}
li span{overflow-wrap:anywhere}.track{background:#edf2ef;border-radius:4px}.bar{height:13px;background:#16806c;border-radius:4px}
.note{font-size:14px;color:#4d666c;margin-top:24px}
</style><main><p>TEXTLAB / REPRODUCIBLE ANALYSIS</p><h1>What is in these documents?</h1>
""" + f"""<p class="lead">{len(records)} documents · {total} total word occurrences</p>
<table><thead><tr><th>Document</th><th>Words</th><th>Unique words</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table><div class="cards">{''.join(cards)}</div>
<p class="note">Raw Markdown analysis: links and code are included. Common words are not excluded.
Bars use a separate scale for each document. Frequency is not a measure of document quality.</p>
</main></html>"""


def write_report(input_dir: Path, output: Path) -> int:
    """Load all JSON files in a directory and write an HTML report.

    :param input_dir: Directory containing TextLab JSON files only.
    :param output: Destination HTML file.
    :returns: Number of documents included.
    :raises ValueError: If no JSON files exist or a schema version is unknown.
    """
    files = sorted(input_dir.glob("*.json"))
    if not files:
        raise ValueError(f"No JSON results found in {input_dir}; run analyze.py first")
    records = [json.loads(path.read_text(encoding="utf-8")) for path in files]
    if any(record.get("schema_version") != 1 for record in records):
        raise ValueError("Unsupported analysis schema; regenerate results with analyze.py")
    html = render_report(records)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    return len(records)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an HTML report from TextLab JSON files.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        count = write_report(args.input, args.output)
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"Report failed: {error}\n")
    print(f"Report: {count} documents -> {args.output}")


if __name__ == "__main__":
    main()
