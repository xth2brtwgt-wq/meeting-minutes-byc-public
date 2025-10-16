# Insta360自動同期システム

Insta360カメラで撮影したファイルをMacからNASへ自動転送するシステムです。

## 概要

- **目的**: Mac上のInsta360ファイルをNASへ自動バックアップ
- **実行タイミング**: 毎日深夜0時（JST）
- **通知**: 転送完了をメールで通知
- **対応ファイル**: `VID_*.mp4`, `*.insv`, `*.insp`, `*.jpg`, `*.dng`, `*.raw`
- **ファイル削除**: Mac側で毎週日曜日午前2時に30日以上前のファイルを自動削除

## 主な機能

✅ **自動バックアップ**: NAS側で毎日深夜0時に自動実行
✅ **元ファイル保持**: Mac側のファイルは即座に削除せず保持
✅ **自動削除**: Mac側で週1回、古いファイルを自動削除（30日以上前）
✅ **メール通知**: 同期結果をメールで通知
✅ **SMBマウント**: Mac共有フォルダを自動マウント
✅ **Docker化**: コンテナで実行、管理が簡単

## システム構成

```
insta360-auto-sync/
├── config/                 # 設定ファイル
│   ├── app.json           # アプリケーション設定
│   └── email.json         # メール設定
├── logs/                  # ログファイル
├── scripts/               # 実行スクリプト（NAS側）
│   ├── sync.py           # メイン同期スクリプト
│   ├── run_scheduler.py  # スケジューラー
│   ├── mount_mac.sh      # Macマウントスクリプト
│   ├── test_connection.py # 接続テストスクリプト
│   └── setup_cron.sh     # cron設定スクリプト
├── mac-scripts/           # Mac側スクリプト
│   └── cleanup_old_files.sh # 古いファイル削除スクリプト
├── utils/                 # ユーティリティ
│   ├── email_sender.py   # メール送信
│   ├── file_utils.py     # ファイル操作
│   └── config_utils.py   # 設定管理
├── docs/                  # ドキュメント
│   ├── setup.md          # セットアップ手順
│   └── operation.md      # 運用手順
├── docker-compose.yml     # Docker設定
├── Dockerfile            # Dockerイメージ定義
├── requirements.txt      # Python依存関係
└── .env                  # 環境変数設定（Git管理外）
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

### 環境変数（.env）

```bash
# Mac接続設定
MAC_IP=192.168.68.88            # MacのIPアドレス
MAC_USERNAME=Admin              # Mac共有ユーザー名
MAC_PASSWORD=****               # Mac共有パスワード
MAC_SHARE=Insta360              # 共有フォルダ名

# 同期設定
SYNC_SCHEDULE=0 0 * * *         # 毎日深夜0時
SOURCE_PATH=/source             # コンテナ内のマウントパス
DESTINATION_PATH=/volume2/data/insta360  # NAS上の保存先

# メール設定
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=****             # Googleアプリパスワード
EMAIL_FROM=your-email@gmail.com
TO_EMAIL=your-email@gmail.com
```

### アプリケーション設定（config/app.json）

```json
{
  "sync": {
    "delete_source": false,      # ソースファイル削除: false（保持）
    "file_patterns": [           # 対象ファイルパターン
      "VID_*.mp4",
      "*.insv",
      "*.insp",
      "*.jpg",
      "*.dng",
      "*.raw"
    ]
  },
  "notification": {
    "send_success": true,        # 成功時にメール送信
    "send_error": true,          # エラー時にメール送信
    "send_no_files": false       # ファイルなし時は送信しない
  }
}
```

## 運用フロー

### 自動実行スケジュール

| タイミング | 処理 | 実行場所 |
|---|---|---|
| 毎日 00:00 | Insta360ファイルをMac→NASにバックアップ | NAS |
| 毎週日曜 02:00 | 30日以上前のファイルを削除 | Mac |

### 確認コマンド

**NAS側**
```bash
# コンテナの状態を確認
docker compose ps

# ログを確認
docker compose logs insta360-auto-sync | tail -50

# 次回実行予定を確認
docker compose logs insta360-auto-sync | grep "次回実行予定"
```

**Mac側**
```bash
# crontabの設定を確認
crontab -l

# 削除ログを確認
tail -f /Users/Yoshi/nas-project/insta360-auto-sync/logs/cleanup.log
```

## トラブルシューティング

### ログの確認

```bash
# NAS側: Dockerログを確認
docker compose logs insta360-auto-sync

# NAS側: エラーログのみ確認
docker compose logs insta360-auto-sync | grep ERROR

# Mac側: 削除ログを確認
cat /Users/Yoshi/nas-project/insta360-auto-sync/logs/cleanup.log
```

### よくある問題

**問題1: マウントエラー**
```bash
# Mac側でSMB共有が有効か確認
sudo sharing -l | grep Insta360

# NAS側でマウントを確認
mount | grep mac-share
```

**問題2: メール送信エラー**
- Googleアプリパスワードが正しいか確認
- `.env`ファイルの`EMAIL_PASSWORD`を確認

**問題3: ファイルが転送されない**
- Mac側のファイルパスを確認: `/Users/Yoshi/Movies/Insta360/Download/`
- ファイルパターンが一致しているか確認

## ライセンス

このプロジェクトは社内利用目的で作成されています。
