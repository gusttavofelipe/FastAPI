# arquivo de configuracoes do db

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://gustavo:gustavo@localhost:5432/fastapi1'

    class Config:
        case_sensitive = True


settings: Settings = Settings()
