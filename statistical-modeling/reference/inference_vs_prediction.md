# Inference vs. Prediction — Which Skill Do I Need?

A quick decision guide between this `statistical-modeling` skill and the companion `ml-modeling` skill.

---

## Two different goals, two different toolboxes

| Question | Goal | Skill | Stack |
|---|---|---|---|
| "How big is the effect of X on Y, and are we sure?" | **Inference** | `statistical-modeling` | `statsmodels`, `stargazer`, robust SE, CIs, hypothesis tests |
| "How accurately can I predict Y for new observations?" | **Prediction** | `ml-modeling` | `scikit-learn`, Pipeline, CV, leaderboard, held-out test set |
| "Both, on the same project" | Use **both**, in this order | start with this one for inference, then `ml-modeling` for prediction | sequential, separate notebooks if possible |

---

## Symptoms you're in inference territory

- The deliverable is a **table of coefficients** for a stakeholder.
- You care about which variables matter, not raw accuracy.
- You need **confidence / prediction intervals**.
- You'll be asked "is this effect statistically significant?" in the meeting.
- The `R²` is a number you'll report, not a number you'll improve.

→ Use `statsmodels` (`smf.ols`, `smf.logit`), report with `stargazer`, plot fitted values with confidence and prediction bands.

---

## Symptoms you're in prediction territory

- The deliverable is a **score / probability / class** for new rows.
- You'll be evaluated on accuracy / AUC / RMSE on a held-out set.
- You'll try multiple algorithms and pick the best.
- Coefficients (if they exist) are not the point.
- You'll deploy something — even a notebook handover counts.

→ Use `scikit-learn` Pipelines, cross-validate, keep a leaderboard, never touch the test set twice.

---

## Where the two skills overlap

### Comparing models

- **Two nested OLS specifications:** F-test (`statsmodels.stats.anova.anova_lm`) — *this skill*.
- **Two non-nested OLS specifications:** AIC / BIC / adj-R² — *this skill*.
- **Two predictive models on the same CV folds:** paired t-test / Wilcoxon on per-fold scores — *the `ml-modeling` skill*.

### Confidence vs prediction intervals

- For a **fitted regression**, both come from `statsmodels` — *this skill*.
- For a **predictive ML model**, use bootstrap CI on the held-out metric — *the `ml-modeling` skill*.

### "Is the difference significant?"

The cleanest mental rule:

- If you're comparing **estimated parameters of one model**, you're in inference → this skill.
- If you're comparing **out-of-sample performance of two models**, you're in prediction → ML-modeling skill.
- A single numeric "score" with no CI / SE is **never** a reportable finding in either world.

---

## Common mistake: using the wrong toolbox

| Mistake | Symptom | Fix |
|---|---|---|
| Using `statsmodels` p-values to "prove the model generalises" | The training-data fit is being treated as evidence of predictive accuracy | Add a held-out test set or CV |
| Using `sklearn.LogisticRegression.coef_` as if they were `statsmodels` coefficients with SE | Reporting odds ratios with no uncertainty | Switch to `smf.logit` for inference, or bootstrap the sklearn fit |
| Reporting `R² = 0.92` from `statsmodels` and calling it "great prediction" | No held-out evaluation | Switch to predictive workflow, evaluate on test set |
| Comparing two ML models with a t-test on test-set accuracy across two seeds | Not enough variation captured | Use 10-fold paired CV scores instead |

---

## TL;DR

**Inference asks "what is the truth about the population?". Prediction asks "what is the next observation?".**

They use different machinery, different uncertainty quantification, and different reporting. Pick the right one for the question being asked, and don't pretend one answers the other.
