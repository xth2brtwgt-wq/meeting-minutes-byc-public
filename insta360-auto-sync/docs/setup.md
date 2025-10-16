# Insta360自動同期システム - セットアップ手順書

## 概要

このドキュメントでは、Insta360自動同期システムのセットアップ手順を説明します。

## 前提条件

### ハードウェア要件

- **Mac**: macOS 10.14以降、固定IPアドレス推奨
- **NAS**: UGREEN DXP2800、Docker対応
- **ネットワーク**: 同一ローカルネットワーク内

### ソフトウェア要件

- **Mac側**: SMB共有機能が有効
- **NAS側**: UGOS Pro 1.x以降、Docker 20.x以降

## セットアップ手順

### 1. Mac側の準備

#### 1.1 SMB共有の有効化

1. **システム環境設定**を開く
2. **共有**を選択
3. **ファイル共有**にチェックを入れる
4. **オプション**をクリック
5. **SMBを使用してファイルやフォルダを共有**にチェック
6. 共有するユーザーを選択し、**読み取りと書き込み**を設定

#### 1.2 共有フォルダの設定

1. **共有フォルダ**に`/Users/Yoshi/Movies/Insta360`を追加
2. アクセス権限を**読み取りと書き込み**に設定
3. **完了**をクリック

#### 1.3 ネットワーク設定の確認

```bash
# IPアドレスを確認
ifconfig | grep "inet "

# SMB共有の確認
smbutil status
```

### 2. NAS側の準備

#### 2.1 Dockerの有効化

1. UGOS Proの管理画面にログイン
2. **アプリケーション** → **Docker**を選択
3. Dockerを有効化

#### 2.2 ディレクトリの作成

```bash
# 転送先ディレクトリを作成
mkdir -p /volume2/data/insta360

# ログディレクトリを作成
mkdir -p /home/AdminUser/insta360-auto-sync/logs
```

### 3. システムのデプロイ

#### 3.1 ファイルの配置

```bash
# プロジェクトディレクトリに移動
cd /home/AdminUser/nas-project/insta360-auto-sync

# 設定ファイルを作成
cp env.example .env
```

#### 3.2 環境変数の設定

`.env`ファイルを編集して以下の値を設定：

```bash
# Mac接続設定
MAC_IP=192.168.68.69          # MacのIPアドレス
MAC_USERNAME=Yoshi            # Macのユーザー名
MAC_PASSWORD=your_password    # Macのパスワード
MAC_SHARE=Yoshi              # Macの共有名

# メール設定
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
TO_EMAIL=admin@example.com

# 同期設定
SYNC_SCHEDULE=0 0 * * *       # 毎日0時実行
```

#### 3.3 設定ファイルの作成

```bash
# 設定ディレクトリを作成
mkdir -p config

# アプリケーション設定を作成
cat > config/app.json << EOF
{
  "app": {
    "name": "Insta360自動同期システム",
    "version": "1.0.0",
    "timezone": "Asia/Tokyo"
  },
  "sync": {
    "source_path": "/source",
    "destination_path": "/volume2/data/insta360",
    "file_patterns": [
      "VID_*.mp4",
      "*.insv",
      "*.insp",
      "*.jpg",
      "*.dng",
      "*.raw"
    ],
    "schedule": "0 0 * * *"
  },
  "mac": {
    "ip_address": "192.168.68.69",
    "username": "Yoshi",
    "password": "",
    "share_name": "Yoshi"
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/insta360_sync.log",
    "max_days": 30
  }
}
EOF

# メール設定を作成
cat > config/email.json << EOF
{
  "smtp": {
    "server": "smtp.gmail.com",
    "port": 587,
    "user": "",
    "password": "",
    "from": ""
  },
  "notification": {
    "to_email": "",
    "send_success": true,
    "send_error": true,
    "send_no_files": false
  }
}
EOF
```

### 4. Dockerコンテナの起動

#### 4.1 コンテナのビルドと起動

```bash
# Docker Composeでコンテナを起動
docker-compose up -d --build

# コンテナの状態を確認
docker-compose ps
```

#### 4.2 ログの確認

```bash
# コンテナのログを確認
docker-compose logs -f insta360-auto-sync

# ログファイルを確認
tail -f logs/insta360_sync.log
```

### 5. 動作確認

#### 5.1 接続テスト

```bash
# 接続テストを実行
docker-compose exec insta360-auto-sync python3 /app/scripts/test_connection.py
```

#### 5.2 手動実行テスト

```bash
# 手動で同期を実行
docker-compose exec insta360-auto-sync python3 /app/scripts/sync.py --test
```

#### 5.3 メール通知テスト

```bash
# メール接続テスト
docker-compose exec insta360-auto-sync python3 -c "
from utils.email_sender import EmailSender
sender = EmailSender()
print('メール接続テスト:', sender.test_connection())
"
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. Mac接続エラー

**症状**: `Mac共有フォルダのマウントに失敗しました`

**解決方法**:
- Mac側のSMB共有が有効か確認
- IPアドレスとユーザー名・パスワードが正しいか確認
- ファイアウォール設定を確認

#### 2. メール送信エラー

**症状**: `メール送信に失敗しました`

**解決方法**:
- Gmailアプリパスワードが正しく設定されているか確認
- 2段階認証が有効になっているか確認
- SMTP設定が正しいか確認

#### 3. ファイル転送エラー

**症状**: `ファイルコピー失敗`

**解決方法**:
- NAS側のディスク容量を確認
- ファイルのアクセス権限を確認
- ネットワーク接続を確認

### ログの確認方法

```bash
# 最新のログを確認
tail -f logs/insta360_sync.log

# エラーログのみを確認
grep ERROR logs/insta360_sync.log

# 特定の日付のログを確認
grep "2025-01-15" logs/insta360_sync.log
```

## セキュリティ設定

### 1. パスワードの管理

- `.env`ファイルのパーミッションを600に設定
- 定期的にパスワードを変更
- アプリパスワードを使用（Gmail）

### 2. ネットワークセキュリティ

- 内部ネットワークのみからのアクセス
- 不要なポートの開放を避ける
- 定期的なセキュリティアップデート

## バックアップ設定

### 1. 設定ファイルのバックアップ

```bash
# 設定ファイルをバックアップ
tar -czf insta360-config-backup-$(date +%Y%m%d).tar.gz config/ .env
```

### 2. ログファイルのバックアップ

```bash
# ログファイルをバックアップ
tar -czf insta360-logs-backup-$(date +%Y%m%d).tar.gz logs/
```

## 完了確認

セットアップが完了したら、以下を確認してください：

- [ ] Mac側のSMB共有が有効
- [ ] NAS側のDockerが動作中
- [ ] 環境変数が正しく設定
- [ ] 接続テストが成功
- [ ] メール通知が正常に送信
- [ ] 手動実行テストが成功

すべての項目が完了したら、システムは本格運用の準備が整いました。
