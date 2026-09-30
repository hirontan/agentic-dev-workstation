# ADR-0007 — AGENTSと運用の正本をAgentから独立させる

- Status: Accepted
- Date: 2026-09-30

## Context

Agent製品の変更で環境全体を作り直したくない。

## Decision

AGENTS.mdとGit運用を正本とし、Agent固有settingsとauthは別管理する。

## Consequences

Agentを交換しやすい。rule読込とCLI互換性は製品ごとに検証する。

## Alternatives

Antigravity専用dotfilesへ統合、製品ごとに異なる運用。

## Revisit

実機運用で前提が変わった時は後続ADRで置換する。過去の判断を黙って書き換えない。
