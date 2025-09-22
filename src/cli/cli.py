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

def parse_url_file(path: str) -> list[dict[str, str | None]]:
    """Parse a file of comma-separated links into structured dicts.

    Each line: code_link, dataset_link, model_link
    """
    results = []
    seen_datasets = set()

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = [p.strip() for p in line.split(",")]
            # pad missing fields so we always have 3
            while len(parts) < 3:
                parts.append("")

            code_url, dataset_url, model_url = parts

            entry = {
                "code": classify_url(code_url) if code_url else None,
                "dataset": None,
                "model": None,
            }

            # Dataset handling
            if dataset_url:
                d = classify_url(dataset_url)
                entry["dataset"] = d if d["type"] != "unknown" else None
                if entry["dataset"]:
                    seen_datasets.add((d["owner"], d["name"]))
            else:
                entry["dataset"] = None
                
            if model_url:
                m = classify_url(model_url)
                entry["model"] = m
            if not entry["dataset"]:
                entry["dataset"] = {"type": "dataset", "owner": None, "name": "inferred"}

            results.append(entry)

    return results


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
        parser.error('Missing positional argument: install | test | URL_FILE')
        
    if os.path.isfile(ns.target):
        url_entries = parse_url_file(ns.target)
        return CLIArgs(
            'process',
            ns.target,
            ns.output,
            ns.parallelism,
            ns.log_file,
            ns.log_level,
            None, None, None
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