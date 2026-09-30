# Repository instructions

## このリポジトリの目的

Windows + WSLの開発環境を再構築できるよう、設計書・bootstrap・設定・運用スクリプトを管理する。
READMEとdocsを日本語の正本とし、コード識別子とcommit messageは英語でもよい。

## 作業ルール

- Issueまたは依頼に定義された範囲と受入条件から着手する。
- README、関連docs、ADR、対象スクリプトを読み、既存方針に合わせる。
- mainを直接変更せず作業branch/worktreeを使う。
- bootstrapを利用者のホストへ勝手に適用しない。検証は一時ディレクトリや隔離環境で行う。
- 実在しないCLI引数・IDE拡張ID・設定キー・認証方法を作らない。公式情報と確認日を残す。
- スクリプトでevalや未検証のshell文字列連結を避ける。subprocessには引数配列を渡す。
- 既存設定は削除・上書きしない。新規作成または内容が一致する場合のみ適用する。
- bootstrapはdry-runを既定とし、明示的なapplyの時だけ変更する。
- root権限はOSパッケージ導入に限定する。Agentをrootで実行しない。
- secrets、認証キャッシュ、実Issue本文、会社コードをリポジトリへ保存しない。
- worktreeをsandboxと説明しない。共有Git・port・DB・認証の制約を説明する。
- `git reset --hard`、`git clean -fd`、worktree強制削除、force push、自動mergeを追加しない。
- Node/Ruby等の追加profileは既存bootstrapへ無条件に混ぜずADRと受入条件を作る。

## Verification

```bash
bash tests/check.sh
```

作成・削除スクリプトを変更したら、dirty/未merge/既存path/同名repo/不正Issueを含めて検証する。
tmux起動を変更したら実tmuxテストも実行する。SKIPは成功扱いと区別して報告する。
Windows/WSL/Agentを実行できない場合は未検証と記載し、検証済みとしない。
挙動を変更したらdocs、CLI help、受入テストを同時更新する。

## 完了報告

変更内容、実行した検証、未検証事項、利用者が必要な手順を記載する。
無関係なrefactor、課金サービス追加、外部送信、公開を行わない。
