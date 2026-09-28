from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql://loh:loh@db:5432/loh"
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  # 8 hours

    # First superuser seeded on startup
    FIRST_ADMIN_EMAIL: str = "admin@loh.local"
    FIRST_ADMIN_PASSWORD: str = "admin"


settings = Settings()
