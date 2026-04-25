---
name: statistical-modeling
description: Best-practice suggestions for statistical / inferential modelling in Python — OLS and logistic regression with statsmodels, robust standard errors, side-by-side regression tables with stargazer, confidence and prediction intervals, hypothesis tests, and significance reporting. Use when interpreting coefficients, building explanatory regressions, comparing nested models, reporting confidence/prediction intervals, or testing whether an effect is statistically significant.
---

# Statistical Modelling Best Practices

These are **suggestions**, not absolute rules. The user is industry-experienced but wants to get sharper at the more academic side of modelling — confidence intervals, prediction intervals, significance tests, and clean regression-table reporting. The patterns here cover that gap.

The patterns are inspired by these CEU MSBA / Békés–Kézdi-style course repositories the user worked with:

- `python-for-data-analysis` — especially `class-09-generalizing-regression-results`, `class-13-framework-for-prediction`, and onwards. Heavy use of `statsmodels` + `stargazer`.
- `ceu-coding-2` — `intro_to_regression.ipynb` (`smf.ols`, robust SE, `stargazer` side-by-side tables, linear splines).
- `da_data_repo` (Békés–Kézdi *Data Analysis for Business, Economics, and Policy* datasets — upstream <https://github.com/gabors-data-analysis>).
- `Data-Analysis-3` for the link to predictive evaluation.

This skill is the **inferential / explanatory counterpart** to the `ml-modeling` skill. Use this when the question is *"how big is the effect, and are we sure?"*. Use `ml-modeling` when the question is *"how accurately can we predict?"*. They overlap on significance testing of model differences — see [reference/inference_vs_prediction.md](reference/inference_vs_prediction.md).

## When to Use

Auto-apply when the task involves:

- Estimating and *interpreting* regression coefficients (not just predicting).
- Confidence intervals on parameters or fitted values.
- Prediction intervals for individual observations.
- Side-by-side comparison of nested or competing regression specifications.
- Hypothesis tests (t-test, F-test for joint significance, Wald, likelihood ratio).
- Robust / heteroscedasticity-consistent standard errors.
- Linear splines, log-log specifications, fixed effects on cross-sections.
- Reading a colleague's regression notebook and asking "is this defensible?".

## Default Stack

- `statsmodels` — `smf.ols`, `smf.logit`, `sm.OLS`. Use the formula API (`smf`) by default; falls back to `sm.OLS` when you need a design matrix.
- `stargazer` — side-by-side regression tables (the package used across `python-for-data-analysis` and `ceu-coding-2`).
- `scipy.stats` — t-tests, F-tests, Wilcoxon, etc. when you need raw tests.
- `pandas`, `numpy`, `matplotlib`, `seaborn` for the rest.

For **predictive** workflows (cross-validation, held-out test sets, leaderboards) → switch to the `ml-modeling` skill and use `scikit-learn`.

## Core Principles

1. **Always report standard errors and confidence intervals**, never just point estimates.
2. **Use robust standard errors by default** for cross-sectional data — `cov_type="HC3"` (or `HC0`/`HC1` to match older textbooks). Don't trust homoscedasticity unless you've checked.
3. **Distinguish confidence interval from prediction interval.** CI is uncertainty around the *expected value*; PI is uncertainty around an *individual observation* and is wider.
4. **Stargazer tables make comparisons honest.** When showing >1 specification, put them side by side with the same dependent variable.
5. **Test significance explicitly** — don't infer from "the coefficient is large". A coefficient is *significantly different from zero* only when the test says so.
6. **Distinguish statistical from practical significance.** A `p < 0.001` effect of $0.02 may be irrelevant. Always report effect size in the units stakeholders understand.
7. **Pre-specify the model.** If you ran 50 specifications and report the 3 with the smallest p-values, you have nothing.

## OLS — the workhorse

```python
import statsmodels.formula.api as smf

reg = smf.ols("price ~ distance + rating", data=hotels).fit(cov_type="HC3")
print(reg.summary())

# Coefficients with 95% CI
print(reg.params)
print(reg.conf_int(alpha=0.05))

# Coefficient-level test
print("p-values:", reg.pvalues)

# Joint test of multiple coefficients (F-test)
print(reg.f_test("distance = 0, rating = 0"))
```

Common specification choices:

| Goal | Specification |
|---|---|
| Linear | `y ~ x` |
| Log-level | `np.log(y) ~ x` (interpret coef as ~% change in y per unit x) |
| Level-log | `y ~ np.log(x)` (interpret coef as change in y per 1% change in x ≈ coef/100) |
| Log-log (elasticity) | `np.log(y) ~ np.log(x)` (coef = elasticity directly) |
| Polynomial | `y ~ x + I(x**2) + I(x**3)` |
| Linear spline | `y ~ lspline(x, [knot1, knot2])` (helper from `python-for-data-analysis`) |
| Categorical | `y ~ C(category)` |
| Interaction | `y ~ x * z` (includes `x`, `z`, `x:z`) |

The `lspline` / `knot_ceil` helpers live in [snippets/spline_helpers.py](snippets/spline_helpers.py), copied from `python-for-data-analysis/class-09`.

## Logistic Regression (when the dependent is binary)

```python
logit = smf.logit("default ~ income + age + C(region)", data=df).fit(cov_type="HC3")
print(logit.summary())

# Odds ratios with 95% CI
import numpy as np
ors = np.exp(logit.params)
ci  = np.exp(logit.conf_int())
print(pd.concat([ors.rename("OR"), ci], axis=1))
```

For pure prediction with logistic regression at scale, switch to `sklearn.linear_model.LogisticRegression` (`ml-modeling` skill).

## Side-by-side Tables with Stargazer

The pattern from `python-for-data-analysis/class-13`:

```python
from stargazer.stargazer import Stargazer

reg1 = smf.ols("price ~ distance", data=hotels).fit(cov_type="HC3")
reg2 = smf.ols("price ~ distance + rating", data=hotels).fit(cov_type="HC3")
reg3 = smf.ols("price ~ distance + rating + C(stars)", data=hotels).fit(cov_type="HC3")

sg = Stargazer([reg1, reg2, reg3])
sg.rename_covariates({"distance": "Distance to centre", "rating": "User rating"})
sg.show_model_numbers(False)
sg.title("Hotel price models")
sg                 # in Jupyter, renders HTML; .render_latex() for LaTeX
```

A worked template lives in [snippets/stargazer_table.py](snippets/stargazer_table.py).

## Confidence vs Prediction Intervals

This trip-up is the single most common one. From `python-for-data-analysis/class-09`:

- **Confidence interval (CI):** uncertainty around the *fitted value* (i.e. `E[Y | X = x]`). Narrow.
- **Prediction interval (PI):** uncertainty around a *single new observation* — adds the residual variance on top. Wider.

```python
pred = reg.get_prediction(new_X)
summary = pred.summary_frame(alpha=0.05)
# columns: mean, mean_se, mean_ci_lower, mean_ci_upper,  ← CI on E[Y|X]
#          obs_ci_lower, obs_ci_upper                    ← PREDICTION interval on Y
```

When plotting fitted values, draw both intervals as differently shaded bands and label them. See [snippets/intervals_plot.py](snippets/intervals_plot.py).

## Hypothesis Tests You'll Actually Use

| Question | Test |
|---|---|
| Is this single coefficient ≠ 0? | t-test (built into `summary()`) |
| Are these k coefficients jointly 0? | F-test: `reg.f_test("a = 0, b = 0")` |
| Is the bigger model actually better than the nested one? | Likelihood-ratio test or compare adj-R²/BIC; for nested OLS use `anova_lm(small, big)` |
| Are two means / two groups different? | `scipy.stats.ttest_ind` (independent) or `ttest_rel` (paired) |
| Same as above but non-normal | `scipy.stats.mannwhitneyu` or `wilcoxon` |
| Are two proportions different? | `statsmodels.stats.proportion.proportions_ztest` or chi-square |
| Is the residual heteroscedastic? | Breusch–Pagan or White: `het_breuschpagan`, `het_white` |
| Is there autocorrelation? | Durbin–Watson (already in `summary()`) or `acorr_ljungbox` |

A code catalogue with one-liners for each lives in [reference/tests_catalogue.md](reference/tests_catalogue.md).

## When You Compare *Models* (not coefficients)

This is the bridge to `ml-modeling`:

- **Nested OLS models (one is a subset of the other):** use F-test via `statsmodels.stats.anova.anova_lm(small, big)`.
- **Non-nested:** compare on adj-R², AIC, BIC. The model with lower AIC/BIC wins; there's no formal test.
- **Predictive ML models on the same CV folds:** use the **paired t-test on per-fold scores** pattern from the `ml-modeling` skill.

## Significance Reporting Etiquette

When reporting an effect, give the reader four things in one sentence:

> The coefficient on `experience` is **0.034 log-points** (95% CI: 0.022–0.046; p < 0.001), implying an additional year of experience is associated with roughly **3.4% higher wages**.

That's: estimate, CI, p-value, plain-English interpretation. **Always include the unit and the practical magnitude.** A p-value alone is not a finding.

## Anti-Patterns to Flag

- Reporting only the point estimate, no SE / CI.
- Using default homoscedastic SE on cross-sectional data without checking residuals.
- Reporting `R² = 0.87` without showing test/holdout performance — high R² on training data is uninformative.
- Picking the "best" specification after looking at p-values across many runs (HARKing / p-hacking).
- Calling a coefficient "significant" without saying at what α and with what test.
- Confusing confidence interval with prediction interval in plots.
- Comparing models by R² alone — penalise complexity (adj-R², BIC) or compare on a held-out set.
- Treating logistic-regression coefficients as probabilities (they're log-odds).

## Code Snippets

In [snippets/](snippets/):

- `spline_helpers.py` — `knot_ceil` and `lspline` from `python-for-data-analysis/class-09` for use inside `smf.ols("y ~ lspline(x, [...])", ...)`.
- `stargazer_table.py` — full stargazer table template with renamed covariates, custom rows, BIC/AIC footer.
- `intervals_plot.py` — fitted line + confidence band + prediction band for OLS, properly labeled.
- `regression_diagnostics.py` — residual plots, heteroscedasticity tests, influence diagnostics in one call.

## Data Sources Used in the Inspiration Courses

Almost all worked examples across `python-for-data-analysis`, `ceu-coding-2`, `Data-Analysis-3`,
`da_data_repo`, and `da_case_studies` come from **Békés & Kézdi, *Data Analysis for Business,
Economics, and Policy*** (Cambridge, 2021). The companion data is openly available and is the
single best collection of cleanly-documented small/medium datasets for inferential modeling practice:

| Resource | What | URL |
|---|---|---|
| Book site (datasets, code in R/Python/Stata, case studies) | Hub for everything | <https://gabors-data-analysis.com/> |
| `da_data_repo` (raw + clean datasets) | Download via OSF or GitHub | <https://osf.io/7epdj/> · <https://github.com/gabors-data-analysis/da_data_repo> |
| `da_case_studies` (chapter notebooks) | End-to-end workflows per chapter | <https://github.com/gabors-data-analysis/da_case_studies> |

Specific datasets you'll keep returning to (all small, all interpretable):

| Dataset | Typical use | Direct URL |
|---|---|---|
| `hotels-europe` (Vienna subset) | OLS on hotel price; log specs; splines; CIs vs PIs | <https://osf.io/r6uqb/> |
| `cps-earnings` (CPS earnings) | Mincer-style log-wage regression, gender gap, robust SE | <https://osf.io/g8p9j/> |
| `wms-management-survey` | Cross-country firm management practices regressions | <https://osf.io/uzpce/> |
| `used-cars` | Hedonic price regression with feature engineering | <https://osf.io/7gvz9/> |
| `share-health` | Logistic regression on health outcomes | <https://osf.io/yhdte/> |
| `bisnode-firms` | Probability prediction (probit/logit), classification thresholds with business loss | <https://osf.io/3qyut/> |
| `football-managers` | Difference-in-differences, event studies | <https://osf.io/r2psv/> |

Other free, well-suited sources for inferential exercises:

| Source | What | URL |
|---|---|---|
| Statsmodels built-ins | `sm.datasets.{anes96, fair, longley, macrodata, statecrime, ...}` for quick OLS/Logit demos | `import statsmodels.api as sm; sm.datasets.longley.load_pandas().data` |
| Seaborn datasets | `tips`, `diamonds`, `mpg`, `penguins` — small enough to teach, big enough to find effects | `import seaborn as sns; sns.load_dataset("diamonds")` |
| OpenML | Tabular datasets with metadata; great for replication exercises | <https://www.openml.org/> |
| World Bank Open Data | Country-year panels for cross-country regressions | <https://data.worldbank.org/> |
| FRED (Federal Reserve Economic Data) | Macro time series for ARIMA / interrupted time-series | <https://fred.stlouisfed.org/> via `pandas_datareader` |

When loading from OSF, the canonical pattern from the `da_*` repos works directly in Python:

```python
import pandas as pd
hotels = pd.read_csv("https://osf.io/r6uqb/download")  # hotels-europe price snapshot
```

## Further Reference

Inspiration repos (check these for full worked examples):

- `python-for-data-analysis` — most relevant chapters: `class-07-simple-ols`, `class-08-complicated-patterns`, `class-09-generalizing-regression-results`, `class-10-multiple-linear-regression`, `class-11-probabilities`, `class-13-framework-for-prediction`, `class-17-probability-and-classification`.
- `ceu-coding-2/session-1-20251109/intro_to_regression.ipynb` — gentle intro with `smf.ols`, robust SE, log-log, splines, stargazer.
- `da_data_repo` (upstream: <https://github.com/gabors-data-analysis>) — companion datasets for the Békés–Kézdi book; `da_case_studies` (<https://github.com/gabors-data-analysis/da_case_studies>) has chapter notebooks.
- `Data-Analysis-3` — connects this to predictive evaluation under business loss.

External:

- Békés & Kézdi, *Data Analysis for Business, Economics, and Policy* (the textbook the `da_*` repos accompany).
- [statsmodels user guide](https://www.statsmodels.org/stable/user-guide.html) — especially "Linear Regression" and "Robust Statistics".
- [Stargazer for Python](https://github.com/StatsReporting/stargazer) — package + examples.

---

*Suggestions, not gospel. When in doubt, **show the standard errors and the practical magnitude**, not just the point estimate and the p-value.*
