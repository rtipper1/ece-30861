import json
from src.metrics.license import LicenseMetric
from src.metrics.size import SizeMetric
from src.metrics.ramp_up_time import RampUpTimeMetric
from src.metrics.code_quality import CodeQualityMetric
from src.metrics.dataset_quality import DatasetQualityMetric
from src.metrics.bus_factor import BusFactorMetric
from src.metrics.performance_claims import PerformanceClaimsMetric
from src.metrics.glue_score import GlueScoreMetric
from src.cli.output import build_output
from src.cli.cli import URL

def test_build_output():
    # Instantiate all metric classes
    dummy_url = URL(raw="", url_type="", author="", name="")
    metrics = [
        RampUpTimeMetric(),
        BusFactorMetric(),
        PerformanceClaimsMetric(),
        LicenseMetric(dummy_url),
        SizeMetric(),
        GlueScoreMetric(),
        DatasetQualityMetric(),
        CodeQualityMetric(),
    ]

    # Hard-code scores and latencies for test
    test_values = {
        "ramp_up_time": (0.8, 10),
        "bus_factor": (0.6, 20),
        "performance_claims": (0.7, 15),
        "license": (1.0, 5),
        "size": (0.9, 12),
        "dataset_and_code_score": (0.85, 30),
        "dataset_quality": (0.75, 18),
        "code_quality": (0.65, 25),
    }

    for m in metrics:
        score, latency = test_values[m.name]
        m.score = score
        m.latency = latency

    # Define weights for all metrics (sum doesn’t have to be 1 for test)
    weights = {m.name: 0.1 for m in metrics}

    # Build NDJSON output
    result_json = build_output("bert-base-uncased", metrics, weights)
    result = json.loads(result_json)

    # Assertions: check top-level keys exist
    assert result["name"] == "bert-base-uncased"
    assert result["category"] == "MODEL"

    # Check each metric’s values got inserted
    for name, (score, latency) in test_values.items():
        assert abs(result[name] - score) < 1e-6
        assert result[f"{name}_latency"] == latency

    # Check net_score matches weighted sum
    expected_score = sum(weights[name] * score for name, (score, _) in test_values.items())
    assert abs(result["net_score"] - expected_score) < 1e-6

    # Check net_score_latency matches sum of latencies
    expected_latency = sum(lat for _, lat in test_values.values())
    assert result["net_score_latency"] == expected_latency
