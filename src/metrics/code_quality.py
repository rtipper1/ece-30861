"""
code_quality.py
-----------------
Code Quality Metric.

Summary:
- Performs static analysis on repository source code (e.g., Flake8).
- Scores maintainability and style consistency based on issues per 1,000 LOC.
- Runs independently of Hugging Face API, fulfilling non-API metric requirement.

- Input: path to a local clone/snapshot of the model repo
- Process: 
  1. Collect all .py files
  2. Count total lines of code
  3. Run Flake8, count style issues
  4. Compute issues per 1000 LOC
  5. Map to 0 - 1 score per rubric

Rubric:
- 0.2 = >60 issues per 1000 LOC
- 0.4 = 31–60 issues per 1000 LOC
- 0.6 = 16–30 issues per 1000 LOC
- 0.8 = 6–15 issues per 1000 LOC
- 1 = 0–5 issues per 1000 LOC
"""

'''


temp_dir = tempfile.TemporaryDirectory()
print(temp_dir.name)
# use temp_dir, and when done:
temp_dir.cleanup()
'''

import tempfile
import contextlib
import io
from typing import Dict, Optional

from flake8.api import legacy as flake8
from huggingface_hub import HfApi, hf_hub_download

from src.cli.url import CodeURL, ModelURL
from src.metrics.metric import Metric


class CodeQualityMetric(Metric):
    def __init__(self, code_url: CodeURL, model_url: ModelURL):
        super().__init__("code_quality")
        self.code_url = code_url
        self.model_url = model_url

    def get_data(self) -> Dict[str, Optional[int]]:
        temp_dir = tempfile.TemporaryDirectory()

        full_name = f"{self.model_url.author}/{self.model_url.name}"
        api = HfApi()
        info = api.model_info(full_name)

        fileList: list = []
        LoC = 0  # lines of code

        # Collect Python files
        for sib in info.siblings:
            if sib.rfilename.endswith(".py"):
                path = self.SingleFileDownload(full_name, sib.rfilename, temp_dir.name)
                fileList.append(path)
                with open(path, "r") as f:
                    LoC += len(f.readlines())

        # If no .py files, try the base model
        if not fileList and info.cardData:
            base_model = info.cardData.get("base_model")
            if base_model:
                full_name = base_model
                info = api.model_info(full_name)
                for sib in info.siblings:
                    if sib.rfilename.endswith(".py"):
                        path = self.SingleFileDownload(full_name, sib.rfilename, temp_dir.name)
                        fileList.append(path)
                        with open(path, "r") as f:
                            LoC += len(f.readlines())

        # Run flake8 silently
        if fileList:
            import os
            from flake8.api import legacy as flake8

            with open(os.devnull, "w") as devnull:
                style_guide = flake8.get_style_guide(
                    output_file=devnull,
                    quiet=2,
                    show_source=False,
                    statistics=False,
                )
                report = style_guide.check_files(fileList)
            errors = report.total_errors
        else:
            errors, LoC = -1, -1

        temp_dir.cleanup()
        return {"Issues": errors, "Lines of Code": LoC}





    def SingleFileDownload(self, full_name: str, filename: str, landingPath: str):
        # full_name = model_owner + "/" + model_name # Full model name
        model_path = hf_hub_download(
            repo_id=full_name, filename=filename, local_dir=landingPath)
        # print(f"File downloaded to: {model_path}")

        return model_path

    def calculate_score(self) -> float:
        if self.data["Issues"] == None or self.data["Lines of Code"] == None:
            return 0.0

        # Retrieve license from metric data
        issues = self.data["Issues"]
        loc = self.data["Lines of Code"]
        ratio = issues / loc
        # Score metric based on categories
        if ratio >= 0 and ratio <= .005:
            return 1

        elif ratio >= .006 and ratio <= .015:
            return 0.8

        elif ratio >= .016 and ratio < .03:
            return 0.6

        elif ratio >= .03 and ratio <= .06:
            return 0.4

        elif ratio > .06:
            return 0.2

        else:
            return 0.0
