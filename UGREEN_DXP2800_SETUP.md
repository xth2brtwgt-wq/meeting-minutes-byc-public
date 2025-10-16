# UGreen DXP2800 最適化セットアップガイド

## 🎯 最適な配置場所

### 分析結果
- **volume1**: 1.1T (1%使用) - アプリケーション用
- **volume2**: 4.4T (13%使用) - 大容量データ用
- **既存Docker環境**: `/volume1/docker/services/` に複数サービス配置済み

### 推奨配置

#### メインプロジェクト
```
/home/AdminUser/meeting-minutes-byc/
├── meeting-minutes-byc/  # メインアプリケーション
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── config/
├── docker/
└── docs/
```

#### データ保存（大容量）
```
/volume2/data/meeting-minutes-byc/
├── uploads/      # 音声ファイル
├── transcripts/  # 文字起こし結果
├── logs/         # ログファイル
└── backups/      # バックアップ
```

## 🚀 セットアップ手順

### Step 1: プロジェクトファイルの転送

```bash
# ローカルからNASにプロジェクトファイルを転送
cd /Users/Yoshi
tar -czf nas-project.tar.gz nas-project/
scp nas-project.tar.gz AdminUser@192.168.68.110:/home/AdminUser/

# NASにSSH接続
ssh AdminUser@192.168.68.110

# プロジェクトファイルを展開
cd /home/AdminUser
tar -xzf nas-project.tar.gz
mv nas-project meeting-minutes-byc
```

### Step 2: Docker Compose設定ファイルの作成

```bash
# NASにSSH接続
ssh AdminUser@192.168.68.110

# プロダクション用のdocker-compose.ymlを作成
cd /home/AdminUser/meeting-minutes-byc/meeting-minutes-byc
cat > docker-compose-production.yml << 'EOF'
version: '3.8'

services:
  meeting-minutes-byc:
    build: .
    container_name: meeting-minutes-byc-app
    ports:
      - "5000:5000"
    volumes:
      # データ保存パス（/volume2/data/meeting-minutes-byc配下）
      - /volume2/data/meeting-minutes-byc/uploads:/app/uploads
      - /volume2/data/meeting-minutes-byc/transcripts:/app/transcripts
      - /volume2/data/meeting-minutes-byc/logs:/app/logs
    environment:
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
      - UPLOAD_DIR=/app/uploads
      - TRANSCRIPT_DIR=/app/transcripts
      - WHISPER_MODEL=base
      - WHISPER_LANGUAGE=ja
    restart: unless-stopped
    networks:
      - bridge
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

networks:
  bridge:
    driver: bridge
EOF
```

### Step 3: デプロイの実行

```bash
# 管理者権限でDocker Composeを実行
sudo docker compose -f docker-compose-production.yml up -d --build

# コンテナの状態確認
docker ps | grep meeting-minutes-byc

# アプリケーションの動作確認
curl -f http://localhost:5000/health
```

### Step 4: アクセス確認

1. **アプリケーションにアクセス**
   - URL: http://192.168.68.110:5000
   - ヘルスチェック: http://192.168.68.110:5000/health

2. **データ保存場所の確認**
   ```bash
   # データディレクトリの確認
   ls -la /volume2/data/meeting-minutes-byc/
   
   # 音声ファイルアップロードテスト後
   ls -la /volume2/data/meeting-minutes-byc/uploads/
   ls -la /volume2/data/meeting-minutes-byc/transcripts/
   ```

## 📋 システム構成

### 最終的な構成
- **アプリケーション**: `meeting-minutes-byc-app` コンテナ
- **ポート**: 5000
- **データ保存**: `/volume2/data/meeting-minutes-byc/`
- **プロジェクト場所**: `/home/AdminUser/meeting-minutes-byc/`

### データ保存場所
```
/volume2/data/meeting-minutes-byc/
├── uploads/      # 音声ファイル
├── transcripts/  # 文字起こし結果・議事録
├── logs/         # ログファイル
└── backups/      # バックアップ
```

## 🔧 管理コマンド

### コンテナの管理
```bash
# コンテナの状態確認
docker ps | grep meeting-minutes-byc

# コンテナの停止
sudo docker stop meeting-minutes-byc-app

# コンテナの再起動
sudo docker restart meeting-minutes-byc-app

# ログの確認
docker logs meeting-minutes-byc-app

# コンテナの削除（再デプロイ時）
sudo docker compose -f /home/AdminUser/meeting-minutes-byc/meeting-minutes-byc/docker-compose-production.yml down
```

### データの管理
```bash
# データディレクトリの使用量確認
du -sh /volume2/data/meeting-minutes-byc/*

# 古いファイルの削除（30日以上前）
find /volume2/data/meeting-minutes-byc -type f -mtime +30 -delete
```
## 📊 設定の特徴

### 最適化された構成
- **アプリケーション**: `/home/AdminUser/meeting-minutes-byc/` (ユーザーディレクトリ)
- **データ**: `/volume2/data/meeting-minutes-byc/` (大容量ストレージ)
- **デプロイ方法**: Docker Compose (コマンドライン)

### ボリュームマウント
```yaml
volumes:
  - /volume2/data/meeting-minutes-byc/uploads:/app/uploads
  - /volume2/data/meeting-minutes-byc/transcripts:/app/transcripts
  - /volume2/data/meeting-minutes-byc/logs:/app/logs
```

### 環境変数
```yaml
environment:
  - FLASK_ENV=production
  - PYTHONUNBUFFERED=1
  - UPLOAD_DIR=/app/uploads
  - TRANSCRIPT_DIR=/app/transcripts
  - WHISPER_MODEL=base
  - WHISPER_LANGUAGE=ja
```

## 🔍 アクセス方法

- **Webアプリケーション**: http://192.168.68.110:5000
- **ヘルスチェック**: http://192.168.68.110:5000/health

## 🔄 メンテナンス

### データバックアップ
```bash
# データのバックアップ
tar -czf meeting-minutes-backup-$(date +%Y%m%d).tar.gz /volume2/data/meeting-minutes-byc/
```

### ログ確認
```bash
# コンテナログ
docker logs meeting-minutes-byc-app

# アプリケーションログ
tail -f /volume2/data/meeting-minutes-byc/logs/app.log
```

### ディスク使用量確認
```bash
# プロジェクト全体の使用量
du -sh /home/AdminUser/meeting-minutes-byc
du -sh /volume2/data/meeting-minutes-byc

# 詳細な使用量
du -sh /volume2/data/meeting-minutes-byc/*
```

## 🚨 トラブルシューティング

### よくある問題

1. **権限エラー**
   ```bash
   sudo chown -R AdminUser:admin /home/AdminUser/meeting-minutes-byc
   sudo chown -R AdminUser:admin /volume2/data/meeting-minutes-byc
   ```

2. **ポート競合**
   - 5000番ポートが使用中の場合、`docker-compose-production.yml`でポート番号を変更

3. **ディスク容量不足**
   - volume2の使用量を確認: `df -h /volume2`
   - 古いファイルを削除: `find /volume2/data/meeting-minutes-byc -type f -mtime +30 -delete`

### ログ確認
```bash
# コンテナの状態確認
docker ps | grep meeting-minutes-byc

# コンテナログの確認
docker logs meeting-minutes-byc-app

# システムログ
journalctl -u docker -f
```

## 📞 サポート

問題が発生した場合は、以下の情報と一緒にお知らせください：

1. エラーメッセージの詳細
2. ディスク使用量: `df -h`
3. コンテナの状態: `docker ps`
4. ログの内容

