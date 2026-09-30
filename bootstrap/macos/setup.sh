#!/usr/bin/env bash
set -euo pipefail
apply=0
case "${1:-}" in
    '') ;;
    --apply) apply=1 ;;
    --help|-h) echo 'Usage: bash bootstrap/macos/setup.sh [--apply]'; exit 0 ;;
    *) echo 'Unknown argument. Use --help.' >&2; exit 1 ;;
esac
[[ $# -le 1 ]] || { echo 'Too many arguments.' >&2; exit 1; }
repo_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)
packages=(git curl wget jq ripgrep fd fzf tmux direnv tree htop gh python3 shellcheck)
echo 'Plan: macOS (Darwin) base CLI packages via Homebrew, non-destructive config copies, workstation symlink.'
printf 'Packages: %s\n' "${packages[*]}"
printf 'Config destination: %s\n' "$HOME/.config/agentic-dev-workstation"
echo 'No Agent/runtime/cloud installation or login. Different existing config files will be preserved.'
if (( ! apply )); then
    echo 'No changes. Re-run with --apply.'
    exit 0
fi
[[ $(uname -s) == "Darwin" ]] || { echo 'macOS (Darwin) required.' >&2; exit 1; }
(( EUID != 0 )) || { echo 'Do not run as root. Homebrew must be run as a normal user.' >&2; exit 1; }
command -v brew >/dev/null || {
    echo 'Homebrew is required. Install it from https://brew.sh first.' >&2
    exit 1
}
brew install "${packages[@]}"
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
safe_copy "$repo_dir/config/shell/workstation.zsh" "$HOME/.config/agentic-dev-workstation/workstation.zsh"
cli_target="$HOME/.local/bin/workstation"
if [[ -L $cli_target ]] && [[ $(readlink "$cli_target") == "$repo_dir/bin/workstation" ]]; then
    echo 'UNCHANGED workstation symlink'
elif [[ -L $cli_target || -e $cli_target ]]; then
    echo 'CONFLICT preserved workstation executable/symlink' >&2
    conflicts=$((conflicts + 1))
else
    chmod +x "$repo_dir/bin/workstation" "$repo_dir/scripts/agent-shell.sh"
    ln -s "$repo_dir/bin/workstation" "$cli_target"
fi

# HOME must expand when the user's shell starts, not while writing the source line.
# shellcheck disable=SC2016
source_line_zsh='[ -f "$HOME/.config/agentic-dev-workstation/workstation.zsh" ] && source "$HOME/.config/agentic-dev-workstation/workstation.zsh"'
# shellcheck disable=SC2016
source_line_bash='[ -f "$HOME/.config/agentic-dev-workstation/workstation.bash" ] && source "$HOME/.config/agentic-dev-workstation/workstation.bash"'

add_shell_source() {
    local target_file=$1 source_line=$2 shell_name=$3
    if [[ -L $target_file ]]; then
        echo "CONFLICT preserved symlinked $shell_name; add source line manually." >&2
        conflicts=$((conflicts + 1))
    elif [[ -e $target_file && ! -f $target_file ]]; then
        echo "CONFLICT $shell_name is not a regular file." >&2
        conflicts=$((conflicts + 1))
    elif [[ -f $target_file ]]; then
        if ! rg -Fqx "$source_line" "$target_file" 2>/dev/null; then
            printf '\n# agentic-dev-workstation\n%s\n' "$source_line" >> "$target_file"
        fi
    else
        printf '# agentic-dev-workstation\n%s\n' "$source_line" > "$target_file"
    fi
}

add_shell_source "$HOME/.zshrc" "$source_line_zsh" ".zshrc"
if [[ -f $HOME/.bash_profile ]]; then
    add_shell_source "$HOME/.bash_profile" "$source_line_bash" ".bash_profile"
else
    add_shell_source "$HOME/.bashrc" "$source_line_bash" ".bashrc"
fi

umask 077
brew list --versions "${packages[@]}" \
    > "$HOME/.local/state/agentic-dev-workstation/packages.tsv" 2>/dev/null || true
printf 'Finished; conflicts: %s. Open a new terminal or source your shell config.\n' "$conflicts"
(( conflicts == 0 )) || exit 2
