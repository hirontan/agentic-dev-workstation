# Repository workflow

## 一つのIssueのライフサイクル

Ready → Running → Review → Merged → Cleanedを運用上の状態とする。
GitHub Projectやlabelへ反映できるが、v0.1は状態同期を実装しない。

| 状態 | 証拠 | 次へ進める条件 |
|---|---|---|
| Ready | Issueと受入条件 | 依存Issue解消、担当と範囲が明確 |
| Running | branch / worktree / tmux session | 実装とlocal checkを完了 |
| Review | commit / PR / CI | 差分、テスト、人間レビューが完了 |
| Merged | mainに変更が反映 | Agentとserverを停止、差分を保存 |
| Cleaned | worktreeを削除 | branchは必要に応じて別途整理 |

CLIの削除はcleanかつ指定baseへ通常merge済みのworktreeに限定する。
Squash/rebase mergeではcommit ancestryが一致しないことがあるため、CLIは保守的に削除を拒否する。
その場合はPRとdiffを人間が確認し、標準の`git worktree remove`を手動で使う。
