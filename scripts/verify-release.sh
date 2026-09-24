#!/bin/bash

set -euo pipefail

if [ "$#" -ne 2 ]; then
    printf 'Usage: verify-release.sh CANDIDATE_SHA codexnk-vVERSION\n' >&2
    exit 64
fi
candidate_sha="$1"
tag="$2"
[[ "$candidate_sha" =~ ^[0-9a-f]{40}$ ]] || exit 64
[[ "$tag" =~ ^codexnk-v[0-9]+\.[0-9]+\.[0-9]+$ ]] || exit 64

repo=possibilities/codexnk-codex
tag_object=$(gh api "repos/$repo/git/ref/tags/$tag")
tag_type=$(jq -r '.object.type' <<<"$tag_object")
tag_sha=$(jq -r '.object.sha' <<<"$tag_object")
if [ "$tag_type" = tag ]; then
    tag_object=$(gh api "repos/$repo/git/tags/$tag_sha")
    tag_type=$(jq -r '.object.type' <<<"$tag_object")
    tag_sha=$(jq -r '.object.sha' <<<"$tag_object")
fi
[ "$tag_type" = commit ] && [ "$tag_sha" = "$candidate_sha" ] || {
    printf 'release: %s does not resolve to %s\n' "$tag" "$candidate_sha" >&2
    exit 1
}

release=$(gh release view "$tag" --repo "$repo" --json assets)
[ "$(jq '.assets | length' <<<"$release")" -eq 2 ] || {
    printf 'release: expected exactly two archives\n' >&2
    exit 1
}
temporary=$(mktemp -d "${CODEXNK_VERIFY_TMPDIR:-${TMPDIR:-/tmp}}/codexnk-release.XXXXXX")
trap 'rm -rf -- "$temporary"' EXIT
for target in aarch64-apple-darwin x86_64-unknown-linux-gnu; do
    name="codex-$target"
    archive="$name.tar.gz"
    asset=$(jq -c --arg name "$archive" '.assets[] | select(.name == $name)' <<<"$release")
    digest=$(jq -r '.digest' <<<"$asset")
    size=$(jq -r '.size' <<<"$asset")
    state=$(jq -r '.state' <<<"$asset")
    [[ "$digest" =~ ^sha256:[0-9a-f]{64}$ ]] && [ "$size" -gt 0 ] \
        && [ "$state" = uploaded ] || {
        printf 'release: invalid asset metadata for %s\n' "$archive" >&2
        exit 1
    }
    gh release download "$tag" --repo "$repo" --pattern "$archive" --dir "$temporary"
    actual=$(shasum -a 256 "$temporary/$archive" | awk '{ print $1 }')
    [ "sha256:$actual" = "$digest" ] && [ "$(stat -f%z "$temporary/$archive")" = "$size" ] || {
        printf 'release: digest or size mismatch for %s\n' "$archive" >&2
        exit 1
    }
    python3 "$(dirname "$0")/verify-archive.py" "$temporary/$archive" "$target" "$tag"
    printf 'Verified %s (%s bytes, %s).\n' "$archive" "$size" "$digest"
    rm "$temporary/$archive"
done
