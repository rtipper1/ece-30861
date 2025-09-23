"""
bus_factor.py
---------------
Bus Factor Metric.

Summary
- Calculates contributor redundancy relative to project size.
- Uses number of contributors per parameter scale as described in the rubric.
- Scores in [0,1]; higher = safer (more maintainers).

Notes
- Determine with: git shortlog -s -n 
- lists contributor and number of commits
"""

from src.metrics.metric import Metric
from src.cli.cli import URL
from typing import Dict, Optional, Any
from huggingface_hub import HfApi

class BusFactorMetric(Metric):
    def __init__(self, model_url: URL):
        super().__init__("bus_factor")
        self.model_url = model_url

    def get_data(self) -> Dict[str, Optional[Any]]:
        """
            Gets number of parameters from model_info.safetensors or
            cardata params

            Gets contributrs from api.list_of_contributors
        """
        api = HfApi()
        info = api.model_info(f"{self.model_url.author}/{self.model_url.name}")

        params = None
        if info.safetensors and "total" in info.safetensors:
            params = info.safetensors.get("total")

        contributors = api.list_repo_contributors(f"{self.model_url.author}/{self.model_url.name}")
        num_contributors = len(contributors)
        
        return {
            "params": params,
            "num_contributors": num_contributors,
        }
    

    def calculate_score(self) -> float:
        return 0.0