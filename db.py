import asyncpg
from config import DATABASE_URL

pool: asyncpg.Pool | None = None


async def create_pool():
    global pool
    pool = await asyncpg.create_pool(dsn=DATABASE_URL)


async def close_pool():
    global pool
    if pool:
        await pool.close()


async def create_tables():
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS surveys (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT NOT NULL,
                telegram_username VARCHAR(255),
                role VARCHAR(50) NOT NULL,
                name VARCHAR(255) NOT NULL,
                is_member BOOLEAN NOT NULL,
                is_sole_owner BOOLEAN NOT NULL,
                debt_period VARCHAR(50) NOT NULL,
                debt_amount VARCHAR(50) NOT NULL,
                actions_taken TEXT[] NOT NULL,
                actions_other VARCHAR(500),
                has_written_response BOOLEAN NOT NULL,
                debtor_data TEXT[] NOT NULL,
                contact_phone VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)


async def save_survey(data: dict) -> int:
    async with pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO surveys (
                telegram_id, telegram_username, role, name,
                is_member, is_sole_owner, debt_period, debt_amount,
                actions_taken, actions_other, has_written_response,
                debtor_data, contact_phone
            ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)
            RETURNING id
        """,
            data["telegram_id"],
            data["telegram_username"],
            data["role"],
            data["name"],
            data["is_member"],
            data["is_sole_owner"],
            data["debt_period"],
            data["debt_amount"],
            data["actions_taken"],
            data.get("actions_other"),
            data["has_written_response"],
            data["debtor_data"],
            data["contact_phone"],
        )
        return row["id"]
