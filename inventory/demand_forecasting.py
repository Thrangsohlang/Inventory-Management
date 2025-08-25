"""Demand forecasting utilities.

This module provides a helper to forecast future demand using Holt-Winters
exponential smoothing.  The function expects a ``pandas.Series`` indexed by
``datetime`` and returns a forecast for the requested number of periods.
"""
from __future__ import annotations

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


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
