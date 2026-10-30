# Examples

## Show fewer frequent words

```bash
python analyze.py documents/flask.md --top 5 --output results/flask.json
python report.py --input results --output report/index.html
```

`--top` changes the displayed vocabulary, not the total word count.

## Analyze your own document

Save a UTF-8 file as `documents/my-notes.md`, then run:

```bash
python analyze.py documents/my-notes.md --output results/my-notes.json
python report.py --input results --output report/index.html
```

Use your own text or text that you have permission to redistribute.
Do not edit the supplied source snapshots during the first exercise: that would
invalidate their recorded checksums. Copy a snapshot first if you want to edit it.

## Read the command help

```bash
python analyze.py --help
python report.py --help
```

## Controlled failure

```bash
python analyze.py documents/flask.md --top 0 --output results/flask.json
```

Expected: an error and exit code 1. The existing output is not replaced.
Correct the argument and rerun before interpreting an older report as current.
