from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # PostgreSQL
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "trendsee"
    postgres_password: str = "trendsee_secret"
    postgres_db: str = "trendsee"

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379

    # JWT
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}"
            f":{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}"


settings = Settings()
