# 17 — 使い方ガイド（実践ワークフロー）

本ワークステーションを使って、Coding Agent（Antigravity等）と並列開発を進めるための実践的な操作手順ガイドです。

---

## 1. コマンド早見表（チートシート）

| フェーズ | 実行コマンド | 説明 |
|---|---|---|
| **準備** | `cd /path/to/your-project`<br>`git fetch origin` | 対象のGitリポジトリへ移動し、最新情報を取得 |
| **作業場所の作成** | `workstation new-worktree --issue 106` | ブランチ `agent/issue-106` と専用ディレクトリを自動作成 |
| **セッション起動** | `workstation session --issue 106 --agent agy` | 左右2分割（左: Agent / 右: レビューシェル）でtmux起動 |
| **接続** | `tmux attach -t ws-<リポジトリ名>-<id>` | 作成されたtmuxセッションへ接続 |
| **指示出し** | AgentプロンプトにIssue本文・受入条件を入力 | 左ペインのAgent（`agy`）へ実装を依頼 |
| **一時離脱 (並列化)** | `Ctrl-b` → `d` | Agentのバックグラウンド実行を維持したままシェルへ戻る |
| **確認・PR** | 右ペインでテスト・差分確認<br>`git push -u origin agent/issue-106`<br>`gh pr create` | 右ペインのシェルを使ってレビューとPR作成 |
| **後片付け** | `git fetch origin`<br>`workstation remove-worktree --issue 106` | PRマージ後、元のリポジトリでworktreeを安全に削除 |

---

## 2. 初回セットアップ

各OS用のbootstrapスクリプトを実行します。既定はdry-run（Plan表示のみ）のため、`--apply`を指定して適用します。

### Windows + WSL2の場合
```bash
# WSL上のUbuntuターミナルで実行
cd ~/src/agentic-dev-workstation
bash bootstrap/wsl/setup.sh --apply
source ~/.zshrc  # Bashの場合は source ~/.bashrc
workstation doctor
```

### macOSの場合
```bash
# macOSのターミナルで実行（Homebrew導入済み環境）
cd ~/src/agentic-dev-workstation
bash bootstrap/macos/setup.sh --apply
source ~/.zshrc  # Bashの場合は source ~/.bash_profile
workstation doctor
```

`workstation doctor` を実行し、Git、Python3、tmux、ripgrep、Agent等のツールが認識されていることを確認します。

---

## 3. 日常の開発手順（ステップ・バイ・ステップ）

### Step 1: 作業対象のリポジトリに移動する
対象のリポジトリはどこにあっても構いません（`~/src/` 配下でなくても、任意のGitリポジトリで動作します）。
```bash
cd /path/to/your-project
git fetch origin
```

### Step 2: Issue専用の作業場所を作成する（`new-worktree`）
**手動でブランチを作成する必要はありません。** CLIが自動的に最新の `origin/main` からブランチと作業ディレクトリを作成します。

```bash
workstation new-worktree --issue 106
```
- `--issue` にはGitHubの **Issue番号（半角数字）** を指定します（ブランチ名文字列は指定できません）。
- ローカルの `main` をベースにしたい場合は `--base main` を付与します。
- 実行後、`~/worktrees/<リポジトリ名>-<id>/issue-106` ディレクトリと `agent/issue-106` ブランチが生成されます。

### Step 3: Agentセッションを起動する（`session`）
```bash
workstation session --issue 106 --agent agy
```
起動時に表示される `tmux attach` コマンドで接続します：
```bash
tmux attach -t ws-<リポジトリ名>-<id>
```

#### 画面レイアウト（自動で左右2分割されます）
セッションに接続すると、ターミナル1画面が自動的に左右2分割で立ち上がります：

