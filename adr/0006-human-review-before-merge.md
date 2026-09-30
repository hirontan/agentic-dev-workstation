# ADR-0006 — PRと人間レビューを統合条件にする

- Status: Accepted
- Date: 2026-09-30

## Context

Agent完了宣言のみでは受入条件や安全性の確認が足りない。

## Decision

main直接変更を避け、CIと人間review後にmergeする。

## Consequences

review負荷が発生する。GitHubのbranch protectionを別途設定する。

## Alternatives

Agent自動merge、mainへ直接commit。

## Revisit

実機運用で前提が変わった時は後続ADRで置換する。過去の判断を黙って書き換えない。
