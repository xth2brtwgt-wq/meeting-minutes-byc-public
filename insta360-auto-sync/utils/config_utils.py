#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Insta360自動同期システム - 設定管理ユーティリティ
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ConfigManager:
    """設定管理クラス"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._config_cache = {}
    
    def load_config(self, config_name: str) -> Dict[str, Any]:
        """設定ファイルを読み込み"""
        config_file = self.config_dir / f"{config_name}.json"
        
        if not config_file.exists():
            logger.warning(f"設定ファイルが見つかりません: {config_file}")
            return {}
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self._config_cache[config_name] = config
            return config
            
        except Exception as e:
            logger.error(f"設定ファイル読み込みエラー: {e}")
            return {}
    
    def save_config(self, config_name: str, config_data: Dict[str, Any]) -> bool:
        """設定ファイルを保存"""
        config_file = self.config_dir / f"{config_name}.json"
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            
            self._config_cache[config_name] = config_data
            return True
            
        except Exception as e:
            logger.error(f"設定ファイル保存エラー: {e}")
            return False
    
    def get_config_value(self, config_name: str, key: str, default: Any = None) -> Any:
        """設定値の取得"""
        if config_name not in self._config_cache:
            self.load_config(config_name)
        
        config = self._config_cache.get(config_name, {})
        return config.get(key, default)
    
    def set_config_value(self, config_name: str, key: str, value: Any) -> bool:
        """設定値の設定"""
        if config_name not in self._config_cache:
            self.load_config(config_name)
        
        config = self._config_cache.get(config_name, {})
        config[key] = value
        self._config_cache[config_name] = config
        
        return self.save_config(config_name, config)

# デフォルト設定
DEFAULT_APP_CONFIG = {
    "app": {
        "name": "Insta360自動同期システム",
        "version": "1.0.0",
        "timezone": "Asia/Tokyo"
    },
    "sync": {
        "source_path": "/source",
        "destination_path": "/volume2/data/insta360",
        "file_patterns": [
            "VID_*.mp4",
            "*.insv",
            "*.insp", 
            "*.jpg",
            "*.dng",
            "*.raw"
        ],
        "schedule": "0 0 * * *"  # 毎日0時
    },
    "mac": {
        "ip_address": "192.168.68.69",
        "username": "Yoshi",
        "password": "",
        "share_name": "Yoshi"
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "logs/insta360_sync.log",
        "max_days": 30
    }
}

DEFAULT_EMAIL_CONFIG = {
    "smtp": {
        "server": "smtp.gmail.com",
        "port": 587,
        "user": "",
        "password": "",
        "from": ""
    },
    "notification": {
        "to_email": "",
        "send_success": True,
        "send_error": True,
        "send_no_files": False
    }
}

def create_default_config_files(config_dir: str = "config") -> bool:
    """デフォルト設定ファイルを作成"""
    try:
        config_manager = ConfigManager(config_dir)
        
        # アプリケーション設定
        config_manager.save_config("app", DEFAULT_APP_CONFIG)
        
        # メール設定
        config_manager.save_config("email", DEFAULT_EMAIL_CONFIG)
        
        logger.info(f"デフォルト設定ファイルを作成しました: {config_dir}")
        return True
        
    except Exception as e:
        logger.error(f"デフォルト設定ファイル作成エラー: {e}")
        return False

def load_environment_config() -> Dict[str, Any]:
    """環境変数から設定を読み込み"""
    config = {}
    
    # アプリケーション設定
    config["app"] = {
        "debug": os.getenv("DEBUG", "False").lower() == "true",
        "timezone": os.getenv("TZ", "Asia/Tokyo")
    }
    
    # Mac接続設定
    config["mac"] = {
        "ip_address": os.getenv("MAC_IP", "192.168.68.69"),
        "username": os.getenv("MAC_USERNAME", "Yoshi"),
        "password": os.getenv("MAC_PASSWORD", ""),
        "share_name": os.getenv("MAC_SHARE", "Yoshi")
    }
    
    # 同期設定
    config["sync"] = {
        "source_path": os.getenv("SOURCE_PATH", "/source"),
        "destination_path": os.getenv("DESTINATION_PATH", "/volume2/data/insta360"),
        "schedule": os.getenv("SYNC_SCHEDULE", "0 0 * * *")
    }
    
    # メール設定
    config["email"] = {
        "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", "587")),
        "email_user": os.getenv("EMAIL_USER", ""),
        "email_password": os.getenv("EMAIL_PASSWORD", ""),
        "email_from": os.getenv("EMAIL_FROM", ""),
        "to_email": os.getenv("TO_EMAIL", "")
    }
    
    return config
