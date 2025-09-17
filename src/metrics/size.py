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
    def __init__(self):
        super().__init__("size")

    def calculate_score(self) -> float:
        return 0.0