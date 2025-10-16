# Insta360自動同期システム - 運用手順書

## 概要

このドキュメントでは、Insta360自動同期システムの日常運用方法を説明します。

## 日常運用

### 自動実行

システムは毎日深夜0時（JST）に自動実行されます。

- **実行タイミング**: 毎日 0:00
- **処理内容**: Insta360ファイルの検索・転送・削除
- **通知**: 処理完了後にメールで通知

### 監視項目

#### 1. ログファイルの確認

```bash
# 最新のログを確認
tail -f /home/AdminUser/insta360-auto-sync/logs/insta360_sync.log

# エラーログのみを確認
grep ERROR /home/AdminUser/insta360-auto-sync/logs/insta360_sync.log

# 今日のログを確認
grep "$(date +%Y-%m-%d)" /home/AdminUser/insta360-auto-sync/logs/insta360_sync.log
```

#### 2. メール通知の確認

- **成功時**: 転送ファイル数と容量が記載された完了メール
- **失敗時**: エラー内容が記載された警告メール
- **ファイルなし時**: 転送対象ファイルがない旨の通知メール

#### 3. ストレージ容量の監視

```bash
# NAS側の容量確認
df -h /volume2/data/insta360

# 転送済みファイルの確認
ls -la /volume2/data/insta360/
```

### 定期メンテナンス

#### 週次メンテナンス（毎週月曜日）

1. **ログファイルの確認**
   ```bash
   # 過去1週間のログを確認
   grep "$(date -d '1 week ago' +%Y-%m-%d)" /home/AdminUser/insta360-auto-sync/logs/insta360_sync.log
   ```

2. **エラーログの確認**
   ```bash
   # 過去1週間のエラーを確認
   grep -A 5 -B 5 ERROR /home/AdminUser/insta360-auto-sync/logs/insta360_sync.log | tail -20
   ```

3. **メール通知の受信確認**
   - 過去1週間の通知メールが正常に受信されているか確認

#### 月次メンテナンス（毎月1日）

1. **ストレージ容量の確認**
   ```bash
   # ディスク使用量を確認
   du -sh /volume2/data/insta360/
   
   # 容量が90%を超えている場合は警告
   df -h /volume2/data/insta360 | awk 'NR==2 {if($5+0 > 90) print "WARNING: Disk usage over 90%"}'
   ```

2. **古いログファイルの削除**
   ```bash
   # 30日以上古いログファイルを削除
   find /home/AdminUser/insta360-auto-sync/logs/ -name "*.log*" -mtime +30 -delete
   ```

3. **設定ファイルのバックアップ**
   ```bash
   # 設定ファイルをバックアップ
   tar -czf /home/AdminUser/insta360-auto-sync/backup/config-backup-$(date +%Y%m%d).tar.gz \
       /home/AdminUser/insta360-auto-sync/config/ \
       /home/AdminUser/insta360-auto-sync/.env
   ```

#### 四半期メンテナンス（3ヶ月ごと）

1. **転送速度テスト**
   ```bash
   # 手動実行で転送速度をテスト
   cd /home/AdminUser/insta360-auto-sync
   docker-compose exec insta360-auto-sync python3 /app/scripts/sync.py --test
   ```

2. **システム全体のレビュー**
   - ログファイルの傾向分析
   - エラー発生パターンの確認
   - 設定の最適化検討

## 手動操作

### 手動実行

#### 1. 同期処理の手動実行

```bash
# 通常の同期処理を実行
cd /home/AdminUser/insta360-auto-sync
docker-compose exec insta360-auto-sync python3 /app/scripts/sync.py

# テストモードで実行（実際の転送は行わない）
docker-compose exec insta360-auto-sync python3 /app/scripts/sync.py --test
```

#### 2. 接続テストの実行

```bash
# 全体的な接続テスト
docker-compose exec insta360-auto-sync python3 /app/scripts/test_connection.py

# メール接続テストのみ
docker-compose exec insta360-auto-sync python3 -c "
from utils.email_sender import EmailSender
sender = EmailSender()
print('メール接続テスト:', sender.test_connection())
"
```

### 設定変更

#### 1. 実行時刻の変更

```bash
# .envファイルを編集
nano /home/AdminUser/insta360-auto-sync/.env

# SYNC_SCHEDULEの値を変更（例: 毎日2時に変更）
SYNC_SCHEDULE=0 2 * * *

# コンテナを再起動
docker-compose restart insta360-auto-sync
```

#### 2. メール設定の変更

```bash
# .envファイルを編集
nano /home/AdminUser/insta360-auto-sync/.env

# メール設定を変更
EMAIL_USER=new_email@gmail.com
EMAIL_PASSWORD=new_app_password
TO_EMAIL=new_admin@example.com

# コンテナを再起動
docker-compose restart insta360-auto-sync
```

#### 3. ファイルパターンの変更

```bash
# 設定ファイルを編集
nano /home/AdminUser/insta360-auto-sync/config/app.json

# file_patternsセクションを編集
"file_patterns": [
  "VID_*.mp4",
  "*.insv",
  "*.insp",
  "*.jpg",
  "*.dng",
  "*.raw",
  "*.mov"  # 新しいパターンを追加
]

# コンテナを再起動
docker-compose restart insta360-auto-sync
```

## 障害対応

### 障害レベル定義

| レベル | 定義 | 対応時間 |
|--------|------|----------|
| Lv.1 | システム停止 | 1時間以内 |
| Lv.2 | 一部機能停止 | 4時間以内 |
| Lv.3 | 性能劣化 | 24時間以内 |

### エスカレーションフロー

