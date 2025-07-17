import os
from datetime import datetime


def validate_video_file(file_path):
    """Проверяет существование файла и его расширение"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Video file not found: {file_path}")

    valid_extensions = ['.mp4', '.mov', '.avi', '.mkv']
    ext = os.path.splitext(file_path)[1].lower()

    if ext not in valid_extensions:
        raise ValueError(f"Unsupported video format. Supported formats: {', '.join(valid_extensions)}")

    return True


def generate_video_title(base="Video"):
    """Генерирует название видео с timestamp"""
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{now}"


def format_duration(seconds):
    """Форматирует длительность в HH:MM:SS"""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"