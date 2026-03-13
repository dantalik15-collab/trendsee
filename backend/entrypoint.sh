#!/bin/bash
set -e

echo "Ожидание готовности PostgreSQL..."
max_retries=30
retry_count=0
until python -c "
import asyncio, asyncpg, os
async def check():
    conn = await asyncpg.connect(
        host=os.environ['POSTGRES_HOST'],
        port=int(os.environ['POSTGRES_PORT']),
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        database=os.environ['POSTGRES_DB'],
    )
    await conn.close()
asyncio.run(check())
" 2>/dev/null; do
    retry_count=$((retry_count + 1))
    if [ $retry_count -ge $max_retries ]; then
        echo "PostgreSQL недоступен после $max_retries попыток"
        exit 1
    fi
    echo "PostgreSQL недоступен, повтор через 2 сек... ($retry_count/$max_retries)"
    sleep 2
done
echo "PostgreSQL готов"

echo "Запуск миграций Alembic..."
alembic upgrade head

echo "Проверка наличия данных..."
python -c "
import asyncio, asyncpg, os
async def check():
    conn = await asyncpg.connect(
        host=os.environ['POSTGRES_HOST'],
        port=int(os.environ['POSTGRES_PORT']),
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        database=os.environ['POSTGRES_DB'],
    )
    count = await conn.fetchval('SELECT COUNT(*) FROM publications')
    await conn.close()
    return count
count = asyncio.run(check())
exit(0 if count > 0 else 1)
" && echo "Данные уже есть, пропускаем seed" || {
    echo "База пустая, заполняем тестовыми данными..."
    python -m app.seed
}

echo "Запуск сервера Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000