#!/usr/bin/env bash
set -euo pipefail
repo_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
cd "$repo_dir"
while IFS= read -r -d '' script; do
    bash -n "$script"
done < <(find bootstrap scripts tests -name '*.sh' -print0)
bash -n bin/workstation
if command -v shellcheck >/dev/null; then
    mapfile -d '' scripts < <(find bootstrap scripts tests -name '*.sh' -print0)
    shellcheck "${scripts[@]}" bin/workstation
else
    echo 'SKIP: shellcheck is not installed.'
fi
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
PYTHONDONTWRITEBYTECODE=1 python3 tests/check_docs.py
