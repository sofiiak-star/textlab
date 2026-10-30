# TextLab workshop starter

A small Python program for analyzing real documents and creating an offline
HTML report. Prepared for the NLTU workshop inspired by CodeRefinery.

## Create your own copy

On GitHub, select **Use this template > Create a new repository**. Choose your
account as the owner, create the repository, then clone your copy and open its
folder in VS Code.

The template includes Python code, tests, real input documents and complete
Sphinx documentation sources (`docs/*.md`, `docs/api.rst`, `docs/conf.py`).
Generated JSON results and HTML files are deliberately absent. Run the commands
below to see `results/`, `report/` and `docs/_build/` appear.

## Requirements

Python 3.11 or newer. Core analysis uses only the standard library.
Tested interpreter and dependency versions are recorded in `VERIFICATION.md`.

## Windows / PowerShell

Create the environment once; if `.venv` already exists, skip the first command.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt -r requirements-docs.txt
python -m pytest -v
```

Generate analysis results, then combine them into a report:

```powershell
python analyze.py documents/flask.md --output results/flask.json
python analyze.py documents/click.md --output results/click.json
python analyze.py documents/jinja.md --output results/jinja.json
python report.py --input results --output report/index.html
Start-Process .\report\index.html
```

Build the documentation separately:

```powershell
python -m sphinx -b html docs docs/_build/html
Start-Process .\docs\_build\html\index.html
```

Rebuilding documentation does not rerun the analysis. After changing source
files, rerun the relevant command and refresh your browser. For a strict check
that rereads documentation and fails on warnings, run
`python -m sphinx -E -b html -W docs docs/_build/html`.

## Windows / Git Bash

```bash
py -3.13 -m venv .venv
source .venv/Scripts/activate
python --version
python -m pip install -r requirements-dev.txt -r requirements-docs.txt
python analyze.py documents/flask.md --output results/flask.json
python analyze.py documents/click.md --output results/click.json
python analyze.py documents/jinja.md --output results/jinja.json
python report.py --input results --output report/index.html
python -m pytest -v
python -m sphinx -b html -W --keep-going docs docs/_build/html
```

On macOS/Linux create the environment with `python3 -m venv .venv` and activate
with `source .venv/bin/activate`. For PowerShell without activation, replace
`python` with `.\.venv\Scripts\python.exe` after creating the environment.

Open `report/index.html` for results and `docs/_build/html/index.html` for docs.
The environment may already exist in the prepared local copy; activate it.

## Files

| Path | Purpose |
| --- | --- |
| `documents/` | Real upstream README snapshots; no synthetic dataset |
| `analysis.py` | Word extraction, counting, file reading |
| `analyze.py` | Command-line arguments and JSON output |
| `report.py` | Combining JSON records into an offline HTML report |
| `tests/` | Unicode, validation, deterministic results, CLI and report tests |
| `docs/` | Editable Sphinx documentation sources |
| `requirements.txt` | Explicitly documents zero runtime dependencies |
| `requirements-dev.txt` | Test dependency |
| `requirements-docs.txt` | Documentation dependencies |
| `requirements-validated.txt` | Full installed dependency snapshot from local verification |
| `sources.json` | Upstream commit IDs, checksums and retrieval timestamps |
| `third_party/` | Original licenses of the input documents |
| `next_steps/` | Inactive examples for Pages and Docker; see its README |
| `results/`, `report/`, `docs/_build/` | Generated, ignored outputs |

## Scope

The program counts raw Markdown tokens, including words from links and code.
It is not a language model, a Markdown renderer or a document-quality score.
See the Method page for exact rules. All JSON files in the chosen results
directory are included; use a fresh directory when switching datasets.

The ready documentation is a worked example. Start by changing one paragraph
in `docs/quickstart.md`, then a docstring in `analysis.py`, and rebuild each time.
You do not need to run `sphinx-quickstart` over this existing setup.

## Attribution

See `sources.json` and `third_party/` for Pallets README attribution.
Workshop code is MIT licensed; input documents keep their original licenses.
Inspired by https://coderefinery.github.io/reproducible-research/workflow-management/.
