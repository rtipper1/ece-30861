"""
metric.py
---------------
Abstract base class for project metrics.

Summary
Each metric:
- Has a unique name.
- Stores the raw data it needs for calculation.
- Computes a score in the range [0,1].
- Records its own computation latency (milliseconds).
- Exports results in a dict format for NDJSON output.

To add a new metric:
1. Subclass Metric.
2. Implement calculate_score(self) using self.data.
3. Optionally override __init__ to set a default name.
"""

import time
from typing import Any, Dict, Optional


class Metric():
    """
    Base class for all metrics.

    Attributes:
        name (str): Unique identifier for the metric.
        data (dict): Parsed metadata required for scoring.
        score (float): Computed score in [0,1].
        latency (int): Computation time in milliseconds.

    Subclasses must implement:
        calculate_score(self) -> float
    """

    def __init__(self, name: str):
        self.name = name
        self.data: Optional[Dict[str, Any]] = None
        self.score: Optional[float] = None
        self.latency: Optional[int] = None

    def set_data(self, data: Dict[str, Any]) -> None:
        """Attach metadata needed to calculate metric."""
        self.data = data

    def calculate_score(self) -> float:
        """
        Compute the metric score.

        Must be implemented by subclasses.
        Should return a float [0, 1]
        """
        return 0

    def run(self) -> None:
        """
        Calculates metric with latency and sets fields
        """
        if self.data is None:
            raise ValueError(f"No data set for metric '{self.name}'")
        start = time.time()
        self.score = self.calculate_score()
        self.latency = int((time.time() - start) * 1000)

    def as_dict(self) -> Dict[str, Any]:
        """
        Returns metric data as a dictionary, may change to NDJSON format, not sure yet
        self.name must reflect what the exact name should be in the NDJSON format table
        """
        return {
            self.name: self.score,
            f"{self.name}_latency": self.latency,
        }
