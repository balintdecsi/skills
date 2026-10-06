---
name: product-discovery
description: Suggestions for the earliest stage of a revenue-generating product — brainstorming problems and ideas, framing hypotheses, customer-discovery interviews (Mom Test), personas and beachhead markets, market sizing (TAM), competitor tables, riskiest-assumption tests, MVP design (landing page, concierge, Wizard of Oz, pre-order), business models, pricing and unit economics (LTV, CAC). Use when starting a new product or side-business repo, when the user asks "is this idea worth building?", "how do I validate this?", "who is the customer?", "how big is the market?", "what should the MVP be?", "how should I price it?", or wants a pitch / one-pager. Not for analytics project scoping — see designing-analytics-projects for that.
---

# Product Discovery — from idea to evidence before code

These are **suggestions** for the stage *before* a product repo has much code: finding a problem
worth solving, proving someone will pay, and deciding the smallest thing to build. The aim is
revenue, so every step ends in a question about money or behaviour, not opinion.

The structure follows the user's CEU MSBA course **Entrepreneurship and Innovation** (2026),
taught by Andrea Kozma — in particular the session order ideation → product-market fit →
validation → MVP → financing, and the "desirability / feasibility / viability" lens for the final
pitch. The course slides are not redistributed here; this skill is written from scratch and
restates widely published frameworks (Ries, Blank, Sarasvathy, Aulet, Christensen,
Fitzpatrick), credited below. Attribution, not endorsement.

## Cardinal Rule — Evidence, not enthusiasm

> **Never invent customers, quotes, interview results, market sizes, conversion rates or
> competitor prices.** If a number is not in the user's notes or a cited source, write
> `TBD — how to find out: …` instead.

Made-up traction is worse than none: it makes a bad idea look validated. When drafting,
label every claim with its evidence level:

| Level | What it is | Weight |
|---|---|---|
| 0 — Assumption | "We believe…" | Nothing yet; a hypothesis to test |
| 1 — Opinion | "I'd use that", "great idea!" | ≈ zero — compliments are noise |
| 2 — Past behaviour | "Last month I spent 3 h / €40 on this" | Real signal about the problem |
| 3 — Commitment | Time (a follow-up call, a pilot), reputation (an intro), money (pre-order, deposit, LOI) | Real signal about *your solution* |
| 4 — Repeat payment / retention | They paid again, they came back | Product-market fit territory |

Ideas move forward on levels 2–4. Levels 0–1 never justify building.

## When to Use

- A new repo or folder is being set up for a product, SaaS, app, service or side business.
- The user asks to brainstorm ideas, pick between ideas, or "sanity-check" one.
- Drafting interview scripts, personas, a competitor table, a TAM estimate, an MVP plan, pricing
  or a pitch / one-pager.
- Reviewing an existing plan for skipped validation ("we'll build it and then find users").

Do **not** use for scoping an internal analytics project (→ `designing-analytics-projects`) or
for the technical repo scaffold (→ `analytics-project-setup`, `uv`).

## The Discovery Loop (default workflow)

Work through these in order, but expect to loop back — a failed test at step 6 often means a
new beachhead at step 3. Keep outputs in the repo (see *Repo Artifacts* below).

1. **Problems, not ideas.** List 5–10 problems the founder has *experienced or observed*.
   Score each: frequency, intensity (painkiller vs vitamin — "migraine or nice-to-have?"),
   willingness to pay today, and founder fit (Bird-in-Hand: what do we already know / whom do
   we know?). Keep the top 1–3.
2. **Reframe and diverge.** Turn the top problem into a *How Might We…?* question that names
   the user and not the solution. Generate many solutions fast (Crazy 8s / 4s: one rough
   sketch per minute), then push the best one through **SCAMPER** (Substitute, Combine,
   Adapt, Modify, Put to other use, Eliminate, Reverse). See
   [reference/ideation.md](reference/ideation.md).
