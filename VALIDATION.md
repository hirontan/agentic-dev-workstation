# Validation — v0.1.0

確認日: 2026-09-30。Linux検証環境で次を実行し、すべてPASS。

```bash
bash tests/check.sh
```

| 検証 | 結果 |
|---|---|
| Bash syntax / ShellCheck 0.9.0 | PASS |
| Python syntaxとunittest 14件 | PASS、skipなし |
| Git worktree作成/再利用/変更隔離 | PASS |
| 不正Issue / 不明base / 既存branch / 既存path | PASS、変更を拒否 |
| 同名repository / path内space / subdirectory / linked worktree | PASS |
| 同時作成 | PASS、一つだけ作成して再利用 |
| dirty / untracked / ignored filesの削除保護 | PASS |
| 未merge削除拒否 / 通常merge後削除 / branch保持 | PASS |
| 実tmux起動 / worktree path / Agent二重起動防止 / owner確認 | PASS |
| project AGENTS templateの既存ファイル保護 | PASS |
| Ubuntu bootstrapの既定plan出力 | PASS |
| Markdown内部リンク / code fences | PASS |

実Git 2.51.1、tmux 3.4、Python 3.12.3を使用。
実tmux検証は専用socketと一時repository上で、外部通信をしないテスト用commandを起動した。
Antigravity本体の起動・model inferenceをテストしたものではない。

## 利用者の実機受入

WindowsのWSL導入、Ubuntu bootstrapのapt installと既存設定統合、Antigravityの導入/login、
IDEのWSL接続、Docker/runtime profile、会社規程・利用枠の確認は配布時検証に含めない。
[実機受入](docs/15_ACCEPTANCE.md)に従い、private inventoryへ結果を記録する。

## CI

GitHub ActionsはLinuxのShellCheck/Git/tmux testと、WindowsのPowerShell parse/plan/WhatIfを定義する。
この配布物の作成中にGitHubのCIを起動したものではない。
