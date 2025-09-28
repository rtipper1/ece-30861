"""
bus_factor.py
---------------
Bus Factor Metric.

Summary
- Calculates contributor redundancy relative to project size.
- Uses number of contributors per parameter scale as described in the rubric.
- Gets number of paramenters from model_info.safetensors
- Gets contributors from github status json

"""

from src.metrics.metric import Metric
from src.cli.url import ModelURL, CodeURL
from typing import Dict
from huggingface_hub import HfApi
import requests


def get_contributors(owner: str, repo: str, token: str = None):
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return [c["login"] for c in r.json()]


class BusFactorMetric(Metric):
    def __init__(self, code_url: CodeURL, model_url: ModelURL):
        super().__init__("bus_factor")
        self.model_url = model_url
        self.code_url = code_url

    def get_data(self) -> Dict[str, int]:
        """
            Gets number of parameters from model_info.safetensors

            Gets contributrs from github api
        """
        api = HfApi()
        info = api.model_info(f"{self.model_url.author}/{self.model_url.name}")

        params = None
        if info.safetensors and "total" in info.safetensors:
            params = info.safetensors.get("total")

        num_contributors = 0
        if self.code_url:
            contributors = get_contributors(
                self.code_url.author, self.code_url.name)
            num_contributors = len(contributors)

        return {
            "params": params,
            "num_contributors": num_contributors,
        }

    def calculate_score(self) -> float:
        """
        Calculate bus factor score based on contributors per billion parameters.
        Normalized to [0,1].
        """
        params = self.data.get("params")
        num_contributors = self.data.get("num_contributors")

        # Defensive: missing or invalid data
        if not params or num_contributors is None:
            return 0.0

        # Convert to billions to match rubric scale
        params_in_billions = params / 1e9 if params > 0 else 1
        ratio = num_contributors / params_in_billions

        # Map rubric → raw score 1–5
        if num_contributors == 0:
            raw_score = 0.2
        elif ratio < 1:
            raw_score = .4
        elif 1 <= ratio <= 2:
            raw_score = 0.6
        elif 3 <= ratio <= 9:
            raw_score = 0.8
        else:  # ratio >= 10
            raw_score = 1

        return raw_score
