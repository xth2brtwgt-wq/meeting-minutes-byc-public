"""
設定管理に関する共通ユーティリティ
"""

import os
import json
import yaml
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
    
    def load_config(self, config_name: str, config_type: str = "json") -> Dict[str, Any]:
        """設定ファイルを読み込み"""
        config_file = self.config_dir / f"{config_name}.{config_type}"
        
        if not config_file.exists():
            logger.warning(f"設定ファイルが見つかりません: {config_file}")
            return {}
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                if config_type == "json":
                    config = json.load(f)
                elif config_type == "yaml":
                    config = yaml.safe_load(f)
                else:
                    raise ValueError(f"サポートされていない設定ファイル形式: {config_type}")
            
            self._config_cache[config_name] = config
            return config
            
        except Exception as e:
            logger.error(f"設定ファイル読み込みエラー: {e}")
            return {}
    
    def save_config(self, config_name: str, config_data: Dict[str, Any], config_type: str = "json") -> bool:
        """設定ファイルを保存"""
        config_file = self.config_dir / f"{config_name}.{config_type}"
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                if config_type == "json":
                    json.dump(config_data, f, ensure_ascii=False, indent=2)
                elif config_type == "yaml":
                    yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
                else:
                    raise ValueError(f"サポートされていない設定ファイル形式: {config_type}")
            
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
DEFAULT_CONFIG = {
    "app": {
        "name": "NAS音声文字起こしシステム",
        "version": "1.0.0",
        "debug": False,
        "host": "0.0.0.0",
        "port": 5000
    },
    "whisper": {
        "model": "base",
        "language": "ja",
        "temperature": 0.0,
        "best_of": 5,
        "beam_size": 5
    },
    "audio": {
        "max_file_size": 100 * 1024 * 1024,  # 100MB
        "max_duration": 3600,  # 1時間
        "supported_formats": [".wav", ".mp3", ".m4a", ".flac", ".ogg", ".aac"],
        "sample_rate": 16000
    },
    "storage": {
        "upload_dir": "/tmp/uploads",
        "transcript_dir": "/tmp/transcripts",
        "cleanup_days": 7
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "app.log"
    }
}

def get_default_config() -> Dict[str, Any]:
    """デフォルト設定を取得"""
    return DEFAULT_CONFIG.copy()

def create_default_config_files(config_dir: str = "config"):
    """デフォルト設定ファイルを作成"""
    config_manager = ConfigManager(config_dir)
    
    # アプリケーション設定
    config_manager.save_config("app", DEFAULT_CONFIG["app"])
    
    # Whisper設定
    config_manager.save_config("whisper", DEFAULT_CONFIG["whisper"])
    
    # 音声設定
    config_manager.save_config("audio", DEFAULT_CONFIG["audio"])
    
    # ストレージ設定
    config_manager.save_config("storage", DEFAULT_CONFIG["storage"])
    
    # ログ設定
    config_manager.save_config("logging", DEFAULT_CONFIG["logging"])
    
    logger.info(f"デフォルト設定ファイルを作成しました: {config_dir}")

def load_environment_config() -> Dict[str, Any]:
    """環境変数から設定を読み込み"""
    config = {}
    
    # アプリケーション設定
    config["app"] = {
        "debug": os.getenv("FLASK_DEBUG", "False").lower() == "true",
        "host": os.getenv("FLASK_HOST", "0.0.0.0"),
        "port": int(os.getenv("FLASK_PORT", "5000"))
    }
    
    # Whisper設定
    config["whisper"] = {
        "model": os.getenv("WHISPER_MODEL", "base"),
        "language": os.getenv("WHISPER_LANGUAGE", "ja")
    }
    
    # ストレージ設定
    config["storage"] = {
        "upload_dir": os.getenv("UPLOAD_DIR", "/tmp/uploads"),
        "transcript_dir": os.getenv("TRANSCRIPT_DIR", "/tmp/transcripts")
    }
    
    return config

