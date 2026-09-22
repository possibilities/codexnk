# Scratchpad

2026-09-22: public CI is only `codexnk-release.yml`. It tests
`invocation_axes` on branch pushes and builds release binaries on
`codexnk-v*` tags. Upstream workflows on `possibilities/codexnk-codex` are
disabled. The first release build failed while packaging because it looked in
`target/` after setup-ci had set `CARGO_TARGET_DIR`.

Carry tip `7bccdfb0e8` installs nextest before `just test`. The previous
public test failed immediately because `cargo nextest` was not installed.
Base remains upstream `main` `40eeb6e8a8`. Worktree:
`~/worktrees/openai--codex/invocation-axes/openai--codex`. Not published to
`possibilities/codex`. The system Codex is unchanged.

Proof: `just test -p codex-cli invocation_axes` in that worktree's `codex-rs`
ran 2 tests, 2 passed.
