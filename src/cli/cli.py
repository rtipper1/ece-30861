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

def parse_url_file(path: str) -> list[list[Optional[URL]]]:
    """
    Parse a file of comma-separated links int URL dataclass
    
    input:
    <code_link_1>, <dataset_link_1>,<model_link_1>
    <code_link_2>, <dataset_link_2>,<model_link_2>
    ... and so on

    example:
    https://github.com/google-research/bert, https://huggingface.co/datasets/bookcorpus/bookcorpus, https://huggingface.co/google-bert/bert-base-uncased
    ,,https://huggingface.co/parvk11/audience_classifier_model
    ,,https://huggingface.co/openai/whisper-tiny/tree/main
    
    """
    url_lines = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = [p.strip() for p in line.split(",")]
            new_line = []

            for url in parts:
                if url == "":
                    new_line.append(None)
                else:
                    raw = url
                    url_type = classify_url(url)
                    if url_type == 'model':
                        author = get_model_url_author(url)
                        name = get_model_url_name(url)
                    else:
                        author = None
                        name = None

                    new_line.append(URL(raw, url_type, author, name))

            url_lines.append(new_line)
     
    return url_lines


def classify_url(url: str) -> Literal['model', 'code', 'dataset']:
    """Classify URL and return only its type: 'model' | 'code' | 'dataset'."""
    # CODE
    if url.startswith("https://github.com/") or url.startswith("https://gitlab.com/"):
        return 'code'
    if "/spaces/" in url:
        return 'code'

    # DATASET
    if "/datasets/" in url or "image-net.org" in url:
        return 'dataset'

    # MODEL (default Hugging Face URL)
    m = HF_PATTERN.match(url)
    if m:
        return 'model'

    # Fallback: treat as model by default if none matched
    return 'model'

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