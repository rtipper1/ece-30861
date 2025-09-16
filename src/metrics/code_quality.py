"""
Code Quality Metric
===================
- Input: path to a local clone/snapshot of the model repo
- Process: 
  1. Collect all .py files
  2. Count total lines of code
  3. Run Flake8, count style issues
  4. Compute issues per 1000 LOC
  5. Map to 1–5 score per rubric

Rubric:
- 1 = >60 issues per 1000 LOC
- 2 = 31–60 issues per 1000 LOC
- 3 = 16–30 issues per 1000 LOC
- 4 = 6–15 issues per 1000 LOC
- 5 = 0–5 issues per 1000 LOC
"""

from pathlib import Path
from flake8.api import legacy as flake8
from huggingface_hub import HfApi

def code_quality_score(model_owner: str, model_name: str) -> int:
    repo = model_owner + "/" + model_name # contains full model name: owner/model_name
    py_files = [str(p) for p in repo.rglob("*.py") if p.is_file()]

    if not py_files:
        return 1  # no Python code, lowest score by default

    # count lines of code
    loc = 0
    for f in py_files:
        with open(f, encoding="utf-8", errors="ignore") as fh:
            loc += sum(1 for line in fh if line.strip())

    if loc == 0:
        return 1

    # run flake8
    style_guide = flake8.get_style_guide(ignore=["E501"])  # example: ignore long lines
    report = style_guide.check_files(py_files)
    issues = report.total_errors

    issues_per_1000 = issues / (loc / 1000)

    if issues_per_1000 > 60: return 1
    if issues_per_1000 > 30: return 2
    if issues_per_1000 > 15: return 3
    if issues_per_1000 > 5:  return 4
    return 5

# Main file for testing
if __name__ == "__main__":
    owner = "Atiqah"
    model = "Atiqah"
    score = code_quality_score(model_owner=owner, model_name=model)
    print('Score: ', score)
