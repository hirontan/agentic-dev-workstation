# 02 — Windows host

## 初回導入

Windows 11、仮想化が有効なPC、WSLを導入できる管理者権限が前提。
会社管理PCでは組織の端末管理ルールに従う。

```powershell
.\bootstrap\windows\setup.ps1
.\bootstrap\windows\setup.ps1 -Apply
```

初回はWSLのインストールにより再起動を要求されることがある。
再起動後Ubuntuを初回起動し、Linux用ユーザー名とパスワードを作る。

```powershell
wsl --status
wsl --version
wsl -l -v
wsl -d Ubuntu-24.04
```

WSL1の場合は作業を保存してから`wsl --set-version Ubuntu-24.04 2`を手動実行する。
bootstrapは既存distributionのversion変換やデフォルトdistribution変更を自動で行わない。

## 手動で用意するUI

Windows Terminal、使用するIDE、必要ならDocker Desktopを公式配布元から導入する。
VS Codeを使う場合はWindows版とMicrosoftのWSL extensionを用意する。
Antigravity IDEは[IDE手順](09_IDE.md)の実機検証を通して採用する。

## Resource limits

最初はWindows/WSLの既定値から始め、並列Agentとtest実行時のメモリを観測する。
必要ならWSL Settingsで調整する。手動設定例は[config](../config/windows/wslconfig.example)。
memory/processor値は全PCで固定せず、Windows側にもRAMを残す。
設定変更後に必要な`wsl --shutdown`は全WSLのプロセスを停止するため、作業を保存してから行う。

## Power settings

長時間実行にはAC電源・スリープ設定を確認する。tmuxがあってもスリープ中は計算が継続しない。
画面ロックとスリープは別。Windows updateの再起動にも備えて小さくcommitする。
