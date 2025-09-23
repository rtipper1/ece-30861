"""
bus_factor.py
---------------
Bus Factor Metric.

Summary
- Calculates contributor redundancy relative to project size.
- Uses number of contributors per parameter scale as described in the rubric.
- Gets number of paramenters from model_info.safetensors
- Gets conitrubutors from github status json

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

            Gets contributrs from api.list_of_contributors
        """
        api = HfApi()
        info = api.model_info(f"{self.model_url.author}/{self.model_url.name}")

        params = None
        if info.safetensors and "total" in info.safetensors:
            params = info.safetensors.get("total")

        contributors = get_contributors(self.code_url.author, self.code_url.name)
        num_contributors = len(contributors)
        
        return {
            "params": params,
            "num_contributors": num_contributors,
        }
    

    def calculate_score(self) -> float:
        return 0.0
    
