import asyncio
from psycopg import AsyncConnection
import os


async def db_requests(request) -> list:
    async with await AsyncConnection.connect(
            host=os.environ["HOST"],
            user=os.environ["USER"],
            password=os.environ['PASSWORD'],
            dbname=os.environ["NAME"],
            ) as conn:

        try:

            async with conn.cursor() as cursor:
                await cursor.execute(request)
                response = await cursor.fetchall()
                return response
        except Exception as _ex:
            print("[INFO] Ошибка в работе PostgreSQL", _ex)
        finally:
            if conn:
                await conn.close()


def main():
    asyncio.run(db_requests())


if __name__ == "__main__":
    main()
