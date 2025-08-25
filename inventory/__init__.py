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
from .datasets import load_datasets
from .sales_analysis import top_selling_from_zip, top_selling_products

__all__ = [
    "forecast_demand",
    "classify_inventory",
    "calculate_eoq",
    "calculate_reorder_point",
    "compute_lead_times",
    "load_datasets",
    "top_selling_products",
    "top_selling_from_zip",
]
