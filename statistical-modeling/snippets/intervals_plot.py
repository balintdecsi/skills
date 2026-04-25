"""
Plot fitted line + confidence band + prediction band for a statsmodels OLS.

Distinguishes the two intervals visually. Pattern from
python-for-data-analysis/class-09-generalizing-regression-results.

The single most common reporting mistake is to draw a confidence band and
label it as a prediction interval (or vice versa). This helper makes both
explicit.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_with_intervals(reg, df, x_col: str, y_col: str,
                        alpha: float = 0.05,
                        n_grid: int = 200,
                        ax=None):
    """
    Plot raw points, fitted line, confidence band and prediction band.

    `reg` must be a fitted statsmodels model produced from `df` containing
    `x_col` and `y_col`. Other regressors in the model are held at their
    column mean / mode for the prediction grid.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 5))

    grid = pd.DataFrame({
        x_col: np.linspace(df[x_col].min(), df[x_col].max(), n_grid),
    })
    for col in reg.model.exog_names:
        if col == "Intercept" or col == x_col or col.startswith(x_col + ":"):
            continue
        if col in df.columns:
            v = df[col]
            grid[col] = v.mean() if pd.api.types.is_numeric_dtype(v) else v.mode().iloc[0]

    pred = reg.get_prediction(grid).summary_frame(alpha=alpha)

    ax.scatter(df[x_col], df[y_col], s=12, alpha=0.4, label="data")
    ax.plot(grid[x_col], pred["mean"], lw=2, label="fitted")
    ax.fill_between(grid[x_col], pred["mean_ci_lower"], pred["mean_ci_upper"],
                    alpha=0.30, label=f"{int((1-alpha)*100)}% CI (mean)")
    ax.fill_between(grid[x_col], pred["obs_ci_lower"], pred["obs_ci_upper"],
                    alpha=0.12, label=f"{int((1-alpha)*100)}% PI (observation)")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.legend(loc="best")
    ax.set_title(f"{y_col} ~ {x_col}: fit + CI + PI")
    return ax
