"""
Meeting Minutes BYC - バージョン情報管理
"""

# アプリケーション情報
APP_NAME = "Meeting Minutes BYC"
APP_VERSION = "1.0.2"
APP_DESCRIPTION = "音声文字起こし・議事録生成アプリケーション"

# バージョン履歴
VERSION_HISTORY = {
    "1.0.0": "初回リリース",
    "1.0.1": "UI改善とバグ修正 - 結果画面の不要な文言削除、WebSocket接続ステータス削除、進捗バーテストボタン削除、メール件名・本文の修正、システムバージョン表示追加",
    "1.0.2": "カスタム辞書機能の追加 - 音声文字起こし精度向上のための辞書管理システム、専門用語・固有名詞の誤認識防止機能"
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
