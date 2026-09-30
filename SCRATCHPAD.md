# Scratchpad

## Completed worktree retirement, 2026-09-30

- The operator confirmed no Workshop work remained active and authorized
  retiring the preserved maintenance and release-speed worktrees. All 11
  completed trees were quiescent and matched the full, hash-verified recovery
  backup before retirement through their actual common Git repositories.
- Retired trees reclaimed 2.49 GiB internally. All branch refs and unpublished
  commits remain; detached release-speed HEAD `02f19c94dca76710a5857ddb30c697b30819a119`
  is anchored at `archive/release-speed/codexnk-codex-20260930`. The untracked
  skills snapshot has an individually hash-verified archived copy; ignored
  content remains recoverable from the complete Scratch backup.
- No historical codexnk Workshop-related worktree remains. This supersedes the
  retention disposition below, not its historical evidence. Retirement receipt:
  `/Volumes/Scratch/archive/codexnk-relocation-20260930T154531Z/historical-worktree-retirement.json`.
  Installed packages, consumer pins and unrelated application worktrees were
  untouched. The receipt-writing task worktree is retired after this entry lands.

## Workshop relocation and cycle disk lifecycle, 2026-09-30

- The coordinating agent completed and byte/Git-state verified relocation to
  `~/workshops/codexnk/fork` and `~/workshops/codexnk/worktrees/`, repairing all
  four common repositories' worktree registrations. Recovery and before/after
  evidence: `/Volumes/Scratch/archive/codexnk-relocation-20260930T154531Z/`.
  Historical entries below retain their original paths and observations.
- Active Workshop docs and script defaults now resolve the canonical Workshop's
  `fork/`, including from linked Workshop worktrees; the explicit checkout
  override remains available. Ignored local fork/worktrees and Python bytecode
  stay outside Workshop commits; existing bytecode is preserved.
- `scripts/cycle.py` owns new cycle output only: one shared Scratch target,
  non-incremental builds by default, automatic idle temporary cleanup, mandatory
  phase checkpoints and final output cleanup after evidence is saved. Matching
  ownership receipts, cycle locking and open-file inspection bound destructive
  cleanup. Evidence stays under Scratch's archive; legacy caches are not adopted.
- Every `/maintain` now reviews retained completed worktrees at startup and
  retires finished cycle-owned worktrees after delivery through their actual
  common repositories. Detached commits and untracked/ignored evidence must be
  preserved first; active or unfinished trees get an explicit retention handoff.
  Source retirement is coordinator-owned and separate from target cleanup.
- Verification: four destructive-boundary/lifecycle tests, 17 existing
  installer tests, shell syntax, linked-worktree/default-override path checks,
  and the project docs check passed. A tiny real Scratch command completed its
  checkpoint/final lifecycle with empty output and preserved evidence under
  `/Volumes/Scratch/archive/codexnk-cycles/relocation-policy-proof-20260930T160549Z/`.
  No Codex build, release publication, runtime restart or source-tree retirement
  was performed by this tooling change.
- Parent-review follow-up: reconciliation now resolves `MAINTAIN_WORKSHOP` to
  the canonical Workshop as well as resolving the fork there. Linked-worktree
  `--print-model` and `--check-supervision` pass; the explicit fork override
  remains valid and supervision config was verified unchanged. Cleanup now
  unlinks symlink entries inside target/tmp without following them, while still
  rejecting redirected owned roots. The updated boundary test failed against
  the prior implementation and passed after the fix, preserving an open outside
  sentinel through directory/file/dangling-link removal. All four cycle tests,
  shell syntax, project docs and diff checks passed again.
- Parent acceptance: all four cycle tests and 17 installer tests passed in the
  integrated task worktree. Canonical default-path and supervision checks passed;
  pinned read-only branch reconciliation preserved the captured upstream and
  published Integration/carry heads. The historical Scratchpad body is unchanged.
- Removed the idle, ownership-verified legacy cycle target
  `/Volumes/Scratch/codexnk-maintain-20260929-vutj0aww-target`, reclaiming
  52.98 GiB on Scratch. The relocation archive holds the cleanup receipt and a
  full source/worktree recovery backup. Installed package and vendor hashes,
  unpublished commits and untracked evidence remain preserved.
- The 11 historical maintenance/release-speed worktrees remain intact under the
  explicit preservation handoff. Their exact inventory, retention owner and
  next-cycle retirement review are recorded in `retained-worktrees-handoff.json`
  in the relocation archive above. The next `/maintain` coordinator must apply
  the mandatory retirement workflow; retaining a branch does not require keeping
  its worktree.
- This changes Workshop policy/tooling only. Public `main` remains
  `b1e72963c3b71a9265a551e54beff078384efed9`, Integration remains
  `3aae20d1ad1d41734b7303b4f0a4bfe95eb56d8c`, and release `codexnk-v0.1.7`
  and all consumer pins remain unchanged.

## Relocation handoff: READY, 2026-09-30

The operator assigned this session coordination of relocation readiness. This
section supersedes the earlier NOT READY observations below. Maintenance is
delivered and the source/worktrees are quiescent for the relocation agent.

- Verified identities and gracefully stopped all six orphan test processes:
  35693, 39772, 44576, 79234, 79200 and 79208; confirmed they exited.
- Rebound session `ses_f11c2434effeqFYM5aVs0b8nRY` to `/Users/arthack`.
  Evicted the old Integration location from the shared OpenCode server. An idle
  standalone frontend repeatedly recreated its old services, so its absence of
  active sessions was verified before gracefully closing frontend 1694 and its
  server 1695. The current shared-server conversation and other active session
  were preserved. Final `lsof` inspection found zero handles/cwds under the fork,
  codexnk worktree tree or cycle Scratch target.
