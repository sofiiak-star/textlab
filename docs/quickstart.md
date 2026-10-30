# Quickstart

Use Python 3.11 or newer. The analyzer needs no third-party packages.
Run commands from the repository root.

```bash
python analyze.py documents/flask.md --output results/flask.json
python analyze.py documents/click.md --output results/click.json
python analyze.py documents/jinja.md --output results/jinja.json
python report.py --input results --output report/index.html
```

Open `report/index.html` in your browser. The report has no network dependencies.

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

## Build this documentation

```bash
python -m pip install -r requirements-docs.txt
python -m sphinx -b html -W --keep-going docs docs/_build/html
```

Open `docs/_build/html/index.html` in your browser. Edit sources in `docs/`,
not generated HTML. The next build replaces generated pages.
