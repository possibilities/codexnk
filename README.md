# codexnk

Workshop for a downstream Codex fork whose app-server launch can split
identity, capabilities, and session history.

`MAINTAIN.md` is the behavior and release contract. `SCRATCHPAD.md` records
the delivered and audited upstream state. Run `/maintain` from this repository
for one cycle.

The dedicated checkout is this Workshop's `fork/` (`~/workshops/codexnk/fork`).
Public `main` mirrors upstream; public `integration` carries the patch and is
the release source. Releases publish binaries without replacing the system Codex.

AgentStart consumes an exact release with `scripts/install.sh --install --tag
codexnk-vVERSION --sha FULL_COMMIT`. The workshop owns its isolated executable
and verification; `scripts/install.sh --print-bin` reports the path for shims.
See the Consumer section of `MAINTAIN.md` for ownership and recovery boundaries.
