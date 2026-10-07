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

- Bound checkout: `fork/` under the canonical Workshop (`~/workshops/codexnk/fork`).
  Persistent maintenance worktrees belong under the Workshop's ignored
  `worktrees/`. `upstream` is `openai/codex`.
  `public` is `possibilities/codexnk-codex`, the release repository. This
  checkout has no `fork` remote. Do not base or publish this effort on the
  unrelated `possibilities/codex` repository.
- Contribution stance: downstream-only. Offer nothing upstream and do not open
  an upstream pull request. Judge future upstream replacements from code and
  behavior, not request status.
- Base: one exact upstream `main` captured for each cycle.
- `scripts/reconcile-branches.sh` and `scripts/publish-release.sh` resolve the
  canonical Workshop through Git's common directory, including when invoked in
  a linked Workshop worktree. Reconciliation's `MAINTAIN_WORKSHOP` always names
  that canonical Workshop, so supervision never binds a disposable task tree.
  `CODEXNK_CODEX_CHECKOUT` overrides only the fork path. Canonical Workshop
  discovery requires its standard `.git` layout. No old-path symlink is needed.

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
- Enterprise MCP authentication is unavailable in three-axis mode while upstream
  requires keyring-backed enterprise grants. Enterprise sign-in is explicitly
  rejected and account logout does not access or clean up enterprise keyring
  grants. Ordinary MCP OAuth remains available through private runtime files.
  Config refresh and agent-role application retain these launch restrictions.
  A managed credential-storage requirement incompatible with file-only identity
  fails the scoped launch rather than replacing that policy.
- Model-provider gateway OAuth is likewise unavailable in three-axis mode while
  its upstream storage requires keyring authority. Selecting such a provider at
  launch or for a thread is rejected; unused gateway provider definitions do not
  prevent ordinary provider selection.
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
  `turn/steer` input and finalized realtime handoff/tail text before
  native submission or transcript persistence. A terminal realtime tail persists
  admitted text as history only, without inference; interception or rejection
  creates neither a transcript tail nor a working turn. A registered typed
  submission needs a stable `clientUserMessageId`. A handoff's existing
  working-agent text may include
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
`carry/invocation-axes` branch runs the first six checks; the
`carry/input-middleware` and `carry/runtime-companions` heads are gated as
ancestors of Integration, since they do not run Integration's full check set
on their upstream-based trees.

```sh
just test -p codex-cli invocation_axes
just test -p codex-config scoped_capabilities_keep_trusted_project_mcp_without_home_config
just test -p codex-skills-extension scoped_capabilities_keep_project_skills_without_home_skills
just test -p codex-core-plugins scoped_capabilities_omit_home_marketplace_but_keep_project_marketplace
just test -p codex-core invocation_axes
just test -p codex-app-server invocation_axes
just test -p codex-app-server-protocol
just test -p codex-app-server input_middleware
just test -p codex-app-server realtime_handoff_is_intercepted_before_working_turn
```

A `codexnk-v*` tag runs that test, then builds `codex`,
`codex-code-mode-host`, and on Linux a digest-bound `bwrap` for
`aarch64-apple-darwin` and `x86_64-unknown-linux-gnu`. The package step reads
the binaries from `CARGO_TARGET_DIR`, which setup-ci sets outside `target/`.

These focused checks are the local gate, from the carry or Integration
worktree's `codex-rs`, through the cycle helper below. A complete `just test` is
attempted when authorized and practical; report any system-dependency or
build-capacity blocker rather than claiming an incomplete suite passed.

Gate the exact committed candidate. Hosted branch CI is checked after
publication and before creating a release tag.

## Local disk lifecycle (mandatory)

Use `python3 scripts/cycle.py` for **every local maintenance cycle**. This is a
macOS helper, not a scheduler. It requires mounted `/Volumes/Scratch` and the
system `/usr/sbin/lsof`; missing storage or incomplete activity inspection is a
blocking error, never permission to use internal disk. Choose a unique cycle
name (letters, digits, `_`, `-`; at most 80 characters) and retain it throughout
the cycle. For example, from the Workshop task worktree:

