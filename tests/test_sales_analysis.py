import os
import sys
import zipfile

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from inventory import top_selling_products, top_selling_from_zip


def _make_zip(path, files):
    with zipfile.ZipFile(path, "w") as zf:
        for name, df in files.items():
            zf.writestr(f"{name}.csv", df.to_csv(index=False))
    return path


def test_top_selling_products():
    df = pd.DataFrame({"product": ["A", "B", "A", "C"], "qty": [10, 5, 3, 20]})
    result = top_selling_products(df, "product", "qty", top_n=2)
    assert list(result["product"]) == ["C", "A"]
    assert list(result["total_quantity"]) == [20, 13]


def test_top_selling_from_zip(tmp_path):
    df = pd.DataFrame({"product": ["A", "B", "A"], "qty": [10, 5, 3]})
    zip_path = _make_zip(tmp_path / "sales.zip", {"sales": df})
    result = top_selling_from_zip(
        zip_path,
        sales_file="sales.csv",
        product_col="product",
        quantity_col="qty",
        top_n=1,
    )
    assert result.iloc[0]["product"] == "A"
    assert result.iloc[0]["total_quantity"] == 13
