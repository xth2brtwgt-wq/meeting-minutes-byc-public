# Meeting Minutes BYC - 音声議事録生成システム

## 🎯 概要

音声ファイルをアップロードして、AI（Gemini）を使用して文字起こしと議事録を自動生成するWebアプリケーションです。

## ✨ 機能

- **音声ファイルアップロード**: MP3、WAV、M4A等の音声ファイルに対応
- **AI文字起こし**: Google Gemini APIを使用した高精度な文字起こし
- **議事録自動生成**: 文字起こし結果から構造化された議事録を生成
- **Notion連携**: 生成した議事録をNotionデータベースに自動保存
- **メール送信**: 議事録をメールで送信
- **履歴管理**: 過去の議事録を閲覧・管理

## 🚀 技術スタック

- **Backend**: Python Flask
- **AI**: Google Gemini API
- **Database**: Notion API
- **Container**: Docker & Docker Compose
- **Frontend**: HTML, CSS, JavaScript

## 📋 セットアップ

### 1. 環境変数ファイルの作成

```bash
# 環境変数ファイルを作成
cp meeting-minutes-byc/env.example meeting-minutes-byc/.env
```

### 2. 必要なAPIキーの設定

`.env`ファイルに以下のAPIキーを設定してください：

```bash
# Gemini API設定
GEMINI_API_KEY=your_gemini_api_key_here

# Notion API設定
NOTION_API_KEY=your_notion_api_key_here
NOTION_DATABASE_ID=your_notion_database_id_here

# SMTP設定
SMTP_SERVER=your_smtp_server_here
SMTP_PORT=587
EMAIL_USER=your_email_here
EMAIL_PASSWORD=your_email_password_here
```

### 3. Docker Composeで起動

```bash
cd meeting-minutes-byc
sudo docker compose -f docker-compose.dev.yml up -d
```

### 4. アプリケーションアクセス

```
http://localhost:5000
```

## 📚 ドキュメント

- `GITHUB_DEPLOYMENT_GUIDE.md` - GitHub + NAS デプロイガイド
- `GITHUB_AUTHENTICATION_GUIDE.md` - GitHub認証ガイド
- `DEPLOYMENT_DOCUMENTATION.md` - 詳細な技術ドキュメント
- `TROUBLESHOOTING_GUIDE.md` - トラブルシューティングガイド

## 🔧 開発

### ローカル開発環境

```bash
# 仮想環境の作成
python -m venv venv
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate     # Windows

# 依存関係のインストール
pip install -r meeting-minutes-byc/requirements.txt

# アプリケーションの起動
cd meeting-minutes-byc
python app.py
```

### Docker開発環境

```bash
cd meeting-minutes-byc
docker compose -f docker-compose.dev.yml up -d
```

## 🌐 デプロイ

### NAS環境へのデプロイ

詳細は `GITHUB_DEPLOYMENT_GUIDE.md` を参照してください。

### GitHub Actions自動デプロイ

プッシュ時に自動的にNAS環境にデプロイされます。

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🤝 貢献

プルリクエストやイシューの報告を歓迎します。

## 📞 サポート

問題が発生した場合は、`TROUBLESHOOTING_GUIDE.md` を参照するか、イシューを作成してください。

---

**バージョン**: 1.0  
**作成者**: AI Assistant  
**プロジェクト**: Meeting Minutes BYC
