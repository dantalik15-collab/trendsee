FROM python:3.12-slim

WORKDIR /backend

ENV PYTHONPATH=/backend

RUN pip install --no-cache-dir --upgrade pip

COPY pyproject.toml .

# Сначала ставим только зависимости (кэширование Docker-слоёв)
RUN pip install --no-cache-dir .

COPY alembic.ini .
COPY alembic/ alembic/
COPY app/ app/
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
