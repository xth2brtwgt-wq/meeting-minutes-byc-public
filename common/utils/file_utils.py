"""
ファイル操作に関する共通ユーティリティ
"""

import os
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import json
import logging

logger = logging.getLogger(__name__)

class FileManager:
    """ファイル管理クラス"""
    
    def __init__(self, base_path: str = "/tmp"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def create_directory(self, dir_name: str) -> Path:
        """ディレクトリを作成"""
        dir_path = self.base_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path
    
    def save_file(self, file_data: bytes, filename: str, subdir: str = "") -> str:
        """ファイルを保存"""
        if subdir:
            save_dir = self.create_directory(subdir)
        else:
            save_dir = self.base_path
        
        file_path = save_dir / filename
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        return str(file_path)
    
    def get_file_hash(self, file_path: str) -> str:
        """ファイルのハッシュ値を取得"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def cleanup_old_files(self, directory: str, days: int = 7) -> int:
        """古いファイルを削除"""
        import time
        
        dir_path = Path(directory)
        if not dir_path.exists():
            return 0
        
        current_time = time.time()
        deleted_count = 0
        
        for file_path in dir_path.iterdir():
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                if file_age > (days * 24 * 60 * 60):
                    file_path.unlink()
                    deleted_count += 1
                    logger.info(f"削除されたファイル: {file_path}")
        
        return deleted_count

def get_safe_filename(filename: str) -> str:
    """安全なファイル名を生成"""
    import re
    
    # 危険な文字を除去
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # 連続するアンダースコアを単一に
    safe_name = re.sub(r'_+', '_', safe_name)
    
    # 先頭と末尾のアンダースコアを除去
    safe_name = safe_name.strip('_')
    
    return safe_name

def generate_unique_filename(original_filename: str, directory: str = "") -> str:
    """重複しないファイル名を生成"""
    import uuid
    
    name, ext = os.path.splitext(original_filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    
    new_filename = f"{timestamp}_{unique_id}_{name}{ext}"
    return get_safe_filename(new_filename)

def save_json_data(data: Dict[Any, Any], file_path: str) -> bool:
    """JSONデータをファイルに保存"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logger.error(f"JSON保存エラー: {e}")
        return False

def load_json_data(file_path: str) -> Optional[Dict[Any, Any]]:
    """JSONファイルを読み込み"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"JSON読み込みエラー: {e}")
        return None

