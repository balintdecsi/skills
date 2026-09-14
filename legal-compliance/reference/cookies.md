# Cookies, localStorage and the consent banner question

## The rule

**Status, September 2026.** The Digital Omnibus proposes moving consent-for-terminal-equipment
out of ePrivacy and into the GDPR (new Arts. 88a/88b: no re-asking for six months after a
refusal, browser-level signals binding). That part is **still a proposal** — final text is not
expected before late 2026. The rules below are the ones in force; build to them.

The ePrivacy Directive (Art. 5(3)) covers *any* storage of, or access to, information on the
user's device — cookies, `localStorage`, `sessionStorage`, IndexedDB, fingerprinting, pixels.
Consent is required **unless** the storage is:

1. strictly necessary to deliver a service the user explicitly requested, or
2. used solely to transmit a communication.

Sensitivity of the data is irrelevant. A closed internal system is **not** exempt by virtue
of being closed — it is exempt only if every storage item is strictly necessary.

## Decision tree

```
Does the app write anything to the device?
├── No  → no banner, still describe "no cookies used" in the policy
└── Yes → classify each key
     ├── auth/session token, CSRF, load balancing, language chosen by the user,
     │   in-progress form state       → strictly necessary → NO consent needed
     └── analytics (GA4, Plausible with cookies, Hotjar), ads, social pixels,
         A/B testing, error tools that set persistent IDs → consent REQUIRED
             → prior, granular, opt-in banner; reject must be as easy as accept;
               no pre-ticked boxes; nothing fires before the click
```

Cookieless, IP-anonymised analytics can sometimes avoid consent, but the analysis must be
per-tool and documented. Do not assume.

## Always required, banner or not

A cookie/storage section in the privacy page listing every key, its purpose, its lifetime,
and whether it is first- or third-party.

## Inventory table template

| Key | Type | Purpose | Lifetime | Consent |
| --- | --- | --- | --- | --- |
| `<app>-auth-token` | localStorage | keeps signed-in users authenticated | session / until logout | not required |
| `form-progress-<id>` | localStorage | preserves in-progress form entry | until submit | not required |
| `_ga` | cookie | audience analytics | 2 years | **required** |

## Auditing what the app actually stores

```ts
// paste in the browser console on a fresh session
console.table([
  ...Object.keys(localStorage).map(k => ({ store: "localStorage", key: k })),
  ...Object.keys(sessionStorage).map(k => ({ store: "sessionStorage", key: k })),
  ...document.cookie.split("; ").filter(Boolean).map(c => ({ store: "cookie", key: c.split("=")[0] })),
]);
```

Run it before every release; a new dependency can silently add a third-party cookie.

## Consent-gated loading pattern

Never ship the tag and disable it — never load it at all until consent exists.

```tsx
// src/components/analytics-gate.tsx
import { useEffect, useState } from "react";

const KEY = "cookie-consent-v1"; // bump the version when the tool list changes

export function useCookieConsent() {
  const [consent, setConsent] = useState<"granted" | "denied" | null>(null);
  useEffect(() => {
    setConsent((localStorage.getItem(KEY) as "granted" | "denied" | null) ?? null);
  }, []);
  const decide = (value: "granted" | "denied") => {
    localStorage.setItem(KEY, value);
    setConsent(value);
  };
  return { consent, decide };
}

export function AnalyticsGate() {
  const { consent } = useCookieConsent();
  useEffect(() => {
    if (consent !== "granted") return;
    const s = document.createElement("script");
    s.src = "https://example-analytics.test/script.js";
    s.async = true;
    document.head.appendChild(s);
    return () => { s.remove(); };
  }, [consent]);
  return null;
}
```

Banner requirements: equally prominent "Accept all" and "Reject all", per-category toggles,
a link to the policy, and a way to change the decision later (a footer link that clears the
key). Store the decision and its version so you can prove what was agreed.

## If you have no non-essential storage

Say so plainly in the policy, list the essential keys, and add: "If analytics or marketing
tools are introduced, prior explicit consent will be requested." That sentence is what makes
the omission of a banner a documented decision rather than an oversight.
