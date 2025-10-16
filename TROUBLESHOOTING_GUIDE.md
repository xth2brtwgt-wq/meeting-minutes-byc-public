# Meeting Minutes BYC - トラブルシューティングガイド

## 概要

このドキュメントは、Meeting Minutes BYCアプリケーションのデプロイメントと運用中に発生する可能性のある問題とその解決方法をまとめています。

## デプロイメント関連の問題

### 1. YAML構文エラー

#### 問題
```
YAMLSyntaxError: All collection items must start at the same column
```

#### 原因
- Docker Composeファイルのインデントが不統一
- スペースとタブの混在
- ネストした構造のインデントエラー

#### 解決方法
```bash
# YAMLファイルの構文チェック
sudo docker compose config

# インデントを統一（スペース2つまたは4つ）
# 例：
services:
  app:
    image: python:3.11
    ports:
      - "5000:5000"
```

### 2. Dockerfile構文エラー

#### 問題
```
failed to solve: dockerfile parse error on line 19: FROM requires either one or three arguments
```

#### 原因
- Dockerfileの構文エラー
- 不正なCOPYコマンドの使用
- サポートされていない構文の使用

#### 解決方法
```dockerfile
# 正しい構文例
FROM python:3.11-slim

WORKDIR /app

# ファイルをコピー
COPY requirements.txt .
COPY app.py .
COPY utils/ ./utils/

# 依存関係をインストール
RUN pip install -r requirements.txt

# ポートを公開
EXPOSE 5000

# アプリケーションを起動
CMD ["python", "app.py"]
```

### 3. ファイル転送エラー

#### 問題
```
scp: dest open "/home/AdminUser/meeting-minutes-byc/docker-compose.yml": No such file or directory
```

#### 原因
- リモートディレクトリが存在しない
- 権限不足
- パスの指定ミス

#### 解決方法
```bash
# 1. リモートディレクトリを作成
ssh AdminUser@192.168.68.110 'mkdir -p /home/AdminUser/meeting-minutes-byc'

# 2. 権限を確認
ssh AdminUser@192.168.68.110 'ls -la /home/AdminUser/'

# 3. ファイルを直接作成（scpの代替）
ssh AdminUser@192.168.68.110 'cat > /home/AdminUser/meeting-minutes-byc/docker-compose.yml << "EOF"
# YAML content here
EOF'
```

### 4. 権限エラー

#### 問題
```
mkdir: cannot create directory '/var/services': Permission denied
```

#### 原因
- 不正なディレクトリへのアクセス試行
- 権限不足
- 存在しないパスの使用

#### 解決方法
```bash
# 正しいディレクトリを使用
mkdir -p /home/AdminUser/meeting-minutes-byc

# 権限を確認
ls -la /home/AdminUser/

# 必要に応じて権限を変更
chmod 755 /home/AdminUser/meeting-minutes-byc
```

## コンテナ関連の問題

### 5. コンテナ起動エラー

#### 問題
```
Container meeting-minutes-byc-app exited with code 1
```

#### 原因
- アプリケーションの起動エラー
- 依存関係の不足
- 環境変数の設定ミス

#### 解決方法
```bash
# 1. ログを確認
sudo docker compose logs

# 2. コンテナ内でデバッグ
sudo docker exec -it meeting-minutes-byc-app bash

# 3. 環境変数を確認
sudo docker exec -it meeting-minutes-byc-app env

# 4. アプリケーションファイルを確認
sudo docker exec -it meeting-minutes-byc-app ls -la /app/
```

### 6. ポート接続エラー

#### 問題
```
curl: (7) Failed to connect to 192.168.68.110 port 5002 after 0 ms: Couldn't connect to server
```

#### 原因
- コンテナが起動していない
- ポートマッピングの設定ミス
- ファイアウォールの設定

#### 解決方法
```bash
# 1. コンテナの状態を確認
sudo docker ps -a

# 2. ポートマッピングを確認
sudo docker port meeting-minutes-byc-app

# 3. コンテナ内からテスト
sudo docker exec -it meeting-minutes-byc-app curl localhost:5000/health

# 4. ネットワーク設定を確認
sudo netstat -tlnp | grep 5002
```

### 7. ボリュームマウントエラー

#### 問題
```
Error response from daemon: invalid mount config for type "bind"
```

#### 原因
- マウント先ディレクトリが存在しない
- 権限不足
- パスの指定ミス

#### 解決方法
```bash
# 1. マウント先ディレクトリを作成
sudo mkdir -p /volume1/data/meeting-minutes-byc/uploads
sudo mkdir -p /volume1/data/meeting-minutes-byc/transcripts

# 2. 権限を設定
sudo chown -R AdminUser:admin /volume1/data/meeting-minutes-byc/

# 3. Docker Composeを再起動
sudo docker compose down
sudo docker compose up -d
```

## アプリケーション関連の問題

### 8. API キーエラー

#### 問題
```
文字起こしに失敗しました: 400 API key not valid. Please pass a valid API key.
```

#### 原因
- API キーが設定されていない
- 無効なAPI キー
- 環境変数の設定ミス

#### 解決方法
```bash
# 1. .envファイルを確認
cat .env

# 2. 環境変数を確認
sudo docker exec -it meeting-minutes-byc-app env | grep GEMINI

# 3. 正しいAPI キーを設定
echo "GEMINI_API_KEY=your_valid_api_key" >> .env

# 4. コンテナを再起動
sudo docker compose down
sudo docker compose up -d
```

