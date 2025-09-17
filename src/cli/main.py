"""
main.py
---------
Top-level program dispatcher.

Summary
- Entry point invoked by the ./run script.
- Loads URL input (file or inline).
- Delegates handling to the URL factory and model handler.
- Orchestrates metric execution and output generation.
"""

from cli import parse_args
import sys

if __name__ == "__main__":

    args = parse_args(sys.argv[1:])
    print(args)
