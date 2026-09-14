# Licensing, attribution and permission

Two questions, always kept apart:

- **May we use it?** — the licence. Answered by reading a file, not by emailing anyone.
- **How must we credit it?** — the licence's conditions, plus ordinary academic honesty.

The single most common misconception is backwards: people assume that anything *other than*
MIT needs permission. In fact **every declared licence is permission already granted**. The
case that needs an email is the one with **no licence at all**.

## The decision

```
Is there a LICENSE / COPYING file, or an SPDX header, in the source?
├── No  → ALL RIGHTS RESERVED. Nothing is granted, however public the repo is.
│         → Did you actually copy expression, or only learn an approach?
│            ├── approach only  → free to use; credit as courtesy (see "Ideas vs expression")
│            └── copied code/text → ASK. Hold the derived file back until the answer arrives.
└── Yes → permission is granted. Satisfy its conditions (table below). Do not email.
```

"I couldn't find a licence, but the author clearly wants people to use it" is not a licence.
Neither is a permissive README, a conference talk, or the fact that it is on GitHub. Publishing
something publicly grants no implied licence to copy it.

## Per-licence obligations

| Licence | You may | You must | Notes |
| --- | --- | --- | --- |
| **MIT** | use, modify, sublicense, sell | reproduce the copyright line **and** the permission notice in derivative files or docs | The most common obligation people miss: it is not "link back", it is *retain the notice*. |
| **BSD-2/3-Clause** | same as MIT | retain notice; BSD-3 also forbids using the author's name to endorse | Otherwise identical in practice to MIT. |
| **Apache-2.0** | same, plus an explicit patent grant | retain notice **and** any `NOTICE` file contents; **state that you changed the files** | The "state changes" duty is the one that gets skipped. |
| **CC BY 4.0** | share, adapt, commercially | credit author + title + licence **by name**, link the licence, indicate changes, don't imply endorsement | No ShareAlike ⇒ your derivative may carry a different licence (e.g. MIT) as long as attribution survives. |
| **CC BY-NC** | as above | as above | **Commercial use is blocked.** A public portfolio repo is usually fine; a paid product is not. Flag it. |
| **CC BY-SA** | as above | as above, **plus** license derivatives under the same terms | Incompatible with a permissively-licensed repo. Cite, don't derive. |
| **GPL-2.0 / GPL-3.0** | use, modify, distribute | distribute derivative *works* under the GPL, with source | Copyleft attaches to derivative works. **Merely importing a GPL library from your own code does not relicense your code** — distributing a combined work is the question. |
| **CC0 / public domain / Unlicense** | anything | nothing | Credit anyway; it costs nothing. |
| **None declared** | nothing | — | Ask, or write a clean-room replacement. |

Read the licence file itself. A README badge, a package registry field and the actual
`LICENSE` disagree more often than you would expect, and only the file counts.

## Notice retention in practice

Put the notice in the derived file, at the top, where anyone reading the code sees it. Not
buried in a root file nobody opens.

```python
"""Spline helpers.

Derived from da_helper_functions.py in gabors-data-analysis/da_case_studies:
https://github.com/gabors-data-analysis/da_case_studies/blob/master/ch00-tech-prep/da_helper_functions.py

Upstream is MIT licensed; its notice is retained here as MIT requires:

    MIT License
    Copyright (c) 2021 Gabors Data Analysis
    Full text: https://github.com/gabors-data-analysis/da_case_studies/blob/master/LICENSE
"""
```

Copy the copyright line **verbatim from the upstream `LICENSE`**. Paraphrasing the holder's
name defeats the point of a notice, and it is trivially checkable that you got it wrong.

For an unlicensed source you are still waiting on, say exactly that:

```python
"""...

PROVENANCE: the upstream repository carries no licence file, so no rights are granted by
default. Permission from the author (<name>) is being sought and has not yet been obtained.
See THIRD-PARTY-NOTICES.md at the repo root; if consent is declined, replace this with an
independent implementation.
"""
```

Once the answer is yes, replace the provenance line with who granted it, how, and when — and
keep the email, because it is now your licence:

```python
PROVENANCE: the upstream repository carries no licence file. The author (<name>) granted
permission by email (<month year>) to publish this adaptation here.
```

If the author later adds a licence file to the repo, cite the licence instead — a public
licence is easier for others to verify than your inbox. Check its scope: course repos often
licence the teaching material but carve out redistributed datasets.

**Never write "used by permission" before the reply arrives.** Intending to ask, having asked,
and having been told yes are three different states, and only the third one licenses anything.
Mirror whichever is true in both the file header and the notices index, and update both when
the answer comes.

## Ideas vs expression

Copyright protects the **expression**, not the idea. Not protected:

- A method, workflow, or the order you teach things in.
- A choice of libraries or a recommended default stack.
- Facts, parameter values, API names, function signatures you must write to call a library.
- Bare imports (`import geopandas as gpd`) and canonical one-liners with essentially one
  correct form — merger and *scènes à faire*.

