#!/bin/bash

# Meeting Minutes BYC ドキュメント参照スクリプト
# 使用方法: ./reference-docs.sh [ドキュメント名]

DOCS_DIR="/Users/Yoshi/nas-project"

case "$1" in
    "readme"|"README")
        echo "=== README.md ==="
        cat "$DOCS_DIR/README.md"
        ;;
    "quick"|"quickstart")
        echo "=== QUICK_START_GUIDE.md ==="
        cat "$DOCS_DIR/QUICK_START_GUIDE.md"
        ;;
    "deploy"|"deployment")
        echo "=== DEPLOYMENT_DOCUMENTATION.md ==="
        cat "$DOCS_DIR/DEPLOYMENT_DOCUMENTATION.md"
        ;;
    "trouble"|"troubleshooting")
        echo "=== TROUBLESHOOTING_GUIDE.md ==="
        cat "$DOCS_DIR/TROUBLESHOOTING_GUIDE.md"
        ;;
    "api"|"apikeys")
        echo "=== API_KEYS_SETUP.md ==="
        cat "$DOCS_DIR/API_KEYS_SETUP.md"
        ;;
    "list"|"ls")
        echo "=== 利用可能なドキュメント ==="
        echo "1. README.md - プロジェクト概要"
        echo "2. QUICK_START_GUIDE.md - クイックスタートガイド"
        echo "3. DEPLOYMENT_DOCUMENTATION.md - デプロイメントドキュメント"
        echo "4. TROUBLESHOOTING_GUIDE.md - トラブルシューティングガイド"
        echo "5. API_KEYS_SETUP.md - API キー設定ガイド"
        echo ""
        echo "使用方法: ./reference-docs.sh [ドキュメント名]"
        ;;
    *)
        echo "使用方法: ./reference-docs.sh [ドキュメント名]"
        echo ""
        echo "利用可能なドキュメント:"
        echo "  readme, quick, deploy, trouble, api, list"
        echo ""
        echo "例:"
        echo "  ./reference-docs.sh readme"
        echo "  ./reference-docs.sh quick"
        echo "  ./reference-docs.sh trouble"
        ;;
esac

