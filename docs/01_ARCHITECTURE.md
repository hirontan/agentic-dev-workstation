# 01 — Architecture

## 責務

| 層 | 標準 | 責務 |
|---|---|---|
| Host | Windows 11 / Windows Terminal | 入出力、ネットワーク、電源管理 |
| Execution | WSL2 / Ubuntu 24.04 | Git、Agent CLI、test、dev server |
| Session | tmux | 端末からdetach/attachする実行セッション |
| Workspace | Git worktree | Issueごとのファイルとbranchの分離 |
| Agent | Antigravity CLI `agy` | 調査、実装、テスト、説明 |
| Review UI | WSL対応を確認したIDE | 差分、デバッグ、レビュー |
| Workflow | GitHub Issue / PR | 範囲・受入条件・レビュー・統合 |

## データと実行

[Workstation topology](../architecture/workstation.md)と
[Agent execution](../architecture/agent-execution.md)を参照。

Windows側にはIDEとTerminalを置き、Linux側にソース・依存関係・Agentを置く。
Agentのmodel inferenceはprovider側へ送信され得る。WSLで動くことと推論のローカル完結は別である。

## 隔離の境界

worktreeごとにbranchとファイルは分離されるが、Git object store、refs、OSユーザー、HOME、資格情報を共有する。
port、DB、Docker daemon、外部サービスも自動では分離されない。
同じファイルへの並列編集は避ける。共有API/DB schema変更は依存Issueにして順番に統合する。

機密プロジェクトや異なる組織の仕事を同じWSLユーザーで並列実行するかは会社の規程に従う。
必要なら別Linuxユーザー、container、VMへ隔離を強める。

## 復帰の境界

Terminalを閉じてもtmux serverが動いていれば再接続できる。
スリープ中の計算継続、OS再起動後のプロセス保持、WSL shutdown後の復活は提供しない。
再起動後の再開はGit差分・Issue・Agentのresume機能から行う。
