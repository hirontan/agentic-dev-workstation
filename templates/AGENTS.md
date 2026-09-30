# Project agent instructions

このテンプレートをproject用に編集する。PLACEHOLDERを残したまま実装を開始しない。

## Read first

- README.md
- projectのarchitectureとADR（パスを記入）
- 対象Issueと受入条件

## Working policy

- Issueごとのbranch/worktreeを使う。mainへ直接commitしない。
- 対象範囲以外のrefactor、依存更新、schema変更を行わない。
- local servicesとテスト用データを使う。productionへ接続しない。
- worktree別のport、Compose project名、DB名を指定する。
- secret、実顧客データ、auth cacheをcommitしない。
- AGENTS.mdだけでsandboxや権限制限が成立するとは考えない。
- 破壊的command、force push、deploy、自動mergeは行わない。
- public interface変更時は対応する受入テストとdocsを更新する。

## Architecture boundaries

PLACEHOLDER: UI/BFF/domain/infraの責務、変更禁止領域を記載する。
PLACEHOLDER: database migration方式と互換性要件を記載する。

## Validation commands

PLACEHOLDER: install / lint / typecheck / unit test / integration test / buildの正確なcommandを記載する。
利用できないserviceや必要credentialがあれば事前に説明する。
プロジェクトに存在しないcommandを推測して実行しない。

## Completion report

変更内容、Issue受入条件への対応、実行したcheckと結果、未検証、migration影響を報告する。
PR下書きはprojectで許可された場合に作成し、mergeは人間に任せる。
