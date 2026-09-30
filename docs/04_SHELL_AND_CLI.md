# 04 — Shell and CLI

## Base profile

bootstrapはUbuntu aptで以下を導入する。
`build-essential ca-certificates git curl wget unzip zip jq ripgrep fd-find fzf tmux direnv tree htop gh python3 shellcheck ncurses-term`

`apt-get update`と`apt-get install`を実行するが、全OSのupgradeは自動実行しない。
apt repoの現在versionを使うため、bit単位で同一の再現は保証しない。
適用後のpackage versionsを`~/.local/state/agentic-dev-workstation/packages.tsv`へ記録する。
fd-findのUbuntuコマンド名は`fdfind`。

## Git設定

identityとcredential helperは自動設定しない。
共通設定を使う場合は、自分の`~/.gitconfig`へ以下を手動で追加する。
既に設定がある項目は競合を確認する。

```ini
[include]
    path = ~/.config/agentic-dev-workstation/gitconfig
```

`git config --show-origin --get user.email`等で個人/会社のidentityを確認する。
プロジェクト別identityは`includeIf`かrepository-local configで設定する。

## Runtime profiles — v0.1では手動

| Tool | 方針 | 正本 |
|---|---|---|
| Node | LTSとproject指定versionを照合しversion managerで導入 | `.node-version`等、lockfile |
| Python | system Pythonをbootstrap専用にし、projectはvenv/uv/Poetry等 | `pyproject.toml`、lockfile |
| Ruby | system Rubyに依存せずversion managerで導入 | `.ruby-version`、Gemfile.lock |
| Docker | Desktop WSL integrationかLinux Engineの一つを選択 | Compose / project docs |
| AWS CLI | 必要時のみ公式配布。SSOと短期credentialを優先 | project infra docs |
| Terraform | projectが指定するversionを導入 | required_version / lockfile |

このリポジトリに業務アプリのruntime versionを一律固定しない。
新しいprofileを自動化する際は、導入元・version・update・rollback・権限のADRを追加する。

## Dockerの分離

同一WSLに二つのDocker daemon方式を混在させない。
worktreeごとに`COMPOSE_PROJECT_NAME`、host port、DB名を分ける。
例: `demo-issue-123`と`demo-issue-124`、portは3101/3102等。
Docker volumeの共有と本番DBへの接続を避け、テスト用seedを使う。
