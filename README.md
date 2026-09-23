# codexnk

Workshop for a downstream Codex fork whose app-server launch can split
identity, capabilities, and session history.

`MAINTAIN.md` is the behavior and release contract. `SCRATCHPAD.md` records
the delivered and audited upstream state. Run `/maintain` from this repository
for one cycle.

The dedicated checkout is `~/source/openai--codex-codexnk`. Public `main`
mirrors upstream; public `integration` carries the patch and is the release
source. Releases publish binaries without replacing the system Codex.
