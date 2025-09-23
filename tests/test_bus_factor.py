"""
test_bus_factor.py
---------------
Basic unit tests for BusFactorMetric.

Tests cover:
- 
"""

import pytest
from src.metrics.bus_factor import BusFactorMetric
from src.cli.url import CodeURL, ModelURL

def test_get_data_contributors1():
    model_url = ModelURL(raw="https://huggingface.co/google-bert/bert-base-uncased")
    code_url = CodeURL(raw="https://github.com/google-research/bert")

    metric = BusFactorMetric(code_url, model_url)
    metric.run()
    print(metric.data)
    assert metric.data["num_contributors"] == 25


def test_get_data_contributors2():
    model_url = ModelURL(raw="https://huggingface.co/google-bert/bert-base-uncased")
    code_url = CodeURL(raw="https://github.com/rtipper1/ece-30861")
    # Thats us!
    
    metric = BusFactorMetric(code_url, model_url)
    metric.run()
    print(metric.data)
    assert metric.data["num_contributors"] == 4