```
障害検知
  ↓
ログ確認
  ↓
一次対応（再起動等）
  ↓
解決しない場合
  ↓
詳細調査・原因特定
  ↓
恒久対策実施
```

### よくある障害と対応方法

#### 1. Mac接続エラー

**症状**: `Mac共有フォルダのマウントに失敗しました`

**一次対応**:
```bash
# コンテナを再起動
docker-compose restart insta360-auto-sync

# 接続テストを実行
docker-compose exec insta360-auto-sync python3 /app/scripts/test_connection.py
```

**詳細調査**:
- Mac側のSMB共有状態を確認
- ネットワーク接続を確認
- IPアドレスと認証情報を確認

#### 2. メール送信エラー

**症状**: `メール送信に失敗しました`

**一次対応**:
```bash
# メール接続テストを実行
docker-compose exec insta360-auto-sync python3 -c "
from utils.email_sender import EmailSender
sender = EmailSender()
print('メール接続テスト:', sender.test_connection())
"
```

**詳細調査**:
- Gmailアプリパスワードの有効性を確認
- 2段階認証の設定を確認
- SMTP設定の正確性を確認

#### 3. ファイル転送エラー

**症状**: `ファイルコピー失敗`

**一次対応**:
```bash
# ディスク容量を確認
df -h /volume2/data/insta360

# 手動実行でテスト
docker-compose exec insta360-auto-sync python3 /app/scripts/sync.py --test
```

**詳細調査**:
- NAS側のディスク容量を確認
- ファイルのアクセス権限を確認
- ネットワーク帯域を確認

### 緊急時の対応

#### 1. システム完全停止時

```bash
# コンテナの状態を確認
docker-compose ps

# コンテナを強制停止
docker-compose down

# ログを確認
docker-compose logs insta360-auto-sync

# コンテナを再起動
docker-compose up -d
```

#### 2. データ損失の可能性がある場合

```bash
# 転送先のバックアップを作成
tar -czf /volume2/backup/insta360-emergency-backup-$(date +%Y%m%d_%H%M%S).tar.gz \
    /volume2/data/insta360/

# ログファイルをバックアップ
tar -czf /volume2/backup/insta360-logs-emergency-backup-$(date +%Y%m%d_%H%M%S).tar.gz \
    /home/AdminUser/insta360-auto-sync/logs/
```

## パフォーマンス監視

### 1. 転送速度の監視

```bash
# ログから転送速度を確認
grep "転送完了" /home/AdminUser/insta360-auto-sync/logs/insta360_sync.log | tail -10

# 実行時間を確認
grep "実行時間" /home/AdminUser/insta360-auto-sync/logs/insta360_sync.log | tail -10
```

### 2. リソース使用量の監視

```bash
# コンテナのリソース使用量を確認
docker stats insta360-auto-sync

# ディスクI/Oを確認
iostat -x 1 5
```

### 3. ネットワーク監視

```bash
# ネットワーク接続を確認
netstat -an | grep :445

# 帯域使用量を確認
iftop -i eth0
```

## バックアップとリストア

### 1. 設定のバックアップ

```bash
# 設定ファイルをバックアップ
tar -czf /volume2/backup/insta360-config-$(date +%Y%m%d).tar.gz \
    /home/AdminUser/insta360-auto-sync/config/ \
    /home/AdminUser/insta360-auto-sync/.env \
    /home/AdminUser/insta360-auto-sync/docker-compose.yml
```

### 2. データのバックアップ

```bash
# 転送済みファイルをバックアップ
rsync -av /volume2/data/insta360/ /volume2/backup/insta360-data-$(date +%Y%m%d)/
```

### 3. リストア手順

```bash
# 設定のリストア
tar -xzf /volume2/backup/insta360-config-20250115.tar.gz -C /

# データのリストア
rsync -av /volume2/backup/insta360-data-20250115/ /volume2/data/insta360/

# コンテナを再起動
docker-compose restart insta360-auto-sync
```

## セキュリティ管理

### 1. パスワード管理

- 定期的なパスワード変更（3ヶ月ごと）
- アプリパスワードの有効期限管理
- ログファイルのアクセス権限設定

### 2. アクセス制御

```bash
# 設定ファイルの権限設定
chmod 600 /home/AdminUser/insta360-auto-sync/.env
chmod 600 /home/AdminUser/insta360-auto-sync/config/*.json

# ログファイルの権限設定
chmod 644 /home/AdminUser/insta360-auto-sync/logs/*.log
```

### 3. 監査ログ

```bash
# アクセスログを確認
grep "insta360-auto-sync" /var/log/auth.log

# ファイルアクセスログを確認
auditctl -l | grep insta360
```

## アップグレード手順

### 1. バックアップの作成

```bash
# 現在の設定とデータをバックアップ
tar -czf /volume2/backup/insta360-pre-upgrade-$(date +%Y%m%d).tar.gz \
    /home/AdminUser/insta360-auto-sync/
```

### 2. 新バージョンのデプロイ

```bash
# 新しいコードを取得
cd /home/AdminUser/nas-project/insta360-auto-sync
git pull origin main

# コンテナを再ビルド
docker-compose down
docker-compose up -d --build
```

### 3. 動作確認

```bash
# 接続テストを実行
docker-compose exec insta360-auto-sync python3 /app/scripts/test_connection.py

# 手動実行テスト
docker-compose exec insta360-auto-sync python3 /app/scripts/sync.py --test
```

## 連絡先

### システム管理者

- **担当者**: AdminUser
- **連絡先**: admin@example.com
- **緊急時**: 24時間対応

### 開発者

- **担当者**: Yoshi
- **連絡先**: yoshi@example.com
- **対応時間**: 平日 9:00-18:00
