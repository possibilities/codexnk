#!/bin/bash

set -euo pipefail

# codexnk's branch declaration. The maintain skill owns reconciliation logic.
skill_dir="${MAINTAIN_SKILL_DIR:-$HOME/.local/share/agentstart/resources/skills/maintain}"
script="$skill_dir/scripts/reconcile-branches.sh"
if [ ! -f "$script" ]; then
    printf 'codexnk branches: maintain skill is missing at %s\n' "$skill_dir" >&2
    exit 1
fi

MAINTAIN_WORKSHOP="$(cd "$(dirname "$0")/.." && pwd)"
export MAINTAIN_WORKSHOP
export MAINTAIN_CHECKOUT="${CODEXNK_CODEX_CHECKOUT:-$HOME/source/openai--codex-codexnk}"
export MAINTAIN_FORK_REPO=possibilities/codexnk-codex
export MAINTAIN_UPSTREAM_REPO=openai/codex
export MAINTAIN_FORK_REMOTE=public
export MAINTAIN_UPSTREAM_REMOTE=upstream
export MAINTAIN_MAIN_BRANCH=main
export MAINTAIN_INTEGRATION_BRANCH=integration
export MAINTAIN_CARRY_PREFIX=''
export MAINTAIN_CARRY_REFS='carry/invocation-axes carry/input-middleware carry/runtime-companions'
export MAINTAIN_QUARANTINE_PREFIX=DELETEME/
export MAINTAIN_PRESERVE_OPEN_PRS=0

exec bash "$script" "$@"
