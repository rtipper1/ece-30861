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
import subprocess
import re

from src.cli.cli import parse_args
from src.cli.cli import parse_url_file
from src.cli.output import build_output
from src.metrics.license import LicenseMetric
from src.metrics.size import SizeMetric
from src.metrics.ramp_up_time import RampUpTimeMetric
from src.metrics.code_quality import CodeQualityMetric
from src.metrics.dataset_quality import DatasetQualityMetric
from src.metrics.bus_factor import BusFactorMetric
from src.metrics.performance_claims import PerformanceClaimsMetric
from src.metrics.dataset_and_code import DatasetAndCodeMetric
from src.cli.cli import URL
from src.cli.url import ModelURL, DatasetURL, CodeURL


# Dummy empty url to pass into test cases in which we just set the data manually
dummy_model_url = ModelURL(raw="https://huggingface.co/google-bert/bert-base-uncased")
dummy_code_url = CodeURL(raw="https://github.com/google-research/bert")
dummy_dataset_url = DatasetURL(raw="https://huggingface.co/datasets/bookcorpus/bookcorpus")

metrics = [
    RampUpTimeMetric(),
    BusFactorMetric(dummy_code_url, dummy_model_url),
    PerformanceClaimsMetric(dummy_model_url),
    LicenseMetric(dummy_model_url),
    SizeMetric(dummy_model_url),
    DatasetAndCodeMetric(), # Dataset and code score
    DatasetQualityMetric(),
    CodeQualityMetric(dummy_code_url, dummy_model_url),
]
        
def main(argv=None):
    cli_args = parse_args(argv)

    if cli_args.command == 'process':
        lines = parse_url_file(cli_args.url_file)

        # Define metric weights (adjust as needed)
        weights = {
            "ramp_up_time": 0.1,
            "bus_factor": 0.15,
            "performance_claims": 0.1,
            "license": 0.1,
            "size_score": 0.1,
            "dataset_and_code_score": 0.15,
            "dataset_quality": 0.15,
            "code_quality": 0.15,
        }
        
        for line in lines:
            code_url, dataset_url, model_url = line

            metrics = [
                RampUpTimeMetric(),
                BusFactorMetric(code_url, model_url),
                PerformanceClaimsMetric(model_url),
                LicenseMetric(model_url),
                SizeMetric(model_url),
                DatasetAndCodeMetric(),
                DatasetQualityMetric(),
                CodeQualityMetric(code_url, model_url),
            ]

            # If line contains a model url, process it
            if model_url:
                for metric in metrics:
                    metric.run()

            output_str = build_output(model_url, metrics, weights)
            print(output_str)

# Allows us to run with 'python3 main.py [args]'
if __name__ == "__main__":
    main(sys.argv[1:])
