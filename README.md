# Agentic Dev Workstation

Reproducible development workstation for agentic software engineering.

Windows 11 + WSL2 Ubuntu または macOS + tmux + Git worktree を使い、GitHub Issue単位で
Coding Agentへ実装を依頼するための、設計・セットアップ・運用の正本です。
人間は作業範囲と受入条件を決め、差分・テスト・PRをレビューします。
Antigravity CLIを最初の実行ツールとし、他のAgentへ交換できる構成にします。

## v0.1の範囲

| 含む | 適用方法 |
|---|---|
| Architecture / ADR / 日本語の運用手順 | `docs/`、`architecture/`、`adr/` |
| WindowsのWSL導入 | PowerShell、既定は変更予定の表示 |
| Ubuntu基本CLI・tmux・shell設定 | Bash、既定は変更予定の表示 |
| macOS基本CLI・tmux・shell設定 | Bash/Homebrew、既定は変更予定の表示 |
| worktree作成・安全な削除 | `bin/workstation` |
| tmuxセッション作成・Agent起動 | `bin/workstation session` |
| プロジェクト用AGENTS・Issue・PRテンプレート | `templates/` |
| ローカル検証とGitHub Actions | `tests/`、`.github/workflows/` |

Node / Ruby / Docker / AWS / Terraformは[導入方針](docs/04_SHELL_AND_CLI.md)を記載しています。
v0.1のbootstrapはそれらやAgentを自動インストールせず、ログイン・クラウド接続も行いません。
GitHubへリポジトリを作成・公開する操作は含みません。

## 最初に読む

1. [全体像](docs/00_OVERVIEW.md)
2. [Architecture](docs/01_ARCHITECTURE.md)
3. [Bootstrap方針](docs/13_BOOTSTRAP_POLICY.md)
4. [Windows](docs/02_WINDOWS_HOST.md) → [WSL2](docs/03_WSL2.md) または [macOS](docs/16_MACOS_HOST.md)
5. [Antigravity](docs/06_ANTIGRAVITY.md) → [最初のIssue](examples/tmux-agent-workflow.md)

## Quick start

### Windows + WSL2

Windows側で展開したフォルダから、管理者PowerShellを開きます。
WSL導入済みならWindowsの導入工程を省略できます。

```powershell
.\bootstrap\windows\setup.ps1
.\bootstrap\windows\setup.ps1 -Apply
```

再起動が必要な場合はWindowsの案内に従い、Ubuntuを開いてLinuxユーザーを作成します。
Ubuntuの`~/src/agentic-dev-workstation`へこのフォルダを置きます。
GitHubに登録済みの場合は、自分のURLを指定してcloneしてください。

```bash
cd ~/src/agentic-dev-workstation
bash bootstrap/wsl/setup.sh
bash bootstrap/wsl/setup.sh --apply
source ~/.bashrc
workstation doctor
```

### macOS

Homebrewが導入された環境でターミナルを開きます（未導入時は [macOS host](docs/16_MACOS_HOST.md) 参照）。

```bash
cd ~/src/agentic-dev-workstation
bash bootstrap/macos/setup.sh
bash bootstrap/macos/setup.sh --apply
source ~/.zshrc  # Bashの場合は source ~/.bashrc
workstation doctor
```

`~/.local/bin/workstation`はこのフォルダへのsymlinkです。移動後はbootstrapを再実行してください。
実行権限が失われたZIP展開でも、Bash/Pythonで呼び出せます。

Git identityとGitHub認証は本人が設定します。

```bash
git config --global user.name 'YOUR_NAME'
git config --global user.email 'YOUR_EMAIL'
gh auth login
```

Antigravityは[公式インストーラを確認して導入](docs/06_ANTIGRAVITY.md)し、WSLまたはmacOSで`agy`を起動してログインします。
プロジェクトでは次の順に使います。

```bash
cd ~/src/your-project
git fetch origin
workstation new-worktree --issue 123
workstation session --issue 123 --agent agy
# 表示されたtmux attachコマンドで接続し、Issueの指示を入力する
```

既定の作成元は`origin/main`です。GitHub未登録のローカル環境では`--base main`を指定できます。
Issue本文は[テンプレート](templates/AGENT_TASK_PROMPT.md)に沿って渡します。
CLIはIssueの取得・自動送信・PR作成・mergeを行いません。

## 設計原則

- ソースコード・依存関係・worktreeはWSLのLinuxファイルシステム（またはmacOSネイティブ領域）へ置く。
- 一つのIssueに一つのbranch/worktreeを割り当てる。
- worktreeはファイルの分離。資格情報、DB、Docker、portの分離は別途設計する。
- tmuxは端末切断からセッションを保護する。スリープ・WSL停止・OS再起動時の実行保証はない。
- mainへの直接変更と自動mergeを避け、PRでレビューする。
- ローカル開発でもモデルへの通信は発生し得る。課金上限と会社の利用規程を確認する。

## ディレクトリと運用

[ディレクトリ構成](docs/14_REPOSITORY_STRUCTURE.md) / [日常運用](docs/08_AGENT_WORKFLOW.md) / [macOS環境](docs/16_MACOS_HOST.md) /
[Security](docs/10_SECURITY.md) / [Troubleshooting](docs/11_TROUBLESHOOTING.md) /
[Migration](docs/12_MIGRATION.md) / [Roadmap](ROADMAP.md) / [検証結果](VALIDATION.md)

設計判断は[ADR一覧](adr/README.md)、外部仕様の確認日と参照先は[SOURCES.md](SOURCES.md)へ残します。
OSやAgentの最新版を恒久的に保証する構成ではありません。
