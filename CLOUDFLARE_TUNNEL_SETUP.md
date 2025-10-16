# Cloudflare Tunnel 設定ガイド（初心者向け）

## 🎯 このガイドのゴール

**NASのアプリに独自ドメインでHTTPSアクセスできるようにします！**

```
Before: http://192.168.68.110:5000/ （家の中だけ）
After:  https://meeting-minutes.yourdomain.com/ （どこからでもアクセス可能！）
```

## 📋 必要なもの

1. ✅ NAS（UGREEN DXP2800）- 既にある
2. ✅ Cloudflareアカウント（無料）- これから作る
3. ✅ ドメイン名 - 無料または有料

**所要時間: 30分～1時間**  
**難易度: ⭐⭐☆☆☆（中級）**  
**コスト: 無料～年1,000円程度**

---

## ステップ1: ドメインを準備する（10分）

### オプションA: 無料ドメインを使う（おすすめ）

#### Freenom（完全無料）
1. https://www.freenom.com/ にアクセス
2. 好きなドメイン名を検索（例: `my-meeting-minutes`）
3. `.tk`, `.ml`, `.ga`, `.cf`, `.gq` から選択（全て無料）
4. アカウント作成して取得

**例:** `my-meeting-minutes.tk`

### オプションB: 有料ドメインを買う（推奨）

#### お名前.com（日本語対応）
1. https://www.onamae.com/ にアクセス
2. ドメイン検索（例: `meeting-minutes.com`）
3. `.com` なら年1,000円程度
4. 購入

**例:** `meeting-minutes.com`

---

## ステップ2: Cloudflareアカウント作成（5分）

### 2-1. アカウント登録

1. https://dash.cloudflare.com/sign-up にアクセス

2. メールアドレスとパスワードを入力して登録
   ```
   メール: your-email@example.com
   パスワード: 強固なパスワード
   ```

3. メールアドレス確認
   - 届いたメールのリンクをクリック

### 2-2. ドメインを追加

1. Cloudflareダッシュボードにログイン

2. 「サイトを追加」をクリック

3. 取得したドメイン名を入力
   ```
   例: my-meeting-minutes.tk
   または meeting-minutes.com
   ```

4. プランを選択
   - **「Freeプラン」を選択**（無料でOK！）

5. 「次へ」をクリック

### 2-3. DNSレコードをスキャン

- Cloudflareが自動的にDNSレコードをスキャンします
- そのまま「次へ」をクリック

### 2-4. ネームサーバーを変更

**重要なステップです！**

1. Cloudflareが2つのネームサーバーを表示します：
   ```
   例:
   carter.ns.cloudflare.com
   josie.ns.cloudflare.com
   ```

2. これをメモしておきます

3. ドメイン取得元のサイトに戻ります

#### Freenomの場合
1. Freenom → Services → My Domains
2. 該当ドメインの「Manage Domain」をクリック
3. 「Management Tools」→「Nameservers」
4. 「Use custom nameservers」を選択
5. Cloudflareのネームサーバー2つを入力
6. 「Change Nameservers」をクリック

#### お名前.comの場合
1. お名前.com Naviにログイン
2. 「ドメイン設定」→「ネームサーバーの設定」
3. 「他のネームサーバーを利用」を選択
4. Cloudflareのネームサーバー2つを入力
5. 「確認」→「OK」

### 2-5. 確認を待つ

- ネームサーバーの変更には**最大24時間**かかる場合があります
- 通常は**数時間～1時間**で完了します
- Cloudflareからメールが届いたら完了です

---

## ステップ3: Cloudflare Tunnelをセットアップ（10分）

### 3-1. Zero Trust設定

1. Cloudflareダッシュボードで左メニューから「Zero Trust」をクリック

2. 初回のみ：組織名を入力
   ```
   例: My Organization
   ```

3. プランを選択
   - **「Free」を選択**

### 3-2. Tunnelを作成

1. 左メニュー → 「Access」 → 「Tunnels」

2. 「Create a tunnel」をクリック

3. Tunnel名を入力
   ```
   例: meeting-minutes-tunnel
   ```

4. 「Save tunnel」をクリック

