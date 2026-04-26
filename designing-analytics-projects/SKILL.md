---
name: designing-analytics-projects
description: Suggestions for scoping and writing an Analytics Project Brief — the one-page artifact that defines problem, metrics, counter-metrics, stakeholders, methodology, success criteria, and pre-mortem before any analysis begins. Use when the task is to draft, review, or critique a project brief, scope an analytics project, define KPIs, identify counter-metrics or blockers, or prepare a stakeholder map. Not for technical implementation — see ml-modeling, statistical-modeling, or data-warehousing for that.
---

# Designing Analytics Projects — the Brief

These are **suggestions** based on the user's CEU MSBA course **Designing Analytics Projects** (`ECBS5228A`), taught by Eduardo Arino de la Rubia (ex-Meta, ex-Domino). Source: <https://github.com/earino/designing-analytics-projects>.

The course centres on **one artifact: the Analytics Project Brief**. Everything in this skill exists to help write one well.

## Cardinal Rule — Use What You're Given

A brief is only as good as its grounding in the scenario.

> **If the scenario, scoping notes, stakeholder list, data dictionary, prior analysis, or any other local file mentions a number, name, metric, system, or business rule — use it verbatim. Do not invent.**

When information is missing, **say so explicitly** ("not specified in scenario; recommend confirming with X") rather than fabricating a baseline, headcount, KPI, or stakeholder name. Made-up specificity is the single most common failure mode for AI-drafted briefs — it looks professional and is wrong, which is worse than vague.

If the user gives a scenario file, **read it first and extract**:

