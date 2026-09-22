# Scratchpad

2026-09-22: `carry/invocation-axes` is `033a1a586590aa613b4aa47c876d175e1c6e9410`,
based on upstream `main` `40eeb6e8a8`. Worktree:
`~/worktrees/openai--codex/invocation-axes/openai--codex`.

Published to public `possibilities/codexnk-codex` `main` and
`carry/invocation-axes`, not to `possibilities/codex`. Tag `codexnk-v0.1.0`
starts the release build. Local `integration` matches the carry tip. The
system Codex is unchanged.

Proof: `just test -p codex-cli invocation_axes` in that worktree's `codex-rs`
ran 2 tests, 2 passed.
