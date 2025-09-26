"""
test_performance_claims.py
---------------
Basic unit tests for PerformanceClaimsMetric.

Tests cover:
- Model with any number of likes and downloads
- Model does not have any likes or downloads
- Model or download data is unavailable (Should be the same as previous case)
- Model and download numbers create the correct metric score

"""

import pytest
from src.metrics.performance_claims import PerformanceClaimsMetric
from src.cli.url import ModelURL

# Dummy empty url to pass into test cases in which we just set the data manually
dummy_url = ModelURL(raw="https://huggingface.co/Alibaba-NLP/Tongyi-DeepResearch-30B-A3B")


def test_get_data():
    url = ModelURL(raw="https://huggingface.co/Alibaba-NLP/Tongyi-DeepResearch-30B-A3B")

    metric = PerformanceClaimsMetric(url)
    metric.run()
    downloadCheck = metric.data["Downloads"]
    likeCheck = metric.data["Likes"]
    assert likeCheck > 0
    assert downloadCheck > 0


def test_level_5_PC():
    metric = PerformanceClaimsMetric(dummy_url)
    metric.set_data({"Downloads": "100", "Likes" : "80"})
    metric.run()
    assert metric.score == 1


def test_level_4_PC():
    metric = PerformanceClaimsMetric(dummy_url)
    metric.set_data({"Downloads": "1000", "Likes" : "600"})
    metric.run()
    assert metric.score == 0.8


def test_level_3_PC():
    metric = PerformanceClaimsMetric(dummy_url)
    metric.set_data({"Downloads": "10000", "Likes" : "3500"})
    metric.run()
    assert metric.score == 0.6


def test_level_2_PC():
    metric = PerformanceClaimsMetric(dummy_url)
    metric.set_data({"Downloads": "100", "Likes" : "15"})
    metric.run()
    assert metric.score == 0.4


def test_level_1_PC():
    metric = PerformanceClaimsMetric(dummy_url)
    metric.set_data({"Downloads": "100", "Likes" : "8"})
    metric.run()
    assert metric.score == 0.2


def test_none_PC():
    metric = PerformanceClaimsMetric(dummy_url)
    metric.set_data({"Downloads": None, "Likes" : None})
    metric.run()
    assert metric.score == 0.0


def test_zero_likes_downloads():
    metric = PerformanceClaimsMetric(dummy_url)
    metric.set_data({"Downloads": "0", "Likes" : "0"})
    metric.run()
    assert metric.score == 0.0
    
    
def test_empty_likes_downloads():
    metric = PerformanceClaimsMetric(dummy_url)
    metric.set_data({"Downloads": "", "Likes" : ""})
    metric.run()
    assert metric.score == 0.0