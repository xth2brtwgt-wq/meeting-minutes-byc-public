# GitHub認証ガイド

## 🔐 GitでSign in with Appleを使った場合の認証問題

GitでSign in with Appleを使った場合、`git pull`などでパスワードを求められた際は、**Personal Access Token（パーソナルアクセストークン）**を入力する必要があります。

## 🚨 問題の背景

GitHubは2021年からパスワード認証を廃止しており、Personal Access TokenまたはSSH鍵での認証が必須となっています。Sign in with Appleでログインしていても、Git操作には別途トークンが必要です。

## 🔧 解決方法

### 1. Personal Access Tokenを作成

GitHubの場合：
1. GitHub.comにログイン
2. 右上のプロフィールアイコン → **Settings**
3. 左下の **Developer settings**
4. **Personal access tokens** → **Tokens (classic)**
5. **Generate new token** → **Generate new token (classic)**
6. トークンに名前をつけ、必要な権限（最低限`repo`）を選択
7. **Generate token**をクリック
8. **表示されたトークンをコピー**（この画面を閉じると二度と見られません）

### 2. Gitコマンドで使用

```bash
git pull
# Username: あなたのGitHubユーザー名
# Password: （作成したPersonal Access Token）
```

パスワード欄にコピーしたトークンを貼り付けてください。

### 3. 毎回入力しないために（推奨）

**認証情報を保存する：**
```bash
# macOSの場合
git config --global credential.helper osxkeychain

# Windowsの場合
git config --global credential.helper wincred

# Linuxの場合
git config --global credential.helper store
```

一度トークンを入力すれば、次回から自動的に使用されます。

## 🔑 代替案：SSH鍵認証

Personal Access Tokenの代わりにSSH鍵を使用することもできます：

### SSH鍵の生成
```bash
# SSH鍵を生成
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 公開鍵をGitHubに追加
cat ~/.ssh/id_rsa.pub
```

### GitHubにSSH鍵を追加
1. GitHub.com → **Settings** → **SSH and GPG keys**
2. **New SSH key**をクリック
3. 公開鍵の内容を貼り付け
4. **Add SSH key**をクリック

### SSH URLに変更
```bash
# HTTPS URLからSSH URLに変更
git remote set-url origin git@github.com:username/repository.git
```

## 📋 トラブルシューティング

### 認証エラーが続く場合
```bash
# 認証情報をクリア
git config --global --unset credential.helper

# 再設定
git config --global credential.helper osxkeychain
```

### トークンの権限が不足している場合
- GitHubのPersonal Access Token設定で`repo`権限が有効になっているか確認
- 組織のリポジトリの場合は、組織の設定も確認

## 🎯 推奨設定

### セキュリティのベストプラクティス
1. **Personal Access Token**は定期的に更新
2. **最小権限の原則**：必要な権限のみ付与
3. **SSH鍵**の使用を推奨（より安全）
4. **2要素認証**の有効化

### 開発環境での設定
```bash
# グローバル設定
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global credential.helper osxkeychain

# リポジトリ固有の設定
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

## 📚 参考リンク

- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [GitHub SSH Keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Git Credential Helper](https://git-scm.com/book/en/v2/Git-Tools-Credential-Storage)

---

**最終更新**: 2025年10月15日  
**作成者**: AI Assistant  
**プロジェクト**: Meeting Minutes BYC
