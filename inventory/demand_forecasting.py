"""Demand forecasting utilities.

This module provides a helper to forecast future demand using Holt-Winters
exponential smoothing.  The function expects a ``pandas.Series`` indexed by
``datetime`` and returns a forecast for the requested number of periods.
"""
from __future__ import annotations

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from pathlib import Path

from .datasets import load_datasets


def forecast_demand(
    series: pd.Series,
    periods: int,
    *,
    seasonal_periods: int | None = None,
) -> pd.Series:
    """Forecast future demand.

    Parameters
    ----------
    series:
        Historical demand indexed by ``datetime``.
    periods:
        Number of future periods to forecast.
    seasonal_periods:
        Length of the seasonal cycle.  If ``None`` no seasonality is
        modelled.

    Returns
    -------
    pandas.Series
        Forecasted demand for the next ``periods`` periods.
    """
    if not isinstance(series.index, pd.DatetimeIndex):
        raise TypeError("series must be indexed by a DatetimeIndex")
    if series.empty:
        raise ValueError("series must contain at least one observation")

    model = ExponentialSmoothing(
        series,
        trend="add",
        seasonal="add" if seasonal_periods else None,
        seasonal_periods=seasonal_periods,
    ).fit()
    forecast = model.forecast(periods)
    return forecast


def forecast_from_zip(
    zip_path: str | Path,
    sales_file: str,
    date_col: str,
    quantity_col: str,
    periods: int,
    *,
    seasonal_periods: int | None = None,
) -> pd.Series:
    """Load sales data from a zip archive and forecast future demand.

    The CSV file is read using :func:`load_datasets`.  The resulting DataFrame
    is aggregated by ``date_col`` and the specified ``quantity_col`` is used as
    the demand series.

    Parameters
    ----------
    zip_path:
        Path to the zip archive containing the sales data.
    sales_file:
        Name of the CSV file within the archive.
    date_col, quantity_col:
        Columns representing the sale date and quantity sold.
    periods:
        Number of future periods to forecast.
    seasonal_periods:
        Length of the seasonal cycle.  If ``None`` no seasonality is modelled.

    Returns
    -------
    pandas.Series
        Forecasted demand for the next ``periods`` periods.
    """

    datasets = load_datasets(zip_path, files=[sales_file])
    key = Path(sales_file).stem
    if key not in datasets:
        raise FileNotFoundError(f"{sales_file!r} not found in {zip_path!r}")
    df = datasets[key]
    for col in (date_col, quantity_col):
        if col not in df.columns:
            raise KeyError(f"{col!r} not in sales data")

    df[date_col] = pd.to_datetime(df[date_col])
    series = df.groupby(df[date_col])[quantity_col].sum().sort_index()
    series = series.asfreq("D", fill_value=0)
    return forecast_demand(
        series,
        periods,
        seasonal_periods=seasonal_periods,
    )
