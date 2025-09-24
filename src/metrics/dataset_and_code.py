"""
glue_score.py
---------------
Dataset and Code Availability Metric.

Summary

"""

from src.metrics.metric import Metric
from typing import Dict

class DatasetAndCodeMetric(Metric):
    def __init__(self):
        super().__init__("dataset_and_code_score")

    def calculate_score(self) -> float:
        return 0.0

    def get_data(self) -> Dict[str, float]:
        return {
            "dataset_and_code": 0.0,
        }