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
from src.cli.cli import parse_args, parse_url_file, CLIArgs

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
    assert args.url_type is None

def test_test_command(): 
    args = parse_args(['test'])
    assert args.command == "test"
    assert args.url_file is None
    assert args.url_type is None

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
    assert args.url_type is None  # file input does not classify a single URL

    entries = parse_url_file(str(url_file))
    assert len(entries) == 4

    # Check first line
    first = entries[0]
    assert first['code']['type'] == 'code'
    assert first['dataset']['type'] == 'dataset'
    assert first['dataset']['owner'] == 'dataset-owner'
    assert first['model']['type'] == 'model'
    assert first['model']['owner'] == 'owner'

    # Second line: missing code/dataset, only model
    second = entries[1]
    assert second['code'] is None
    assert second['dataset'] == {'type': 'dataset', 'owner': None, 'name': 'inferred'}
    assert second['model']['type'] == 'model'

    # Third line: GitLab code
    third = entries[2]
    assert third['code']['type'] == 'code'
    # previously: assert third['dataset'] is None
    assert third['dataset'] == {"type": "dataset", "owner": None, "name": "inferred"}

    # Fourth line: HF Spaces code only
    fourth = entries[3]
    assert fourth['code']['type'] == 'code'
    assert fourth['dataset'] == {"type": "dataset", "owner": None, "name": "inferred"}
    assert fourth['model'] is None

def test_file_empty_and_comments(tmp_path):
    url_file = tmp_path / "urls.txt"
    write_url_file(url_file, [
        "# comment line",
        "",
        " , , https://huggingface.co/owner/model-only"
    ])
    entries = parse_url_file(str(url_file))
    assert len(entries) == 1
    entry = entries[0]
    assert entry['model']['type'] == 'model'
    assert entry['code'] is None
    assert entry['dataset'] == {"type": "dataset", "owner": None, "name": "inferred"}

def test_file_unknown_url(tmp_path):
    url_file = tmp_path / "urls.txt"
    write_url_file(url_file, [
        "https://unknownsite.com/some/path, , "
    ])
    entries = parse_url_file(str(url_file))
    # classify_url returns type 'unknown' for unknown sites
    entry = entries[0]
    assert entry['code'] == {"type": "unknown", "owner": None, "name": None}
    assert entry['dataset'] == {"type": "dataset", "owner": None, "name": "inferred"}
    assert entry['model'] is None

def test_file_mixed_invalid_and_valid(tmp_path):
    url_file = tmp_path / "urls.txt"
    write_url_file(url_file, [
        "https://unknown.com/path, , https://huggingface.co/owner/model-valid"
    ])
    entries = parse_url_file(str(url_file))
    entry = entries[0]
    assert entry['code'] == {"type": "unknown", "owner": None, "name": None}
    assert entry['dataset'] == {"type": "dataset", "owner": None, "name": "inferred"}
    assert entry['model']['type'] == "model"

def test_hf_model_extra_path(tmp_path):
    url_file = tmp_path / "urls.txt"
    write_url_file(url_file, [
        " , , https://huggingface.co/owner/model/subdir"
    ])
    entries = parse_url_file(str(url_file))
    entry = entries[0]
    assert entry['model']['owner'] == "owner"
    assert entry['model']['name'] == "model"
