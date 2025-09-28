import os
import sys
import logging
from github import Github, BadCredentialsException

def validate_github_token():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("ERROR: Missing GITHUB_TOKEN environment variable", file=sys.stderr)
        sys.exit(1)

    g = Github(token)
    try:
        g.get_user().id  # cheap check
    except BadCredentialsException:
        print("ERROR: Invalid GITHUB_TOKEN provided", file=sys.stderr)
        sys.exit(1)

    return g

