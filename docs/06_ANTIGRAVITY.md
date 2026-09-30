# 06 — Antigravity

## 確認状態

2026-09-30に公式CLIインストール手順を確認。
Linux側の標準実行名は`agy`、公式配布先は`~/.local/bin/agy`。
この配布物はAntigravityを導入・認証して動作確認したものではない。
参照先と未確定事項は[SOURCES](../SOURCES.md)へ記録する。

## 導入

WSLの通常ユーザーで公式インストーラをダウンロードし、内容を確認してから実行する。
bootstrapに組み込まないため、再実行だけでAgentを更新することはない。

```bash
mkdir -p ~/.local/share/agentic-dev-workstation
curl -fSL https://antigravity.google/cli/install.sh \
  -o ~/.local/share/agentic-dev-workstation/antigravity-install.sh
less ~/.local/share/agentic-dev-workstation/antigravity-install.sh
bash ~/.local/share/agentic-dev-workstation/antigravity-install.sh --skip-aliases --skip-path
source ~/.bashrc
command -v agy
```

公式側の配布URL・引数が変更されたら、公式手順を再確認して更新する。
インストーラのhashを記録する場合は`sha256sum`を使う。hash記録だけで配布元の信頼性を証明しない。

## 初回設定

worktree内で`agy`を実行し、CLIの案内に従って本人がログインする。
tmuxではInline renderingを選び、scrollbackと画面崩れを確認する。
WSLのブラウザ/keyring連携が失敗したら、公式Auth/Troubleshootingを確認する。
認証tokenを貼り付けて共有したり、Windowsの認証cacheを手でコピーしたりしない。

## 料金とデータ

アカウント方式とAPI key方式の課金を同一視しない。
初期構成はAPI keyを設定しない。利用枠と制限はログイン後に確認する。
local CLIでもコード・指示・tool結果がproviderへ送られ得る。
会社コードは会社が認めた契約、設定、アカウントでのみ利用する。

## Rules

AGENTS.mdをproject rulesの正本とする。
CLIへ最初に「AGENTS.mdを読んでこのIssueに適用する制約を要約」と依頼し、読み込みを確認する。
IDEとCLIのrule discoveryの差は実機確認する。別形式が必要なら正本からの短い参照文にする。
利用権限を回避するフラグはlauncherへ追加しない。

## 最初の起動

```bash
workstation session --issue 123 --agent agy
```

別Agentの起動にも`--agent <コマンド名>`を使える。v0.1は追加引数やAPI設定を自動生成しない。
provider内部subagentとworktreeを分けた独立Agentは別の並列化である。
最初は独立Agentを2つ程度とし、nested並列化は利用枠を確認してから扱う。
