# ADR-0001 — Windows + WSL2を標準にする

- Status: Accepted
- Date: 2026-09-30

## Context

既存Windows PCを活用しLinux系開発ツールを動かしたい。

## Decision

Windowsをhost、WSL2 Ubuntuをexecution環境とする。

## Consequences

Linux native toolingを使える。Windows電源管理とWSL停止の影響を受ける。

## Alternatives

Omarchy専用PC、Linux dual boot、Windows native実行。

## Revisit

実機運用で前提が変わった時は後続ADRで置換する。過去の判断を黙って書き換えない。