```sh
helper="$PWD/scripts/cycle.py"
cycle=maintain-20261001
python3 "$helper" start "$cycle"
# From each carry/Integration worktree's codex-rs, reuse this same helper/cycle:
python3 "$helper" run "$cycle" -- just test -p codex-cli invocation_axes
python3 "$helper" run "$cycle" -- just test -p codex-core invocation_axes
# After a gate batch / before switching maintenance phases:
python3 "$helper" checkpoint "$cycle"
# At a deliberate clean-candidate rebuild boundary, after saving evidence:
python3 "$helper" checkpoint "$cycle" --clean
# After last gate, release verification and evidence handover:
python3 "$helper" final "$cycle" --evidence-saved
```

The command contract is intentionally small:

- **`start CYCLE`** exclusively creates
  `/Volumes/Scratch/codexnk-cycles/CYCLE/{target,tmp}` and matching ownership
  receipts under `/Volumes/Scratch/archive/codexnk-cycles/CYCLE`. It refuses an
  existing name rather than adopting output. Its JSON output reports these
  paths. Tiny ownership/lock records and empty output directories remain after
  final cleanup; a finalized name is not reusable.
- **`run CYCLE -- COMMAND [ARG ...]`** runs in the caller's current directory,
  with `CARGO_TARGET_DIR` set to that one target, `CARGO_INCREMENTAL=0` unless
  explicitly overridden in the environment, and `TMPDIR`, `TMP`, `TEMP` set
  to the cycle's temporary directory. All cycle worktrees share this target;
  serialize commands. Do not pass `--target-dir`, override the target in a
  child shell, or configure another Cargo build directory. An incremental
  override needs a recorded reason and phase cleanup. Shared Cargo/Rust stores
  are left alone. Exit status is preserved unless cleanup itself fails.
  Successful and failed commands both reclaim temporary output when idle;
  compiled output is retained for the next check, avoiding per-test rebuilds.
- **`checkpoint CYCLE`** is required after each gate batch, at each phase
  transition, and when resuming an interrupted cycle. It reclaims idle temporary
  output, checks build activity, and records target size. **`--clean`** also
  discards the target contents: use it when changing the captured base or
  needing an uncontaminated candidate, or at a completed phase whose cache is
  no longer useful. Save useful evidence first. Do not clean between every
  individual Cargo test. Disk pressure calls for a checkpoint and an explicit
  phase decision, not an unattended deletion loop.
- **`final CYCLE --evidence-saved`** requires confirmation that useful evidence
  has already been saved, then removes all cycle target/tmp contents and closes
  the cycle to further runs. It is required after delivery, or after an
  abandoned cycle is quiescent and its evidence is preserved. It is safe to
  repeat; it never deletes the evidence archive.

Each run archives a compact command/cwd/exit/cleanup receipt, not full build
stdout. `CODEXNK_EVIDENCE_DIR` points commands at the separate archive; save
small logs, summaries, hashes and failure fixtures there **before** the command
exits (tmp is disposable). Stream output normally, or explicitly capture a
bounded log in that directory; do not copy multi-gigabyte targets into evidence.
Do not put secrets in command arguments or receipts. Existing recovery archives
and historical Scratchpad entries remain evidence, not cleanup candidates.

Cleanup validates matching ownership receipts and exact directory identities,
rejects redirected owned roots, foreign ownership and nested mounts, holds a
cycle lock, and requires a successful system-wide open-file listing
with no handles, mapped executables or working directories in target/tmp.
Symlink entries inside target/tmp are unlinked without following them, including
dangling links and links to outside directories. Their destinations are never
cleaned. Recursive removal requires Python's symlink-safe `shutil.rmtree` support;
if unavailable, cleanup refuses before deleting output.
Commands must stay foreground and must not leave servers or detached children.
The lock serializes helper users; it does not fence unrelated processes that
ignore the helper. Ensure the whole cycle is quiescent before destructive
checkpoints; do not launch other processes into its output during inspection.
The helper never stops processes. A refusal preserves output for inspection.

On interruption or a cleanup refusal, keep the cycle name and receipts. Wait
for its commands to exit, inspect any reported PID/path, then run `checkpoint`
before continuing. A killed wrapper or unplugged Scratch can leave disposable
output behind; no signal handler can guarantee cleanup then. Never delete a
lock or rewrite an ownership receipt to force progress. A direct child retains
the lock if its wrapper exits. A missing/partial ownership receipt requires
manual recovery of that exact cycle, not automatic adoption by this helper.

