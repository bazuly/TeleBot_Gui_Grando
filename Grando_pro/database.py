import asyncpg
import config


async def setup_db():
    db = await asyncpg.connect(host=config.DB_HOST,
                               port=config.DB_PORT,
                               database=config.DB_NAME,
                               user=config.DB_USER,
                               password=config.DB_PASS)
    return db