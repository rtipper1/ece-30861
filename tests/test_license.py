"""
test_license.py
---------------
Basic unit tests for LicenseMetric.

Tests cover:
- All license tiers (1–5)
- Unknown license string
- Missing license field
"""

import pytest
from metrics.license import LicenseMetric


def test_level_5_license():
    metric = LicenseMetric()
    metric.set_data({"license": "apache-2.0"})
    metric.run()
    assert metric.score == 1.0


def test_level_4_license():
    metric = LicenseMetric()
    metric.set_data({"license": "lgpl-3.0"})
    metric.run()
    assert metric.score == 0.8


def test_level_3_license():
    metric = LicenseMetric()
    metric.set_data({"license": "cc-by-nc-4.0"})
    metric.run()
    assert metric.score == 0.6


def test_level_2_license():
    metric = LicenseMetric()
    metric.set_data({"license": "openrail"})
    metric.run()
    assert metric.score == 0.4


def test_level_1_license():
    metric = LicenseMetric()
    metric.set_data({"license": "llama3"})
    metric.run()
    assert metric.score == 0.2


def test_case_insensitivity():
    metric = LicenseMetric()
    metric.set_data({"license": "APACHE-2.0"})
    metric.run()
    assert metric.score == 1.0


def test_license_with_whitespace():
    metric = LicenseMetric()
    metric.set_data({"license": "  mit  "})
    metric.run()
    assert metric.score == 1.0


def test_unknown_license():
    metric = LicenseMetric()
    metric.set_data({"license": "something-unknown"})
    metric.run()
    assert metric.score == 0.0


def test_none_license():
    metric = LicenseMetric()
    metric.set_data({"license": None})
    metric.run()
    assert metric.score == 0.0

def test_empty_license_string():
    metric = LicenseMetric()
    metric.set_data({"license": ""})
    metric.run()
    assert metric.score == 0.0