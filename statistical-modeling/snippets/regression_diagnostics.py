"""
One-call regression diagnostics for a statsmodels OLS fit.

Produces:
    - residuals vs fitted plot
    - Q-Q plot of residuals
    - scale-location plot
    - Cook's distance plot
And prints:
    - Breusch–Pagan and White heteroscedasticity tests
    - Jarque–Bera normality test
    - Durbin–Watson autocorrelation statistic

Inspired by patterns across python-for-data-analysis and ceu-coding-2.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan, het_white
from statsmodels.stats.stattools import durbin_watson, jarque_bera


def diagnose(reg) -> dict:
    """Run a standard battery of diagnostics on a fitted statsmodels OLS."""
    fitted = reg.fittedvalues
    resid = reg.resid
    influence = reg.get_influence()
    cooks = influence.cooks_distance[0]

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    fig.suptitle("Regression diagnostics")

    axes[0, 0].scatter(fitted, resid, s=12, alpha=0.5)
    axes[0, 0].axhline(0, color="red", lw=1)
    axes[0, 0].set(xlabel="Fitted", ylabel="Residuals", title="Residuals vs Fitted")

    sm.qqplot(resid, line="45", fit=True, ax=axes[0, 1])
    axes[0, 1].set_title("Normal Q-Q")

    std_resid = np.sqrt(np.abs(resid / resid.std(ddof=1)))
    axes[1, 0].scatter(fitted, std_resid, s=12, alpha=0.5)
    axes[1, 0].set(xlabel="Fitted", ylabel="√|standardised residuals|",
                   title="Scale-Location")

    axes[1, 1].stem(np.arange(len(cooks)), cooks, markerfmt=" ", basefmt=" ")
    axes[1, 1].set(xlabel="Observation", ylabel="Cook's distance",
                   title="Influence (Cook's D)")
    plt.tight_layout()

    bp_stat, bp_p, _, _ = het_breuschpagan(resid, reg.model.exog)
    w_stat,  w_p,  _, _ = het_white(       resid, reg.model.exog)
    jb_stat, jb_p, skew, kurt = jarque_bera(resid)
    dw = durbin_watson(resid)

    print(f"Breusch–Pagan  : stat={bp_stat:.3f}  p={bp_p:.4f}")
    print(f"White          : stat={w_stat:.3f}  p={w_p:.4f}")
    print(f"Jarque–Bera    : stat={jb_stat:.3f}  p={jb_p:.4f}  skew={skew:.2f}  kurt={kurt:.2f}")
    print(f"Durbin–Watson  : {dw:.3f}   (≈2 → no autocorrelation)")

    return {
        "bp_p": float(bp_p),
        "white_p": float(w_p),
        "jarque_bera_p": float(jb_p),
        "dw": float(dw),
        "max_cooks": float(np.max(cooks)),
    }
