# Using psychometric and clinical instruments legally

A worked case of the general rules in `licensing-and-attribution.md`, for a domain where they
bite unusually hard: assessment instruments carry copyright in the items, trademark in the
name, and produce special-category data on top.

Two separate questions, always: **may we use the items?** (copyright/licence/trademark) and
**may we process the results?** (GDPR). A royalty-free instrument still produces sensitive
data.

## Classification

| Class | Meaning | Examples | What you may ship |
| --- | --- | --- | --- |
| Public / research-published | items + key printed in a peer-reviewed article, author allows non-commercial and applied use | ACSI-28 (Smith, Schutz, Smoll & Ptacek, 1995, *JSEP* 17(4) 379–398, doi:10.1123/jsep.17.4.379); SMTQ (Sheard, Golby & van Wersch, 2009, *EJPA* 25(3) 186–193); MTI (Gucciardi et al., 2015, *J. Personality* 83(1) 26–44) | items verbatim, with citation; interpretation by a qualified professional |
| Public-domain **model**, proprietary **products** | the theory is free, specific commercial instruments are not | DISC model (Marston, 1928, *Emotions of Normal People*) vs. Everything DiSC® (Wiley), Extended DISC®, Thomas PPA | your own item set built on the four-factor model; never the branded items, report text, or the "DiSC®" styling |
| Fully proprietary | items, key and reports licensed, accredited users only | MTQ48 / MTQPlus (AQR International); MBTI® (The Myers-Briggs Company); NEO-PI-R, 16PF (publisher-controlled) | nothing without a licence — do not reimplement the key, do not claim comparability |

## Rules that keep you clean

1. **Cite the source** for published instruments, in-app and in the internal memo.
2. **Do not alter items** of a published instrument — a modified version is no longer the
   validated instrument, and claiming otherwise is a validity problem as well as a legal one.
3. **Do not claim equivalence.** "Our 14-item resilience questionnaire" — never "MTQ48
   results", never "comparable to AQR norms", never the trademark in marketing copy.
4. **Norm tables are separately copyrighted.** Publishing raw scores plus your own verbal
   interpretation avoids the issue entirely.
5. **Translations are copyrightable** — separately from the original. A translation supplied
   by a client or a third party is their responsibility; record who supplied it, when, and on
   what basis, so the provenance is answerable later.
6. **Competence condition.** Most free-use permissions assume interpretation by someone
   qualified. Build that into the product: results reach the subject through, or alongside,
   a professional.
7. **Never expose the scoring key or raw item mapping to the subject** if the licence or good
   practice requires test security — hide the A/B/C/D letters, hide reverse-coding.

## Repo hygiene

Keep items and keys in reviewable content files (`content/<instrument>.md`) with a header:

```markdown
# ACSI-28
Source: Smith, Schutz, Smoll & Ptacek (1995), JSEP 17(4), 379–398. doi:10.1123/jsep.17.4.379
Licence: published in peer-reviewed literature, free for research and applied use with citation.
Translation: supplied by {{WHO}}, {{DATE}}; provenance is the supplier's responsibility.
Reverse-scored items: 3, 7, 10, 12, 19, 23
```

This makes a licence audit a five-minute file read instead of a code archaeology exercise.

## Wording that stays defensible

Describe what you built, not what it resembles. Safe: "a 14-item resilience questionnaire",
"built on the public-domain four-factor model with our own items", "published in the
peer-reviewed literature and free to use with citation".

Avoid: trademarked product names, "validated", "norm-referenced", "clinically proven",
"comparable to <product>" — unless you can produce the paper that says so about *your*
version. Trademark is a separate right from copyright: reimplementing a public-domain model
is fine, calling the result by a commercial product's name is not.

## GDPR side of the same feature

Psychometric results about an identified person, used to inform decisions, are sensitive in
practice: explicit consent, strict role scoping, no third-party sharing, professional
interpretation, and a clear statement that the result is not a medical or clinical diagnosis.
