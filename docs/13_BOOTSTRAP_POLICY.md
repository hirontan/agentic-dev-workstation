# 13 — Bootstrap policy

## 二段階

既定はplanのみ。Windowsは`-Apply`、WSLは`--apply`で変更する。
OS導入・再起動・Linuxユーザー作成・認証を一つの無人commandに隠さず、境界ごとに手順を残す。
初回Windows導入からAgentログインまでは人間の操作が必要。

## Windows

WSL default versionを2へ設定し、指定distributionが未導入の場合だけinstallする。
既存WSLのversion変換、distribution削除、shutdown、IDE導入、課金契約を行わない。
失敗時はnative commandのexit codeを確認して停止する。

## WSL

1. Ubuntu 24.04を確認し、apply時は通常ユーザーであることを確認する。
2. sudoでapt cacheとbase packagesを更新する。
3. `~/src`、`~/worktrees`、`~/.local/bin`等を作成する。
4. templateと内容が一致する既存設定は維持し、異なる場合はconflictとして維持する。
5. shell source行を重複なく追加し、workstationのsymlinkを作る。
6. package inventoryをprivate stateへ保存する。

既存symlinkが違う宛先の場合も上書きしない。
一部conflictがあれば終了code 2。導入済みpackagesや作成済みdirectoryは残る。
dry-runはapt、file作成、state更新を実行しない。

## 再実行

同じ入力で既存設定を重複追加しない。ただしapt packageは利用repoの現行versionへ更新され得る。
完全なversion固定やtransactional rollbackはv0.1では提供しない。
異常終了後は原因を直し再実行する。設定の勝手なrollbackやOSpackage削除はしない。

## Rollback

作成されたsymlinkと設定ファイルを確認して手動で取り除き、`.bashrc`のsource行を削除する。
導入済みOSpackagesを無条件にremoveしない。他projectが使用している可能性がある。
既存設定に手でmergeする前は、自分でbackupを作る。
