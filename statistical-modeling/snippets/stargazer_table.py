"""
Stargazer side-by-side regression-table template.

Pattern from python-for-data-analysis/class-13-framework-for-prediction
and ceu-coding-2/session-1-20251109/intro_to_regression.ipynb.

Renders well in Jupyter (HTML) and to LaTeX via `.render_latex()`.
"""

from __future__ import annotations

import statsmodels.formula.api as smf
from stargazer.stargazer import LineLocation, Stargazer


def example_table(df):
    """Build a 4-column comparison table for hotel-price-style data."""
    reg1 = smf.ols("price ~ distance",                         data=df).fit(cov_type="HC3")
    reg2 = smf.ols("price ~ distance + rating",                data=df).fit(cov_type="HC3")
    reg3 = smf.ols("price ~ distance + rating + C(stars)",     data=df).fit(cov_type="HC3")
    reg4 = smf.ols("np.log(price) ~ np.log(distance) + rating", data=df).fit(cov_type="HC3")
    models = [reg1, reg2, reg3, reg4]

    sg = Stargazer(models)
    sg.title("Hotel price models — robust SE (HC3)")
    sg.custom_columns(
        ["Linear", "+ Rating", "+ Stars", "Log-log"],
        [1, 1, 1, 1],
    )
    sg.show_model_numbers(False)

    sg.rename_covariates({
        "distance":         "Distance to centre (km)",
        "rating":           "User rating",
        "np.log(distance)": "log(distance)",
    })

    sg.covariate_order([
        "Intercept",
        "distance", "np.log(distance)",
        "rating",
    ])

    bic_row  = [f"{m.bic:.0f}" for m in models]
    n_row    = [f"{int(m.nobs):,}" for m in models]
    sg.add_line("BIC", bic_row, location=LineLocation.FOOTER_BOTTOM)
    sg.add_line("N",   n_row,   location=LineLocation.FOOTER_BOTTOM)

    sg.show_degrees_of_freedom(False)
    sg.significance_levels([0.10, 0.05, 0.01])

    return sg


def render_latex(sg: Stargazer, path: str) -> None:
    with open(path, "w") as fh:
        fh.write(sg.render_latex())
