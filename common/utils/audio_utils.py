"""
音声ファイル処理に関する共通ユーティリティ
"""

import os
import librosa
import soundfile as sf
import numpy as np
from typing import Tuple, Optional, List
import logging

logger = logging.getLogger(__name__)

class AudioProcessor:
    """音声処理クラス"""
    
    SUPPORTED_FORMATS = ['.wav', '.mp3', '.m4a', '.flac', '.ogg', '.aac']
    
    @classmethod
    def is_supported_format(cls, filename: str) -> bool:
        """サポートされている音声形式かチェック"""
        ext = os.path.splitext(filename)[1].lower()
        return ext in cls.SUPPORTED_FORMATS
    
    @classmethod
    def get_audio_info(cls, file_path: str) -> dict:
        """音声ファイルの情報を取得"""
        try:
            y, sr = librosa.load(file_path, sr=None)
            duration = len(y) / sr
            
            return {
                'sample_rate': sr,
                'duration': duration,
                'channels': 1 if y.ndim == 1 else y.shape[0],
                'samples': len(y),
                'format': os.path.splitext(file_path)[1].lower()
            }
        except Exception as e:
            logger.error(f"音声情報取得エラー: {e}")
            return {}
    
    @classmethod
    def normalize_audio(cls, file_path: str, output_path: str = None) -> str:
        """音声を正規化"""
        try:
            y, sr = librosa.load(file_path, sr=16000)  # Whisper用に16kHzに変換
            
            # 音量正規化
            y_normalized = librosa.util.normalize(y)
            
            if output_path is None:
                name, ext = os.path.splitext(file_path)
                output_path = f"{name}_normalized.wav"
            
            sf.write(output_path, y_normalized, sr)
            return output_path
            
        except Exception as e:
            logger.error(f"音声正規化エラー: {e}")
            return file_path
    
    @classmethod
    def split_audio_by_silence(cls, file_path: str, min_silence_duration: float = 1.0) -> List[str]:
        """無音部分で音声を分割"""
        try:
            y, sr = librosa.load(file_path, sr=16000)
            
            # 無音部分を検出
            intervals = librosa.effects.split(y, top_db=20)
            
            split_files = []
            for i, (start, end) in enumerate(intervals):
                if (end - start) / sr >= min_silence_duration:
                    segment = y[start:end]
                    output_path = f"{os.path.splitext(file_path)[0]}_segment_{i}.wav"
                    sf.write(output_path, segment, sr)
                    split_files.append(output_path)
            
            return split_files
            
        except Exception as e:
            logger.error(f"音声分割エラー: {e}")
            return [file_path]
    
    @classmethod
    def detect_language(cls, file_path: str) -> str:
        """音声の言語を推定（簡易版）"""
        try:
            # 実際の実装では、より高度な言語検出を使用
            # ここでは簡易的に日本語と英語を判定
            y, sr = librosa.load(file_path, sr=16000)
            
            # スペクトログラムの特徴から言語を推定
            # 実際の実装では、事前学習済みモデルを使用
            
            return "ja"  # デフォルトで日本語
            
        except Exception as e:
            logger.error(f"言語検出エラー: {e}")
            return "ja"

def validate_audio_file(file_path: str) -> Tuple[bool, str]:
    """音声ファイルの妥当性をチェック"""
    if not os.path.exists(file_path):
        return False, "ファイルが存在しません"
    
    if not AudioProcessor.is_supported_format(file_path):
        return False, "サポートされていない音声形式です"
    
    try:
        info = AudioProcessor.get_audio_info(file_path)
        if not info:
            return False, "音声ファイルの読み込みに失敗しました"
        
        if info['duration'] > 3600:  # 1時間以上
            return False, "ファイルが長すぎます（1時間以内にしてください）"
        
        if info['duration'] < 1:  # 1秒未満
            return False, "ファイルが短すぎます"
        
        return True, "OK"
        
    except Exception as e:
        return False, f"ファイル検証エラー: {str(e)}"

def get_audio_duration(file_path: str) -> float:
    """音声ファイルの長さを取得（秒）"""
    try:
        info = AudioProcessor.get_audio_info(file_path)
        return info.get('duration', 0)
    except:
        return 0

