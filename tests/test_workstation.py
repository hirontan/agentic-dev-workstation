import concurrent.futures
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'scripts/workstation.py'


def execute(args, cwd=None, env=None):
    return subprocess.run([str(a) for a in args], cwd=cwd, env=env, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class WorktreeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='workstation test ')
        self.base = Path(self.temp.name)
        self.repo = self.base / 'repo with spaces'
        self.repo.mkdir()
        self.root = self.base / 'trees with spaces'
        self.g('init', '-b', 'main')
        self.g('config', 'user.name', 'Test User')
        self.g('config', 'user.email', 'test@example.invalid')
        (self.repo / 'README.md').write_text('Initial\n')
        self.g('add', 'README.md')
        self.g('commit', '-m', 'Initial')

    def tearDown(self):
        self.temp.cleanup()

    def g(self, *args, repo=None):
        result = execute(['git', '-C', repo or self.repo, *args])
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def cli(self, command, *extra, issue='123', repo=None, env=None):
        return execute([sys.executable, CLI, command, '--repo', repo or self.repo,
                        '--root', self.root, '--issue', issue, *extra], env=env)

    def make_tree(self, issue='123'):
        result = self.cli('new-worktree', '--base', 'main', issue=issue)
        self.assertEqual(result.returncode, 0, result.stderr)
        return Path(result.stdout.splitlines()[0].split(' ', 1)[1])

    def test_create_reuse_spaces_and_main_isolation(self):
        tree = self.make_tree()
        result = self.cli('new-worktree', '--base', 'main')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('REUSED', result.stdout)
        (tree / 'README.md').write_text('Agent change\n')
        self.assertEqual((self.repo / 'README.md').read_text(), 'Initial\n')
        self.assertEqual(self.g('branch', '--show-current', repo=tree), 'agent/issue-123')

    def test_issue_validation(self):
        for bad in ['0', '-1', '123; touch injected', '1/../../x', '01', 'abc']:
            self.assertNotEqual(self.cli('new-worktree', '--base', 'main', issue=bad).returncode, 0)
        self.assertFalse(self.root.exists())

    def test_missing_base_no_branch_created(self):
        result = self.cli('new-worktree')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.g('branch', '--list', 'agent/issue-123'), '')

    def test_existing_branch_no_reset(self):
        self.g('branch', 'agent/issue-123')
        result = self.cli('new-worktree', '--base', 'main')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('already exists', result.stderr)

    def test_nested_root_rejected(self):
        result = self.cli('new-worktree', '--base', 'main', '--root', self.repo / 'trees')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.repo / 'trees').exists())

    def test_dirty_and_ignored_data_protected(self):
        tree = self.make_tree()
        (tree / 'local.txt').write_text('untracked')
        result = self.cli('remove-worktree', '--base', 'main')
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(tree.exists())
        (tree / 'local.txt').unlink()
        self.g('config', 'core.excludesFile', str(self.base / 'ignore'))
        (self.base / 'ignore').write_text('.env\n')
        (tree / '.env').write_text('TEST_DATA=private\n')
        self.assertNotEqual(self.cli('remove-worktree', '--base', 'main').returncode, 0)
        self.assertTrue((tree / '.env').exists())

    def test_unmerged_rejected_and_merged_removed_branch_retained(self):
        tree = self.make_tree()
        (tree / 'feature.txt').write_text('Feature\n')
        self.g('add', 'feature.txt', repo=tree)
        self.g('commit', '-m', 'Feature', repo=tree)
        self.assertNotEqual(self.cli('remove-worktree', '--base', 'main').returncode, 0)
        self.g('merge', '--ff-only', 'agent/issue-123')
        result = self.cli('remove-worktree', '--base', 'main')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(tree.exists())
        self.assertIn('agent/issue-123', self.g('branch', '--list'))

    def test_collision_same_name_repositories(self):
        first = self.make_tree()
        second_repo = self.base / 'other' / self.repo.name
        second_repo.parent.mkdir()
        result = execute(['git', 'clone', '--no-local', self.repo, second_repo])
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.cli('new-worktree', '--base', 'main', repo=second_repo)
        self.assertEqual(result.returncode, 0, result.stderr)
        second = Path(result.stdout.splitlines()[0].split(' ', 1)[1])
        self.assertNotEqual(first.parent, second.parent)

    def test_subdirectory_and_linked_worktree_resolve_same_identity(self):
        tree = self.make_tree()
        sub = self.repo / 'subdirectory'
        sub.mkdir()
        for place in [sub, tree]:
            result = self.cli('new-worktree', '--base', 'main', repo=place)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(tree), result.stdout)

    def test_concurrent_creation_reuses_one_tree(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: self.cli('new-worktree', '--base', 'main'), range(2)))
        self.assertTrue(all(item.returncode == 0 for item in results), [r.stderr for r in results])
        self.assertEqual(sum('CREATED' in item.stdout for item in results), 1)

    def test_wrong_path_refuses_reuse(self):
        tree = self.make_tree()
        self.g('worktree', 'remove', tree)
        tree.mkdir()
        (tree / 'valuable.txt').write_text('Do not overwrite\n')
        result = self.cli('new-worktree', '--base', 'main')
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue((tree / 'valuable.txt').exists())

    def test_project_template_refuses_overwrite(self):
        script = ROOT / 'scripts/bootstrap-project.sh'
        first = execute(['bash', script, self.repo])
        self.assertEqual(first.returncode, 0, first.stderr)
        (self.repo / 'AGENTS.md').write_text('Existing project policy\n')
        second = execute(['bash', script, self.repo])
        self.assertNotEqual(second.returncode, 0)
        self.assertEqual((self.repo / 'AGENTS.md').read_text(), 'Existing project policy\n')

    def test_bootstrap_default_is_plan(self):
        result = execute(['bash', ROOT / 'bootstrap/wsl/setup.sh'])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('No changes', result.stdout)

    @unittest.skipUnless(shutil.which('tmux'), 'Real tmux not installed')
    def test_real_tmux_launch_and_no_duplicate_agent(self):
        tree = self.make_tree()
        tmux_binary = shutil.which('tmux')
        helpers = self.base / 'helpers'
        helpers.mkdir()
        socket = 'workstation-test-' + str(os.getpid())
        wrapper = helpers / 'tmux'
        # All runtime paths are passed through environment, not interpolated into shell code.
        wrapper.write_text('#!/usr/bin/env bash\nexec "$TEST_TMUX_BINARY" -L "$TEST_TMUX_SOCKET" -f "$TEST_TMUX_CONFIG" "$@"\n')
        wrapper.chmod(0o755)
        agent = helpers / 'test-agent'
        agent.write_text('#!/usr/bin/env bash\nprintf "run\\n" >> "$TEST_AGENT_MARKER"\n')
        agent.chmod(0o755)
        marker = self.base / 'agent-runs'
        environment = dict(os.environ, PATH=str(helpers) + os.pathsep + os.environ['PATH'],
                           TEST_TMUX_BINARY=tmux_binary, TEST_TMUX_SOCKET=socket,
                           TEST_TMUX_CONFIG=str(ROOT / 'config/tmux/tmux.conf'),
                           TEST_AGENT_MARKER=str(marker), TERM='xterm-256color')
        environment.pop('TMUX', None)
        try:
            result = self.cli('session', '--agent', 'test-agent', env=environment)
            self.assertEqual(result.returncode, 0, result.stderr)
            for _ in range(50):
                if marker.exists():
                    break
                time.sleep(.05)
            self.assertTrue(marker.exists(), result.stdout)
            second = self.cli('session', '--agent', 'test-agent', env=environment)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn('REUSED', second.stdout)
            self.assertEqual(marker.read_text(), 'run\n')
            session_name = [line[8:] for line in result.stdout.splitlines() if line.startswith('SESSION ')][0]
            paths = execute(['tmux', 'list-panes', '-a', '-F', '#{pane_current_path}'], env=environment)
            self.assertIn(str(tree), paths.stdout)
            # Unknown session ownership must stop reuse.
            execute(['tmux', 'set-option', '-t', session_name, '@workstation-owner', 'other'], env=environment)
            self.assertNotEqual(self.cli('session', '--agent', 'test-agent', env=environment).returncode, 0)
        finally:
            execute(['tmux', 'kill-server'], env=environment)


if __name__ == '__main__':
    unittest.main()
