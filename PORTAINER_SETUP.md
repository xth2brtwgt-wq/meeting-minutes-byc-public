# Portainer環境でのセットアップガイド

## 🔧 必要な情報

Portainer環境との整合性を取るために、以下の情報が必要です：

### 1. Portainerアクセス情報
```
Portainer URL: http://your_nas_ip:9000
管理者ユーザー名: adminuser
パスワード: Tsuj!19700308
```

### 2. 現在のDocker環境確認
以下のコマンドで現在の環境を確認してください：

```bash
# PortainerにSSH接続後
docker network ls
docker volume ls  
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

### 3. NASストレージ構成
```
データ保存先: /volume1/docker または /volume1/[共有フォルダ名]
共有フォルダ名: [例：docker, apps, data]
```

## 📋 確認手順

### Step 1: Portainerアクセス確認
1. ブラウザで `http://your_nas_ip:9000` にアクセス
2. 管理者アカウントでログイン
3. 現在のスタック・コンテナ・ネットワークを確認

### Step 2: 既存環境の確認
```bash
# SSH接続
ssh your_username@your_nas_ip

# 既存のネットワーク確認
docker network ls

# 既存のボリューム確認
docker volume ls

# 使用中のポート確認
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

### Step 3: ストレージ確認
```bash
# 共有フォルダの確認
ls -la /volume1/

# Docker関連ディレクトリの確認
ls -la /volume1/docker/
```

## 🛠️ 自動デプロイスクリプト

情報をいただければ、以下のスクリプトを実行して自動デプロイできます：

```bash
# スクリプトの実行
./docker/compose/portainer-deploy.sh
```

## 📝 手動設定手順

### 1. Portainerスタックの作成
1. Portainer管理画面にアクセス
2. "Stacks" → "Add stack" をクリック
3. スタック名: `audio-transcription`
4. `docker/compose/portainer-stack.yml` の内容をコピー&ペースト
5. "Deploy the stack" をクリック

### 2. ボリュームマウントの調整
`portainer-stack.yml` の以下の部分を実際の環境に合わせて調整：

```yaml
volumes:
  - /volume1/docker/audio-transcription/uploads:/tmp/uploads
  - /volume1/docker/audio-transcription/transcripts:/tmp/transcripts
  - /volume1/docker/audio-transcription/config:/app/meeting-minutes/config
```

### 3. ネットワーク設定の調整
既存のネットワークに合わせて調整：

```yaml
networks:
  docker_default:
    external: true  # 既存のネットワーク名に変更
```

## 🔍 トラブルシューティング

### よくある問題

1. **ポート競合**
   - 5000番ポートが既に使用されている場合
   - `ports` セクションでポート番号を変更

2. **ボリュームマウントエラー**
   - NASの共有フォルダパスが正しくない
   - 権限設定を確認

3. **ネットワーク接続エラー**
   - 既存のネットワーク名を確認
   - ネットワーク設定を調整

### ログ確認
```bash
# コンテナログの確認
docker logs audio-transcription-app

# Portainerでのログ確認
# Portainer管理画面 → Containers → audio-transcription-app → Logs
```

## 📊 監視・管理

### Portainerでの管理
- **Containers**: コンテナの状態監視
- **Images**: イメージの管理
- **Volumes**: ボリュームの管理
- **Networks**: ネットワークの管理

### アクセス方法
- **Webアプリケーション**: `http://your_nas_ip:5000`
- **Portainer管理画面**: `http://your_nas_ip:9000`

## 🔄 更新・メンテナンス

### アプリケーションの更新
1. 新しいイメージをビルド
2. Portainerでスタックを更新
3. または自動デプロイスクリプトを実行

### データバックアップ
```bash
# バックアップスクリプトの実行
python common/scripts/backup_data.py --action create --backup-name meeting_data
```

## 📞 サポート

設定で不明な点があれば、以下の情報と一緒にお知らせください：

1. Portainerの現在の設定
2. 既存のDocker環境
3. エラーメッセージ（ある場合）
4. 希望する設定変更
