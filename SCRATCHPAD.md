# Scratchpad

## Delivered baseline

- Captured upstream `main`: `e154f7b80789b742b162cf0e44de0bc021068a20`.
- Public `main` mirrors that commit. `carry/invocation-axes` is
  `02f19c94dca76710a5857ddb30c697b30819a119`; `carry/input-middleware`
  is `0f8797fbbe3103e0edb8c9d951c22e20fe310e26`; and
  `carry/runtime-companions` is `7939215687df51e24d39662507d4e392a3856211`.
  Public and local Integration are
  `7ffcc693c1ac3e19b688aedea2fb4b2a6afc124f`, with all three carries as
  ancestors. This already-published follow-up restored the compact macOS
  release profile after v0.1.5; it was discovered during the 2026-09-29 cycle,
  not published by that cycle. [Integration CI 36181531537](https://github.com/possibilities/codexnk-codex/actions/runs/36181531537)
  and [carry CI 36179188424](https://github.com/possibilities/codexnk-codex/actions/runs/36179188424)
  passed. The public default branch remains `integration`.
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

## Blocked maintenance attempt: 2026-09-29

- Immutable upstream target: `b1e72963c3b71a9265a551e54beff078384efed9`.
  Captured all public heads before fetching that exact upstream object once.
  Read the full messages for the
  [215-commit interval](https://github.com/openai/codex/compare/e154f7b80789b742b162cf0e44de0bc021068a20...b1e72963c3b71a9265a551e54beff078384efed9)
  and inspected carry interactions. Groups include GPT-6.1 Sol as the default
  catalog model and GPT-5.4 removal; instant input preemption and WebSocket
  continuation; enterprise MCP authentication and policy refresh; cached MCP,
  plugin and skill discovery; Guardian context and remote message boards;
  history/SQLite performance, sandbox fixes, and TUI copy/reconnect/rendering.
  No single release note covers this interval. Audit closure remains pending
  the credential-boundary review; the audited frontier below is unchanged.
- Working dispositions: **0 retire, 2 repair, 1 unchanged**. Invocation axes
  needs the home-exclusion bit in upstream's new explicit config equality and
  refresh paths, plus the home filter around cached marketplace discovery.
  Those source adaptations are committed in the task carry. Input middleware's
  Core gate remains before native start/steer and upstream's new accepted-turn
  trace; that source conflict is resolved. Runtime-companion packaging replays
  unchanged. No material change to downstream-only stance or `MAINTAIN.md`.
- Further required invocation-axes review: upstream
  [`4994306e9f80448bde85e770a0b0c93d3fee5665`](https://github.com/openai/codex/commit/4994306e9f80448bde85e770a0b0c93d3fee5665)
  enables enterprise sign-in and account-logout grant cleanup. The new
  app-server paths call `EnterpriseOAuthCredentialGuard`, whose deletion and
  login commit use `OAuthCredentialsStoreMode::Keyring` directly, bypassing
  the private runtime's file-only setting. Logout cleanup is not gated by
  `use_xaa`; a signed-in workspace with managed IdP policy can reach it.
  Enterprise credential rereads also require a keyring-backed snapshot.
  Preserve file-only three-axis isolation when repairing this interaction;
  changing only ordinary OAuth configuration is insufficient. The independent
  review was cancelled during the interrupted session and supplied no result.
- Blocker: `/Volumes/Scratch` is unmounted. Both `~/.rustup` and `~/.cargo`
  are symlinks into that volume. `just write-app-server-schema` failed before
  compilation with `could not create home directory: '/Users/arthack/.rustup':
  File exists (os error 17)`. `just fmt` in both modified carry worktrees failed
  at Rust formatting for the same reason; other formatter groups passed.
  `actionlint` and committed-diff whitespace checks passed for invocation axes
  and runtime companions. No focused Rust gate, full suite, or release gate
  passed; no Integration candidate has been composed.
- Retained worktrees under `~/worktrees/codexnk/maintain-20260929/`:
  `invocation-axes` on `carry/cycle-20260929-invocation-axes` at
  `6a7ffa904888a9b5f2836e726334ccef0dd36359`; `runtime-companions` on
  `carry/cycle-20260929-runtime-companions` at
  `c8ec723729b001d4f40232df5d249c90ffa5aa2d`; `input-middleware` is mid-rebase
  on `carry/cycle-20260929-input-middleware`, detached at
  `ccac492e777aac236d11d24ab250fb1ee23bfaff`. Only the two precomputed
  protocol `.json.zst` bundles remain conflicted. Regenerate stable and
  experimental exports before continuing that rebase. The `integration`
  worktree remains at the captured upstream target.
- Leases, upstream fetch receipt, interval inventory, failed schema log and
  final read-only reconciliation are retained in
  `/private/var/folders/9g/l0rgs8rs2_9__kqn0smr9tnh0000gp/T/opencode/codexnk-maintain-20260929-vutj0aww/`.
  The workshop's pre-existing installer bytecode cache was preserved there
  as `preexisting-installer-pycache` to establish a clean workshop. No Rust
  build cache was created; disposable formatter virtual environments were
  removed from the owned worktrees.
- Publication targets were re-read and match the starting leases. The pinned
  read-only branch check passed, retaining ten other public heads. Supervision
  had the old `~/code/codexnk` path; the declared entrypoint reconverged it to
  `~/workshops/codexnk` and `--check-supervision` passed. No branch apply was run.
  The installed v0.1.4 package passed its per-file ownership hashes, modes and
  metadata checks; AgentStart still pins its exact tag/SHA. Public refs,
  release tags and consumer bindings retain the delivered baseline above.

## Audited upstream frontier

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
