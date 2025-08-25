from __future__ import annotations

"""Utilities for working with the bundled ZIP datasets.

This module exposes :func:`load_datasets` which reads all CSV files from a
zip archive into :class:`pandas.DataFrame` objects.  The function is
lightweight and does not make assumptions about the structure of the CSV
files, making it suitable for loading the sample datasets included with the
project as well as synthetic datasets used in tests.
"""

from pathlib import Path
import zipfile
from typing import Iterable, Mapping

import pandas as pd


def load_datasets(
    zip_path: str | Path,
    *,
    files: Iterable[str] | None = None,
) -> Mapping[str, pd.DataFrame]:
    """Load CSV files from ``zip_path``.

    Parameters
    ----------
    zip_path:
        Path to a zip archive containing one or more CSV files.
    files:
        Optional iterable of file names to load from the archive.  If ``None``
        all CSV files are loaded.  Names are matched against the base name of
        each file inside the archive (e.g. ``"sales.csv"``).

    Returns
    -------
    dict[str, pandas.DataFrame]
        Mapping of file stem (e.g. ``"sales"``) to its corresponding
        :class:`~pandas.DataFrame`.
    """
    path = Path(zip_path)
    if not path.is_file():  # pragma: no cover - sanity check
        raise FileNotFoundError(f"{zip_path!r} does not exist")

    with zipfile.ZipFile(path) as zf:
        members = [name for name in zf.namelist() if name.lower().endswith('.csv')]
        if files is not None:
            wanted = {Path(f).name for f in files}
            members = [m for m in members if Path(m).name in wanted]

        data: dict[str, pd.DataFrame] = {}
        for member in members:
            with zf.open(member) as fp:
                df = pd.read_csv(fp)
            data[Path(member).stem] = df

    return data


def load_sample_datasets(zip_path: str | Path) -> Mapping[str, pd.DataFrame]:
    """Convenience wrapper around :func:`load_datasets` for sample archives.

    The sample data distributed with this project lives in zip archives.  This
    helper simply delegates to :func:`load_datasets` but documents the intent
    more clearly and provides a single import point for users analysing the
    supplied sample data.

    Parameters
    ----------
    zip_path:
        Path to the sample dataset zip archive.

    Returns
    -------
    Mapping[str, pandas.DataFrame]
        DataFrames for every CSV file contained within ``zip_path``.
    """

    return load_datasets(zip_path)
