#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meeting Minutes BYC - Flask Application
音声ファイルの文字起こしと議事録生成アプリケーション
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# カスタムユーティリティのインポート
from utils.email_sender import EmailSender
from utils.notion_client import NotionClient
from utils.markdown_generator import MarkdownGenerator

# 環境変数の読み込み
load_dotenv()

# Flask アプリケーションの初期化
app = Flask(__name__)
CORS(app)

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 設定
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
UPLOAD_FOLDER = os.getenv('UPLOAD_DIR', './uploads')
TRANSCRIPT_FOLDER = os.getenv('TRANSCRIPT_DIR', './transcripts')
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'flac', 'ogg', 'webm'}

# ディレクトリの作成
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)

# Gemini AI の設定
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    logger.info('Gemini AI configured successfully')
else:
    logger.warning('GEMINI_API_KEY not found')
    model = None

# ユーティリティクラスの初期化
email_sender = EmailSender()
notion_client = NotionClient()
markdown_generator = MarkdownGenerator()

def allowed_file(filename):
    """ファイル拡張子のチェック"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    """ユニークなファイル名を生成"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(filename)
    return f"{name}_{timestamp}{ext}"

def transcribe_audio_with_gemini(file_path):
    """Gemini AI を使用して音声を文字起こし"""
    try:
        if not model:
            raise Exception("Gemini AI model not configured")
        
        # 音声ファイルを読み込み
        with open(file_path, 'rb') as audio_file:
            audio_data = audio_file.read()
        
        # ファイル形式の判定
        file_ext = os.path.splitext(file_path)[1].lower()
        mime_type_map = {
            '.wav': 'audio/wav',
            '.mp3': 'audio/mp3',
            '.m4a': 'audio/mp4',
            '.flac': 'audio/flac',
            '.ogg': 'audio/ogg',
            '.webm': 'audio/webm'
        }
        mime_type = mime_type_map.get(file_ext, 'audio/wav')
        
        # Gemini AI に送信するためのプロンプト
        prompt = """
        以下の音声ファイルの内容を正確に文字起こししてください。
        日本語の会議内容を想定し、話者の区別も含めて詳細に文字起こししてください。
        
        出力形式：
        [時刻] 話者名: 発言内容
        
        例：
        [00:01:23] 田中: 今日の会議の議題について説明します
        [00:02:15] 佐藤: ありがとうございます。質問があります
        """
        
        # Gemini AI に送信
        response = model.generate_content([
            prompt,
            {
                "mime_type": mime_type,
                "data": audio_data
            }
        ])
        
        return response.text
        
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise Exception(f"文字起こしに失敗しました: {str(e)}")

def _format_datetime_for_gemini(datetime_str):
    """日時文字列をYYYY/MM/DD HH24:Mi形式に変換"""
    if not datetime_str or datetime_str == '未設定':
        return '[日時]'
    
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

def generate_meeting_notes_with_gemini(transcript, conditions="", meeting_date=""):
    """Gemini AI を使用して議事録を生成"""
    try:
        if not model:
            raise Exception("Gemini AI model not configured")
        
        conditions_text = f"\n\n追加条件: {conditions}" if conditions else ""
        meeting_date_text = f"\n\n会議日時: {meeting_date}" if meeting_date else ""
        
        # 日時形式を変換（空の場合は現在時刻を使用）
        if meeting_date and meeting_date.strip():
            formatted_meeting_date = _format_datetime_for_gemini(meeting_date)
        else:
            formatted_meeting_date = datetime.now().strftime('%Y/%m/%d %H:%M')
        
        prompt = f"""
        あなたは議事録作成の専門家です。
        
        以下の会議の文字起こし内容を基に、構造化された議事録を作成してください。
        
        文字起こし内容：
        {transcript}
        {conditions_text}
        {meeting_date_text}
        
        以下の形式で議事録を作成してください：
        
        # 会議議事録
        
        ## 会議概要
        - 日時: {formatted_meeting_date}
        - 参加者: [参加者名]
        - 議題: [主要な議題]
        
        ## 主要な議題・トピック
        1. [議題1]
           - 内容: [詳細]
           - 決定事項: [決定内容]
        
        2. [議題2]
           - 内容: [詳細]
           - 決定事項: [決定内容]
        
        3. [議題3]
           - 内容: [詳細]
           - 決定事項: [決定内容]
        
        ## 決定事項
        - [決定事項1]
        - [決定事項2]
        - [決定事項3]
        
        ## アクションアイテム
        - [担当者]: [タスク内容] - [期限]
        - [担当者]: [タスク内容] - [期限]
        - [担当者]: [タスク内容] - [期限]
        
        ## 次回までの課題
        - [課題1]
        - [課題2]
        - [課題3]
        
        ## 備考
        [その他の重要な情報]
        
        重要：議題・トピックの番号は必ず1から順番に連番で記載してください。文字起こし内容から複数の議題を抽出し、それぞれに適切な番号を付けてください。
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        logger.error(f"Meeting notes generation error: {str(e)}")
        raise Exception(f"議事録生成に失敗しました: {str(e)}")

@app.route('/')
def index():
    """メインページ"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """ヘルスチェック"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'gemini_configured': model is not None,
        'flask_version': '3.1.2'
    })

