import asyncpg
import asyncio
from config import DATABASE_URL
from typing import Optional, List, Dict


class Database:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.db_url)
        print("Database connection pool created!")

    async def create_table(self):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    full_name text NOT NULL,
                    username varchar(225) UNIQUE NOT NULL,
                    email varchar(100) UNIQUE NOT NULL,
                    password varchar(255) NOT NULL
                )
            ''')
            print("Table 'users' created successfully!")

    async def add(self, full_name: str, username: str, email: str, password: str) -> List[Dict]:
        async with self.pool.acquire() as conn:
            try:
                await conn.execute(
                    "INSERT INTO users (full_name, username, email, password) VALUES ($1, $2, $3, $4)",
                    full_name,
                    username,
                    email,
                    password
                )
                return [{
                    "fullname": full_name,
                    "username": username,
                    "email": email
                }]
            except asyncpg.UniqueViolationError:
                raise UserAlreadyExistsError("Username or email already exists")

    async def all(self) -> List[Dict]:
        async with self.pool.acquire() as conn:
            users = await conn.fetch("SELECT id, full_name, username, email FROM users")
            return [dict(user) for user in users]
        
    async def get_user_by_id(self, id: int) -> Optional[Dict]:
        async with self.pool.acquire() as conn:
            user = await conn.fetchrow("SELECT id, full_name, username, email FROM users WHERE id = $1", id)
            return dict(user) if user else None

    async def is_exists(self, user_id: int) -> bool:
        async with self.pool.acquire() as conn:
            user = await conn.fetchval("SELECT EXISTS(SELECT 1 FROM users WHERE id = $1)", user_id)
            return user

    async def update(self, id: int, full_name: str, username: str, email: str, password: str) -> bool:
        async with self.pool.acquire() as conn:
            try:
                exists = await conn.fetchval("SELECT EXISTS(SELECT 1 FROM users WHERE id = $1)", id)
                if not exists:
                    return False

                await conn.execute(
                    "UPDATE users SET full_name = $1, username = $2, email = $3, password = $4 WHERE id = $5", 
                    full_name, 
                    username,
                    email,
                    password,
                    id
                )
                return True
            except asyncpg.UniqueViolationError:
                raise UserAlreadyExistsError("Username or email already exists")
            except Exception as e:
                raise DatabaseError(f"Error updating user: {str(e)}")

    async def delete(self, user_id: int) -> bool:
        async with self.pool.acquire() as conn:
            try:
                exists = await conn.fetchval("SELECT EXISTS(SELECT 1 FROM users WHERE id = $1)", user_id)
                if not exists:
                    return False

                await conn.execute("DELETE FROM users WHERE id = $1", user_id)
                return True
            except Exception as e:
                raise DatabaseError(f"Error deleting user: {str(e)}")

    async def close(self):
        if self.pool:
            await self.pool.close()
            print("Database connection pool closed!")


class UserAlreadyExistsError(Exception):
    pass


class DatabaseError(Exception):
    pass


async def main():
    db = Database(DATABASE_URL)
    await db.connect()
    await db.create_table()

    # Example: Add a user
    # await db.add("John Doe", "john_doe", "john.doe@example.com", "securepassword")

    await db.close()


if __name__ == "__main__":
    asyncio.run(main())
