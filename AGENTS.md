# codexnk agent guidance

This repository is the workshop for a downstream Codex fork. Read `CONTEXT.md`,
`MAINTAIN.md`, and `SCRATCHPAD.md` before changing the fork.

The Codex checkout is `~/source/openai--codex-codexnk`. Develop a carry in its own
worktree on `carry/<feature>`, based on the captured upstream `main`. Do not
commit feature work on the bound checkout, and do not use `possibilities/codex`
as the base. Public `main` mirrors upstream; publish patched code from
`integration` in `possibilities/codexnk-codex`. Read that checkout's
`AGENTS.md` before modifying Codex.

There is no installer and no consumer pin. Do not replace the system Codex.
