# app/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://admin:admin@localhost/rutacriticadb   "

    class Config:
        env_file = ".env"  # Para cargar variables de entorno desde un archivo .env

settings = Settings()
