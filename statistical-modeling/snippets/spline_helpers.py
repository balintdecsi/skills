"""
Linear spline helpers for use with statsmodels formulas.

Source: python-for-data-analysis/class-09-generalizing-regression-results/utils.py
(CEU MSBA, originally written for the Békés–Kézdi data analysis style).

Use inside an `smf.ols` formula:

    from spline_helpers import lspline
    smf.ols("price ~ lspline(distance, [1.0, 3.0])", data=df).fit()
"""

from __future__ import annotations

import copy
from typing import List

import numpy as np
import pandas as pd


def knot_ceil(vector: np.ndarray, knot: float) -> np.ndarray:
    """Cap each element at `knot`."""
    out = copy.deepcopy(vector)
    out[out > knot] = knot
    return out


def lspline(series: pd.Series, knots: List[float]) -> np.ndarray:
    """
    Linear-spline basis matrix. Each column is the increment within one segment.

    Example:
        >>> lspline(pd.Series([1, 2, 3, 4, 5]), [2, 4])
        array([[1, 0, 0],
               [2, 0, 0],
               [2, 1, 0],
               [2, 2, 0],
               [2, 2, 1]])
    """
    if not isinstance(knots, list):
        knots = [knots]
    design = None
    vector = series.values.astype(float)

    for i, k in enumerate(knots):
        if i == 0:
            column = knot_ceil(vector, k)
        else:
            column = knot_ceil(vector, k - knots[i - 1])
        design = column if design is None else np.column_stack((design, column))
        vector = vector - column

    design = np.column_stack((design, vector))
    return design
