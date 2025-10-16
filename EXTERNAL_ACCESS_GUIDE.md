# 外部アクセス設定ガイド

## 概要
NAS上のMeeting Minutes BYCアプリケーションに外部（インターネット経由）からアクセスする方法を説明します。

## ⚠️ セキュリティの重要性

外部アクセスを設定する前に、以下のセキュリティリスクを理解してください：

- **未承認アクセスのリスク**: 適切に設定しないと、誰でもアクセス可能になります
- **データ漏洩のリスク**: 音声ファイルや議事録が外部に漏れる可能性
- **攻撃のリスク**: DDoS攻撃やハッキングの標的になる可能性

**推奨**: 必ずVPNまたは認証機能を実装してください。

## 方法の比較

| 方法 | セキュリティ | 難易度 | コスト | 推奨度 |
|------|------------|--------|--------|---------|
| **VPN** | ⭐⭐⭐⭐⭐ | 中 | 無料 | ⭐⭐⭐⭐⭐ |
| **Cloudflare Tunnel** | ⭐⭐⭐⭐⭐ | 低 | 無料 | ⭐⭐⭐⭐⭐ |
| **Tailscale** | ⭐⭐⭐⭐⭐ | 低 | 無料 | ⭐⭐⭐⭐⭐ |
| **ポートフォワーディング + HTTPS** | ⭐⭐⭐ | 中 | 有料 | ⭐⭐⭐ |
| **ポートフォワーディングのみ** | ⭐ | 低 | 無料 | ❌ 非推奨 |

---

## 🌟 推奨方法

### 方法1: Tailscale（最も簡単で安全）

**メリット:**
- ✅ 設定が非常に簡単
- ✅ 完全に暗号化
- ✅ ポート開放不要
- ✅ 無料プラン（個人利用なら十分）
- ✅ クロスプラットフォーム対応

**デメリット:**
- 各デバイスにTailscaleアプリが必要

#### 設定手順

##### 1. Tailscaleアカウント作成
1. https://tailscale.com/ にアクセス
2. アカウント作成（Googleアカウントで簡単登録）

##### 2. NAS側設定
```bash
# NASにSSH接続
ssh AdminUser@192.168.68.110

# Tailscaleインストール
curl -fsSL https://tailscale.com/install.sh | sh

# Tailscale起動（認証URLが表示されます）
sudo tailscale up

# 表示されたURLをブラウザで開いて認証

# Tailscale IPアドレスを確認
tailscale ip -4
# 例: 100.x.x.x が表示されます
```

