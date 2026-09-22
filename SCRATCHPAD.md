# Scratchpad

2026-09-22: public CI is only `codexnk-release.yml`. It tests
`invocation_axes` on branch pushes and builds release binaries on
`codexnk-v*` tags. Upstream workflows on `possibilities/codexnk-codex` are
disabled. The first release build failed while packaging because it looked in
`target/` after setup-ci had set `CARGO_TARGET_DIR`.

Carry tip `06a454c81b9e700c9c48210e25137a38e89c69d5` includes the CI fix.
Base remains upstream `main` `40eeb6e8a8`. Worktree:
`~/worktrees/openai--codex/invocation-axes/openai--codex`. Not published to
`possibilities/codex`. The system Codex is unchanged.

Proof: `just test -p codex-cli invocation_axes` in that worktree's `codex-rs`
ran 2 tests, 2 passed.
