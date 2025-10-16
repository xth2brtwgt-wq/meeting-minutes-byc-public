#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Insta360自動同期システム - メイン同期スクリプト
"""

import os
import sys
import logging
import argparse
from datetime import datetime
from pathlib import Path

# パスを追加してutilsモジュールをインポート可能にする
sys.path.append('/app')
sys.path.append('/app/utils')

from utils.config_utils import ConfigManager, load_environment_config
from utils.file_utils import FileManager, format_file_size
from utils.email_sender import EmailSender

# ログ設定
def setup_logging():
    """ログ設定を初期化"""
    log_dir = Path('/app/logs')
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / 'insta360_sync.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

class Insta360Sync:
    """Insta360自動同期クラス"""
    
    def __init__(self):
        self.logger = setup_logging()
        self.config_manager = ConfigManager('/app/config')
        self.email_sender = EmailSender()
        
        # 設定を読み込み
        self.app_config = self.config_manager.load_config('app')
        self.env_config = load_environment_config()
        
        # 設定値を取得
        self.source_path = self.env_config.get('sync', {}).get('source_path', '/source')
        self.destination_path = self.env_config.get('sync', {}).get('destination_path', '/volume2/data/insta360')
        self.file_patterns = self.app_config.get('sync', {}).get('file_patterns', [
            'VID_*.mp4', '*.insv', '*.insp', '*.jpg', '*.dng', '*.raw'
        ])
        
        # メール設定
        self.to_email = self.env_config.get('email', {}).get('to_email', '')
        self.send_success = self.app_config.get('notification', {}).get('send_success', True)
        self.send_error = self.app_config.get('notification', {}).get('send_error', True)
        self.send_no_files = self.app_config.get('notification', {}).get('send_no_files', False)
        
        self.logger.info("Insta360自動同期システムを初期化しました")
    
    def run_sync(self) -> dict:
        """同期処理を実行"""
        start_time = datetime.now()
        self.logger.info("Insta360ファイル同期を開始します")
        
        try:
            # ファイルマネージャーを初期化
            file_manager = FileManager(
                self.source_path,
                self.destination_path,
                self.file_patterns
            )
            
            # Insta360ファイルを検索
            files = file_manager.find_insta360_files()
            
            if not files:
                self.logger.info("転送対象のInsta360ファイルは見つかりませんでした")
                result = self._create_sync_result(start_time, files, [], [])
                
                if self.send_no_files and self.to_email:
                    self._send_notification(result, "no_files")
                
                return result
            
            self.logger.info(f"転送対象ファイル: {len(files)}件")
            
            # ファイル転送を実行
            success_list, failed_list = self._transfer_files(file_manager, files)
            
            # 結果を作成
            result = self._create_sync_result(start_time, files, success_list, failed_list)
            
            # メール通知を送信
            if self.to_email:
                if success_list and self.send_success:
                    self._send_notification(result, "success")
                elif failed_list and self.send_error:
                    self._send_notification(result, "error")
            
            self.logger.info("Insta360ファイル同期が完了しました")
            return result
            
        except Exception as e:
            self.logger.error(f"同期処理でエラーが発生しました: {e}", exc_info=True)
            
            # エラー通知を送信
            if self.to_email and self.send_error:
                try:
                    self.email_sender.send_error_notification(
                        self.to_email,
                        str(e),
                        f"同期処理中にエラーが発生しました。詳細はログファイルを確認してください。"
                    )
                except Exception as email_error:
                    self.logger.error(f"エラー通知メール送信失敗: {email_error}")
            
            raise
    
    def _transfer_files(self, file_manager: FileManager, files: list) -> tuple:
        """ファイル転送を実行"""
        success_list = []
        failed_list = []
        
        for file_info in files:
            try:
                self.logger.info(f"ファイル転送開始: {file_info['filename']}")
                
                # ファイルをコピー
                copy_success, copy_message = file_manager.copy_file(file_info)
                
                if copy_success:
                    # ソースファイルを削除
                    delete_success, delete_message = file_manager.delete_source_file(file_info)
                    
                    if delete_success:
                        success_list.append({
                            'filename': file_info['filename'],
                            'size': file_info['size'],
                            'message': '転送完了'
                        })
                        self.logger.info(f"ファイル転送完了: {file_info['filename']}")
                    else:
                        failed_list.append({
                            'filename': file_info['filename'],
                            'size': file_info['size'],
                            'error': f"削除失敗: {delete_message}"
                        })
                        self.logger.error(f"ソースファイル削除失敗: {file_info['filename']} - {delete_message}")
                else:
                    failed_list.append({
                        'filename': file_info['filename'],
                        'size': file_info['size'],
                        'error': f"コピー失敗: {copy_message}"
                    })
                    self.logger.error(f"ファイルコピー失敗: {file_info['filename']} - {copy_message}")
                    
            except Exception as e:
                failed_list.append({
                    'filename': file_info['filename'],
                    'size': file_info['size'],
                    'error': str(e)
                })
                self.logger.error(f"ファイル転送エラー: {file_info['filename']} - {e}")
        
        return success_list, failed_list
    
    def _create_sync_result(self, start_time: datetime, files: list, success_list: list, failed_list: list) -> dict:
        """同期結果を作成"""
        end_time = datetime.now()
        total_size = sum(file['size'] for file in files)
        
        return {
            'execution_date': start_time.strftime('%Y/%m/%d'),
            'execution_time': start_time.strftime('%H:%M:%S'),
            'total_files': len(files),
            'total_size': total_size,
            'success_files': len(success_list),
            'failed_files': len(failed_list),
            'success_list': success_list,
            'failed_list': failed_list,
            'duration_seconds': (end_time - start_time).total_seconds(),
            'timestamp': end_time.isoformat()
        }
    
    def _send_notification(self, result: dict, notification_type: str):
        """通知を送信"""
        try:
            if notification_type == "success":
                self.email_sender.send_sync_report(self.to_email, result)
            elif notification_type == "error":
                error_message = f"転送失敗: {result['failed_files']}件"
                error_details = f"成功: {result['success_files']}件, 失敗: {result['failed_files']}件"
                self.email_sender.send_error_notification(self.to_email, error_message, error_details)
            elif notification_type == "no_files":
                # ファイルなし通知（簡易版）
                self.email_sender.send_sync_report(self.to_email, result)
                
        except Exception as e:
            self.logger.error(f"通知送信エラー: {e}")

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='Insta360自動同期システム')
    parser.add_argument('--test', action='store_true', help='テストモードで実行')
    parser.add_argument('--dry-run', action='store_true', help='ドライランモード（実際の転送は行わない）')
    
    args = parser.parse_args()
    
    try:
        sync = Insta360Sync()
        
        if args.test:
            # テストモード
            print("テストモード: 設定確認")
            print(f"ソースパス: {sync.source_path}")
            print(f"転送先パス: {sync.destination_path}")
            print(f"ファイルパターン: {sync.file_patterns}")
            print(f"通知先メール: {sync.to_email}")
            
            # メール接続テスト
            if sync.to_email:
                print("メール接続テスト中...")
                if sync.email_sender.test_connection():
                    print("メール接続テスト: 成功")
                else:
                    print("メール接続テスト: 失敗")
            
            return 0
        
        # 通常の同期処理
        result = sync.run_sync()
        
        # 結果を表示
        print(f"同期完了: 成功 {result['success_files']}件, 失敗 {result['failed_files']}件")
        print(f"総容量: {format_file_size(result['total_size'])}")
        print(f"実行時間: {result['duration_seconds']:.2f}秒")
        
        return 0 if result['failed_files'] == 0 else 1
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
