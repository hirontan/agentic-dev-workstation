#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 1 || ${1:-} == --help ]]; then
    echo 'Usage: bash scripts/bootstrap-project.sh /path/to/project' >&2
    exit 1
fi
script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
project_dir=$(cd -- "$1" && pwd -P)
git -C "$project_dir" rev-parse --show-toplevel >/dev/null
destination="$project_dir/AGENTS.md"
[[ ! -e $destination && ! -L $destination ]] || {
    echo 'AGENTS.md already exists; no change made.' >&2; exit 1;
}
install -m 644 "$script_dir/../templates/AGENTS.md" "$destination"
echo 'Created AGENTS.md. Customize commands and scope before using an Agent.'
