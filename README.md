# HayDay - Автоматическая генерация видео

Проект для автоматической генерации и публикации видео на YouTube.

## Запуск в Docker

### 1. Подготовка

Убедитесь что у вас есть файл `.env` с необходимыми переменными окружения:

```env
RUNWAY_API_KEY=your_runway_api_key
GIGACHAT_API_KEY=your_gigachat_api_key
```

### 2. Запуск

```bash
# Сборка и запуск
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d --build

# Остановка
docker-compose down
```

### 3. Просмотр логов

```bash
docker-compose logs -f
```

## Структура проекта

- `main.py` - основной файл запуска
- `video_processing.py` - обработка видео
- `content_generation/` - генерация контента
- `publications/` - публикация на платформы
- `config/` - конфигурация

## Требования

- Docker
- Docker Compose
- API ключи для Runway и GigaChat

https://dev.runwayml.com/organization/c916252b-13a8-4884-8900-79f8f3c324d8/api-keys