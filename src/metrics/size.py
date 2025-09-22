"""
size.py
-------
Model Size Metric.

Summary
- Scores model size based on parameter count and deployability.
- Uses Hugging Face API metadata and repo files (e.g., config.json, weight files).
- Normalizes parameter ranges (100M to trillions) into a [0,1] score.
- Reports calculation latency in milliseconds.
"""

from .metric import Metric

class SizeMetric(Metric):
    def __init__(self, name: str = "size"):
        super().__init__(name)

    def calculate_score(self) -> float:
        """
        Calculate the size score based on parameter count.
        Expects self.data to include {"params": <int>} where params is the total parameter count.
        """
        if not self.data or "params" not in self.data:
            raise ValueError("SizeMetric requires 'params' field in data")

        params = self.data["params"]

        if params < 100_000_000:        # < 100M
            raw_score = 1
        elif params < 1_000_000_000:    # 100M - 1B
            raw_score = 2
        elif params < 10_000_000_000:   # 1B - 10B
            raw_score = 3
        elif params < 50_000_000_000:   # 10B - 50B
            raw_score = 4
        else:                           # > 50B
            raw_score = 5

        # Normalize to [0,1]
        return raw_score / 5.0