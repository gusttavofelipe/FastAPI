from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from core.configs import settings


# cria conexão async com o db
engine: AsyncEngine = create_async_engine(settings.DB_URL)

# gerencia a engine
Session: AsyncSession = sessionmaker(
    autocomit=False, 
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)