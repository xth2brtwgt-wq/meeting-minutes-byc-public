#!/bin/bash
# Insta360自動同期システム - Mac共有フォルダマウントスクリプト

set -e

# 設定
MAC_IP="${MAC_IP:-192.168.68.69}"
MAC_USERNAME="${MAC_USERNAME:-Yoshi}"
MAC_PASSWORD="${MAC_PASSWORD}"
MAC_SHARE="${MAC_SHARE:-Yoshi}"
MOUNT_POINT="/mnt/mac-share"
SOURCE_PATH="/source"

# ログ関数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# エラーハンドリング
error_exit() {
    log "ERROR: $1"
    exit 1
}

# マウントポイントの作成
create_mount_point() {
    log "マウントポイントを作成中: $MOUNT_POINT"
    mkdir -p "$MOUNT_POINT" || error_exit "マウントポイントの作成に失敗しました"
}

# 既存のマウントを解除
unmount_existing() {
    if mountpoint -q "$MOUNT_POINT"; then
        log "既存のマウントを解除中: $MOUNT_POINT"
        umount "$MOUNT_POINT" || log "WARNING: マウント解除に失敗しました（無視します）"
    fi
}

# Mac共有フォルダをマウント
mount_mac_share() {
    log "Mac共有フォルダをマウント中..."
    log "接続先: //$MAC_IP/$MAC_SHARE"
    log "マウントポイント: $MOUNT_POINT"
    
    # マウントコマンドを実行
    mount -t cifs "//$MAC_IP/$MAC_SHARE" "$MOUNT_POINT" \
        -o username="$MAC_USERNAME",password="$MAC_PASSWORD",uid=1000,gid=1000,iocharset=utf8,file_mode=0777,dir_mode=0777 \
        || error_exit "Mac共有フォルダのマウントに失敗しました"
    
    log "Mac共有フォルダのマウントが完了しました"
}

# ソースパスのシンボリックリンクを作成
create_source_link() {
    log "ソースパスのシンボリックリンクを作成中: $SOURCE_PATH -> $MOUNT_POINT"
    
    # 既存のリンクを削除
    if [ -L "$SOURCE_PATH" ] || [ -e "$SOURCE_PATH" ]; then
        rm -rf "$SOURCE_PATH" || log "WARNING: 既存のソースパス削除に失敗しました"
    fi
    
    # シンボリックリンクを作成
    ln -s "$MOUNT_POINT" "$SOURCE_PATH" || error_exit "ソースパスのシンボリックリンク作成に失敗しました"
    
    log "ソースパスのシンボリックリンクが作成されました"
}

# 接続テスト
test_connection() {
    log "接続テストを実行中..."
    
    # マウントポイントの確認
    if ! mountpoint -q "$MOUNT_POINT"; then
        error_exit "マウントポイントがマウントされていません"
    fi
    
    # ディレクトリの確認
    if [ ! -d "$MOUNT_POINT" ]; then
        error_exit "マウントポイントがディレクトリではありません"
    fi
    
    # 読み取り権限の確認
    if [ ! -r "$MOUNT_POINT" ]; then
        error_exit "マウントポイントに読み取り権限がありません"
    fi
    
    log "接続テストが成功しました"
}

# メイン処理
main() {
    log "Insta360自動同期システム - Mac共有フォルダマウント開始"
    
    # 必要な環境変数の確認
    if [ -z "$MAC_PASSWORD" ]; then
        error_exit "MAC_PASSWORD環境変数が設定されていません"
    fi
    
    # マウント処理を実行
    create_mount_point
    unmount_existing
    mount_mac_share
    create_source_link
    test_connection
    
    log "Mac共有フォルダマウントが完了しました"
    
    # マウント情報を表示
    log "マウント情報:"
    df -h "$MOUNT_POINT" || true
    ls -la "$SOURCE_PATH" || true
}

# スクリプト実行
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi
