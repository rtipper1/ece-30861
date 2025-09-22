"""
cli.py
--------
Command-line interface definition and argument parsing.

Summary
- Defines subcommands: install, test, process (via URL file).
- Parses CLI arguments and forwards execution to main entrypoints.
- Complies with the spec: only URL files are accepted for processing.

Spec alignment
- Invocation form: ./run URL_FILE
- URL_FILE is an ASCII-encoded, newline-delimited set of URLs (our helper also
  supports CSV rows with code,dataset,model as used by tests).
- Direct single-URL inputs on the command line are not supported; users must
  place URLs in a file.

NOTES: Needs to be updated to handle invalid URLS, i.e. URLS in which classify URL does not catch as model, code, or dataset
"""

from __future__ import annotations
import argparse
import os
from dataclasses import dataclass
from typing import Optional, Literal
import re

# Regex to capture Hugging Face URLs
HF_PATTERN = re.compile(r"^https?://huggingface\.co/([^/]+)/([^/]+)")

@dataclass
class URL:
    raw: str
    url_type: Literal['model', 'dataset', 'code']
    author: Optional[str]
    name: Optional[str]


@dataclass
class CLIArgs:
    command: Literal['install', 'test', 'process']
    url_file: Optional[str]
    output: str
    parallelism: int
    log_file: Optional[str]
    log_level: int


def parse_url_file(path: str) -> list[list[Optional[URL]]]:
    """
    Parse a file of comma-separated links into URL dataclasses.

    Input format (CSV-style):
        <code_link>, <dataset_link>, <model_link>

    Note: URL type can be inferred from its position per spec
    
    Example:
        https://github.com/google-research/bert, https://huggingface.co/datasets/bookcorpus/bookcorpus, https://huggingface.co/google-bert/bert-base-uncased
        ,,https://huggingface.co/parvk11/audience_classifier_model
        ,,https://huggingface.co/openai/whisper-tiny/tree/main
    """
    url_lines: list[list[Optional[URL]]] = []

    # fixed mapping of column -> type
    url_types = {0: "code", 1: "dataset", 2: "model"}

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = [p.strip() for p in line.split(",")]
            new_line: list[Optional[URL]] = []

            for idx, url in enumerate(parts):
                if not url:
                    new_line.append(None)
                    continue

                url_type = url_types.get(idx, "model")
                author = name = None

                if url_type == "model":
                    author = get_model_url_author(url)
                    name = get_model_url_name(url)

                new_line.append(URL(url, url_type, author, name))

            url_lines.append(new_line)

    return url_lines


def parse_args(argv) -> CLIArgs:
    parser = create_parser()
    ns = parser.parse_args(list(argv) if argv is not None else None)

    # Subcommands
    if ns.target == 'install':
        return CLIArgs('install', None, ns.output, ns.parallelism, ns.log_file, ns.log_level)
    if ns.target == 'test':
        return CLIArgs('test', None, ns.output, ns.parallelism, ns.log_file, ns.log_level)
    if ns.target is None:
        parser.error('Missing positional argument: install | test | URL_FILE')
        
    if os.path.isfile(ns.target):
        return CLIArgs(
            'process',
            ns.target,
            ns.output,
            ns.parallelism,
            ns.log_file,
            ns.log_level,
        )

    # Any other target is invalid per spec (must be a file)
    parser.error('Target must be a path to a URL file. Direct URLs are not supported. Use: ./run URL_FILE')
    
def create_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='run')
    p.add_argument('target', nargs='?', help='install | test | URL_FILE')
    p.add_argument('-o','--output', default='-', help='NDJSON output path ("-" = stdout)')
    p.add_argument('-p', '--parallelism', type=int, default=4, help='parallel workers')
    p.add_argument('--log-file', default=os.environ.get('LOG_FILE'))
    p.add_argument('--log-level', type=int, default=int(os.environ.get('LOG_LEVEL', '0')))
    return p


def get_model_url_author(url: str):
    """Extract (author, model) from a Hugging Face model URL."""
    m = HF_PATTERN.match(url)
    if not m:
        return None, None
    return m.group(1)

def get_model_url_name(url: str):
    """Extract (name) from a Hugging Face model URL."""
    m = HF_PATTERN.match(url)
    if not m:
        return None, None
    return m.group(2)