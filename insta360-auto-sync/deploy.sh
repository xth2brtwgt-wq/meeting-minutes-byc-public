#!/bin/bash
# Insta360自動同期システム - デプロイスクリプト

set -e

# 設定
PROJECT_DIR="/home/AdminUser/nas-project/insta360-auto-sync"
BACKUP_DIR="/volume2/backup/insta360-auto-sync"
LOG_FILE="$PROJECT_DIR/logs/deploy.log"

# ログ関数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# エラーハンドリング
error_exit() {
    log "ERROR: $1"
    exit 1
}

# バックアップの作成
create_backup() {
    log "バックアップを作成中..."
    
    # バックアップディレクトリを作成
    mkdir -p "$BACKUP_DIR"
    
    # 現在の設定をバックアップ
    if [ -d "$PROJECT_DIR" ]; then
        tar -czf "$BACKUP_DIR/backup-$(date +%Y%m%d_%H%M%S).tar.gz" \
            -C "$(dirname "$PROJECT_DIR")" \
            "$(basename "$PROJECT_DIR")" \
            || log "WARNING: バックアップの作成に失敗しました"
    fi
    
    log "バックアップが完了しました"
}

# 環境の確認
check_environment() {
    log "環境を確認中..."
    
    # Dockerの確認
    if ! command -v docker &> /dev/null; then
        error_exit "Dockerがインストールされていません"
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error_exit "Docker Composeがインストールされていません"
    fi
    
    # 必要なディレクトリの確認
    if [ ! -d "/volume2/data" ]; then
        error_exit "/volume2/dataディレクトリが存在しません"
    fi
    
    log "環境確認が完了しました"
}

# 設定ファイルの確認
check_config() {
    log "設定ファイルを確認中..."
    
    # .envファイルの確認
    if [ ! -f "$PROJECT_DIR/.env" ]; then
        log "WARNING: .envファイルが見つかりません。env.exampleからコピーしてください"
        if [ -f "$PROJECT_DIR/env.example" ]; then
            cp "$PROJECT_DIR/env.example" "$PROJECT_DIR/.env"
            log ".envファイルを作成しました。設定を編集してください"
        fi
    fi
    
    # 設定ディレクトリの確認
    if [ ! -d "$PROJECT_DIR/config" ]; then
        error_exit "configディレクトリが存在しません"
    fi
    
    log "設定ファイルの確認が完了しました"
}

# ディレクトリの作成
create_directories() {
    log "必要なディレクトリを作成中..."
    
    # ログディレクトリ
    mkdir -p "$PROJECT_DIR/logs"
    
    # 転送先ディレクトリ
    mkdir -p "/volume2/data/insta360"
    
    # マウントポイント
    mkdir -p "/mnt/mac-share"
    
    log "ディレクトリの作成が完了しました"
}

# 権限の設定
set_permissions() {
    log "権限を設定中..."
    
    # 設定ファイルの権限
    chmod 600 "$PROJECT_DIR/.env" 2>/dev/null || true
    chmod 600 "$PROJECT_DIR/config"/*.json 2>/dev/null || true
    
    # スクリプトの実行権限
    chmod +x "$PROJECT_DIR/scripts"/*.py 2>/dev/null || true
    chmod +x "$PROJECT_DIR/scripts"/*.sh 2>/dev/null || true
    
    # ログディレクトリの権限
    chmod 755 "$PROJECT_DIR/logs"
    
    log "権限の設定が完了しました"
}

# Dockerコンテナの起動
start_containers() {
    log "Dockerコンテナを起動中..."
    
    cd "$PROJECT_DIR"
    
    # 既存のコンテナを停止
    docker-compose down 2>/dev/null || true
    
    # コンテナをビルドして起動
    docker-compose up -d --build
    
    # 起動を待機
    sleep 10
    
    # コンテナの状態を確認
    if ! docker-compose ps | grep -q "Up"; then
        error_exit "コンテナの起動に失敗しました"
    fi
    
    log "Dockerコンテナの起動が完了しました"
}

# 動作確認
verify_deployment() {
    log "動作確認を実行中..."
    
    cd "$PROJECT_DIR"
    
    # 接続テストを実行
    if docker-compose exec -T insta360-auto-sync python3 /app/scripts/test_connection.py; then
        log "接続テストが成功しました"
    else
        log "WARNING: 接続テストが失敗しました。設定を確認してください"
    fi
    
    # コンテナのログを確認
    log "コンテナのログを確認中..."
    docker-compose logs --tail=20 insta360-auto-sync
    
    log "動作確認が完了しました"
}

# メイン処理
main() {
    log "Insta360自動同期システムのデプロイを開始します"
    
    # 各処理を実行
    create_backup
    check_environment
    check_config
    create_directories
    set_permissions
    start_containers
    verify_deployment
    
    log "デプロイが完了しました"
    
    # 次のステップを表示
    echo ""
    echo "=== デプロイ完了 ==="
    echo "1. .envファイルの設定を確認してください"
    echo "2. 接続テストを実行してください:"
    echo "   docker-compose exec insta360-auto-sync python3 /app/scripts/test_connection.py"
    echo "3. 手動実行テストを実行してください:"
    echo "   docker-compose exec insta360-auto-sync python3 /app/scripts/sync.py --test"
    echo "4. ログを確認してください:"
    echo "   tail -f $PROJECT_DIR/logs/insta360_sync.log"
    echo ""
}

# スクリプト実行
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi
