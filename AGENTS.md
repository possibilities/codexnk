# codexnk agent guidance

This repository is the workshop for a downstream Codex fork. Read `CONTEXT.md`,
`MAINTAIN.md`, and `SCRATCHPAD.md` before changing the fork.

The Codex checkout is `~/source/openai--codex-codexnk`. Develop a carry in its own
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
