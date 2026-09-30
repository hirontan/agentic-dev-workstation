#!/usr/bin/env python3
"""Local workstation operations. No provider requests, GitHub writes, or force deletion."""
import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent


class Failure(Exception):
    pass


def run(args, *, cwd=None, check=True):
    result = subprocess.run([str(a) for a in args], cwd=cwd, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and result.returncode:
        # Do not print command-line credentials or arbitrary env variables.
        message = result.stderr.strip() or 'Command failed'
        raise Failure(message)
    return result


def git(repo, *args, check=True):
    return run(['git', '-C', repo, *args], check=check)


def issue_number(value):
    if not re.fullmatch(r'[1-9][0-9]{0,9}', value):
        raise argparse.ArgumentTypeError('Issue must be a positive number (up to 10 digits).')
    return value


def repository(path):
    directory = Path(path).expanduser().resolve()
    if git(directory, 'rev-parse', '--is-bare-repository').stdout.strip() == 'true':
        raise Failure('A non-bare repository is required.')
    top = Path(git(directory, 'rev-parse', '--show-toplevel').stdout.strip()).resolve()
    raw = git(directory, 'rev-parse', '--path-format=absolute', '--git-common-dir').stdout.strip()
    common = Path(raw).resolve()
    token = hashlib.sha256(os.fsencode(common)).hexdigest()[:10]
    # The common directory can identify the primary repository even when called from a worktree.
    primary = common.parent if common.name == '.git' else top
    name = re.sub(r'[^a-zA-Z0-9_-]', '-', primary.name).strip('-')[:40] or 'repo'
    return top, common, f'{name}-{token}'


@contextmanager
def locked(common):
    with (common / 'workstation.lock').open('a') as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        yield


def layout(args, repo, name):
    root = Path(args.root).expanduser().resolve()
    # Includes symlink normalization. Never create nested worktrees in this repository.
    common = repository(repo)[1]
    primary = common.parent if common.name == '.git' else repo
    if any(root == item or item in root.parents for item in (repo, primary)):
        raise Failure('Worktree root must be outside the current repository.')
    return root / name / f'issue-{args.issue}', f'agent/issue-{args.issue}'


def records(repo):
    raw = git(repo, 'worktree', 'list', '--porcelain', '-z').stdout
    output = {}
    current = None
    for field in raw.split('\0'):
        if field.startswith('worktree '):
            current = str(Path(field[9:]).resolve())
            output[current] = {}
        elif current and field:
            key, _, value = field.partition(' ')
            output[current][key] = value
    return output


def validate_tree(repo, common, tree, branch):
    record = records(repo).get(str(tree))
    if not record or record.get('branch') != f'refs/heads/{branch}':
        raise Failure('Path is not the registered worktree for this Issue branch.')
    if not tree.is_dir():
        raise Failure('Registered worktree is missing. Inspect git worktree list/prune manually.')
    actual = repository(tree)[1]
    if actual != common:
        raise Failure('Worktree belongs to a different repository.')


def commit(repo, reference):
    # End of option parsing: a supplied ref cannot become a Git option.
    return git(repo, 'rev-parse', '--verify', '--end-of-options', reference + '^{commit}').stdout.strip()


def new_tree(args):
    repo, common, name = repository(args.repo)
    tree, branch = layout(args, repo, name)
    with locked(common):
        if tree.exists() or tree.is_symlink():
            validate_tree(repo, common, tree, branch)
            print(f'REUSED {tree}')
            return
        if git(repo, 'show-ref', '--verify', f'refs/heads/{branch}', check=False).returncode == 0:
            raise Failure('Issue branch already exists. Inspect it manually; no branch was reset.')
        base = commit(repo, args.base)
        tree.parent.mkdir(parents=True, exist_ok=True)
        git(repo, 'worktree', 'add', '-b', branch, tree, base)
    print(f'CREATED {tree}\nBRANCH {branch}\nBASE {args.base} ({base[:12]})')


def remove_tree(args):
    repo, common, name = repository(args.repo)
    tree, branch = layout(args, repo, name)
    with locked(common):
        validate_tree(repo, common, tree, branch)
        primary = common.parent if common.name == '.git' else repo
        if tree == repo or tree == primary:
            raise Failure('Refusing to remove the current or primary worktree. Run from the primary repository.')
        # Protect ignored local data as well as tracked/untracked changes.
        if git(tree, 'status', '--porcelain', '--untracked-files=all', '--ignored').stdout:
            raise Failure('Worktree contains changed, untracked, or ignored files. Preserve/clean them manually.')
        base = commit(repo, args.base)
        head = commit(tree, 'HEAD')
        if git(repo, 'merge-base', '--is-ancestor', head, base, check=False).returncode:
            raise Failure('Worktree commits are not ancestors of the selected base. No deletion; review merge status.')
        git(repo, 'worktree', 'remove', tree)
    print(f'REMOVED {tree}\nBranch preserved: {branch}')


def find_agent(name):
    executable = shutil.which(name)
    if not executable:
        raise Failure(f'Agent executable not found: {name}. Install and authenticate it manually.')
    executable = str(Path(executable).resolve())
    if executable.lower().endswith('.exe') or executable.startswith('/mnt/'):
        raise Failure('Use a Linux Agent executable, not a Windows/mounted-drive executable.')
    return executable


def session(args):
    if not shutil.which('tmux'):
        raise Failure('tmux is required.')
    agent = find_agent(args.agent)
    repo, common, name = repository(args.repo)
    tree, branch = layout(args, repo, name)
    session_name, window_name = f'ws-{name}', f'issue-{args.issue}'
    with locked(common):
        validate_tree(repo, common, tree, branch)
        owner = str(common)
        if run(['tmux', 'has-session', '-t', session_name], check=False).returncode:
            run(['tmux', 'new-session', '-d', '-s', session_name, '-n', 'control', '-c', repo])
            run(['tmux', 'set-option', '-t', session_name, '@workstation-owner', owner])
        else:
            actual_name = run(['tmux', 'display-message', '-p', '-t', session_name, '#{session_name}']).stdout.strip()
            if actual_name != session_name:
                raise Failure('tmux matched a different session name. Inspect it manually.')
            saved = run(['tmux', 'show-options', '-t', session_name, '-v', '@workstation-owner'], check=False)
            if saved.returncode or saved.stdout.strip() != owner:
                raise Failure('Existing tmux session has a different/unknown owner. Inspect it manually.')
        windows = run(['tmux', 'list-windows', '-t', session_name, '-F', '#{window_id}\t#{window_name}']).stdout
        matches = [line.split('\t')[0] for line in windows.splitlines()
                   if line.partition('\t')[2] == window_name]
        if matches:
            if len(matches) != 1:
                raise Failure('Multiple windows share this Issue name. Inspect tmux manually.')
            saved = run(['tmux', 'show-options', '-w', '-t', matches[0], '-v', '@workstation-tree'], check=False)
            saved_agent = run(['tmux', 'show-options', '-w', '-t', matches[0], '-v', '@workstation-agent'], check=False)
            if saved.returncode or saved.stdout.strip() != str(tree):
                raise Failure('Existing Issue window has a different/unknown worktree. No Agent launched.')
            if saved_agent.returncode or saved_agent.stdout.strip() != agent:
                raise Failure('Existing Issue window uses a different Agent. Inspect it manually.')
            print('REUSED existing Issue window; Agent was not started again.')
        else:
            # Multiple shell-command arguments are executed directly by tmux, without string evaluation.
            window_id = run(['tmux', 'new-window', '-d', '-P', '-F', '#{window_id}',
                             '-t', session_name + ':', '-n', window_name, '-c', tree,
                             'bash', str(HERE / 'agent-shell.sh'), agent]).stdout.strip()
            run(['tmux', 'set-option', '-w', '-t', window_id, 'automatic-rename', 'off'])
            run(['tmux', 'set-option', '-w', '-t', window_id, '@workstation-tree', str(tree)])
            run(['tmux', 'set-option', '-w', '-t', window_id, '@workstation-agent', agent])
            print(f'LAUNCHED {args.agent} in {tree}')
    print(f'SESSION {session_name}\nATTACH: tmux attach -t {session_name}')


def doctor(_args):
    missing = []
    release = Path('/proc/sys/kernel/osrelease').read_text().strip() if Path('/proc/sys/kernel/osrelease').exists() else ''
    print('WSL kernel detected: ' + ('yes' if 'microsoft' in release.lower() else 'no (verify Windows wsl -l -v)'))
    for tool, version_arg, required in [('git', '--version', True), ('python3', '--version', True),
                                       ('tmux', '-V', True), ('rg', '--version', True),
                                       ('gh', '--version', False), ('agy', '--version', False),
                                       ('docker', '--version', False), ('node', '--version', False),
                                       ('ruby', '--version', False)]:
        executable = shutil.which(tool)
        if not executable:
            print(f'{"MISSING" if required else "OPTIONAL"} {tool}')
            if required:
                missing.append(tool)
            continue
        if tool == 'agy':
            # Existence only: no model request, login, or provider startup during doctor.
            print(f'FOUND {tool}: {executable} (auth/version not probed)')
            if executable.lower().endswith('.exe') or executable.startswith('/mnt/'):
                print('WARNING: use WSL Linux Agent binary.')
        else:
            value = run([executable, version_arg], check=False)
            first = (value.stdout or value.stderr).splitlines()
            print(f'FOUND {tool}: {first[0] if first else "version unavailable"}')
    print('No authentication, provider, plan, or cloud checks performed.')
    return 1 if missing else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version='workstation 0.1.0')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor', help='Local presence checks only').set_defaults(func=doctor)
    for command, func in [('new-worktree', new_tree), ('remove-worktree', remove_tree), ('session', session)]:
        p = sub.add_parser(command)
        p.add_argument('--repo', default='.', help='Non-bare Git repository path')
        p.add_argument('--issue', required=True, type=issue_number)
        p.add_argument('--root', default=str(Path.home() / 'worktrees'), help='Parent root, outside source repo')
        if command == 'session':
            p.add_argument('--agent', default='agy', help='Single Linux executable name/path; no shell command')
        else:
            p.add_argument('--base', default='origin/main', help='Existing commit reference; no implicit fetch')
        p.set_defaults(func=func)
    args = parser.parse_args()
    try:
        return args.func(args) or 0
    except (Failure, OSError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