Protected: prose, comments, non-obvious code of any length, exercise text, figures, slide
decks, datasets that involved selection or arrangement.

This is why a skill can distil a course without licensing anything from it. But **verify
before you claim it.** Run `snippets/overlap_check.py` against the source and the derivative;
it reports exact shared lines and near-matches with a similarity ratio. A real result reads
like:

> 0 overlapping prose lines out of 270; 11 exact code lines out of 213, all bare imports or
> a single canonical library call; 5 near-matches differing only in variable names.

That sentence, backed by a measurement, is worth more in the repo than any amount of
"I'm pretty sure nothing was copied."

## Privately-shared material

Course notebooks emailed to enrolled students, a colleague's script, an unpublished draft:

- Copyright is **automatic on creation**. Private sharing does not weaken it — if anything the
  absence of public posting removes even the weak "they clearly wanted it read" argument.
- **Do not redistribute.** Keep it in a private repo, gitignored, or outside the project.
- You may still use the **approach**. Attribute it: *"the approach here was shaped by X's
  course; the notebooks were shared privately and are not redistributed here; all text and
  code are written from scratch."*
- Verify that last clause before writing it, and check what actually got committed:
  `git ls-files <dir>` before the first push.

## Repository layout

One licence at the root, one index of everything borrowed:

```
LICENSE                    your terms for your own work
THIRD-PARTY-NOTICES.md     everything borrowed, indexed
README.md                  attribution table: skill/module → source → author → licence
```

**Per-folder licences are possible but rarely sensible.** They are for when a folder is
genuinely under different terms (a vendored GPL dependency, a CC BY-SA dataset). Retained
upstream notices in the derived files are *not* a reason to add one — they live in the file
header and the notices index. Multiple `LICENSE` files with no real difference between them
just make the actual terms harder to determine.

`THIRD-PARTY-NOTICES.md` template:

```markdown
# Third-party notices

## Derived material

| File | Source | Upstream licence | Obligation met | Permission status |
| --- | --- | --- | --- | --- |
| `path/to/file.py` | [repo/file](url) | MIT | Notice retained in file header | Granted by licence |
| `path/to/other.py` | [repo/file](url) | **None declared** | Header records provenance | ⚠️ Permission is being sought; not yet obtained. |

## Cited-only sources

Material referenced or distilled but not copied. No licence obligations arise; credited as
attribution, not endorsement.

| Source | Terms | How it is used here |
| --- | --- | --- |
| Course, instructor, link | Notebooks shared privately; **not redistributed here** | Teaching approach only. Verified: no prose overlap; matching code lines are bare imports. |
```

Keep the two tables separate. "Derived" carries obligations; "cited" carries only credit, and
conflating them makes it look like you copied more than you did.

## Asking for permission

**Required** — you copied expression from an unlicensed source. Be specific and easy to say yes
to: what you copied, where it will live, what licence you would publish it under, and what you
will do if the answer is no.

> I adapted `<file>` from your `<repo>`. The repository has no licence file, so I'm asking
> rather than assuming. It would live at `<url>` under MIT, with your name and a link to the
> original in the file header. If you'd rather I didn't, I'll replace it with my own
> implementation — no hard feelings either way.

**Courtesy** — nothing was copied, but the person's teaching or work shaped the result. Do not
frame it as a permission request; that invites a "no" to something you did not need.

> I'm not asking permission, since nothing of yours is republished. This is a courtesy note so
> you know your course is credited publicly, and an offer: if you'd like the attribution worded
> differently, expanded, or removed, tell me and I'll change it.

Send the courtesy note *after* running the overlap check, so its factual claims are true.

## Wording that stays defensible

| Say | Not |
| --- | --- |
| "based on", "distilled from", "taught by", "adapted from" | "endorsed by", "in partnership with", "official" |
| "derived from X, used under MIT" | "X's code" (implies they published it here) |
| "permission is being sought" | "used by permission" (before the reply) |
| "shaped by the course; written from scratch" | "the course materials" (implies redistribution) |

The same rules apply to a social-media post about the work. "Built on lecture notes from X's
course" is fine. Anything that reads as the author's involvement or approval is not.

## Link rot in cited sources

Citations decay faster than code. Before publishing, and periodically after:

- **Default branch**: many older repos are on `master`, not `main`. A `/blob/main/` deep link
  into a `master` repo 404s silently for every reader.
- **File existence**: check the git tree, not your memory — files cited from a course get
  renamed or never existed under the name in your notes.
- **OSF and data portals**: a project node id is not a file id. `osf.io/<project>/download`
  fails; each file has its own short id (`osf.io/download/<fileid>/`).
- **Bot blocking ≠ dead**: some hosts return 403 or an empty body to `curl` but load fine in a
  browser. Retry with a normal User-Agent before "fixing" a link that was never broken.

## Trademark is a separate right

A licence to copy the code says nothing about the name. You may reimplement a public-domain
model freely and still not call the result by a trademarked product name, use its styling, or
claim comparability with it. See `psychometrics-licensing.md` for the worked case.
