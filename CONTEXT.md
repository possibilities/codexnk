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
