# Scratchpad

## Delivered baseline

- Captured upstream `main`: `e154f7b80789b742b162cf0e44de0bc021068a20`.
- Public `main` mirrors that commit. `carry/invocation-axes` is
  `154c48569b4df5e4319b55f7745461d37fee2a23`; `carry/input-middleware`
  is `0f8797fbbe3103e0edb8c9d951c22e20fe310e26`. Both were published
  atomically with Integration `7d341030af1c243eeb334294be31aeb3c58d233c`.
  A concurrent, later runtime-companions carry
  `7939215687df51e24d39662507d4e392a3856211` advanced public
  Integration to `f2905ff011ff8fda607e91dfdd8f13b6083b1642` after the
  v0.1.3 tag; that newer commit contains the v0.1.3 source commit. The public
  default branch remains `integration`.
- `codexnk-v0.1.3` points at `7d341030af1c243eeb334294be31aeb3c58d233c`.
  Release workflow [36062064372](https://github.com/possibilities/codexnk-codex/actions/runs/36062064372)
  succeeded; both published archives passed tag, digest, size, and structure
  verification. An isolated macOS install passed the AgentStack middleware
  smoke, then the verified release was installed at
  `~/.local/libexec/codexnk/codex` on 2026-09-24 with a matching ownership
  receipt. Installed-binary runtime and WebSocket middleware tests passed.
  AgentStart `104e611b7170e1190ace5c9ee50e98b3db13f844` and AgentStack
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

- Exact carry commit: `154c48569b4df5e4319b55f7745461d37fee2a23`,
  based on the captured upstream target and an ancestor of published
  Integration `7d341030af1c243eeb334294be31aeb3c58d233c`. Historical
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
  captured upstream `main`. Its generated stable and experimental protocol
  exports were regenerated after replay. Integration is at
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
  AgentStack's host-side client and optional
  pass-through observation UI remain; actual command-routing policy follows
  later.

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
aligned AgentStart/AgentStack pins without restarting any resident Codex
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
