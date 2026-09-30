# ADR-0003 — tmuxで実行セッションを管理する

- Status: Accepted
- Date: 2026-09-30

## Context

複数Agentとtest/serverを端末windowから切り離して管理したい。

## Decision

repository単位のsessionとIssue単位のwindowを使う。

## Consequences

detach/attachできる。OS停止とスリープを越える計算継続は保証しない。

## Alternatives

Terminal windowだけ、IDE内terminalだけ、system service化。

## Revisit

実機運用で前提が変わった時は後続ADRで置換する。過去の判断を黙って書き換えない。
