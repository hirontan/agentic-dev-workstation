# ADR-0008 — 非破壊bootstrapと明示apply

- Status: Accepted
- Date: 2026-09-30

## Context

既存PCへの導入で設定上書きや予期しないcloud costを避けたい。

## Decision

既定はplan、異なる既存設定は保護し、Agent導入とloginは手動にする。

## Consequences

既存環境を守れる。conflictの手動統合と初回loginが必要。

## Alternatives

curl pipeから全設定を強制上書き、無人cloud provisioning。

## Revisit

実機運用で前提が変わった時は後続ADRで置換する。過去の判断を黙って書き換えない。
