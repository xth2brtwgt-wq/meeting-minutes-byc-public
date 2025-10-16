#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini AI 利用可能モデルの確認スクリプト
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY が設定されていません")
    print("📝 .envファイルにGEMINI_API_KEYを設定してください")
    exit(1)

# Gemini AI の設定
genai.configure(api_key=GEMINI_API_KEY)

print("🔍 利用可能なGemini AIモデルを確認中...")
print("=" * 60)

try:
    # 利用可能なモデル一覧を取得
    models = genai.list_models()
    
    print("📋 利用可能なモデル一覧:")
    print("-" * 60)
    
    for model in models:
        model_name = model.name
        display_name = model.display_name
        supported_methods = model.supported_generation_methods
        
        print(f"🔹 モデル名: {model_name}")
        print(f"   表示名: {display_name}")
        print(f"   サポートメソッド: {', '.join(supported_methods)}")
        
        # generateContentをサポートしているかチェック
        if 'generateContent' in supported_methods:
            print("   ✅ generateContent サポート")
        else:
            print("   ❌ generateContent 非サポート")
        
        print("-" * 60)
    
    print("\n🎯 推奨モデル:")
    print("   - gemini-1.5-flash (高速・軽量)")
    print("   - gemini-1.5-pro (高精度)")
    print("   - gemini-pro (標準)")
    
except Exception as e:
    print(f"❌ エラーが発生しました: {str(e)}")
    print("\n🔧 トラブルシューティング:")
    print("   1. API Keyが正しく設定されているか確認")
    print("   2. インターネット接続を確認")
    print("   3. API Keyの権限を確認")
