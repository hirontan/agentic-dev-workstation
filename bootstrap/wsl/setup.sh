#!/usr/bin/env bash
set -euo pipefail
apply=0
case "${1:-}" in
    '') ;;
    --apply) apply=1 ;;
    --help|-h) echo 'Usage: bash bootstrap/wsl/setup.sh [--apply]'; exit 0 ;;
    *) echo 'Unknown argument. Use --help.' >&2; exit 1 ;;
esac
[[ $# -le 1 ]] || { echo 'Too many arguments.' >&2; exit 1; }
repo_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)
packages=(build-essential ca-certificates git curl wget unzip zip jq ripgrep fd-find
          fzf tmux direnv tree htop gh python3 shellcheck ncurses-term)
echo 'Plan: Ubuntu 24.04 base CLI packages, non-destructive config copies, workstation symlink.'
printf 'Packages: %s\n' "${packages[*]}"
printf 'Config destination: %s\n' "$HOME/.config/agentic-dev-workstation"
echo 'No Agent/runtime/cloud installation or login. Different existing config files will be preserved.'
if (( ! apply )); then
    echo 'No changes. Re-run with --apply.'
    exit 0
fi
[[ -f /etc/os-release ]] || { echo 'Ubuntu 24.04 required.' >&2; exit 1; }
# shellcheck disable=SC1091
source /etc/os-release
[[ ${ID:-} == ubuntu && ${VERSION_ID:-} == 24.04 ]] || {
    echo 'This bootstrap supports Ubuntu 24.04 only.' >&2; exit 1;
}
(( EUID != 0 )) || { echo 'Run as a normal Linux user, not root.' >&2; exit 1; }
command -v sudo >/dev/null || { echo 'sudo is required.' >&2; exit 1; }
sudo apt-get update
sudo apt-get install -y "${packages[@]}"
mkdir -p "$HOME/src" "$HOME/worktrees" "$HOME/.local/bin" \
    "$HOME/.config/agentic-dev-workstation" "$HOME/.local/state/agentic-dev-workstation"
conflicts=0
safe_copy() {
    local source_path=$1 destination=$2
    if [[ -L $destination || -e $destination ]]; then
        if [[ -f $destination ]] && cmp -s "$source_path" "$destination"; then
            printf 'UNCHANGED %s\n' "$destination"
        else
            printf 'CONFLICT preserved %s (merge manually)\n' "$destination" >&2
            conflicts=$((conflicts + 1))
        fi
    else
        install -m 644 "$source_path" "$destination"
        printf 'CREATED %s\n' "$destination"
    fi
}
safe_copy "$repo_dir/config/tmux/tmux.conf" "$HOME/.tmux.conf"
safe_copy "$repo_dir/config/git/gitconfig" "$HOME/.config/agentic-dev-workstation/gitconfig"
safe_copy "$repo_dir/config/shell/workstation.bash" "$HOME/.config/agentic-dev-workstation/workstation.bash"
cli_target="$HOME/.local/bin/workstation"
if [[ -L $cli_target ]] && [[ $(readlink "$cli_target") == "$repo_dir/bin/workstation" ]]; then
    echo 'UNCHANGED workstation symlink'
elif [[ -L $cli_target || -e $cli_target ]]; then
    echo 'CONFLICT preserved workstation executable/symlink' >&2
    conflicts=$((conflicts + 1))
else
    # Windows ZIP extraction may lose executable modes.
    chmod +x "$repo_dir/bin/workstation" "$repo_dir/scripts/agent-shell.sh"
    ln -s "$repo_dir/bin/workstation" "$cli_target"
fi
# HOME must expand when the user's shell starts, not while writing the source line.
# shellcheck disable=SC2016
source_line='[ -f "$HOME/.config/agentic-dev-workstation/workstation.bash" ] && source "$HOME/.config/agentic-dev-workstation/workstation.bash"'
if [[ -L $HOME/.bashrc ]]; then
    echo 'CONFLICT preserved symlinked .bashrc; add source line manually.' >&2
    conflicts=$((conflicts + 1))
elif [[ -e $HOME/.bashrc && ! -f $HOME/.bashrc ]]; then
    echo 'CONFLICT .bashrc is not a regular file.' >&2
    conflicts=$((conflicts + 1))
elif ! rg -Fqx "$source_line" "$HOME/.bashrc" 2>/dev/null; then
    printf '\n# agentic-dev-workstation\n%s\n' "$source_line" >> "$HOME/.bashrc"
fi
umask 077
dpkg-query -W -f='${Package}\t${Version}\n' "${packages[@]}" \
    > "$HOME/.local/state/agentic-dev-workstation/packages.tsv"
printf 'Finished; conflicts: %s. Open a new Bash or source ~/.bashrc.\n' "$conflicts"
(( conflicts == 0 )) || exit 2
