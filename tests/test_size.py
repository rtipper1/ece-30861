"""
test_size.py
---------------
Basic unit tests for SizeMetric.

Tests cover:
-
"""

import pytest
from src.metrics.size import SizeMetric
from src.cli.cli import URL

# Dummy empty url to pass into test cases in which we just set the data manually
dummy_url = URL(raw="", url_type="", author="", name="")

def test_get_data1():
    url = URL(raw="https://huggingface.co/Alibaba-NLP/Tongyi-DeepResearch-30B-A3B", 
            url_type="model", 
            author="Alibaba-NLP", 
            name="Tongyi-DeepResearch-30B-A3B"
    )

    metric = SizeMetric(url)
    metric.run()
    scores = metric.score
    assert isinstance(scores, dict)
    assert "aws_server" in scores


def test_get_data2():
    url = URL(raw="https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct", 
        url_type="model", 
        author="Qwen", 
        name="Qwen3-Omni-30B-A3B-Instruct"
    )
    metric = SizeMetric(url)
    metric.run()
    scores = metric.score
    assert isinstance(scores, dict)
    assert "aws_server" in scores


def test_get_data3():
    url = URL(raw="https://huggingface.co/ibm-granite/granite-docling-258M", 
        url_type="model", 
        author="ibm-granite", 
        name="granite-docling-258M"
    )
    metric = SizeMetric(url)
    metric.run()
    scores = metric.score
    assert isinstance(scores, dict)
    assert "aws_server" in scores


def test_get_data_none():
    url = URL(raw="https://huggingface.co/bytedance-research/HuMo", 
        url_type="model", 
        author="bytedance-research", 
        name="HuMo"
    )
    metric = SizeMetric(url)
    metric.run()
    scores = metric.score
    assert isinstance(scores, dict)


def test_none_size():
    metric = SizeMetric(dummy_url)
    metric.set_data({"size": None})
    metric.run()
    scores = metric.score
    assert isinstance(scores, dict)
    assert all(v == 0 for v in scores.values())
