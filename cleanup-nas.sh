#!/bin/bash

# NAS環境クリーンアップスクリプト
# 不要になったファイルを整理

NAS_IP="192.168.68.110"
NAS_USER="AdminUser"

echo "=== NAS環境クリーンアップ ==="
echo ""

# SSH接続テスト
echo "🔍 NAS接続テスト..."
if ping -c 1 $NAS_IP > /dev/null 2>&1; then
    echo "✅ NAS接続可能: $NAS_IP"
else
    echo "❌ NAS接続不可: $NAS_IP"
    exit 1
fi

echo ""
echo "📋 NAS環境で確認すべき不要ファイル:"
echo ""

# NAS環境のクリーンアップコマンドを生成
cat << 'EOF'
# NASにSSH接続して以下のコマンドを実行してください:

ssh AdminUser@192.168.68.110

# 1. ホームディレクトリの確認
ls -la /home/AdminUser/

# 2. 不要なプロジェクトディレクトリの確認
ls -la /home/AdminUser/meeting-minutes-*

# 3. 不要なDocker Composeファイルの確認
find /home/AdminUser/ -name "docker-compose*.yml" -type f

# 4. 不要なDockerfileの確認
find /home/AdminUser/ -name "Dockerfile*" -type f

# 5. 不要なrequirementsファイルの確認
find /home/AdminUser/ -name "requirements*.txt" -type f

# 6. 不要な.envファイルの確認
find /home/AdminUser/ -name ".env*" -type f

# 7. 不要なスクリプトファイルの確認
find /home/AdminUser/ -name "*.sh" -type f

# 8. 不要なPortainerスタックファイルの確認
find /home/AdminUser/ -name "portainer-stack*.yml" -type f

# 9. 不要なバックアップファイルの確認
find /home/AdminUser/ -name "*.backup" -o -name "*.bak" -o -name "*~" -type f

# 10. 空のディレクトリの確認
find /home/AdminUser/ -type d -empty

EOF

echo ""
echo "🧹 推奨クリーンアップコマンド:"
echo ""

cat << 'EOF'
# 以下のコマンドで不要ファイルをクリーンアップできます:

# 1. 古いmeeting-minutes-bycディレクトリを削除（簡易版）
rm -rf /home/AdminUser/meeting-minutes-byc

# 2. 不要なDocker Composeファイルを削除
rm -f /home/AdminUser/docker-compose-meeting-minutes-*.yml

# 3. 不要なDockerfileを削除
rm -f /home/AdminUser/Dockerfile.meeting-minutes-*

# 4. 不要なrequirementsファイルを削除
rm -f /home/AdminUser/requirements-meeting-minutes-*.txt

# 5. 不要なスクリプトファイルを削除
rm -f /home/AdminUser/setup-nas-env.sh

# 6. 不要なPortainerスタックファイルを削除
rm -f /home/AdminUser/portainer-stack-*.yml

# 7. 空のディレクトリを削除
find /home/AdminUser/ -type d -empty -delete

# 8. 一時ファイルを削除
find /home/AdminUser/ -name "*.tmp" -o -name "*.temp" -delete

# 9. ログファイルをクリーンアップ
find /home/AdminUser/ -name "*.log" -mtime +7 -delete

EOF

echo ""
echo "⚠️  注意事項:"
echo "   - 削除前に必ずファイルの内容を確認してください"
echo "   - 重要なファイルは削除しないでください"
echo "   - バックアップを取ってから実行することを推奨します"
echo ""
echo "💡 安全なクリーンアップ手順:"
echo "   1. まず上記の確認コマンドを実行"
echo "   2. 不要なファイルを特定"
echo "   3. バックアップを作成"
echo "   4. 段階的に削除を実行"
echo ""
echo "🔍 現在のNAS環境の状態確認:"
echo "   - メインアプリケーション: /home/AdminUser/meeting-minutes-byc/"
echo "   - データ保存: /volume1/data/meeting-minutes-byc/"
echo "   - これらのディレクトリは削除しないでください"

