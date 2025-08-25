import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import pytest

from inventory import (
    calculate_eoq,
    calculate_reorder_point,
    classify_inventory,
    compute_lead_times,
    forecast_demand,
)


def test_forecast_demand_returns_correct_length():
    dates = pd.date_range("2023-01-01", periods=12, freq="M")
    series = pd.Series(range(1, 13), index=dates)
    forecast = forecast_demand(series, periods=3)
    assert len(forecast) == 3


def test_abc_classification():
    df = pd.DataFrame({"item": list("ABCD"), "value": [100, 60, 30, 10]})
    result = classify_inventory(df, "value")
    categories = result.set_index("item")["category"].to_dict()
    assert categories == {"A": "A", "B": "A", "C": "B", "D": "C"}


def test_eoq_formula():
    eoq = calculate_eoq(demand=1000, order_cost=50, holding_cost=5)
    assert pytest.approx(eoq, rel=1e-3) == 141.4213562373095


def test_reorder_point():
    rop = calculate_reorder_point(10, 5, safety_stock=20)
    assert rop == 70


def test_lead_time():
    df = pd.DataFrame(
        {
            "order": ["2024-01-01", "2024-01-05"],
            "receive": ["2024-01-11", "2024-01-10"],
            "supplier": ["X", "X"],
        }
    )
    res = compute_lead_times(df, "order", "receive")
    assert list(res) == [10, 5]
    grouped = compute_lead_times(df, "order", "receive", group_col="supplier")
    assert pytest.approx(grouped["X"], rel=1e-3) == 7.5
