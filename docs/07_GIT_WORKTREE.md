# 07 — Git worktree

## 作成

```bash
cd ~/src/your-project
git fetch origin
workstation new-worktree --issue 123
```

作成先: `~/worktrees/<repository>-<id>/issue-123`（または `--name` 指定時は `<repository>-<id>/<name>`）
branch: `agent/issue-123`（`--name` 指定時は `agent/<name>`）、base: `origin/main`。
`--issue <番号>` の代わりに `--name <名前>` で任意のタスク名やレビュー環境を作成できる。
`--base <ref>`（ブランチ名、タグ、コミットハッシュ）、`--root <absolute-or-relative-path>`で変更できる。
rootには対象repositoryの内側を指定できない。repository名/id/workspaceをさらに配下へ作る。
同じIssue/名前を再実行した場合は、repositoryとbranchが一致する既存worktreeを再利用する。
同名branchだけ存在しworktreeがない場合は停止し、人間の確認を求める。
同一repositoryのCLI操作はGit common directory内のflockで直列化する。

## 差分確認

```bash
git worktree list
git -C <worktree> status --short
git -C <worktree> diff
```

worktree内の`.git`はファイルの場合がある。`.git`がdirectoryであることを前提にしない。
依存ライブラリのinstallはworktree内で、projectの手順を使う。

## 削除

```bash
workstation remove-worktree --issue 123 --base origin/main
```

削除前にAgentとserverを停止する。CLIはdirtyファイル・未追跡・ignoredファイルも保護する。
生成されたnode_modules等も保護されるため、不要な生成物は確認して手動で片付ける。
通常merge済みのcommit ancestryのみ自動判定する。ネットワークfetchはCLIが勝手に実行しない。
最新baseに更新したい時は人間が先に`git fetch origin`する。
branchは削除しない。branch整理は人間が別途行う。

Squash/rebase merge時の拒否は仕様。PRと残る差分を確認した後、
必要なら`git worktree remove <path>`を手動で行う。forceは使わない。
gitの標準removeもuntracked/ignoredファイルを確認し、必要な`.env`等を先に退避する。
