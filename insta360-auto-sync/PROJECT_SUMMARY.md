# Insta360自動同期システム - プロジェクト完了サマリー

## プロジェクト概要

Insta360カメラで撮影したファイルをMacからNASへ自動バックアップするシステムを構築しました。

**プロジェクト期間**: 2025年10月16日  
**ステータス**: ✅ 完了・稼働中

## 実装内容

### ✅ 完了した機能

1. **ファイル自動バックアップ機能**
   - Insta360ファイルの自動検出（`VID_*.mp4`, `*.insv`, `*.insp`, `*.jpg`, `*.dng`, `*.raw`）
   - Mac → NASへの自動転送
   - **元ファイル保持**（即座に削除しない）
   - コピー成功/失敗の詳細ログ

2. **定期実行機能**
   - **NAS側**: 毎日深夜0時（JST）に自動バックアップ
   - **Mac側**: 毎週日曜日午前2時に古いファイル削除（30日以上前）
   - Dockerコンテナによるスケジューリング
   - Mac側はcronによるスケジューリング

3. **メール通知機能**
   - 転送完了通知（成功件数、失敗件数）
   - エラー通知
   - 詳細な転送レポート
   - Gmailアプリパスワード対応

4. **SMBマウント機能**
   - Mac共有フォルダの自動マウント
   - 接続エラーハンドリング
   - マウントポイント: `/mnt/mac-share`

5. **設定管理機能**
   - JSON形式の設定ファイル（`config/app.json`）
   - 環境変数による設定（`.env`）
   - 削除有無の切り替え可能（`delete_source: false`）

6. **ログ管理機能**
   - 詳細なログ記録
   - NAS側: Dockerログ
   - Mac側: 削除ログ（`logs/cleanup.log`）

7. **Docker化**
   - Alpine Linuxベースの軽量イメージ
   - 自動再起動設定（`restart: unless-stopped`）
   - rootユーザーで実行（ファイル操作権限）
   - ヘルスチェック機能

## システム構成

### ディレクトリ構造

```
insta360-auto-sync/
├── README.md                 # プロジェクト概要
├── PROJECT_SUMMARY.md        # このファイル
├── deploy.sh                 # デプロイスクリプト
├── docker-compose.yml        # Docker Compose設定
├── Dockerfile               # Dockerイメージ定義
├── requirements.txt         # Python依存関係
├── env.example             # 環境変数設定例
├── config/                 # 設定ファイル
│   ├── app.json           # アプリケーション設定
│   └── email.json         # メール設定
├── scripts/               # 実行スクリプト
│   ├── sync.py           # メイン同期スクリプト
│   ├── mount_mac.sh      # Macマウントスクリプト
│   ├── test_connection.py # 接続テストスクリプト
│   ├── setup_cron.sh     # cron設定スクリプト
│   └── run_scheduler.py  # スケジューラー
├── utils/                 # ユーティリティ
│   ├── email_sender.py   # メール送信
│   ├── file_utils.py     # ファイル操作
│   └── config_utils.py   # 設定管理
├── docs/                  # ドキュメント
│   ├── setup.md          # セットアップ手順
│   └── operation.md      # 運用手順
└── logs/                  # ログファイル（実行時に作成）
```

### 技術スタック

- **言語**: Python 3.12
- **コンテナ**: Docker, Docker Compose
- **OS**: Alpine Linux
- **スケジューリング**: cron
- **メール**: SMTP (Gmail)
- **ファイル共有**: SMB/CIFS

## 共通化された機能

既存の議事録システムから以下の機能を共通化して活用：

1. **メール送信機能** (`EmailSender`クラス)
   - SMTP設定の統一
   - エラーハンドリングの統一
   - ログ出力の統一

2. **設定管理機能** (`ConfigManager`クラス)
   - JSON設定ファイルの読み込み
   - 環境変数との連携
   - 設定値の動的取得

3. **ログ管理機能**
   - 統一されたログフォーマット
   - ファイル出力とコンソール出力
   - ログローテーション

## 対応ファイル形式

- **動画**: `.mp4`, `.insv`, `.insp`
- **画像**: `.jpg`, `.dng`, `.raw`

## 主要な改善点

1. **エラーハンドリングの強化**
   - 詳細なエラーメッセージ
   - リトライ機能
   - エラー通知の自動化

2. **設定の柔軟性向上**
   - 環境変数による設定
   - 設定ファイルの分離
   - 動的な設定変更

3. **運用性の向上**
   - 詳細なログ出力
   - 接続テスト機能
   - 手動実行機能

4. **セキュリティの強化**
   - パスワードの環境変数管理
   - ファイル権限の適切な設定
   - ログファイルの保護

## デプロイ手順

1. **環境準備**
   ```bash
   cd /home/AdminUser/nas-project/insta360-auto-sync
   ```

2. **設定ファイルの準備**
   ```bash
   cp env.example .env
   # .envファイルを編集して実際の値を設定
   ```

3. **デプロイ実行**
   ```bash
   ./deploy.sh
   ```

4. **動作確認**
   ```bash
   docker-compose exec insta360-auto-sync python3 /app/scripts/test_connection.py
   ```

## 本番環境設定

### Mac側
- **IPアドレス**: 192.168.68.88（有線接続）
- **共有フォルダ**: Insta360（`/Users/Yoshi/Movies/Insta360`）
- **SMB共有**: 有効、ユーザー: Admin
- **cron設定**: 毎週日曜日 02:00に古いファイル削除

### NAS側
- **マウントポイント**: `/mnt/mac-share`
- **バックアップ先**: `/volume2/data/insta360`
- **Docker実行**: rootユーザー
- **スケジュール**: 毎日 00:00にバックアップ

## 運用開始後の確認事項

- [x] Mac側のSMB共有が有効
- [x] NAS側のDockerが動作中
- [x] 環境変数が正しく設定
- [x] 接続テストが成功
- [x] メール通知が正常に送信（Gmailアプリパスワード設定済み）
- [x] 手動実行テストが成功
- [x] 定期実行が正常に動作
- [x] Mac側のcron設定が完了
- [x] ファイル削除をスキップする設定が有効（`delete_source: false`）

## 今後の拡張予定

### 短期（必要に応じて）
- ファイルサイズ制限の追加
- 重複ファイルチェック機能
- バックアップ履歴の可視化

### 中期（3ヶ月以内）
- ファイルタイプ別整理
- 日付別フォルダ整理
- 容量監視機能

### 長期（6ヶ月以降）
- Webダッシュボード
- 自動バックアップの多重化
- サムネイル自動生成

## トラブルシューティング

問題が発生した場合は、以下の順序で確認してください：

1. **ログファイルの確認**
   ```bash
   tail -f logs/insta360_sync.log
   ```

2. **接続テストの実行**
   ```bash
   docker-compose exec insta360-auto-sync python3 /app/scripts/test_connection.py
   ```

3. **手動実行テスト**
   ```bash
   docker-compose exec insta360-auto-sync python3 /app/scripts/sync.py --test
   ```

4. **コンテナの再起動**
   ```bash
   docker-compose restart insta360-auto-sync
   ```

## 連絡先

- **開発者**: Yoshi
- **システム管理者**: AdminUser
- **ドキュメント**: `docs/`ディレクトリ内の各ファイルを参照

---

**プロジェクト完了日**: 2025年1月15日  
**バージョン**: 1.0.0  
**ステータス**: 本格運用準備完了
