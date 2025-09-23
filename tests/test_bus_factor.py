"""
test_bus_factor.py
---------------
Basic unit tests for BusFactorMetric.

Tests cover:
- 
"""

import pytest
from src.metrics.bus_factor import BusFactorMetric
from src.cli.cli import URL

def test_get_data1():
    model_url = URL(raw="https://huggingface.co/google-bert/bert-base-uncased", 
              url_type="model", 
              author="google-bert", 
              name="bert-base-uncased"
        )
    
    code_url = URL(raw="https://github.com/google-research/bert", 
              url_type="code", 
              author="google-research", 
              name="bert"
        )
    
    metric = BusFactorMetric(code_url, model_url)
    metric.run()
    print(metric.data)