Some macOS Unix-socket fixtures require a shorter path than Scratch provides.
Only those small socket fixtures may use an explicitly created, uniquely named
directory under `/private/tmp`. Keep its exact path in the cycle evidence,
scope its cleanup to that fixture, and remove it on success/failure after its
processes exit. That exception never applies to Cargo targets, large temporary
output or evidence. The cycle helper does not sweep `/private/tmp`.

Source/worktrees, untracked source evidence, shared package/Cargo/Rust caches,
installed release packages and legacy targets are outside the helper's cleanup
scope. Do not run broad `cargo clean` in historical or shared worktrees. Legacy
target removal needs a separately authorized exact-path ownership/activity
review; relocation cleanup belongs to its coordinating parent. Keep worktrees
while their branches still need development; cleanup does not discard source.

### Worktree retirement (mandatory at cycle start and handover)

Target reclamation and source worktree retirement are separate requirements.
Every `/maintain` begins by reviewing **previously completed** retained cycle
worktrees and finishes with the coordinator retiring this cycle's delivered,
finished trees. Do not treat indefinite source retention as the default cleanup
policy. Record each tree's disposition in the cycle archive and Scratchpad:
retired, or retained with an explicit reason, responsible owner and next step.
An unfinished branch, another active agent or unverified evidence is a reason
to retain and hand off that specific tree, not to skip the whole review.

The coordinator owns this workflow; `cycle.py` deliberately cannot delete
source worktrees or select candidates. Use an explicit cycle inventory, never
all directories under `worktrees/` as an implicit deletion list. A Workshop
maintenance tree can contain worktrees registered in different common Git
repositories (Codex, Workshop, AgentStart, Stack); physical location alone
does not establish ownership or the repository that must remove it.

For each exact candidate, in order:

1. Establish that the cycle owns it and its work is delivered/accepted, identify
   its actual common repository with `git -C "$tree" rev-parse
   --path-format=absolute --git-common-dir`, and record the matching entry from
   that repository's `git worktree list --porcelain`. Coordinate with any named
   owner. Canonical checkouts and another cycle's active trees are not candidates.
2. Record HEAD, branch, status and reachability. Preserve **all** branch refs and
   unpublished commits; worktree retirement never deletes branches. For a
   detached HEAD, create and verify a durable, uniquely named local ref such as
   `refs/heads/archive/<cycle>/<tree-name>` at the exact HEAD before removal.
   Do not overwrite an existing archive ref. If delivery/commit reachability is
   uncertain, retain the tree and report the missing check.
3. Inspect tracked changes plus both untracked and ignored files, using
   `git status --short --untracked-files=all --ignored` and the two explicit
   inventories `git ls-files --others --exclude-standard` and
   `git ls-files --others --ignored --exclude-standard` (use `-z` when scripting).
   Preserve source edits on an owned branch through normal review. Archive
   useful untracked/ignored evidence under `/Volumes/Scratch/archive`, recording
   source paths, file sizes and SHA-256 hashes; verify the saved copy before
   retiring its exact source copy. Never assume ignored files are disposable:
   `git worktree remove` can discard ignored content. Resolve each item;
   incomplete evidence preservation blocks removal. Preserve historical
   relocation/recovery archives unchanged.
4. Require a successful open-file/activity inspection with no process cwd,
   mapped executable or open handle beneath the exact tree; failed/incomplete
   inspection blocks removal. Coordinate release of tool-service/session cwd
   bindings and any live owner. Never stop an unrelated process to force cleanup.
5. From **outside** that tree and from its actual common repository's stable
   checkout, recheck HEAD, clean status, empty untracked/ignored inventories,
   registration and activity immediately before `git worktree remove "$tree"`.
   Use no `--force`, `rm -rf`, reset, stash, or prune as a deletion shortcut.
   Let a refusal block that candidate and preserve its state. Verify the exact
   registration/path is gone and the retained refs still resolve, then archive
   the retirement receipt.

A worker must never remove its own checkout or its parent's checkout. Return
committed work and verification first, stop writing, and hand retirement to
the coordinator after integration/delivery. Move the coordinator's session/cwd
to a stable location before removing its own completed task tree. The current
relocation handoff trees remain the relocation parent's responsibility; this
policy does not retroactively authorize a worker to delete them. Final cycle
handover is complete only when every owned tree is retired or has the explicit
retention handoff above, alongside successful `cycle.py final` output cleanup.

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
