#!/bin/bash
# Meeting Minutes BYC - NAS環境デプロイスクリプト

set -e

# カラー出力
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Meeting Minutes BYC NAS環境デプロイ ===${NC}"
echo ""

# 現在のディレクトリを確認
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ エラー: app.pyが見つかりません${NC}"
    echo "このスクリプトはmeeting-minutes-bycディレクトリで実行してください"
    exit 1
fi

# 環境変数ファイルの確認
if [ ! -f "env.production" ]; then
    echo -e "${YELLOW}⚠️  env.productionファイルが見つかりません${NC}"
    echo "env.productionファイルを作成して環境変数を設定してください"
    echo "env.exampleを参考にしてください"
    exit 1
fi

# 必要なディレクトリを作成
echo -e "${YELLOW}📁 必要なディレクトリを作成中...${NC}"
mkdir -p /home/AdminUser/meeting-minutes-data/uploads
mkdir -p /home/AdminUser/meeting-minutes-data/transcripts
mkdir -p /home/AdminUser/meeting-minutes-data/templates
mkdir -p /home/AdminUser/meeting-minutes-data/logs

# 権限設定
echo -e "${YELLOW}🔐 ディレクトリ権限を設定中...${NC}"
chmod 755 /home/AdminUser/meeting-minutes-data
chmod 755 /home/AdminUser/meeting-minutes-data/uploads
chmod 755 /home/AdminUser/meeting-minutes-data/transcripts
chmod 755 /home/AdminUser/meeting-minutes-data/templates
chmod 755 /home/AdminUser/meeting-minutes-data/logs

# Dockerネットワークを作成（存在しない場合）
echo -e "${YELLOW}🌐 Dockerネットワークを作成中...${NC}"
docker network create nas-network 2>/dev/null || echo "ネットワークは既に存在します"

# 既存のコンテナを停止・削除
echo -e "${YELLOW}🛑 既存のコンテナを停止中...${NC}"
docker compose down 2>/dev/null || echo "既存のコンテナはありません"

# 環境変数を読み込み
echo -e "${YELLOW}📋 環境変数を読み込み中...${NC}"
export $(grep -v '^#' env.production | xargs)

# イメージをビルド
echo -e "${YELLOW}🔨 Dockerイメージをビルド中...${NC}"
docker compose build --no-cache

# コンテナを起動
echo -e "${YELLOW}🚀 コンテナを起動中...${NC}"
docker compose up -d

# 起動確認
echo -e "${YELLOW}⏳ 起動確認中...${NC}"
sleep 15

if docker ps | grep -q meeting-minutes-byc; then
    echo -e "${GREEN}✅ Meeting Minutes BYCが正常に起動しました${NC}"
    echo ""
    echo -e "${BLUE}📊 アクセス情報:${NC}"
    echo "  URL: http://192.168.68.110:5002"
    echo "  ヘルスチェック: http://192.168.68.110:5002/health"
    echo ""
    echo -e "${BLUE}📁 データディレクトリ:${NC}"
    echo "  アップロード: /home/AdminUser/meeting-minutes-data/uploads"
    echo "  議事録: /home/AdminUser/meeting-minutes-data/transcripts"
    echo "  テンプレート: /home/AdminUser/meeting-minutes-data/templates"
    echo "  ログ: /home/AdminUser/meeting-minutes-data/logs"
    echo ""
    echo -e "${BLUE}🔧 管理コマンド:${NC}"
    echo "  ログ確認: docker logs -f meeting-minutes-byc"
    echo "  停止: docker compose down"
    echo "  再起動: docker compose restart"
    echo "  状態確認: docker ps | grep meeting-minutes-byc"
    echo ""
    echo -e "${BLUE}🛡️  セキュリティ設定:${NC}"
    echo "  環境変数ファイル: env.production"
    echo "  シークレットキー: 必ず変更してください"
    echo "  API キー: 適切に設定してください"
    echo ""
    echo -e "${GREEN}🎉 デプロイが完了しました！${NC}"
    echo ""
    echo -e "${YELLOW}📝 次のステップ:${NC}"
    echo "1. ブラウザで http://192.168.68.110:5002 にアクセス"
    echo "2. テンプレート管理機能をテスト"
    echo "3. 音声ファイルのアップロードをテスト"
    echo "4. メール送信機能をテスト"
else
    echo -e "${RED}❌ コンテナの起動に失敗しました${NC}"
    echo ""
    echo -e "${YELLOW}🔍 トラブルシューティング:${NC}"
    echo "1. ログを確認: docker logs meeting-minutes-byc"
    echo "2. 環境変数を確認: cat env.production"
    echo "3. ポートが使用中でないか確認: netstat -tlnp | grep 5002"
    echo "4. Docker デーモンが起動しているか確認: systemctl status docker"
    exit 1
fi
