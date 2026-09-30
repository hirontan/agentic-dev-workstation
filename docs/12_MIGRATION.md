# 12 — Migration and resume

## 新PC

このリポジトリをcloneし、Windows → WSL → base bootstrap → runtime profilesの順に適用する。
GitHub/Agent/AWSへ本人が再ログインし、[受入手順](15_ACCEPTANCE.md)を実行する。
credential cacheをzipへ入れて移動しない。

## 開発ソース

Gitにcommit/pushできる作業を保存する。未追跡の必要ファイルはprivate backupへ分ける。
worktreeをWindows側へ丸ごとコピーして再利用しない。branchを取得してworktreeを再作成する。
DB/volume等のローカル状態はprojectのbackup/restore手順を使う。

WSL全体のexportは任意で、停止とbackup容量を確認して手動実行する。

```powershell
wsl --export Ubuntu-24.04 D:\Backups\ubuntu-24.04.tar
```

このbackupには資格情報や会社データが含まれ得る。暗号化と保存先の権限を確認する。

## 再起動後の復帰

1. WSLを起動し、`git worktree list`を確認する。
2. 作業worktreeの`git status`とIssue受入条件を確認する。
3. `workstation session --issue <number> --agent agy`を実行する。
4. Agentの公式resume機能を使うか、保存した進捗から再開を指示する。
5. 未完了testを再実行する。

launcherは会話IDを管理しない。会話resumeとtmux process restoreは別機能。

## 更新

本リポジトリの変更はdiffとCHANGELOGを確認して取り込む。
bootstrapは内容の違う既存設定を上書きしないため、conflict表示後に手動統合する。
apt/Agent/IDEの更新は別操作。変更後はversionと確認日をprivate inventoryへ残す。
