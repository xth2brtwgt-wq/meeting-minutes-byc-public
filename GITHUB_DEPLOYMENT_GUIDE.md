# GitHub + NAS デプロイガイド

## 🚀 概要

このガイドでは、GitHubリポジトリを使用してNAS環境にMeeting Minutes BYCアプリケーションをデプロイする方法を説明します。

## 📋 前提条件

- GitHubアカウント
- NAS環境（Ugreen NAS）
- SSH接続可能な環境
- Docker & Docker Compose

## 🔧 初期セットアップ

### 1. ローカル環境でのGitHubリポジトリ作成

```bash
# プロジェクトディレクトリでGitを初期化
cd /Users/Yoshi/nas-project
git init

# .gitignoreファイルを作成
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
.env

# Docker
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# 一時ファイル
*.tmp
*.temp

# バックアップファイル
backup-*
EOF

# ファイルをステージング
git add .

# 初回コミット
git commit -m "Initial commit: Meeting Minutes BYC project with NAS deployment"
```

### 2. GitHubリポジトリの作成

1. GitHub.comにアクセス
2. **New repository**をクリック
3. リポジトリ設定：
   - Repository name: `meeting-minutes-byc`
   - Description: `Meeting Minutes BYC - 音声議事録生成システム`
   - Public/Private: お好みで
   - **重要**: README、.gitignore、ライセンスは追加しない

### 3. リモートリポジトリの追加とプッシュ

```bash
# リモートリポジトリを追加
git remote add origin https://github.com/yourusername/meeting-minutes-byc.git

# メインブランチに設定
git branch -M main

# GitHubにプッシュ
git push -u origin main
```

## 🏗️ NAS環境でのセットアップ

### 1. NAS環境でのGitインストール

```bash
# NASに接続
ssh your_username@your_nas_ip

# Gitをインストール（Ubuntuベースの場合）
sudo apt update
sudo apt install git -y

# インストール確認
git --version
```

### 2. GitHubからプロジェクトをクローン

```bash
# 既存のプロジェクトをバックアップ
cd /home/your_username
mv meeting-minutes-byc-dev meeting-minutes-byc-dev-backup

# GitHubからクローン
git clone https://github.com/yourusername/meeting-minutes-byc.git meeting-minutes-byc-dev

# プロジェクトディレクトリに移動
cd meeting-minutes-byc-dev/meeting-minutes-byc-dev
```

### 3. 環境変数ファイルの設定

```bash
# 環境変数ファイルを作成
cp env.example .env

# .envファイルを編集（APIキーを設定）
nano .env
```

### 4. 初回デプロイ

```bash
# Docker Composeでデプロイ
sudo docker compose -f docker-compose.dev.yml down
sudo docker compose -f docker-compose.dev.yml build --no-cache
sudo docker compose -f docker-compose.dev.yml up -d

# ヘルスチェック
sleep 15
curl -f http://localhost:5000/health
```

## 🔄 日常的なデプロイ手順

### 手動デプロイ

```bash
# NAS環境で実行
cd /home/your_username/meeting-minutes-byc-dev/meeting-minutes-byc-dev

# 最新のコードを取得
git pull origin main

# コンテナを再起動
sudo docker compose -f docker-compose.dev.yml down
sudo docker compose -f docker-compose.dev.yml up -d

# ヘルスチェック
curl -f http://localhost:5000/health
```

### デプロイスクリプトの使用

```bash
# デプロイスクリプトを作成
cat > ../deploy.sh << 'EOF'
#!/bin/bash

echo "🚀 Starting deployment..."

# 最新のコードを取得
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# コンテナを停止
echo "🛑 Stopping containers..."
sudo docker compose -f docker-compose.dev.yml down

# 新しいイメージをビルド
echo "🔨 Building new image..."
sudo docker compose -f docker-compose.dev.yml build --no-cache

# コンテナを起動
echo "🚀 Starting containers..."
sudo docker compose -f docker-compose.dev.yml up -d

# ヘルスチェック
echo "🔍 Checking application health..."
sleep 15
if curl -f http://localhost:5000/health; then
    echo "✅ Deployment completed successfully!"
    echo "🌐 Application is running at: http://your_nas_ip:5000"
else
    echo "❌ Health check failed!"
    echo "📋 Checking logs..."
    sudo docker compose -f docker-compose.dev.yml logs --tail=20
    exit 1
fi
EOF

# 実行可能にする
chmod +x ../deploy.sh

# デプロイ実行
../deploy.sh
```

