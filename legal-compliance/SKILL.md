---
name: legal-compliance
description: Practical compliance guidance for software and data projects — EU data protection (GDPR lawful basis, consent, retention, data-subject rights), ePrivacy/cookie consent, the EU AI Act, and open-source licence compliance when reusing third-party code, content, datasets or course material (notice retention, attribution, permission requests, THIRD-PARTY-NOTICES). Use when an app collects personal data, when adding an AI feature that touches people, when auditing what a repo borrowed from elsewhere, or before publishing a repo publicly.
---

# Legal compliance for software and data projects

These are **suggestions** for turning EU data-protection, AI and licensing rules into concrete
engineering steps. This is engineering guidance, **not legal advice** — a lawyer or DPO signs
off before launch, and the licence conclusions here are how to stay obviously clean, not a
legal opinion on how far you could push.

The skill covers two independent questions that tend to arrive together:

- **May we process this data?** — GDPR, ePrivacy, AI Act.
- **May we reuse this code, content or dataset?** — licences, attribution, permission.

Either half stands alone. Load only the reference you need.

## When to use

Auto-apply when the task involves:

- Any app, service, notebook or pipeline that stores data about identifiable people.
- Consent UI, cookie banners, retention rules, deletion or export requests, access control.
- Adding an LLM, scoring, ranking or profiling feature that affects a person.
- Copying code, prose, figures, datasets or course material from somewhere else.
- A licence audit, a `README` attribution table, or making a private repo public.
- Writing a privacy page, a records-of-processing table, or a permission-request email.

Not for: contract drafting, employment law, tax, corporate structure, or anything where the
answer turns on facts a lawyer must gather. Say so and stop rather than improvising.

## Decision routing

| Situation | Read |
| --- | --- |
| Any project storing personal data of EU people | `reference/gdpr.md` |
| Deciding whether a cookie banner is required | `reference/cookies.md` |
| Any AI/LLM/scoring/profiling feature | `reference/ai-act.md` |
| Reusing third-party code, content, data or course material | `reference/licensing-and-attribution.md` |
| Consent UI, minors, retention, deletion, RLS — **web-app implementation** | `reference/web-app-patterns.md` |
| Using a psychometric or clinical instrument (DISC, MTQ, ACSI, MBTI…) | `reference/psychometrics-licensing.md` |
| Writing the public policy page or the internal memo | `reference/policy-templates.md` |

`reference/web-app-patterns.md` is deliberately stack-specific (React / TypeScript /
Postgres). The rules above it are stack-agnostic; use the patterns file when the deliverable
really is a web app, and translate the structure otherwise.

## Non-negotiable rules — data

1. **"Closed / internal system" is not an exemption.** GDPR applies to any processing of
   identifiable people, regardless of whether registration is public. Only purely personal
   household use is out of scope.
2. **Pick one lawful basis per purpose and write it down** (consent, contract, legitimate
   interest with a documented balancing test, legal obligation). Do not stack "consent +
   legitimate interest" as a fallback.
3. **Special-category data** (health, biometrics, and in practice psychological or
   psychometric results used to judge a person) needs Art. 9 grounds — normally *explicit*
   consent.
4. **Minors** need guardian consent for consent-based processing; store the flag and the age
   basis, not just a checkbox boolean.
5. **Consent must be recorded**: timestamp, policy version, scope. A checkbox with no audit
   row is unprovable.
6. **Access control is a legal control.** Enforce role scoping in the database (RLS or
   equivalent), never only in the UI.
7. **Retention needs a rule, not a number.** "As long as the relationship lasts + N years,
   then pseudonymise" is defensible; "we keep everything" is not.
8. **Cookie consent is triggered by non-essential storage**, not by data sensitivity. Adding
   analytics later means adding a banner later — plan the hook now.
9. **Data location matters less than transfer safeguards**, but EU-region hosting removes an
   entire class of Chapter V questions. State the region and the sub-processors explicitly.
