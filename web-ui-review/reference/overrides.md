<!--
Adapts rules from command.md in vercel-labs/web-interface-guidelines:
https://github.com/vercel-labs/web-interface-guidelines/blob/4ecfb9f/command.md

Upstream is MIT licensed; its notice is retained here as MIT requires:

    MIT License
    Copyright (c) 2025 Vercel Labs
    Full text: https://github.com/vercel-labs/web-interface-guidelines/blob/main/LICENSE
-->

# Overrides for the Web Interface Guidelines

This file sits on top of the upstream rules (live `command.md`, or the snapshot in [upstream-command.md](upstream-command.md)). It does three things: it sorts findings into tiers, rewrites the rules that conflict with WCAG or with this repository's other skills, and translates React and Tailwind wording for other stacks.

Precedence, highest first:

1. The project's own style guide, brand spec, or `DESIGN.md`, for **style** findings only.
2. This file.
3. Upstream wording.

## Contents

- Tiers
- Rewritten rules
- Other stacks
- shadcn/ui projects

---

## Tiers

Each finding gets one tier. **Any rule not listed under required or style is recommended**, including rules upstream adds after the snapshot, so new rules never block a review by accident.

| Tier | Meaning | In the report |
| --- | --- | --- |
| **required** | Fails WCAG 2.2 A/AA, breaks function, or risks data loss. Also the reduced-motion item, which `web-design` treats as its quality floor even though WCAG puts it at AAA. | Fix before shipping. |
| **recommended** | Craft, performance, and robustness. | Fix unless there is a reason not to. |
| **style** | House preferences: typography micro-rules and copy conventions. | Mention once per pattern rather than per line. |

Only WCAG success criteria that clearly apply are cited. Where none is listed, the reason is given instead.

### required

| Rule | Why |
| --- | --- |
| Icon-only controls have an accessible name (`aria-label` or visually hidden text) | WCAG 4.1.2 |
| Form controls have an associated label (`<label for>`, a wrapping `<label>`, `aria-label`, or `aria-labelledby`); a placeholder alone is not a label | WCAG 1.3.1, 3.3.2, 4.1.2 |
| Actions use `<button>`, navigation uses `<a href>`; no click handlers on `div` or `span` | WCAG 2.1.1, 4.1.2 |
| Custom (non-native) interactive widgets are keyboard operable | WCAG 2.1.1 — see the rewritten rules |
| Custom modal overlays use `<dialog>` with `showModal()`, or `role="dialog"` with `aria-modal="true"`; they have an accessible name, keep focus inside while open, and close with Escape or a visible close control | WCAG 4.1.2, 2.4.3, 2.1.2 |
| Meaningful images have `alt`; decorative images have `alt=""` | WCAG 1.1.1 |
| Asynchronous status updates (toasts, inline validation, "Saved") are announced through a live region | WCAG 4.1.3 |
| Pages with repeated navigation offer a way past it: a skip link or landmark regions | WCAG 2.4.1 |
| Meaningful media has captions or transcripts; media controls work from the keyboard | WCAG 1.2.x, 2.1.1 |
| Every interactive element has a visible focus indicator; `outline: none` / `outline-none` only with a replacement | WCAG 2.4.7 |
| Sticky headers, footers, and overlays do not entirely hide the focused element (partly covering it is recommended to fix: WCAG 2.4.12 is AAA) | WCAG 2.4.11 |
| Paste is never blocked (`onPaste` with `preventDefault`) | WCAG 3.3.8 for password and code fields; a usability failure everywhere else |
| Fields that collect the user's own data carry the matching `autocomplete` token | WCAG 1.3.5 |
| Errors are identified and described in text, not by color alone | WCAG 3.3.1, 1.4.1 |
| Auto-playing motion lasting more than 5 seconds next to other content can be paused, stopped, or hidden | WCAG 2.2.2 |
| Path, multipoint, and drag gestures have a single-pointer alternative that needs no path or drag, and the action also works from the keyboard. A keyboard alternative alone does not satisfy 2.5.1 or 2.5.7. | WCAG 2.5.1, 2.5.7, 2.1.1 |
| Zoom is never disabled (`user-scalable=no`, `maximum-scale=1`) | WCAG 1.4.4 |
| Content reflows at 320 CSS px wide without horizontal page scrolling, except content that needs a two-dimensional layout, such as data tables, maps, and toolbars | WCAG 1.4.10 |
| Text contrast is at least 4.5:1 (3:1 for large text); component boundaries, focus indicators, and meaningful graphics are at least 3:1 against their surroundings | WCAG 1.4.3, 1.4.11 |
| Pointer targets are at least 24×24 CSS px, or spaced so that a 24 px circle centred on each does not touch another target; links inside running text are exempt | WCAG 2.5.8 |
| Non-essential animation respects `prefers-reduced-motion` | House floor shared with `web-design` (WCAG 2.3.3 is AAA) |
| Destructive actions have a confirmation or an undo window | Data loss |
| Controlled inputs have a change handler (React `value` without `onChange` makes the field read-only). Applies to all React code, not only server-rendered pages. | Broken function |
| Key handlers do not re-trigger a native action, for example calling `click()` on Enter in a submit button | Broken function: the action fires twice |

### style

