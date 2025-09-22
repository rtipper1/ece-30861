"""
test_cli_parse_url_file.py
----------------------
Unit tests for parsing url file to format into URL dataclasses

Tests cover:
- 

"""

import pytest
from src.cli.cli import parse_url_file

def test_parse_url_file_example(tmp_path):
    url_file = tmp_path / "example.txt"
    url_file.write_text(
        "https://github.com/google-research/bert, https://huggingface.co/datasets/bookcorpus/bookcorpus, https://huggingface.co/google-bert/bert-base-uncased\n"
        ",,https://huggingface.co/parvk11/audience_classifier_model\n"
        ",,https://huggingface.co/openai/whisper-tiny/tree/main",
        encoding="utf-8",
    )

    lines = parse_url_file(str(url_file))

    # Expect three lines
    assert len(lines) == 3

    # Line 1
    l1 = lines[0]
    assert len(l1) == 3
    code1, dataset1, model1 = l1
    assert code1 is not None
    assert code1.url_type == 'code'
    assert code1.author is None and code1.name is None
    assert code1.raw == "https://github.com/google-research/bert"

    assert dataset1 is not None
    assert dataset1.url_type == 'dataset'
    # Current implementation does not parse dataset owner/name
    assert dataset1.author is None and dataset1.name is None
    assert dataset1.raw == "https://huggingface.co/datasets/bookcorpus/bookcorpus"

    assert model1 is not None
    assert model1.url_type == 'model'
    assert model1.author == 'google-bert'
    assert model1.name == 'bert-base-uncased'
    assert model1.raw == "https://huggingface.co/google-bert/bert-base-uncased"

    # Line 2
    l2 = lines[1]
    assert len(l2) == 3
    code2, dataset2, model2 = l2
    assert code2 is None
    assert dataset2 is None
    assert model2 is not None
    assert model2.url_type == 'model'
    assert model2.author == 'parvk11'
    assert model2.name == 'audience_classifier_model'
    assert model2.raw == "https://huggingface.co/parvk11/audience_classifier_model"

    # Line 3 (model URL with extra path)
    l3 = lines[2]
    assert len(l3) == 3
    code3, dataset3, model3 = l3
    assert code3 is None
    assert dataset3 is None
    assert model3 is not None
    assert model3.url_type == 'model'
    assert model3.author == 'openai'
    assert model3.name == 'whisper-tiny'
    assert model3.raw == "https://huggingface.co/openai/whisper-tiny/tree/main"

