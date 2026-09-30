# 00 — 全体像

## Goal

新しいWindows PCでも開発環境を再構築し、Issue単位で複数のCoding Agentを動かす。
特定のアプリケーションに依存せず、作業環境と運用方法を一つのリポジトリへ残す。

## 管理するもの

| 正本 | 管理先 |
|---|---|
| 環境と運用の意思決定 | 本リポジトリのdocsとADR |
| アプリの設計・ソース・テスト | 各アプリのリポジトリ |
| 作業の目的と受入条件 | GitHub Issue |
| 変更・レビュー・統合 | branchとPR |
| 認証情報 | OS keyring / 管理されたcredential store |
| 個別PCの実測状態 | private inventory |

初期の並列数は2 Agent程度から始める。利用枠、CPU、RAM、test時間を観測して増やす。
tmuxのwindow数だけでは実行中Agent数や料金は分からないため、人間が状態を確認する。

## 成立条件

bootstrapを再実行しても既存設定を破壊しない。Agentを入れ替えてもworktreeとPR運用を維持する。
Issueには観測可能な受入条件を記載し、Agentの完了宣言だけで完了扱いにしない。

## 非対象

IDE自体の開発、業務アプリのコード、production接続、取引実行、クラウドAgent基盤の構築は含めない。
この環境はローカルのCoding Agent運用を対象とする。
