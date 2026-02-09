"""FSM storage backed by PostgreSQL — survives bot restarts."""

import json
import logging
from typing import Any

from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType

import db

logger = logging.getLogger(__name__)


async def create_fsm_table():
    async with db.pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS fsm_states (
                key TEXT PRIMARY KEY,
                state TEXT,
                data TEXT DEFAULT '{}'
            );
        """)


def _make_key(key: StorageKey) -> str:
    return f"{key.bot_id}:{key.chat_id}:{key.user_id}"


class PgStorage(BaseStorage):

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        sk = _make_key(key)
        state_str = state.state if isinstance(state, State) else state
        async with db.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO fsm_states (key, state)
                VALUES ($1, $2)
                ON CONFLICT (key) DO UPDATE SET state = $2
            """, sk, state_str)

    async def get_state(self, key: StorageKey) -> str | None:
        sk = _make_key(key)
        async with db.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT state FROM fsm_states WHERE key = $1", sk
            )
            return row["state"] if row else None

    async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        sk = _make_key(key)
        data_json = json.dumps(data, ensure_ascii=False)
        async with db.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO fsm_states (key, data)
                VALUES ($1, $2)
                ON CONFLICT (key) DO UPDATE SET data = $2
            """, sk, data_json)

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        sk = _make_key(key)
        async with db.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT data FROM fsm_states WHERE key = $1", sk
            )
            if row and row["data"]:
                return json.loads(row["data"])
            return {}

    async def close(self) -> None:
        pass
