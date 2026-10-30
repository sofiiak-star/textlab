# Local verification

Verified on Windows on 2026-10-27 using Python 3.13.0.

- `python -m pytest -v`: 17 passed.
- `python -m pip check`: no broken requirements.
- Sphinx 8.2.3 and MyST 5.0.0: strict HTML build succeeded without warnings.
- Analysis: Flask 234 words, Click 251, Jinja 265; total 750.
- HTML report generated successfully from all three JSON records.
- Five expected function entries exist in the generated API documentation.
- Three upstream document SHA-256 hashes match `sources.json`.
- Corresponding upstream BSD-3-Clause license texts are included.
- 268 relative HTML link targets checked across the walkthrough, report and docs.
- Pages sample YAML parsed; trigger, dependency and permission structure checked.
- `requirements-validated.txt` records the complete installed package snapshot.
  The shorter requirements files pin direct dependencies; transitive versions
  can otherwise change. The snapshot is a record of this environment, not proof
  of testing on all operating systems.

Not performed: GitHub repository creation, push, hosted Actions runs, Pages
deployment, container build/run, release, DOI registration or Snakemake execution.
Docker CLI 29.5.3-rd is installed, but the default Docker Engine named pipe was
unavailable during the check. Docker examples are prepared, not runtime-verified.

The Ukrainian walkthrough is stored alongside the local repository as
`../TextLab_walkthrough_UA.html`. It is not part of the source distribution.
