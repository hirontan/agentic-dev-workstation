# External sources and verification

確認日: 2026-09-30。外部製品の仕様は変更され得るため、導入/更新時に再確認する。
以下は公式文書。設計上の推奨と実機検証済み状態は区別する。

| Topic | Source | 配布物へ反映した範囲 |
|---|---|---|
| WSL install | https://learn.microsoft.com/en-us/windows/wsl/install | WSL2 / Ubuntuの導入手順 |
| WSL filesystems | https://learn.microsoft.com/en-us/windows/wsl/filesystems | Linux CLIから使うソースの配置 |
| WSL configuration | https://learn.microsoft.com/en-us/windows/wsl/wsl-config | resource例と停止を伴う反映 |
| WSL commands | https://learn.microsoft.com/en-us/windows/wsl/basic-commands | shutdownの停止範囲、export |
| VS Code WSL | https://code.visualstudio.com/docs/remote/wsl | Windows IDEからWSLへ接続 |
| Git worktree | https://git-scm.com/docs/git-worktree | worktreeの作成/削除と共有Git |
| tmux | https://github.com/tmux/tmux/wiki/Getting-Started | session/windowとdetach/attach |
| Antigravity CLI install/auth | https://antigravity.google/docs/cli/install/ | Linux installer、配布先、手動login |
| Antigravity settings | https://antigravity.google/docs/settings?tab=cli | renderingと権限の確認方針 |
| Antigravity best practices | https://antigravity.google/docs/cli/best-practices | root rulesを読ませる方針 |

## 未検証/採用しない断定

- Antigravity standalone IDEの特定versionが最新であるという固定記述。
- standalone IDEのWSL対応有無を恒久的に断定すること。
- VS Code向けAntigravity extensionのWSL互換性や正確なextension ID。
- WindowsとWSL間でAgent認証が自動共有されること。
- tmuxがsleep/rebootを越えてAgentを24時間継続実行すること。
- AGENTS.mdだけで権限・情報送信が制限されること。
- 月額契約だけで無制限のAgent並列実行を保証すること。

CLI導入先と方法は公式情報から確認済み。実際のinstall/login/料金/IDE接続は利用者の実機受入で確認する。
