# GDPR essentials for app builders

## Does it apply?

Yes if you process personal data of people in the EU/EEA — including an internal HR tool, a
membership system, a research dataset, or an invite-only platform. "Closed access" reduces risk
exposure; it does not remove obligations.

Personal data = anything that identifies a person directly or indirectly, including an
internal ID that you can still link back to a name. Pseudonymised data is still personal
data; only genuinely anonymous data falls outside.

## Lawful basis (Art. 6)

| Basis | Fits | Watch out |
| --- | --- | --- |
| Consent 6(1)(a) | voluntary questionnaires, marketing, optional features | must be freely given — hard where there is a power imbalance (employer, teacher, service gatekeeper) |
| Contract 6(1)(b) | account, billing, delivering the service the user asked for | not for "nice to have" analytics |
| Legal obligation 6(1)(c) | tax, accounting, statutory reporting | cite the actual law |
| Legitimate interest 6(1)(f) | fraud prevention, basic security logging | requires a written Legitimate Interest Assessment; never for special-category data |

Power imbalance note: if a coach or employer asks a person to fill in an assessment,
consent may not be "freely given". Mitigations: no consequence for refusal, stated in
writing; an alternative path; or a different basis with a documented balancing test.

## Special categories (Art. 9)

Health, biometric, genetic, sex life, religion, politics, trade-union, race. Psychometric
and psychological profiling results are treated as sensitive in practice when they inform
decisions about a person. Default ground: **explicit consent** — a separate, specific,
affirmative act naming the type of data.

## Minors

- GDPR sets the information-society-services consent age between 13 and 16 (Member State
  choice; Hungary: 16). For sensitive assessments about a minor, obtain guardian consent
  regardless, and up to 18 where the national/civil-law rules on capacity apply.
- Implement: age input → conditional guardian consent checkbox → persist a boolean plus the
  age at consent time.

## Data subject rights (Arts. 15–22)

Access, rectification, erasure, restriction, portability, objection, and no solely
automated decisions with legal/significant effect. One-month response deadline, extendable
by two months with justification.

Build at minimum: a documented email route and an internal runbook. Better: a self-serve
export and a deletion request queue.

## Storage limitation (Art. 5(1)(e))

There is no fixed maximum. A 20–30 year record is lawful if the purpose genuinely spans
that period and you wrote the rule down. Defensible pattern:

```
active            → while the relationship (licence, employment, membership) exists
+ N years         → follow-up / professional continuity  (state N, e.g. 5)
within 12 months  → pseudonymise: drop name + email, keep random internal ID
after that        → statistical/research purpose only (Art. 5(1)(b), Art. 89)
annual review     → re-justify or delete; immediate deletion on consent withdrawal
```

## Security (Art. 32)

Encryption at rest and in transit, access control, pseudonymisation, resilience, testing.
Managed Postgres platforms give you AES-256 at rest and TLS in transit by default; the
application still owns role scoping, pseudonymisation and audit.

## Transfers (Chapter V)

Hosting inside the EU/EEA is the simplest answer. If any sub-processor is outside, you need
an adequacy decision or SCCs plus a transfer impact assessment. Always name the region and
the sub-processors in the policy.

## Paperwork you actually need

- **Records of processing (Art. 30)** — a table of purposes, categories, recipients,
  retention, transfers. Keep it in the repo as markdown.
- **DPA (Art. 28)** with every processor (hosting, database, email, AI provider).
- **DPIA (Art. 35)** — required for large-scale special-category processing, systematic
  profiling, or processing about vulnerable subjects (minors, patients, employees, or anyone
  in a dependent relationship with the controller). If two of those are true, do it.
- **Breach process** — 72 hours to the supervisory authority. Know who calls it.

## Member-state specifics

GDPR leaves real choices to national law: the digital consent age (13–16), employment-context
rules, and the supervisory authority you answer to. Fill these in for your jurisdiction before
writing the policy — the authority's full postal address is a required element of it.

- **Supervisory authority:** name, address, contact.
- **National supplementing act** and anything it adds.
- **Digital consent age.**
- **Language:** the policy must be understandable to the people it describes — publish it in
  the local language even when the codebase is English.

Filled in for Hungary:

- Supervisory authority: NAIH, 1055 Budapest, Falk Miksa u. 9–11., ugyfelszolgalat@naih.hu.
- Info Act (2011. évi CXII. tv.) supplements GDPR; digital consent age 16.
