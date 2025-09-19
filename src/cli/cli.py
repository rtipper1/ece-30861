"""
cli.py
--------
Command-line interface definition and argument parsing.

Summary
- Defines subcommands: install, test, runfile.
- Parses CLI arguments and forwards execution to main entrypoints.
- Ensures compliance with the auto-grader interface specified in project requirements.

Requirements
- Validates URL, if invalid exit
- Parses URL into model owner and model name
- Parses URL by type (model, code, dataset) NOTE: code and dataset are not used until phase 2

Output format could look something like this

https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Thinking

 dict = {
	"type": "model",
	"owner": "Qwen",
	"name": "Qwen3-Next-80B-A3B-Thinking"
}
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
class CLIArgs:
    command: Literal['install', 'test', 'process']
    url_file: Optional[str]
    output: str
    parallelism: int
    log_file: Optional[str]
    log_level: int
    url_type: Optional[Literal['model', 'code', 'dataset']] = None
    owner: Optional[str] = None
    name: Optional[str] = None


def parse_hf_url(url: str):
    """Extract (author, model) from a Hugging Face model URL."""
    m = HF_PATTERN.match(url)
    if not m:
        return None, None
    return m.group(1), m.group(2)
def classify_url(url: str) -> dict[str, str | None]:
    """Classify URL into type: model, code, or dataset."""
    # CODE
    if url.startswith("https://github.com/") or url.startswith("https://gitlab.com/"):
        return {"type": "code", "owner": None, "name": None}
    if "/spaces/" in url:
        return {"type": "code", "owner": None, "name": None}

    # DATASET
    if "/datasets/" in url:
        parts = url.split("/datasets/")[-1].split("/")
        if len(parts) >= 2:
            return {"type": "dataset", "owner": parts[0], "name": parts[1]}
        return {"type": "dataset", "owner": None, "name": None}
    if "image-net.org" in url:
        return {"type": "dataset", "owner": None, "name": "imagenet"}

    # MODEL (default Hugging Face URL)
    m = HF_PATTERN.match(url)
    if m:
        return {"type": "model", "owner": m.group(1), "name": m.group(2)}

    return {"type": "unknown", "owner": None, "name": None}

def parse_args(argv) -> CLIArgs:
    parser = create_parser()
    ns = parser.parse_args(list(argv) if argv is not None else None)

    # Subcommands
    if ns.target == 'install':
        return CLIArgs('install', None, ns.output, ns.parallelism, ns.log_file, ns.log_level)
    if ns.target == 'test':
        return CLIArgs('test', None, ns.output, ns.parallelism, ns.log_file, ns.log_level)
    if ns.target is None:
        parser.error('Missing positional argument: install | test | /path/to/urls.txt | Hugging Face URL')

    # Process URLs
    url_type, owner, name = None, None, None
    if ns.target.startswith("http"):
        classification = classify_url(ns.target)
        url_type, owner, name = classification["type"], classification["owner"], classification["name"]
        if url_type == "unknown":
            parser.error(f"Invalid or unsupported URL: {ns.target}")
        print(f"Classified URL: type={url_type}, owner={owner}, name={name}")

    return CLIArgs(
        'process',
        ns.target,
        ns.output,
        ns.parallelism,
        ns.log_file,
        ns.log_level,
        url_type,
        owner,
        name,
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
