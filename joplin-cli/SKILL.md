---
name: joplin-cli
description: >-
  Read and edit Joplin notes from the terminal with the Joplin CLI (`joplin`),
  and keep the local copy safely in sync with the sync target. Use when the
  user asks to read, search, add to, or update a Joplin note or notebook, run
  `joplin sync`, or fix a "Fail-safe: Sync was interrupted" error.
---

# Joplin CLI

The CLI documents itself: run `joplin help <command>` before guessing syntax.

Each Joplin client (CLI, desktop, mobile) keeps its own local database and
exchanges data only through the sync target. A CLI profile that hasn't synced
for a while is stale. Treat the sync target as the source of truth unless the
user says otherwise.

## Always sync before and after every edit

1. Run the [preflight](#sync-preflight), then `joplin sync`.
2. Edit by note ID (see [Editing](#editing)) and read the note back.
3. Run the preflight again, then `joplin sync`.
4. `joplin status`: confirm `Conflicted: 0` and `To delete: 0`.

Read-only work also starts with a sync. If a sync fails, stop and report.

## Sync preflight

```bash
joplin status | sed -n '/Sync status/,/To delete/p'
```

Ask the user before syncing if:

- **`To delete:` is greater than 0.** These deletions go to the sync target and
  every other device. A stale profile can queue them on its own, for example
  when trash older than the retention period is purged locally.
- **The last sync was stopped by the fail-safe.**
- **The sync refuses to run because the CLI is too old.** Upgrade the CLI, then
  run the preflight again before the first sync.

## When the fail-safe fires

`Fail-safe: Sync was interrupted because N% of the data (X items) is about to be
deleted` means the sync target no longer has most of the items this profile
synced before. Nothing was deleted locally. Explain this to the user, and
disable the fail-safe only with their go-ahead:

```bash
joplin export --format jex joplin-backup-$(date +%F).jex     # backup first
joplin status | grep 'To delete'                              # must be 0
joplin config sync.wipeOutFailSafe false; joplin sync; joplin config sync.wipeOutFailSafe true
joplin config sync.wipeOutFailSafe                            # verify: true
```

Separate the three commands with `;`, not `&&`, so the fail-safe is turned back
on even if the sync fails.

Never delete notes with `joplin rmnote` to get around the fail-safe. Each
deletion is queued and pushed to the sync target.

## Sign-in

Signing in to the sync target is a browser flow the agent can't complete. Ask
the user to run `joplin sync` themselves (in Claude Code: `! joplin sync`).

## Reading

```bash
joplin ls /                    # notebooks
joplin use "<Notebook>"        # set the current notebook
joplin ls -l                   # notes in it: short ID, date, title
joplin cat <id> | tail -n +3   # body only (`cat` prints title, blank line, body)
joplin cat -v <id>             # plus metadata, including deleted_time
```

- **Titles aren't unique.** With duplicate titles, a title argument silently
  matches one note. Use IDs everywhere. The short ID from `ls -l` works.
- **Notebook note counts in `joplin status` include trashed notes.**

## Editing

`joplin edit` is interactive. Use `joplin set`, which replaces the whole body:

```bash
joplin cat <id> | tail -n +3 > note.md       # fresh body, right after syncing
#                                              change note.md, keep the rest as is
joplin set <id> body -- "$(cat note.md)"
joplin cat <id> | tail -n +3 | diff note.md - && echo OK
```

- **Always put `--` before the value.** Without it, a value starting with `-`
  (a Markdown list, for example) saves an empty body and still exits 0.
- **New note:** `joplin use "<Notebook>"`, `joplin mknote "<title>"`, get its ID
  from `joplin ls -l`, then set the body.
- **Delete:** `joplin rmnote <id>` moves a note to the trash; `-p` deletes it
  permanently. Both sync to every device, so delete only when asked.

## Testing

Never create test notes in the real profile: they sync to every device. Use a
separate profile with no sync target:

```bash
J="joplin --profile <scratch-dir>"
$J mkbook Test; $J use Test; $J mknote demo
```

## Install and upgrade

The CLI is the `joplin` npm package. Install into the same prefix as the
existing binary, and allow its native build scripts, or the `sqlite3` module
will be missing:

```bash
npm install -g joplin@<version> --allow-scripts=keytar,sharp,sqlite3
```
