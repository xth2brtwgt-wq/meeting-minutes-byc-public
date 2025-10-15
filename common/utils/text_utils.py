"""
テキスト処理に関する共通ユーティリティ
"""

import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    """テキスト処理クラス"""
    
    @staticmethod
    def clean_transcript(text: str) -> str:
        """文字起こしテキストをクリーンアップ"""
        if not text:
            return ""
        
        # 余分な空白を除去
        text = re.sub(r'\s+', ' ', text)
        
        # 句読点の正規化
        text = re.sub(r'[。、，．]', '。', text)
        
        # 改行の正規化
        text = re.sub(r'\n+', '\n', text)
        
        return text.strip()
    
    @staticmethod
    def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
        """キーワードを抽出"""
        # 簡単なキーワード抽出（実際の実装では形態素解析を使用）
        words = re.findall(r'[一-龯]+', text)  # 日本語の文字のみ
        
        # 頻度をカウント
        word_count = {}
        for word in words:
            if len(word) >= 2:  # 2文字以上の単語のみ
                word_count[word] = word_count.get(word, 0) + 1
        
        # 頻度順にソート
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, count in sorted_words[:max_keywords]]
    
    @staticmethod
    def generate_summary(text: str, max_length: int = 200) -> str:
        """テキストの要約を生成"""
        if len(text) <= max_length:
            return text
        
        # 文単位で分割
        sentences = re.split(r'[。！？]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return text[:max_length] + "..."
        
        # 最初の文から順に追加
        summary = ""
        for sentence in sentences:
            if len(summary + sentence) <= max_length:
                summary += sentence + "。"
            else:
                break
        
        return summary if summary else text[:max_length] + "..."

class MeetingNotesGenerator:
    """議事録生成クラス"""
    
    @staticmethod
    def generate_meeting_notes(transcript: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """議事録を生成"""
        if not transcript:
            return {"エラー": "文字起こしデータがありません"}
        
        # メタデータの設定
        if metadata is None:
            metadata = {}
        
        # 基本情報
        notes = {
            "会議概要": metadata.get("title", "音声ファイルから生成された議事録"),
            "開催日時": metadata.get("date", datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')),
            "参加者": metadata.get("participants", "未記載"),
            "場所": metadata.get("location", "未記載"),
        }
        
        # テキスト処理
        clean_text = TextProcessor.clean_transcript(transcript)
        
        # 要約生成
        summary = TextProcessor.generate_summary(clean_text, 300)
        notes["要約"] = summary
        
        # キーワード抽出
        keywords = TextProcessor.extract_keywords(clean_text, 5)
        notes["キーワード"] = ", ".join(keywords)
        
        # 発言内容
        notes["発言内容"] = clean_text
        
        # アクションアイテムの抽出（簡易版）
        action_items = MeetingNotesGenerator.extract_action_items(clean_text)
        if action_items:
            notes["アクションアイテム"] = action_items
        
        # 次回までの課題
        notes["次回までの課題"] = metadata.get("next_actions", "特になし")
        
        return notes
    
    @staticmethod
    def extract_action_items(text: str) -> List[str]:
        """アクションアイテムを抽出"""
        action_patterns = [
            r'([^。]*?)(?:やる|する|対応|検討|確認|報告|準備|作成|修正|更新)([^。]*?)',
            r'([^。]*?)(?:TODO|タスク|課題|宿題)([^。]*?)',
            r'([^。]*?)(?:次回|来週|明日|後で)([^。]*?)',
        ]
        
        action_items = []
        for pattern in action_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                item = "".join(match).strip()
                if len(item) > 10 and len(item) < 100:  # 適切な長さのアイテムのみ
                    action_items.append(item)
        
        return action_items[:5]  # 最大5個まで

def format_meeting_notes_html(notes: Dict[str, Any]) -> str:
    """議事録をHTML形式でフォーマット"""
    html = "<div class='meeting-notes'>"
    
    for key, value in notes.items():
        if key == "発言内容":
            html += f"<h4>{key}</h4>"
            html += f"<div class='transcript-content'>{value}</div>"
        elif key == "アクションアイテム" and isinstance(value, list):
            html += f"<h4>{key}</h4>"
            html += "<ul>"
            for item in value:
                html += f"<li>{item}</li>"
            html += "</ul>"
        else:
            html += f"<h4>{key}</h4>"
            html += f"<p>{value}</p>"
    
    html += "</div>"
    return html

def format_meeting_notes_markdown(notes: Dict[str, Any]) -> str:
    """議事録をMarkdown形式でフォーマット"""
    md = "# 議事録\n\n"
    
    for key, value in notes.items():
        if key == "発言内容":
            md += f"## {key}\n\n{value}\n\n"
        elif key == "アクションアイテム" and isinstance(value, list):
            md += f"## {key}\n\n"
            for item in value:
                md += f"- {item}\n"
            md += "\n"
        else:
            md += f"## {key}\n\n{value}\n\n"
    
    return md

