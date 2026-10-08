---
name: maritime-cli
description: >-
  Operate Maritime (https://maritime.sh) from the maritime CLI: authenticate,
  create and deploy agents, set secrets, chat, schedule wakes, and debug with
  logs and exec. Use when the user mentions Maritime, maritime.sh, the
  maritime command, hosting an agent in a micro-VM, OpenClaw, Hermes,
  ZeroClaw, Claude Code on Maritime, end-user messaging, or a claim URL.
---

# Maritime CLI

Maritime hosts AI agents in serverless micro-VMs with a persistent disk at
`/data`. Agents sleep when idle and wake in about a second on the next
message or trigger. Hosting is a flat plan; asleep machines are the cheap
state. The npm package is `maritime-cli` (Node 20.12+); the command is
`maritime`.

Drive it as a program. The installed CLI is the contract. Pages such as
https://maritime.sh/docs/cli/llms.txt and https://maritime.sh/SKILL.md are a
map, and that map can be ahead of the package on disk.

## Read the manifest

Before using a flag or subcommand you have not confirmed this session:

```bash
maritime guide --json
```

The manifest is introspected from the binary, so it cannot drift from what
is installed. `maritime guide` without `--json` prints the same contract as
prose. `maritime --help` omits working commands, including `start`, `stop`,
`restart`, `sleep`, `exec`, `info`, `history`, `triggers`, `templates`, and
`open`. `maritime create --help` omits flags the parser accepts, including
`--name`, `--framework`, `--ram`, `--cpu`, `--idle`, `--always-on`, and
`--disk`. Follow the manifest.

This drift is real, not hypothetical. Checked against `maritime-cli` 1.9.0
(what `npm view maritime-cli version` reported as latest): the published
agent docs describe `maritime users`, `maritime usage`, and
`create --claim-later`, and the parser rejects all three with exit 1 and
plain text. After `npm install -g maritime-cli@latest`, read the manifest
again before using a command from the docs.

## The JSON contract

Pass `--json` on every command.

- Success: one JSON value on stdout, stderr empty.
- Failure: `{"ok": false, "error": {"code", "message", "status"}}` on stderr, stdout empty.
- Exit codes: `0` success, `1` request, server, or network, `2` auth, `3` not found, `4` usage.

Flag-parse failures stay plain text. An unknown command, unknown option, or
missing option argument exits `1` with stderr such as
`error: unknown option '--claim-later'`, including when `--json` is set.
Unparseable stderr means the invocation does not match this binary. Read the
manifest and retry. CLI-validated mistakes use exit `4` and the JSON shape
(for example `delete` without `--yes` returns `error.code`
`confirmation_required`).

`<agent>` is the exact name or an ID prefix. After `maritime init` or
`maritime link`, omit it. The CLI walks up to `.maritime/project.json`.
`maritime.json` is the committed config (name, template, persona, env keys).

`create` and `delete` never prompt. A name is enough to create, and that
spends a machine seat immediately. Delete only when the user asked, and pass
`--yes`.

## Authenticate

`MARITIME_TOKEN` is read before a saved login. It may be an `mk_` key or a
login token. `MARITIME_API_URL` overrides the API base (default
`https://api.maritime.sh`).

Stop at the first path that works:

1. `maritime whoami --json`. Exit `2` means the token is missing, expired, or wrong. A `method` of `jwt` expires at `expiresAt`. An `mk_` key does not expire.
2. No browser (sandbox, SSH, coding agent): `maritime login --device --json`. One JSON line on stderr carries `user_code` and `verification_uri_complete`. Show both to the user and wait for approval (about 15 minutes).
3. A browser on this machine: `maritime login`.
4. No account, and the user is here: `maritime signup -e <email> -p <password> -n <name> --json`. Ask for the email and password. Signup stores a token and returns `emailVerified: false`.
5. No account, and the task should continue: use `create --claim-later` only when the manifest lists that flag. It runs one agent on a temporary account for 72 hours and returns a claim URL. A template agent on that path needs its own model key, for example `-e ANTHROPIC_API_KEY=...`.

Until the user clicks the link Maritime emailed them, `create`, `deploy`,
`start`, `restart`, `keys create`, and computer creation fail with status
`403` and `error.code` `email_not_verified`. Ask them to open the email.
`maritime login --resend` sends the link again. Then retry the same command.
`list`, `status`, `logs`, and `templates` work before verification.

For unattended work, after the account is verified:

```bash
maritime keys create --name my-agent --json   # raw_key (mk_...) is shown once
export MARITIME_TOKEN=mk_...
```

Keep keys, tokens, and env values out of the chat. Store secrets with
`maritime env set`.

## Billing

A plan caps the number of machines. An agent counts as one machine, and so
does a Computer. The free plan includes 3. A refused create exits `1` with
`error.status` `402` and a server `error.code`, usually `seat_limit`. Show
`error.message` as Maritime wrote it. It already names the fix and links to
https://maritime.sh/billing.

Confirm with the user before `create`, `delete`, `keys create`, `--always-on`,
and RAM or disk above the included 2 GB / 5 GB SSD.

`create --count <n>` (2–50) names the agents `<name>-1` through `<name>-n`.
Exit `0` means every agent was created. Exit `1` means some or all failed.
With `--count`, the manifest allows `--template`, `--idle` / `--always-on`,
`--repo`, and `-e` / `--env`. Other create flags exit `4`. The JSON body has
`created`, `failed`, and `requested`.

## Deploy

```bash
maritime templates --json
maritime create my-agent --template openclaw -e OPENAI_API_KEY=sk-... --json
maritime status my-agent --json
maritime chat my-agent "introduce yourself" --json
```

Read `envRequired` from `templates --json` and set those secrets first. On
the template list fetched while writing this skill, `openclaw` and `hermes`
require `OPENAI_API_KEY`, `claude_code` requires `ANTHROPIC_API_KEY`, and
`zeroclaw`, `codex`, and `dsh` require none. Fetch the list again; it changes.
The reply text is `.response`. Poll `status` until it is `active`. `sleeping`
after idle is healthy. Sleeping agents wake on the next chat.

Own code, any framework, Dockerfile at the repo root:

```bash
maritime create my-bot --repo https://github.com/you/agent --json
maritime deploy my-bot --source github --repo https://github.com/you/agent --branch main --wait --json
```

Builds often take one to three minutes. `maritime history <agent> --json`
includes `buildLog`. Private GitHub repos need the Maritime GitHub App.

Custom container contract (https://maritime.sh/docs/frameworks/custom.md):

- Listen on `0.0.0.0:$PORT`. `PORT` is injected. Hardcoding `8080` collides with the VM port forwarder.
- `GET /health` returns any 2xx, quickly, with no side effects.
- `POST /chat` accepts `{"message":"..."}` and replies within 30 seconds with plain text or JSON. Accepted fields, in order: `response`, `reply`, `message`, `text`, `output`.
- Persist under `/data` only. The process is snapshotted and resumed, so re-open long-lived connections lazily.
- Install `ca-certificates` on slim images.
- Use an exec-form `CMD` that starts a real program. A shell-string `CMD` is flattened and the VM fails to boot.
- A custom image starts with no LLM key. Bring a secret, or turn on Maritime's proxy (`OPENAI_API_KEY` plus `OPENAI_BASE_URL`).

A public web app skips the chat contract. It sleeps when idle and wakes on the next visit:

```bash
maritime create my-app --repo https://github.com/you/app --public --port 3000 --json
```

`maritime init <name>` writes `maritime.json`, creates the agent, and links
this directory (default template `openclaw`). `--no-create` only writes the
files. `maritime deploy` in a linked directory reconciles the agent to
`maritime.json` and ships it.

## Env, schedules, end users

Values are secret by default and apply on the next boot. `--reload`, or
`maritime env reload <agent>`, pushes them into the running agent.
`env set` marks a plain value with `--no-secret`. `env import` marks plain
values with `--plain`.

```bash
maritime env set my-agent OPENAI_API_KEY=sk-... --reload --json
maritime env import my-agent ./prod.env --reload --json
maritime env list my-agent --json
maritime restart my-agent --json
```

`env pull` writes a local `.env` with secret values masked.

Timers inside a sleeping VM do not run. Put scheduled work on a platform trigger:

```bash
maritime triggers create my-agent --type cron --cron "0 9 * * *" --prompt "Send the morning summary" --json
```

`--type` is `webhook`, `cron`, `telegram`, or `discord`. `--prompt` is
cron-only and capped at 2000 characters. A custom container can serve
`GET /schedules` instead, and Maritime registers the wakes. Details:
https://maritime.sh/docs/triggers

To speak as one of the product's end users (the same `--user` reaches the same instance):

```bash
maritime message my-agent --user cust_42 "where is my order?" --json
```

`--wait` defaults to 30 seconds and accepts 0–60. `status` `replied` carries
`.reply`. `provisioning` or `queued` means the reply arrives later on the
`message.reply` webhook. When `users` is absent from the manifest, per-customer
agents, spend caps, and browser `eu_` tokens belong to the SDK
(`npm install maritime-sdk` or `pip install maritime`, key in
`MARITIME_API_KEY`): https://maritime.sh/docs/build

Computers (a desktop per end user) are documented at
https://maritime.sh/docs/computers.md. Use a CLI computers command only after
the manifest lists it.

## Debug

```bash
maritime list --json
maritime info my-agent --json
maritime logs my-agent --level error --json
maritime history my-agent --json
maritime exec my-agent ls /data --json
```

`exec` prints combined output on `.stdout`, waits until the command finishes,
and uses a 60-second timeout. It has no detach flag and no timeout flag.
Detached submit, fetch, and cancel are the REST API:
https://maritime.sh/docs/api#exec
A null or omitted API timeout means 60 seconds when attached and 3600 seconds
when detached. On agents that support detached exec, dropping the connection
leaves the command running. After a lost response, assume the command may
already be in progress. Older agents return HTTP 501
`unsupported: outdated vm` for detached submit. A restart does not add
detached exec; create a new agent for that.

`error.code` `agent_unavailable` on chat means the agent is stopped.
`maritime start <agent>`, wait a few seconds, and retry the chat. A 404 or
"not running" on exec or files means the agent is asleep or has errored.
Start it and retry. Keep the same agent.

`logs --follow` streams. Prefer a bounded `logs -n` unless the user wants a tail.

## When you are done

Tell the user the agent name, the status, the dashboard
(https://maritime.sh/agents), what you changed, and any claim URL with its
expiry.

When a documented flag and this CLI disagree, or a failure says nothing about
what to do next, send feedback with any `mk_` key. Put `X-Request-Id` in
`requestId` when the failing call returned one. Set `tool` to the client you
are. Leave out keys, tokens, and env values.

```bash
curl -X POST https://api.maritime.sh/api/v1/feedback \
  -H "Authorization: Bearer $MARITIME_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"kind":"cli","subject":"maritime env set","message":"what failed and what you expected","tool":"cursor"}'
```

`kind` is one of `docs`, `sdk`, `api`, `cli`, `computers`, `dashboard`, `other`.
The account cap is 5 reports a minute and 20 a day.
https://maritime.sh/docs/sdk/feedback

## Reference

- Setup order: https://maritime.sh/agents.md
- Human CLI reference: https://maritime.sh/docs/cli
- Driving Maritime from an agent: https://maritime.sh/docs/ai-agents
- REST API: https://maritime.sh/docs/api
- Docs index: https://maritime.sh/llms.txt
