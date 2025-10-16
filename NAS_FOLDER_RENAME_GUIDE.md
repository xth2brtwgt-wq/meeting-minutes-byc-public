# NASフォルダ名変更ガイド

## 概要
`meeting-minutes-byc-dev` → `meeting-minutes-byc` へのフォルダ名変更に伴うNAS側の対応手順です。

## 影響範囲

### 変更が必要な箇所
1. **アプリケーションディレクトリ**: `/home/AdminUser/meeting-minutes-byc-dev/` → `/home/AdminUser/meeting-minutes-byc/`
2. **データディレクトリ**: `/volume1/data/meeting-minutes-byc-dev/` → `/volume1/data/meeting-minutes-byc/`
3. **Dockerコンテナ名**: `meeting-minutes-byc-dev-app` → `meeting-minutes-byc-app`

## 対応手順

### ステップ1: 現在の状態確認

```bash
# NASにSSH接続
ssh AdminUser@192.168.68.110

# 現在のディレクトリを確認
ls -la /home/AdminUser/
ls -la /volume1/data/

# 実行中のコンテナを確認
sudo docker ps | grep meeting-minutes
```

### ステップ2: アプリケーションを停止

```bash
# コンテナを停止（現在のフォルダから実行）
cd /home/AdminUser/meeting-minutes-byc-dev/meeting-minutes-byc-dev
sudo docker compose down

# または、Portainerを使用している場合
# Portainer Web UIからStackを停止
```

### ステップ3: フォルダ名変更

#### 方法A: リネーム（推奨 - データを保持）

```bash
# アプリケーションディレクトリをリネーム
cd /home/AdminUser/
mv meeting-minutes-byc-dev meeting-minutes-byc

# データディレクトリをリネーム（存在する場合）
sudo mv /volume1/data/meeting-minutes-byc-dev /volume1/data/meeting-minutes-byc

# 権限を確認
sudo chown -R AdminUser:admin /home/AdminUser/meeting-minutes-byc
sudo chown -R AdminUser:admin /volume1/data/meeting-minutes-byc
```

#### 方法B: 再cloneとデータ移行（クリーンな環境が必要な場合）

```bash
# 古いディレクトリをバックアップ
cd /home/AdminUser/
mv meeting-minutes-byc-dev meeting-minutes-byc-dev-backup

# 新しくclone
git clone https://github.com/xth2brtwgt-wq/meeting-minutes-byc.git meeting-minutes-byc
cd meeting-minutes-byc/meeting-minutes-byc

# 環境設定ファイルをコピー
cp /home/AdminUser/meeting-minutes-byc-dev-backup/meeting-minutes-byc-dev/.env .env

# データディレクトリをリネーム
sudo mv /volume1/data/meeting-minutes-byc-dev /volume1/data/meeting-minutes-byc

# 権限設定
sudo chown -R AdminUser:admin /home/AdminUser/meeting-minutes-byc
sudo chown -R AdminUser:admin /volume1/data/meeting-minutes-byc
```

### ステップ4: Gitリポジトリを最新化（方法Aの場合）

```bash
cd /home/AdminUser/meeting-minutes-byc/meeting-minutes-byc

# 最新のコミットを取得
git fetch origin
git pull origin main
```

### ステップ5: docker-compose.ymlの確認

```bash
cd /home/AdminUser/meeting-minutes-byc/meeting-minutes-byc

# docker-compose.ymlを確認（コンテナ名やボリュームパスが正しいか）
cat docker-compose.yml

# または docker-compose.dev.yml を使用している場合
cat docker-compose.dev.yml
```

**確認ポイント:**
- コンテナ名が `meeting-minutes-byc` になっているか
- ボリュームパスが `/volume1/data/meeting-minutes-byc/` になっているか

### ステップ6: アプリケーションを起動

```bash
cd /home/AdminUser/meeting-minutes-byc/meeting-minutes-byc

# Dockerイメージを再ビルド（必要に応じて）
sudo docker compose build

# コンテナを起動
sudo docker compose up -d

# ログを確認
sudo docker compose logs -f
```

### ステップ7: 動作確認

```bash
# コンテナの状態確認
sudo docker ps | grep meeting-minutes

# ヘルスチェック
curl http://192.168.68.110:5001/health

# ブラウザでアクセス
# http://192.168.68.110:5001/
```

### ステップ8: クリーンアップ（成功確認後）

```bash
# バックアップフォルダを削除（方法Bの場合のみ）
sudo rm -rf /home/AdminUser/meeting-minutes-byc-dev-backup

# 古いDockerイメージを削除（オプション）
sudo docker images | grep meeting-minutes-byc-dev
sudo docker rmi <IMAGE_ID>
```

## Portainerを使用している場合

### Stackの更新

1. **Portainer Web UIにアクセス**
   - http://192.168.68.110:9000/

2. **既存のStackを停止**
   - Stacks → 既存のStack → Stop

3. **Stackを削除または更新**
   - オプションA: Stackを削除して再作成
   - オプションB: Stack定義を編集（コンテナ名やボリュームパスを更新）

4. **新しいStackをデプロイ**
   - Repository: `https://github.com/xth2brtwgt-wq/meeting-minutes-byc.git`
   - Compose path: `meeting-minutes-byc/docker-compose.yml`

## トラブルシューティング

### コンテナが起動しない

```bash
# ログを確認
sudo docker compose logs

# ポートの競合を確認
sudo netstat -tulpn | grep 5001

# 古いコンテナが残っている場合は削除
sudo docker ps -a | grep meeting-minutes-byc-dev
sudo docker rm -f <CONTAINER_ID>
```

### データが見つからない

```bash
# データディレクトリの確認
ls -la /volume1/data/meeting-minutes-byc/

# 権限の確認と修正
sudo chown -R AdminUser:admin /volume1/data/meeting-minutes-byc/
sudo chmod -R 755 /volume1/data/meeting-minutes-byc/
```

### 環境変数が引き継がれていない

```bash
# .envファイルの確認
cd /home/AdminUser/meeting-minutes-byc/meeting-minutes-byc
cat .env

# 必要に応じて、旧ディレクトリから.envをコピー
# cp /home/AdminUser/meeting-minutes-byc-dev-backup/meeting-minutes-byc-dev/.env .env
```

## 推奨対応フロー

**最も安全な方法:**

1. **停止** → Dockerコンテナを停止
2. **バックアップ** → データとアプリディレクトリをバックアップ
3. **リネーム** → フォルダ名を変更（方法A）
4. **Pull** → 最新のコードを取得
5. **起動** → コンテナを起動
6. **確認** → 動作確認

所要時間: 約5-10分

## 注意事項

- 作業前に必ずバックアップを取ってください
- 実行中のトランスクリプション処理がある場合は完了を待ってから停止してください
- データディレクトリ（`/volume1/data/`）のリネームは慎重に行ってください
- Portainer Stackを使用している場合は、Stack定義も更新が必要です

## 確認コマンド集

```bash
# 全体の状況確認
echo "=== Application Directory ==="
ls -la /home/AdminUser/ | grep meeting-minutes

echo "=== Data Directory ==="
ls -la /volume1/data/ | grep meeting-minutes

echo "=== Docker Containers ==="
sudo docker ps -a | grep meeting-minutes

echo "=== Docker Images ==="
sudo docker images | grep meeting-minutes

echo "=== Current Working Directory ==="
pwd
```

