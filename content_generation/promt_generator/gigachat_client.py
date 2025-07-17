import requests
from typing import Optional, Dict, Any
from .utils import fetch_access_token

class GigaChatClient:
    """
    Клиент для работы с GigaChat API.
    Автоматически обновляет токен при истечении срока действия.
    """

    def __init__(self):
        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1"
        self.access_token = None
        self.update_token()

    def update_token(self) -> None:
        """Обновляет JWT-токен доступа."""
        self.access_token = fetch_access_token()

    def _make_request(
        self,
        method: str,
        endpoint: str,
        payload: Optional[Dict[str, Any]] = None,
        retry: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Отправляет HTTP-запрос к GigaChat API.
        Если токен истёк, обновляет его и повторяет запрос (1 раз).
        """
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        url = f"{self.base_url}/{endpoint}"

        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                json=payload,
                verify=False  # Отключаем проверку SSL
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401 and retry:
                self.update_token()
                return self._make_request(method, endpoint, payload, retry=False)
            raise

    def send_prompt(self, prompt: str, model: str = "GigaChat") -> Optional[str]:
        """Отправляет текстовый запрос (prompt) и возвращает ответ."""
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = self._make_request("POST", "chat/completions", payload)
        return response["choices"][0]["message"]["content"]

    def get_models(self) -> Optional[Dict[str, Any]]:
        """Получает список доступных моделей."""
        return self._make_request("GET", "models")