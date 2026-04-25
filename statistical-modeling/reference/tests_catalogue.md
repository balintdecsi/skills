# Hypothesis Tests Catalogue (Python)

One-line recipes for the tests that actually come up. Inspired by patterns across `python-for-data-analysis` and `Data-Analysis-3` (CEU MSBA).

For each test, **always report**: test name, statistic, p-value, sample size, and an effect-size measure or a CI. A bare p-value is not a result.

---

## Single-coefficient significance (regression)

Already in `summary()` of any `statsmodels` fit:

```python
reg = smf.ols("y ~ x1 + x2", data=df).fit(cov_type="HC3")
print(reg.tvalues)    # t-statistics
print(reg.pvalues)    # p-values
print(reg.conf_int()) # 95% CIs (use alpha=0.01 for 99%)
```

---

## Joint significance of multiple coefficients (Wald F-test)

```python
reg.f_test("x1 = 0, x2 = 0")
# Or test linear combinations:
reg.f_test("x1 - x2 = 0")
```

---

## Nested-model comparison (likelihood-ratio for OLS / GLM)

```python
from statsmodels.stats.anova import anova_lm

small = smf.ols("y ~ x1",        data=df).fit()
big   = smf.ols("y ~ x1 + x2*x3", data=df).fit()
print(anova_lm(small, big))
# Significant F-stat → the bigger model adds explanatory power.
```

For non-nested: compare `aic`, `bic`, `rsquared_adj` on the SAME sample.

---

## Two means (independent groups)

```python
from scipy.stats import ttest_ind, mannwhitneyu

t, p = ttest_ind(group_a, group_b, equal_var=False)   # Welch's by default
u, p = mannwhitneyu(group_a, group_b, alternative="two-sided")  # non-parametric
```

Always pair with **Cohen's d**:

```python
import numpy as np
def cohens_d(a, b):
    pooled = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
    return (a.mean() - b.mean()) / pooled
```

---

## Two means (paired)

```python
from scipy.stats import ttest_rel, wilcoxon

t, p = ttest_rel(before, after)
w, p = wilcoxon(before, after)   # non-parametric
```

This is the test to use on **per-fold CV scores** when comparing two ML models — see `ml-modeling/snippets/paired_cv_test.py`.

---

## Two proportions

```python
from statsmodels.stats.proportion import proportions_ztest, proportion_confint

count = [successes_a, successes_b]
nobs  = [n_a,        n_b]
z, p = proportions_ztest(count, nobs)

# Per-group 95% CIs (Wilson):
ci_a = proportion_confint(successes_a, n_a, method="wilson")
ci_b = proportion_confint(successes_b, n_b, method="wilson")
```

---

## Categorical association (chi-square / Fisher's exact)

```python
from scipy.stats import chi2_contingency, fisher_exact

table = pd.crosstab(df["region"], df["churned"])
chi2, p, dof, expected = chi2_contingency(table)

# 2x2 with small counts — exact:
oddsratio, p = fisher_exact(table.values)
```

---

## Heteroscedasticity (residual non-constant variance)

```python
from statsmodels.stats.diagnostic import het_breuschpagan, het_white

bp_stat, bp_p, _, _ = het_breuschpagan(reg.resid, reg.model.exog)
w_stat,  w_p,  _, _ = het_white(       reg.resid, reg.model.exog)
```

If significant → use `cov_type="HC3"` (or any `HCx`) when fitting. Don't refit a different model — the point estimates are still unbiased; only the SE need fixing.

---

## Autocorrelation (residuals correlated over time)

```python
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.diagnostic import acorr_ljungbox

print("DW:", durbin_watson(reg.resid))   # close to 2 = no autocorrelation
print(acorr_ljungbox(reg.resid, lags=[1, 5, 10], return_df=True))
```

If significant → `cov_type="HAC", cov_kwds={"maxlags": L}` for OLS, or move to a time-series model.

---

## Normality of residuals

```python
from scipy.stats import shapiro, jarque_bera

stat, p = shapiro(reg.resid)             # small samples
stat, p = jarque_bera(reg.resid)[:2]     # large samples
```

Honestly, plot a Q-Q plot — `sm.qqplot(reg.resid, line="45")` — visual check is often more useful than a p-value here.

---

## Mediation / moderation

Out of scope for one-liners; use `pingouin.mediation_analysis` or `statsmodels` interactions (`y ~ x * z`) and interpret the interaction term carefully.

---

## Multiple testing

If you run >1 test:

```python
from statsmodels.stats.multitest import multipletests

reject, pvals_corr, _, _ = multipletests(pvals, method="holm")  # or "fdr_bh"
```

Especially important when scanning many coefficients or many subgroup tests.

---

## Statistical vs practical significance — the reminder

A test answering "is the effect ≠ 0?" is not the same as "is the effect big enough to matter?". Always pair every test with:

- An **effect size** (Cohen's d, odds ratio, R², etc.).
- The estimate **in the units stakeholders use** ($, percentage points, customers).
- A **CI**, not just a p-value.

If `n` is huge, everything is "significant". If `n` is tiny, nothing is. Significance ≠ importance.
