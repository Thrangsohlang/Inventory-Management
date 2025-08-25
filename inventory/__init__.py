"""Inventory analysis package.

Provides tools for common inventory management analyses such as
forecasting, ABC classification, EOQ, reorder point and lead time
calculations.
"""

from .demand_forecasting import forecast_demand
from .abc_analysis import classify_inventory
from .eoq import calculate_eoq
from .reorder_point import calculate_reorder_point
from .lead_time import compute_lead_times

__all__ = [
    "forecast_demand",
    "classify_inventory",
    "calculate_eoq",
    "calculate_reorder_point",
    "compute_lead_times",
]
