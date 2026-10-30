"""Sphinx configuration for the TextLab workshop."""

import sys
from pathlib import Path

# Import analysis.py and report.py without installing a Python package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

project = "TextLab"
author = "TextLab workshop contributors"
release = "0.1.0"
extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx.ext.viewcode"]
exclude_patterns = ["_build"]
html_theme = "alabaster"
html_title = "TextLab — reproducible document analysis"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_theme_options = {"description": "From real documents to a repeatable report"}
