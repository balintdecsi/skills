---
name: bitwarden-cli
description: >-
  Install, configure, log in, unlock, and use the Bitwarden CLI (`bw`) for vault
  items, passwords, and sync. Use when the user asks to set up Bitwarden CLI,
  unlock a vault, fetch a login from Bitwarden, sync the vault, or target a
  regional server such as Bitwarden EU (`vault.bitwarden.eu`).
---

# Bitwarden CLI

Prefer `bw` over pasting secrets into chat or storing master passwords in agent
memory. Never echo a master password, session key, TOTP, or item password in a
user-visible message. Prefer `--passwordenv` / `--passwordfile` and
`BW_SESSION` over putting secrets on the command line.

Run `bw help <command>` before guessing flags.

## Install (Linux x86_64)

```bash
TAG=$(curl -fsSL https://api.github.com/repos/bitwarden/clients/releases?per_page=30 \
  | python3 -c "import sys,json; print(next(r['tag_name'] for r in json.load(sys.stdin) if r['tag_name'].startswith('cli-')))")
VER=${TAG#cli-v}
curl -fsSL -o /tmp/bw.zip \
  "https://github.com/bitwarden/clients/releases/download/${TAG}/bw-linux-${VER}.zip"
unzip -o /tmp/bw.zip -d /tmp/bw-install
sudo install -m 755 /tmp/bw-install/bw /usr/local/bin/bw
bw --version
```

Use `bw-linux-arm64-*.zip` on arm64. Alternative: `npm i -g @bitwarden/cli`.

## Server region

Default cloud is US. For EU:

```bash
bw config server https://vault.bitwarden.eu
bw config server   # confirm
```

Changing server while logged in requires `bw logout` first.

## Login (non-interactive)

```bash
export BW_PASSWORD='…'   # from a secure prompt / one-time file, never chat logs you keep
bw login "$EMAIL" --passwordenv BW_PASSWORD --raw
unset BW_PASSWORD
```

Save the printed session key as `BW_SESSION` (or write it to a mode-`600` file and
`source` an env snippet). Status should become `unlocked` after a successful
login with `--raw` session export.

### New-device email OTP

A first login from a new machine often prompts:

`New device verification required. Enter OTP sent to login email`

That code is emailed to the login address. It is **not** the same as 2FA
`--method` / `--code`. Drive the prompt through a PTY (or feed stdin) once the
OTP arrives; each login attempt may send a new code — use the newest unread
Bitwarden verification email.

Example pattern: spawn `bw login … --raw` under a PTY, wait until the OTP prompt
appears, read the latest mail from `no-reply@bitwarden.eu` (or `@bitwarden.com`),
write the six-digit code into the PTY, then capture the session key from
`--raw` output.

### Two-step login (authenticator / email 2FA)

When the account uses classic 2FA (not only new-device verification):

```bash
bw login "$EMAIL" --passwordenv BW_PASSWORD --method 0 --code "$TOTP" --raw
# methods: 0 Authenticator, 1 Email, 2 Duo, 3 YubiKey, …
```

### API key login

```bash
bw login --apikey   # uses BW_CLIENTID and BW_CLIENTSECRET
```

## Session lifecycle

```bash
bw status                 # unauthenticated | locked | unlocked
bw unlock --passwordenv BW_PASSWORD --raw   # when locked; refresh BW_SESSION
bw sync                   # after unlock, before trusting list/get
bw lock                   # destroy session keys
bw logout                 # end account session on this machine
```

Persist `export BW_SESSION=…` in a mode-`600` file under
`~/.config/Bitwarden CLI/` (or equivalent) so later shells can `source` it.
After `unlock`, previous session keys are invalid.

## Read vault data

```bash
bw sync
bw list items --search 'github'
bw get item '<id-or-name>'
bw get username example.com
bw get password example.com
bw get totp example.com
bw list folders
bw list collections
```

Pipe JSON through `jq` / Python; never paste secret fields into chat. When an
outer product vault or form-fill tool exists, prefer it for typing passwords into
browsers; use `bw` for automation and for accounts that live only in Bitwarden.

## Safety

- Do not store the master password in agent durable memory or in a shared skill.
- Scrub temp password/OTP files after login (`shred` or `rm` mode-`600` paths).
- Do not commit `data.json`, `session.key`, or `session.env`.
- Confirm before `bw export`, bulk `delete`, or org-wide changes.
