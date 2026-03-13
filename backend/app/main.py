import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import engine
from app.exceptions import ForbiddenError, NotFoundError
from app.redis import redis_client
from app.routers import publications, users

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Управление жизненным циклом — подключения к БД и Redis."""
    logger.info("Запуск приложения Trendsee")
    yield
    logger.info("Остановка приложения Trendsee")
    await redis_client.aclose()
    await engine.dispose()


app = FastAPI(
    title="Trendsee",
    description="Сервис ленты публикаций с кэшированием и JWT-авторизацией",
    version="0.1.0",
    lifespan=lifespan,
)


# --- Глобальные обработчики доменных исключений ---

@app.exception_handler(NotFoundError)
async def not_found_handler(request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.detail},
    )


@app.exception_handler(ForbiddenError)
async def forbidden_handler(request, exc: ForbiddenError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": exc.detail},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api")
app.include_router(publications.router, prefix="/api")


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
