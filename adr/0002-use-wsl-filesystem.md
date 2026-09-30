# ADR-0002 — ソースをWSL filesystemへ置く

- Status: Accepted
- Date: 2026-09-30

## Context

LinuxツールからWindows mountへ大量I/Oすると性能とpathの問題が生じる。

## Decision

repositoryとworktreeは~/srcと~/worktrees配下へ置く。

## Consequences

Linux側I/Oを一貫させる。WindowsからはWSL対応接続を使う。

## Alternatives

/mnt/c上で開発、同期フォルダ内で開発。

## Revisit

実機運用で前提が変わった時は後続ADRで置換する。過去の判断を黙って書き換えない。
