# Codex fork maintenance

This repository specifies a downstream fork of
[openai/codex](https://github.com/openai/codex). The fork adds launch-time
separation of identity, capabilities, and session history. It is not published
to `possibilities/codex`.

## Purpose

Keep the carried behavior below rebuilt on `openai/codex` `main`. The fork does
not overwrite the vendor Codex binary. The workshop installs a separately owned
release binary; AgentStart selects it through its managed shim.

## Upstream

- Bound checkout: `~/source/openai--codex-codexnk`. `upstream` is `openai/codex`.
  `public` is `possibilities/codexnk-codex`, the release repository. This
  checkout has no `fork` remote. Do not base or publish this effort on the
  unrelated `possibilities/codex` repository.
- Contribution stance: downstream-only. Offer nothing upstream and do not open
  an upstream pull request. Judge future upstream replacements from code and
  behavior, not request status.
- Base: one exact upstream `main` captured for each cycle.

## Branch model

- Composition model: rebased carry heads. Local and public `main` mirror the
  captured `openai/codex` `main` exactly. Public `integration` is the default
  branch and the only patched release source; local `integration` points at
  that published tip.
- Exact carry ref: `carry/invocation-axes`, the only carry. It contains the
  app-server launch split and its release workflow. Temporary carry branches
  are not publication targets. The carry tip is an ancestor of `integration`.
- Reconcile through `scripts/reconcile-branches.sh`, which delegates to the
  maintain skill's shared branch script. The public remote is `public`. Do not
  publish this effort to the unrelated `fork` remote.
- Deletion marker prefix: `DELETEME/`. Do not create one without an explicit
  request naming the branch.
- No upstream pull-request heads are validated; this fork offers nothing
  upstream. Recorded rerere resolutions are not relied on.

## Features

### Invocation axes

- On `codex app-server` only, accept `--identity DIR`, `--capabilities DIR`,
  and `--history-dir DIR`. The three flags are all present or all absent.
  Absent leaves stock `CODEX_HOME` behavior unchanged.
- One process keeps one identity and one capability set until it exits. Do not
  switch either between turns or between threads in that process.
- `--identity` supplies `auth.json` only. The file is copied into a private
  runtime directory and the identity directory is not written. Credential
  storage for that process is the file, not the OS keyring.
- `--capabilities` supplies user skills from `skills/` when that directory
  exists, MCP servers from the `[mcp_servers]` table in `config.toml`, and
  developer instructions from `SYSTEM_APPEND.md`. Skills are copied into the
  private runtime directory, so later writes do not change the capabilities
  directory. Other keys in that config file are ignored. Project config
  layers are not loaded for that process. CLI auth and MCP OAuth credentials
  for the process are stored in files under the runtime home, not the OS
  keyring.
- `--history-dir` supplies `sessions/` and `archived_sessions/`. Separate
  processes using the same history directory and different identity or
  capability directories append to that same session store.
- This does not remove Codex's other skill discovery, such as a repository
  `.agents/skills` directory or `~/.agents/skills`.

## Gate

The public repo runs only `.github/workflows/codexnk-release.yml`. Upstream
workflows copied with the tree are disabled there. OpenAI's own CI covers
code this patch does not change.

On `integration` and `carry/invocation-axes`, that workflow runs:

```sh
just test -p codex-cli invocation_axes
```

A `codexnk-v*` tag runs that test, then builds `codex` for
`aarch64-apple-darwin` and `x86_64-unknown-linux-gnu`. The package step reads
the binary from `CARGO_TARGET_DIR`, which setup-ci sets outside `target/`.

The same test command is the local check, from the carry worktree's `codex-rs`.
Gate the exact committed candidate. Hosted branch CI is checked after
publication and before creating a release tag.

## Consumer

AgentStart pins an exact stable release tag and Integration SHA and invokes:

```sh
scripts/install.sh --install --tag codexnk-vVERSION --sha FULL_COMMIT
```

The installer checks the tag's commit, GitHub asset SHA-256 and size, archive
structure, and invocation flags before atomically publishing the executable at
`~/.local/libexec/codexnk/codex`. Existing installs must match their ownership
receipts. It never launches a session, writes auth/config, or restarts processes.
`--print-bin` reports the absolute consumer path without mutation; `--check`
prints the plan. `CODEXNK_INSTALL_ROOT` relocates the private install directory
for isolated tests. Prior release directories remain for recovery. Vendor Codex
remains separate. Updating a release does not advance AgentStart's consumer pin.

Public binaries are GitHub Releases on `possibilities/codexnk-codex`. The
release workflow attaches one `codex` archive per target. The first published
tag was `codexnk-v0.1.0`. Select the next unused patch tag after the current
release recorded in `SCRATCHPAD.md`; it must point at the exact gated
Integration commit. After branch CI succeeds for that commit, run from this
workshop:

```sh
scripts/publish-release.sh "$candidate_sha" "$release_tag"
```

Wait for the tag workflow to succeed, then run from this workshop:

```sh
scripts/verify-release.sh "$candidate_sha" "$release_tag"
```

Never move an existing release tag.

## Notify

Use title `codexnk maintenance` and group `codexnk-maintain` for a material
finding or blocked gate. Record the carry and Integration commits in
`SCRATCHPAD.md`.