3. **Choose a beachhead.** Segment the market into 6–12 candidate segments, then pick **one**
   where customers can pay, can be reached directly, have a compelling reason to buy, buy
   similar things the same way, and talk to each other. Write an end-user profile and one
   persona (with the decision-making unit if the payer isn't the user).
4. **Write falsifiable hypotheses.** Use the PMF hypothesis template:
   *"We believe [target customer] has a problem with [pain]. Our solution, [product], solves it
   because [reason]. We'll know we're right when [metric / evidence threshold]."*
   Also write the job story: *"When [situation], I want to [progress], so I can [outcome]."*
5. **Customer-discovery interviews.** 5–10 interviews per segment before building anything.
   Talk about their life, not your idea. Script and synthesis template:
   [snippets/interview_script.md](snippets/interview_script.md).
6. **Riskiest assumption test (RAT).** Name the single assumption that, if false, kills the
   business — usually desirability ("do they want it?") or viability ("will they pay?"), rarely
   feasibility. Design the cheapest test that could prove it *wrong* (MVP menu below).
7. **Size and position.** Bottom-up TAM for the beachhead, competitor table, and the
   two-axis competitive-position chart on the persona's top two priorities.
8. **Model the money.** Business model, value-based pricing, LTV vs CAC, payback. Use
   [snippets/unit_economics.py](snippets/unit_economics.py) — never eyeball it.
9. **Decide: pivot, persevere, or kill.** Compare results against the thresholds written in
   step 4 *before* the test ran. Moving the goalposts afterwards is the classic failure.
10. **Only then build** the minimum viable *business* product: users get value, users pay, and
    it produces a feedback loop.

## Interviewing — the Mom Test in one screen

From Rob Fitzpatrick's *The Mom Test*: ask questions even someone who loves you can't lie to.

| Ask | Don't ask |
|---|---|
| "Tell me about the last time you [had the problem]." | "Would you use a product that…?" |
| "How do you solve this today? What does it cost you?" | "Do you like our idea?" |
| "What's the hardest part about [activity]?" | "Would you buy this?" / "How much would you pay?" |
| "What have you already tried? Why did you stop?" | "Isn't this a great idea?" |
| "Who else should I talk to?" | Anything that starts with your pitch |

Rules: listen, don't pitch; dig into specifics and past behaviour; note emotion; end every
interview by asking for a commitment (intro, follow-up, pilot, pre-order). Deflect compliments
("thanks — how do you handle it today?"). Don't interview only friends and family.

## MVP Menu — pick the cheapest test of the riskiest assumption

An MVP is an experiment, not a half-built product. Prefer the top of this list.

| MVP type | Tests | Example | Build cost |
|---|---|---|---|
| **Problem interviews** | Problem exists, current workaround | Mom Test interviews | Hours |
| **Landing page / smoke test** | Demand, messaging, channel | Value prop + email sign-up or "Buy" button → waitlist | 1 day |
| **Explainer video** | Demand for a hard-to-build product | Dropbox's demo video drove a large beta waitlist | Days |
| **Pre-order / deposit / LOI** | Willingness to pay | Tesla Model 3 deposits; B2B letter of intent | Days |
| **Concierge** | Value of the outcome; workflow | Deliver the service by hand to 3–5 customers | Days |
| **Wizard of Oz** | Value with a "real" front end, manual back end | Zappos: photos of shoes in shops, bought only after an order | Days–weeks |
| **Single-feature / no-code** | Retention around one job | Carrd, Figma, Bubble, a spreadsheet, a Telegram bot | Weeks |
| **Paper / click-through prototype** | Usability of the core flow | Sketches or Figma, tested think-aloud | Hours–days |

When testing a prototype with a user: the builder stays silent, the tester thinks aloud, no
defending or explaining. Ask at the end: *would you pay / use it? why or why not?*

## Product-Market Fit Signals

PMF = a product that satisfies a strong market demand. Indicators to track (rough rules of
thumb; vary a lot by category, so benchmark against your own segment):

- **Retention curve flattens** instead of decaying to zero — the single best signal.
- **Sean Ellis test**: ≥ 40% of active users would be "very disappointed" without it.
- **NPS** clearly positive (strong products often score > 50).
- **Organic growth / referrals** — new users arriving without paid acquisition.
- **Unit economics**: LTV ≥ 3× CAC and CAC payback ≲ 12 months (B2B SaaS heuristics).
- **Churn** low for the category (consumer subscriptions often target < 5% / month).

Pick **One Metric That Matters (OMTM)** for the current stage (e.g. interview → pre-order
conversion now; week-4 retention later) and write the target before measuring. Avoid vanity
metrics: page views, likes and sign-ups without activation say little.

## Market Sizing (TAM) — do it bottom-up

- **Bottom-up** (preferred): number of reachable customers matching the end-user profile ×
  annual revenue per customer. Count names: directories, association lists, registries,
  LinkedIn filters, census tables.
- **Top-down** (sanity check): industry report → share that fits the profile. The two should
  be within the same order of magnitude; if not, explain why.
- Aulet's rule of thumb for a beachhead: roughly **$20M–$100M TAM**. Far smaller → wrong
  beachhead; far larger → segment further. VCs want beachhead + follow-on markets ≥ $1B; a
  bootstrapped, revenue-first project can thrive on far less.
- Show the arithmetic and sources. TAM / SAM / SOM is fine if the user prefers it; SOM must
  be justified by channel capacity, not by "1% of a big number".

## Competitors and Positioning

Table with 3–5 competitors **including the status quo / do-nothing option** and DIY
workarounds:

| Competitor | Strengths | Weaknesses | Pricing | Business model | Our differentiation |
|---|---|---|---|---|---|

Then one positioning line: *"Unlike [alternatives], we offer [unique benefit] for [target
customer]."* And the competitive-position chart: x = persona's #1 priority, y = #2 priority;
you must be top-right, or rethink the segment. Name your **core** — the thing that is hard to
copy (network effects, proprietary data, deep domain expertise, cost, service) — and accept that
"better technology" alone rarely stays a moat.

