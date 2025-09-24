import sys
import re
import subprocess

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