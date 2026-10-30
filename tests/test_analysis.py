"""Tests for the documented text-analysis contract."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from analysis import analyze_file, analyze_text, tokenize
from report import render_report, write_report

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("text, expected", [
    ("Git git PYTHON", ["git", "git", "python"]),
    ("Код, ТЕСТИ! п’ять п'ять", ["код", "тести", "п'ять", "п'ять"]),
    ("123 hello_world", ["hello", "world"]),
    ("", []),
])
def test_tokenize(text, expected):
    assert tokenize(text) == expected


def test_counts_and_alphabetical_tie_break():
    result = analyze_text("zebra apple zebra apple pear", top=2)
    assert result == {"total_words": 5, "unique_words": 3,
                      "top_words": [{"word": "apple", "count": 2},
                                    {"word": "zebra", "count": 2}]}


@pytest.mark.parametrize("top", [0, -1, True, 1.5])
def test_invalid_top(top):
    with pytest.raises(ValueError, match="positive integer"):
        analyze_text("hello", top)


def test_empty_text():
    assert analyze_text("") == {"total_words": 0, "unique_words": 0, "top_words": []}


def test_unicode_file_with_bom(tmp_path):
    path = tmp_path / "notes.md"
    path.write_text("Код код", encoding="utf-8-sig")
    assert analyze_file(path)["total_words"] == 2


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        analyze_file(tmp_path / "missing.md")


def test_html_escapes_document_name():
    record = {"source": "<script>alert(1)</script>", **analyze_text("hello")}
    html = render_report([record])
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_no_results(tmp_path):
    with pytest.raises(ValueError, match="No JSON results"):
        write_report(tmp_path, tmp_path / "index.html")


def test_unsupported_schema(tmp_path):
    (tmp_path / "bad.json").write_text('{"schema_version": 99}', encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported"):
        write_report(tmp_path, tmp_path / "index.html")


def test_cli_round_trip_and_determinism(tmp_path):
    source = tmp_path / "notes.md"
    source.write_text("Тести тести код", encoding="utf-8")
    result = tmp_path / "results" / "notes.json"
    command = [sys.executable, str(ROOT / "analyze.py"), str(source), "--output", str(result)]
    subprocess.run(command, check=True, capture_output=True)
    first = result.read_bytes()
    subprocess.run(command, check=True, capture_output=True)
    assert result.read_bytes() == first
    assert json.loads(first)["total_words"] == 3
    output = tmp_path / "report" / "index.html"
    subprocess.run([sys.executable, str(ROOT / "report.py"), "--input", str(result.parent),
                    "--output", str(output)], check=True, capture_output=True)
    assert "1 documents" in output.read_text(encoding="utf-8")


def test_cli_missing_file_fails_without_output(tmp_path):
    output = tmp_path / "result.json"
    run = subprocess.run([sys.executable, str(ROOT / "analyze.py"), str(tmp_path / "absent.md"),
                          "--output", str(output)], capture_output=True)
    assert run.returncode == 1
    assert b"Analysis failed" in run.stderr
    assert not output.exists()