### 9. メール送信エラー

#### 問題
```
メール送信に失敗しました: Authentication failed
```

#### 原因
- Gmailのアプリパスワードが設定されていない
- 2段階認証が有効になっていない
- SMTP設定のミス

#### 解決方法
```bash
# 1. Gmailのアプリパスワードを生成
# - Gmail設定 > セキュリティ > 2段階認証 > アプリパスワード

# 2. .envファイルに設定
echo "EMAIL_PASSWORD=your_app_password" >> .env

# 3. コンテナを再起動
sudo docker compose down
sudo docker compose up -d
```

### 10. Notion連携エラー

#### 問題
```
Notionページ作成に失敗しました: Invalid database ID
```

#### 原因
- Notion API キーが無効
- データベースIDが間違っている
- 権限不足

#### 解決方法
```bash
# 1. Notion API キーを確認
# - https://www.notion.so/my-integrations

# 2. データベースIDを確認
# - NotionデータベースのURLから取得

# 3. .envファイルに設定
echo "NOTION_API_KEY=your_notion_token" >> .env
echo "NOTION_DATABASE_ID=your_database_id" >> .env

# 4. コンテナを再起動
sudo docker compose down
sudo docker compose up -d
```

## パフォーマンス関連の問題

### 11. メモリ不足

#### 問題
```
Container killed due to memory limit
```

#### 原因
- コンテナのメモリ制限が低い
- アプリケーションのメモリ使用量が多い
- システムリソースの不足

#### 解決方法
```yaml
# docker-compose.ymlにメモリ制限を追加
services:
  meeting-minutes-byc:
    # ... other settings
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

### 12. ディスク容量不足

#### 問題
```
No space left on device
```

#### 原因
- ディスク容量の不足
- ログファイルの蓄積
- 不要なDockerイメージの蓄積

#### 解決方法
```bash
# 1. ディスク使用量を確認
df -h

# 2. 不要なDockerリソースを削除
sudo docker system prune -a

# 3. ログファイルを削除
sudo find /var/log -name "*.log" -mtime +7 -delete

# 4. 古いファイルを削除
sudo find /volume1/data/meeting-minutes-byc/ -name "*.mp3" -mtime +30 -delete
```

## ネットワーク関連の問題

### 13. DNS解決エラー

#### 問題
```
Failed to resolve hostname
```

#### 原因
- DNS設定の問題
- ネットワーク接続の問題
- ファイアウォールの設定

#### 解決方法
```bash
# 1. DNS設定を確認
cat /etc/resolv.conf

# 2. ネットワーク接続をテスト
ping google.com

# 3. ファイアウォール設定を確認
sudo ufw status
```

### 14. プロキシ設定

#### 問題
```
Connection timeout
```

#### 原因
- プロキシサーバーの設定
- 企業ネットワークの制限

#### 解決方法
```bash
# 1. プロキシ設定を確認
echo $HTTP_PROXY
echo $HTTPS_PROXY

# 2. Docker Composeにプロキシ設定を追加
services:
  meeting-minutes-byc:
    environment:
      - HTTP_PROXY=http://proxy.company.com:8080
      - HTTPS_PROXY=http://proxy.company.com:8080
```

## ログ分析

### 15. ログの確認方法

#### アプリケーションログ
```bash
# リアルタイムログ
sudo docker compose logs -f

# 特定の行数のログ
sudo docker compose logs --tail=100

# 特定の時間のログ
sudo docker compose logs --since="2025-10-14T10:00:00"
```

#### システムログ
```bash
# システムログ
sudo journalctl -u docker

# カーネルログ
sudo dmesg | tail -50
```

### 16. ログレベルの設定

#### アプリケーションログレベル
```python
# app.pyでログレベルを設定
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 緊急時の対応

### 17. サービス停止時の対応

#### 緊急停止
```bash
# 全コンテナを停止
sudo docker compose down

# 特定のコンテナを停止
sudo docker stop meeting-minutes-byc-app
```

#### 緊急再起動
```bash
# コンテナを再起動
sudo docker compose restart

# システム全体を再起動
sudo reboot
```

### 18. データ復旧

#### バックアップからの復旧
```bash
# バックアップファイルを展開
tar -xzf meeting-minutes-backup-20251014.tar.gz

# データを復元
sudo cp -r meeting-minutes-byc/ /volume1/data/
```

## 予防策

### 19. 定期的なメンテナンス

#### 週次メンテナンス
```bash
# ログのローテーション
sudo docker system prune -f

# ディスク使用量の確認
df -h

# コンテナの状態確認
sudo docker ps -a
```

#### 月次メンテナンス
```bash
# 完全なクリーンアップ
sudo docker system prune -a

# バックアップの作成
tar -czf meeting-minutes-backup-$(date +%Y%m%d).tar.gz /volume1/data/meeting-minutes-byc/

# セキュリティアップデート
sudo apt update && sudo apt upgrade -y
```

### 20. 監視設定

#### ヘルスチェックの自動化
```bash
# ヘルスチェックスクリプト
#!/bin/bash
if ! curl -f http://192.168.68.110:5002/health; then
    echo "Service is down, restarting..."
    sudo docker compose restart
fi
```

#### ログ監視
```bash
# エラーログの監視
sudo docker compose logs | grep -i error | tail -10
```

---

**最終更新**: 2025年10月14日  
**バージョン**: 1.0  
**作成者**: AI Assistant  
**プロジェクト**: Meeting Minutes BYC