- Physical relocation belongs to the receiving agent:
  `~/source/openai--codex-codexnk` → `~/workshops/codexnk/fork`, and
  `~/worktrees/codexnk/` → `~/workshops/codexnk/worktrees/`.
  Preserve both maintenance and release-speed worktrees and their branch/detached
  state. The agentstart, stack and workshop task worktrees belong to three other
  common Git repositories; repair their registrations in those repositories too.
  Update active Workshop path defaults/docs as part of relocation; historical
  evidence retains original paths. No checkout has been moved by this session.
- Preservation inventory, all four repositories' refs/worktree registrations,
  process-stop receipts and final quiescence evidence are under
  `/Volumes/Scratch/archive/codexnk-maintain-20260929-completed-20260930T125013Z/`.
  Preserve the invocation worktree's untracked skills `.snap.new` (hash recorded
  in `relocation-worktree-inventory.json`) and canonical Workshop's untracked
  `scripts/__pycache__/`. AgentStart's unrelated fleet-map edit and Stack's local
  unpublished history remain outside the move and must be preserved.
- Installed v0.1.7 and vendor Codex bindings are independent of these source
  paths. Cycle Scratch build cache is now unused; its removal is optional cleanup,
  not a relocation prerequisite. Keep backups/recovery archives on Scratch.

## Delivered baseline: v0.1.7, 2026-09-30

- On 2026-09-29 (2026-09-30 UTC), one atomic push using the original cycle leases
  published upstream mirror `b1e72963c3b71a9265a551e54beff078384efed9`, Integration
  `3aae20d1ad1d41734b7303b4f0a4bfe95eb56d8c`, invocation carry
  `73c2f483b8e9d64fdc7ea7ec8d9e54b2ed7ff624`, middleware carry
  `b3705e387f2115b48351192a3394d8150e43e61d`, and runtime carry
  `c8ec723729b001d4f40232df5d249c90ffa5aa2d`. All three carries are ancestors.
  All five published refs were re-read and matched; eleven unrelated public
  heads were retained. Local declared refs now match that published graph.
  Pinned read-only reconciliation and supervision checks passed.