5. **次の画面で表示される「Token」をメモ**
   ```
   例: eyJhIjoixxxxxxxxxxxxxxx...
   ```
   このTokenは後で使います！

---

## ステップ4: NAS側の設定（10分）

### 4-1. cloudflaredのインストール

NASにSSH接続します：

```bash
ssh AdminUser@192.168.68.110
```

cloudflaredをインストール：

```bash
# 最新版をダウンロード
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb

# インストール
sudo dpkg -i cloudflared.deb

# 確認
cloudflared --version
```

### 4-2. Tunnelを起動

ステップ3-2でメモした**Token**を使います：

```bash
# Tokenを使ってTunnelを起動（実際のTokenに置き換えてください）
sudo cloudflared service install eyJhIjoixxxxxxxxxxxxxxx...
```

### 4-3. サービスを開始

```bash
# サービス開始
sudo systemctl start cloudflared

# 自動起動を有効化
sudo systemctl enable cloudflared

# ステータス確認（正常に動作しているか）
sudo systemctl status cloudflared
```

**正常な場合の表示:**
```
● cloudflared.service
   Active: active (running)
```

---

## ステップ5: ルーティング設定（5分）

### 5-1. Cloudflareダッシュボードに戻る

1. Cloudflare Zero Trust → Tunnels
2. 作成したTunnel（`meeting-minutes-tunnel`）をクリック

### 5-2. Public Hostnameを設定

1. 「Public Hostname」タブをクリック

2. 「Add a public hostname」をクリック

3. 以下のように入力：

| 項目 | 入力内容 | 例 |
|------|---------|-----|
| **Subdomain** | meeting-minutes | meeting-minutes |
| **Domain** | yourdomain.com | my-meeting-minutes.tk |
| **Path** | （空白） | （空白） |
| **Type** | HTTP | HTTP |
| **URL** | localhost:5000 | localhost:5000 |

4. 「Save hostname」をクリック

### 完成！

これで完了です！以下のURLでアクセスできるようになります：

```
https://meeting-minutes.yourdomain.com/
```

例: `https://meeting-minutes.my-meeting-minutes.tk/`

---

## 🎉 動作確認

### 1. 外部からアクセス

スマホのモバイルデータ通信（Wi-Fiオフ）で以下にアクセス：

```
https://meeting-minutes.yourdomain.com/
```

### 2. HTTPS確認

- ブラウザのアドレスバーに🔒マークが表示されていればOK！
- クリックすると証明書情報が見られます

### 3. 機能テスト

- ファイルアップロードができるか
- 文字起こしが動作するか
- 辞書管理が使えるか

---

## 🔧 トラブルシューティング

### 問題1: 「このサイトにアクセスできません」

#### 原因と解決策

**原因1: ネームサーバーがまだ反映されていない**
```bash
# 反映確認コマンド（ローカルPC/Macで実行）
nslookup meeting-minutes.yourdomain.com

# Cloudflareのネームサーバーが表示されればOK
```
→ 待つしかありません（最大24時間）

**原因2: cloudflaredが起動していない**
```bash
# NASで確認
sudo systemctl status cloudflared

# 起動していない場合
sudo systemctl start cloudflared
```

**原因3: ポート番号が間違っている**
- Cloudflareダッシュボードで `localhost:5000` になっているか確認

### 問題2: 502 Bad Gateway

#### 原因と解決策

**原因: NAS側のアプリが起動していない**
```bash
# NASでアプリの状態確認
sudo docker ps | grep meeting-minutes

# 起動していない場合
cd /home/AdminUser/meeting-minutes-byc
sudo docker compose -f docker-compose.dev.yml up -d
```

### 問題3: SSL証明書のエラー

#### 解決策

- Cloudflareの設定で「SSL/TLS」→「Overview」
- 「Flexible」または「Full」を選択
- **「Full (strict)」は使わないでください**

---

## 🛡️ セキュリティ設定（推奨）

### 1. アクセス制限を追加

#### メールアドレスでアクセス制限

1. Cloudflare Zero Trust → Access → Applications

2. 「Add an application」をクリック

3. 「Self-hosted」を選択

4. 設定：
   ```
   Application name: Meeting Minutes
   Subdomain: meeting-minutes
   Domain: yourdomain.com
   ```

