#!/usr/bin/env python3
import asyncio
import aiosqlite

DB_NAME = 'users.db'

async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows  # <-- Now explicitly returning

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return rows  # <-- Returning here too

async def fetch_concurrently():
    results_all, results_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All Users:")
    for row in results_all:
        print(row)
    print("Users older than 40:")
    for row in results_older:
        print(row)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
