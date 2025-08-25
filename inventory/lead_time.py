"""Lead time analysis."""
from __future__ import annotations

import pandas as pd

from pathlib import Path

from .datasets import load_datasets


def compute_lead_times(
    df: pd.DataFrame,
    order_date_col: str,
    receipt_date_col: str,
    *,
    group_col: str | None = None,
) -> pd.Series:
    """Compute lead times in days.

    Parameters
    ----------
    df:
        Data containing order and receipt dates.
    order_date_col, receipt_date_col:
        Column names for order placement and receipt dates.
    group_col:
        Optional column to group by (e.g. supplier) to obtain average lead
        times per group.

    Returns
    -------
    pandas.Series
        Lead times in days.  If ``group_col`` is provided the index will be the
        groups and the values the average lead time for each group.
    """
    if order_date_col not in df.columns or receipt_date_col not in df.columns:
        raise KeyError("order or receipt date column missing")

    order_dates = pd.to_datetime(df[order_date_col])
    receipt_dates = pd.to_datetime(df[receipt_date_col])
    lead_times = (receipt_dates - order_dates).dt.days

    if group_col:
        if group_col not in df.columns:
            raise KeyError(f"{group_col!r} not in DataFrame")
        return lead_times.groupby(df[group_col]).mean()

    return lead_times


def compute_lead_times_from_zip(
    zip_path: str | Path,
    purchases_file: str,
    order_date_col: str,
    receipt_date_col: str,
    *,
    group_col: str | None = None,
) -> pd.Series:
    """Load purchase data from ``zip_path`` and compute lead times."""

    datasets = load_datasets(zip_path, files=[purchases_file])
    key = Path(purchases_file).stem
    if key not in datasets:
        raise FileNotFoundError(f"{purchases_file!r} not found in {zip_path!r}")
    return compute_lead_times(
        datasets[key],
        order_date_col,
        receipt_date_col,
        group_col=group_col,
    )