10. **Never ship a policy that describes features you did not build.** Every claim in the
    privacy page must map to code or configuration you can point at.

## Non-negotiable rules — licensing

11. **A declared licence is permission already granted.** MIT, Apache-2.0, BSD, CC BY, GPL —
    each *is* the author saying yes, under conditions. You do not need to email anyone. The
    conditions are the whole obligation, and they are usually just notice retention plus
    attribution.
12. **No licence means all rights reserved.** A public repo with no `LICENSE` file grants
    nothing. That — not the permissive licences — is the case where you must ask.
13. **State permission status truthfully.** Write "permission is being sought; not yet
    obtained" while you wait. Never write "used by permission" before the reply arrives, and
    never let a plan to ask read as an answer received.
14. **Methods are not expression.** A workflow, an approach, a library choice, a bare import
    line and a canonical one-liner are not protected. Verify overlap before claiming "written
    from scratch" — then the claim is evidence, not hope.
15. **Attribution is not endorsement.** Credit instructors and authors as "based on" or
    "taught by". Never imply they reviewed, approved or endorsed the result — CC BY forbids
    it explicitly and it is misleading everywhere else.

## Minimum shippable compliance checklist

Data:

- [ ] Public privacy/legal page, linked from every entry point and every data-entry form.
- [ ] Named controller with real postal address, phone, and a data-protection contact.
- [ ] Explicit, unticked consent checkbox gating submit; conditional guardian checkbox < 18.
- [ ] `consent_given_at`, `consent_version`, `guardian_consent` persisted server-side.
- [ ] Documented retention rule + a pseudonymisation job (or a written plan and owner).
- [ ] Row-level access policies for every table holding personal data; roles in their own table.
- [ ] Cookie section listing every storage key and its purpose; banner only if non-essential.
- [ ] Data-subject rights route (access, rectification, erasure, portability, objection) with
      an owner and an SLA of one month.
- [ ] DPA with every processor; list them in the policy.
- [ ] AI features: disclosure of AI use, human-in-the-loop for any decision about a person.
- [ ] Records of processing (Art. 30) kept as an internal doc in the repo.

Licensing (before a repo goes public):

- [ ] A `LICENSE` file at the root — without one, nobody may use your work either.
- [ ] Every borrowed file carries its upstream notice and a link to the source.
- [ ] `THIRD-PARTY-NOTICES.md` listing derived material and cited-only sources, with the
      licence and the current permission status of each.
- [ ] Anything derived from an unlicensed source is either cleared, replaced, or held back.
- [ ] No private or privately-shared material committed — check before the first push, not after.
- [ ] Every cited link resolves (branch names and file paths rot fastest).

## Working method

**For a data feature:**

1. Enumerate every data field the project writes and the purpose of each. Delete fields with
   no purpose — minimisation is the cheapest compliance win.
2. Map purpose → lawful basis → retention → who can read it. One table, one row per purpose.
3. Implement the access rule in the database first, then in the UI.
4. Implement consent capture and versioning before the first real user.
5. Write the public page from the map, not from a template.
6. Re-run the checklist whenever a new field, integration or AI feature is added.

**For a licence audit:**

1. List every external source the project borrowed from, by file.
2. Fetch each one's licence — the actual `LICENSE` file, not the README's claim.
3. Classify: derived from (obligations apply) vs. cited only (no obligations, credit anyway).
4. Measure overlap where you claim there is none. Guessing is how false statements get shipped.
5. Satisfy each licence's condition in the file that needs it, and index all of them in one
   `THIRD-PARTY-NOTICES.md`.
6. Ask only where nothing was granted; hold that material back until the answer comes.

Full procedure and per-licence obligations: `reference/licensing-and-attribution.md`.

## Related skills

- `analytics-project-setup` — repo scaffolding; add `LICENSE` and `THIRD-PARTY-NOTICES.md`
  at scaffold time rather than retrofitting them before launch.
- `designing-analytics-projects` — the brief is where "what data do we need, and may we have
  it?" should first be asked.
