---
name: ml-modeling
description: Best-practice suggestions for predictive ML modelling with scikit-learn — Pipelines, ColumnTransformer, cross-validation, hyperparameter search, honest train/test evaluation, model leaderboards, and threshold/loss-based decisions. Use when building, comparing or reviewing supervised ML models (regression or classification) in Python notebooks or scripts.
---

# ML Modelling Best Practices (scikit-learn flavoured)

These are **suggestions**, not absolute rules — the user is an industry-experienced developer and prefers pragmatic patterns that resonated across several CEU MSBA course repos. Adapt freely to context.

The patterns below are inspired by these repositories the user worked with:

- **Primary inspiration (the user resonated most):**
  - `ceu-ml` — *Data Science 3: Machine Learning Concepts and Tools* (CEU MSBA). The `ResultCollector` model-comparison pattern below comes straight from this course.
  - `Data-Analysis-3` (`zarizachow/Data-Analysis-3`) — `StratifiedKFold` cross-validation + business-loss-function thresholding for classification.
- **Lightly related (data/AI engineering context only):** `ceu-ai-engineering-class`, `de-3`, `ceu-modern-data-platforms`.
- **More academic, but the user wants to get better at them — use idioms from these too:** `ceu-coding-2`, `python-for-data-analysis`, `da_data_repo` (Békés–Kézdi). For statistical modelling specifically (OLS, confidence intervals, significance), see the companion **`statistical-modeling`** skill.

## When to Use

Auto-apply when the task involves:

- Building or refactoring sklearn / xgboost / lightgbm / catboost models.
- Cross-validation, hyperparameter tuning, train/test splitting.
- Comparing multiple candidate models on a held-out set.
- Choosing a classification threshold for a real business decision.
- Reviewing a colleague's modelling notebook.

For pure inference / explanation work (OLS coefficient interpretation, confidence intervals, hypothesis tests), reach for the **`statistical-modeling`** skill instead — they're complementary.

## Default Stack (industry-standard, what the inspiration repos use)

- `scikit-learn` for everything that fits (Pipeline, ColumnTransformer, model_selection, metrics).
- `xgboost` / `lightgbm` for tabular boosting baselines.
- `pandas` + `numpy` for data wrangling.
- `matplotlib` + `seaborn` for plots.
- `optuna` *only* when sklearn's `GridSearchCV` / `RandomizedSearchCV` is genuinely too slow.
- For experiment tracking: a plain DataFrame leaderboard is often enough (see `ResultCollector` below). Reach for MLflow / W&B when you have many runs across sessions.

Keep the stack boring. Sometimes a `print(score)` in a notebook cell beats wiring a tracker.

## Core Principles

1. **Always have a baseline.** Predict the mean / majority class first — every model must beat it.
2. **Pipeline everything.** No fitting transformers on the full dataset before the split. Fit-transform leaks are silent and devastating.
3. **One held-out test set, touched once.** All model selection happens in CV on the train set.
4. **Same split, same metric, same test set** for every candidate — fair comparison only.
5. **Track results in a leaderboard** as you go. The `ResultCollector` pattern below makes this a one-liner.
6. **Set a `random_state`.** Reproducibility is free.
7. **Optimize the metric the business cares about**, not just the one easiest to compute. For classification, that often means a custom loss + tuned threshold, not raw accuracy.
8. **Sanity-check generalisation.** When in doubt, run a paired statistical test on per-fold CV scores before declaring "Model B beats Model A" (see [reference/significance.md](reference/significance.md)).

## The Workflow

When asked to build a predictive model, follow this skeleton:

```
1. Frame:    What are we predicting? What metric matters?
2. Split:    Train / test (and time-aware if temporal data!).
3. Baseline: Mean / majority. Beat this or stop.
4. Pipeline: ColumnTransformer + estimator. No leakage possible.
5. Cross-validate the train set with a fair CV scheme.
6. Add candidates one at a time, log to leaderboard.
7. Tune the best 1-2 with GridSearchCV / RandomizedSearchCV.
8. Decide a threshold (classification) using a business loss function.
9. Final fit on full train, evaluate ONCE on held-out test.
10. Report: leaderboard, key plots, confusion matrix, calibration if relevant.
```

For details on each step see [reference/workflow.md](reference/workflow.md). For ready-to-paste code see [snippets/](snippets/).

## The Pipeline Pattern (no leakage, no exceptions)

