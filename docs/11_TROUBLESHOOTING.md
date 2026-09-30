# 11 — Troubleshooting

| 症状 | 確認 | 対応 |
|---|---|---|
| WSL導入失敗 | virtualization、Windows version、管理権限 | Microsoft公式WSL troubleshooting |
| Linuxコマンドが遅い | repositoryが`/mnt/c`か | Linux側`~/src`へcloneし直す |
| `workstation`が見つからない | PATH、symlink | `source ~/.bashrc`、bootstrap再実行 |
| `agy`がWindows binary | `command -v agy`、doctor | WSL側へLinux CLIを導入 |
| `origin/main`がない | remote / default branch | `git fetch origin`、正しい`--base` |
| worktree作成を拒否 | branch/pathの既存状態 | `git worktree list`、残存branchを確認 |
| worktree削除を拒否 | dirty/ignored/未merge | `.env`退避、Agent停止、PR確認 |
| tmuxで画面が崩れる | TERM、rendering | `infocmp tmux-256color`、Inline、再接続 |
| sessionが残ってAgentが終了 | windowでexit code表示 | 再接続後commandを手動で再起動 |
| 起動時に同じsession名が衝突 | tmux内のowner情報 | 別のsessionを改名、無条件killしない |
| browserログイン失敗 | WSL browser/keyring | Antigravity公式Auth guide |
| appがport conflict | Docker/host port共有 | worktree別のport、DB、Compose名 |
| PC再起動でtmuxが消えた | OS/WSL停止したか | Git差分とAgent resumeから再開 |

doctorは存在・versionのローカル診断だけを行う。
GitHub/Agentのログイン済み判定、プラン判定、Docker daemon健全性、全依存関係の保証はしない。
不明な認証tokenや環境変数を出力して調べない。
