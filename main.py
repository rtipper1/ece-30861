"""
main.py
---------
Top-level program dispatcher.

Summary
- Entry point invoked by the ./run script.
- Loads URL input (file or inline).
- Delegates handling to the URL factory and model handler.
- Orchestrates metric execution and output generation.
"""

import sys

from src.cli.cli import parse_args
from src.cli.output import build_output
from src.metrics.license import LicenseMetric
from src.metrics.size import SizeMetric
from src.metrics.ramp_up_time import RampUpTimeMetric
from src.metrics.code_quality import CodeQualityMetric
from src.metrics.dataset_quality import DatasetQualityMetric
from src.metrics.bus_factor import BusFactorMetric
from src.metrics.performance_claims import PerformanceClaimsMetric
from src.metrics.glue_score import GlueScoreMetric

metrics = [
    SizeMetric(),
    LicenseMetric(),
    RampUpTimeMetric(),
    BusFactorMetric(),
    DatasetQualityMetric(),
    GlueScoreMetric(),
    CodeQualityMetric(),
    PerformanceClaimsMetric(),
]

if __name__ == "__main__":
    """
        Parse command line argumetns using parse args
            - outputs model owner, name, and URL type

        
        Make model API call to get model metadata
        Download model codebase for relavent metrics
            - Time these operations for accurate latency maybe, still need to check if metric latency 
            Only includes calculation time or also needs to include time to fetch metadata/files
            - Outputs metric data structure to be passed into metrics\

        # Sets data and calculates score and latency for each metric. Worry about doing this concurrently later
        for metric in metrics:
            metric.set_data(model_metadata)
            m.run()

        return build_output(url_name, metrics, METRIC_WEIGHTS)
    """
    pass
