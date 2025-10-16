#!/bin/bash
# Insta360自動同期システム - cron設定スクリプト

set -e

# 設定
CRON_SCHEDULE="${SYNC_SCHEDULE:-0 0 * * *}"  # デフォルト: 毎日0時
SCRIPT_PATH="/app/scripts/sync.py"
LOG_FILE="/app/logs/cron.log"

# ログ関数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# エラーハンドリング
error_exit() {
    log "ERROR: $1"
    exit 1
}

# cron設定を追加
setup_cron() {
    log "cron設定を追加中..."
    
    # 既存のcronエントリを削除
    crontab -l 2>/dev/null | grep -v "insta360-auto-sync" | crontab - || true
    
    # 新しいcronエントリを追加
    (crontab -l 2>/dev/null; echo "# Insta360自動同期システム"; echo "$CRON_SCHEDULE /usr/bin/python3 $SCRIPT_PATH >> $LOG_FILE 2>&1") | crontab -
    
    log "cron設定が追加されました"
    log "スケジュール: $CRON_SCHEDULE"
    log "スクリプト: $SCRIPT_PATH"
    log "ログファイル: $LOG_FILE"
}

# cron設定を確認
verify_cron() {
    log "cron設定を確認中..."
    
    crontab -l | grep -A 1 -B 1 "insta360-auto-sync" || error_exit "cron設定が見つかりません"
    
    log "cron設定の確認が完了しました"
}

# cronサービスを開始
start_cron() {
    log "cronサービスを開始中..."
    
    # cronデーモンを開始
    crond -f -l 2 &
    CRON_PID=$!
    
    log "cronサービスが開始されました (PID: $CRON_PID)"
    
    # PIDファイルを作成
    echo $CRON_PID > /var/run/crond.pid
    
    # プロセスを待機
    wait $CRON_PID
}

# メイン処理
main() {
    log "Insta360自動同期システム - cron設定開始"
    
    # ログディレクトリを作成
    mkdir -p "$(dirname "$LOG_FILE")"
    
    # cron設定を実行
    setup_cron
    verify_cron
    
    log "cron設定が完了しました"
    
    # 設定内容を表示
    log "--- 現在のcron設定 ---"
    crontab -l | grep -A 1 -B 1 "insta360-auto-sync" || true
    
    # cronサービスを開始
    start_cron
}

# スクリプト実行
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi
