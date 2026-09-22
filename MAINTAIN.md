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
- Local `integration` points at that same carry commit. It is not published.
  There is no publication remote for this carry.
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
  developer instructions from `SYSTEM_APPEND.md`. Other keys in that config
  file are ignored. Project config layers are not loaded for that process.
- `--history-dir` supplies `sessions/` and `archived_sessions/`. Separate
  processes using the same history directory and different identity or
  capability directories append to that same session store.
- This does not remove Codex's other skill discovery, such as a repository
  `.agents/skills` directory or `~/.agents/skills`.

## Gate

From the carry worktree, in `codex-rs`:

```sh
just test -p codex-cli invocation_axes
```

## Consumer

No consumer is bound. Do not install this fork over the system Codex.

## Notify

No notification target. Record the carry commit in `SCRATCHPAD.md`.
