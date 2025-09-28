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
# from pathlib import Path
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

        # Full model name
        full_name = f"{self.model_url.author}/{self.model_url.name}"
        api = HfApi()
        info = api.model_info(full_name)
        style_guide = flake8.get_style_guide()
        fileList: list = []
        LoC = 0  # lines of code
        # info.siblings is a list of all files in the repo, each file is a RepoSibling
        sibs = info.siblings
        for sib in sibs:
            file = sib.rfilename
            if '.py' in file:
                # Repo Contains a pytohn file
                path = self.SingleFileDownload(
                    full_name=full_name, filename=file, landingPath=temp_dir.name)
                fileList.append(path)
                # Count number of lines in python file
                f = open(path, "r")
                length = len(f.readlines())
                LoC += length

        # If fileList is empty, check the base model for python files
        if fileList == []:
            base_model = info.cardData.get(
                'base_model') if info.cardData else None
            if base_model:
                print("FULL NAME: " + full_name)
                full_name = base_model
                info = api.model_info(full_name)  # Reset API endpoint
                # info.siblings is a list of all files in the repo, each file is a RepoSibling
                sibs = info.siblings
                for sib in sibs:
                    file = sib.rfilename
                    if '.py' in file:
                        # Repo Contains a pytohn file
                        path = self.SingleFileDownload(
                            full_name=full_name, filename=file, landingPath=temp_dir.name)
                        fileList.append(path)
                        # Count number of lines in python file
                        f = open(path, "r")
                        length = len(f.readlines())
                        LoC += length

        if fileList != []:
            report = style_guide.check_files([fileList])
            errors = report.total_errors
        else:
            errors = -1
            LoC = -1
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