- [Integration CI 36655373435](https://github.com/possibilities/codexnk-codex/actions/runs/36655373435)
  and [carry CI 36655372543](https://github.com/possibilities/codexnk-codex/actions/runs/36655372543)
  both passed for those exact commits. The immutable `codexnk-v0.1.7` tag now
  points at Integration `3aae20d1ad1d41734b7303b4f0a4bfe95eb56d8c`.
  [Release workflow 36658591665](https://github.com/possibilities/codexnk-codex/actions/runs/36658591665)
  passed and published both archives. Exact-tag, archive digest/size, package
  membership/modes and metadata verification passed. The macOS archive is
  138,508,059 bytes, SHA-256 `46e16eeee574ae31289bb20a8cfd61e9d2c798b1b5c43af4582d0dca9bb98fc1`;
  Linux is 399,130,819 bytes, SHA-256 `d00f427493984f77920a609e858142e1495ab354277e63aab6dac4307f98797c`.
- The verified release is installed at `~/.local/libexec/codexnk/codex`; all three
  macOS package-file hashes match its v2 ownership receipt. Prior release packages
  and the separate vendor Codex binding are preserved. Isolated private-runtime,
  WebSocket interception/read/completion, and packaged code-mode file-read/count/
  SHA-256 checks passed. The code-mode proof disabled in-process fallback. Both
  runtime/middleware checks also passed against the installed consumer. The first
  middleware fixture used an overlong macOS temporary socket path; it passed with
  `/private/tmp`. No resident Bot or owner process was restarted.
- AgentStart `9e0aeb85527d3a697b1f9bb237187099a97e4794` is landed and pushed on
  main. Stack `10cd42698a3571056569f99808738c376af5f128` is landed on local main,
  preserving twelve prior unpublished commits; no Stack push was made. Its remote
  main remains `9ab415a6d4295e10f545ae324565e2704ed44092`. Both canonical pins now
  select v0.1.7 / `3aae20d1ad1d41734b7303b4f0a4bfe95eb56d8c`. AgentStart's unrelated
  uncommitted `skills/fleet/MAP.md` edit is preserved byte-for-byte. Consumer proof:
  AgentStart full validation, 68 Stack settings/Bots tests, four installer tests,
  plus the two real-runtime tests above. No dependency-build approvals were added.
- All nine required local gates passed after a clean candidate-only rebuild
  (333 tests). All six fixture-isolation/V8-feature controls passed on both
  candidate and captured upstream. The authorized full suite remains recorded as
  20,959 passed, nine failed, four timed out, 66 skipped. The four timeouts passed
  serially; all nine persistent failures reproduced upstream. Four were host Git
  ignores, one ambient MCP configuration, one linked-V8 feature mismatch, and three
  upstream-reproduced WebRTC/RTP timeouts. Do not describe the full suite as green.
- Post-handover pinned branch check/apply/check and supervision checks passed.
  Apply changed no published commit. Eleven unrelated public heads were retained;
  their independent Dependabot movement was observed and not overwritten.
- Relocation and cleanup are explicitly delegated to the coordinating agent.
  Keep current worktrees, test evidence and cycle caches for that handoff; do not
  remove them as normal maintenance cleanup. Backups and recovery archives belong
  under `/Volumes/Scratch/archive`. The session and any tool-service cwd bindings
  must be checked/released before physical relocation. No maintenance build,
  release watcher, test or install job remains pending after this delivery.
- Final relocation inspection still found old test-created processes 35693,
  39772, 44576 and 79234 holding the Integration CLI cwd, and Scratch test helpers
  79200/79208. Current session tool services also hold the Integration cwd;
  OpenCode session `ses_f11c2434effeqFYM5aVs0b8nRY` remains bound there. These
  processes were not stopped because cleanup is reserved for the coordinator.
  Maintenance delivery is complete, but physical relocation is **NOT READY**
  until those live bindings are released/rebound and rechecked. PID values are
  observations, not authority to stop a later process that reuses one.
  Canonical Workshop has installer-generated untracked `scripts/__pycache__/`;
  it was preserved, as was the invocation carry's untracked failed skills snapshot.
- After delivery the operator explicitly authorized reclaiming this cycle's own
  disk usage. Removed the unused internal Rust/Cargo copy and isolated test
  installation: 1.25 GiB total, leaving 47.27 GiB free internally. The large
  internal target was already absent at inspection. Installed v0.1.7 receipt
  hashes were reverified; source worktrees and live-process Scratch target remain.
  Verification records and the isolated receipt were copied and hash-checked at
  `/Volumes/Scratch/archive/codexnk-maintain-20260929-completed-20260930T125013Z/`.
  Its `cleanup-receipt.json` records exact removed paths; `evidence-sha256.json`
  binds the archived records. This later authorization changes only disposable
  artifact cleanup, not the coordinator-owned checkout relocation.

## Prior delivered baselines

- Captured upstream `main`: `e154f7b80789b742b162cf0e44de0bc021068a20`.
- Before the current publication, public `main` mirrored that commit. `carry/invocation-axes` was
  `02f19c94dca76710a5857ddb30c697b30819a119`; `carry/input-middleware`
  was `0f8797fbbe3103e0edb8c9d951c22e20fe310e26`; and
  `carry/runtime-companions` was `7939215687df51e24d39662507d4e392a3856211`.
  Public and local Integration were
  `7ffcc693c1ac3e19b688aedea2fb4b2a6afc124f`, with all three carries as
  ancestors. This already-published follow-up restored the compact macOS
  release profile after v0.1.5; it was discovered during the 2026-09-29 cycle,
  not published by that cycle. [Integration CI 36181531537](https://github.com/possibilities/codexnk-codex/actions/runs/36181531537)
  and [carry CI 36179188424](https://github.com/possibilities/codexnk-codex/actions/runs/36179188424)
  passed. The public default branch remains `integration`.
- `codexnk-v0.1.6` also points at `7ffcc693c1ac3e19b688aedea2fb4b2a6afc124f`.
  The [release](https://github.com/possibilities/codexnk-codex/releases/tag/codexnk-v0.1.6)
  was published on 2026-09-25 with both runtime archives; its existence was
  omitted from the earlier scratchpad. This cycle discovered it during tag
  selection and has not reverified those archives. The next unused patch tag
  for the maintenance candidate is `codexnk-v0.1.7`.
- `codexnk-v0.1.5` points at `f88f7d781ea78ed65fbb9f65d110ee3e4b280323`.
  [Integration CI 36100034582](https://github.com/possibilities/codexnk-codex/actions/runs/36100034582),
  [carry CI 36100034795](https://github.com/possibilities/codexnk-codex/actions/runs/36100034795),
  and [tag workflow 36157887653](https://github.com/possibilities/codexnk-codex/actions/runs/36157887653)
  passed. Both published archives passed exact-tag, asset digest/size, package
  membership, executable-mode, and metadata verification. The shipping macOS
  profile retains thin LTO and uses eight codegen units; Linux is unchanged.
  The macOS tag build step took 81m 44s versus v0.1.4's 106m 49s (25m 05s,
  about 23% faster). The separately dispatched codegen-8 benchmark took
  65m 36s. No installed package or AgentStart/Stack consumer pin was
  advanced from v0.1.4 as part of this release-speed experiment.
- `codexnk-v0.1.4` points at `f2905ff011ff8fda607e91dfdd8f13b6083b1642`.
  [Branch CI 36074724963](https://github.com/possibilities/codexnk-codex/actions/runs/36074724963)
  and [tag workflow 36076524505](https://github.com/possibilities/codexnk-codex/actions/runs/36076524505)
  passed. Both published archives passed tag, asset digest/size, exact package
  members, executable modes, and metadata verification. An isolated macOS
  installation used the published release and its code-mode `exec` read and
  counted a temporary file in the Stack Bot cwd through a local mock
  Responses provider. The isolated installation and fixture were removed.
  The verified v2 package was installed at `~/.local/libexec/codexnk/codex`
  with an exact ownership receipt, retaining the separately installed vendor
  binary and previous releases. AgentStart pin commit
  `03e161c5d0dedccfd4dae99f487483cc2eb7c830` and Stack main
  `4fabd6d968a57ed1226ebfe2c778d908f40e088b` select this tag/SHA.
  AgentStart's bound and remote main now both include its separate Devin
  commit and the pin at `dacaecf4d626de7bca2c659b752d9f919bf670ac`.
  No live Bot or owner process was restarted.
- `codexnk-v0.1.3` points at `7d341030af1c243eeb334294be31aeb3c58d233c`.
  Release workflow [36062064372](https://github.com/possibilities/codexnk-codex/actions/runs/36062064372)
  succeeded; both published archives passed tag, digest, size, and structure
  verification. An isolated macOS install passed the Stack middleware
  smoke, then the verified release was installed at
  `~/.local/libexec/codexnk/codex` on 2026-09-24 with a matching ownership
  receipt. Installed-binary runtime and WebSocket middleware tests passed.
  AgentStart `104e611b7170e1190ace5c9ee50e98b3db13f844` and Stack
  `4015bec95d52b6821f328413c49eb15a290dec20` pin that tag/SHA; neither
  an owner nor running Bots were restarted.
- The previous release `codexnk-v0.1.2` points at
  `9103c8d5162ca57717814733e66a49a2ed756e30`. Release workflow
  [35932602669](https://github.com/possibilities/codexnk-codex/actions/runs/35932602669)
  succeeded; the macOS and Linux archives passed release digest verification.
  Its isolated interception smoke and installation passed at delivery.
- `codexnk-v0.1.1` points at
  `2945e58e2fb751dcaa1957f594bbef50fbd78392`. Release workflow
  [35880396004](https://github.com/possibilities/codexnk-codex/actions/runs/35880396004)
  succeeded and its archives were verified at delivery.
- The earlier `codexnk-v0.1.0` points at
  `7bccdfb0e871681472ff9c9e2a160c4e1d479453`; before the v0.1.1 cycle,
  public `main` and its carry were `f832ae88f82a5aed86a072556e753bd253f11619`.

## Historical preparation and recovery notes: 2026-09-29

The following records earlier cycle states; the delivered baseline above supersedes
their pending-work and old consumer-pin statements. Retained for relocation handoff.

- Immutable upstream target: `b1e72963c3b71a9265a551e54beff078384efed9`.
  Captured all public heads before fetching that exact upstream object once.
  Read the full messages for the
  [215-commit interval](https://github.com/openai/codex/compare/e154f7b80789b742b162cf0e44de0bc021068a20...b1e72963c3b71a9265a551e54beff078384efed9)
  and inspected carry interactions. Groups include GPT-6.1 Sol as the default
  catalog model and GPT-5.4 removal; instant input preemption and WebSocket
  continuation; enterprise MCP authentication and policy refresh; cached MCP,
  plugin and skill discovery; Guardian context and remote message boards;
  history/SQLite performance, sandbox fixes, and TUI copy/reconnect/rendering.
  No single release note covers this interval. Independent reviews are complete;
  the credential-boundary repairs are reviewed and verified. All nine required
  exact-candidate gates passed. Full-suite triage resumed on the internal disk
  after two Scratch disconnections. Publication and hosted branch CI are complete;
  the tagged release build, verification and consumer delivery remain pending.
- Working dispositions: **0 retire, 2 repair, 1 unchanged**. Invocation axes
  needs the home-exclusion bit in upstream's new explicit config equality and
  refresh paths, plus the home filter around cached marketplace discovery.
  Those source adaptations are committed in the task carry. Input middleware's
  Core gate remains before native start/steer and upstream's new accepted-turn
  trace; that source conflict is resolved. Runtime-companion packaging replays
  unchanged. The downstream-only contribution stance is unchanged.
- Further required invocation-axes review: upstream
  [`4994306e9f80448bde85e770a0b0c93d3fee5665`](https://github.com/openai/codex/commit/4994306e9f80448bde85e770a0b0c93d3fee5665)
  enables enterprise sign-in and account-logout grant cleanup. The new
  app-server paths call `EnterpriseOAuthCredentialGuard`, whose deletion and
  login commit use `OAuthCredentialsStoreMode::Keyring` directly, bypassing
  the private runtime's file-only setting. Logout cleanup is not gated by
  `use_xaa`; a signed-in workspace with managed IdP policy can reach it.
  Enterprise credential rereads also require a keyring-backed snapshot.
  Preserve file-only three-axis isolation when repairing this interaction;
  changing only ordinary OAuth configuration is insufficient. The resumed
  independent review confirmed those paths and found marker loss when rebuilding
  retained-session and agent-role config stacks. It also found that runtime-file
  credential settings were defaults rather than enforced launch restrictions.
- The operator approved rejecting keyring-only enterprise MCP authentication in
  three-axis mode, with ordinary file-backed OAuth retained. `MAINTAIN.md` now
  states this exception. No-flags launches retain stock enterprise behavior.
  The operator also authorized a complete `just test` attempt after focused
  gates pass. This is a material narrowing of scoped enterprise support; actual
  file-backed enterprise support remains a future upstream replacement opportunity.
- A further source review found pre-existing model-provider gateway OAuth also
  uses keyring authority independently of ordinary credential modes. The operator
  approved rejecting a selected gateway-OAuth provider in three-axis mode;
  unused provider definitions and no-flags behavior remain available. This is a
  related existing credential-isolation defect, not a new upstream accommodation.
  Source repair `293b5e9b89` closes all concrete credential-review findings,
  including the selected-provider gateway guard; the independent closure review
  found no remaining defect in the patch. Regression commit `6925692ffc` reproduced
  seven intended failures before the repair, including one counted keyring-access
  attempt for each enterprise logout and unreadable identity after an ephemeral
  credential override. The repair was applied to the invocation carry at
  `7fec92c130`; all ten post-fix invocation-axis checks passed. The enterprise
  API test counted zero keyring access attempts with XAA enabled and disabled;
  the CLI launch test preserved source identity while removing runtime auth on
  logout. Scoped `just fix` passed; its three unrelated upstream unused-import
  edits were restored. Final formatting, workflow lint and diff whitespace checks
  passed. Candidate `3aae20d1ad1d41734b7303b4f0a4bfe95eb56d8c` is frozen.
- Initial blocker: `/Volumes/Scratch` was unmounted. Both `~/.rustup` and `~/.cargo`
  are symlinks into that volume. `just write-app-server-schema` failed before
  compilation with `could not create home directory: '/Users/arthack/.rustup':
  File exists (os error 17)`. `just fmt` in both modified carry worktrees failed
  at Rust formatting for the same reason; other formatter groups passed.
  `actionlint` and committed-diff whitespace checks passed for invocation axes
  and runtime companions. This initial blocker was resolved after Scratch mounted.
- Resumed after the operator mounted Scratch. Rust 1.95.0 is available and all
  five publication targets still match the original leases. Scratch has 153 GiB
  free; the cycle-owned Cargo target is
  `/Volumes/Scratch/codexnk-maintain-20260929-vutj0aww-target`.
  Stable and experimental protocol generation passed; the middleware rebase
  finished at `b3705e387f`. Middleware and runtime-companion `just fmt` passed.
  Independent middleware review found no actionable upstream-induced regression:
  interception precedes native input queueing and instant preemption, while the
  new trace records only accepted turns.
  The regenerated middleware protocol passed all 314 tests (one ignored writer).
  An initial regression compile exposed an ambiguous assertion import; the
  corrected baseline run also includes credential overrides and selected-gateway
  coverage. The additional owned `credential-repair` worktree retains the reviewed
  source commit. Workflow conflict resolution retains runtime companions, compact
  release profiles, timing artifacts and read-only benchmarks, and adds the two
  new scoped-auth/config regression gates. All nine exact-candidate focused gates
  passed via the evidence directory's `run-candidate-gates.py`. The authorized
  complete `just test` finished with 20,959 passed, nine failed, four timed out,
  and 66 skipped (20,972 run). Receipts and per-command logs are retained there.
- The 13 full-suite failures/timeouts were rerun serially with canonical
  `TMPDIR`. All four daemon timeouts then passed; the nine failures persisted.
  Bounded independent read-only reviews identified:
  - Four worktree fixtures inherit the host's global `.codex` Git ignore rule.
    CLI/TUI fixtures silently fail to commit their destination config; exec's
    explicit `git add .codex/config.toml` reports that it is ignored. The owner
    binding assertions passed before these failures. A focused retry should set
    `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=core.excludesFile`, and
    `GIT_CONFIG_VALUE_0=/dev/null` for the invocation, leaving host config intact.
  - The skills snapshot has three extra MCP resource tools after executor
    readiness. All catalog retention assertions before the snapshot passed.
    The upstream fixture's real executor reads process-level Codex configuration;
    ambient HTTP MCP configuration is the likely cause. Compare the original
    environment with an existing empty temporary `CODEX_HOME` on both revisions.
  - V8's proof-of-concept test expects its disabled crate-level sandbox feature
    to match the sandbox-enabled linked V8 archive. Three voice-host WebRTC/RTP
    tests time out. Their source and dependency declarations are unchanged from
    captured upstream; baseline execution is still needed to close triage.
  The full-suite compilation log records candidate `integration` paths for Core
  and test support; the skills snapshot writer reports the sibling invocation
  worktree path. Preserve that provenance detail when comparing baseline results.
- An additional owned `upstream-baseline` worktree is pinned at captured
  `b1e72963c3b71a9265a551e54beff078384efed9`. Its nine-case comparison could not
  start: Rust reported `could not create home directory: '/Users/arthack/.rustup':
  File exists (os error 17)`. `/Volumes` now contains only `Macintosh HD`;
  `/Volumes/Scratch` is absent and both Rust-home symlinks are dangling again.
  This second disconnect led the operator to authorize moving work to the internal
  disk and reclaiming disposable caches. Do not fetch/reselect upstream or replace
  the original publication leases.
- Internal storage is now
  `/Users/arthack/Library/Caches/codexnk-maintain-20260929-vutj0aww/`.
  It owns a copied Rust 1.95.0 toolchain, Cargo registry/Git sources, verified V8
  artifacts, and a fresh targeted Cargo build directory. Process-local
  `RUSTUP_HOME`, `CARGO_HOME`, and `CARGO_TARGET_DIR` are recorded in the evidence
  directory's `internal-build-env.json`; `internal-rust.py` applies them and
  checks for at least 8 GiB free before a build. Global Rust-home symlinks are
  unchanged. Offline macOS Cargo metadata resolved 1,268 package manifests with
  no Scratch paths. Internal free space was 30.36 GiB before rebuilding.
  `run-internal-baseline.py` completed bounded baseline tests sequentially,
  recording free space and command results between builds. All nine persistent
  failures reproduced on the captured upstream with the same failure messages;
  its snapshot writer correctly named `upstream-baseline`. The baseline controls
  passed all six cases: four worktree cases with a process-local Git-ignore
  override, the skills case with an empty `CODEX_HOME`, and the V8 case with its
  `sandbox` feature matching the linked archive. The three WebRTC/RTP failures
  remain upstream-reproduced timeouts, not an identified carry regression.
- Switching the shared internal Cargo target from upstream to Integration exposed
  stale cross-worktree artifacts: CLI compilation could not see the carry's
  `LoaderOverrides.exclude_home_capabilities` field even though it exists in
  the candidate source. All 159 workspace packages were cleaned (7.6 GiB),
  retaining third-party dependencies. The target is now bound to the exact
  Integration worktree/SHA via `cycle-source.json`. All nine required gates and
  the candidate fixture-isolation controls passed after rebuilding; distinct
  `candidate-internal-gate-*` logs preserve the earlier receipts. Free space
  after cleanup was 24.77 GiB. The 8 GiB guard paused twice between commands;
  reclaimed only completed cycle test executables and resumed from retained
  passing receipts. All nine required gates passed (333 tests), as did the six
  candidate isolation/feature-control cases. Free space after the final local
  check was 8.38 GiB. No source repair was made for this cache issue. The complete
  suite's original failing status is retained; it is not claimed green.
- With the operator's cache-cleanup authorization, removed regenerable Bazel/Zig
  caches, Homebrew download/pip caches, UV's cache, and four abandoned July/August/
  September runtime-download staging directories with no open handles. Ran PNPM's
  own store-prune command. Installed runtimes, active tools and repository source
  were retained. Cleanup receipts are in the cycle evidence directory. The old
  53 GiB Scratch target remains a recovery cache; it is not the active build path.
- Consumer preparation uses additional owned `agentstart` and `stack` worktrees.
  AgentStart starts at `fa6ff5075cbde11010cf67a51a63481c2da4c809`; Stack starts
  at local main `952ecb3fc04f7f352c66fa421e5cc7f9e5fe62b6`, seven commits ahead
  of its public main `9ab415a6d4295e10f545ae324565e2704ed44092`. Preserve those
  unrelated unpublished Stack commits when aligning its local consumer pin;
  publishing them is not part of this cycle. Proposed v0.1.7/candidate pin changes
  exist only in those task worktrees. Stack's updated settings-schema and Bots
  checks passed (68 passed, two live-runtime tests skipped); its installer checks
  passed all four cases after updating the exact-pin fixture. AgentStart validation
  passed with canonical `TMPDIR` after an unrelated notification test compared
  `/private/var` and `/var` spellings of the same temporary path. Prepared local
  consumer commits are AgentStart `74fe5a3` and Stack `0ba88b3`; neither is landed.
  The macOS V8 150.4.0 archive and bindings passed the repository-pinned manifest
  checksum and both artifact checksums, ready for the focused build gates.
- Retained worktrees under `~/worktrees/codexnk/maintain-20260929/`:
  `invocation-axes` on `carry/cycle-20260929-invocation-axes` at
  `73c2f483b8e9d64fdc7ea7ec8d9e54b2ed7ff624`; `runtime-companions` on
  `carry/cycle-20260929-runtime-companions` at
  `c8ec723729b001d4f40232df5d249c90ffa5aa2d`; `input-middleware` on
  `carry/cycle-20260929-input-middleware` at
  `b3705e387f2115b48351192a3394d8150e43e61d`; and `integration` at the frozen
  candidate above. The `credential-repair`, `upstream-baseline`, `workshop`,
  `agentstart`, and `stack` worktrees are also cycle-owned. All pre-existing
  release-speed worktrees remain.
  As approved, after successful publication the clean release-speed
  `codexnk-codex` worktree was detached at its existing `02f19c94dc`, preserving
  its files while freeing the declared local carry ref for reconciliation.
- Leases, upstream fetch receipt, interval inventory, failed schema log and
  final read-only reconciliation are retained in
  `/private/var/folders/9g/l0rgs8rs2_9__kqn0smr9tnh0000gp/T/opencode/codexnk-maintain-20260929-vutj0aww/`.
  The workshop's pre-existing installer bytecode cache was preserved there
  as `preexisting-installer-pycache` to establish a clean workshop. Rust build
  artifacts are confined to the cycle-owned internal and prior Scratch targets. Initial
  disposable formatter environments were removed before resumption.
- Publication targets were re-read and match the starting leases. The pinned
  final read-only branch check passed, retaining eleven other public heads
  (including a newly observed unrelated Rust-toolchain Dependabot branch). Supervision
  had the old `~/code/codexnk` path; the declared entrypoint reconverged it to
  `~/workshops/codexnk` and `--check-supervision` passed. No branch apply was run.
  The installed v0.1.4 package passed its per-file ownership hashes, modes and
  metadata checks; AgentStart still pins its exact tag/SHA. Public refs have now
  advanced to the gated candidate and the v0.1.7 tag was created after hosted
  branch CI passed. Consumer bindings retain the delivered baseline above.

## Audited upstream frontier

- Complete through `b1e72963c3b71a9265a551e54beff078384efed9` on 2026-09-30.
  Reviewed all 215 commits since `e154f7b80789b742b162cf0e44de0bc021068a20`:
  [audited interval](https://github.com/openai/codex/compare/e154f7b80789b742b162cf0e44de0bc021068a20...b1e72963c3b71a9265a551e54beff078384efed9).
  Groups: GPT-6.1 Sol default/GPT-5.4 removal, instant input preemption,
  enterprise auth/policy refresh, cached capability discovery, Guardian and remote
  message boards, history performance, sandbox and TUI fixes. No single release
  note covers the interval. Dispositions: **0 retire, 2 repair, 1 unchanged**.
  Downstream-only stance remains; approved material scope narrowing rejects
  keyring-only enterprise MCP and selected model-provider gateway OAuth in
  three-axis mode. Ordinary runtime-file MCP OAuth and no-flags behavior remain.

Previous frontier:

- Complete through `e154f7b80789b742b162cf0e44de0bc021068a20` on
  2026-09-24. The previous frontier was
  `30fc6864cc1318121eca1843c217fe00ce1212f1`.
- [Aggregate interval](https://github.com/openai/codex/compare/30fc6864cc1318121eca1843c217fe00ce1212f1...e154f7b80789b742b162cf0e44de0bc021068a20):
  130 commits. Notable groups: native Unix/Linux process launching and
  executor capability-discovery V2 infrastructure (not yet dispatched);
  project-trust lookup and MCP OAuth client secrets; app-server prewarm,
  attestation, and network-policy repairs; paginated history by default and
  Guardian retained-authorization changes; diagnostic telemetry and logs;
  TUI clipboard, Markdown copy, and prompt suggestions. No single upstream
  release note covers this exact interval. Neither carried launch axes nor
  input middleware became upstream behavior.

## Carry: invocation axes

- Current published tip: `73c2f483b8e9d64fdc7ea7ec8d9e54b2ed7ff624`, integrated
  at `3aae20d1ad1d41734b7303b4f0a4bfe95eb56d8c`. **Repair**: preserve launch
  restrictions across config equality, retained-session refresh and agent-role
  reconstruction; filter cached home marketplaces; enforce runtime-file credential
  storage and approved enterprise/gateway exclusions. Ten regression checks passed
  after seven intended pre-fix failures; exact-candidate/hosted/release checks pass.
  The gateway guard also repairs a pre-existing credential defect. Prior history:

- Current published carry tip `02f19c94dca76710a5857ddb30c697b30819a119`
  restores the compact upstream release profile after the eight-codegen-unit
  experiment, retaining release timings and non-publishing profile benchmarks.
  Its behavioral commit is `154c48569b4df5e4319b55f7745461d37fee2a23`.
  The carry is based on the delivered upstream baseline and is an ancestor
  of public Integration. Historical
  upstream reference: `40eeb6e8a89ef421c25d4c40e06fa1d40ce66b4f`.
- Disposition: **repair**. The launch split remains necessary. The carry now
  excludes home-level skill and personal marketplace discovery while retaining
  copied selected skills, trusted project config/MCP and project skills. Only
  `[mcp_servers]` and `[projects]` are copied from the selected config. The
  upstream project-trust lookup changes and new executor discovery path were
  audited; discovery V2 is not yet connected to RPC dispatch.
- Stance: the downstream-only launch split remains necessary, with a narrower
  ambient-capability contract. Retire it only after upstream code and a focused
  run satisfy all three axes and their isolation rules. No upstream offer is
  planned.
- Proof: the freshly built three-axis app-server exposed selected and trusted
  project skills/MCP while excluding the prior Codex home; the local CLI gate
  passed four tests, and config, skills, and plugin discovery checks passed.
  Hosted carry and Integration branch CI succeeded for the exact published
  commits; the v0.1.3 release, isolated smoke, and installed-binary tests passed.
- Follow-up: the current `TempDir::keep()` leaves the private runtime home,
  including its copied `auth.json`, after process exit. A later carry repair
  should make that directory's lifetime match the app-server process.

## Carry: input middleware

- Current published tip: `b3705e387f2115b48351192a3394d8150e43e61d`, integrated
  at `3aae20d1ad1d41734b7303b4f0a4bfe95eb56d8c`. **Repair**: adapt the gate to
  upstream's native start/steer and accepted-turn trace, preserving interception
  before native dispatch. Stable/experimental exports regenerated. Protocol,
  WebSocket ownership/journal and realtime gates and installed interception pass.
  Prior history:

- Exact carry `0f8797fbbe3103e0edb8c9d951c22e20fe310e26` is based on the
  delivered upstream `main`. Its generated stable and experimental protocol
  exports were regenerated after replay. It was first integrated at
  `7d341030af1c243eeb334294be31aeb3c58d233c`.
- An explicit app-server WebSocket owner handles direct typed text and
  finalized realtime handoffs with `pass`, `replace` or `intercept`; no owner
  leaves stock Codex behavior. It journals dispositions in History before
  acknowledging an external effect and supports read/reconnect, explicit
  detach and bounded effect receipts. Queue, multimodal, internal input and
  utterances not delegated by realtime remain outside the gate.
- Disposition: **repair**. Upstream changed realtime context capture and
  defaulted local threads to paginated history; source conflicts were resolved
  without changing the admission journal's ownership. Local protocol,
  app-server WebSocket-owner, restart/receipt and realtime handoff checks all
  passed, as did hosted Integration and tag CI and the installed release smoke.
  A complete local `just test` was not practical within disk capacity.
  Stack's host-side client and optional
  pass-through observation UI remain; actual command-routing policy follows
  later.

## Carry: runtime companions

- Current published tip: `c8ec723729b001d4f40232df5d249c90ffa5aa2d`, integrated
  at `3aae20d1ad1d41734b7303b4f0a4bfe95eb56d8c`. **Unchanged** semantic replay:
  package layout, code-mode companion and digest-bound Linux bwrap remain needed.
  Both v0.1.7 archives and isolated host execution pass. Prior history:

- Exact carry `7939215687df51e24d39662507d4e392a3856211` is based on the
  previous captured upstream `main` and merged into Integration at
  `f2905ff011ff8fda607e91dfdd8f13b6083b1642` on top of the v0.1.3
  release source. The release workflow builds `codex` and
  `codex-code-mode-host` together and bundles digest-bound `bwrap` on Linux.
- The package-layout metadata makes Codex find the host beside the versioned
  executable even when launched through the public symlink. The workshop's v2
  receipt records every required file; installation rejects missing, redirected,
  non-executable or altered companions. A verified v1 binary-only installation
  remains an upgrade source but cannot be reused as a complete v2 package.
- `python3 tests/install.py` passed 17 cases; `actionlint` and `just fmt`
  passed. Hosted branch and tag focused tests passed, as did both tagged release
  builds and archive verification. The published macOS release passed an
  isolated code-mode file-read/count smoke in the Bot cwd. No task-owned Rust
  build caches were created locally. A complete local `just test` was not run.

## macOS release-speed experiment

- The v0.1.4 shipping build used thin LTO and four codegen units; its macOS
  build step took 106m 49s and the `codex` binary was 320,691,416 bytes.
  Cargo timing artifacts were added to release builds and opt-in, non-publishing
  macOS profile benchmarks. No tag-only sccache was added because GitHub cache
  scope prevents ordinary reuse between successive tag builds.
- [No-LTO benchmark 36082826747](https://github.com/possibilities/codexnk-codex/actions/runs/36082826747)
  took 88m 31s, but grew `codex` to 347,907,560 bytes and slowed basic
  startup tests. [Thin-LTO/codegen-16 benchmark 36089524068](https://github.com/possibilities/codexnk-codex/actions/runs/36089524068)
  took 68m 51s, grew `codex` to 384,612,728 bytes, and made `--help` about
  2 ms slower in a local comparison.
- [Thin-LTO/codegen-8 benchmark 36094945997](https://github.com/possibilities/codexnk-codex/actions/runs/36094945997)
  took 65m 36s; its `codex` binary was 355,176,888 bytes (+10.8% against
  v0.1.4) and `--help` startup was effectively tied in a 30-run local comparison
  (about 6.0 ms versus 6.1 ms). It was selected for the macOS release build.
  The tagged release's 81m 44s build demonstrates runner-to-runner variability;
  the measured shipping improvement is 25m 05s against v0.1.4, not a promise
  of the benchmark's 41m 13s improvement on every run. The local M4 Air has
  10 CPU cores/16 GB memory, but only 27 GiB free at evaluation; no local full
  build was attempted and no local-build speedup was measured.

## Cycle history

2026-09-30: Closed the 215-commit maintenance audit and delivered v0.1.7. All
required local and hosted gates passed; full-suite failures were classified with
captured-upstream controls. Atomic original-leased publication, both release
archives, isolated/installed runtime checks and consumer handover completed.
Invocation axes and middleware repaired; runtime companions replayed unchanged.
Scoped enterprise/gateway exceptions are approved in MAINTAIN.md. AgentStart pin
published; Stack pin landed locally without publishing unrelated commits. Final
reconciliation passed. Cleanup and checkout relocation are reserved for the
coordinating agent, including preservation of records under Scratch/archive.

2026-09-23: Reviewed the complete 138-commit interval above. Dispositions:
0 retired, 1 repaired, 0 unchanged. Migrated the public branch layout to a
true upstream mirror `main` and patched `integration`, and bound codexnk to
its own checkout. The previous workshop shared a checkout with codpiece.
Pinned branch reconciliation and supervision checks passed; one unrelated
Dependabot head disappeared after publication, leaving 10 other heads.
The dedicated checkout uses HTTPS with the `gh` credential helper after its
SSH key became unavailable at tag creation. Release verification and the
exact-pin macOS installation completed on 2026-09-23.
No `DELETEME/*` marker affects this cycle.

2026-09-24: Published the separate input-middleware carry and merged it into
Integration, verified `codexnk-v0.1.2` on both platforms, and activated the
aligned AgentStart/Stack pins without restarting any resident Codex
process. The local feature/build worktrees and their task-owned Rust caches
were removed after verification. The integration/workflow push used the
available SSH credential because the HTTPS OAuth token lacked workflow scope;
the push was atomic and branch reconciliation passed afterward.

2026-09-24: Audited the complete 130-commit interval from the prior frontier
to `e154f7b80789b742b162cf0e44de0bc021068a20`: 0 retired, 2 repaired,
0 unchanged. Upstream did not replace either carry. The invocation-axes
contract materially narrowed ambient home capability discovery while
retaining explicit trusted project capabilities; input middleware was replayed
through realtime/history changes and regenerated protocol exports. The exact
candidate passed all seven local and hosted focused checks. Public mirror,
Integration and the two declared carries moved in one atomic leased push;
v0.1.3 released and the verified macOS binary and consumer pins were installed
without process restarts. A separate runtime-companions cycle then advanced
public Integration and created a third carry. Local mirror and Integration
were bound to the published heads, and pinned read-only branch reconciliation
passed, classifying the new carry as `KEEP-OTHER`. No second remote apply was
run against the concurrent publication; that carry's owner will update the
declared branch model in its own cycle.

2026-09-25: Published the runtime-companions carry and v0.1.4 release after
the v0.1.3 cycle. The release corrects the missing code-mode host and includes
the Linux sandbox companion. The workshop installer and branch declaration
were updated for receipt-verified runtime packages and an isolated release
smoke. The exact tag/SHA consumer pins were subsequently published to
AgentStart and Stack, and the verified v2 package was installed without
restarting active processes. Supervision was reconverged for all three
carries and the pinned read-only branch check passed against the newer
public Integration. AgentStart's concurrent local-main divergence was merged
by its owner without losing the exact pin. No source checkout handoff remains.

2026-09-25: Benchmarked macOS release profiles, selected thin LTO with eight
codegen units, published the carry and Integration with exact-commit hosted
branch gates, and released `codexnk-v0.1.5`. Both release archives passed
verification. The shipping macOS build step improved by 25m 05s against
v0.1.4; Linux build settings and v0.1.4 consumer installation/pins were left
unchanged. Only workflow code changed; local `actionlint` and `just fmt` and
hosted focused tests passed. No complete local Rust suite was run.

2026-09-29: Captured `b1e72963c3b71a9265a551e54beff078384efed9` and reviewed
the 215-commit interval from the audited frontier. Prepared invocation-axes and
runtime-companion replays and resolved the input gate's source conflict.
Schema regeneration and Rust formatting are blocked by the unmounted Scratch
volume. The new enterprise login/logout keyring path needs an isolation repair
and completed review before candidate gating. No fork publication or consumer
handover occurred; the audited frontier remains at the previous completed
audit. Recorded the previously published compact-profile rollback, verified
the retained installed package, and corrected the derived supervision path.

2026-09-29, resumed: Completed middleware schema regeneration, credential-boundary
repairs and bounded independent reviews. The operator approved scoped enterprise
MCP and gateway-OAuth rejection while storage is keyring-only, and authorized the
complete suite. Candidate `3aae20d1ad1d41734b7303b4f0a4bfe95eb56d8c` passed all
nine required local gates. The full suite had nine failures and four timeouts;
all timeouts passed serial rechecks, while failure isolation remains in progress.
Scratch became unmounted again before the captured-upstream comparison could
compile. No fork refs, release tags, installation or canonical consumer pins were
advanced. Prepared consumer commits, owned worktrees and original leases remain
for recovery; final pinned read-only reconciliation passed.
