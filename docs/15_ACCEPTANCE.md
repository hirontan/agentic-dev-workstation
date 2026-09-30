# 15 — 実機受入

## Windows / WSL

- Windows bootstrapをplanで実行し、変更しないことを確認。
- apply後`wsl -l -v`でUbuntuがVERSION 2、通常ユーザーでログイン可能。
- WSL bootstrapをplanで実行し、packages/settingsが変わらない。
- applyを2回実行し、source行・symlinkが重複せず、既存設定を維持。
- doctorでLinux Git/Python/tmux/CLIを確認。

## Sandbox project

外部サービス不要の練習repositoryで始める。

```bash
mkdir -p ~/src/workstation-demo
cd ~/src/workstation-demo
git init -b main
printf '# Demo\n' > README.md
git add README.md
git commit -m 'Initial demo'
workstation new-worktree --issue 1 --base main
workstation session --issue 1 --agent agy
```

AgentへAGENTS.mdを読ませ、READMEの簡単な変更を依頼する。
mainのworktreeへ変更が入らないこと、detach/attach後に戻れることを確認する。
CLI終了後はAgent windowのshellで進捗とexit codeを見られる。

## Parallel

別Issueを作り、別branch/path/windowで動くことを確認する。
shared port/DBの衝突が起きない設定をproject側へ用意する。
実機のCPU/RAM/利用枠を確認し、並列数を決める。

## Cleanup

dirtyファイルがある状態、未merge状態で削除を拒否することを確認。
Agent停止・通常merge後、cleanなworktreeだけ削除されbranchは残ることを確認。
練習で作ったローカルIssue番号はGitHub上に存在しなくてもCLIは動作する。

## Record

PC、Windows、WSL、Ubuntu、tmux、Agent/IDE versions、確認日、成功/失敗/未検証をprivate inventoryへ残す。
配布時の検証と実機受入を区別する。配布時の結果は[VALIDATION](../VALIDATION.md)。
