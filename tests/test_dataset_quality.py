"""
test_dataset_quality.py
---------------
Basic unit tests for DatasetQualityeMetric.

Tests cover:
- Metric gets the correct score from an example url
- Metric gets the correct score given the number of significant phrases
- Metric gives the correct score when there are no significant phrases
"""

import pytest
from src.metrics.dataset_quality import DatasetQualityMetric
from src.cli.url import DatasetURL

# Dummy empty url to pass into test cases in which we just set the data manually
dummy_url = DatasetURL(raw="https://huggingface.co/datasets/HuggingFaceM4/FineVision")


def test_get_data():
    url = DatasetURL(raw="https://huggingface.co/datasets/HuggingFaceM4/FineVision")

    metric = DatasetQualityMetric(url)
    metric.run()
    assert metric.data == {"score": 1}
    assert metric.score == 0.2


def test_level_5_DQ():
    metric = DatasetQualityMetric(dummy_url)
    metric.set_data({"score ": 5})
    metric.run()
    assert metric.score == 1


def test_level_4_DQv ():
    metric = DatasetQualityMetric(dummy_url)
    metric.set_data({"score": 4})
    metric.run()
    assert metric.score == 0.8


def test_level_3_DQ():
    metric = DatasetQualityMetric(dummy_url)
    metric.set_data({"score": 3})
    metric.run()
    assert metric.score == 0.6


def test_level_2_DQ():
    metric = DatasetQualityMetric(dummy_url)
    metric.set_data({"score": 2})
    metric.run()
    assert metric.score == 0.4


def test_level_1_DQ():
    metric = DatasetQualityMetric(dummy_url)
    metric.set_data({"score": 1})
    metric.run()
    assert metric.score == 0.2


def test_level_0_DQ():
    metric = DatasetQualityMetric(dummy_url)
    metric.set_data({"score": 0})
    metric.run()
    assert metric.score == 0.0


def test_none_DQ():
    metric = DatasetQualityMetric(dummy_url)
    metric.set_data({"score": None})
    metric.run()
    assert metric.score == 0.0


def test_empty_DQ():
    metric = DatasetQualityMetric(dummy_url)
    metric.set_data({"score": ""})
    metric.run()
    assert metric.score == 0.0