5. ポリシー追加：
   ```
   Policy name: Email Auth
   Action: Allow
   Include: Emails ending in @yourdomain.com
   ```

6. 保存

これで、指定したメールアドレスのみアクセス可能になります！

### 2. IPアドレス制限

自宅と会社のIPアドレスのみ許可：

1. Access → Applications → 該当アプリ編集

2. ポリシーに追加：
   ```
   Include: IP ranges
   IP ranges: 
     - 自宅のIPアドレス
     - 会社のIPアドレス
   ```

---

## 💡 便利な機能

### 1. 複数のアプリを公開

他のアプリも同じTunnelで公開できます：

```
https://app1.yourdomain.com/ → localhost:5000
https://app2.yourdomain.com/ → localhost:8080
https://nas.yourdomain.com/ → localhost:5001
```

### 2. カスタムエラーページ

1. Zero Trust → Settings → Custom pages
2. エラーページをカスタマイズ

### 3. アクセスログの確認

1. Zero Trust → Logs → Access
2. 誰がいつアクセスしたかわかります

---

## 📊 料金について

### 無料プラン（Free）でできること

- ✅ 無制限のTunnel
- ✅ 無制限のPublic Hostname
- ✅ DDoS保護
- ✅ SSL/TLS証明書（自動更新）
- ✅ 最大50ユーザー
- ✅ 月1GBのログ保存

**個人利用なら完全に無料で十分！**

---

## 🔄 メンテナンス

### アップデート

```bash
# cloudflaredのアップデート
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb
sudo systemctl restart cloudflared
```

### ログ確認

```bash
# ログを見る
sudo journalctl -u cloudflared -f

# 最新100行を表示
sudo journalctl -u cloudflared -n 100
```

### Tunnel再起動

```bash
sudo systemctl restart cloudflared
```

---

## 📱 スマホでのアクセス

### ホーム画面に追加

#### iPhone
1. Safariで `https://meeting-minutes.yourdomain.com/` を開く
2. 共有ボタン → 「ホーム画面に追加」
3. アプリのように使えます！

#### Android
1. Chromeで `https://meeting-minutes.yourdomain.com/` を開く
2. メニュー → 「ホーム画面に追加」

---

## ❓ FAQ

### Q1: 無料で本当に使い続けられる？
**A:** はい！Cloudflareは無料プランをずっと提供しています。

### Q2: 速度は遅くならない？
**A:** Cloudflareは世界中にCDNがあるので、むしろ速くなることが多いです。

### Q3: ドメイン名を変更できる？
**A:** はい、Public Hostnameの設定を変更するだけです。

### Q4: 複数のサブドメインを使える？
**A:** はい！無制限に追加できます。

### Q5: 他の人と共有できる？
**A:** はい！URLを教えるだけ。アクセス制限も設定できます。

---

## 🆚 Tailscale vs Cloudflare Tunnel

| 項目 | Tailscale | Cloudflare Tunnel |
|------|-----------|-------------------|
| 設定の簡単さ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| セキュリティ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| アクセス方法 | アプリ必要 | ブラウザのみ |
| URL | IP直接 | 独自ドメイン |
| 共有のしやすさ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 無料範囲 | 個人利用 | 個人利用 |

**結論:**
- **自分だけが使う**: Tailscaleが簡単
- **他の人とも共有**: Cloudflare Tunnelが便利

---

## 🎓 まとめ

### ✅ できるようになったこと

1. 世界中どこからでもアクセス可能
2. HTTPS暗号化で安全
3. 独自ドメインでプロフェッショナル
4. ポート開放不要
5. 完全無料（または年1,000円のドメイン代のみ）

### 🚀 次のステップ

- [ ] アクセス制限を追加
- [ ] 他のアプリも公開
- [ ] カスタムエラーページ設定
- [ ] アクセスログの定期確認

---

## 🆘 困ったときは

1. このドキュメントのトラブルシューティングを確認
2. Cloudflare公式ドキュメント: https://developers.cloudflare.com/
3. GitHubのIssueで質問

**頑張ってください！設定が完了したら素晴らしい体験が待っています！** 🎉

