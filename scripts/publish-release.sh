#!/bin/bash

set -euo pipefail

if [ "$#" -ne 2 ]; then
    printf 'Usage: publish-release.sh CANDIDATE_SHA codexnk-vVERSION\n' >&2
    exit 64
fi
candidate_sha="$1"
tag="$2"
[[ "$candidate_sha" =~ ^[0-9a-f]{40}$ ]] || {
    printf 'release: candidate must be an exact commit SHA\n' >&2
    exit 64
}
[[ "$tag" =~ ^codexnk-v[0-9]+\.[0-9]+\.[0-9]+$ ]] || {
    printf 'release: invalid tag %s\n' "$tag" >&2
    exit 64
}

checkout="${CODEXNK_CODEX_CHECKOUT:-$HOME/source/openai--codex-codexnk}"
for url in "$(git -C "$checkout" remote get-url public)" \
    "$(git -C "$checkout" remote get-url --push public)"; do
    case "$url" in
        https://github.com/possibilities/codexnk-codex | \
        https://github.com/possibilities/codexnk-codex.git | \
        git@github.com:possibilities/codexnk-codex.git) ;;
        *) printf 'release: unexpected public remote %s\n' "$url" >&2; exit 1 ;;
    esac
done
git -C "$checkout" cat-file -e "$candidate_sha^{commit}"
published_sha=$(gh api repos/possibilities/codexnk-codex/git/ref/heads/integration --jq '.object.sha')
[ "$candidate_sha" = "$published_sha" ] || {
    printf 'release: public integration is %s, expected %s\n' "$published_sha" "$candidate_sha" >&2
    exit 1
}
if gh api "repos/possibilities/codexnk-codex/git/ref/tags/$tag" >/dev/null 2>&1; then
    printf 'release: tag %s already exists\n' "$tag" >&2
    exit 1
fi

gh api --method POST repos/possibilities/codexnk-codex/git/refs \
    -f "ref=refs/tags/$tag" -f "sha=$candidate_sha" --jq '.object.sha'
printf 'Published %s at %s; verify the release workflow and both archives.\n' "$tag" "$candidate_sha"
