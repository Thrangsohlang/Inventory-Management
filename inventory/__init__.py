"""Inventory analysis package.

Provides tools for common inventory management analyses such as
forecasting, ABC classification, EOQ, reorder point and lead time
calculations.
"""

from .demand_forecasting import forecast_demand, forecast_from_zip
from .abc_analysis import classify_inventory, classify_inventory_from_zip
from .eoq import calculate_eoq, calculate_eoq_from_df, calculate_eoq_from_zip
from .reorder_point import (
    calculate_reorder_point,
    calculate_reorder_points_from_df,
    calculate_reorder_points_from_zip,
)
from .lead_time import compute_lead_times, compute_lead_times_from_zip
from .datasets import load_datasets, load_sample_datasets
from .sales_analysis import (
    top_selling_from_zip,
    top_selling_products,
    top_selling_sample,
)

__all__ = [
    "forecast_demand",
    "forecast_from_zip",
    "classify_inventory",
    "classify_inventory_from_zip",
    "calculate_eoq",
    "calculate_eoq_from_df",
    "calculate_eoq_from_zip",
    "calculate_reorder_point",
    "calculate_reorder_points_from_df",
    "calculate_reorder_points_from_zip",
    "compute_lead_times",
    "compute_lead_times_from_zip",
    "load_datasets",
    "load_sample_datasets",
    "top_selling_products",
    "top_selling_from_zip",
    "top_selling_sample",
]
