"""
Meeting Minutes BYC - バージョン情報管理
"""

# アプリケーション情報
APP_NAME = "Meeting Minutes BYC"
APP_VERSION = "1.1.0"
APP_DESCRIPTION = "音声文字起こし・議事録生成アプリケーション"

# バージョン履歴
VERSION_HISTORY = {
    "1.0.0": "初回リリース",
    "1.0.1": "UI改善とバグ修正 - 結果画面の不要な文言削除、WebSocket接続ステータス削除、進捗バーテストボタン削除、メール件名・本文の修正、システムバージョン表示追加",
    "1.0.2": "カスタム辞書機能の追加 - 音声文字起こし精度向上のための辞書管理システム、専門用語・固有名詞の誤認識防止機能",
    "1.0.3": "レスポンシブデザインの大幅強化 - タブレット・モバイル・小型モバイル対応、タッチデバイス最適化（48px最小タップターゲット、iOS自動ズーム防止）、辞書管理画面のモバイル対応、横向き表示対応、アクセシビリティ改善、印刷スタイル追加",
    "1.1.0": "セキュリティ強化と本番環境移行 - Dockerセキュリティ強化（リソース制限、ログ制限、ヘルスチェック）、本番環境設定（production mode）、セキュリティオプション追加（no-new-privileges）、コンテナ名標準化（docker-compose.yml使用）"
}

def get_version_info():
    """バージョン情報を取得"""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "description": APP_DESCRIPTION
    }

def get_version_string():
    """バージョン文字列を取得"""
    return f"{APP_NAME} v{APP_VERSION}"

def get_version_history():
    """バージョン履歴を取得"""
    return VERSION_HISTORY
