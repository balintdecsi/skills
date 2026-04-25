"""
ResultCollector — running leaderboard for model comparison.

Adapted from the pattern in ceu-ml/notebooks/class5_bike_share_demand.ipynb
(CEU MSBA "Data Science 3: Machine Learning Concepts and Tools").

Drop into any modelling notebook to keep a styled, sortable leaderboard
of train / test scores with automatic improvement-over-baseline.

Usage:
    results = ResultCollector(metric_name="RMSLE", lower_is_better=True)
    results.add("baseline (mean)", train=base_train, test=base_test)
    results.add("xgboost",         train=xgb_train,  test=xgb_test)
    results.show()        # styled DataFrame in a notebook
    results.as_frame()    # raw DataFrame (for saving / programmatic use)
"""

from __future__ import annotations

import pandas as pd


class ResultCollector:
    def __init__(self, metric_name: str = "score", lower_is_better: bool = True):
        self.metric_name = metric_name
        self.lower_is_better = lower_is_better
        self._results: dict[str, dict[str, float]] = {}

    def add(self, name: str, train: float, test: float) -> "ResultCollector":
        """Add or overwrite a model's row. Returns self for chaining."""
        self._results[name] = {
            f"Train {self.metric_name}": float(train),
            f"Test {self.metric_name}":  float(test),
            "Gap": float(test) - float(train),
        }
        return self

    def as_frame(self) -> pd.DataFrame:
        df = pd.DataFrame(self._results).T
        if df.empty:
            return df

        test_col = f"Test {self.metric_name}"
        baseline = df[test_col].iloc[0]

        if self.lower_is_better:
            df["Improvement vs baseline"] = (
                (baseline - df[test_col]) / baseline * 100
            ).round(1).astype(str) + "%"
        else:
            df["Improvement vs baseline"] = (
                (df[test_col] - baseline) / baseline * 100
            ).round(1).astype(str) + "%"
        return df

    def show(self):
        """Styled view for notebooks. Returns a Styler if pandas styling is available."""
        df = self.as_frame()
        if df.empty:
            return df
        test_col = f"Test {self.metric_name}"
        train_col = f"Train {self.metric_name}"
        try:
            cmap = "RdYlGn_r" if self.lower_is_better else "RdYlGn"
            return (
                df.style
                  .format("{:.4f}", subset=[train_col, test_col, "Gap"])
                  .background_gradient(cmap=cmap, subset=[test_col], axis=None)
            )
        except Exception:
            return df

    def best(self) -> str:
        df = self.as_frame()
        test_col = f"Test {self.metric_name}"
        return df[test_col].idxmin() if self.lower_is_better else df[test_col].idxmax()

    def __repr__(self) -> str:
        return repr(self.as_frame())
