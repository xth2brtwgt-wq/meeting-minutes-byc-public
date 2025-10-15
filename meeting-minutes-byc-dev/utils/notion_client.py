#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notion統合機能
"""

import os
import logging
from notion_client import Client
import re
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

class NotionClient:
    def __init__(self):
        self.notion_api_key = os.getenv('NOTION_API_KEY')
        self.database_id = os.getenv('NOTION_DATABASE_ID')
        
        if self.notion_api_key:
            self.client = Client(auth=self.notion_api_key)
        else:
            self.client = None
            logger.warning("Notion API Key not configured")
    
    def create_meeting_page(self, meeting_data):
        """Notionに議事録ページを作成"""
        try:
            if not self.client or not self.database_id:
                raise Exception("Notion設定が不完全です")
            
            # 日時形式を変換
            formatted_meeting_date = self._format_datetime_for_notion(meeting_data.get('meeting_date', ''))
            
            # 議事録のタイトル
            title = f"議事録 - {formatted_meeting_date}"
            
            # ページのプロパティ（ユーザーのNotionデータベース構成に合わせて修正）
            properties = {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
                "WaveFile": {
                    "rich_text": [
                        {
                            "text": {
                                "content": meeting_data.get('filename', '不明')
                            }
                        }
                    ]
                }
            }
            
            # 日時プロパティの追加（空文字列の場合は現在時刻を使用）
            meeting_date = meeting_data.get('meeting_date', '')
            if meeting_date and meeting_date.strip():
                try:
                    # ISO形式に変換
                    if 'T' in meeting_date:
                        dt = datetime.fromisoformat(meeting_date.replace('Z', '+00:00'))
                    else:
                        # その他の形式をISO形式に変換
                        dt = datetime.strptime(meeting_date, '%Y-%m-%d %H:%M:%S')
                    
                    # UIから入力された日時は日本時間として扱い、JSTタイムゾーンを明示的に設定
                    # 日本時間（UTC+9）として設定
                    jst = timezone(timedelta(hours=9))
                    dt_jst = dt.replace(tzinfo=jst)
                    iso_date = dt_jst.isoformat()
                    
                    properties["MeetingDate"] = {
                        "date": {
                            "start": iso_date
                        }
                    }
                except ValueError:
                    # パースできない場合は現在時刻を日本時間として使用
                    jst = timezone(timedelta(hours=9))
                    dt_jst = datetime.now(jst)
                    properties["MeetingDate"] = {
                        "date": {
                            "start": dt_jst.isoformat()
                        }
                    }
            else:
                # 空の場合は現在時刻を日本時間として使用
                jst = timezone(timedelta(hours=9))
                dt_jst = datetime.now(jst)
                properties["MeetingDate"] = {
                    "date": {
                        "start": dt_jst.isoformat()
                    }
                }
            
            # 作成日時は常に現在時刻（日本時間）
            jst = timezone(timedelta(hours=9))
            dt_jst = datetime.now(jst)
            properties["CreationDate"] = {
                "date": {
                    "start": dt_jst.isoformat()
                }
            }
            
            # Tagプロパティは設定なしなので追加しない
            
            # ページの作成
            response = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
            
            page_id = response['id']
            
            # 議事録の内容を追加
            self._add_meeting_content(page_id, meeting_data)
            
            logger.info(f"Notionページ作成完了: {page_id}")
            return page_id
            
        except Exception as e:
            logger.error(f"Notionページ作成エラー: {str(e)}")
            raise Exception(f"Notionページ作成に失敗しました: {str(e)}")
    
    def _add_meeting_content(self, page_id, meeting_data):
        """ページに議事録の内容を追加"""
        try:
            # 文字起こし内容は除外し、議事録のみを追加
            meeting_notes = meeting_data.get('meeting_notes', '')
            
            # ブロックの作成
            blocks = []
            
            # 議事録セクションのみ
            if meeting_notes:
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": "議事録"
                                }
                            }
                        ]
                    }
                })
                
                # 議事録テキストを改行毎に分割
                meeting_blocks = self._split_text_by_lines(meeting_notes)
                blocks.extend(meeting_blocks)
            
            # ブロックを追加（一度に追加するブロック数も制限があるため、バッチ処理）
            if blocks:
                self._add_blocks_in_batches(page_id, blocks)
            
            logger.info(f"Notionページ内容追加完了: {page_id}")
            
        except Exception as e:
            logger.error(f"Notionページ内容追加エラー: {str(e)}")
            raise Exception(f"Notionページ内容追加に失敗しました: {str(e)}")
    
    def _split_text_by_lines(self, text):
        """テキストを改行毎に分割してブロックを作成（Markdown形式をNotionブロックに変換）"""
        blocks = []
        
        # テキストを改行で分割
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line:  # 空行はスキップ
                # Markdown形式をNotionブロックに変換
                block = self._convert_markdown_to_notion_block(line)
                if block:
                    blocks.append(block)
        
        return blocks
    
    def _convert_markdown_to_notion_block(self, line):
        """Markdown形式の行をNotionブロックに変換"""
        # 見出しの処理
        if line.startswith('# '):
            heading_text = '📝 ' + line[2:].strip()
            return {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "text": {
                                "content": heading_text
                            }
                        }
                    ]
                }
            }
        elif line.startswith('## '):
            heading_text = '📌 ' + line[3:].strip()
            return {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {
                            "text": {
                                "content": heading_text
                            }
                        }
                    ]
                }
            }
        elif line.startswith('### '):
            heading_text = '🔹 ' + line[4:].strip()
            return {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [
                        {
                            "text": {
                                "content": heading_text
                            }
                        }
                    ]
                }
            }
        # 引用の処理
        elif line.startswith('> '):
            content = line[2:].strip()
            return {
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": self._parse_inline_rich_text(content)
                }
            }
        # タスク（チェックボックス）の処理: "- [ ] text" / "- [x] text"
        elif re.match(r"^- \[( |x|X)\] ", line):
            checked = True if re.match(r"^- \[(x|X)\] ", line) else False
            content = re.sub(r"^- \[( |x|X)\] ", "", line).strip()
            return {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "checked": checked,
                    "rich_text": self._parse_inline_rich_text(content)
                }
            }
        # 箇条書きの処理
        elif line.startswith('- '):
            content = line[2:].strip()
            return {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": self._parse_inline_rich_text(content)
                }
            }
        # 番号付きリストの処理（任意桁数の番号に対応）
        elif re.match(r"^\d+\. ", line):
            content = re.sub(r"^\d+\. ", "", line).strip()
            return {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": self._parse_inline_rich_text(content)
                }
            }
        # 区切り線の処理
        elif line.startswith('---'):
            return {
                "object": "block",
                "type": "divider",
                "divider": {}
            }
        # 通常の段落
        else:
            # 2000文字を超える場合は分割
            if len(line) > 2000:
                chunks = self._split_long_line(line)
                return chunks[0] if chunks else None
            else:
                return {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": self._parse_inline_rich_text(line)
                    }
                }

    def _parse_inline_rich_text(self, text: str):
        """Markdownのインライン装飾をNotionのrich_text配列に変換。
        サポート: **bold**, *italic*, `code`, [text](url)
        複雑な入れ子は簡易対応（左から順に評価）。
        """
        if not text:
            return [{"text": {"content": ""}}]

        tokens = []
        i = 0
        length = len(text)

        link_pattern = re.compile(r"\[([^\]]+)\]\(([^\)]+)\)")

        while i < length:
            # リンク
            m = link_pattern.search(text, i)
            if m and m.start() == i:
                tokens.append({
                    "text": {"content": m.group(1), "link": {"url": m.group(2)}},
                    "annotations": {"bold": False, "italic": False, "code": False, "underline": False, "strikethrough": False}
                })
                i = m.end()
                continue

            # コード `code`
            if text.startswith('`', i):
                j = text.find('`', i + 1)
                if j != -1:
                    code_content = text[i+1:j]
                    tokens.append({
                        "text": {"content": code_content},
                        "annotations": {"bold": False, "italic": False, "code": True, "underline": False, "strikethrough": False}
                    })
                    i = j + 1
                    continue
            # 太字 **bold**
            if text.startswith('**', i):
                j = text.find('**', i + 2)
                if j != -1:
                    bold_content = text[i+2:j]
                    tokens.append({
                        "text": {"content": bold_content},
                        "annotations": {"bold": True, "italic": False, "code": False, "underline": False, "strikethrough": False}
                    })
                    i = j + 2
                    continue
            # 斜体 *italic*
            if text.startswith('*', i):
                j = text.find('*', i + 1)
                if j != -1:
                    italic_content = text[i+1:j]
                    tokens.append({
                        "text": {"content": italic_content},
                        "annotations": {"bold": False, "italic": True, "code": False, "underline": False, "strikethrough": False}
                    })
                    i = j + 1
                    continue

            # 通常文字（次の特殊トークンまで）
            next_positions = [
                pos for pos in [
                    text.find('`', i),
                    text.find('**', i),
                    text.find('*', i),
                ] if pos != -1
            ]
            # リンクの次位置
            m2 = link_pattern.search(text, i)
            if m2:
                next_positions.append(m2.start())

            if next_positions:
                j = min(next_positions)
            else:
                j = length

            chunk = text[i:j]
            if chunk:
                tokens.append({
                    "text": {"content": chunk},
                    "annotations": {"bold": False, "italic": False, "code": False, "underline": False, "strikethrough": False}
                })
            i = j

        # Notion API仕様ではrich_textは配列、各要素は{"text":{...}, "annotations":{...}}形式
        # annotationsが無い場合は省略可だが、明示しておく
        normalized = []
        for t in tokens:
            if "annotations" not in t:
                t["annotations"] = {"bold": False, "italic": False, "code": False, "underline": False, "strikethrough": False}
            normalized.append(t)
        return normalized
    
    def _split_long_line(self, line, max_length=2000):
        """長い行を2000文字ずつに分割"""
        blocks = []
        
        for i in range(0, len(line), max_length):
            chunk = line[i:i + max_length]
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "text": {
                                "content": chunk
                            }
                        }
                    ]
                }
            })
        
        return blocks
    
    def _add_blocks_in_batches(self, page_id, blocks, batch_size=100):
        """ブロックをバッチで追加（Notion APIの制限に対応）"""
        for i in range(0, len(blocks), batch_size):
            batch = blocks[i:i + batch_size]
            try:
                self.client.blocks.children.append(
                    block_id=page_id,
                    children=batch
                )
                logger.info(f"Notionブロックバッチ追加完了: {len(batch)}個のブロック")
            except Exception as e:
                logger.error(f"Notionブロックバッチ追加エラー: {str(e)}")
                # バッチサイズを小さくして再試行
                if batch_size > 10:
                    self._add_blocks_in_batches(page_id, batch, batch_size // 2)
                else:
                    raise e
    
    def _format_datetime_for_notion(self, datetime_str):
        """日時文字列をNotion用の形式に変換"""
        if not datetime_str or datetime_str == '未設定':
            return '未設定'
        
        try:
            # ISO形式の日時をパース
            if 'T' in datetime_str:
                dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            else:
                # その他の形式を試行
                dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            
            # YYYY/MM/DD HH24:Mi形式に変換
            return dt.strftime('%Y/%m/%d %H:%M')
        except ValueError:
            # パースできない場合は元の文字列を返す
            return datetime_str

    def test_connection(self):
        """Notion接続テスト"""
        try:
            if not self.client:
                return False, "Notion API Key not configured"
            
            if not self.database_id:
                return False, "Notion Database ID not configured"
            
            # データベースの情報を取得
            database = self.client.databases.retrieve(database_id=self.database_id)
            return True, f"Connected to database: {database.get('title', [{}])[0].get('plain_text', 'Unknown')}"
            
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
