# Git学習ガイド - Meeting Minutes BYC プロジェクト

## 🎯 学習目標

このプロジェクトを使って、実践的にGitの使い方を学習します。

## 📋 学習内容

### 第1章: Gitの基本概念
- バージョン管理とは
- リポジトリ、コミット、ブランチの理解
- ローカルとリモートの違い

### 第2章: 基本的な操作
- リポジトリのクローン
- ファイルの修正とコミット
- ブランチの作成と切り替え
- プッシュとプル

### 第3章: コラボレーション
- プルリクエストの作成
- コードレビューの体験
- マージの実行
- コンフリクトの解決

## 🚀 実習課題

### 課題1: ドキュメント改善
**目標**: README_PUBLIC.mdを改善する

**手順**:
1. 新しいブランチを作成
```bash
git checkout -b feature/improve-readme
```

2. README_PUBLIC.mdを編集
3. 変更をコミット
```bash
git add README_PUBLIC.md
git commit -m "Improve README documentation"
```

4. プッシュ
```bash
git push origin feature/improve-readme
```

### 課題2: 新機能の追加
**目標**: 簡単な機能を追加する

**手順**:
1. 新しいブランチを作成
```bash
git checkout -b feature/add-new-feature
```

2. 機能を実装
3. テストを実行
4. 変更をコミット
5. プルリクエストを作成

### 課題3: バグ修正
**目標**: 既存のバグを修正する

**手順**:
1. バグを特定
2. 修正ブランチを作成
3. バグを修正
4. テストを実行
5. プルリクエストを作成

## 🔧 学習環境の準備

### 1. リポジトリのクローン
```bash
git clone https://github.com/xth2brtwgt-wq/meeting-minutes-byc.git
cd meeting-minutes-byc
```

### 2. 環境の確認
```bash
# 現在のブランチを確認
git branch -a

# 公開用ブランチに切り替え
git checkout public
```

### 3. 開発環境の準備
```bash
# 環境変数ファイルを作成
cp meeting-minutes-byc-dev/env.example meeting-minutes-byc-dev/.env

# 必要なAPIキーを設定（学習用）
nano meeting-minutes-byc-dev/.env
```

## 📚 参考資料

- [Git公式ドキュメント](https://git-scm.com/doc)
- [GitHub公式ガイド](https://guides.github.com/)
- [Atlassian Git Tutorial](https://www.atlassian.com/git/tutorials)

## 🎓 学習の進め方

### 初心者向け
1. まずはリポジトリをクローンして中身を確認
2. READMEを読んでプロジェクトを理解
3. 簡単な修正から始める

### 中級者向け
1. ブランチ戦略を理解
2. プルリクエストの作成
3. コードレビューの体験

### 上級者向け
1. 複雑なマージの実行
2. コンフリクトの解決
3. プロジェクトの改善提案

## 🤝 コラボレーション

### プルリクエストの作成
1. 新しいブランチを作成
2. 変更を実装
3. プッシュ
4. GitHubでプルリクエストを作成

### コードレビュー
1. プルリクエストを確認
2. コメントを追加
3. 改善提案を行う
4. 承認または修正要求

## 📞 サポート

質問や問題がある場合は、以下を参照してください：
- プロジェクトのIssues
- GitHub Discussions
- 学習者向けのSlackチャンネル

---

**作成者**: AI Assistant  
**プロジェクト**: Meeting Minutes BYC  
**最終更新**: 2025年10月15日
