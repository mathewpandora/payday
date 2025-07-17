import os
import requests
from uuid import uuid4
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

def get_auth_key() -> str:
    """Получает ключ авторизации из .env."""
    auth_key = os.getenv("GIGACHAT_AUTH_KEY")
    if not auth_key:
        raise ValueError("GIGACHAT_AUTH_KEY не найден в .env!")
    return auth_key

def generate_rquid() -> str:
    """Генерирует уникальный RqUID для запроса."""
    return str(uuid4())

def fetch_access_token() -> str:
    """Получает новый JWT-токен от GigaChat API."""
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": generate_rquid(),
        "Authorization": f"Basic {get_auth_key()}"
    }
    payload = {"scope": "GIGACHAT_API_PERS"}

    try:
        # Добавляем параметр verify=False для игнорирования SSL-ошибок
        response = requests.post(url, headers=headers, data=payload, verify=False)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении токена: {e}")
        raise