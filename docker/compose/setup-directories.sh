#!/bin/bash
"""
UGreen DXP2800用ディレクトリセットアップスクリプト
既存のDocker環境に合わせた最適な配置
"""

set -e

echo "🔧 UGreen DXP2800用ディレクトリをセットアップ中..."

# 1. メインプロジェクトディレクトリの作成
echo "📁 メインプロジェクトディレクトリを作成中..."
sudo mkdir -p /volume1/docker/services/nas-project
sudo chown -R AdminUser:AdminUser /volume1/docker/services/nas-project

# 2. データ保存ディレクトリの作成（大容量データ用）
echo "💾 データ保存ディレクトリを作成中..."
sudo mkdir -p /volume2/data/meeting-minutes-byc/{uploads,transcripts,logs,backups}
sudo chown -R AdminUser:AdminUser /volume2/data/meeting-minutes-byc

# 3. 権限設定
echo "🔐 権限を設定中..."
sudo chmod -R 755 /volume1/docker/services/nas-project
sudo chmod -R 755 /volume2/data/meeting-minutes-byc

# 4. 既存のmeeting-minutesディレクトリの確認
echo "🔍 既存のmeeting-minutesディレクトリを確認中..."
if [ -d "/volume1/docker/services/meeting-minutes" ]; then
    echo "⚠️  既存のmeeting-minutesディレクトリが見つかりました"
    echo "   既存のデータをバックアップしますか？ (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "📦 既存データをバックアップ中..."
        sudo cp -r /volume1/docker/services/meeting-minutes /volume1/docker/services/meeting-minutes.backup.$(date +%Y%m%d_%H%M%S)
        echo "✅ バックアップ完了"
    fi
fi

# 5. ディレクトリ構造の確認
echo "📊 作成されたディレクトリ構造:"
echo ""
echo "メインプロジェクト:"
tree /volume1/docker/services/nas-project 2>/dev/null || ls -la /volume1/docker/services/nas-project
echo ""
echo "データ保存:"
tree /volume2/data/meeting-minutes-byc 2>/dev/null || ls -la /volume2/data/meeting-minutes-byc

echo ""
echo "✅ ディレクトリセットアップが完了しました！"
echo ""
echo "📋 次のステップ:"
echo "1. プロジェクトファイルをアップロード:"
echo "   rsync -avz --progress /path/to/nas-project/ AdminUser@192.168.68.110:/volume1/docker/services/nas-project/"
echo ""
echo "2. Portainerでスタックをデプロイ"
echo "3. Webアプリケーションにアクセス: http://192.168.68.110:5000"

