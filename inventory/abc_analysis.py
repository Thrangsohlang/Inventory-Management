"""ABC analysis for inventory classification."""
from __future__ import annotations

import pandas as pd
from pathlib import Path

from .datasets import load_datasets


def classify_inventory(
    df: pd.DataFrame,
    value_col: str,
    *,
    a_threshold: float = 0.8,
    b_threshold: float = 0.95,
) -> pd.DataFrame:
    """Classify inventory items into A/B/C categories.

    The classification is based on cumulative contribution of ``value_col``.
    Items contributing up to ``a_threshold`` of total value are category ``A``,
    the next up to ``b_threshold`` are ``B`` and the remainder are ``C``.

    Parameters
    ----------
    df:
        Input data containing an item identifier and a value column.
    value_col:
        Column representing the value of each item (e.g. annual usage value).
    a_threshold, b_threshold:
        Cumulative percentage cut-offs for class ``A`` and ``B``.

    Returns
    -------
    pandas.DataFrame
        Original data with an additional ``category`` column.
    """
    if value_col not in df.columns:
        raise KeyError(f"{value_col!r} not in DataFrame")

    working = df.copy()
    working = working.sort_values(value_col, ascending=False)
    total = working[value_col].sum()
    if total <= 0:
        raise ValueError("total inventory value must be positive")
    working["cumulative_pct"] = working[value_col].cumsum() / total

    def _assign(pct: float) -> str:
        if pct <= a_threshold:
            return "A"
        if pct <= b_threshold:
            return "B"
        return "C"

    working["category"] = working["cumulative_pct"].apply(_assign)
    return working.drop(columns=["cumulative_pct"])


def classify_inventory_from_zip(
    zip_path: str | Path,
    inventory_file: str,
    value_col: str,
    *,
    a_threshold: float = 0.8,
    b_threshold: float = 0.95,
) -> pd.DataFrame:
    """Load data from a zip archive and classify inventory items.

    Parameters
    ----------
    zip_path:
        Path to the zip archive containing the inventory CSV.
    inventory_file:
        Name of the CSV file within the archive.
    value_col:
        Column representing the value of each item.
    a_threshold, b_threshold:
        Cumulative percentage cut-offs for class ``A`` and ``B``.

    Returns
    -------
    pandas.DataFrame
        Classified inventory data.
    """

    datasets = load_datasets(zip_path, files=[inventory_file])
    key = Path(inventory_file).stem
    if key not in datasets:
        raise FileNotFoundError(f"{inventory_file!r} not found in {zip_path!r}")
    return classify_inventory(
        datasets[key],
        value_col,
        a_threshold=a_threshold,
        b_threshold=b_threshold,
    )
