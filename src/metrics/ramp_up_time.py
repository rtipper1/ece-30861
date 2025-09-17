"""
ramp_up_time.py
---------------
Ramp Up Time Metric.

Summary
- Estimates ease of adoption for developers using the model.
- Considers availability of documentation, tutorials, and example code.
- Maps estimated learning curve (minutes to days) into a [0,1] score.
- Calculates latency of the scoring process to support performance reporting.
"""

from .metric import Metric

class RampUpTimeMetric(Metric):
    def __init__(self):
        super().__init__("ramp_up_time")

    def calculate_score(self) -> float:
        return 0.0