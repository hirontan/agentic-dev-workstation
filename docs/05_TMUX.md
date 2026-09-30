# 05 — tmux

## 構成

repositoryごとに一つのsessionを持ち、controlとIssueごとのwindowを置く。
CLIは名前にrepository idを含めるため、同名repositoryを別場所にcloneしても区別する。

`workstation session`はIssueウィンドウを既定で**左右2分割レイアウト**（左65%: Agent実装、右35%: レビュー・統制シェル）で作成します。
単一画面で起動したい場合は`--no-split`を指定できます。

```bash
tmux list-sessions
tmux attach -t <表示されたsession名>
```

## キー

| キー | 操作 |
|---|---|
| Ctrl-b → d | detach（バックグラウンドで処理継続） |
| Ctrl-b → w | window一覧・プレビュー付き選択 |
| Ctrl-b → n / p | 次 / 前のwindow |
| Ctrl-b → 数字 | window番号へ移動 |
| Ctrl-b → 矢印 | ペイン間（Agent ⇔ レビューシェル）の移動 |
| Ctrl-b → z | 現在のペインを一時的に全画面化 / 復元 |
| Ctrl-b → [ | scroll/copy mode、qで終了 |
| Ctrl-b → r | config再読み込み |
| Ctrl-b → \| / - | 左右 / 上下に手動split |
| マウスクリック | ペイン選択・境界ドラッグでサイズ調整 |

設定は[tmux.conf](../config/tmux/tmux.conf)。既存`~/.tmux.conf`がある場合は自動で置換しない。
必要な行だけ手動で統合してから`tmux source-file ~/.tmux.conf`を使う。

## 継続と停止

Terminalを閉じることと、Agent停止は別。detach後もAgentは動作して通信を継続し得る。
Agentを止める時は、windowに戻ってCLIを終了させる。
window削除や`kill-session`はプロセスを終了させるので未保存状態を確認する。
`kill-server`は全sessionを停止するため、普段の終了操作として使わない。

Windowsのスリープ中に進捗は止まり、WSL/OS停止ではsessionが失われる。
24時間稼働が必要な場合は電源設定とホストの稼働条件が必要。
再起動時は[Migration/Resume](12_MIGRATION.md)に従う。
