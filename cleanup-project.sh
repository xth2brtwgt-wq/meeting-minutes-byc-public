#!/bin/bash

# Meeting Minutes BYC プロジェクトクリーンアップスクリプト
# 不要なプロトタイプファイルと試行錯誤ファイルを整理

echo "=== Meeting Minutes BYC プロジェクトクリーンアップ ==="
echo ""

# バックアップディレクトリを作成
BACKUP_DIR="backup-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📁 バックアップディレクトリを作成: $BACKUP_DIR"
echo ""

# 1. 不要なPortainerスタックファイルをバックアップ
echo "🗂️  不要なPortainerスタックファイルをバックアップ..."
mv portainer-stack-*.yml "$BACKUP_DIR/" 2>/dev/null || true
echo "   - portainer-stack-*.yml ファイルを移動"

# 2. 不要なDockerfileをバックアップ
echo "🐳 不要なDockerfileをバックアップ..."
mv Dockerfile.meeting-minutes-* "$BACKUP_DIR/" 2>/dev/null || true
echo "   - Dockerfile.meeting-minutes-* ファイルを移動"

# 3. 不要なdocker-composeファイルをバックアップ
echo "📦 不要なdocker-composeファイルをバックアップ..."
mv docker-compose-meeting-minutes-* "$BACKUP_DIR/" 2>/dev/null || true
echo "   - docker-compose-meeting-minutes-* ファイルを移動"

# 4. 不要なrequirementsファイルをバックアップ
echo "📋 不要なrequirementsファイルをバックアップ..."
mv requirements-meeting-minutes-* "$BACKUP_DIR/" 2>/dev/null || true
echo "   - requirements-meeting-minutes-* ファイルを移動"

# 5. 古いmeeting-minutes-bycディレクトリをバックアップ（簡易版）
echo "📂 古いmeeting-minutes-bycディレクトリをバックアップ..."
if [ -d "meeting-minutes-byc" ]; then
    mv meeting-minutes-byc "$BACKUP_DIR/"
    echo "   - meeting-minutes-byc/ ディレクトリを移動"
fi

# 6. 不要なスクリプトファイルをバックアップ
echo "🔧 不要なスクリプトファイルをバックアップ..."
mv setup-nas-env.sh "$BACKUP_DIR/" 2>/dev/null || true
echo "   - setup-nas-env.sh を移動"

# 7. 空のディレクトリを削除
echo "🗑️  空のディレクトリを削除..."
find . -type d -empty -delete 2>/dev/null || true
echo "   - 空のディレクトリを削除"

# 8. Pythonキャッシュファイルを削除
echo "🐍 Pythonキャッシュファイルを削除..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
echo "   - __pycache__ ディレクトリと .pyc ファイルを削除"

# 9. 現在のプロジェクト構造を表示
echo ""
echo "📊 クリーンアップ後のプロジェクト構造:"
echo ""

# 主要なファイルとディレクトリのみ表示
echo "📁 主要ディレクトリ:"
ls -la | grep "^d" | grep -E "(meeting-minutes-byc|common|docker|docs|scripts)" | awk '{print "   " $9}'

echo ""
echo "📄 主要ファイル:"
ls -la | grep "^-" | grep -E "\.(md|sh|yml|txt)$" | awk '{print "   " $9}'

echo ""
echo "📋 ドキュメントファイル:"
ls -la *.md 2>/dev/null | awk '{print "   " $9}'

echo ""
echo "✅ クリーンアップ完了!"
echo ""
echo "📦 バックアップされたファイル:"
echo "   - バックアップディレクトリ: $BACKUP_DIR"
echo "   - 必要に応じて復元可能です"
echo ""
echo "🎯 現在のプロジェクト構成:"
echo "   - meeting-minutes-byc/ (メインアプリケーション)"
echo "   - 各種ドキュメント (*.md)"
echo "   - common/ (共通ユーティリティ)"
echo "   - docker/ (Docker設定)"
echo ""
echo "💡 次のステップ:"
echo "   1. 必要に応じてバックアップファイルを確認"
echo "   2. プロジェクトの動作確認"
echo "   3. 不要なバックアップディレクトリの削除"

