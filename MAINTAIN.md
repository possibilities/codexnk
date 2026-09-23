# Codex fork maintenance

This repository specifies a downstream fork of
[openai/codex](https://github.com/openai/codex). The fork adds launch-time
separation of identity, capabilities, and session history. It is not published
to `possibilities/codex`.

## Purpose

Keep the carried behavior below rebuilt on `openai/codex` `main`. The fork does
not replace the system Codex binary and has no installer.

## Upstream

- Bound checkout: `~/source/openai--codex`. `upstream` is `openai/codex`.
  `fork` currently points at `possibilities/codex`; do not base or publish this
  effort there.
- Contribution stance: downstream-only. Do not open an upstream pull request.
- Base: the captured upstream `main` recorded in `SCRATCHPAD.md`.

## Branch model

- Mirror branch: local `main`, an exact mirror of `openai/codex` `main`.
- Carry branch: `carry/invocation-axes`, the only carry. It contains the
  app-server launch split and nothing else.
- Local `integration` points at the carry tip. The public release repository
  is `possibilities/codexnk-codex`. Its `main` and `carry/invocation-axes`
  are that same patched commit. Do not publish this effort to
  `possibilities/codex`.
- Deletion marker prefix: `DELETEME/`. Do not create one without an explicit
  request naming the branch.

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

On `main` and `carry/invocation-axes`, that workflow runs:

```sh
just test -p codex-cli invocation_axes
```

A `codexnk-v*` tag runs that test, then builds `codex` for
`aarch64-apple-darwin` and `x86_64-unknown-linux-gnu`. The package step reads
the binary from `CARGO_TARGET_DIR`, which setup-ci sets outside `target/`.

The same test command is the local check, from the carry worktree's `codex-rs`.

## Consumer

No local installer is bound. Do not replace the system Codex.

Public binaries are GitHub Releases on `possibilities/codexnk-codex`. The
release workflow attaches one `codex` archive per target. The release tag is
`codexnk-v0.1.0`.

## Notify

No notification target. Record the carry commit in `SCRATCHPAD.md`.
