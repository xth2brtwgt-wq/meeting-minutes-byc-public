# Windows環境セットアップガイド

## 🪟 概要

このガイドでは、Windows環境でMeeting Minutes BYCシステムをセットアップする方法を説明します。

## 📋 前提条件

- Windows 10/11
- 管理者権限
- インターネット接続

## 🔧 必要なソフトウェアのインストール

### 1. Docker Desktop for Windows

#### ダウンロード
1. [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)にアクセス
2. 「Download for Windows」をクリック
3. インストーラーを実行

#### インストール
1. インストーラーを管理者として実行
2. 「Use WSL 2 instead of Hyper-V」を推奨
3. インストール完了後、再起動

#### 確認
```powershell
# PowerShellで確認
docker --version
docker compose version
```

### 2. Git for Windows

#### ダウンロード
1. [Git for Windows](https://git-scm.com/download/win)にアクセス
2. 最新版をダウンロード
3. インストーラーを実行

#### インストール
1. デフォルト設定でインストール
2. 「Git Bash Here」オプションを有効化

#### 確認
```powershell
# PowerShellで確認
git --version
```

### 3. Python（オプション）

#### ダウンロード
1. [Python公式サイト](https://www.python.org/downloads/windows/)にアクセス
2. Python 3.11以上をダウンロード
3. インストーラーを実行

#### インストール
1. 「Add Python to PATH」をチェック
2. 「Install for all users」を推奨

#### 確認
```powershell
# PowerShellで確認
python --version
pip --version
```

## 🚀 プロジェクトのセットアップ

### 1. プロジェクトのクローン

```powershell
# PowerShellで実行
git clone https://github.com/xth2brtwgt-wq/meeting-minutes-byc.git
cd meeting-minutes-byc
git checkout public
```

### 2. 環境変数ファイルの設定

```powershell
# 環境変数ファイルを作成
copy meeting-minutes-byc-dev\env.example meeting-minutes-byc-dev\.env

# ファイルを編集
notepad meeting-minutes-byc-dev\.env
```

### 3. 必要なAPIキーの設定

`.env`ファイルに以下のAPIキーを設定：

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

## 🐳 Docker Composeで起動

### 1. プロジェクトディレクトリに移動

```powershell
cd meeting-minutes-byc-dev
```

### 2. Docker Composeで起動

```powershell
# コンテナを起動
docker compose -f docker-compose.dev.yml up -d

# ログを確認
docker compose -f docker-compose.dev.yml logs -f
```

### 3. アプリケーションアクセス

```
http://localhost:5000
```

## 🔍 トラブルシューティング

### Docker Desktopが起動しない

```powershell
# WSL2の確認
wsl --list --verbose

# WSL2の更新
wsl --update
```

### ポートが使用中

```powershell
# ポート5000の使用状況確認
netstat -ano | findstr :5000

# プロセスを終了
taskkill /PID <PID> /F
```

### ファイル権限エラー

```powershell
# 管理者権限でPowerShellを実行
# または、Docker Desktopの設定でファイル共有を有効化
```

## 🎯 Windows固有の設定

### 1. ファイルパスの設定

```powershell
# 相対パスの使用
.\uploads
.\transcripts

# 絶対パスの使用
C:\path\to\project\uploads
```

### 2. 環境変数の設定

```powershell
# PowerShell
$env:GEMINI_API_KEY="your_api_key"

# コマンドプロンプト
set GEMINI_API_KEY=your_api_key

# システム環境変数（永続的）
[Environment]::SetEnvironmentVariable("GEMINI_API_KEY", "your_api_key", "User")
```

### 3. サービスとして実行

```powershell
# Windowsサービスとして登録（オプション）
# Docker Desktopの設定で「Start Docker Desktop when you log in」を有効化
```

## 📚 開発環境

### 1. ローカル開発

```powershell
# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
.\venv\Scripts\Activate.ps1

# 依存関係のインストール
pip install -r meeting-minutes-byc-dev\requirements.txt

# アプリケーションの起動
cd meeting-minutes-byc-dev
python app.py
```

### 2. VS Codeでの開発

```powershell
# VS Codeでプロジェクトを開く
code .
```

## 🔄 更新とメンテナンス

### 1. プロジェクトの更新

```powershell
# 最新のコードを取得
git pull origin public

# コンテナを再起動
docker compose -f docker-compose.dev.yml down
docker compose -f docker-compose.dev.yml up -d
```

### 2. ログの確認

```powershell
# コンテナのログを確認
docker compose -f docker-compose.dev.yml logs -f

# 特定のコンテナのログ
docker logs meeting-minutes-byc-dev
```

## 📞 サポート

### よくある問題

1. **Docker Desktopが起動しない**
   - WSL2の更新
   - 仮想化の有効化

2. **ポートが使用中**
   - 他のアプリケーションの終了
   - ポート番号の変更

3. **ファイル権限エラー**
   - 管理者権限での実行
   - Docker Desktopの設定確認

### 参考リンク

- [Docker Desktop for Windows](https://docs.docker.com/desktop/windows/)
- [Git for Windows](https://git-scm.com/download/win)
- [Python for Windows](https://www.python.org/downloads/windows/)

---

**作成者**: AI Assistant  
**プロジェクト**: Meeting Minutes BYC  
**最終更新**: 2025年10月15日
