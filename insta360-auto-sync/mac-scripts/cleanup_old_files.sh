#!/bin/bash
# Insta360フォルダの古いファイルを削除するスクリプト

# 設定
INSTA360_DIR="/Users/Yoshi/Movies/Insta360/Download"
DAYS_TO_KEEP=30  # 30日以上前のファイルを削除

# ログ
echo "==================================="
echo "Insta360ファイル削除スクリプト"
echo "実行日時: $(date '+%Y-%m-%d %H:%M:%S')"
echo "==================================="

# 削除対象のファイルを検索
echo "削除対象ファイルを検索中..."
find "$INSTA360_DIR" -type f \
  \( -name "VID_*.mp4" -o -name "*.insv" -o -name "*.insp" -o -name "*.jpg" -o -name "*.dng" -o -name "*.raw" \) \
  -mtime +$DAYS_TO_KEEP -print | while read file; do
    echo "削除: $file"
    rm -f "$file"
done

echo "==================================="
echo "完了"
echo "==================================="

