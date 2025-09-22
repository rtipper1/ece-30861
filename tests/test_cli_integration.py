"""
test_cli_integration.py
------------------------
End-to-end CLI tests focused on file-based inputs as required by the spec.

Covers:
- Parsing a URL file with multiple rows (code, dataset, model columns)
- Handling missing code/dataset columns and dataset inference
- Hugging Face model URL parsing with extra path segments (e.g., /tree/main)
- Rejecting direct URL targets (non-file) per spec
"""

import pytest
from cli.cli import parse_args, parse_url_file

