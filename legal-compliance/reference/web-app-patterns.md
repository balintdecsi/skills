# Web-app implementation patterns (React / TypeScript / Postgres)

Copy-paste starting points for the stack-specific half of the skill. The rules in `SKILL.md`
are stack-agnostic; these are one concrete way to satisfy them. Adapt names; keep the
structure. The Postgres examples use Supabase idioms (`auth.uid()`, `service_role`) — any
Postgres with an authenticated-user function works the same way.

The worked example throughout is a system where **subjects** submit a form, **reviewers** see
only the subjects assigned to them, and **admins** see everything. Substitute your own nouns.

## 1. Consent capture with versioning

Bump `CONSENT_VERSION` whenever the policy text changes materially — old rows stay
attributable to the text they agreed to.

```ts
// src/lib/consent.ts
export const CONSENT_VERSION = "2026-09-02";
export const GUARDIAN_CONSENT_AGE = 18;
```

```tsx
// intake form fragment
const needsGuardian = Number(age) > 0 && Number(age) < GUARDIAN_CONSENT_AGE;
const canSubmit = consent && (!needsGuardian || guardianConsent);

<label className="flex items-start gap-3 text-sm">
  <input type="checkbox" checked={consent} onChange={e => setConsent(e.target.checked)} />
  <span>
    I have read the <Link to="/legal">privacy notice</Link> and I consent to the
    processing of my answers and results for the purpose described there.
  </span>
</label>

{needsGuardian && (
  <label className="flex items-start gap-3 text-sm">
    <input type="checkbox" checked={guardianConsent}
           onChange={e => setGuardianConsent(e.target.checked)} />
    <span>As the participant is under 18, the legal guardian has given consent.</span>
  </label>
)}

<button disabled={!canSubmit}>Start</button>
```

Rules: never pre-tick, never bundle several purposes in one checkbox, never make the link
open-in-new-tab-only content that the user cannot read before consenting.

## 2. Persisting consent server-side

Trust the server, not the client: re-validate.

```sql
alter table public.submissions
  add column consent_given_at timestamptz,
  add column consent_version  text,
  add column guardian_consent boolean not null default false;
```

```ts
// server function handler
if (!data.consent) throw new Error("Consent is required");
if (data.age < 18 && !data.guardianConsent) throw new Error("Guardian consent is required");

await supabase.from("assessments").insert({
  ...payload,
  consent_given_at: new Date().toISOString(),
  consent_version: CONSENT_VERSION,
  guardian_consent: data.age < 18,
});
```

## 3. Role-based access enforced in the database

Roles live in their own table. Never a `role` column on `profiles` — that is a privilege
escalation waiting to happen.

```sql
create type public.app_role as enum ('admin', 'reviewer');

create table public.user_roles (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  role public.app_role not null,
  unique (user_id, role)
);

grant select on public.user_roles to authenticated;
grant all    on public.user_roles to service_role;
alter table public.user_roles enable row level security;

create or replace function public.has_role(_user_id uuid, _role public.app_role)
returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.user_roles where user_id = _user_id and role = _role)
$$;

-- admin sees everything, reviewer only their assigned subjects
create policy "admin reads all" on public.submissions
  for select to authenticated
  using (public.has_role(auth.uid(), 'admin'));

create policy "reviewer reads assigned" on public.submissions
  for select to authenticated
  using (
    public.has_role(auth.uid(), 'reviewer')
    and reviewer_id in (select id from public.reviewers where user_id = auth.uid())
  );
```

Every new public table: `CREATE TABLE` → `GRANT` → `ENABLE ROW LEVEL SECURITY` → policies.
A table without grants is unreachable; a table without policies is silently open to nobody
or, worse, to everybody if RLS was never enabled.

## 4. Anonymous submission without a login

The subject has no account, so the write path must be a server function using a privileged
client after validating input — not an `anon` INSERT policy that lets anyone write anything.

```ts
export const submitEntry = createServerFn({ method: "POST" })
  .inputValidator(schema.parse)
  .handler(async ({ data }) => {
    const { supabaseAdmin } = await import("@/integrations/supabase/client.server");
    // validate consent, rate-limit by IP/email, then insert
  });
```

Reads by the subject: one-time token in the report URL, not an enumerable integer id.

## 5. Retention and pseudonymisation job

```sql
-- run monthly (pg_cron or a scheduled public API route)
update public.submissions a
   set subject_name  = null,
       subject_email = null,
       pseudonymised_at = now()
 from public.subjects t
where a.subject_id = t.id
  and t.relationship_ended_at is not null
  and t.relationship_ended_at < now() - interval '12 months'
  and a.pseudonymised_at is null;

-- hard delete after the full retention window
delete from public.submissions
 where pseudonymised_at is not null
   and pseudonymised_at < now() - interval '5 years';
```

Log every run. An untested retention policy is a policy you cannot demonstrate.

## 6. Erasure / withdrawal request

```sql
create table public.erasure_requests (
  id uuid primary key default gen_random_uuid(),
  email text not null,
  reason text,
  requested_at timestamptz not null default now(),
  handled_at timestamptz,
  handled_by uuid references auth.users(id)
);
grant insert on public.erasure_requests to anon, authenticated;
grant all on public.erasure_requests to service_role;
alter table public.erasure_requests enable row level security;
create policy "admins read requests" on public.erasure_requests
  for select to authenticated using (public.has_role(auth.uid(), 'admin'));
```

Withdrawal of consent must be as easy as giving it, and stops future processing without
invalidating what was lawful before.

## 7. Data export (portability)

Return structured, machine-readable data — JSON or CSV, not a PDF.

```ts
const payload = { profile, assessments, generated_at: new Date().toISOString() };
return new Response(JSON.stringify(payload, null, 2), {
  headers: { "content-type": "application/json",
             "content-disposition": 'attachment; filename="my-data.json"' },
});
```

## 8. Minimisation review

Before adding a column, answer: which purpose needs it, how long, who reads it. If any
answer is missing, do not add the column. Free-text notes fields are the most common source
of accidental special-category data — label them and restrict them.
