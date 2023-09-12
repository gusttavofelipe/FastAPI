from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = 'api/v1'
    DB_URL: str = 'postgresql+asyncpg://gustavo:gustavo@localhost:5432/fastapi1'
    DB_Basemodel = declarative_base()

    JWT_SECRET: str = 'XzYuOcnO_selkgIx0dbFu4d8knv44BKynie9_IGsvnU'
    '''
    import secrets

    token: secrets = secrets.token_urlsafe(32)
    '''
    ALGORITHM: str = 'HS256'

    # tempo de expiracao do token de acesso
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

settings: Settings = Settings()