# Portainer手動セットアップガイド

## 🔧 現在の状況
- **Portainer URL**: http://192.168.68.110:9000
- **ユーザー**: adminuser
- **パスワード**: Tsuj!19700308
- **Docker権限**: AdminUserでDockerコマンド実行時に権限エラー

## 📋 手動セットアップ手順

### Step 1: Docker権限の修正

SSH接続で以下のコマンドを実行：

```bash
# AdminUserをdockerグループに追加
sudo usermod -aG docker AdminUser

# Dockerサービスを再起動
sudo systemctl restart docker

# SSH接続を一度切断して再接続
exit
```

再接続後、権限を確認：
```bash
ssh AdminUser@192.168.68.110
docker ps
```

### Step 2: プロジェクトファイルのアップロード

ローカルからNASにファイルを転送：

```bash
# プロジェクト全体をアップロード
scp -r /Users/Yoshi/nas-project AdminUser@192.168.68.110:/volume1/docker/

# または rsync を使用（推奨）
rsync -avz --progress /Users/Yoshi/nas-project/ AdminUser@192.168.68.110:/volume1/docker/nas-project/
```

### Step 3: 必要なディレクトリの作成

NAS上で以下のディレクトリを作成：

```bash
ssh AdminUser@192.168.68.110

# 必要なディレクトリを作成
sudo mkdir -p /volume1/docker/audio-transcription/{uploads,transcripts,config,logs}
sudo chown -R AdminUser:AdminUser /volume1/docker/audio-transcription
```

### Step 4: Portainerでのスタック作成

1. **Portainer管理画面にアクセス**
   - URL: http://192.168.68.110:9000
   - ユーザー: adminuser
   - パスワード: Tsuj!19700308

2. **スタックの作成**
   - "Stacks" → "Add stack" をクリック
   - スタック名: `audio-transcription`
   - Web editor を選択

3. **スタック定義の入力**
   `docker/compose/portainer-stack.yml` の内容をコピー&ペースト

4. **デプロイ**
   - "Deploy the stack" をクリック

### Step 5: 動作確認

1. **コンテナの状態確認**
   - Portainer → Containers → audio-transcription-app
   - ステータスが "Running" であることを確認

2. **Webアプリケーションのアクセス**
   - URL: http://192.168.68.110:5000
   - 音声ファイルアップロード機能をテスト

3. **ログの確認**
   - Portainer → Containers → audio-transcription-app → Logs
   - エラーがないことを確認

## 🔍 トラブルシューティング

### Docker権限エラーの場合
```bash
# 権限を再確認
groups AdminUser

# dockerグループに追加されていない場合
sudo usermod -aG docker AdminUser
newgrp docker
```

### ポート競合の場合
- 5000番ポートが使用中の場合、`portainer-stack.yml` でポート番号を変更
- 例: `"5001:5000"` に変更

### ボリュームマウントエラーの場合
```bash
# ディレクトリの権限を確認
ls -la /volume1/docker/audio-transcription/

# 権限を修正
sudo chown -R AdminUser:AdminUser /volume1/docker/audio-transcription
sudo chmod -R 755 /volume1/docker/audio-transcription
```

### ビルドエラーの場合
```bash
# 手動でイメージをビルド
cd /volume1/docker/nas-project
docker build -f docker/Dockerfile -t audio-transcription:latest .
```

## 📊 監視・管理

### Portainerでの管理項目
- **Containers**: コンテナの状態監視
- **Images**: イメージの管理
- **Volumes**: ボリュームの管理
- **Networks**: ネットワークの管理
- **Logs**: アプリケーションログの確認

### アクセス方法
- **Webアプリケーション**: http://192.168.68.110:5000
- **Portainer管理画面**: http://192.168.68.110:9000

## 🔄 更新・メンテナンス

### アプリケーションの更新
1. 新しいコードをNASにアップロード
2. Portainerでスタックを再デプロイ
3. または手動でイメージを再ビルド

### データバックアップ
```bash
# バックアップスクリプトの実行
cd /volume1/docker/nas-project
python common/scripts/backup_data.py --action create --backup-name meeting_data
```

## 📞 サポート

問題が発生した場合は、以下の情報と一緒にお知らせください：

1. エラーメッセージの詳細
2. Portainerのログ
3. コンテナの状態
4. 実行したコマンド
