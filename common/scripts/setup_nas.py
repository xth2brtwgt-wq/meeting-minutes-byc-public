#!/usr/bin/env python3
"""
NAS環境セットアップスクリプト
UGreen DXP2800での環境構築を自動化
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import argparse
import logging

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from common.utils.config_utils import ConfigManager, create_default_config_files

logger = logging.getLogger(__name__)

class NASSetup:
    """NAS環境セットアップクラス"""
    
    def __init__(self, nas_ip: str, username: str, password: str):
        self.nas_ip = nas_ip
        self.username = username
        self.password = password
        self.project_name = "nas-project"
    
    def check_ssh_connection(self) -> bool:
        """SSH接続をテスト"""
        try:
            cmd = f"ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no {self.username}@{self.nas_ip} 'echo SSH接続成功'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"SSH接続テストエラー: {e}")
            return False
    
    def upload_project(self, local_path: str, remote_path: str = "/volume1/docker") -> bool:
        """プロジェクトファイルをNASにアップロード"""
        try:
            # rsyncを使用してファイルを同期
            cmd = f"rsync -avz --progress {local_path}/ {self.username}@{self.nas_ip}:{remote_path}/{self.project_name}/"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("プロジェクトファイルのアップロードが完了しました")
                return True
            else:
                logger.error(f"アップロードエラー: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"アップロードエラー: {e}")
            return False
    
    def setup_docker_on_nas(self) -> bool:
        """NAS上でDocker環境をセットアップ"""
        try:
            # SSH経由でDockerコマンドを実行
            commands = [
                f"cd /volume1/docker/{self.project_name}",
                "docker-compose down",  # 既存のコンテナを停止
                "docker-compose build",  # イメージをビルド
                "docker-compose up -d"   # コンテナを起動
            ]
            
            for cmd in commands:
                ssh_cmd = f"ssh {self.username}@{self.nas_ip} '{cmd}'"
                result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True)
                
                if result.returncode != 0:
                    logger.error(f"コマンド実行エラー: {cmd}")
                    logger.error(f"エラー出力: {result.stderr}")
                    return False
            
            logger.info("Docker環境のセットアップが完了しました")
            return True
            
        except Exception as e:
            logger.error(f"Dockerセットアップエラー: {e}")
            return False
    
    def check_service_status(self) -> bool:
        """サービスの状態を確認"""
        try:
            cmd = f"ssh {self.username}@{self.nas_ip} 'docker-compose -f /volume1/docker/{self.project_name}/docker/compose/docker-compose.yml ps'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("サービス状態:")
                logger.info(result.stdout)
                return True
            else:
                logger.error(f"サービス状態確認エラー: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"サービス状態確認エラー: {e}")
            return False
    
    def run_full_setup(self, local_project_path: str) -> bool:
        """完全なセットアップを実行"""
        logger.info("NAS環境セットアップを開始します...")
        
        # 1. SSH接続テスト
        logger.info("1. SSH接続をテスト中...")
        if not self.check_ssh_connection():
            logger.error("SSH接続に失敗しました。NASの設定を確認してください。")
            return False
        
        # 2. プロジェクトファイルのアップロード
        logger.info("2. プロジェクトファイルをアップロード中...")
        if not self.upload_project(local_project_path):
            logger.error("プロジェクトファイルのアップロードに失敗しました。")
            return False
        
        # 3. Docker環境のセットアップ
        logger.info("3. Docker環境をセットアップ中...")
        if not self.setup_docker_on_nas():
            logger.error("Docker環境のセットアップに失敗しました。")
            return False
        
        # 4. サービス状態の確認
        logger.info("4. サービス状態を確認中...")
        if not self.check_service_status():
            logger.warning("サービス状態の確認に失敗しました。")
        
        logger.info("NAS環境セットアップが完了しました！")
        logger.info(f"Webアプリケーション: http://{self.nas_ip}:5000")
        return True

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="NAS環境セットアップスクリプト")
    parser.add_argument("--nas-ip", required=True, help="NASのIPアドレス")
    parser.add_argument("--username", required=True, help="NASのユーザー名")
    parser.add_argument("--password", help="NASのパスワード（SSH鍵認証の場合は不要）")
    parser.add_argument("--project-path", default=".", help="ローカルプロジェクトパス")
    parser.add_argument("--verbose", "-v", action="store_true", help="詳細ログを表示")
    
    args = parser.parse_args()
    
    # ログ設定
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # セットアップ実行
    setup = NASSetup(args.nas_ip, args.username, args.password)
    success = setup.run_full_setup(args.project_path)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

