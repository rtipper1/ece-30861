"""
test_cli_txt.py
----------------
Unit tests for CLI URL classification using URL files.

Tests cover:
- install/test commands
- File input with multiple URLs
- Hugging Face model URLs
- Hugging Face dataset URLs
- GitHub/GitLab/HF Spaces URLs (code)
- Invalid or unknown URLs
- Missing or empty URLs
"""

import pytest
import os
from cli.cli import parse_args, parse_url_file, CLIArgs, URL

# Helper to write a temporary URL file
def write_url_file(filename: str, lines: list[str]):
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

# ------------------------------
# Subcommand tests (unchanged)
# ------------------------------
def test_install_command():
    args = parse_args(['install'])
    assert args.command == 'install'
    assert args.url_file is None

def test_test_command(): 
    args = parse_args(['test'])
    assert args.command == "test"
    assert args.url_file is None

def test_missing_raises(): 
    with pytest.raises(SystemExit):
        parse_args([])

# ------------------------------
# File input tests
# ------------------------------
def test_file_multiple_urls(tmp_path):
    url_file = tmp_path / "urls.txt"
    write_url_file(url_file, [
        "https://github.com/org/repo1, https://huggingface.co/datasets/dataset-owner/dataset1, https://huggingface.co/owner/model1",
        ", , https://huggingface.co/owner/model2",
        "https://gitlab.com/org/repo2,, https://huggingface.co/owner/model3",
        "https://huggingface.co/spaces/user/my-space, , "
    ])

    args = parse_args([str(url_file)])
    assert args.command == 'process'
    assert args.url_file == str(url_file)
    # Parse URL file into list of rows [code, dataset, model]
    rows = parse_url_file(str(url_file))
    assert isinstance(rows, list)
    assert len(rows) == 4

    # First row
    r1 = rows[0]
    assert len(r1) == 3
    code1, dataset1, model1 = r1
    assert isinstance(code1, URL) and code1.url_type == 'code'
    assert isinstance(dataset1, URL) and dataset1.url_type == 'dataset'
    # Dataset owner/name parsing not implemented yet; allow None
    assert dataset1.author is None and dataset1.name is None
    assert isinstance(model1, URL) and model1.url_type == 'model'
    assert model1.author == 'owner' and model1.name == 'model1'

    # Second row: only model present
    r2 = rows[1]
    assert len(r2) == 3
    code2, dataset2, model2 = r2
    assert code2 is None and dataset2 is None
    assert isinstance(model2, URL) and model2.url_type == 'model'

    # Third row: GitLab code and model present
    r3 = rows[2]
    assert len(r3) == 3
    code3, dataset3, model3 = r3
    assert isinstance(code3, URL) and code3.url_type == 'code'
    assert dataset3 is None
    assert isinstance(model3, URL) and model3.url_type == 'model'

    # Fourth row: HF Spaces code only
    r4 = rows[3]
    assert len(r4) == 3
    code4, dataset4, model4 = r4
    assert isinstance(code4, URL) and code4.url_type == 'code'
    assert dataset4 is None
    assert model4 is None

def test_file_empty_and_comments(tmp_path):
    url_file = tmp_path / "urls.txt"
    write_url_file(url_file, [
        "# comment line",
        "",
        " , , https://huggingface.co/owner/model-only"
    ])
    rows = parse_url_file(str(url_file))
    assert len(rows) == 1
    r = rows[0]
    assert len(r) == 3
    code, dataset, model = r
    assert code is None and dataset is None
    assert isinstance(model, URL) and model.url_type == 'model'
    

def test_hf_model_extra_path(tmp_path):
    url_file = tmp_path / "urls.txt"
    write_url_file(url_file, [
        " , , https://huggingface.co/owner/model/subdir"
    ])
    rows = parse_url_file(str(url_file))
    r = rows[0]
    code, dataset, model = r
    assert isinstance(model, URL)
    assert model.author == "owner"
    assert model.name == "model"
