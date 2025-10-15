# NAS プロジェクト構造

## 📁 プロジェクト全体構造

```
nas-project/
├── 📁 common/                    # 共通モジュール・スクリプト
│   ├── 📁 utils/                 # 共通ユーティリティ
│   │   ├── __init__.py          # パッケージ初期化
│   │   ├── file_utils.py        # ファイル操作ユーティリティ
│   │   ├── audio_utils.py       # 音声処理ユーティリティ
│   │   ├── text_utils.py        # テキスト処理ユーティリティ
│   │   └── config_utils.py      # 設定管理ユーティリティ
│   └── 📁 scripts/              # 共通スクリプト
│       ├── __init__.py          # パッケージ初期化
│       ├── setup_nas.py         # NAS環境セットアップスクリプト
│       └── backup_data.py       # データバックアップスクリプト
│
├── 📁 meeting-minutes/           # 議事録作成アプリケーション
│   ├── 📁 app/                  # アプリケーション本体
│   │   └── app.py              # メインアプリケーション（Flask）
│   ├── 📁 templates/            # HTMLテンプレート
│   │   └── index.html          # メインWebページ
│   ├── 📁 config/              # 設定ファイル
│   │   ├── app.json            # アプリケーション設定
│   │   ├── whisper.json        # Whisper設定
│   │   ├── audio.json          # 音声処理設定
│   │   ├── storage.json        # ストレージ設定
│   │   └── logging.json        # ログ設定
│   ├── 📁 data/                # データディレクトリ
│   │   ├── uploads/            # アップロードされた音声ファイル
│   │   └── transcripts/        # 文字起こし結果
│   └── requirements.txt        # Python依存関係
│
├── 📁 docker/                   # Docker関連ファイル
│   ├── Dockerfile              # Dockerイメージ定義
│   └── 📁 compose/             # Docker Compose設定
│       └── docker-compose.yml  # サービス定義
│
├── 📁 docs/                     # ドキュメント（将来拡張用）
│
├── README.md                    # プロジェクト概要
├── PROJECT_STRUCTURE.md         # このファイル
└── .devcontainer/               # VS Code開発環境設定
    ├── devcontainer.json
    └── Dockerfile
```

## 🔧 各モジュールの役割

### Common モジュール

#### `common/utils/`
- **`file_utils.py`**: ファイル操作、ハッシュ生成、JSON保存/読み込み
- **`audio_utils.py`**: 音声ファイル検証、正規化、言語検出
- **`text_utils.py`**: テキスト処理、議事録生成、キーワード抽出
- **`config_utils.py`**: 設定ファイル管理、環境変数読み込み

#### `common/scripts/`
- **`setup_nas.py`**: NAS環境の自動セットアップ
- **`backup_data.py`**: データのバックアップ・復元

### Meeting Minutes アプリケーション

#### `meeting-minutes/app/`
- **`app.py`**: Flask Webアプリケーション
  - 音声ファイルアップロード
  - Whisper文字起こし
  - 議事録生成
  - 履歴管理

#### `meeting-minutes/config/`
- **`app.json`**: アプリケーション基本設定
- **`whisper.json`**: Whisperモデル設定
- **`audio.json`**: 音声処理設定
- **`storage.json`**: ファイル保存設定
- **`logging.json`**: ログ設定

## 🚀 使用方法

### 1. ローカル開発
```bash
cd meeting-minutes
pip install -r requirements.txt
python app/app.py
```

### 2. Docker実行
```bash
cd docker/compose
docker-compose up -d
```

### 3. NAS環境セットアップ
```bash
python common/scripts/setup_nas.py --nas-ip your_nas_ip --username your_username
```

### 4. データバックアップ
```bash
python common/scripts/backup_data.py --action create --backup-name meeting_data
```

## 🔄 拡張性

### 新しいアプリケーションの追加
1. `meeting-minutes/` と同様の構造で新しいフォルダを作成
2. `common/utils/` の機能を活用
3. `docker/compose/` に新しいサービスを追加

### 共通機能の追加
1. `common/utils/` に新しいユーティリティを追加
2. `common/scripts/` に新しいスクリプトを追加
3. 各アプリケーションからインポートして使用

## 📋 設定管理

### 環境変数
- `FLASK_HOST`: アプリケーションのホスト
- `FLASK_PORT`: アプリケーションのポート
- `WHISPER_MODEL`: 使用するWhisperモデル
- `UPLOAD_DIR`: アップロードディレクトリ
- `TRANSCRIPT_DIR`: 文字起こし結果ディレクトリ

### 設定ファイル
各アプリケーションの `config/` ディレクトリでJSON形式で管理

## 🔒 セキュリティ

- ファイルアップロード時の検証
- 安全なファイル名生成
- 古いファイルの自動削除
- 設定ファイルの適切な管理

## 📊 監視・ログ

- 構造化ログ出力
- エラーハンドリング
- パフォーマンス監視
- データバックアップ機能

