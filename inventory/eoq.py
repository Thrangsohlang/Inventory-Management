"""Economic order quantity (EOQ) calculations."""
from __future__ import annotations

import math

from pathlib import Path
import pandas as pd

from .datasets import load_datasets


def calculate_eoq(demand: float, order_cost: float, holding_cost: float) -> float:
    """Compute the optimal order quantity using the EOQ formula.

    Parameters
    ----------
    demand:
        Demand over the period (typically annual demand).
    order_cost:
        Cost of placing a single order.
    holding_cost:
        Cost of holding one unit of inventory for the period.

    Returns
    -------
    float
        Optimal order quantity that minimises total inventory cost.
    """
    if demand <= 0:
        raise ValueError("demand must be positive")
    if order_cost <= 0:
        raise ValueError("order_cost must be positive")
    if holding_cost <= 0:
        raise ValueError("holding_cost must be positive")

    return math.sqrt(2 * demand * order_cost / holding_cost)


def calculate_eoq_from_df(
    df: pd.DataFrame,
    demand_col: str,
    order_cost_col: str,
    holding_cost_col: str,
) -> pd.Series:
    """Vectorised EOQ calculation for data frames.

    Parameters
    ----------
    df:
        Data containing demand, order cost and holding cost columns.
    demand_col, order_cost_col, holding_cost_col:
        Column names corresponding to the EOQ parameters.

    Returns
    -------
    pandas.Series
        EOQ for each row of ``df``.
    """

    for col in (demand_col, order_cost_col, holding_cost_col):
        if col not in df.columns:
            raise KeyError(f"{col!r} not in DataFrame")
    return df.apply(
        lambda r: calculate_eoq(r[demand_col], r[order_cost_col], r[holding_cost_col]),
        axis=1,
    )


def calculate_eoq_from_zip(
    zip_path: str | Path,
    file_name: str,
    demand_col: str,
    order_cost_col: str,
    holding_cost_col: str,
) -> pd.Series:
    """Load EOQ parameters from ``zip_path`` and compute EOQ values."""

    datasets = load_datasets(zip_path, files=[file_name])
    key = Path(file_name).stem
    if key not in datasets:
        raise FileNotFoundError(f"{file_name!r} not found in {zip_path!r}")
    return calculate_eoq_from_df(
        datasets[key],
        demand_col,
        order_cost_col,
        holding_cost_col,
    )
