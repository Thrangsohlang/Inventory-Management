"""Sales analysis utilities."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

from .datasets import load_datasets


def top_selling_products(
    df: pd.DataFrame,
    product_col: str,
    quantity_col: str,
    *,
    top_n: int = 10,
) -> pd.DataFrame:
    """Return the top ``top_n`` products by quantity sold.

    Parameters
    ----------
    df:
        Sales data containing product and quantity columns.
    product_col:
        Column identifying the product.
    quantity_col:
        Column representing quantity sold.
    top_n:
        Number of top products to return.

    Returns
    -------
    pandas.DataFrame
        DataFrame with ``product_col`` and ``total_quantity`` columns
        sorted in descending order of quantity.
    """
    for col in (product_col, quantity_col):
        if col not in df.columns:
            raise KeyError(f"{col!r} not in DataFrame")
    if top_n <= 0:
        raise ValueError("top_n must be positive")

    aggregated = (
        df.groupby(product_col)[quantity_col]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .rename("total_quantity")
        .reset_index()
    )
    return aggregated


def top_selling_from_zip(
    zip_path: str | Path,
    *,
    sales_file: str,
    product_col: str,
    quantity_col: str,
    top_n: int = 10,
) -> pd.DataFrame:
    """Load sales data from ``zip_path`` and compute top products.

    This is a convenience wrapper around :func:`load_datasets` and
    :func:`top_selling_products`.
    """
    datasets = load_datasets(zip_path, files=[sales_file])
    key = Path(sales_file).stem
    if key not in datasets:
        raise FileNotFoundError(f"{sales_file!r} not found in {zip_path!r}")
    return top_selling_products(
        datasets[key],
        product_col,
        quantity_col,
        top_n=top_n,
    )
