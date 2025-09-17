"""
test_metric.py
---------------
Basic unit tests for CLI Parser

Tests cover:
- idk
"""

import pytest
from cli.cli import parse_args


def test_initial_command():
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
