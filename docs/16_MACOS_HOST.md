# 16 — macOS host

## 初回導入

macOS（Apple Silicon / Intel）、Homebrewが動作する環境が前提。
会社管理PCでは組織の端末管理ルールに従う。

1. **前提ツールの確認**:
   Xcode Command Line ToolsとHomebrewが未導入の場合は先に導入する。

   ```bash
   xcode-select --install
   # Homebrewが未導入の場合: https://brew.sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Bootstrapの実行**:

   ```bash
   bash bootstrap/macos/setup.sh
   bash bootstrap/macos/setup.sh --apply
   ```

   既定はplan（dry-run）です。`--apply`を指定した時のみHomebrewパッケージの導入と設定の安全コピーが行われます。

3. **シェルの反映と確認**:

   ```bash
   # Zshの場合
   source ~/.zshrc
   # Bashの場合
   source ~/.bashrc  # または source ~/.bash_profile

   workstation doctor
   ```

## シェルとPATH

macOSの標準シェルはZshです。
bootstrapは`~/.config/agentic-dev-workstation/workstation.zsh`（Bash向けには`workstation.bash`）を配置し、`~/.local/bin`へのPATH追加行を`~/.zshrc`（または`~/.bashrc` / `~/.bash_profile`）へ安全に追加します。
既存の設定ファイルは削除・上書きされず、内容が一致しない場合は`CONFLICT`として保護されます。

## Gitと認証

Git identityとGitHub CLI認証は本人が設定します。

```bash
git config --global user.name 'YOUR_NAME'
git config --global user.email 'YOUR_EMAIL'
gh auth login
```

macOSではOS標準のキーチェーン（Keychain Access）との統合が標準的に利用できます。

## Agentの導入

Antigravity（`agy`）等のCoding Agentは、macOSネイティブ版の公式インストーラから導入します。
WSLや仮想マシンを介さず直接動作するため、ターミナルからそのまま起動・認証できます。

## IDE連携

VS CodeやAntigravity IDEは、macOSネイティブ版を使用します。
WSL2のようなリモート拡張機能（Remote - WSL）は不要であり、作成されたworktree（`~/worktrees/<repository>-<id>/issue-<num>`）をローカルディレクトリとして直接開くことができます。

## Power settings（省電力とスリープ）

- MacBookのクラムシェル（蓋閉じ）やシステムスリープに入ると、tmuxセッション内であってもAgentの処理やテストは一時停止します。
- 長時間のAgent実行時は、AC電源を接続し、システム設定の省電力設定を確認するか、`caffeinate`コマンドの活用を検討してください。
- 画面ロックとスリープは異なります。突然のOS再起動やスリープに備え、作業はIssue単位で小さくcommitします。
