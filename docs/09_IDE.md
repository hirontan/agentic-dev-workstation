# 09 — IDE

## 確実なWSL接続の参照構成

Windows版VS Code + Microsoft WSL extensionで、Linux側repositoryへ接続する。
公式のRemote WSL手順を[SOURCES](../SOURCES.md)に記載する。
WSLのworktreeから`code .`で開き、status barとterminalの`uname -s`がLinuxであることを確認する。
この構成ではAntigravity CLIをtmuxから動かせる。

## Antigravity IDEを使う場合

希望するWindows版Antigravity IDEで以下を確認する。

1. WSL folderをremote workspaceとして開けるか。
2. Agent terminalがWSL内で動くか。Windows shellでLinux pathを操作していないか。
3. Python/Node/Ruby/formatterがWSLのruntimeを参照するか。
4. worktreeの`.git`を認識し、正しいbranch/diffを表示するか。
5. localhostのappへ接続し、debugできるか。

CLI版とIDE版、standaloneとextensionの機能を同一視しない。
この配布物ではAntigravity IDEのWSL互換性や特定extension IDを実機確認していない。
先行会話の「standalone WSLは未対応」「特定versionが最新」等を固定の事実として採用しない。
導入時の公式互換性と実機結果を確認して採用する。

使える場合はAntigravity IDEをレビューUIにする。安定しない場合はWSL接続を確認できるIDEを使い、
Agent実行はWSLのtmux + CLIを継続する。WSLgや非公式bridgeはv0.1標準に含めない。
