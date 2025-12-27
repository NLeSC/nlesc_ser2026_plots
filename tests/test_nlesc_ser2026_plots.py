"""Tests for the nlesc_ser2026_plots.my_module module."""

import pytest
from nlesc_ser2026_plots.my_module import create_stacked_bar_chart
"""Tests for the nlesc_ser2026_plots.my_module module."""


def test_create_stacked_bar_chart_valid_input():
    """Test create_stacked_bar_chart with valid input data."""
    data = {
        "Category A": [10, 20, 30],
        "Category B": [15, 25, 35],
    }
    labels = ["Label 1", "Label 2", "Label 3"]
    title = "Test Stacked Bar Chart"

    try:
        create_stacked_bar_chart(data, labels, title)
    except Exception as e:
        pytest.fail(f"create_stacked_bar_chart raised an exception: {e}")


def test_create_stacked_bar_chart_empty_data():
    """Test create_stacked_bar_chart with empty data."""
    data = {}
    labels = []
    title = "Empty Chart"

    with pytest.raises(ValueError, match="Data cannot be empty"):
        create_stacked_bar_chart(data, labels, title)


def test_create_stacked_bar_chart_mismatched_labels():
    """Test create_stacked_bar_chart with mismatched labels and data."""
    data = {
        "Category A": [10, 20],
        "Category B": [15, 25],
    }
    labels = ["Label 1"]  # Mismatched length
    title = "Mismatched Labels Chart"

    with pytest.raises(ValueError, match="Labels length must match data length"):
        create_stacked_bar_chart(data, labels, title)

