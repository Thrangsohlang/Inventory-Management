"""Reorder point calculations."""
from __future__ import annotations


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
