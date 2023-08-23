from pydantic import BaseSettings, Field
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    '''General settings used in the application'''

    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://gustavo:gustavo@localhost:5432/fastapi1'
    DBBasemodel = declarative_base()

    class Config:
        case_sensitive = True

settings = Settings()