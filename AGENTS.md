# codexnk agent guidance

This repository is the workshop for a downstream Codex fork. Read `CONTEXT.md`,
`MAINTAIN.md`, and `SCRATCHPAD.md` before changing the fork.

The Codex checkout is this Workshop's ignored `fork/` at
`~/workshops/codexnk/fork`; persistent maintenance worktrees live under its
ignored `worktrees/`. Linked Workshop worktrees use the canonical Workshop's
fork, not a nested copy. Develop a carry in its own
worktree on `carry/<feature>`, based on the captured upstream `main`. Do not
commit feature work on the bound checkout, and do not use `possibilities/codex`
as the base. Public `main` mirrors upstream; publish patched code from
`integration` in `possibilities/codexnk-codex`. Read that checkout's
`AGENTS.md` before modifying Codex.

`scripts/install.sh` owns an isolated, receipt-verified release installation at
`~/.local/libexec/codexnk/codex`. AgentStart owns the exact release tag/Integration
SHA consumer pin and its shim binding. Preserve the separately installed vendor
Codex binary; never overwrite it. Test installer changes with
`python3 tests/install.py` and an isolated real release installation.
Every local maintenance cycle must use `python3 scripts/cycle.py` as specified
in `MAINTAIN.md`: one Scratch target shared across the cycle's worktrees,
non-incremental builds by default, phase checkpoints, and final cleanup after
saving evidence. Missing Scratch or uncertain ownership/activity blocks cleanup
and builds; never fall back to worktree-local targets or internal-disk build output.
Small private validation fixtures follow the scoped exceptions in `MAINTAIN.md`.
At each `/maintain` start, review retained completed-cycle worktrees. After
delivery, the coordinator must retire finished cycle-owned worktrees from
outside them using the evidence/commit/activity checks in `MAINTAIN.md`, or
record the specific owner, reason and next step for every retained tree.