```text
┌──────────────────────────────────────┬─────────────────────────┐
│ 左ペイン (65%): Agent 実装           │ 右ペイン (35%): 統制・PR│
│ (初期フォーカス)                     │                         │
│                                      │ $ git status            │
│ $ agy                                │ $ git diff              │
│ > Issue #106 の実装を進めています... │ $ cargo test / npm test │
│                                      │ $ gh pr create          │
│                                      │                         │
└──────────────────────────────────────┴─────────────────────────┘
```
- **左ペイン（65%）**: Agent（`agy`）が起動しており、そのまま指示を入力できます。
- **右ペイン（35%）**: 同じworktreeのシェルが開いており、テスト実行や差分確認を並行して行えます。

### Step 4: AgentにIssueを指示する
プロジェクト配下に独自の `.antigravity*` 等の設定フォルダを作る必要はありません。
プロジェクトルートの `AGENTS.md` にルールを記載し、Agentに以下のように指示を渡します：

```text
このworktreeのAGENTS.md、README、対象設計書を読み、下記Issueを実装してください。
受入条件を満たしたらテストを実行し、変更概要を報告してください。

【Issue #106 内容】
...ここにGitHubのIssue本文や受入条件を貼り付け...
```

### Step 5: tmuxの画面操作と並列実行

| やりたいこと | キー操作 | 説明 |
|---|---|---|
| **ペインの移動** | `Ctrl-b` → 矢印キー（またはマウスクリック） | 左ペイン（Agent）と右ペイン（シェル）を往復 |
| **一時的に全画面化** | `Ctrl-b` → `z` | 狭いペインを一時的に全画面表示（再度押すと戻る） |
| **一時離脱（Detach）** | `Ctrl-b` → `d` | Agentを動かしたままセッションを抜ける |
| **複数Issueの切り替え** | `Ctrl-b` → `w` | 別Issueのウィンドウをプレビュー付きで一覧選択 |

> [!TIP]
> `Ctrl-b` → `d` で抜けた後、別のIssue（例: `--issue 107`）を立ち上げれば、複数のAgentを並列で動かせます。

### Step 6: レビューとPR作成
Agentの実装が完了したら、右ペイン（またはローカルのIDE）で成果物を確認します：

```bash
# 差分の確認
git status
git diff origin/main

# プロジェクトの検証テスト
cargo test  # npm test, pytest など
```

問題がなければ、PRを作成します：
```bash
git push -u origin agent/issue-106
gh pr create --title "feat: Issue 106の変更内容"
```

### Step 7: マージ後の片付け（`remove-worktree`）
PRがGitHub上でマージされたら、元のリポジトリに戻ってworktreeを安全に削除します：

```bash
cd /path/to/your-project  # 元のリポジトリへ戻る
git fetch origin
workstation remove-worktree --issue 106
```

※未マージのコミットや、未コミットの変更・無視ファイルが存在する場合、CLIはデータを保護するため安全に削除を拒否します。

---

## 4. よくあるエラーと対処法

### Q1. `ERROR: Path is not the registered worktree for this Issue branch.`
- **原因**: 先に `workstation new-worktree --issue <番号>` を実行していないか、コマンド入力時のハイフンが1つ（`-issue`）になっていたためworktreeが未作成です。
- **対処**: まず `workstation new-worktree --issue <番号>` を実行してから、`session` を起動してください。

### Q2. `error: argument --issue: Issue must be a positive number`
- **原因**: `--issue` にブランチ名文字列（例: `feat/xxx`）を指定しています。
- **対処**: `--issue` には数字（Issue番号、例: `106`）のみを指定してください。

### Q3. `CONFLICT preserved ... (merge manually)`
- **原因**: bootstrap再実行時に、リポジトリ側のテンプレートと既存設定ファイルの内容に差分があるため、既存設定が上書きされず保護されました。
- **対処**: 意図した保護動作です。最新テンプレートに統一したい場合は、手動でファイルを更新または削除して再実行してください。

### Q4. `workstation: command not found`
- **原因**: 新しいターミナルを開いていないか、シェルの設定ファイルが再読み込みされていません。
- **対処**: お使いのシェルに合わせて `source ~/.zshrc`（または `source ~/.bashrc`）を実行してください。
