"""Reorder point calculations."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

from .datasets import load_datasets

def calculate_reorder_point(
    daily_demand: float,
    lead_time_days: float,
    *,
    safety_stock: float = 0.0,
) -> float:
    """Determine the inventory level at which to place a new order.

    Parameters
    ----------
    daily_demand:
        Average demand per day.
    lead_time_days:
        Lead time in days.
    safety_stock:
        Additional stock to account for demand variability.

    Returns
    -------
    float
        The reorder point quantity.
    """
    if daily_demand < 0:
        raise ValueError("daily_demand cannot be negative")
    if lead_time_days < 0:
        raise ValueError("lead_time_days cannot be negative")
    if safety_stock < 0:
        raise ValueError("safety_stock cannot be negative")

    return daily_demand * lead_time_days + safety_stock


def calculate_reorder_points_from_df(
    df: pd.DataFrame,
    daily_demand_col: str,
    lead_time_col: str,
    *,
    safety_stock_col: str | None = None,
) -> pd.Series:
    """Vectorised reorder point calculation for data frames."""

    for col in (daily_demand_col, lead_time_col):
        if col not in df.columns:
            raise KeyError(f"{col!r} not in DataFrame")
    if safety_stock_col and safety_stock_col not in df.columns:
        raise KeyError(f"{safety_stock_col!r} not in DataFrame")

    def _calc(row: pd.Series) -> float:
        safety = row[safety_stock_col] if safety_stock_col else 0.0
        return calculate_reorder_point(row[daily_demand_col], row[lead_time_col], safety_stock=safety)

    return df.apply(_calc, axis=1)


def calculate_reorder_points_from_zip(
    zip_path: str | Path,
    file_name: str,
    daily_demand_col: str,
    lead_time_col: str,
    *,
    safety_stock_col: str | None = None,
) -> pd.Series:
    """Load reorder point parameters from ``zip_path`` and compute values."""

    datasets = load_datasets(zip_path, files=[file_name])
    key = Path(file_name).stem
    if key not in datasets:
        raise FileNotFoundError(f"{file_name!r} not found in {zip_path!r}")
    return calculate_reorder_points_from_df(
        datasets[key],
        daily_demand_col,
        lead_time_col,
        safety_stock_col=safety_stock_col,
    )
