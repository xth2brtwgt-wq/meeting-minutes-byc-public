# UGreen DXP2800 最適化セットアップガイド

## 🎯 最適な配置場所

### 分析結果
- **volume1**: 1.1T (1%使用) - アプリケーション用
- **volume2**: 4.4T (13%使用) - 大容量データ用
- **既存Docker環境**: `/volume1/docker/services/` に複数サービス配置済み

### 推奨配置

#### メインプロジェクト
```
/volume1/docker/services/nas-project/
├── meeting-minutes/
│   ├── app/
│   ├── templates/
│   ├── config/
│   └── data/ (シンボリックリンク)
├── common/
├── docker/
└── docs/
```

#### データ保存（大容量）
```
/volume2/data/nas-project/audio-transcription/
├── uploads/      # 音声ファイル
├── transcripts/  # 文字起こし結果
├── logs/         # ログファイル
└── backups/      # バックアップ
```

## 🚀 セットアップ手順

### Step 1: ディレクトリの作成

```bash
# SSH接続
ssh AdminUser@192.168.68.110

# ディレクトリセットアップスクリプトを実行
cd /volume1/docker/services/
sudo mkdir -p nas-project
sudo chown -R AdminUser:AdminUser nas-project

# データ保存ディレクトリの作成
sudo mkdir -p /volume2/data/nas-project/audio-transcription/{uploads,transcripts,logs,backups}
sudo chown -R AdminUser:AdminUser /volume2/data/nas-project
sudo chmod -R 755 /volume2/data/nas-project
```

### Step 2: プロジェクトファイルのアップロード

```bash
# ローカルからNASにアップロード
rsync -avz --progress /Users/Yoshi/nas-project/ AdminUser@192.168.68.110:/volume1/docker/services/nas-project/
```

### Step 3: Docker権限の修正

```bash
# SSH接続後
sudo usermod -aG docker AdminUser
sudo systemctl restart docker

# SSH接続を一度切断して再接続
exit
ssh AdminUser@192.168.68.110

# 権限確認
docker ps
```

### Step 4: Portainerでのスタック作成

1. **Portainer管理画面にアクセス**
   - URL: http://192.168.68.110:9000
   - ユーザー: adminuser
   - パスワード: Tsuj!19700308

2. **スタックの作成**
   - "Stacks" → "Add stack" をクリック
   - スタック名: `audio-transcription`
   - Web editor を選択

3. **スタック定義の入力**
   `docker/compose/portainer-stack.yml` の内容をコピー&ペースト

4. **デプロイ**
   - "Deploy the stack" をクリック

## 📊 設定の特徴

### 最適化された構成
- **アプリケーション**: volume1 (高速アクセス)
- **データ**: volume2 (大容量ストレージ)
- **既存環境との統合**: `/volume1/docker/services/` パターンに準拠

### ボリュームマウント
```yaml
volumes:
  - /volume2/data/nas-project/audio-transcription/uploads:/tmp/uploads
  - /volume2/data/nas-project/audio-transcription/transcripts:/tmp/transcripts
  - /volume1/docker/services/nas-project/meeting-minutes/config:/app/meeting-minutes/config
  - /volume2/data/nas-project/audio-transcription/logs:/app/logs
```

### 環境変数
```yaml
environment:
  - FLASK_ENV=production
  - PYTHONUNBUFFERED=1
  - PYTHONPATH=/app
  - UPLOAD_DIR=/tmp/uploads
  - TRANSCRIPT_DIR=/tmp/transcripts
  - WHISPER_MODEL=base
  - WHISPER_LANGUAGE=ja
```

## 🔍 アクセス方法

- **Webアプリケーション**: http://192.168.68.110:5000
- **Portainer管理画面**: http://192.168.68.110:9000

## 🔄 メンテナンス

### データバックアップ
```bash
cd /volume1/docker/services/nas-project
python common/scripts/backup_data.py --action create --backup-name meeting_data
```

### ログ確認
```bash
# コンテナログ
docker logs audio-transcription-app

# アプリケーションログ
tail -f /volume2/data/nas-project/audio-transcription/logs/app.log
```

### ディスク使用量確認
```bash
# プロジェクト全体の使用量
du -sh /volume1/docker/services/nas-project
du -sh /volume2/data/nas-project

# 詳細な使用量
du -sh /volume2/data/nas-project/audio-transcription/*
```

## 🚨 トラブルシューティング

### よくある問題

1. **権限エラー**
   ```bash
   sudo chown -R AdminUser:AdminUser /volume1/docker/services/nas-project
   sudo chown -R AdminUser:AdminUser /volume2/data/nas-project
   ```

2. **ポート競合**
   - 5000番ポートが使用中の場合、`portainer-stack.yml`でポート番号を変更

3. **ディスク容量不足**
   - volume2の使用量を確認: `df -h /volume2`
   - 古いファイルを削除: `find /volume2/data/nas-project -type f -mtime +30 -delete`

### ログ確認
```bash
# Portainerでのログ確認
# Portainer管理画面 → Containers → audio-transcription-app → Logs

# システムログ
journalctl -u docker -f
```

## 📞 サポート

問題が発生した場合は、以下の情報と一緒にお知らせください：

1. エラーメッセージの詳細
2. ディスク使用量: `df -h`
3. コンテナの状態: `docker ps`
4. ログの内容

