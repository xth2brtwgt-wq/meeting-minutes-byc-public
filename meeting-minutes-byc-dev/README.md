# Meeting Minutes BYC - 音声文字起こし・議事録生成アプリケーション

## 📋 概要

音声ファイルをアップロードして、Gemini AIを使用した自動文字起こしと議事録生成を行うWebアプリケーションです。

## ✨ 機能

- 🎤 **音声ファイルアップロード**: WAV, MP3, M4A, FLAC, OGG, WEBM対応
- 🤖 **AI文字起こし**: Gemini 1.5 Flashによる高精度な文字起こし
- 📝 **議事録自動生成**: 構造化された議事録の自動作成
- 💾 **結果保存**: JSON形式での結果保存とダウンロード
- 🎨 **美しいUI**: レスポンシブデザインのWebインターフェース

## 🚀 クイックスタート

### 1. 必要な準備

- Python 3.11以上
- Gemini AI API Key ([Google AI Studio](https://makersuite.google.com/app/apikey)で取得)

### 2. 環境設定

```bash
# リポジトリのクローン
git clone <repository-url>
cd meeting-minutes-byc-dev

# 環境変数ファイルの作成
cp env_example.txt .env
# .envファイルを編集してGEMINI_API_KEYを設定
```

### 3. 開発環境での実行

```bash
# 開発用スクリプトの実行
./run_dev.sh
```

または手動で実行:

```bash
# 仮想環境の作成とアクティベート
python3 -m venv venv
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# アプリケーションの起動
python app.py
```

### 4. アクセス

ブラウザで http://localhost:5000 にアクセス

## 🐳 Dockerでの実行

### 開発環境

```bash
# 環境変数の設定
export GEMINI_API_KEY=your_api_key_here

# Docker Composeで起動
docker-compose -f docker-compose.dev.yml up --build
```

### 本番環境

```bash
# 本番用Docker Composeで起動
docker-compose up --build
```

## 📁 プロジェクト構造

```
meeting-minutes-byc-dev/
├── app.py                 # メインアプリケーション
├── requirements.txt       # Python依存関係
├── Dockerfile            # Dockerイメージ定義
├── docker-compose.dev.yml # 開発用Docker Compose
├── run_dev.sh            # 開発用実行スクリプト
├── templates/
│   └── index.html        # メインHTMLテンプレート
├── static/
│   ├── css/
│   │   └── style.css     # スタイルシート
│   └── js/
│       └── app.js        # JavaScript
├── uploads/              # アップロードファイル（一時）
├── transcripts/          # 生成された議事録
└── README.md
```

## 🔧 設定

### 環境変数

| 変数名 | 説明 | デフォルト値 |
|--------|------|-------------|
| `GEMINI_API_KEY` | Gemini AI API Key | 必須 |
| `FLASK_ENV` | Flask環境 | `development` |
| `FLASK_DEBUG` | デバッグモード | `True` |
| `UPLOAD_DIR` | アップロードディレクトリ | `./uploads` |
| `TRANSCRIPT_DIR` | 議事録保存ディレクトリ | `./transcripts` |
| `HOST` | サーバーホスト | `0.0.0.0` |
| `PORT` | サーバーポート | `5000` |

## 📱 使用方法

1. **API Key設定**: Gemini AI API Keyを入力
2. **ファイルアップロード**: 音声ファイルをドラッグ&ドロップまたは選択
3. **処理実行**: 「文字起こし・議事録生成」ボタンをクリック
4. **結果確認**: 文字起こしと議事録を確認
5. **ダウンロード**: 結果をJSON形式でダウンロード

## 🎯 対応ファイル形式

- **WAV**: 無圧縮音声
- **MP3**: MPEG-1 Audio Layer 3
- **M4A**: MPEG-4 Audio
- **FLAC**: Free Lossless Audio Codec
- **OGG**: Ogg Vorbis
- **WEBM**: WebM Audio

## 🔍 API エンドポイント

- `GET /`: メインページ
- `GET /health`: ヘルスチェック
- `POST /upload`: 音声ファイルアップロードと処理
- `GET /transcripts/<filename>`: 議事録ファイルの取得

## 🛠️ 開発

### ローカル開発

```bash
# 開発サーバーの起動
python app.py

# テスト実行
python -m pytest tests/
```

### Docker開発

```bash
# 開発用コンテナの起動
docker-compose -f docker-compose.dev.yml up --build

# ログの確認
docker-compose -f docker-compose.dev.yml logs -f
```

## 📊 ログ

アプリケーションのログは以下の形式で出力されます:

```
2024-01-01 12:00:00 - app - INFO - ファイルをアップロードしました: meeting_20240101_120000.wav
2024-01-01 12:00:05 - app - INFO - 処理完了: meeting_20240101_120000.wav
```

## 🚨 トラブルシューティング

### よくある問題

1. **API Keyエラー**
   - Gemini AI API Keyが正しく設定されているか確認
   - API Keyの権限とクォータを確認

2. **ファイルアップロードエラー**
   - ファイル形式が対応しているか確認
   - ファイルサイズが100MB以下か確認

3. **文字起こしエラー**
   - 音声ファイルの品質を確認
   - ネットワーク接続を確認

## 📄 ライセンス

MIT License

## 🤝 貢献

プルリクエストやイシューの報告を歓迎します。

## 📞 サポート

問題が発生した場合は、GitHubのIssuesページで報告してください。