##### 3. クライアント側設定
1. スマホ/PCにTailscaleアプリをインストール
   - [iOS](https://apps.apple.com/app/tailscale/id1470499037)
   - [Android](https://play.google.com/store/apps/details?id=com.tailscale.ipn)
   - [Windows/Mac](https://tailscale.com/download)

2. 同じアカウントでログイン

3. アクセス
   ```
   http://100.x.x.x:5000/
   （NASのTailscale IPアドレス）
   ```

---

### 方法2: Cloudflare Tunnel（無料で簡単）

**メリット:**
- ✅ 完全無料
- ✅ ポート開放不要
- ✅ 自動HTTPS化
- ✅ DDoS保護
- ✅ カスタムドメイン対応

**デメリット:**
- Cloudflareアカウントが必要
- ドメインが必要（無料のものでも可）

#### 設定手順

##### 1. Cloudflareアカウント作成
1. https://www.cloudflare.com/ でアカウント作成
2. ドメインを追加（持っていない場合は無料サービスで取得可能）

##### 2. Cloudflare Tunnelインストール
```bash
# NASにSSH接続
ssh AdminUser@192.168.68.110

# cloudflaredインストール
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb

# Cloudflareにログイン
cloudflared tunnel login

# トンネル作成
cloudflared tunnel create meeting-minutes

# 設定ファイル作成
sudo mkdir -p /etc/cloudflared
sudo nano /etc/cloudflared/config.yml
```

##### 3. 設定ファイル内容
```yaml
tunnel: YOUR_TUNNEL_ID
credentials-file: /root/.cloudflared/YOUR_TUNNEL_ID.json

ingress:
  - hostname: meeting-minutes.yourdomain.com
    service: http://localhost:5000
  - service: http_status:404
```

##### 4. DNS設定とサービス起動
```bash
# DNS設定
cloudflared tunnel route dns meeting-minutes meeting-minutes.yourdomain.com

# サービスとして起動
sudo cloudflared service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

##### 5. アクセス
```
https://meeting-minutes.yourdomain.com/
```

---

### 方法3: VPN（WireGuard）

**メリット:**
- ✅ 非常に安全
- ✅ 高速
- ✅ 完全にプライベート
- ✅ NAS全体にアクセス可能

**デメリット:**
- 設定がやや複雑
- ルーター設定が必要

#### 設定手順

##### 1. NAS側にWireGuardインストール
```bash
ssh AdminUser@192.168.68.110

# WireGuardインストール
sudo apt update
sudo apt install wireguard

# 秘密鍵と公開鍵の生成
wg genkey | sudo tee /etc/wireguard/private.key
sudo chmod go= /etc/wireguard/private.key
sudo cat /etc/wireguard/private.key | wg pubkey | sudo tee /etc/wireguard/public.key
```

##### 2. サーバー設定ファイル作成
```bash
sudo nano /etc/wireguard/wg0.conf
```

```ini
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = YOUR_SERVER_PRIVATE_KEY
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey = YOUR_CLIENT_PUBLIC_KEY
AllowedIPs = 10.0.0.2/32
```

##### 3. WireGuard起動
```bash
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0
```

##### 4. ルーター設定
- ルーター管理画面にアクセス
- ポートフォワーディング設定
  - 外部ポート: 51820
  - 内部ポート: 51820
  - プロトコル: UDP
  - 内部IP: 192.168.68.110 (NASのIP)

##### 5. クライアント設定
スマホにWireGuardアプリをインストールして設定

---

## ⚠️ 非推奨な方法（セキュリティリスク高）

### ポートフォワーディングのみ（HTTPS無し）

**絶対に避けるべき理由:**
- ❌ 通信が暗号化されない（パスワード・データが平文で送信）
- ❌ 中間者攻撃のリスク
- ❌ 誰でもアクセス可能

もしこの方法を使う場合は、**必ず以下を実装してください:**

1. **HTTPS化**（Let's Encrypt + Nginx）
2. **Basic認証**
3. **IP制限**
4. **ファイアウォール設定**

---

## 🔐 セキュリティ強化策

### 1. 認証の追加

#### Basic認証（Nginx）
```bash
# Nginxインストール
sudo apt install nginx apache2-utils

# パスワードファイル作成
sudo htpasswd -c /etc/nginx/.htpasswd admin

# Nginx設定
sudo nano /etc/nginx/sites-available/meeting-minutes
```

```nginx
server {
    listen 80;
    server_name meeting-minutes.local;

    location / {
        auth_basic "Restricted Access";
        auth_basic_user_file /etc/nginx/.htpasswd;
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/meeting-minutes /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 2. ファイアウォール設定

```bash
# UFWインストール・設定
sudo apt install ufw

# デフォルトポリシー
sudo ufw default deny incoming
sudo ufw default allow outgoing

# SSH許可
sudo ufw allow ssh

# 特定のIPからのアクセスのみ許可
sudo ufw allow from YOUR_IP_ADDRESS to any port 5000

# 有効化
sudo ufw enable
```

### 3. Fail2Ban（ブルートフォース攻撃対策）

```bash
# Fail2Banインストール
sudo apt install fail2ban

# 設定
sudo nano /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[nginx-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log
```

```bash
sudo systemctl restart fail2ban
```

---

## 📱 モバイルアプリでのアクセス

### iOSショートカット作成
1. ショートカットアプリを開く
2. 新規ショートカット作成
3. 「URLを開く」アクション追加
4. URL: `http://YOUR_TAILSCALE_IP:5000/`
5. ホーム画面に追加

### Android
1. Chromeでアクセス
2. メニュー → ホーム画面に追加

---

## 🔍 トラブルシューティング

### Tailscale接続できない
```bash
# Tailscaleステータス確認
sudo tailscale status

# ログ確認
sudo journalctl -u tailscaled -f

# 再起動
sudo systemctl restart tailscaled
```

### Cloudflare Tunnel接続できない
```bash
# ステータス確認
sudo systemctl status cloudflared

# ログ確認
sudo journalctl -u cloudflared -f

# 設定確認
cloudflared tunnel info meeting-minutes
```

### VPN接続できない
```bash
# WireGuardステータス確認
sudo wg show

# 再起動
sudo wg-quick down wg0
sudo wg-quick up wg0

# ログ確認
sudo journalctl -xe | grep wireguard
```

---

## 💰 コスト比較

| 方法 | 初期費用 | 月額費用 | 年間費用 |
|------|----------|----------|----------|
| Tailscale | 無料 | 無料 | 無料 |
| Cloudflare Tunnel | 無料 | 無料 | 無料 |
| WireGuard VPN | 無料 | 無料 | 無料 |
| ポート開放 + 独自ドメイン | 1,000円 | - | 1,000円 |
| ポート開放 + SSL証明書 | 無料（Let's Encrypt） | 無料 | 無料 |

---

## 🎯 推奨フロー

### 個人利用（最も簡単）
1. **Tailscaleをインストール** → 5分で完了
2. スマホにもTailscaleアプリ
3. いつでもどこでも安全にアクセス

### チーム利用（複数人）
1. **Cloudflare Tunnelを設定** → 30分で完了
2. カスタムドメインでアクセス
3. HTTPSで暗号化済み

### 本格的な運用
1. **VPN + リバースプロキシ**
2. 認証機能追加
3. ログ監視システム導入

---

## 📚 参考リンク

### Tailscale
- [公式サイト](https://tailscale.com/)
- [ドキュメント](https://tailscale.com/kb/)

### Cloudflare Tunnel
- [公式サイト](https://www.cloudflare.com/products/tunnel/)
- [ドキュメント](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/)

### WireGuard
- [公式サイト](https://www.wireguard.com/)
- [ドキュメント](https://www.wireguard.com/quickstart/)

### Let's Encrypt（無料SSL証明書）
- [公式サイト](https://letsencrypt.org/)
- [Certbot](https://certbot.eff.org/)

---

## ⚡ クイックスタート

### 今すぐ始めるなら（5分）

**Tailscaleで始める:**

```bash
# 1. NAS側
ssh AdminUser@192.168.68.110
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# 2. スマホにTailscaleアプリインストール

# 3. 同じアカウントでログイン

# 4. アクセス！
# http://100.x.x.x:5000/
```

**これだけで外部からも安全にアクセス可能！**

---

## 🆘 サポート

外部アクセス設定でお困りの際は：
1. このドキュメントのトラブルシューティングを確認
2. 各サービスの公式ドキュメントを参照
3. GitHubのIssueで質問

**注意**: セキュリティに関する質問は慎重に扱い、機密情報を公開しないでください。

