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
from src.cli.cli import parse_url_file
from src.cli.output import build_output
from src.metrics.license import LicenseMetric
from src.metrics.size import SizeMetric
from src.metrics.ramp_up_time import RampUpTimeMetric
from src.metrics.code_quality import CodeQualityMetric
from src.metrics.dataset_quality import DatasetQualityMetric
from src.metrics.bus_factor import BusFactorMetric
from src.metrics.performance_claims import PerformanceClaimsMetric
from src.metrics.glue_score import GlueScoreMetric
from src.cli.cli import URL
from src.cli.url import (
    ModelURL,
    DatasetURL,
    CodeURL,
)
import subprocess
import multiprocessing

# Dummy empty url to pass into test cases in which we just set the data manually
dummy_model_url = ModelURL(raw="https://huggingface.co/google-bert/bert-base-uncased")
dummy_code_url = CodeURL(raw="https://github.com/google-research/bert")
dummy_dataset_url = DatasetURL(raw="https://huggingface.co/datasets/bookcorpus/bookcorpus")

metric_classes = [
    (RampUpTimeMetric, []),                          # no URL required
    (BusFactorMetric, ["model"]),                   # needs model URL
    (PerformanceClaimsMetric, []),
    (LicenseMetric, ["model"]),                     # needs model URL
    (SizeMetric, ["model"]),                        # needs model URL
    (GlueScoreMetric, []),
    (DatasetQualityMetric, ["dataset"]),            # needs dataset URL
    (CodeQualityMetric, ["code", "model"]),         # needs both
]

def run_metric(metric_class, url_roles, code_url, dataset_url, model_url):
    try:
        # Map roles -> actual args
        args = []
        for role in url_roles:
            if role == "code":
                args.append(code_url)
            elif role == "dataset":
                args.append(dataset_url)
            elif role == "model":
                args.append(model_url)

        # Instantiate with the correct URLs
        metric = metric_class(*args)

        # Run the metric
        metric.run()
        return (metric.name, metric.score, metric.data)

    except Exception as e:
        return (metric_class.__name__, None, f"Error: {e}")

metrics = [
    RampUpTimeMetric(),
    BusFactorMetric(dummy_model_url),
    PerformanceClaimsMetric(),
    LicenseMetric(dummy_model_url),
    SizeMetric(dummy_model_url),
    GlueScoreMetric(), # Dataset and code score
    DatasetQualityMetric(),
    CodeQualityMetric(dummy_code_url, dummy_model_url),
]

def main(argv=None):
    cli_args = parse_args(argv)
    
    if cli_args.command == 'install':
        print("Installing dependencies from requirements.txt...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

    if cli_args.command == 'test':
        print("test")

    if cli_args.command == 'process':
        lines = parse_url_file(cli_args.url_file)
        
        for line in lines:
            code_url, dataset_url, model_url = line
            print(code_url)
            print(dataset_url)
            print(model_url)

            # If line contains a model url, process it
            if model_url:
                """
                    - calculate metrics in parallel
                """
                with multiprocessing.Pool(processes=len(metric_classes)) as pool:
                    results = pool.starmap(
                    run_metric,
                    [(cls, roles, code_url, dataset_url, model_url) for cls, roles in metric_classes]
                )

                for name, score, data in results:
                    print(f"[{name}] score={score}, data={data}")
                    pass

# Allows us to run with 'python3 main.py [args]'
if __name__ == "__main__":
    main(sys.argv[1:])
