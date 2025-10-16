#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Insta360自動同期システム - スケジューラー
"""

import os
import sys
import time
import signal
import logging
from datetime import datetime, timedelta
from pathlib import Path

# パスを追加してutilsモジュールをインポート可能にする
sys.path.append('/app')
sys.path.append('/app/utils')

from utils.config_utils import ConfigManager, load_environment_config

def setup_logging():
    """ログ設定を初期化"""
    log_dir = Path('/app/logs')
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / 'scheduler.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

class Insta360Scheduler:
    """Insta360自動同期スケジューラー"""
    
    def __init__(self):
        self.logger = setup_logging()
        self.running = True
        self.config_manager = ConfigManager('/app/config')
        
        # 設定を読み込み
        self.app_config = self.config_manager.load_config('app')
        self.env_config = load_environment_config()
        
        # スケジュール設定
        self.schedule = self.env_config.get('sync', {}).get('schedule', '0 0 * * *')
        self.script_path = '/app/scripts/sync.py'
        
        # シグナルハンドラーを設定
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        self.logger.info("Insta360自動同期スケジューラーを初期化しました")
        self.logger.info(f"スケジュール: {self.schedule}")
    
    def _signal_handler(self, signum, frame):
        """シグナルハンドラー"""
        self.logger.info(f"シグナル {signum} を受信しました。スケジューラーを停止します。")
        self.running = False
    
    def _parse_cron_schedule(self, cron_schedule):
        """cronスケジュールを解析して次の実行時刻を計算"""
        try:
            # 簡単なcronパーサー（分 時 日 月 曜日）
            parts = cron_schedule.strip().split()
            if len(parts) != 5:
                raise ValueError("cronスケジュールの形式が正しくありません")
            
            minute, hour, day, month, weekday = parts
            
            # 現在時刻を取得
            now = datetime.now()
            
            # 今日の実行時刻を計算
            if minute == '*':
                target_minute = 0
            else:
                target_minute = int(minute)
            
            if hour == '*':
                target_hour = 0
            else:
                target_hour = int(hour)
            
            # 今日の実行時刻
            today_execution = now.replace(
                hour=target_hour,
                minute=target_minute,
                second=0,
                microsecond=0
            )
            
            # 今日の実行時刻が過ぎている場合は明日の実行時刻を返す
            if today_execution <= now:
                next_execution = today_execution + timedelta(days=1)
            else:
                next_execution = today_execution
            
            return next_execution
            
        except Exception as e:
            self.logger.error(f"cronスケジュール解析エラー: {e}")
            # エラーの場合は1時間後に再試行
            return datetime.now() + timedelta(hours=1)
    
    def _wait_until_next_execution(self, next_execution):
        """次の実行時刻まで待機"""
        while self.running:
            now = datetime.now()
            if now >= next_execution:
                return True
            
            # 1分間隔でチェック
            time.sleep(60)
        
        return False
    
    def _run_sync_script(self):
        """同期スクリプトを実行"""
        try:
            self.logger.info("同期スクリプトを実行中...")
            
            # スクリプトを実行
            import subprocess
            result = subprocess.run([
                sys.executable, self.script_path
            ], capture_output=True, text=True, timeout=3600)  # 1時間のタイムアウト
            
            if result.returncode == 0:
                self.logger.info("同期スクリプトが正常に完了しました")
                self.logger.info(f"出力: {result.stdout}")
            else:
                self.logger.error(f"同期スクリプトがエラーで終了しました (終了コード: {result.returncode})")
                self.logger.error(f"エラー出力: {result.stderr}")
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            self.logger.error("同期スクリプトがタイムアウトしました")
            return False
        except Exception as e:
            self.logger.error(f"同期スクリプト実行エラー: {e}")
            return False
    
    def run(self):
        """スケジューラーを実行"""
        self.logger.info("Insta360自動同期スケジューラーを開始します")
        
        while self.running:
            try:
                # 次の実行時刻を計算
                next_execution = self._parse_cron_schedule(self.schedule)
                self.logger.info(f"次回実行予定: {next_execution.strftime('%Y-%m-%d %H:%M:%S')}")
                
                # 次の実行時刻まで待機
                if self._wait_until_next_execution(next_execution):
                    if self.running:  # シグナルで停止されていない場合のみ実行
                        # 同期スクリプトを実行
                        success = self._run_sync_script()
                        
                        if success:
                            self.logger.info("同期処理が正常に完了しました")
                        else:
                            self.logger.error("同期処理でエラーが発生しました")
                
            except Exception as e:
                self.logger.error(f"スケジューラーエラー: {e}", exc_info=True)
                # エラーが発生した場合は1時間後に再試行
                time.sleep(3600)
        
        self.logger.info("Insta360自動同期スケジューラーを停止しました")

def main():
    """メイン関数"""
    try:
        scheduler = Insta360Scheduler()
        scheduler.run()
        return 0
    except KeyboardInterrupt:
        print("スケジューラーが中断されました")
        return 0
    except Exception as e:
        print(f"スケジューラーでエラーが発生しました: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
