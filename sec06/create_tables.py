from core.configs import settings
from core.database import engine


async def create_tables():
    import models.__all_models
    print('Creating tables...')
    
    async with engine.begin() as conn:
        await conn.run_sync(settings.DB_Basemodel.metadata.drop_all)
        await conn.run_sync(settings.DB_Basemodel.metadata.create_all)

    print('Created tables.')

if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())