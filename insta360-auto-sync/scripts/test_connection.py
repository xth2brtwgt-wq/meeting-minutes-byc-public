#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Insta360自動同期システム - 接続テストスクリプト
"""

import os
import sys
import logging
from pathlib import Path

# パスを追加してutilsモジュールをインポート可能にする
sys.path.append('/app')
sys.path.append('/app/utils')

from utils.config_utils import ConfigManager, load_environment_config
from utils.email_sender import EmailSender

def setup_logging():
    """ログ設定を初期化"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def test_mac_connection():
    """Mac接続テスト"""
    logger = logging.getLogger(__name__)
    
    try:
        # 環境変数から設定を取得
        env_config = load_environment_config()
        mac_config = env_config.get('mac', {})
        
        mac_ip = mac_config.get('ip_address', '192.168.68.69')
        mac_username = mac_config.get('username', 'Yoshi')
        mac_share = mac_config.get('share_name', 'Yoshi')
        
        logger.info(f"Mac接続テスト開始: {mac_ip}")
        
        # マウントポイントの確認
        mount_point = "/mnt/mac-share"
        source_path = "/source"
        
        if not Path(mount_point).exists():
            logger.error(f"マウントポイントが存在しません: {mount_point}")
            return False
        
        if not Path(source_path).exists():
            logger.error(f"ソースパスが存在しません: {source_path}")
            return False
        
        # マウント状態の確認
        with open('/proc/mounts', 'r') as f:
            mounts = f.read()
            if f"//{mac_ip}/{mac_share}" not in mounts:
                logger.error(f"Mac共有フォルダがマウントされていません: //{mac_ip}/{mac_share}")
                return False
        
        # ディレクトリアクセステスト
        try:
            files = list(Path(source_path).iterdir())
            logger.info(f"ソースパスアクセステスト成功: {len(files)}件のファイル/ディレクトリ")
        except Exception as e:
            logger.error(f"ソースパスアクセステスト失敗: {e}")
            return False
        
        logger.info("Mac接続テスト成功")
        return True
        
    except Exception as e:
        logger.error(f"Mac接続テストエラー: {e}")
        return False

def test_nas_storage():
    """NASストレージテスト"""
    logger = logging.getLogger(__name__)
    
    try:
        # 環境変数から設定を取得
        env_config = load_environment_config()
        sync_config = env_config.get('sync', {})
        
        destination_path = sync_config.get('destination_path', '/volume2/data/insta360')
        
        logger.info(f"NASストレージテスト開始: {destination_path}")
        
        # 転送先ディレクトリの確認
        dest_path = Path(destination_path)
        
        if not dest_path.exists():
            logger.error(f"転送先ディレクトリが存在しません: {destination_path}")
            return False
        
        if not dest_path.is_dir():
            logger.error(f"転送先がディレクトリではありません: {destination_path}")
            return False
        
        # 書き込み権限のテスト
        test_file = dest_path / "test_write_permission.tmp"
        try:
            test_file.write_text("test")
            test_file.unlink()
            logger.info("転送先ディレクトリの書き込み権限テスト成功")
        except Exception as e:
            logger.error(f"転送先ディレクトリの書き込み権限テスト失敗: {e}")
            return False
        
        # ディスク容量の確認
        import shutil
        total, used, free = shutil.disk_usage(destination_path)
        free_gb = free / (1024**3)
        
        logger.info(f"転送先ディスク容量: {free_gb:.2f} GB 空き")
        
        if free_gb < 1.0:  # 1GB未満の場合は警告
            logger.warning("転送先ディスクの空き容量が少なくなっています")
        
        logger.info("NASストレージテスト成功")
        return True
        
    except Exception as e:
        logger.error(f"NASストレージテストエラー: {e}")
        return False

def test_email_connection():
    """メール接続テスト"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("メール接続テスト開始")
        
        email_sender = EmailSender()
        
        if email_sender.test_connection():
            logger.info("メール接続テスト成功")
            return True
        else:
            logger.error("メール接続テスト失敗")
            return False
            
    except Exception as e:
        logger.error(f"メール接続テストエラー: {e}")
        return False

def test_file_patterns():
    """ファイルパターンテスト"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("ファイルパターンテスト開始")
        
        # 設定を読み込み
        config_manager = ConfigManager('/app/config')
        app_config = config_manager.load_config('app')
        
        file_patterns = app_config.get('sync', {}).get('file_patterns', [])
        
        if not file_patterns:
            logger.error("ファイルパターンが設定されていません")
            return False
        
        logger.info(f"設定されたファイルパターン: {file_patterns}")
        
        # パターンの妥当性をチェック
        import fnmatch
        test_files = [
            "VID_20250101_120000.mp4",
            "IMG_20250101_120000.jpg",
            "VID_20250101_120000.insv",
            "IMG_20250101_120000.dng",
            "test.txt"  # マッチしないファイル
        ]
        
        for test_file in test_files:
            matches = any(fnmatch.fnmatch(test_file, pattern) for pattern in file_patterns)
            logger.info(f"ファイル '{test_file}': {'マッチ' if matches else 'マッチしない'}")
        
        logger.info("ファイルパターンテスト成功")
        return True
        
    except Exception as e:
        logger.error(f"ファイルパターンテストエラー: {e}")
        return False

def main():
    """メイン関数"""
    logger = setup_logging()
    
    logger.info("Insta360自動同期システム - 接続テスト開始")
    
    tests = [
        ("Mac接続", test_mac_connection),
        ("NASストレージ", test_nas_storage),
        ("メール接続", test_email_connection),
        ("ファイルパターン", test_file_patterns)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"--- {test_name}テスト ---")
        try:
            result = test_func()
            results.append((test_name, result))
            logger.info(f"{test_name}テスト: {'成功' if result else '失敗'}")
        except Exception as e:
            logger.error(f"{test_name}テストでエラー: {e}")
            results.append((test_name, False))
    
    # 結果サマリー
    logger.info("--- テスト結果サマリー ---")
    success_count = 0
    for test_name, result in results:
        status = "成功" if result else "失敗"
        logger.info(f"{test_name}: {status}")
        if result:
            success_count += 1
    
    total_tests = len(results)
    logger.info(f"テスト結果: {success_count}/{total_tests} 成功")
    
    if success_count == total_tests:
        logger.info("すべてのテストが成功しました")
        return 0
    else:
        logger.error("一部のテストが失敗しました")
        return 1

if __name__ == '__main__':
    sys.exit(main())
