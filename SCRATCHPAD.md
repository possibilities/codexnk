# Scratchpad

## Delivered baseline

- Captured upstream `main`: `30fc6864cc1318121eca1843c217fe00ce1212f1`.
- Public `main` mirrors that commit. Public `integration` and
  `carry/invocation-axes` point at `2945e58e2fb751dcaa1957f594bbef50fbd78392`.
  The public default branch is `integration`; 11 unrelated heads were unchanged.
- `codexnk-v0.1.1` points at that Integration commit. Release workflow
  [35880396004](https://github.com/possibilities/codexnk-codex/actions/runs/35880396004)
  succeeded; both macOS and Linux archives passed tag and SHA-256 verification.
  The receipt-verified installer published AgentStart's exact consumer pin at
  `~/.local/libexec/codexnk/codex` on 2026-09-23, preserving vendor Codex.
- The previous release `codexnk-v0.1.0` points at `7bccdfb0e871681472ff9c9e2a160c4e1d479453`.
  Before this cycle, public `main` and the carry were
  `f832ae88f82a5aed86a072556e753bd253f11619`.

## Audited upstream frontier

- Complete through `30fc6864cc1318121eca1843c217fe00ce1212f1` on
  2026-09-23. The prior `40eeb6e8a89ef421c25d4c40e06fa1d40ce66b4f`
  frontier was reconstructed from the initial captured base; the old
  scratchpad had no separate audit field.
- [Aggregate interval](https://github.com/openai/codex/compare/40eeb6e8a89ef421c25d4c40e06fa1d40ce66b4f...30fc6864cc1318121eca1843c217fe00ce1212f1):
  138 commits. Notable groups: agent message-board and Guardian changes;
  daemon, remote-control, and network-policy work; app-server gateway OAuth
  and per-turn host cloud skill refresh; TUI and voice changes; GPT-6 Sol and
  Luna catalog additions. The [0.156.1 release notes](https://github.com/openai/codex/releases/tag/rust-v0.156.1)
  cover the model addition; no release note covers this exact interval.

## Carry: invocation axes

- Exact carry and Integration commit:
  `2945e58e2fb751dcaa1957f594bbef50fbd78392`, based on the captured
  upstream target. Historical upstream reference: `40eeb6e8a89ef421c25d4c40e06fa1d40ce66b4f`.
- Disposition: **repair**. Upstream extracted WebSocket auth argument types,
  requiring one mechanical `cli/main.rs` replay resolution. Upstream's new
  cloud skill refresh and gateway OAuth paths do not supply the three launch
  axes. The carry also now dereferences linked capability skills when copying
  them, so subsequent source edits cannot alter a process's skills.
- Stance: no material change. The downstream launch split remains necessary;
  retire it only after upstream code and a focused run satisfy all three axes
  and their isolation rules. No upstream offer is planned.
- Proof: local `just test -p codex-cli invocation_axes` passed 3 tests from
  the dedicated carry worktree; its freshly built `codex app-server` started
  with all three flags and created both shared history directories. A stock
  launch with a temporary `CODEX_HOME` also exited cleanly. Hosted Integration
  and carry CI succeeded for the same SHA. The release workflow succeeded,
  both published archives verified, and the installed macOS binary passed the
  installer's version and invocation-axis probes.
- Follow-up: the current `TempDir::keep()` leaves the private runtime home,
  including its copied `auth.json`, after process exit. A later carry repair
  should make that directory's lifetime match the app-server process.

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
