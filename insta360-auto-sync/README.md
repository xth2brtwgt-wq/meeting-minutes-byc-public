# Insta360自動同期システム

Insta360カメラで撮影したファイルをMacからNASへ自動転送するシステムです。

## 概要

- **目的**: Mac上のInsta360ファイルをNASへ自動転送
- **実行タイミング**: 毎日深夜0時（JST）
- **通知**: 転送完了をメールで通知
- **対応ファイル**: `.mp4`, `.insv`, `.insp`, `.jpg`, `.dng`, `.raw`

## システム構成

```
insta360-auto-sync/
├── config/                 # 設定ファイル
│   ├── app.json           # アプリケーション設定
│   ├── sync.json          # 同期設定
│   └── email.json         # メール設定
├── logs/                  # ログファイル
├── scripts/               # 実行スクリプト
│   ├── sync.py           # メイン同期スクリプト
│   ├── mount_mac.sh      # Macマウントスクリプト
│   └── test_connection.sh # 接続テストスクリプト
├── utils/                 # ユーティリティ
│   ├── email_sender.py   # メール送信
│   ├── file_utils.py     # ファイル操作
│   └── config_utils.py   # 設定管理
├── docs/                  # ドキュメント
│   ├── setup.md          # セットアップ手順
│   └── operation.md      # 運用手順
├── docker-compose.yml     # Docker設定
├── Dockerfile            # Dockerイメージ定義
└── requirements.txt      # Python依存関係
```

## 要件

- **Mac**: macOS 10.14以降、SMB共有有効
- **NAS**: UGREEN DXP2800、Docker対応
- **ネットワーク**: 同一ローカルネットワーク

## セットアップ

詳細なセットアップ手順は [docs/setup.md](docs/setup.md) を参照してください。

## 運用

日常の運用方法は [docs/operation.md](docs/operation.md) を参照してください。

## 設定

主要な設定項目：

- **Mac接続情報**: IPアドレス、ユーザー名、パスワード
- **転送先**: NAS上の保存先ディレクトリ
- **メール通知**: SMTP設定、送信先アドレス
- **実行スケジュール**: cron設定

## トラブルシューティング

問題が発生した場合は、ログファイルを確認してください：

```bash
# 最新のログを確認
tail -f logs/insta360_sync.log

# エラーログのみを確認
grep ERROR logs/insta360_sync.log
```

## ライセンス

このプロジェクトは社内利用目的で作成されています。
