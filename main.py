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
from src.metrics.dataset_and_code import DatasetAndCodeMetric
from src.cli.cli import URL
from src.cli.url import (
    ModelURL,
    DatasetURL,
    CodeURL,
)
import subprocess
import re 

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
def run_tests() -> None:
    """
    Run pytest on the `tests/` folder with coverage for `src/`,
    print a summary line, and exit per spec.
    """

    completed: subprocess.CompletedProcess[str] = subprocess.run(
        [sys.executable, "-m", "pytest",
         "tests",               # explicitly run test folder
         "--maxfail=1",
         "--disable-warnings",
         "--cov=src",
         "--cov-report=term"],
        capture_output=True,
        text=True
    )

    output: str = completed.stdout + completed.stderr

    # Parse total tests
    collected_match: Optional[re.Match] = re.search(r"collected (\d+) items", output)
    if not collected_match:
        collected_match = re.search(r"collected (\d+) test", output)
    total: int = int(collected_match.group(1)) if collected_match else 0

    # Parse passed tests
    passed_match: Optional[re.Match] = re.search(r"=+ (\d+) passed", output)
    passed: int = int(passed_match.group(1)) if passed_match else 0

    # Parse coverage %
    coverage_match: Optional[re.Match] = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", output)
    coverage: int = int(coverage_match.group(1)) if coverage_match else 0

    # Print summary per spec
    print(f"{passed}/{total} test cases passed. {coverage}% line coverage achieved.")

    # Exit code per spec
    if passed == total and total >= 20 and coverage >= 80:
        sys.exit(0)
    else:
        sys.exit(1)
        
def main(argv=None):
    cli_args = parse_args(argv)
    
    if cli_args.command == 'install':
        print("Installing dependencies from requirements.txt...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

    if cli_args.command == 'test':
        run_tests()

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
                pass

            

# Allows us to run with 'python3 main.py [args]'
if __name__ == "__main__":
    main(sys.argv[1:])
