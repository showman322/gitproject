from __future__ import annotations

from datetime import datetime
from typing import List, Tuple

import psycopg2
from psycopg2 import sql
from config import DB_CONFIG


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS players (
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS game_sessions (
    id            SERIAL PRIMARY KEY,
    player_id     INTEGER REFERENCES players(id),
    score         INTEGER   NOT NULL,
    level_reached INTEGER   NOT NULL,
    played_at     TIMESTAMP DEFAULT NOW()
);
"""


class Database:
    def __init__(self):
        self.enabled = True
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.conn.autocommit = True
            self.init_schema()
        except Exception as exc:
            self.enabled = False
            self.conn = None
            print("Database is disabled. Check PostgreSQL config:", exc)

    def init_schema(self) -> None:
        if not self.conn:
            return
        with self.conn.cursor() as cur:
            cur.execute(SCHEMA_SQL)

    def get_or_create_player(self, username: str) -> int | None:
        if not self.enabled or not self.conn:
            return None
        username = username.strip()[:50] or "Player"
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING;",
                (username,),
            )
            cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
            row = cur.fetchone()
            return row[0] if row else None

    def save_session(self, username: str, score: int, level_reached: int) -> None:
        if not self.enabled or not self.conn:
            return
        player_id = self.get_or_create_player(username)
        if player_id is None:
            return
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO game_sessions (player_id, score, level_reached)
                VALUES (%s, %s, %s);
                """,
                (player_id, score, level_reached),
            )

    def get_top_scores(self, limit: int = 10) -> List[Tuple[str, int, int, datetime]]:
        if not self.enabled or not self.conn:
            return []
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT p.username, gs.score, gs.level_reached, gs.played_at
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC, gs.level_reached DESC, gs.played_at ASC
                LIMIT %s;
                """,
                (limit,),
            )
            return cur.fetchall()

    def get_personal_best(self, username: str) -> int:
        if not self.enabled or not self.conn:
            return 0
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT COALESCE(MAX(gs.score), 0)
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                WHERE p.username = %s;
                """,
                (username.strip()[:50] or "Player",),
            )
            row = cur.fetchone()
            return int(row[0]) if row and row[0] is not None else 0
