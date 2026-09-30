# 14 — Repository structure

| Path | 責務 |
|---|---|
| README.md | 入口、quick start、初期scope |
| AGENTS.md | 本リポジトリの編集ルール |
| docs/00〜16 | 設計、導入、運用、受入 |
| architecture/ | topology / execution / workflow |
| adr/ | 判断理由と代替案 |
| bootstrap/windows/setup.ps1 | WSLのplan/apply |
| bootstrap/wsl/setup.sh | Ubuntu base導入、設定保護 |
| bootstrap/macos/setup.sh | macOS base導入、設定保護 |
| config/windows/ | WSL resource設定例 |
| config/tmux/ | tmux標準設定 |
| config/git/gitconfig | identityを含まない共通Git設定 |
| config/shell/ | Bash/ZshのPATH |
| config/antigravity/ | 設定方針のみ。tokenは含めない |
| bin/workstation | symlinkから呼べるCLI入口 |
| scripts/workstation.py | worktree/session/doctorの実装 |
| scripts/*.sh | operation wrapper、project template導入 |
| templates/ | project rules、Issue、Agent指示、inventory |
| examples/ | 最初のIssue並列実行例 |
| tests/ | 実Git、実tmux、syntax、document link検証 |
| .github/ | Issue/PR template、validation CI |
| SOURCES.md | 外部仕様の確認日と公式参照 |
| VALIDATION.md | 配布時の実行結果と未検証 |
| ROADMAP.md | 後続profileと自動化の段階 |

## 初期化してGitHubへ登録

展開したフォルダをWSL側`~/src`へ置いてから実行する。

```bash
cd ~/src/agentic-dev-workstation
git init -b main
git add .
git commit -m 'Bootstrap agentic development workstation'
```

GitHubで自分のaccountまたはorganizationに空repositoryを作る。
public/privateを選び、表示される自分のremote URLを登録する。

```bash
git remote add origin <自分のrepository URL>
git push -u origin main
```

CI成功後にmainのrequired checksとreviewルールを設定する。
既存repositoryへ追加する場合は`git init`をせず作業branchから取り込む。
