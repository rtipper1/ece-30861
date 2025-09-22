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


def write_url_file(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def test_cli_processes_url_file_end_to_end(tmp_path):
    # Input file lines in the requested format (code, dataset, model)
    lines = [
        "https://github.com/google-research/bert, https://huggingface.co/datasets/bookcorpus/bookcorpus, https://huggingface.co/google-bert/bert-base-uncased",
        ",,https://huggingface.co/parvk11/audience_classifier_model",
        ",,https://huggingface.co/openai/whisper-tiny/tree/main",
    ]

    url_file = tmp_path / "urls.txt"
    write_url_file(url_file, lines)

    # Parse args using the file path → should select 'process' mode and set url_file
    args = parse_args([str(url_file)])
    assert args.command == "process"
    assert args.url_file == str(url_file)
    # File-based flow does not classify a single URL
    assert args.url_type is None and args.owner is None and args.name is None

    # Parse the URL file into structured entries
    entries = parse_url_file(str(url_file))
    assert len(entries) == 3

    # 1) GitHub code, HF dataset, HF model
    first = entries[0]
    assert first["code"]["type"] == "code"
    assert first["dataset"]["type"] == "dataset"
    assert first["dataset"]["owner"] == "bookcorpus"
    assert first["dataset"]["name"] == "bookcorpus"
    assert first["model"]["type"] == "model"
    assert first["model"]["owner"] == "google-bert"
    assert first["model"]["name"] == "bert-base-uncased"

    # 2) No code/dataset, only HF model
    second = entries[1]
    assert second["code"] is None
    assert second["dataset"] == {"type": "dataset", "owner": None, "name": "inferred"}
    assert second["model"]["type"] == "model"
    assert second["model"]["owner"] == "parvk11"
    assert second["model"]["name"] == "audience_classifier_model"

    # 3) HF model with extra path (/tree/main) still parses owner/name
    third = entries[2]
    assert third["code"] is None
    assert third["dataset"] == {"type": "dataset", "owner": None, "name": "inferred"}
    assert third["model"]["type"] == "model"
    assert third["model"]["owner"] == "openai"
    assert third["model"]["name"] == "whisper-tiny"


def test_cli_rejects_direct_url_target():
    # Passing a direct URL (not a file) must error per spec
    with pytest.raises(SystemExit):
        parse_args(["https://huggingface.co/openai/whisper-tiny"]) 
