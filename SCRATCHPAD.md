# Scratchpad

2026-09-22: `carry/invocation-axes` is `040b39ef132748e57f3ac240ff846f2ad17a55d8`,
based on upstream `main` `40eeb6e8a8`. Worktree:
`~/worktrees/openai--codex/invocation-axes/openai--codex`.

The carry is local only. It is not pushed to `possibilities/codex`. Local
`integration` points at the same commit. No installed binary.

Proof: `just test -p codex-cli invocation_axes` in that worktree's `codex-rs`
ran 2 tests, 2 passed.
