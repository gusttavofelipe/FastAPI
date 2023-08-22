from core.configs import settings
from core.database import engine

# cria tabelas
async def create_tables() -> None:
    import models.__all_models
    print('creating tables in the database...')

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBasemodel.metadata.drop_all)
        await conn.run_sync(settings.DBBasemodel.metadata.create_all)
    print('tables created successfully')

if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())