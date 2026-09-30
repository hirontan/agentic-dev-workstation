# ADR-0004 — Issueごとにworktreeを割り当てる

- Status: Accepted
- Date: 2026-09-30

## Context

複数Agentが同じcheckoutを編集すると差分とbranchが混ざる。

## Decision

Issueごとにbranch/worktreeを作り、同一worktreeへ複数writerを置かない。

## Consequences

ファイルを分離できる。Git refs、credential、port、DBは共有される。

## Alternatives

同じcheckout、repo丸ごとclone、containerだけで分離。

## Revisit

実機運用で前提が変わった時は後続ADRで置換する。過去の判断を黙って書き換えない。
