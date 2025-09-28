"""
performance_claims.py
-----------------------
Performance Claims Metric

Summary:

- Class for storage and calculation of Performance Claims Data and Metrics
- Metric scores based on number of likes and downloads for a model
- Score will be calculated as a percentage of likes/downloads
- The resulting score will be the higher of the metrics the calculation falls between


Rubric:

- 1.0 = likes / downloads = < .75 (75%)
- 0.8 = likes / downloads = < .50 (50%)
- 0.6 = likes / downloads = < .20 (20%)
- 0.4 = likes / downloads = < .10 (10%)
- 0.2 = likes / downloads = < .01 (1%)

- 0.0 = 0 likes or downloads
"""

from src.metrics.metric import Metric
from huggingface_hub import HfApi
from src.cli.url import ModelURL
from typing import Dict, Optional


class PerformanceClaimsMetric(Metric):
    def __init__(self, model_url: ModelURL):
        super().__init__("performance_claims")
        self.model_url = model_url

    def get_data(self) -> Dict[str, Optional[int]]:
        api = HfApi()
        info = api.model_info(f"{self.model_url.author}/{self.model_url.name}")

        def safe_int(value):
            try:
                return int(value)
            except (ValueError, TypeError):
                return None

        model_downloads = safe_int(getattr(info, "downloads", None))
        model_likes = safe_int(getattr(info, "likes", None))

        return {"downloads": model_downloads, "likes": model_likes}

    def calculate_score(self) -> float:
        downloads = self.data.get("downloads")
        likes = self.data.get("likes")

        # If no likes or downloads, give it a 0
        if downloads is None or likes is None:
            return 0.0

        if likes == 0 or downloads == 0:
            ratio = 0
        else:
            ratio = likes / downloads  # already ints

        # Score metric based on categories
        if ratio > 0.75:
            return 1.0
        elif ratio >= 0.5:
            return 0.8
        elif ratio >= 0.2:
            return 0.6
        elif ratio >= 0.1:
            return 0.4
        elif ratio >= 0.01:
            return 0.2
        else:
            return 0.0
