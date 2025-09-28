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

from src.cli.url import ModelURL
from src.metrics.performance_claims import PerformanceClaimsMetric

# Dummy empty url to pass into test cases in which we just set the data manually
dummy_url = ModelURL(
    raw="https://huggingface.co/Alibaba-NLP/Tongyi-DeepResearch-30B-A3B")


# def test_get_data():
#     url = ModelURL(
#         raw="https://huggingface.co/Alibaba-NLP/Tongyi-DeepResearch-30B-A3B")

#     metric = PerformanceClaimsMetric(url)
#     metric.run()
#     downloadCheck = metric.data["downloads"]
#     likeCheck = metric.data["likes"]
#     assert likeCheck > 0
#     assert downloadCheck > 0


def test_level_5_PC():
    metric = PerformanceClaimsMetric(dummy_url)
    metric.set_data({"downloads": 100, "likes": 80})
    metric.run()
    assert metric.score == 1


def test_level_4_PC():
    metric = PerformanceClaimsMetric(dummy_url)
    metric.set_data({"downloads": 1000, "likes": 600})
    metric.run()
    assert metric.score == 0.8


def test_level_3_PC():
    metric = PerformanceClaimsMetric(dummy_url)
    metric.set_data({"downloads": 10000, "likes": 3500})
    metric.run()
    assert metric.score == 0.6


def test_level_2_PC():
    metric = PerformanceClaimsMetric(dummy_url)
    metric.set_data({"downloads": 100, "likes": 15})
    metric.run()
    assert metric.score == 0.4


def test_level_1_PC():
    metric = PerformanceClaimsMetric(dummy_url)
    metric.set_data({"downloads": 100, "likes": 8})
    metric.run()
    assert metric.score == 0.2


def test_none_PC():
    metric = PerformanceClaimsMetric(dummy_url)
    metric.set_data({"downloads": None, "likes": None})
    metric.run()
    assert metric.score == 0.0


def test_zero_likes_downloads():
    metric = PerformanceClaimsMetric(dummy_url)
    metric.set_data({"downloads": 0, "likes": 0})
    metric.run()
    assert metric.score == 0.0

import pytest
from huggingface_hub import HfApi

from src.cli.url import ModelURL
from src.metrics.performance_claims import PerformanceClaimsMetric


# def test_hf_api_returns_likes_and_downloads():
#     """Direct API test: Make sure HuggingFace Hub gives likes and downloads."""
#     api = HfApi()
#     info = api.model_info("bert-base-uncased")  # well-known model
#     assert hasattr(info, "likes")
#     assert hasattr(info, "downloads")
#     assert isinstance(info.likes, int)
#     assert isinstance(info.downloads, int)
#     assert info.likes > 0  # this repo is very popular
#     assert info.downloads > 0


# def test_performance_claims_metric_data():
#     """Make sure PerformanceClaimsMetric pulls likes and downloads correctly."""
#     model_url = ModelURL(raw="https://huggingface.co/bert-base-uncased")
#     metric = PerformanceClaimsMetric(model_url)
#     data = metric.get_data()
#     assert "likes" in data
#     assert "downloads" in data
#     assert isinstance(data["likes"], int)
#     assert isinstance(data["downloads"], int)
#     assert data["likes"] > 0
#     assert data["downloads"] > 0


# def test_performance_claims_calculate_score():
#     """Run the metric fully and check that score is > 0 for popular models."""
#     model_url = ModelURL(raw="https://huggingface.co/bert-base-uncased")
#     metric = PerformanceClaimsMetric(model_url)
#     metric.run()
#     score = metric.score
#     assert isinstance(score, float)
#     assert 0.0 <= score <= 1.0
#     # bert-base-uncased is popular, so score should not be 0
#     assert score > 0.0
