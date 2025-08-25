import os
import sys
import zipfile

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from inventory import load_datasets, load_sample_datasets, classify_inventory


def _make_zip(path, files):
    """Helper to create a zip file at *path* from a mapping of name->DataFrame."""
    with zipfile.ZipFile(path, "w") as zf:
        for name, df in files.items():
            zf.writestr(f"{name}.csv", df.to_csv(index=False))
    return path


def test_load_datasets(tmp_path):
    df1 = pd.DataFrame({"a": [1, 2]})
    df2 = pd.DataFrame({"b": ["x", "y"]})
    zip_path = _make_zip(tmp_path / "data.zip", {"first": df1, "second": df2})

    loaded = load_datasets(zip_path)
    assert loaded["first"].equals(df1)
    assert loaded["second"].equals(df2)


def test_classify_with_loaded_data(tmp_path):
    inv_df = pd.DataFrame({"item": list("ABC"), "value": [100, 50, 10]})
    zip_path = _make_zip(tmp_path / "inv.zip", {"inventory": inv_df})

    datasets = load_datasets(zip_path)
    classified = classify_inventory(datasets["inventory"], "value")
    categories = classified.set_index("item")["category"].to_dict()
    assert categories == {"A": "A", "B": "B", "C": "C"}


def test_load_sample_datasets(tmp_path):
    df = pd.DataFrame({"a": [1]})
    zip_path = _make_zip(tmp_path / "sample.zip", {"first": df})

    loaded = load_sample_datasets(zip_path)
    assert loaded["first"].equals(df)
