#!/bin/bash
"""
Portainer環境でのデプロイスクリプト
UGreen DXP2800 + Portainer対応
"""

set -e

# 設定変数（UGreen DXP2800環境）
NAS_IP="192.168.68.110"
PORTAINER_URL="http://${NAS_IP}:9000"
PORTAINER_USER="adminuser"
PORTAINER_PASS="Tsuj!19700308"
STACK_NAME="audio-transcription"
PROJECT_PATH="/volume1/docker/services/nas-project"

echo "🚀 Portainer環境でのデプロイを開始します..."

# 1. Portainerの認証トークンを取得
echo "📡 Portainerに接続中..."
AUTH_RESPONSE=$(curl -s -X POST "${PORTAINER_URL}/api/auth" \
  -H "Content-Type: application/json" \
  -d "{\"Username\":\"${PORTAINER_USER}\",\"Password\":\"${PORTAINER_PASS}\"}")

if [ $? -ne 0 ]; then
    echo "❌ Portainerへの接続に失敗しました"
    exit 1
fi

TOKEN=$(echo $AUTH_RESPONSE | jq -r '.jwt')
if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
    echo "❌ 認証に失敗しました。ユーザー名・パスワードを確認してください"
    exit 1
fi

echo "✅ Portainer認証成功"

# 2. 既存のスタックを削除（存在する場合）
echo "🗑️ 既存のスタックを確認中..."
EXISTING_STACK=$(curl -s -H "Authorization: Bearer ${TOKEN}" \
  "${PORTAINER_URL}/api/stacks" | jq -r ".[] | select(.Name==\"${STACK_NAME}\") | .Id")

if [ ! -z "$EXISTING_STACK" ] && [ "$EXISTING_STACK" != "null" ]; then
    echo "📦 既存のスタックを削除中..."
    curl -s -X DELETE -H "Authorization: Bearer ${TOKEN}" \
      "${PORTAINER_URL}/api/stacks/${EXISTING_STACK}"
    echo "✅ 既存のスタックを削除しました"
fi

# 3. Dockerイメージをビルド
echo "🔨 Dockerイメージをビルド中..."
cd "$(dirname "$0")/../.."
docker build -f docker/Dockerfile -t audio-transcription:latest .

# 4. イメージをNASに転送
echo "📤 イメージをNASに転送中..."
docker save audio-transcription:latest | ssh AdminUser@${NAS_IP} "docker load"

# 5. Portainerスタックを作成
echo "📦 Portainerスタックを作成中..."
STACK_CONFIG=$(cat docker/compose/portainer-stack.yml | base64 -w 0)

curl -s -X POST -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  "${PORTAINER_URL}/api/stacks" \
  -d "{
    \"Name\": \"${STACK_NAME}\",
    \"StackFileContent\": \"$(cat docker/compose/portainer-stack.yml)\",
    \"Env\": []
  }"

if [ $? -eq 0 ]; then
    echo "✅ Portainerスタックの作成が完了しました"
    echo "🌐 Webアプリケーション: http://${NAS_IP}:5000"
    echo "📊 Portainer管理画面: ${PORTAINER_URL}"
else
    echo "❌ スタックの作成に失敗しました"
    exit 1
fi

echo "🎉 デプロイが完了しました！"
