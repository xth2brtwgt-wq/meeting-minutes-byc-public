#!/usr/bin/env python3
"""
データバックアップスクリプト
音声ファイルと文字起こし結果のバックアップ
"""

import os
import sys
import shutil
import tarfile
import json
from datetime import datetime
from pathlib import Path
import argparse
import logging

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from common.utils.file_utils import FileManager
from common.utils.config_utils import ConfigManager

logger = logging.getLogger(__name__)

class DataBackup:
    """データバックアップクラス"""
    
    def __init__(self, backup_dir: str = "backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.config_manager = ConfigManager()
    
    def create_backup(self, source_dirs: list, backup_name: str = None) -> str:
        """バックアップを作成"""
        if backup_name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"backup_{timestamp}"
        
        backup_path = self.backup_dir / f"{backup_name}.tar.gz"
        
        try:
            with tarfile.open(backup_path, "w:gz") as tar:
                for source_dir in source_dirs:
                    if os.path.exists(source_dir):
                        tar.add(source_dir, arcname=os.path.basename(source_dir))
                        logger.info(f"バックアップに追加: {source_dir}")
                    else:
                        logger.warning(f"ディレクトリが存在しません: {source_dir}")
            
            logger.info(f"バックアップが作成されました: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            logger.error(f"バックアップ作成エラー: {e}")
            return None
    
    def restore_backup(self, backup_path: str, restore_dir: str = ".") -> bool:
        """バックアップから復元"""
        try:
            with tarfile.open(backup_path, "r:gz") as tar:
                tar.extractall(restore_dir)
            
            logger.info(f"バックアップから復元しました: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"復元エラー: {e}")
            return False
    
    def list_backups(self) -> list:
        """バックアップ一覧を取得"""
        backups = []
        for backup_file in self.backup_dir.glob("backup_*.tar.gz"):
            stat = backup_file.stat()
            backups.append({
                'name': backup_file.name,
                'path': str(backup_file),
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime)
            })
        
        # 作成日時でソート（新しい順）
        backups.sort(key=lambda x: x['created'], reverse=True)
        return backups
    
    def cleanup_old_backups(self, days: int = 30) -> int:
        """古いバックアップを削除"""
        import time
        
        current_time = time.time()
        deleted_count = 0
        
        for backup_file in self.backup_dir.glob("backup_*.tar.gz"):
            file_age = current_time - backup_file.stat().st_mtime
            if file_age > (days * 24 * 60 * 60):
                backup_file.unlink()
                deleted_count += 1
                logger.info(f"古いバックアップを削除: {backup_file}")
        
        return deleted_count
    
    def backup_meeting_data(self) -> str:
        """議事録データのバックアップ"""
        # 設定からディレクトリを取得
        storage_config = self.config_manager.load_config("storage")
        upload_dir = storage_config.get("upload_dir", "/tmp/uploads")
        transcript_dir = storage_config.get("transcript_dir", "/tmp/transcripts")
        
        source_dirs = [upload_dir, transcript_dir]
        return self.create_backup(source_dirs, "meeting_data")
    
    def backup_config(self) -> str:
        """設定ファイルのバックアップ"""
        config_dir = self.config_manager.config_dir
        return self.create_backup([str(config_dir)], "config")

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="データバックアップスクリプト")
    parser.add_argument("--action", choices=["create", "restore", "list", "cleanup"], 
                       required=True, help="実行するアクション")
    parser.add_argument("--backup-name", help="バックアップ名")
    parser.add_argument("--backup-path", help="バックアップファイルのパス（復元時）")
    parser.add_argument("--restore-dir", default=".", help="復元先ディレクトリ")
    parser.add_argument("--days", type=int, default=30, help="クリーンアップ対象の日数")
    parser.add_argument("--verbose", "-v", action="store_true", help="詳細ログを表示")
    
    args = parser.parse_args()
    
    # ログ設定
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    backup = DataBackup()
    
    if args.action == "create":
        if args.backup_name == "meeting_data":
            result = backup.backup_meeting_data()
        elif args.backup_name == "config":
            result = backup.backup_config()
        else:
            # カスタムバックアップ
            source_dirs = input("バックアップするディレクトリを入力（カンマ区切り）: ").split(",")
            source_dirs = [d.strip() for d in source_dirs]
            result = backup.create_backup(source_dirs, args.backup_name)
        
        if result:
            print(f"バックアップが作成されました: {result}")
        else:
            print("バックアップの作成に失敗しました")
            sys.exit(1)
    
    elif args.action == "restore":
        if not args.backup_path:
            print("復元するバックアップファイルのパスを指定してください")
            sys.exit(1)
        
        success = backup.restore_backup(args.backup_path, args.restore_dir)
        if success:
            print("復元が完了しました")
        else:
            print("復元に失敗しました")
            sys.exit(1)
    
    elif args.action == "list":
        backups = backup.list_backups()
        if backups:
            print("バックアップ一覧:")
            for backup_info in backups:
                size_mb = backup_info['size'] / (1024 * 1024)
                print(f"  {backup_info['name']} - {size_mb:.2f}MB - {backup_info['created']}")
        else:
            print("バックアップが見つかりません")
    
    elif args.action == "cleanup":
        deleted_count = backup.cleanup_old_backups(args.days)
        print(f"{deleted_count}個の古いバックアップを削除しました")

if __name__ == "__main__":
    main()

