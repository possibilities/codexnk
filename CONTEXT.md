# codexnk context

**Workshop** — This repository. It owns the specification in `MAINTAIN.md` for
the local Codex fork.
_Avoid_: wrapper, patch repo.

**Main mirror** — Local and public `main` in `~/source/openai--codex-codexnk` and
`possibilities/codexnk-codex`, tracking `openai/codex` `main`.
_Avoid_: possibilities/codex, integration base.

**Integration** — Patched release source in `possibilities/codexnk-codex`.
_Avoid_: upstream mirror, temporary carry branch.

**Carry branch** — A local `carry/<feature>` head based on upstream `main`.
_Avoid_: patch branch, upstream pull request.

**Identity** — The credential directory selected for one app-server process.
_Avoid_: account home, CODEX_HOME.

**Capabilities** — The skills, MCP servers, and developer-instruction append
selected for one app-server process.
_Avoid_: shape, profile.

**History** — The shared session directory. It does not select credentials or
capabilities.
_Avoid_: CODEX_HOME, transcript store.

**Input middleware** — One opt-in app-server WebSocket owner that chooses how
an exact human text candidate enters a loaded Codex thread: unchanged,
replacement text, or intercepted without a working turn.
_Avoid_: transcript listener, generic hook chain.

**Admission journal** — The history-owned, per-thread record of input
dispositions and external effect receipts, separate from the Codex rollout.
_Avoid_: model transcript, WebSocket delivery guarantee.