```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

numeric = ["age", "income", "tenure"]
categorical = ["region", "plan"]

preprocess = ColumnTransformer([
    ("num", Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ]), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
])

pipe = Pipeline([
    ("prep", preprocess),
    ("model", LogisticRegression(max_iter=1000, random_state=42)),
])
pipe.fit(X_train, y_train)
```

**Why this matters:** when you `cross_val_score(pipe, X_train, y_train, ...)`, sklearn re-fits the preprocessor inside each fold automatically. No data leakage from the validation fold into scaling statistics. This is non-negotiable.

## Model Comparison: the `ResultCollector` Pattern

Adapted from `ceu-ml/notebooks/class5_bike_share_demand.ipynb`. Drop into any modelling notebook to keep a running leaderboard. The full class lives at [snippets/result_collector.py](snippets/result_collector.py).

```python
from snippets.result_collector import ResultCollector
results = ResultCollector(metric_name="RMSLE", lower_is_better=True)

results.add("baseline (mean)", train=baseline_train, test=baseline_test)
results.add("linear (FE)",     train=lin_train,      test=lin_test)
results.add("xgboost",         train=xgb_train,      test=xgb_test)

results.show()   # styled DataFrame: train, test, gap, % improvement over baseline
```

A simple `print(pd.DataFrame(rows))` is often enough — don't over-engineer. The point is: **every model lands in the same table, with the same metric, sorted the same way.**

## Cross-Validation Cheatsheet

| Situation | Use |
|---|---|
| iid regression / classification | `KFold(shuffle=True, random_state=42)` |
| imbalanced classification | `StratifiedKFold(...)` (the `Data-Analysis-3` default) |
| grouped data (same user across rows) | `GroupKFold` |
| time-series | `TimeSeriesSplit` — never shuffle time! |
| nested model selection | inner CV for tuning, outer CV for honest score |

Default to `n_splits=5` (good bias-variance trade-off, fast). Use `n_splits=10` only if folds are very small.

## Hyperparameter Search

Order of preference:

1. **Manual sweep over 3–5 sensible values** in a loop. Often enough, fully transparent.
2. **`GridSearchCV`** when the grid is small (< 100 combinations).
3. **`RandomizedSearchCV`** when the search space is wide.
4. **`optuna`** when the above are too slow or you need conditional spaces.

Always wire the search into the pipeline (`pipe__model__C`, `pipe__prep__num__scale__with_mean`) so preprocessing is tuned along with the estimator.

## Classification Thresholds & Business Loss

Don't default to 0.5 if the costs are asymmetric. Pattern from `Data-Analysis-3/Assignment-2`:

```python
# False negatives cost 4x false positives.
def expected_loss(y_true, proba, threshold, fn_cost=4, fp_cost=1):
    pred = (proba >= threshold).astype(int)
    fn = ((pred == 0) & (y_true == 1)).sum()
    fp = ((pred == 1) & (y_true == 0)).sum()
    return fn * fn_cost + fp * fp_cost

# Find the threshold that minimises expected loss on each CV fold,
# average them — that's your operating threshold.
```

See [snippets/threshold_optimization.py](snippets/threshold_optimization.py) for the full per-fold-then-average pattern.

## Are the Differences Significant?

When comparing two models, **don't trust a single test-set number** if the gap is small relative to noise. Use:

- **Paired t-test or Wilcoxon signed-rank** on per-fold CV scores (regression or classification).
- **McNemar's test** on the disagreements between two classifiers on the same test set.
- **Bootstrap CI** on the held-out metric for a single model.

Code and decision rules in [reference/significance.md](reference/significance.md). For the full statistical-inference toolkit (OLS coefficients, confidence intervals on coefficients, prediction intervals), see the **`statistical-modeling`** skill.

## Notebook Hygiene

- Set seeds at the top: `np.random.seed(42)`, `random_state=42` everywhere.
- Print shapes after every split / transform — catches silent bugs.
- One `Pipeline` per model, named clearly (`pipe_xgb`, `pipe_logit_l2`).
- Plot calibration curves and confusion matrices in classification work — accuracy alone hides a lot.
- "Restart & Run All" must succeed before you commit.

## Anti-Patterns to Flag in Reviews

- `StandardScaler().fit(X)` *before* `train_test_split` — leakage.
- Imputing with the full-data mean before CV — leakage.
- Comparing models with different CV splits or different metrics.
- Picking a threshold on the test set after looking at the test scores.
- Reporting a single test-set number without any uncertainty estimate when models are close.
- `accuracy_score` on a 95/5 imbalanced dataset.
- One mega-cell that does load + preprocess + fit + plot — split it.
- Re-using the test set for "one more tweak". The test set is sacred.

