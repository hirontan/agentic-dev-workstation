# Roadmap

## v0.1 — 今回の配布範囲

設計、基本bootstrap、設定、worktree、tmux、テンプレート、検証を一式にする。
Windows実機・WSL実機・Antigravityログイン後の受入は利用者が実施する。

## v0.2 — 実機導入後

- 利用PCのCPU/RAMとWindows/WSL/Agentの実測versionをprivate inventoryに記録。
- 必要なNode/Python/Rubyをproject lockfileに基づき導入するprofileを追加。
- Docker方式を一つ選び、プロジェクトごとのport/volume分離を定型化。
- AntigravityのIDE連携を実機検証し、既知の制約を更新。
- bootstrap rollbackとversion更新手順を改善。

## v0.3 — Agent運用拡張

- Claude Code / Codex / Kiro等を実機検証してadapterとして追加。
- Issue取得、指示ファイル作成、PR下書き作成を段階的に追加。
- 同時実行数と予算管理を追加。課金上限が不明な自動実行は採用しない。
- 再起動後は会話resumeと未commit差分から再開する。プロセス復活とは区別する。

main自動merge・本番deploy・無制限Agent起動はこのリポジトリの初期責務に含めない。
