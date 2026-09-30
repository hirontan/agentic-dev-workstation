# 08 — Agent workflow

## IssueをReadyにする

目的、再現例、変更可能範囲、非対象、受入条件、依存Issue、検証コマンドを記載する。
[Issue template](../templates/ISSUE_TEMPLATE.md)と[Task prompt](../templates/AGENT_TASK_PROMPT.md)を使う。
「この機能を作る」だけでは並列作業で担当が衝突するため、責務とinterfaceを明記する。

## 実装

1. `git fetch origin`後、worktreeを作成する。
2. tmux windowでAgentを起動する。
3. AGENTS.mdとIssueを渡し、範囲と検証方法の理解を確認する。
4. Agentは実装・test・差分説明を行う。
5. 人間は受入条件と実結果を照合する。

shared schemaやAPI契約に依存するIssueは、土台を先にmergeする。
独立したUI、docs、test改善等を同時に実施しやすい単位として扱う。
複数Agentが同じbranch/worktreeを同時編集しない。

## PR

PRには問題と変更後の挙動、検証結果、未検証、migration影響を記載する。
レビュー専用worktreeを使う時は実装worktreeへ変更を書かない。
GitHubでbranch protection・required checks・人間承認を設定する。
AGENTS.mdに禁止と書くだけではGitHub側の権限制御にはならない。

## 完了

merge後にAgent/serverを停止、worktreeの未commit/ignoredファイルを確認、最新mainを取得、worktreeを削除する。
Issueに受入結果とPRリンクを残す。CLIはGitHubへの書き込みを自動では行わない。

## 監督の負荷

同時進行は2 Issueから開始。Ready条件と完了報告を揃え、レビュー待ちが増えたら新規起動を抑える。
「常時Agent数を最大にする」より、受入可能な成果が順に届く状態を目指す。
