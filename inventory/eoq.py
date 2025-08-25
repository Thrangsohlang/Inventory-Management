"""Economic order quantity (EOQ) calculations."""
from __future__ import annotations

import math


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
