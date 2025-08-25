import os
import sys
import zipfile

import pandas as pd
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from inventory import (
    calculate_eoq,
    calculate_eoq_from_df,
    calculate_eoq_from_zip,
    calculate_reorder_point,
    calculate_reorder_points_from_df,
    calculate_reorder_points_from_zip,
    classify_inventory,
    classify_inventory_from_zip,
    compute_lead_times,
    compute_lead_times_from_zip,
    forecast_demand,
    forecast_from_zip,
)


def _make_zip(path, files):
    with zipfile.ZipFile(path, "w") as zf:
        for name, df in files.items():
            zf.writestr(f"{name}.csv", df.to_csv(index=False))
    return path


def test_forecast_demand_returns_correct_length():
    dates = pd.date_range("2023-01-01", periods=12, freq="M")
    series = pd.Series(range(1, 13), index=dates)
    forecast = forecast_demand(series, periods=3)
    assert len(forecast) == 3


def test_forecast_from_zip(tmp_path):
    df = pd.DataFrame({"date": pd.date_range("2023-01-01", periods=3, freq="D"), "qty": [1, 2, 3]})
    zip_path = _make_zip(tmp_path / "sales.zip", {"sales": df})
    forecast = forecast_from_zip(zip_path, "sales.csv", "date", "qty", periods=2)
    assert len(forecast) == 2


def test_abc_classification():
    df = pd.DataFrame({"item": list("ABCD"), "value": [100, 60, 30, 10]})
    result = classify_inventory(df, "value")
    categories = result.set_index("item")["category"].to_dict()
    assert categories == {"A": "A", "B": "A", "C": "B", "D": "C"}


def test_classify_inventory_from_zip(tmp_path):
    inv_df = pd.DataFrame({"item": list("ABC"), "value": [100, 50, 10]})
    zip_path = _make_zip(tmp_path / "inv.zip", {"inventory": inv_df})
    classified = classify_inventory_from_zip(zip_path, "inventory.csv", "value")
    categories = classified.set_index("item")["category"].to_dict()
    assert categories == {"A": "A", "B": "B", "C": "C"}


def test_eoq_formula():
    eoq = calculate_eoq(demand=1000, order_cost=50, holding_cost=5)
    assert pytest.approx(eoq, rel=1e-3) == 141.4213562373095


def test_eoq_from_df_and_zip(tmp_path):
    df = pd.DataFrame({"d": [1000], "o": [50], "h": [5]})
    res = calculate_eoq_from_df(df, "d", "o", "h")
    assert pytest.approx(res.iloc[0], rel=1e-3) == 141.4213562373095
    zip_path = _make_zip(tmp_path / "eoq.zip", {"params": df})
    from_zip = calculate_eoq_from_zip(zip_path, "params.csv", "d", "o", "h")
    assert pytest.approx(from_zip.iloc[0], rel=1e-3) == 141.4213562373095


def test_reorder_point():
    rop = calculate_reorder_point(10, 5, safety_stock=20)
    assert rop == 70


def test_reorder_points_from_df_and_zip(tmp_path):
    df = pd.DataFrame({"d": [10], "l": [5], "s": [20]})
    res = calculate_reorder_points_from_df(df, "d", "l", safety_stock_col="s")
    assert res.iloc[0] == 70
    zip_path = _make_zip(tmp_path / "rop.zip", {"params": df})
    from_zip = calculate_reorder_points_from_zip(
        zip_path, "params.csv", "d", "l", safety_stock_col="s"
    )
    assert from_zip.iloc[0] == 70


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


def test_lead_times_from_zip(tmp_path):
    df = pd.DataFrame({"order": ["2024-01-01"], "receive": ["2024-01-11"]})
    zip_path = _make_zip(tmp_path / "lead.zip", {"purchases": df})
    res = compute_lead_times_from_zip(zip_path, "purchases.csv", "order", "receive")
    assert list(res) == [10]

