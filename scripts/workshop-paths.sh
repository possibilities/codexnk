# Sourced by Workshop commands, including from linked Workshop worktrees.
codexnk_workshop() {
    local common
    common=$(git -C "$(dirname "${BASH_SOURCE[0]}")/.." rev-parse --path-format=absolute --git-common-dir) || return
    if [ "${common##*/}" != .git ]; then
        printf 'codexnk: nonstandard Git directory; cannot resolve canonical Workshop\n' >&2
        return 1
    fi
    dirname "$common"
}

codexnk_checkout() {
    if [ -n "${CODEXNK_CODEX_CHECKOUT:-}" ]; then
        printf '%s\n' "$CODEXNK_CODEX_CHECKOUT"
        return
    fi
    local workshop
    workshop=$(codexnk_workshop) || return
    printf '%s/fork\n' "$workshop"
}