- Company name, business model, current metrics (registered users, MRR, NPS, etc.)
- Named stakeholders, their roles, and their stated motivations / KPIs
- Available data tables and known data-quality caveats
- Stated constraints (time, sample size, privacy, can't survey, etc.)
- The exact ask (what was requested vs what's actually needed)

Quote those facts directly in the brief instead of paraphrasing into something more generic.

## When to Use

- "Draft / review / critique an Analytics Project Brief" or "project brief" or "scoping doc."
- A scenario file is present and the deliverable is a written brief.
- The user is preparing to talk to stakeholders, kicking off a new analysis, or sanity-checking scope.
- Any mention of: counter-metrics, guardrails vs tradeoffs, Goodhart's Law, pre-mortem, Power-Interest Grid, stakeholder map, decision criteria, "what breaks if we succeed."

Do **not** auto-trigger for purely technical tasks (training a model, writing SQL, building a pipeline). The brief is the *pre-code* artifact. Once the brief is approved and you're ready to set up the actual repository, switch to the **`analytics-project-setup`** skill.

## The 10 Sections (one-line each)

1. **Problem & Decision** — what decision will this inform; who actually decides; *why now*; one-sentence hypothesis.
2. **Metrics** — primary metric defined SQL-precisely (event/table, grain, eligibility, time window) + 2–3 counter-metrics labelled **Guardrail** (must not worsen) or **Tradeoff** (may worsen within bounds).
3. **Stakeholder Map** — Power-Interest Grid (4 quadrants) + named **Champions** + named **Blockers with their motivation** (budget / ego / workload / KPI conflict).
4. **Methodology** — 1–3 methods, each tied to a specific hypothesis and the data required, plus **Stop/Go data-validity checks**.
5. **Scope & Deliverables** — In Scope, **Out of Scope** (the line that prevents creep), concrete deliverables.
6. **Success & Decision Criteria** — analytical success vs business success, decision forum + action owner, **pre-committed decision table** ("if we find X, we will do Y; if inconclusive, …"), action thresholds.
7. **Timeline** — milestones with dates, not vibes.
8. **Risks & Assumptions** — assumptions, risks with L/M/H likelihood × impact, mitigations.
9. **Ethics & Privacy** — PII? bias against protected groups? GDPR review? mitigations.
10. **Pre-Mortem** — *"It's 3 months from now and this failed. What happened?"* Tell the **causal story** ("we did X, Y happened, because Z"). This surfaces the risks Section 8 misses.

A blank template lives at `~/repos/ceu/designing-analytics-projects/templates/analytics_project_brief.md` and as [snippets/brief_template.md](snippets/brief_template.md) in this skill. Use it as the literal scaffold.

## Quality Bar — what makes a brief strong

The course's rubric (see `syllabus.md`) rewards four things, in this order:

1. **Metric definition precision.** Not "conversion rate" but "users with `signup_complete` on day 0 → users with ≥1 `app_open` on calendar day 7, eligible cohort: web signups in last 6 months." If you can't write the SQL, the definition isn't done.
2. **Counter-metrics that show adversarial thinking.** What breaks if we hit the target? Sugar-diet growth, zombie retention, casual-user alienation, brand-trust erosion. Two to three is the right number — five looks like padding.
3. **Stakeholder analysis that names blockers and their motivation.** "Head of Growth" is a placeholder. "Head of Growth — bonus tied to signup volume, will resist any onboarding friction" is analysis.
4. **A pre-mortem that surfaces non-obvious risks.** Not "the data could be bad" — a *causal story*: "By month 3 the recommendation was shipped, retention didn't move, and the post-mortem found that Learning Paths were correlated with retention because engaged users self-selected into them, not because the feature caused engagement."

## High-Leverage Patterns

**Counter-metric framing** — for each candidate primary metric, ask: *what's the laziest way to hit this number, and what would break?* Examples from the course cheatsheet:

| Primary metric | Lazy way to hit it | Counter-metric |
|---|---|---|
| Conversion rate | Cut the funnel down to power users | Revenue per visitor |
| D7 retention | Spam push notifications | Notification opt-out rate |
| Subscription conversions | Gut free-tier limits | Free-user retention, brand trust |
| MAU | Send re-engagement to dormant users | Engagement depth ("zombie retention") |
| Power-user revenue | Optimise only for top 1% | Casual user satisfaction |

**Pre-mortem prompt** that consistently produces useful output:

> Imagine it's 3 months from now. We shipped what this brief proposes. The project failed — not in a vague way, but specifically. Tell the causal story in 3 sentences: what we recommended, what happened, and the reason it didn't work that we missed today.

**Stakeholder Power × Interest** in 30 seconds — for each named person:

| | High Interest | Low Interest |
|---|---|---|
| **High Power** | Manage closely (weekly updates, pre-brief) | Keep satisfied (don't surprise them) |
| **Low Power** | Keep informed (channel for advocacy) | Monitor (FYI only) |

Then for each High-Power-High-Interest person, decide: **Champion** or **Blocker**? If Blocker, what's the motivation (KPI conflict, budget, ego, workload, prior burn)? **Pre-brief privately** before any group meeting — no surprises.

## Anti-Patterns to Flag in Reviews

- **Generic stakeholder list** copied from a slide deck (no names, no motivations).
- **Primary metric without a SQL-grade definition** (no event, no grain, no eligibility, no time window).
- **No counter-metrics**, or counter-metrics that are just other primary metrics.
- **"Explore the data"** as the methodology — that's not a project, it's a fishing trip.
- **No "Why now?"** — without urgency, the brief will not get prioritised.
- **Decision criteria written after results are in.** Pre-commit, in the brief.
- **Pre-mortem as a generic risk list** ("data could be incomplete"). It must be a story, not a checklist.
- **Inventing numbers** ("we estimate ~20% lift") when the scenario gave none. Say "to be confirmed with stakeholder" or use the scenario's stated numbers.
- **Treating "Out of Scope" as optional.** It's the section that protects you when the ask quietly grows.

## Worked Examples in the Repo (read at least two before drafting)

In `~/repos/ceu/designing-analytics-projects/templates/examples/` there is one fully-worked brief per foundational analysis:

| Analysis | Example | Company |
|---|---|---|
| Funnel | `brief_01_funnel_analysis.md` | Quickcart |
| Channel Attribution | `brief_02_channel_attribution.md` | DataDash |
| Campaign Effectiveness | `brief_03_campaign_effectiveness.md` | BrightMart |
| CAC / LTV | `brief_04_cac_ltv.md` | MindfulApp |
| Retention | `brief_05_retention_analysis.md` | SnapGram |
| Power User | `brief_06_power_user_analysis.md` | Streamflix |
| Failure Analysis | `brief_07_failure_analysis.md` | FindIt |
| Expansion / Monetisation | `brief_08_expansion_monetization.md` | NoteSpace |
| Ecosystem | `brief_09_ecosystem_analysis.md` | SocialSuite |

Pick the example whose analysis type matches the scenario at hand and mirror its **section depth, table formats, and tone**.

The user's own assignment brief — `~/repos/ceu/designing-analytics-projects/assignments/learnloop_project_brief.md` — is also a strong reference for the depth and style expected on a real submission, drafted from `scenarios/scenario_03_learnloop.md`.

## Foundational Analysis Cheatsheet (which one fits the scenario?)

Match the business question to an analysis type, then mirror that example brief.

| Question | Analysis | Watch out for |
|---|---|---|
| Where do prospects drop off? | Funnel | Cross-device tracking, missing events |
| Who gets credit for the conversion? | Channel Attribution | No "right" model — find where they disagree |
| Did this campaign actually cause the lift? | Campaign Effectiveness | Correlation ≠ causation; pull-forward; contamination |
| Are unit economics healthy? | CAC / LTV | Blended CAC hides bad channels; LTV on margin not revenue |
| Do users come back? | Retention | "Sugar-diet growth" hides churn; correlations ≠ drivers |
| Who are the heaviest users and why? | Power User | Don't alienate the casual majority |
| What's broken / what are we losing? | Failure Analysis | Manual sampling first; size by **impact**, not volume |
| Why do users upgrade / pay more? | Expansion & Monetisation | Free-user churn from over-monetisation |
| Do products help or cannibalise each other? | Ecosystem | Selection bias on multi-product users |

Source: `cheatsheet.md` in the course repo (the one-A4 exam cheat sheet — concentrated wisdom).

## Suggested Workflow When Drafting from a Scenario

1. **Read the scenario twice.** Highlight every number, name, system, and constraint.
2. **Pick the foundational analysis** (table above). Open the matching example brief side-by-side.
3. **Draft Section 1 (Problem & Decision) first** and resist the urge to skip to methodology. If you can't name the decision and the decision-maker, the brief is not ready.
4. **Write the metric definition next**, SQL-precise. If the data dictionary doesn't support it, say so.
5. **Add counter-metrics by asking "what breaks if we hit this number?"** Two or three.
6. **Stakeholder map from the named people in the scenario** (do not invent roles). For each High-Power person, decide Champion vs Blocker and the motivation, *quoting* the scenario where possible.
7. **Methodology + Stop/Go checks.** What must be true before you trust the result?
8. **Decision criteria pre-committed** before you skip ahead to Pre-Mortem.
9. **Pre-mortem last** — it depends on everything above.
10. **Re-read the scenario.** Did you contradict any stated fact? Did you invent any number? Fix.

## From Brief to Technical Setup

Once the brief is approved, the next step is technical project scaffolding. Use the **`analytics-project-setup`** skill to:

1. Create the analytics repository.
2. Create the folder structure (`dev/prod` split, `data/`, numbered notebooks).
3. Set up shared config/constants, `.gitignore`, pre-commit hooks.
4. Write `README.md` using the structured template in the setup skill.
5. Create `AGENTS.md` so AI agents understand the project context.

The brief defines *what* you're building and *why*. The setup skill handles *how* the repo is structured.

## Further Reference

- **Course repo (the source of truth):** <https://github.com/earino/designing-analytics-projects>
  - `templates/analytics_project_brief.md` — blank template (also at `snippets/brief_template.md` in this skill).
  - `templates/examples/` — 9 worked briefs, one per foundational analysis.
  - `cheatsheet.md` — the one-A4 distillation; the densest reference in the repo.
  - `scenarios/` — 18 practice scenarios.
  - `syllabus.md` — full course structure, rubric, and reading list.
- *Designing Experimentation Guardrails*, Airbnb Engineering — the canonical counter-metrics reference.
- *Getting to Yes* (Fisher, Ury, Patton), ch. 1–3 — for the influence / blocker chapters of any brief.
- Goodhart's Law: *"When a measure becomes a target, it ceases to be a good measure."* — the reason counter-metrics exist.
- Géron, [ML project checklist](https://github.com/ageron/handson-ml3/blob/main/ml-project-checklist.md) — his "Frame the problem" section is a complementary checklist to the Analytics Project Brief.

Companion skills:

- **`analytics-project-setup`** — technical scaffolding, folder structure, AGENTS.md, environments. **Use after the brief is approved.**
- **`ml-modeling`** — for building and evaluating predictive models.
- **`statistical-modeling`** — for inferential/explanatory analysis.
- **`data-warehousing`** — for data pipeline architecture.

---

*Suggestions, not gospel. The single highest-leverage habit: **quote the scenario, don't paraphrase it; flag missing info, don't invent it.***
