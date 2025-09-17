# src/cli/main.py
from __future__ import annotations
import argparse
import os
from dataclasses import dataclass
from typing import Optional, Literal
import re

# Regex to capture Hugging Face URLs
HF_PATTERN = re.compile(r"^https?://huggingface\.co/([^/]+)/([^/]+)")

@dataclass
class CLIArgs:
    command: Literal['install', 'test', 'process']
    url_file: Optional[str]
    output: str
    parallelism: int 
    log_file: Optional[str]
    log_level: int
    author: Optional[str] = None
    model: Optional[str] = None

def parse_hf_url(url: str):
    """Extract (author, model) from a Hugging Face model URL."""
    m = HF_PATTERN.match(url)
    if not m:
        return None, None
    return m.group(1), m.group(2)

def parse_args(argv):
    parser = create_parser()
    ns = parser.parse_args(list(argv) if argv is not None else None)

    if ns.target == 'install':
        return CLIArgs('install', None, ns.output, ns.parallelism, ns.log_file, ns.log_level)
    if ns.target == 'test':
        return CLIArgs('test', None, ns.output, ns.parallelism, ns.log_file, ns.log_level)
    if ns.target is None:
        parser.error('Missing positional argument: install | test | /path/to/urls.txt')

    # Hugging Face URL case
    author, model = (None, None)
    if ns.target.startswith("http"):
        author, model = parse_hf_url(ns.target)
        if author is None:
            parser.error(f"Invalid Hugging Face URL: {ns.target}")
        print(f"HuggingFace Author: {author}, Model: {model}")

    return CLIArgs(
        'process',
        ns.target,
        ns.output,
        ns.parallelism,
        ns.log_file,
        ns.log_level,
        author,
        model,
    )
    
def create_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog='run')
    p.add_argument('target', nargs='?', help='install | test | /path/to/urls.txt | Hugging Face URL')
    p.add_argument('-o','--output', default='-', help='NDJSON output path ("-" = stdout)')
    p.add_argument('-p', '--parallelism', type=int, default=4, help='parallel workers')
    p.add_argument('--log-file', default=os.environ.get('LOG_FILE'))
    p.add_argument('--log-level', type=int, default=int(os.environ.get('LOG_LEVEL', '0')))
    return p

if __name__ == "__main__":
    import sys
    args = parse_args(sys.argv[1:])
    print(args)
