# Sourced by Workshop commands, including from linked Workshop worktrees.
codexnk_checkout() {
    if [ -n "${CODEXNK_CODEX_CHECKOUT:-}" ]; then
        printf '%s\n' "$CODEXNK_CODEX_CHECKOUT"
        return
    fi
    local common
    common=$(git -C "$(dirname "${BASH_SOURCE[0]}")/.." rev-parse --path-format=absolute --git-common-dir) || return
    if [ "${common##*/}" != .git ]; then
        printf 'codexnk: nonstandard Workshop Git directory; set CODEXNK_CODEX_CHECKOUT\n' >&2
        return 1
    fi
    printf '%s/fork\n' "$(dirname "$common")"
}
