"""
test_cli.py
---------------
Unit tests for CLI URL classification

Tests cover:
- install/test commands
- Hugging Face model URLs
- Hugging Face dataset URLs
- GitHub/GitLab/HF Spaces URLs (code)
- Invalid or unknown URLs
"""

import pytest
from src.cli.cli import parse_args, CLIArgs


# ------------------------------
# Subcommand tests
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
# URL classification tests
# ------------------------------
def test_hf_model_url():
    url = 'https://huggingface.co/google-bert/bert-base-uncased'
    args = parse_args([url])
    assert args.command == 'process'
    assert args.url_file == url
    assert args.url_type == 'model'
    assert args.owner == 'google-bert'
    assert args.name == 'bert-base-uncased'


def test_hf_dataset_url():
    url = 'https://huggingface.co/datasets/bookcorpus/bookcorpus'
    args = parse_args([url])
    assert args.command == 'process'
    assert args.url_file == url
    assert args.url_type == 'dataset'
    assert args.owner == 'bookcorpus'
    assert args.name == 'bookcorpus'


def test_github_code_url():
    url = 'https://github.com/google-research/bert'
    args = parse_args([url])
    assert args.command == 'process'
    assert args.url_file == url
    assert args.url_type == 'code'
    assert args.owner is None
    assert args.name is None


def test_gitlab_code_url():
    url = 'https://gitlab.com/example/project'
    args = parse_args([url])
    assert args.command == 'process'
    assert args.url_type == 'code'


def test_hf_spaces_code_url():
    url = 'https://huggingface.co/spaces/user/my-space'
    args = parse_args([url])
    assert args.url_type == 'code'


def test_unknown_url_raises():
    url = 'https://unknownsite.com/some/path'
    with pytest.raises(SystemExit):
        parse_args([url])


def test_image_net_dataset_url():
    url = 'https://www.image-net.org/'
    args = parse_args([url])
    assert args.url_type == 'dataset'
    assert args.name == 'imagenet'
