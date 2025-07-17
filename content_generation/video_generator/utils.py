import requests
from pathlib import Path

def safe_filename(text: str, max_length: int = 30) -> str:
    """Создает безопасное имя файла из текста"""
    safe_chars = " _-"
    cleaned = "".join(c for c in text if c.isalnum() or c in safe_chars)
    return cleaned.strip()[:max_length]

def download_file(url: str, filepath: Path):
    """Скачивает файл по URL и сохраняет по указанному пути"""
    response = requests.get(url)
    response.raise_for_status()
    with open(filepath, "wb") as f:
        f.write(response.content)