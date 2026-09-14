# Templates: public policy page and internal memo

Replace every `{{PLACEHOLDER}}`. Delete sections that describe things you did not build.

## A. Public privacy / legal page — section skeleton

```
1. Controller            name, registered address, phone, email, DPO/data-protection contact
2. What we collect       exhaustive field list, grouped by data subject type
3. Purpose & lawful basis one line per purpose; explicit consent flagged for sensitive data
4. Who can see it        role by role; state that access is enforced at database level
5. Retention             the rule, not a number; pseudonymisation step and its trigger
6. Where it is stored    region, provider, sub-processors, transfer safeguards if any
7. Security              encryption at rest and in transit, access control, hashed passwords
8. Cookies & storage     table of keys; why no banner, or how to change the choice
9. Your rights           the seven rights + withdrawal + how to exercise + response time
10. Complaints           supervisory authority with full address
11. AI use               whether AI generates any content; human review; no solely automated decisions
12. Assessment tools     if used: what they are, that results are informational, not a diagnosis
13. Version & date       "Effective from {{DATE}}, version {{N}}"
```

Drafting rules: second person, short sentences, no legalese padding, no claim you cannot
evidence. Link it from the footer *and* from every consent checkbox.

## B. Consent text patterns

Ordinary consent:

> I have read the privacy notice and I consent to {{CONTROLLER}} processing my answers and
> the resulting profile for {{PURPOSE}}. I may withdraw this consent at any time.

Explicit consent for sensitive data:

> I expressly consent to the processing of my {{SENSITIVE_DATA_TYPE}}, which counts as
> sensitive personal data, for {{PURPOSE}}, accessible only to {{ROLES}}.

Guardian:

> As the legal guardian of the participant (under 18), I consent to the processing described
> in the privacy notice.

Each must be a separate, unticked checkbox. Never bundle with terms of service.

## C. Internal licensing & compliance memo — skeleton

For the third-party-code side of licensing, use the `THIRD-PARTY-NOTICES.md` template in
`licensing-and-attribution.md` instead — this memo covers content and instruments.

```
1. Nature of the system      closed/invite-only, who has accounts, how subjects enter
2. Instruments used          per instrument: authorship, citation, licence status, conditions
3. What we deliberately avoid trademarked products, proprietary keys, norm tables
4. Sales pitch (short)       defensible wording, no trademarks, no validity claims
5. GDPR summary              controller, data, basis, access, retention, location, encryption
6. Cookies                   inventory and the banner decision with its reasoning
7. AI Act position           tier, reasoning, human oversight, disclosure
8. Open items                DPA signature, DPIA, deletion tooling, annual review owner
```

Keep it in the repo (`docs/legal-licensing.md`) so it versions with the code.

## D. Records of processing (Art. 30) — minimal table

Example rows, from a system where subjects submit assessments and staff review them —
substitute your own purposes.

| Purpose | Data categories | Subjects | Basis | Recipients | Retention | Location |
| --- | --- | --- | --- | --- | --- | --- |
| Assessment profiling | name, email, age, gender, answers, scores | subjects (incl. minors) | explicit consent | reviewer (assigned only), admin (all) | relationship + 5y, pseudonymised after 12m | EU (eu-west-3) |
| Professional accounts | email, password hash, role | staff | contract | none | while account active | EU |

## E. Pre-launch review questions

1. Can I point at the code line that blocks submission without consent?
2. Can I show a row proving a specific user consented to a specific policy version?
3. Can one reviewer reach another reviewer's records by editing a URL? (Try it.)
4. What exactly does the app write to the device? (Run the storage audit.)
5. Who runs the retention job, and when did it last run?
6. Is every processor covered by a DPA?
7. Does the policy describe anything that is not actually implemented?
8. If an AI feature exists: is there a named human who reviews the output?
