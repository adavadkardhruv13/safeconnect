from .db import get_pool

async def get_db():
    async with (await get_pool()).acquire() as connection:
        yield connection