@app.route('/test-notion')
def test_notion():
    """Notion接続テスト"""
    try:
        success, message = notion_client.test_connection()
        return jsonify({
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Notion接続テストエラー: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """音声ファイルのアップロードと処理"""
    try:
        # ファイルのチェック
        if 'audio' not in request.files:
            return jsonify({'error': '音声ファイルが選択されていません'}), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'ファイルが選択されていません'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'サポートされていないファイル形式です'}), 400
        
        # 追加パラメータの取得
        meeting_date = request.form.get('meeting_date', '')
        conditions = request.form.get('conditions', '')
        email = request.form.get('email', '')
        send_to_notion = request.form.get('send_to_notion', 'false').lower() == 'true'
        
        # ファイルの保存
        filename = generate_unique_filename(secure_filename(file.filename))
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        logger.info(f'ファイルをアップロードしました: {filename}')
        
        # 文字起こし
        transcript = transcribe_audio_with_gemini(filepath)
        
        # 議事録生成
        meeting_notes = generate_meeting_notes_with_gemini(transcript, conditions, meeting_date)
        
        # 結果の保存
        result = {
            'filename': filename,
            'transcript': transcript,
            'meeting_notes': meeting_notes,
            'meeting_date': meeting_date,
            'conditions': conditions,
            'timestamp': datetime.now().isoformat(),
            'file_size': os.path.getsize(filepath)
        }
        
        result_file = os.path.join(TRANSCRIPT_FOLDER, f'{filename}.json')
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        # ファイルの生成
        md_filepath = markdown_generator.generate_meeting_markdown(result)
        transcript_filepath = markdown_generator.generate_transcript_file(result)
        
        # Notion登録（メール送信前に実行）
        notion_page_id = None
        if send_to_notion:
            try:
                notion_page_id = notion_client.create_meeting_page(result)
                result['notion_page_id'] = notion_page_id
                result['notion_sent'] = True
            except Exception as e:
                logger.error(f'Notion登録エラー: {str(e)}')
                result['notion_sent'] = False
                result['notion_error'] = str(e)
        else:
            result['notion_sent'] = False
            result['notion_page_id'] = None
        
        # メール送付（Notion登録結果を含めて送信）
        email_sent = False
        if email and email.strip():  # 空文字列もチェック
            try:
                # デバッグ情報をログに出力
                logger.info(f'メール送信開始 - email_sent: {result.get("email_sent")}, notion_sent: {result.get("notion_sent")}')
                email_sender.send_meeting_minutes(email, result, transcript_filepath, md_filepath)
                email_sent = True
                result['email_sent'] = True
                result['email_address'] = email
                logger.info(f'メール送信完了 - email_sent: {result.get("email_sent")}, notion_sent: {result.get("notion_sent")}')
            except Exception as e:
                logger.error(f'メール送信エラー: {str(e)}')
                result['email_sent'] = False
                result['email_error'] = str(e)
        else:
            result['email_sent'] = False
            result['email_address'] = None
        
        # アップロードファイルの削除
        os.remove(filepath)
        
        logger.info(f'処理完了: {filename}')
        return jsonify(result)
        
    except Exception as e:
        logger.error(f'エラーが発生しました: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/transcripts/<filename>')
def get_transcript(filename):
    """議事録ファイルの取得"""
    try:
        return send_from_directory(TRANSCRIPT_FOLDER, filename)
    except FileNotFoundError:
        return jsonify({'error': 'ファイルが見つかりません'}), 404

if __name__ == '__main__':
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f'Starting Flask application on {host}:{port}')
    app.run(host=host, port=port, debug=debug)