## Code Snippets

In [snippets/](snippets/):

- `result_collector.py` — the leaderboard helper from `ceu-ml`.
- `pipeline_template.py` — full ColumnTransformer + Pipeline + GridSearchCV scaffold for a tabular problem.
- `cv_compare_models.py` — fair `cross_val_score` comparison loop with mean ± std per model.
- `threshold_optimization.py` — find the loss-minimising threshold per CV fold and average.
- `paired_cv_test.py` — paired t-test / Wilcoxon on CV scores; wraps the "is the difference significant?" decision.

## Data Sources Used in the Inspiration Courses (good for ML practice)

The inspiration repos hit a few canonical datasets repeatedly. They're solid defaults when
prototyping a new modelling pattern or wanting a reproducible benchmark:

| Dataset | Task | Used in | URL |
|---|---|---|---|
| Kaggle Bike Sharing Demand | Regression (count target) — the `ceu-ml` flagship example | `ceu-ml/notebooks/class5_bike_share_demand.ipynb` | <https://www.kaggle.com/c/bike-sharing-demand> |
| MNIST (`fetch_openml('mnist_784')`) | Multi-class image classification | `ceu-ml/notebooks/class3_clustering.ipynb`, `class6_deep_learning_intro.ipynb` | <https://www.openml.org/d/554> |
| Synthetic 2D toys: `make_moons`, `make_circles` | Decision-boundary visualisation, clustering | `ceu-ml` deep-learning + clustering classes | `from sklearn.datasets import make_moons, make_circles` |
| Hotels Europe (Vienna) — Békés–Kézdi | Regression on price; pipeline practice | `Data-Analysis-3/Assignment-2`, `python-for-data-analysis/class-09` | <https://osf.io/r6uqb/> (and <https://gabors-data-analysis.com/>) |
| Used Cars — Békés–Kézdi | Regression with feature engineering | `da_data_repo/used-cars/`, `python-for-data-analysis/class-13` | <https://gabors-data-analysis.com/data-and-code/> |
| Bisnode firm exits — Békés–Kézdi | Imbalanced binary classification with business loss — perfect for the threshold-optimization snippet | `Data-Analysis-3/Assignment-2`, `python-for-data-analysis/class-17` | <https://osf.io/3qyut/> |

Reusable scikit-learn / OpenML defaults for quick experiments without downloading anything:

```python
from sklearn.datasets import fetch_california_housing, fetch_openml, load_breast_cancer

X, y = fetch_california_housing(return_X_y=True, as_frame=True)   # regression
X, y = load_breast_cancer(return_X_y=True, as_frame=True)         # binary classification
adult = fetch_openml("adult", version=2, as_frame=True)           # mixed-type tabular classic
```

For larger benchmark suites, see [OpenML CC18](https://www.openml.org/s/99) (72 curated tabular tasks)
or [Kaggle Datasets](https://www.kaggle.com/datasets) filtered by tabular + competition.

When pulling data for a project, pin the **download URL, version/snapshot date, and licence**
in a load-data cell — the `ceu-ml` notebooks consistently load straight from a versioned GitHub URL
(e.g. `https://raw.githubusercontent.com/divenyijanos/ceu-ml/2025/data/bike_sharing_demand/train.csv`),
which is a clean pattern.

## Further Reference

Inspiration repos (check these for full worked examples):

- `ceu-ml` — model comparison, pipelines on bike-share, transfer learning, bias-variance.
- `Data-Analysis-3` — Assignment 2 modelling notebook is a great cross-validated classifier walk-through with business-loss thresholding.
- `python-for-data-analysis` — `class-13` to `class-17` cover the prediction framework, lasso + grid search, regression trees, random forests + boosting, classification.
- `ceu-coding-2` — gentle intro to regression workflows.
- `da_data_repo` — many tidy datasets used by Békés–Kézdi *Data Analysis for Business, Economics, and Policy* (upstream: <https://github.com/gabors-data-analysis>).

External:

- [scikit-learn user guide](https://scikit-learn.org/stable/user_guide.html) — especially Pipeline, model_selection, metrics.
- [Raschka, *Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning*](https://arxiv.org/abs/1811.12808) — the canonical paper on doing this properly.

---

*These patterns are suggestions, not gospel. When in doubt, prefer **simpler models + honest evaluation** over exotic techniques.*
