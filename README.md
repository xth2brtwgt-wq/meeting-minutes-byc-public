# Meeting Minutes BYC

音声ファイルから自動的に議事録を生成するFlaskアプリケーションです。Gemini AI、Notion API、Gmail SMTPを統合した包括的な会議管理システムです。

## 🚀 主要機能

- **音声文字起こし**: Gemini AIによる高精度な音声転写
- **議事録生成**: AIによる構造化された議事録作成
- **Notion連携**: 自動的にNotionページ作成
- **メール送信**: 議事録の自動配信
- **ファイル管理**: アップロードファイルと生成ファイルの管理

## 📋 対応形式

- **音声ファイル**: MP3, WAV, M4A
- **最大ファイルサイズ**: 100MB
- **出力形式**: Markdown, テキスト

## 🛠️ 技術スタック

- **Backend**: Flask 3.1.2 (Python 3.11)
- **AI**: Google Gemini AI
- **Database**: Notion API
- **Email**: Gmail SMTP
- **Container**: Docker & Docker Compose
- **Frontend**: HTML/CSS/JavaScript

## 📚 ドキュメント

### デプロイメント関連
- [**クイックスタートガイド**](QUICK_START_GUIDE.md) - 最短でデプロイする手順
- [**デプロイメントドキュメント**](DEPLOYMENT_DOCUMENTATION.md) - 詳細なデプロイメント手順
- [**トラブルシューティングガイド**](TROUBLESHOOTING_GUIDE.md) - 問題解決方法

### 設定関連
- [**API キー設定ガイド**](API_KEYS_SETUP.md) - 必要なAPI キーの取得と設定方法

### 環境設定
- [**Ugreen NAS セットアップ**](UGREEN_DXP2800_SETUP.md) - NAS環境の構築
- [**Portainer セットアップ**](PORTAINER_SETUP.md) - コンテナ管理ツールの設定

## 🚀 クイックスタート

### 1. 前提条件
- Ugreen NAS (DXP2800)
- Docker & Docker Compose
- 管理者権限 (your_username)

### 2. 必要なAPI キー
- **Gemini AI API キー**: https://makersuite.google.com/app/apikey
- **Notion API キー**: https://www.notion.so/my-integrations
- **Gmail アプリパスワード**: Gmail設定 > セキュリティ

### 3. デプロイメント
```bash
# NASに接続
ssh your_username@your_nas_ip

# プロジェクトディレクトリを作成
mkdir -p /home/your_username/meeting-minutes-byc-dev
cd /home/your_username/meeting-minutes-byc-dev

# 設定ファイルを作成（詳細はクイックスタートガイドを参照）
# docker-compose.yml, Dockerfile, requirements.txt, .env など

# コンテナを起動
sudo docker compose up -d

# ヘルスチェック
curl http://your_nas_ip:5002/health
```

### 4. アクセス
- **URL**: http://your_nas_ip:5002
- **ヘルスチェック**: http://your_nas_ip:5002/health

## 📁 プロジェクト構造

```
meeting-minutes-byc-dev/
├── app.py                    # メインアプリケーション
├── requirements.txt          # Python依存関係
├── docker-compose.yml        # Docker Compose設定
├── Dockerfile               # Dockerイメージ設定
├── .env                     # 環境変数設定
├── utils/                   # ユーティリティモジュール
│   ├── email_sender.py      # メール送信機能
│   ├── notion_client.py     # Notion連携機能
│   └── markdown_generator.py # Markdown生成機能
├── templates/               # HTMLテンプレート
│   └── index.html
└── static/                  # 静的ファイル
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## 🔧 環境変数

```bash
# Gemini AI API Key
GEMINI_API_KEY=your_gemini_api_key

# Notion Integration
NOTION_API_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_database_id

# Email Settings
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com

# Application Settings
FLASK_ENV=production
FLASK_DEBUG=False
UPLOAD_DIR=/app/uploads
TRANSCRIPT_DIR=/app/transcripts
HOST=0.0.0.0
PORT=5000
```

## 🐳 Docker コマンド

### 基本的な操作
```bash
# コンテナ起動
sudo docker compose up -d

# コンテナ停止
sudo docker compose down

# ログ確認
sudo docker compose logs --tail=20

# コンテナ再起動
sudo docker compose restart
```

### デバッグ
```bash
# コンテナ内でコマンド実行
sudo docker exec -it meeting-minutes-byc-dev-app bash

# 環境変数確認
sudo docker exec -it meeting-minutes-byc-dev-app env

# ヘルスチェック
sudo docker exec -it meeting-minutes-byc-dev-app curl localhost:5000/health
```

## 🔍 トラブルシューティング

### よくある問題

1. **コンテナが起動しない**
   ```bash
   sudo docker compose logs
   ```

2. **ポートに接続できない**
   ```bash
   sudo netstat -tlnp | grep 5002
   ```

3. **API キーエラー**
   ```bash
   sudo docker exec -it meeting-minutes-byc-dev-app env | grep -E "(GEMINI|NOTION|EMAIL)"
   ```

詳細な解決方法は [トラブルシューティングガイド](TROUBLESHOOTING_GUIDE.md) を参照してください。

## 📊 監視とメンテナンス

### ヘルスチェック
```bash
# 定期的なヘルスチェック
curl -f http://your_nas_ip:5002/health || echo "Service down"
```

### ログ監視
```bash
# エラーログの監視
sudo docker compose logs | grep -i error | tail -10
```

### バックアップ
```bash
# データのバックアップ
tar -czf meeting-minutes-backup-$(date +%Y%m%d).tar.gz /volume1/data/meeting-minutes-byc-dev/
```

## 🔒 セキュリティ

- API キーは環境変数で管理
- .envファイルの権限を制限 (chmod 600)
- 定期的なAPI キーのローテーション
- 内部ネットワークでのみアクセス可能

## 🚀 今後の拡張予定

### 機能拡張
- [ ] ユーザー認証機能
- [ ] ファイル管理機能
- [ ] 議事録テンプレート機能
- [ ] 多言語対応

### 技術改善
- [ ] 非同期処理の導入
- [ ] レスポンシブデザインの強化
- [ ] エラーハンドリングの改善
- [ ] 詳細な操作ログの記録

## 📞 サポート

問題が発生した場合は、以下の順序で確認してください：

1. [トラブルシューティングガイド](TROUBLESHOOTING_GUIDE.md) を確認
2. ログファイルを確認
3. 環境変数の設定を確認
4. ネットワーク接続を確認

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

---

**最終更新**: 2025年10月15日

## 🚀 GitHub + NAS デプロイ

### 自動デプロイの設定

1. **GitHub Secretsの設定**:
   - `NAS_HOST`: `your_nas_ip`
   - `NAS_USER`: `your_username`
   - `NAS_SSH_KEY`: SSH秘密鍵

2. **手動デプロイ**:
   ```bash
   # NAS環境で実行
   cd /home/your_username/meeting-minutes-byc-dev
   ./deploy.sh
   ```

3. **GitHub Actions**:
   - `main`ブランチにプッシュすると自動デプロイ
   - 手動実行も可能（Actions タブから）  
**バージョン**: 1.0  
**作成者**: AI Assistant  
**プロジェクト**: Meeting Minutes BYC