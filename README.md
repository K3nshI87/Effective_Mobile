# Effective Mobiles - Docker Deployment

Простое веб-приложение с nginx reverse proxy, развёрнутое в Docker-контейнерах.

## Структура проекта

```
├── backend/
│   └── app.py              # FastAPI приложение
├── nginx/
│   └── nginx.conf          # Конфиг nginx (reverse proxy)
├── Dockerfile              # Docker образ для backend
├── docker-compose.yml      # Оркестрация сервисов
├── requirements.txt        # Python зависимости
└── README.md
```

## Как запустить

### Требования
- Docker
- Docker Compose

### Команда запуска

```bash
docker-compose up
```

Контейнеры будут подняты в фоне. Для фонового режима:

```bash
docker-compose up -d
```

## Как проверить результат

Откройте браузер или выполните в терминале:

```bash
curl http://localhost:8000/
```

Ожидаемый ответ:
```
"Hello from Effective Mobile!"
```

Остановка:
```bash
docker-compose down
```

## Как это работает

```
┌─────────────────┐
│   Пользователь │
└────────┬────────┘
         │
    curl :8000/
         │
    ┌────▼───────────────────┐
    │   nginx (порт 8000)    │
    │   - слушает :80        │
    │   - reverse proxy       │
    └────┬───────────────────┘
         │
    proxy_pass http://backend:8080
         │
    ┌────▼──────────────────────────┐
    │   backend (FastAPI)           │
    │   - слушает :8080             │
    │   - не публикует порт наружу   │
    │   - отвечает приложением      │
    └───────────────────────────────┘
```

### Сетевое взаимодействие

- **nginx** и **backend** подключены в одной Docker-сети (`app-network`)
- nginx обращается к backend по имени сервиса: `http://backend:8080`
- Только nginx публикует порт на хост (8000:80)
- backend доступен только из Docker-сети

## Компоненты

### Backend (FastAPI + uvicorn)
- Слушает порт 8080 внутри контейнера
- Отвечает на GET `/` с текстом `"Hello from Effective Mobile!"`
- Запускается автоматически при старте контейнера

### Nginx (reverse proxy)
- Слушает порт 80 внутри контейнера
- Проксирует запросы на backend через `upstream`
- Использует конфиг из `nginx/nginx.conf` (подключается через volume)
- Публикуется на хост-порт 8000

### Docker Compose
- Определяет два сервиса: `backend` и `nginx`
- Создаёт общую сеть для взаимодействия
- Задаёт понятные имена контейнерам
- Пробрасывает только необходимый порт (8000)
