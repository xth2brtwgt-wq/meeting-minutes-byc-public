#!/bin/bash
"""
UGreen DXP2800でのDocker権限修正スクリプト
"""

echo "🔧 Docker権限を修正中..."

# AdminUserをdockerグループに追加
sudo usermod -aG docker AdminUser

# Dockerサービスを再起動
sudo systemctl restart docker

# 権限を確認
echo "✅ 権限修正完了"
echo "📋 確認方法:"
echo "1. SSH接続を一度切断"
echo "2. 再接続後、以下のコマンドで確認:"
echo "   docker ps"
echo "   docker network ls"
echo "   docker volume ls"

echo ""
echo "⚠️ 注意: SSH接続を一度切断して再接続してください"

