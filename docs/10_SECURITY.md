# 10 — Security and cost

## Credentials

SSH secret key、PAT、AWS credentials、Agent auth cache、`.env`をcommitしない。
認証は本人の操作とし、GitHub/AWSは必要最小限の権限と短期credentialsを優先する。
global Git identityを会社/個人で共用しない。repository-local設定を確認する。
.gitignoreは漏洩防止の最終保証ではない。push前に差分を見る。

## Agent permissions

Agentをrootで起動しない。全command自動許可やpermission bypassを既定にしない。
AGENTS.mdは行動指示であり、OSやproviderのアクセス制御ではない。
worktreeはファイルの分離であり、他worktreeやHOMEの読み取りを防ぐsandboxではない。
MCP/ブラウザ/外部connectorの許可は用途ごとに検討する。

## Local-first

DB、queue、storage、serverはprojectが定義するローカル構成を使う。
クラウド本番credentialsをAgentの実行環境へ常駐させない。
Coding Agentの推論通信と本番アプリの通信を区別し、会社データ送信の契約条件を確認する。

## Cost

ログイン後に利用枠、課金方式、上限/停止方法を確認する。
月額プランでも利用枠があり、API key方式は従量課金の可能性がある。
WSLで実行するだけで無料になるとは考えない。
v0.1はAPI key設定、cloud provisioning、常駐scheduler、無限リトライを追加しない。
同時数と作業時間は人間が管理する。launcherには予算の強制停止機能はない。

## Public repository

公開時は汎用設定だけを含め、private host情報、実Issue本文、会社コードを除く。
licenseは初期MIT。公開する前に所有権と適用範囲を確認する。
