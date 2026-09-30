# ADR-0009 — macOSホスト環境をサポートする

- Status: Accepted
- Date: 2026-09-30

## Context

開発者の利用が多いmacOS (Darwin) 環境でも、Windows + WSL2と同様の開発ワークフロー（Git worktree分離、tmuxセッション管理、非破壊bootstrap、Coding Agent運用）を実現したい。

## Decision

1. macOSをホストOSとしてサポートし、仮想環境を介さずネイティブ実行する。
2. パッケージマネージャにはHomebrewを採用し、`bootstrap/macos/setup.sh`を提供する。
3. bootstrapはdry-runを既定とし、`--apply`時のみ変更する非破壊ポリシー（ADR-0008）を維持する。
4. `workstation` CLIはPython 3 + Git + tmuxの構成を共通で利用し、`doctor`でmacOSプラットフォームを識別する。
5. macOSの標準シェルであるZshおよびBashの両方に対応し、PATH設定の読み込みを提供する。

## Consequences

- Windows + WSL2環境とmacOS環境で共通の運用手順（`workstation new-worktree`, `workstation session`等）を利用できる。
- macOS環境ではWSL2のようなファイルシステム境界（Windows側とLinux側の境界）がなく、ファイルI/Oがシンプルになる。
- Homebrewは事前に利用者が導入していることを前提とし、bootstrapはroot権限を要求しない（Homebrewのセキュリティ原則に適合）。

## Alternatives

- Windows + WSL2専用のまま維持する（macOS利用者の環境再構築・共通化に対応できない）。
- MacPortsやNixを採用する（HomebrewがmacOS開発環境において最も普及している）。

## Revisit

macOS特有のAgent挙動やOS更新で前提が変わった場合は後続ADRで置換する。
