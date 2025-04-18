import asyncio
import asyncpg
import logging

class DatabasePool:
    def __init__(self):
        self.db_params = {
            'DB_HOST': '',
            'DB_PORT': 5432,  # PostgreSQL default port
            'DB_NAME': 'safeconnect-db',
            'DB_USER': 'postgres',
            'DB_PASSWORD': 'dhruv2003',
        }
    
        self.connection_pool = None  # Initialize connection pool

    async def connect(self):
        try:
            self.connection_pool = await asyncpg.create_pool(
                host=self.db_params['DB_HOST'],
                port=self.db_params['DB_PORT'],
                user=self.db_params['DB_USER'],
                password=self.db_params['DB_PASSWORD'],
                database=self.db_params['DB_NAME'],
                #min_size=0,
                #max_size=300,
            )
            logging.info("PostgreSQL connection pool created successfully")

        except Exception as e:
            logging.error(f"Failed to create PostgreSQL connection pool: {e}")
            raise

    async def close(self):
        if self.connection_pool:
            await self.connection_pool.close()
            logging.info("PostgreSQL connection pool closed")

    async def get_connection(self):
        if not self.connection_pool:
            await self.connect()
        return await self.connection_pool.acquire()

    async def release_connection(self, connection):
        await self.connection_pool.release(connection)


async def main():
    db = DatabasePool()
    try:
        await db.connect()
        connection = await db.get_connection()
        # Use connection for database operations
        await db.release_connection(connection)

    finally:
        await db.close()

# Run the event loop with the main coroutine
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
