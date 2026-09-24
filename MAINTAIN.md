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

- Composition model: independent carry heads based on the captured upstream
  `main`, merged into Integration. Local and public `main` mirror the
  captured `openai/codex` `main` exactly. Public `integration` is the default
  branch and the only patched release source; local `integration` points at
  that published tip.
- Exact carry refs: `carry/invocation-axes` (app-server launch split),
  `carry/input-middleware` (the opt-in human-input gate), and
  `carry/runtime-companions` (the release package workflow). Temporary carry
  branches are not publication targets. All carry tips must be ancestors of
  `integration`.
- Reconcile through `scripts/reconcile-branches.sh`, which delegates to the
  maintain skill's shared branch script. Publish the captured upstream mirror,
  new Integration commit, and the declared carry heads by one exact-leased
  atomic push to `public`, then run the
  reconciliation check against those published heads. The script validates an
  already-published Integration; it does not advance that branch. Do not publish
  this effort to the unrelated `fork` remote.
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
  exists, MCP servers from `[mcp_servers]` and project trust decisions from
  `[projects]` in `config.toml`, and developer instructions from
  `SYSTEM_APPEND.md`. Skills are copied into the private runtime directory, so
  later writes do not change the capabilities directory. Other keys in that
  config file are ignored. Trusted project config layers, project `.codex/skills`,
  and repository `.agents/skills` remain available; project trust is established
  in the private runtime, not imported from the operator's `~/.codex`. CLI auth
  and MCP OAuth credentials for the process are stored in files under the runtime
  home, not the OS keyring.
- `--history-dir` supplies `sessions/` and `archived_sessions/`. Separate
  processes using the same history directory and different identity or
  capability directories append to that same session store.
- A three-axis launch excludes home-level `~/.agents/skills` and personal plugin
  marketplaces under home dot-directories. It does not change `HOME`, system or
  managed policy, bundled capabilities, explicit runtime selections, or Codex's
  ability to read ordinary files. Absent flags retain stock discovery.

### Input middleware

- App-server v2 exposes experimental `thread/input/middleware/attach` and
  `detach` over its existing bidirectional WebSocket (or stdio). An explicit
  attach claims one loaded retained thread for one connection; merely
  connecting or subscribing never activates it. Without an owner, Codex takes
  its stock local input path with no middleware round trip. An explicit detach
  restores it. Disconnect retains the registered pass/reject unavailable
  policy until a new owner attaches.
- The same Core gate accepts direct, single plain-text human `turn/start` and
  `turn/steer` input and finalized realtime handoff/tail text before the
  working agent starts or steers. A registered typed submission needs a stable
  `clientUserMessageId`. A handoff's existing working-agent text may include
  realtime context wrapping; the middleware sees and may replace that entire
  submitted text. This does not intercept every spoken utterance, suppress
  hosted realtime speech, or cover queued, multimodal, tool, internal or
  otherwise unmarked inputs. Unsupported registered input is rejected, not
  silently allowed to bypass the gate.
- A directed `thread/input/requestDisposition` server request accepts `pass`,
  `replace {text}` or `intercept {operationId}`; one winning result is committed
  before native dispatch. Requests to other connections cannot answer it.
  Bound timeouts and malformed replies follow the explicitly registered
  `onUnavailable: pass | reject` policy. The source identity is fenced and
  deduplicated within the thread, including after restart. A pass or replace
  means selected input, not guaranteed successful native turn dispatch.
- The history-owned `input-middleware/<threadId>.jsonl` journal stays outside
  `sessions/`, is synced before a disposition is acknowledged, and is reloaded
  on attach after process restart. `thread/input/resolved` notifies the owner;
  `thread/input/read` recovers the record; `thread/input/complete` stores an
  idempotent, bounded external effect receipt for an intercepted source.
  Retention is capped at 4096 distinct inputs per thread. A corrupt/full
  journal or storage error refuses new registered input rather than dropping
  its decision. The external effect still needs its own idempotency and
  reconciliation; Codex cannot atomically transact with another service.

## Gate

The public repo runs only `.github/workflows/codexnk-release.yml`. Upstream
workflows copied with the tree are disabled there. OpenAI's own CI covers
code this patch does not change.

On `integration`, the workflow runs the focused checks below. The
`carry/invocation-axes` branch runs the first four checks; the
`carry/input-middleware` and `carry/runtime-companions` heads are gated as
ancestors of Integration, since they do not run Integration's full check set
on their upstream-based trees.

```sh
just test -p codex-cli invocation_axes
just test -p codex-config scoped_capabilities_keep_trusted_project_mcp_without_home_config
just test -p codex-skills-extension scoped_capabilities_keep_project_skills_without_home_skills
just test -p codex-core-plugins scoped_capabilities_omit_home_marketplace_but_keep_project_marketplace
just test -p codex-app-server-protocol
just test -p codex-app-server input_middleware
just test -p codex-app-server realtime_handoff_is_intercepted_before_working_turn
```

A `codexnk-v*` tag runs that test, then builds `codex`,
`codex-code-mode-host`, and on Linux a digest-bound `bwrap` for
`aarch64-apple-darwin` and `x86_64-unknown-linux-gnu`. The package step reads
the binaries from `CARGO_TARGET_DIR`, which setup-ci sets outside `target/`.

These focused checks are the local gate, from the carry or Integration
worktree's `codex-rs`. A complete `just test` is attempted when authorized and
practical; report any system-dependency or build-capacity blocker rather than
claiming an incomplete suite passed.

Gate the exact committed candidate. Hosted branch CI is checked after
publication and before creating a release tag.

After the last local gate and release verification, run `cargo clean` in each
owned Codex build worktree used for this cycle, and remove other disposable
build artifacts made in owned worktrees. Verify the intended paths and Git
status first. Do not clean the bound/shared checkout, another worktree,
global package caches or installed release artifacts. Keep a worktree while
its branch still needs development; release cleanup does not discard source.

## Consumer

AgentStart pins an exact stable release tag and Integration SHA and invokes:

```sh
scripts/install.sh --install --tag codexnk-vVERSION --sha FULL_COMMIT
```

The installer checks the tag's commit, GitHub asset SHA-256 and size, archive
structure, package metadata, and invocation flags before atomically publishing
the executable at `~/.local/libexec/codexnk/codex`. The versioned package
contains `bin/codex`, `bin/codex-code-mode-host`, `codex-package.json`, and on
Linux `codex-resources/bwrap`. Codex's package layout resolves the helper even
when launched through the public symlink. Existing installs must match the
per-file ownership receipt; binary-only v1 receipts are accepted only as an
upgrade source. It never launches a session, writes auth/config, or restarts processes.
`--print-bin` reports the absolute consumer path without mutation; `--check`
prints the plan. `CODEXNK_INSTALL_ROOT` relocates the private install directory
for isolated tests. Prior release directories remain for recovery. Vendor Codex
remains separate. Updating a release does not advance AgentStart's consumer pin.

Public binaries are GitHub Releases on `possibilities/codexnk-codex`. The
release workflow attaches one runtime package archive per target. The first published
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
