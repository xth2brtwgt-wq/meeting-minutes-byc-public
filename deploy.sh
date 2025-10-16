#!/bin/bash

echo "🚀 Starting deployment..."

# 最新のコードを取得
echo "📥 Pulling latest code from GitHub..."
git pull origin main

# コンテナを停止
echo "🛑 Stopping containers..."
sudo docker compose down

# 新しいイメージをビルド
echo "🔨 Building new image..."
sudo docker compose build --no-cache

# コンテナを起動
echo "🚀 Starting containers..."
sudo docker compose up -d

# ヘルスチェック
echo "🔍 Checking application health..."
sleep 15
if curl -f http://localhost:5002/health; then
    echo "✅ Deployment completed successfully!"
    echo "🌐 Application is running at: http://your_nas_ip:5002"
else
    echo "❌ Health check failed!"
    echo "📋 Checking logs..."
    sudo docker compose logs --tail=20
    exit 1
fi