## 🤖 GitHub Actions自動デプロイ（オプション）

### 1. SSH鍵の設定

```bash
# ローカルでSSH鍵を生成（まだない場合）
ssh-keygen -t rsa -b 4096 -C "github-actions"

# 公開鍵をNASに追加
ssh-copy-id -i ~/.ssh/id_rsa.pub your_username@your_nas_ip
```

### 2. GitHub Secretsの設定

GitHubリポジトリで以下を設定：

1. **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** で以下を追加：
- `NAS_HOST`: `your_nas_ip_address`
- `NAS_USER`: `your_nas_username`
   - `NAS_SSH_KEY`: SSH秘密鍵の内容

### 3. ワークフローファイル

`.github/workflows/deploy.yml`が自動実行されます：

```yaml
name: Deploy to NAS

on:
  push:
    branches: [ main ]
  workflow_dispatch:  # 手動実行も可能

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Deploy to NAS
      uses: appleboy/ssh-action@v1.0.3
      with:
        host: ${{ secrets.NAS_HOST }}
        username: ${{ secrets.NAS_USER }}
        key: ${{ secrets.NAS_SSH_KEY }}
        script: |
          cd /home/your_username/meeting-minutes-byc-dev/meeting-minutes-byc-dev
          git pull origin main
          sudo docker compose -f docker-compose.dev.yml down
          sudo docker compose -f docker-compose.dev.yml build --no-cache
          sudo docker compose -f docker-compose.dev.yml up -d
          sleep 15
          curl -f http://localhost:5000/health || exit 1
          echo "✅ Deployment completed successfully!"
```

## 🔍 トラブルシューティング

### 認証エラー

```bash
# Personal Access Tokenが必要
git pull origin main
# Username: あなたのGitHubユーザー名
# Password: Personal Access Token
```

詳細は `GITHUB_AUTHENTICATION_GUIDE.md` を参照。

### ポートの競合

```bash
# ポート5000が使用中か確認
sudo netstat -tlnp | grep 5000

# 既存のコンテナを停止
sudo docker stop $(sudo docker ps -q --filter "publish=5000")
```

### コンテナの状態確認

```bash
# コンテナの状態確認
sudo docker compose -f docker-compose.dev.yml ps

# ログの確認
sudo docker compose -f docker-compose.dev.yml logs --tail=20

# コンテナ内での確認
sudo docker exec -it meeting-minutes-byc-dev bash
```

### ファイル権限の問題

```bash
# ファイルの権限を確認
ls -la

# 必要に応じて権限を変更
sudo chown -R your_username:admin .
sudo chmod -R 755 .
```

## 📊 デプロイの確認

### ヘルスチェック

```bash
# ローカルヘルスチェック
curl -f http://localhost:5000/health

# 外部アクセス確認
curl http://your_nas_ip:5000/health
```

### ブラウザアクセス

```
http://your_nas_ip:5000
```

## 🎯 ベストプラクティス

### 開発フロー

1. **ローカルで開発・テスト**
2. **GitHubにプッシュ**
3. **NAS環境でデプロイ**
4. **動作確認**

### セキュリティ

- **環境変数**: `.env`ファイルはGitにコミットしない
- **APIキー**: 適切に管理し、定期的に更新
- **SSH鍵**: 強力な鍵を使用し、定期的に更新

### バックアップ

```bash
# 定期的なバックアップ
cp -r /home/your_username/meeting-minutes-byc-dev /home/your_username/backup-$(date +%Y%m%d)
```

## 📚 関連ドキュメント

- `GITHUB_AUTHENTICATION_GUIDE.md` - GitHub認証ガイド
- `DEPLOYMENT_DOCUMENTATION.md` - 詳細な技術ドキュメント
- `TROUBLESHOOTING_GUIDE.md` - トラブルシューティングガイド

---

**最終更新**: 2025年10月15日  
**作成者**: AI Assistant  
**プロジェクト**: Meeting Minutes BYC
