from content_generation.promt_generator.gigachat_client import GigaChatClient

def main():
    client = GigaChatClient()

    # Получаем список моделей
    models = client.get_models()
    print("Доступные модели:", models)

    # Отправляем запрос
    response = client.send_prompt("Привет! Как дела?")
    print("Ответ от GigaChat:", response)

if __name__ == "__main__":
    main()