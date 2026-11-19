#!/usr/bin/env bash
# Deploy one website to its Cloudron Surfer, with the folder CONTENTS at the root "/".
#
#   SURFER_TOKEN=... deploy/deploy-to-surfer.sh identity
#   SURFER_TOKEN=... deploy/deploy-to-surfer.sh identity --dry-run   # show what would upload
#
# Files on the Surfer that are not in the folder are deleted (set SURFER_DELETE=false to keep them).
# Needs the Surfer CLI: npm install -g cloudron-surfer
set -euo pipefail
cd "$(dirname "$0")/.."
. deploy/surfer-sites.sh

site="${1:-}"
dry_run="${2:-}"
src="$(site_field "$site" 2)"
if [ -z "$site" ] || [ -z "$src" ]; then
  echo "Usage: $0 <site> [--dry-run]   where <site> is one of: $(site_names | tr '\n' ' ')" >&2
  exit 2
fi
domain="$(site_field "$site" 3)"
[ -f "$src/index.html" ] || { echo "No index.html in $src, refusing to deploy" >&2; exit 1; }

# Copy the folder contents to a staging folder, leaving out build inputs (texts, tools).
stage="$(mktemp -d)"
trap 'rm -rf "$stage"' EXIT
cp -a "$src/." "$stage/"
while read -r e; do
  [ -n "$e" ] || continue
  rm -rf "$stage"/$e   # unquoted on purpose: entries like materials/*/sales are globs
done < <(site_excludes "$site")
find "$stage" -name '.*' -prune -exec rm -rf {} +   # hidden files are not published

echo "Deploying $src/ -> https://$domain/ ($(find "$stage" -type f | wc -l) files)"
if [ "$dry_run" = "--dry-run" ]; then
  (cd "$stage" && find . -type f | sort | sed 's|^\./|  /|')
  exit 0
fi

: "${SURFER_TOKEN:?Set SURFER_TOKEN to the access token from https://$domain/_admin}"
delete_flag=(--delete)
[ "${SURFER_DELETE:-true}" = "false" ] && delete_flag=()

# "surfer put dir /" would create /dir/... on the server. Passing the folder's
# entries (./*) puts them at /..., which is what we want.
cd "$stage"
surfer put --server "${SURFER_SERVER:-https://$domain}" --token "$SURFER_TOKEN" "${delete_flag[@]}" ./* /