## Business Model and Pricing

- Choose the model from **how the customer wants to buy**, not how you'd like to sell.
  Common: subscription, freemium, usage-based, transactional, marketplace (take rate),
  razor-and-blade, ads, affiliate / lead-gen, licensing, services → productised service.
- "Free now, monetise later" is not a business model — name who pays and when.
- **Value-based pricing**: quantify the value to the customer (as-is vs. with-you state in
  time, money or risk) and charge a fraction of it. Anchor against the current workaround's
  cost. Start higher; lowering prices is easier than raising them.
- Test price with real money where possible (pre-sale, deposit, paid pilot), not with
  "how much would you pay?".
- Unit economics: LTV (discounted, ~3–5 year horizon), CAC including failed spend and
  founder time, payback period, gross margin. Calculator:
  [snippets/unit_economics.py](snippets/unit_economics.py).

## AI-era / platform-dependency check

Many new revenue repos sit on top of someone else's platform (LLM APIs, app stores, cloud
marketplaces, social-media distribution). Before committing, write down:

- Which platform could **switch you off, reprice you, or copy you**? ("Is our moat just a
  feature on their roadmap?")
- How do inference / API costs scale with usage, and what happens to margin if prices change?
- What is defensible beyond the model: proprietary data, workflow lock-in, domain expertise,
  distribution, trust?
- Regulatory exposure (GDPR, AI Act, consumer law) → see `legal-compliance`.

## Choosing a framework lens

| Situation | Lens | Key question |
|---|---|---|
| Fast, testable software idea | **Lean Startup** (Ries) | What's the smallest experiment that teaches the most? |
| Customer and business model unclear | **Customer Development** (Blank) | Discovery → Validation → Creation → Company building |
| Very uncertain market, few resources | **Effectuation** (Sarasvathy) | What can we start with *now*, and what can we afford to lose? |
| Step-by-step build, B2B, hardware, regulated | **Disciplined Entrepreneurship** (Aulet) | Who exactly is the customer, and is each step proven before the next? |
| Feature list growing without focus | **Jobs-to-be-Done** (Christensen) | What progress is the customer hiring this for? |
| Founder motivation, habits | **Entrepreneurial Mindset** (Babson) | What action in the next 24 hours moves this forward? |

Use them together, not as rivals. Longer notes, including Aulet's 24 steps:
[reference/frameworks.md](reference/frameworks.md).

## Repo Artifacts

In a new product repo, keep discovery work as versioned Markdown next to the code so later
decisions can be traced to evidence. Suggested layout (adapt to the repo's conventions):

```
docs/discovery/
├── discovery_brief.md      # living one-pager — template: snippets/discovery_brief.md
├── assumptions.md          # assumption log: hypothesis, risk, test, threshold, result, decision
├── interviews/             # one file per interview, pseudonymised (no names / emails)
│   └── 2026-10-05_p01.md
├── market_sizing.md        # TAM arithmetic with sources
└── experiments/            # one file per MVP test: setup, threshold, result, decision
```

- Pseudonymise interview notes (P01, P02…) and keep contact details **out of git** —
  interviewee data is personal data (`legal-compliance`).
- Landing pages and waitlists collect personal data: consent text, privacy notice, cookie
  banner if analytics are used. For the site itself see `specification-website`.
- Record decisions (pivot / persevere / kill) with the date and the evidence that drove them.

## Anti-Patterns to Flag

- **Solution first**: an idea with no named customer or observed problem.
- **"Everyone" is the customer**: no beachhead; marketing to all ages, countries and roles.
- **Leading questions**: "Would you use…?", "How much would you pay?", pitching in interviews.
- **Friends-and-family validation** counted as evidence.
- **Overbuilding** the MVP; polishing before anyone has paid.
- **Vanity metrics** (sign-ups, likes) presented as traction.
- **Thresholds set after the result** came in; ignoring negative data.
- **Top-down only TAM** ("1% of a $50B market").
- **Competitor table without the status quo**, or "we have no competitors".
- **Free with no monetisation path**; LTV/CAC that ignores churn or founder time.
- **Platform dependency** ignored (one API, one app store, one ad channel).
- Using VC-style blitzscaling logic for a business that should be bootstrapped, or the reverse.

## Pitch / One-Pager Structure

When the user needs to present (investor, grant, partner, course), cover desirability,
feasibility and viability in about 10 slides:

1. Name + one-liner (what, for whom, why it matters)
2. Problem and how it is solved today
3. Solution and the unique innovation (show the prototype)
4. Target customer / beachhead / persona
5. Market size now and later (with arithmetic)
6. Competition and positioning
7. Product-market fit evidence (interviews, tests, retention, quotes)
8. Business model, pricing, go-to-market and KPIs
9. Funding need, use of funds, sources (bootstrapping, grants, angels, VC)
10. Team: why us (founder–market fit)

Lead with traction: real numbers beat vision. End with a clear ask.
Financing options and VC basics: [reference/financing.md](reference/financing.md).

## Related skills

- `designing-analytics-projects` — counter-metrics, pre-mortems and stakeholder maps carry
  over well to product experiments.
- `statistical-modeling` — when an A/B test or pricing experiment needs a proper significance
  test or confidence interval.
- `legal-compliance` — interview notes, waitlists and analytics collect personal data; AI
  features may fall under the AI Act.
- `specification-website` — what a landing page needs (metadata, accessibility, consent).
- `analytics-project-setup`, `uv` — scaffolding once the build decision is made.

## Sources

- Course: CEU MSBA *Entrepreneurship and Innovation* (2026), Andrea Kozma — session structure,
  exercises and case framing. Slides shared with enrolled students; not redistributed.
- Eric Ries, *The Lean Startup* (2011); Steve Blank, *The Four Steps to the Epiphany* (2005) and
  "Why the Lean Start-Up Changes Everything", *HBR* (May 2013).
- Saras Sarasvathy, "Causation and Effectuation" (*AMR*, 2001); <https://www.effectuation.org>.
- Bill Aulet, *Disciplined Entrepreneurship: 24 Steps to a Successful Startup* (2013).
- Clayton Christensen et al., *Competing Against Luck* (2016) — Jobs-to-be-Done.
- Rob Fitzpatrick, *The Mom Test* (2013).
- OpenStax, *Entrepreneurship*, §1.3 "The Entrepreneurial Mindset" (CC BY 4.0) —
  <https://openstax.org/books/entrepreneurship/pages/1-3-the-entrepreneurial-mindset>.
- Alexander Osterwalder & Yves Pigneur, *Business Model Generation* (2010).

---

*Suggestions, not gospel. When in doubt, **go talk to five more customers** before writing more code.*