- `…` instead of `...`, including loading labels ("Loading…", "Saving…") and placeholders.
- Curly quotes instead of straight quotes.
- Non-breaking spaces in `10&nbsp;MB`, `⌘&nbsp;K`, and brand names.
- `text-wrap: balance` or `pretty` on headings.
- Placeholders end with `…` and show an example pattern.
- Title Case for headings and buttons (see the rewritten rules).
- Numerals for counts, second person, active voice, and `&` instead of "and" where space is tight.
- `-webkit-tap-highlight-color`, `touch-action: manipulation`, and page rubber-band suppression. Modern mobile browsers no longer add a tap delay on pages with `width=device-width`, so these are polish, not fixes.

---

## Rewritten rules

| Upstream says | Apply instead | Reason |
| --- | --- | --- |
| Interactive elements need keyboard handlers (`onKeyDown`/`onKeyUp`) | Only custom widgets built from non-interactive elements need keyboard handling. Native controls already have it: `<button>` activates on Enter and Space, links on Enter, and checkboxes and radios toggle on Space. | A handler that repeats the native action makes it fire twice (see the required rule). |
| `autocomplete="off"` on non-auth fields | Use `off` only on fields that do not describe the user, such as site search or a form editing someone else's record. One-time codes use `autocomplete="one-time-code"`; passwords use `new-password` or `current-password`. Never strip autocomplete from name, email, phone, address, or payment fields. | WCAG 1.3.5 needs those tokens, and password managers and autofill depend on them. |
| Title Case for headings/buttons (Chicago style) | Kept as the house default, for headings and buttons only. Labels, descriptions, placeholders, toasts, and errors stay in sentence case. A project style guide wins. | Matches `web-design`; tiered as style. |
| Avoid unwanted scrollbars: `overflow-x-hidden` on containers | Fix the element that overflows first. If clipping is still needed, `overflow-x: clip` keeps `position: sticky` working inside the container, because unlike `hidden` it does not create a scroll container. Use it only when nothing interactive can end up clipped, since clipped focusable content cannot be scrolled into view. | `hidden` hides the symptom and breaks sticky positioning. Both values cut off focus rings that extend past the edge. |
| Buttons/links need `hover:` state | Flag only custom elements. Components from a library already carry hover, focus, and active states in their variants. | Avoids recommending style overrides that the library forbids. |
| Errors inline next to fields; focus first error on submit | Describing the error in text is **required** (WCAG 3.3.1). Placing it next to the field and moving focus to the first error are **recommended**. | WCAG 3.3.1 does not prescribe where the error appears. |

---

## Other stacks

Upstream is written for React, Next.js, and Tailwind. Check the intent of each rule, not the literal class or prop name.

| Upstream | Plain HTML/CSS and other frameworks |
| --- | --- |
| `focus-visible:ring-*` | A `:focus-visible` rule with `outline` (or `box-shadow`) |
| `outline-none` | `outline: none` |
| `htmlFor` | `for` |
| `spellCheck={false}`, `autoFocus` | `spellcheck="false"`, `autofocus` |
| `onKeyDown` / `onPaste` | `keydown` / `paste` listeners, or the framework's event binding (`@keydown` in Vue, `onkeydown` in Svelte 5, `on:keydown` in Svelte 4) |
| Next.js `priority` on images | `fetchpriority="high"` and no `loading="lazy"` on the hero image |
| `truncate`, `line-clamp-*`, `break-words` | `overflow: hidden; text-overflow: ellipsis; white-space: nowrap`; `display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: <n>; overflow: hidden`; `overflow-wrap: break-word` |
| `min-w-0` | `min-width: 0` on the flex child |
| `<Link>` | `<a href>` |
| `nuqs` / `useState` URL sync | `URLSearchParams` with `history.replaceState` or `pushState`, or the router's query API |
| `virtua` | `content-visibility: auto`, pagination, or the framework's virtual list |
| Hydration Safety section | Applies only to server-rendered pages that hydrate on the client (Next.js, Remix, Nuxt, SvelteKit, Astro islands). Skip it for static HTML. The controlled-input rule in that section applies to all React code. |

---

## shadcn/ui projects

When `components.json` exists, also apply the `shadcn` skill's Critical Rules. Where the two meet:

- **States come from the component.** Do not flag missing `hover:` or `focus-visible:ring-*` classes on shadcn components, and do not recommend adding them: shadcn reserves `className` for layout. Flag only custom elements.
- **Fix through tokens and variants.** For a contrast problem or a missing status color, fix the CSS variable or add a `cva` variant rather than adding raw Tailwind colors or `dark:` overrides to the element.
- **No `z-index` fixes on overlays.** Dialog, Sheet, Popover, and similar components manage their own stacking.
- **Icon-only buttons still need a name.** `<Button size="icon">` needs `aria-label` even though some upstream shadcn examples omit it (the `InputGroupAddon` search button, for one). This stays **required**.
- **Already covered by the library:** Sonner announces toasts through a live region, so do not flag a missing `aria-live` on them; check any other toast component once rather than assuming. `DialogTitle`, `SheetTitle`, and `DrawerTitle` give overlays an accessible name (shadcn requires them, so flag a missing one as required); `AlertDialog` is the confirmation for destructive actions.
- **Ellipses:** shadcn examples use `...` ("Search...", "Saving..."). Flag them under **style** only.
