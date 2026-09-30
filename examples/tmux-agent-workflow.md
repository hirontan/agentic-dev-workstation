# 最初の2 Issue

前提: projectは`~/src/demo-app`にあり、origin/mainとAGENTS.mdがある。
Agent `agy`はWSLで導入/認証済み。検証commandはproject側へ記載済み。

```bash
cd ~/src/demo-app
git fetch origin
workstation new-worktree --issue 101
workstation new-worktree --issue 102
workstation session --issue 101 --agent agy
workstation session --issue 102 --agent agy
```

表示された`tmux attach`で接続し、Ctrl-b → wでIssueを選択する。
Issue 101はUI、Issue 102はdocsなど、依存しない範囲へ割り当てる。
[Task prompt](../templates/AGENT_TASK_PROMPT.md)をAgentに渡す。

serverが必要ならworktree内でproject固有のcommandを実行し、host portをIssue別に分ける。
「Agent windowを開いた」ことと「Issueが実行中」であることは別。Agent内で作業開始を確認する。

## Review

Agentの報告に従いworktreeへ移動して、diffとtestの結果を確認する。
必要な修正を同じIssueへ返し、PRを作成してCIと人間レビューを通す。
tmuxのcontrol windowはIssue一覧やGit状態確認に使える。

## Cleanup

Agent/serverを停止し、PRのmergeを確認してからprimary repositoryで以下を実行する。

```bash
git fetch origin
workstation remove-worktree --issue 101
```

未merge、dirty、ignored filesがあれば拒否される。PRがsquash mergeの場合は手動確認が必要。
branchは残るため後から人間が整理する。
