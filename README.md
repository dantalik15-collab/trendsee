# Trendsee

Сервис ленты публикаций с кэшированием и JWT-авторизацией.  
Тестовое задание — Fullstack-разработчик (Python + Vue.js).

## Стек

- **Backend:** FastAPI, SQLAlchemy (async), PostgreSQL, Redis, Alembic
- **Frontend:** Vue 3 (Composition API), Vite, Axios
- **Инфраструктура:** Docker, docker-compose, Nginx

## Быстрый старт

```bash
git clone <url>
cd trendsee
docker-compose up --build
```

При первом запуске автоматически:
- Поднимаются PostgreSQL, Redis, Backend, Frontend
- Применяются миграции (создаются таблицы)
- База заполняется тестовыми данными (35 публикаций)

После запуска:

| Сервис | URL |
|--------|-----|
| Фронтенд | http://localhost:3000 |
| API | http://localhost:8000 |
| Swagger (документация API) | http://localhost:8000/docs |

## Структура проекта

```
trendsee/
├── docker-compose.yml            # Полный стек (prod)
├── docker-compose.dev.yml        # Только Postgres + Redis (dev)
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml             # Зависимости Python
│   ├── entrypoint.sh              # Миграции + seed + запуск
│   ├── alembic.ini
│   ├── alembic/                   # Миграции БД
│   └── app/
│       ├── main.py                # FastAPI приложение
│       ├── config.py              # Настройки (pydantic-settings)
│       ├── database.py            # SQLAlchemy async engine
│       ├── redis.py               # Redis клиент
│       ├── auth.py                # JWT утилиты
│       ├── exceptions.py          # Доменные исключения
│       ├── dependencies.py        # Dependency Injection
│       ├── seed.py                # Наполнение тестовыми данными
│       ├── models/                # SQLAlchemy модели
│       ├── schemas/               # Pydantic схемы
│       ├── repositories/          # Работа с БД
│       ├── services/              # Бизнес-логика
│       └── routers/               # HTTP эндпоинты
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── vite.config.js
    ├── nginx.conf                 # Проксирование API
    ├── public/assets/             # Статические изображения
    └── src/
        ├── main.js
        ├── App.vue                # Главная страница
        ├── api/                   # HTTP клиент
        ├── composables/           # Логика infinite scroll
        └── components/
            ├── AppSidebar.vue     # Сайдбар навигации
            ├── VideoCard.vue      # Карточка публикации
            ├── AnalysisPanel.vue  # Панель анализа (оверлей)
            └── LoadingSpinner.vue # Индикатор загрузки
```

## Архитектура backend

Трёхслойная архитектура: **Router → Service → Repository**.

- **Router** — принимает HTTP-запросы, валидирует данные, вызывает сервисы
- **Service** — бизнес-логика, кэширование, проверка прав доступа
- **Repository** — запросы к БД через SQLAlchemy

Все зависимости внедряются через FastAPI `Depends()`.  
Доменные исключения (`NotFoundError`, `ForbiddenError`) обрабатываются глобально в `main.py`.

## API эндпоинты

### Пользователи

| Метод  | URL                      | Описание                     | Авторизация |
|--------|--------------------------|------------------------------|-------------|
| POST   | `/api/users`             | Создать пользователя         | —           |
| GET    | `/api/users/{id}/token`  | Получить токен по ID         | —           |
| PATCH  | `/api/users/me`          | Изменить имя                 | JWT         |
| DELETE | `/api/users/me`          | Удалить пользователя         | JWT         |

### Публикации

| Метод  | URL                             | Описание                          | Авторизация |
|--------|---------------------------------|-----------------------------------|-------------|
| POST   | `/api/publications`             | Создать публикацию                | JWT         |
| GET    | `/api/publications`             | Список публикаций (пагинация)     | —           |
| GET    | `/api/publications/{id}`        | Получить публикацию               | —           |
| PATCH  | `/api/publications/{id}`        | Обновить публикацию               | JWT (автор) |
| DELETE | `/api/publications/{id}`        | Удалить публикацию                | JWT (автор) |

### Параметры пагинации

- `limit` (default: 20, max: 100) — количество записей
- `offset` (default: 0) — смещение
- `user_id` (опционально) — фильтр по автору

## Кэширование (Redis)

Публикации считаются «горячими» первые 10 минут после создания:

- При создании — публикация сохраняется в Redis (TTL: 600 сек)
- При запросе по ID — сначала Redis, затем Postgres
- При чтении из Postgres — искусственная задержка 2 секунды (имитация нагрузки)
- При обновлении/удалении — кэш инвалидируется

## JWT-авторизация

Упрощённая модель без пароля (по условию задания):

- При создании пользователя возвращается JWT-токен
- Токен можно получить по ID пользователя (для тестирования)
- Токен передаётся в заголовке: `Authorization: Bearer <token>`
- Редактировать/удалять публикацию может только её автор

## Frontend

Интерфейс реализован по макету из Figma:

- **Сетка видео-карточек** — данные из API, сайдбар навигации
- **Панель анализа** — появляется поверх по клику «Анализ», подставляет данные публикации
- **Infinite scroll** — подгрузка при скролле за 500px до конца страницы
- **Индикатор загрузки** — отображается во время запроса
- **Vue Transition** — анимация появления/скрытия панели анализа

## Локальная разработка

```bash
# Поднять Postgres + Redis
docker-compose -f docker-compose.dev.yml up -d

# Backend
cd backend
pip install -e .
cp .env.example .env
alembic upgrade head
python -m app.seed          # наполнить тестовыми данными
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev                 # http://localhost:3000
```