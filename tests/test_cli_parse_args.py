"""
test_cli_parse_args.py
----------------------
Unit tests for CLI parse_args function

Tests cover:
- install/test/url_file targets
- CLIArgs dataclass output

Note: Update to test output, log, and parallelism once those are implemented
"""

import pytest
from src.cli.cli import parse_args

def test_install():
    args = parse_args(['install'])
    assert args.command == 'install'
    

def test_test():
    args = parse_args(['test'])
    assert args.command == 'test'


def test_url_file_dne(capsys):
    # Non-existent file should trigger parser.error and exit status 2
    with pytest.raises(SystemExit) as excinfo:
        parse_args(['dne.txt'])
    assert excinfo.value.code == 2
    err = capsys.readouterr().err
    assert 'Target must be a path to a URL file' in err


def test_url_file_exists(tmp_path):
    url_file = tmp_path / "exists.txt"
    url_file.write_text(
        "https://github.com/org/repo, , https://huggingface.co/owner/model\n",
        encoding="utf-8"
    )
    args = parse_args([str(url_file)])
    assert args.command == 'process'
    assert args.url_file == str(url_file)


def test_missing_positional_argument(capsys):
    # No args should trigger the specific missing positional argument error
    with pytest.raises(SystemExit) as excinfo:
        parse_args([])
    assert excinfo.value.code == 2
    err = capsys.readouterr().err
    assert 'Missing positional argument: install | test | URL_FILE' in err
