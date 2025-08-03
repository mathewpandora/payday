#!/bin/bash

echo "🚀 Запуск HayDay в Docker..."

if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "Создайте файл .env с переменными:"
    echo "RUNWAY_API_KEY=your_runway_api_key"
    echo "GIGACHAT_API_KEY=your_gigachat_api_key"
    exit 1
fi

echo "📦 Сборка Docker образа..."
docker-compose build

echo "🔄 Запуск контейнера..."
docker-compose up -d

echo "✅ HayDay запущен!"
echo "📋 Логи: docker-compose logs -f"
echo "🛑 Остановка: docker-compose down" 